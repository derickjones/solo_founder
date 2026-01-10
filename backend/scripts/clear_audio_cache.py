#!/usr/bin/env python3
"""
Clear Audio Cache Script

Deletes cached audio files from Google Cloud Storage.
Options:
  - Clear all audio cache
  - Clear specific content types (podcast, study_guide, lesson_plan, etc.)
"""

import os
import argparse
from google.cloud import storage
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

BUCKET_NAME = os.getenv('BUCKET_NAME')
CACHE_PREFIX = 'audio-cache/'

CONTENT_TYPES = [
    'podcast',
    'study_guide', 
    'lesson_plan',
    'core_content',
    'daily_thoughts',
]


def get_cache_stats(bucket) -> dict:
    """Get statistics about cached audio files"""
    stats = {ct: {'count': 0, 'size_mb': 0} for ct in CONTENT_TYPES}
    stats['other'] = {'count': 0, 'size_mb': 0}
    stats['total'] = {'count': 0, 'size_mb': 0}
    
    blobs = bucket.list_blobs(prefix=CACHE_PREFIX)
    for blob in blobs:
        stats['total']['count'] += 1
        stats['total']['size_mb'] += blob.size / (1024 * 1024)
        
        # Categorize by content type
        categorized = False
        for ct in CONTENT_TYPES:
            if f'/{ct}/' in blob.name or f'/{ct}_' in blob.name:
                stats[ct]['count'] += 1
                stats[ct]['size_mb'] += blob.size / (1024 * 1024)
                categorized = True
                break
        
        if not categorized:
            stats['other']['count'] += 1
            stats['other']['size_mb'] += blob.size / (1024 * 1024)
    
    return stats


def clear_cache(bucket, content_type: str = None, dry_run: bool = False) -> int:
    """
    Clear audio cache files
    
    Args:
        bucket: GCS bucket object
        content_type: Specific content type to clear, or None for all
        dry_run: If True, only show what would be deleted
    
    Returns:
        Number of files deleted
    """
    if content_type:
        prefix = f"{CACHE_PREFIX}{content_type}/"
    else:
        prefix = CACHE_PREFIX
    
    blobs = list(bucket.list_blobs(prefix=prefix))
    
    if not blobs:
        print(f"No cached audio files found with prefix: {prefix}")
        return 0
    
    print(f"\n{'[DRY RUN] ' if dry_run else ''}Found {len(blobs)} file(s) to delete:")
    
    total_size = 0
    for blob in blobs:
        size_mb = blob.size / (1024 * 1024)
        total_size += size_mb
        print(f"  - {blob.name} ({size_mb:.2f} MB)")
    
    print(f"\nTotal size: {total_size:.2f} MB")
    
    if dry_run:
        print("\n[DRY RUN] No files were deleted. Run without --dry-run to delete.")
        return 0
    
    # Confirm deletion
    confirm = input(f"\n⚠️  Delete {len(blobs)} file(s)? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return 0
    
    # Delete files
    deleted = 0
    for blob in blobs:
        try:
            blob.delete()
            deleted += 1
            print(f"  ✅ Deleted: {blob.name}")
        except Exception as e:
            print(f"  ❌ Failed to delete {blob.name}: {e}")
    
    print(f"\n✅ Deleted {deleted} file(s)")
    return deleted


def main():
    parser = argparse.ArgumentParser(description='Clear audio cache from Google Cloud Storage')
    parser.add_argument('--type', '-t', choices=CONTENT_TYPES, 
                        help='Clear only specific content type (default: all)')
    parser.add_argument('--dry-run', '-d', action='store_true',
                        help='Show what would be deleted without actually deleting')
    parser.add_argument('--stats', '-s', action='store_true',
                        help='Show cache statistics only')
    parser.add_argument('--force', '-f', action='store_true',
                        help='Skip confirmation prompt')
    
    args = parser.parse_args()
    
    if not BUCKET_NAME:
        print("❌ Error: BUCKET_NAME environment variable not set")
        print("   Make sure backend/.env contains BUCKET_NAME=your-bucket-name")
        return 1
    
    print(f"🗑️  Audio Cache Manager")
    print(f"=" * 50)
    print(f"Bucket: {BUCKET_NAME}")
    print(f"Cache prefix: {CACHE_PREFIX}")
    
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        
        # Show stats
        stats = get_cache_stats(bucket)
        print(f"\n📊 Cache Statistics:")
        print(f"-" * 40)
        for ct in CONTENT_TYPES:
            if stats[ct]['count'] > 0:
                print(f"  {ct:15} {stats[ct]['count']:4} files  ({stats[ct]['size_mb']:7.2f} MB)")
        if stats['other']['count'] > 0:
            print(f"  {'other':15} {stats['other']['count']:4} files  ({stats['other']['size_mb']:7.2f} MB)")
        print(f"-" * 40)
        print(f"  {'TOTAL':15} {stats['total']['count']:4} files  ({stats['total']['size_mb']:7.2f} MB)")
        
        if args.stats:
            return 0
        
        # Clear cache
        if args.force:
            # Bypass confirmation for scripted use
            if args.type:
                prefix = f"{CACHE_PREFIX}{args.type}/"
            else:
                prefix = CACHE_PREFIX
            
            blobs = list(bucket.list_blobs(prefix=prefix))
            if not blobs:
                print(f"\nNo files to delete.")
                return 0
            
            if args.dry_run:
                print(f"\n[DRY RUN] Would delete {len(blobs)} file(s)")
                return 0
            
            deleted = 0
            for blob in blobs:
                try:
                    blob.delete()
                    deleted += 1
                except Exception as e:
                    print(f"  ❌ Failed: {blob.name}: {e}")
            print(f"\n✅ Deleted {deleted} file(s)")
        else:
            clear_cache(bucket, content_type=args.type, dry_run=args.dry_run)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return 1


if __name__ == "__main__":
    exit(main())
