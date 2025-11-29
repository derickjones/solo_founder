#!/usr/bin/env python3
"""
Cloud Storage integration for Gospel Guide
Downloads content files and search indexes from Google Cloud Storage on startup
"""

import os
import logging
from pathlib import Path
from google.cloud import storage

logger = logging.getLogger(__name__)

class CloudStorageManager:
    def __init__(self, bucket_name: str = None):
        """Initialize Cloud Storage client"""
        self.bucket_name = bucket_name or os.getenv('BUCKET_NAME')
        if not self.bucket_name:
            raise ValueError("BUCKET_NAME environment variable required")
        
        self.client = storage.Client()
        self.bucket = self.client.bucket(self.bucket_name)
    
    def download_indexes(self, local_dir: str = "indexes"):
        """Download search indexes from Cloud Storage"""
        local_path = Path(local_dir)
        local_path.mkdir(parents=True, exist_ok=True)
        
        # Required index files
        required_files = [
            "config.json",
            "scripture_index.faiss", 
            "scripture_metadata.pkl"
        ]
        
        for filename in required_files:
            blob = self.bucket.blob(f"indexes/{filename}")
            local_file = local_path / filename
            
            try:
                logger.info(f"Downloading {filename}...")
                blob.download_to_filename(str(local_file))
                logger.info(f"✅ Downloaded {filename} ({local_file.stat().st_size / 1024 / 1024:.1f}MB)")
            except Exception as e:
                logger.error(f"❌ Failed to download {filename}: {e}")
                raise
    
    def download_content(self, local_dir: str = "content"):
        """Download content files from Cloud Storage (optional)"""
        local_path = Path(local_dir)
        local_path.mkdir(parents=True, exist_ok=True)
        
        # List all content files
        content_blobs = self.bucket.list_blobs(prefix="content/")
        
        for blob in content_blobs:
            if blob.name.endswith('.json'):
                filename = Path(blob.name).name
                local_file = local_path / filename
                
                try:
                    logger.info(f"Downloading content: {filename}...")
                    blob.download_to_filename(str(local_file))
                    logger.info(f"✅ Downloaded {filename}")
                except Exception as e:
                    logger.warning(f"⚠️  Failed to download {filename}: {e}")
    
    def check_bucket_exists(self):
        """Check if the bucket exists and is accessible"""
        try:
            self.bucket.reload()
            logger.info(f"✅ Connected to bucket: {self.bucket_name}")
            return True
        except Exception as e:
            logger.error(f"❌ Cannot access bucket {self.bucket_name}: {e}")
            return False

def setup_cloud_storage():
    """Setup function called on API startup"""
    bucket_name = os.getenv('BUCKET_NAME')
    if not bucket_name:
        logger.warning("No BUCKET_NAME set, skipping Cloud Storage setup")
        return
    
    try:
        manager = CloudStorageManager(bucket_name)
        
        # Check bucket access
        if not manager.check_bucket_exists():
            raise Exception("Cannot access Cloud Storage bucket")
        
        # Download required search indexes
        index_dir = os.getenv('INDEX_DIR', 'indexes')
        manager.download_indexes(index_dir)
        
        logger.info("🎉 Cloud Storage setup complete")
        
    except Exception as e:
        logger.error(f"❌ Cloud Storage setup failed: {e}")
        raise