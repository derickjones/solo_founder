"""
Google Cloud Text-to-Speech (TTS) Service using Vertex AI Chirp 3 HD Voices

This module provides high-quality, cost-effective text-to-speech conversion
using Google Cloud's Vertex AI with Chirp 3 HD voices.

Pricing: ~$0.016/1000 characters (vs ElevenLabs $0.30/1000)
Quality: Excellent with Chirp 3 HD voices
"""

import os
import re
import logging
import base64
import hashlib
from typing import Optional, Dict
from google.cloud import texttospeech

logger = logging.getLogger(__name__)

# Import audio cache manager (will be initialized in factory function)
try:
    from .audio_cache import AudioCacheManager
    AUDIO_CACHE_AVAILABLE = True
except ImportError:
    AUDIO_CACHE_AVAILABLE = False
    logger.warning("Audio cache not available - will generate TTS without caching")


def clean_text_for_tts(text: str) -> str:
    """
    Clean text for TTS by removing or replacing characters that cause issues.
    
    Removes:
    - Pilcrow/paragraph marks (¶) - TTS reads as "paragraph mark"
    - Other special unicode symbols
    - Markdown formatting characters
    - Multiple consecutive spaces/newlines
    
    Converts:
    - Scripture references to natural speech (Moses 1:12–26 -> Moses chapter 1, verses 12 through 26)
    """
    if not text:
        return text
    
    # Characters to remove completely
    remove_chars = [
        '¶',      # Pilcrow/paragraph mark
        '§',      # Section sign
        '†',      # Dagger
        '‡',      # Double dagger
        '•',      # Bullet (sometimes read aloud)
        '◦',      # White bullet
        '‣',      # Triangular bullet
        '⁃',      # Hyphen bullet
        '※',      # Reference mark
        '⁂',      # Asterism
        '⁕',      # Flower punctuation
        '⁎',      # Low asterisk
        '⁑',      # Two asterisks
    ]
    
    for char in remove_chars:
        text = text.replace(char, '')
    
    # Convert scripture references to natural speech
    # Handles: Moses 1:12–26, Genesis 3:1-5, D&C 88:118, 1 Nephi 3:7, etc.
    
    # Pattern for verse ranges: Book Chapter:Verse–Verse or Book Chapter:Verse-Verse
    # Examples: Moses 1:12–26, Genesis 3:1-5, Alma 32:21-23
    text = re.sub(
        r'(\d?\s?[A-Za-z&]+(?:\s[A-Za-z]+)?)\s*(\d+):(\d+)[–\-](\d+)',
        r'\1 chapter \2, verses \3 through \4',
        text
    )
    
    # Pattern for single verses: Book Chapter:Verse
    # Examples: Moses 1:12, John 3:16, D&C 88:118
    text = re.sub(
        r'(\d?\s?[A-Za-z&]+(?:\s[A-Za-z]+)?)\s*(\d+):(\d+)(?![–\-\d])',
        r'\1 chapter \2, verse \3',
        text
    )
    
    # Replace markdown bold/italic markers with nothing
    text = re.sub(r'\*\*([^*]+)\*\*', r'\1', text)  # **bold** -> bold
    text = re.sub(r'\*([^*]+)\*', r'\1', text)      # *italic* -> italic
    text = re.sub(r'__([^_]+)__', r'\1', text)      # __bold__ -> bold
    text = re.sub(r'_([^_]+)_', r'\1', text)        # _italic_ -> italic
    
    # Remove markdown headers but keep text
    text = re.sub(r'^#{1,6}\s*', '', text, flags=re.MULTILINE)  # ### Header -> Header
    
    # Clean up multiple spaces and newlines
    text = re.sub(r' +', ' ', text)           # Multiple spaces -> single space
    text = re.sub(r'\n{3,}', '\n\n', text)    # 3+ newlines -> 2 newlines
    
    return text.strip()


class GoogleCloudTTS:
    """Google Cloud Text-to-Speech client using Chirp 3 HD voices"""
    
    # Chirp 3 HD voice options - high quality voices
    # Format: voice_name -> (language_code, voice_name)
    VOICE_OPTIONS = {
        # Male voices (top picks)
        "alnilam": ("en-US", "en-US-Chirp3-HD-Alnilam"),
        "achird": ("en-US", "en-US-Chirp3-HD-Achird"),
        "enceladus": ("en-US", "en-US-Chirp3-HD-Enceladus"),
        # Female voices (top picks)
        "aoede": ("en-US", "en-US-Chirp3-HD-Aoede"),
        "autonoe": ("en-US", "en-US-Chirp3-HD-Autonoe"),
        "erinome": ("en-US", "en-US-Chirp3-HD-Erinome"),
        # Defaults for CFM
        "cfm_male": ("en-US", "en-US-Chirp3-HD-Alnilam"),
        "cfm_female": ("en-US", "en-US-Chirp3-HD-Aoede"),
    }
    
    def __init__(self, cache_manager: Optional['AudioCacheManager'] = None):
        """
        Initialize Google Cloud TTS client
        
        Args:
            cache_manager: Optional AudioCacheManager for caching support
        """
        try:
            self.client = texttospeech.TextToSpeechClient()
            self.default_voice = "cfm_male"
            self.cache_manager = cache_manager
            
            if self.cache_manager:
                logger.info("✅ Google Cloud TTS client initialized with caching enabled")
            else:
                logger.info("✅ Google Cloud TTS client initialized (no caching)")
        except Exception as e:
            logger.error(f"Failed to initialize Google Cloud TTS client: {e}")
            raise
    
    def test_connection(self) -> bool:
        """Test if Google Cloud TTS is accessible"""
        try:
            # List available voices to verify connection
            request = texttospeech.ListVoicesRequest(language_code="en-US")
            response = self.client.list_voices(request=request)
            voice_count = len(response.voices)
            logger.info(f"✅ Google Cloud TTS connection successful - {voice_count} voices available")
            return True
        except Exception as e:
            logger.error(f"❌ Google Cloud TTS connection failed: {e}")
            return False
    
    def get_voice_config(self, voice: Optional[str] = None) -> tuple:
        """Get voice configuration (language_code, voice_name)"""
        voice_key = (voice or self.default_voice).lower()
        
        if voice_key in self.VOICE_OPTIONS:
            return self.VOICE_OPTIONS[voice_key]
        
        # Default to cfm_male if voice not found
        logger.warning(f"Voice '{voice}' not found, using default cfm_male")
        return self.VOICE_OPTIONS["cfm_male"]
    
    def chunk_text_smartly(self, text: str, max_length: int = 4500) -> list:
        """
        Split text into chunks that respect sentence boundaries.
        Google Cloud TTS has a 5000 byte limit per request.
        """
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by sentences
        sentences = text.replace('\n\n', ' ¶ ').split('. ')
        
        for i, sentence in enumerate(sentences):
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Add period back except for last sentence
            if i < len(sentences) - 1 and not sentence.endswith(('!', '?', '¶')):
                sentence += '.'
            
            # Replace paragraph markers
            sentence = sentence.replace(' ¶ ', '\n\n')
            
            # Check if adding this sentence would exceed limit
            if current_chunk and len(current_chunk + ' ' + sentence) > max_length:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
            else:
                current_chunk += (' ' + sentence if current_chunk else sentence)
        
        # Add final chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        logger.info(f"Split text into {len(chunks)} chunks for Google Cloud TTS")
        return chunks
    
    def generate_audio(
        self,
        text: str,
        voice: Optional[str] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0
    ) -> Optional[bytes]:
        """
        Generate audio from text using Google Cloud TTS
        
        Args:
            text: Text to convert to speech
            voice: Voice name to use (see VOICE_OPTIONS)
            speaking_rate: Speed of speech (0.25 to 4.0, default 1.0)
            pitch: Voice pitch adjustment (-20.0 to 20.0, default 0.0)
            
        Returns:
            Audio bytes in MP3 format or None if failed
        """
        try:
            # Clean text before processing
            text = clean_text_for_tts(text)
            
            language_code, voice_name = self.get_voice_config(voice)
            
            # Handle text chunking for long content
            chunks = self.chunk_text_smartly(text)
            audio_segments = []
            
            for i, chunk in enumerate(chunks):
                logger.info(f"Generating audio for chunk {i+1}/{len(chunks)} ({len(chunk)} chars)")
                
                try:
                    # Set up synthesis input
                    synthesis_input = texttospeech.SynthesisInput(text=chunk)
                    
                    # Configure voice
                    voice_config = texttospeech.VoiceSelectionParams(
                        language_code=language_code,
                        name=voice_name
                    )
                    
                    # Configure audio output
                    audio_config = texttospeech.AudioConfig(
                        audio_encoding=texttospeech.AudioEncoding.MP3,
                        speaking_rate=speaking_rate,
                        pitch=pitch
                    )
                    
                    # Generate speech
                    response = self.client.synthesize_speech(
                        input=synthesis_input,
                        voice=voice_config,
                        audio_config=audio_config
                    )
                    
                    audio_segments.append(response.audio_content)
                    
                except Exception as e:
                    logger.error(f"Failed to generate audio for chunk {i+1}: {e}")
                    return None
            
            # Combine audio segments
            if len(audio_segments) == 1:
                combined_audio = audio_segments[0]
            else:
                # Simple concatenation for MP3 segments
                combined_audio = b''.join(audio_segments)
            
            logger.info(f"✅ Successfully generated {len(combined_audio)} bytes of audio")
            return combined_audio
            
        except Exception as e:
            logger.error(f"Google Cloud TTS audio generation failed: {e}")
            return None
    
    def generate_audio_base64(
        self,
        text: str,
        voice: Optional[str] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0
    ) -> Optional[str]:
        """Generate audio and return as base64 string for API responses"""
        audio_bytes = self.generate_audio(text, voice, speaking_rate, pitch)
        if audio_bytes:
            return base64.b64encode(audio_bytes).decode('utf-8')
        return None
    
    def list_available_voices(self) -> list:
        """List all available Chirp 3 HD voices"""
        return list(self.VOICE_OPTIONS.keys())
    
    def generate_audio_with_cache(
        self,
        text: str,
        voice: Optional[str] = None,
        content_type: str = "tts",
        week_number: Optional[int] = None,
        study_level: Optional[str] = None,
        audience: Optional[str] = None,
        voices: Optional[Dict[str, str]] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0
    ) -> Optional[bytes]:
        """
        Generate audio with caching support
        
        Checks cache first, generates and uploads to cache if not found.
        
        Args:
            text: Text to convert to speech
            voice: Single voice for TTS (ignored for podcast which has fixed voices)
            content_type: Type of content (podcast, study_guide, lesson_plan, etc.)
            week_number: CFM week number (1-52)
            study_level: Study level (essential, connected, scholarly)
            audience: Lesson plan audience (adult, youth, children)
            voices: Voice mapping for multi-speaker ({"Sarah": "aoede", "David": "alnilam"})
            speaking_rate: Speed of speech (0.25 to 4.0, default 1.0)
            pitch: Voice pitch adjustment (-20.0 to 20.0, default 0.0)
            
        Returns:
            Audio bytes in MP3 format or None if failed
        """
        # If no cache manager, generate normally
        if not self.cache_manager:
            return self.generate_audio(text, voice, speaking_rate, pitch)
        
        try:
            # Generate script hash for additional cache key uniqueness
            script_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
            
            # Get cache key
            cache_key = self.cache_manager._get_cache_key(
                content_type=content_type,
                week_number=week_number,
                study_level=study_level,
                audience=audience,
                voice=voice,
                voices=voices,
                script_hash=script_hash
            )
            
            # Check cache first
            cached_audio = self.cache_manager.get_cached_audio(cache_key)
            if cached_audio:
                logger.info(f"🎯 Returning cached audio: {cache_key}")
                return cached_audio
            
            # Cache miss - generate audio
            logger.info(f"⚡ Generating new audio for: {cache_key}")
            audio_bytes = self.generate_audio(text, voice, speaking_rate, pitch)
            
            if audio_bytes:
                # Upload to cache
                upload_success = self.cache_manager.upload_to_cache(cache_key, audio_bytes)
                if upload_success:
                    logger.info(f"💾 Cached audio for future requests: {cache_key}")
                else:
                    logger.warning(f"⚠️ Failed to cache audio, but returning generated audio")
            
            return audio_bytes
            
        except Exception as e:
            logger.error(f"Error in cached audio generation: {e}")
            # Fallback to non-cached generation
            return self.generate_audio(text, voice, speaking_rate, pitch)
    
    def generate_audio_base64_with_cache(
        self,
        text: str,
        voice: Optional[str] = None,
        content_type: str = "tts",
        week_number: Optional[int] = None,
        study_level: Optional[str] = None,
        audience: Optional[str] = None,
        voices: Optional[Dict[str, str]] = None,
        speaking_rate: float = 1.0,
        pitch: float = 0.0
    ) -> Optional[str]:
        """Generate audio with caching and return as base64 string"""
        audio_bytes = self.generate_audio_with_cache(
            text=text,
            voice=voice,
            content_type=content_type,
            week_number=week_number,
            study_level=study_level,
            audience=audience,
            voices=voices,
            speaking_rate=speaking_rate,
            pitch=pitch
        )
        if audio_bytes:
            return base64.b64encode(audio_bytes).decode('utf-8')
        return None


def create_google_tts_client(enable_cache: bool = True) -> Optional[GoogleCloudTTS]:
    """
    Factory function to create Google Cloud TTS client with optional caching
    
    Args:
        enable_cache: Whether to enable audio caching (default: True)
    
    Returns:
        GoogleCloudTTS instance or None if initialization fails
    """
    try:
        # Initialize cache manager if available and requested
        cache_manager = None
        if enable_cache and AUDIO_CACHE_AVAILABLE:
            try:
                from .audio_cache import create_audio_cache_manager
                cache_manager = create_audio_cache_manager()
                if cache_manager:
                    logger.info("✅ Audio caching enabled")
                else:
                    logger.warning("⚠️ Audio cache manager initialization failed - proceeding without caching")
            except Exception as e:
                logger.warning(f"⚠️ Could not initialize audio cache: {e} - proceeding without caching")
        
        # Create TTS client with or without cache
        client = GoogleCloudTTS(cache_manager=cache_manager)
        
        if client.test_connection():
            return client
        return None
    except Exception as e:
        logger.error(f"Failed to create Google Cloud TTS client: {e}")
        return None
