"""
Audio Cache Manager for Google Cloud Storage

Manages caching of TTS-generated audio files in Google Cloud Storage.
- On-demand caching: Generate and upload on first request
- Cache retrieval: Download cached audio for subsequent requests
- Age-based cleanup: Delete files older than 30 days (manual trigger)
- Cache statistics: Track usage and storage

Cost-effective solution for podcast, study guide, and lesson plan audio.
"""

import os
import logging
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List, Tuple
from pathlib import Path
from google.cloud import storage
from google.api_core.exceptions import NotFound

logger = logging.getLogger(__name__)


class AudioCacheManager:
    """Manages audio file caching in Google Cloud Storage"""
    
    def __init__(self, bucket_name: str = None):
        """
        Initialize Audio Cache Manager
        
        Args:
            bucket_name: GCS bucket name (defaults to BUCKET_NAME env var)
        """
        self.bucket_name = bucket_name or os.getenv('BUCKET_NAME')
        if not self.bucket_name:
            raise ValueError("BUCKET_NAME environment variable required")
        
        try:
            self.client = storage.Client()
            self.bucket = self.client.bucket(self.bucket_name)
            logger.info(f"✅ Audio Cache Manager initialized with bucket: {self.bucket_name}")
        except Exception as e:
            logger.error(f"❌ Failed to initialize Audio Cache Manager: {e}")
            raise
    
    def _get_cache_key(
        self,
        content_type: str,
        week_number: int = None,
        study_level: str = None,
        audience: str = None,
        voice: str = None,
        voices: Dict[str, str] = None,
        script_hash: str = None
    ) -> str:
        """
        Generate cache key (GCS blob path) for audio file
        
        Content types and their cache keys:
        - podcast: audio-cache/podcast/podcast_week_01_essential.mp3
        - study_guide: audio-cache/study_guide/study_guide_week_01_essential_alnilam.mp3
        - lesson_plan: audio-cache/lesson_plan/lesson_plan_week_01_adult_aoede.mp3
        - core_content: audio-cache/core_content/core_content_week_01_alnilam.mp3
        - daily_thoughts: audio-cache/daily_thoughts/daily_thoughts_week_01_alnilam.mp3
        
        Args:
            content_type: Type of content (podcast, study_guide, lesson_plan, etc.)
            week_number: CFM week number (1-52)
            study_level: Study level (essential, connected, scholarly)
            audience: Lesson plan audience (adult, youth, children)
            voice: Single voice for TTS (alnilam, aoede, etc.)
            voices: Voice mapping for multi-speaker ({"Sarah": "aoede", "David": "alnilam"})
            script_hash: Optional hash of script content for additional uniqueness
            
        Returns:
            GCS blob path for cache file
        """
        # Base path
        base_path = f"audio-cache/{content_type}"
        
        if content_type == "podcast":
            # Podcasts: week + study_level (voices are fixed in JSON)
            filename = f"podcast_week_{week_number:02d}_{study_level}.mp3"
            
        elif content_type == "study_guide":
            # Study guides: week + study_level + voice
            filename = f"study_guide_week_{week_number:02d}_{study_level}_{voice}.mp3"
            
        elif content_type == "lesson_plan":
            # Lesson plans: week + audience + voice
            filename = f"lesson_plan_week_{week_number:02d}_{audience}_{voice}.mp3"
            
        elif content_type == "core_content":
            # Core content: week + voice
            filename = f"core_content_week_{week_number:02d}_{voice}.mp3"
            
        elif content_type == "daily_thoughts":
            # Daily thoughts: week + voice
            filename = f"daily_thoughts_week_{week_number:02d}_{voice}.mp3"
            
        else:
            # Generic TTS (chat Q&A): content_hash + voice
            if not script_hash:
                raise ValueError("script_hash required for generic content_type")
            filename = f"{content_type}_{script_hash[:16]}_{voice}.mp3"
        
        return f"{base_path}/{filename}"
    
    def check_cache(self, cache_key: str) -> bool:
        """
        Check if audio file exists in cache
        
        Args:
            cache_key: GCS blob path
            
        Returns:
            True if file exists in cache, False otherwise
        """
        try:
            blob = self.bucket.blob(cache_key)
            exists = blob.exists()
            
            if exists:
                logger.info(f"✅ Cache HIT: {cache_key}")
            else:
                logger.info(f"❌ Cache MISS: {cache_key}")
            
            return exists
            
        except Exception as e:
            logger.error(f"Error checking cache for {cache_key}: {e}")
            return False
    
    def get_cached_audio(self, cache_key: str) -> Optional[bytes]:
        """
        Download cached audio file from GCS
        
        Args:
            cache_key: GCS blob path
            
        Returns:
            Audio bytes if found, None otherwise
        """
        try:
            blob = self.bucket.blob(cache_key)
            
            if not blob.exists():
                logger.info(f"Cache miss: {cache_key}")
                return None
            
            # Download audio bytes
            audio_bytes = blob.download_as_bytes()
            file_size_mb = len(audio_bytes) / 1024 / 1024
            
            logger.info(f"✅ Downloaded cached audio: {cache_key} ({file_size_mb:.2f}MB)")
            return audio_bytes
            
        except NotFound:
            logger.info(f"Cache miss: {cache_key}")
            return None
        except Exception as e:
            logger.error(f"Error downloading cached audio {cache_key}: {e}")
            return None
    
    def upload_to_cache(self, cache_key: str, audio_bytes: bytes) -> bool:
        """
        Upload audio file to cache
        
        Args:
            cache_key: GCS blob path
            audio_bytes: Audio file bytes
            
        Returns:
            True if upload successful, False otherwise
        """
        try:
            blob = self.bucket.blob(cache_key)
            
            # Set metadata
            blob.metadata = {
                'created_at': datetime.utcnow().isoformat(),
                'content_type': 'audio/mpeg',
                'cache_version': '1.0'
            }
            
            # Upload with content type
            blob.upload_from_string(
                audio_bytes,
                content_type='audio/mpeg'
            )
            
            file_size_mb = len(audio_bytes) / 1024 / 1024
            logger.info(f"✅ Uploaded to cache: {cache_key} ({file_size_mb:.2f}MB)")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading to cache {cache_key}: {e}")
            return False
    
    def get_cache_stats(self) -> Dict:
        """
        Get cache statistics
        
        Returns:
            Dictionary with cache statistics
        """
        try:
            stats = {
                'total_files': 0,
                'total_size_mb': 0.0,
                'oldest_file_age_days': 0,
                'newest_file_age_days': 0,
                'files_over_30_days': 0,
                'by_type': {}
            }
            
            # List all blobs in audio-cache/
            blobs = list(self.bucket.list_blobs(prefix='audio-cache/'))
            
            if not blobs:
                logger.info("Cache is empty")
                return stats
            
            now = datetime.utcnow()
            oldest_date = now
            newest_date = datetime.min.replace(tzinfo=None)
            
            for blob in blobs:
                # Skip directories
                if blob.name.endswith('/'):
                    continue
                
                stats['total_files'] += 1
                stats['total_size_mb'] += blob.size / 1024 / 1024
                
                # Track by content type
                content_type = blob.name.split('/')[1] if '/' in blob.name else 'unknown'
                if content_type not in stats['by_type']:
                    stats['by_type'][content_type] = {'count': 0, 'size_mb': 0.0}
                
                stats['by_type'][content_type]['count'] += 1
                stats['by_type'][content_type]['size_mb'] += blob.size / 1024 / 1024
                
                # Check age
                created_at = blob.time_created.replace(tzinfo=None)
                age_days = (now - created_at).days
                
                if age_days > 30:
                    stats['files_over_30_days'] += 1
                
                if created_at < oldest_date:
                    oldest_date = created_at
                if created_at > newest_date:
                    newest_date = created_at
            
            # Calculate age ranges
            if stats['total_files'] > 0:
                stats['oldest_file_age_days'] = (now - oldest_date).days
                stats['newest_file_age_days'] = (now - newest_date).days
            
            # Round sizes
            stats['total_size_mb'] = round(stats['total_size_mb'], 2)
            for content_type in stats['by_type']:
                stats['by_type'][content_type]['size_mb'] = round(
                    stats['by_type'][content_type]['size_mb'], 2
                )
            
            logger.info(f"📊 Cache stats: {stats['total_files']} files, {stats['total_size_mb']}MB")
            return stats
            
        except Exception as e:
            logger.error(f"Error getting cache stats: {e}")
            return {'error': str(e)}
    
    def cleanup_old_files(self, max_age_days: int = 30) -> Dict:
        """
        Delete cache files older than specified age
        
        Args:
            max_age_days: Maximum age in days (default: 30)
            
        Returns:
            Dictionary with cleanup results
        """
        try:
            result = {
                'deleted_files': 0,
                'freed_mb': 0.0,
                'kept_files': 0,
                'oldest_remaining_age_days': 0,
                'deleted_file_list': []
            }
            
            now = datetime.utcnow()
            cutoff_date = now - timedelta(days=max_age_days)
            
            # List all blobs in audio-cache/
            blobs = list(self.bucket.list_blobs(prefix='audio-cache/'))
            
            oldest_remaining = now
            
            for blob in blobs:
                # Skip directories
                if blob.name.endswith('/'):
                    continue
                
                created_at = blob.time_created.replace(tzinfo=None)
                
                if created_at < cutoff_date:
                    # Delete old file
                    file_size_mb = blob.size / 1024 / 1024
                    result['deleted_files'] += 1
                    result['freed_mb'] += file_size_mb
                    result['deleted_file_list'].append({
                        'name': blob.name,
                        'age_days': (now - created_at).days,
                        'size_mb': round(file_size_mb, 2)
                    })
                    
                    blob.delete()
                    logger.info(f"🗑️  Deleted old cache file: {blob.name} (age: {(now - created_at).days} days)")
                else:
                    # Keep file
                    result['kept_files'] += 1
                    if created_at < oldest_remaining:
                        oldest_remaining = created_at
            
            # Calculate oldest remaining file age
            if result['kept_files'] > 0:
                result['oldest_remaining_age_days'] = (now - oldest_remaining).days
            
            result['freed_mb'] = round(result['freed_mb'], 2)
            
            logger.info(
                f"🧹 Cleanup complete: Deleted {result['deleted_files']} files, "
                f"freed {result['freed_mb']}MB, kept {result['kept_files']} files"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error during cache cleanup: {e}")
            return {'error': str(e)}
    
    def clear_all_cache(self) -> Dict:
        """
        Delete all cached audio files (nuclear option)
        
        Returns:
            Dictionary with clear results
        """
        try:
            result = {
                'deleted_files': 0,
                'freed_mb': 0.0
            }
            
            # List all blobs in audio-cache/
            blobs = list(self.bucket.list_blobs(prefix='audio-cache/'))
            
            for blob in blobs:
                # Skip directories
                if blob.name.endswith('/'):
                    continue
                
                file_size_mb = blob.size / 1024 / 1024
                result['deleted_files'] += 1
                result['freed_mb'] += file_size_mb
                
                blob.delete()
                logger.info(f"🗑️  Deleted cache file: {blob.name}")
            
            result['freed_mb'] = round(result['freed_mb'], 2)
            
            logger.info(
                f"💣 Cache cleared: Deleted {result['deleted_files']} files, "
                f"freed {result['freed_mb']}MB"
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error clearing cache: {e}")
            return {'error': str(e)}


# Factory function
def create_audio_cache_manager() -> Optional[AudioCacheManager]:
    """
    Factory function to create AudioCacheManager instance
    
    Returns:
        AudioCacheManager instance or None if initialization fails
    """
    try:
        manager = AudioCacheManager()
        return manager
    except Exception as e:
        logger.error(f"Failed to create Audio Cache Manager: {e}")
        return None
