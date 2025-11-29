#!/usr/bin/env python3
"""
Build OpenAI embeddings + FAISS index for LDS Scripture Search
Processes 58K+ text segments from scripture content
"""

import json
import os
import logging
import argparse
from typing import List, Dict, Any, Tuple
from pathlib import Path
import numpy as np
import faiss
from openai import OpenAI
from tqdm import tqdm
import pickle

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScriptureEmbeddingBuilder:
    def __init__(self, content_dir: str, output_dir: str, openai_api_key: str = None):
        """
        Initialize the embedding builder
        
        Args:
            content_dir: Path to directory with JSON content files
            output_dir: Path to save FAISS index and metadata
            openai_api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        """
        self.content_dir = Path(content_dir)
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize OpenAI client
        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
        else:
            self.client = OpenAI()  # Uses OPENAI_API_KEY env var
        
        # Embedding model - text-embedding-3-small is great balance of quality/cost
        self.embedding_model = "text-embedding-3-small"
        self.embedding_dim = 1536  # Dimension for text-embedding-3-small
        
        # Content files to process
        self.content_files = [
            "book_of_mormon.json",
            "old_testament.json", 
            "new_testament.json",
            "doctrine_covenants.json",
            "pearl_of_great_price.json",
            "general_conference.json",
            "come_follow_me.json"
        ]
        
        # Storage for all text segments and metadata
        self.all_texts = []
        self.all_metadata = []
        
    def load_content_files(self):
        """Load all JSON content files and extract text segments"""
        logger.info("Loading content files...")
        
        total_segments = 0
        for filename in self.content_files:
            file_path = self.content_dir / filename
            if not file_path.exists():
                logger.warning(f"File not found: {file_path}")
                continue
                
            logger.info(f"Loading {filename}...")
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            # Process each content item
            for item in data:
                # Extract text content
                text = item.get('content', '').strip()
                if not text:
                    continue
                    
                # Build metadata for search results
                metadata = {
                    'id': item.get('id', ''),
                    'citation': item.get('citation', ''),
                    'source_type': item.get('source_type', ''),
                    'standard_work': item.get('standard_work', ''),
                    'url': item.get('url', ''),
                    'word_count': item.get('word_count', 0),
                    'mode_tags': item.get('mode_tags', []),
                    'filename': filename
                }
                
                # Add source-specific metadata
                if 'book' in item:  # Scripture
                    metadata.update({
                        'book': item.get('book'),
                        'chapter': item.get('chapter'),
                        'verse': item.get('verse')
                    })
                elif 'speaker' in item:  # General Conference
                    metadata.update({
                        'speaker': item.get('speaker'),
                        'title': item.get('title'),
                        'year': item.get('year'),
                        'session': item.get('session'),
                        'paragraph': item.get('paragraph')
                    })
                elif 'lesson_title' in item:  # Come Follow Me
                    metadata.update({
                        'lesson_title': item.get('lesson_title'),
                        'year': item.get('year'),
                        'focus': item.get('focus'),
                        'section': item.get('section')
                    })
                
                self.all_texts.append(text)
                self.all_metadata.append(metadata)
                
            logger.info(f"  Loaded {len(data)} items from {filename}")
            total_segments += len(data)
            
        logger.info(f"Total loaded: {len(self.all_texts)} text segments from {total_segments} items")
        
    def generate_embeddings(self, batch_size: int = 100):
        """Generate OpenAI embeddings for all text segments"""
        logger.info(f"Generating embeddings for {len(self.all_texts)} texts...")
        
        embeddings = []
        
        # Process in batches to handle rate limits
        for i in tqdm(range(0, len(self.all_texts), batch_size), desc="Generating embeddings"):
            batch_texts = self.all_texts[i:i + batch_size]
            
            try:
                # Call OpenAI embeddings API
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=batch_texts
                )
                
                # Extract embeddings from response
                batch_embeddings = [item.embedding for item in response.data]
                embeddings.extend(batch_embeddings)
                
            except Exception as e:
                logger.error(f"Error generating embeddings for batch {i//batch_size + 1}: {e}")
                raise
                
        logger.info(f"Generated {len(embeddings)} embeddings")
        return np.array(embeddings, dtype=np.float32)
    
    def build_faiss_index(self, embeddings: np.ndarray):
        """Build FAISS index from embeddings"""
        logger.info("Building FAISS index...")
        
        # Use IndexFlatIP for cosine similarity (after L2 normalization)
        # This gives exact search results, fast for 58K segments
        faiss.normalize_L2(embeddings)  # Normalize for cosine similarity
        index = faiss.IndexFlatIP(self.embedding_dim)
        
        # Add embeddings to index
        index.add(embeddings)
        
        logger.info(f"FAISS index built with {index.ntotal} vectors")
        return index
    
    def save_index_and_metadata(self, index: faiss.Index):
        """Save FAISS index and metadata to disk"""
        logger.info("Saving index and metadata...")
        
        # Save FAISS index
        index_path = self.output_dir / "scripture_index.faiss"
        faiss.write_index(index, str(index_path))
        logger.info(f"FAISS index saved to {index_path}")
        
        # Save metadata
        metadata_path = self.output_dir / "scripture_metadata.pkl"
        with open(metadata_path, 'wb') as f:
            pickle.dump(self.all_metadata, f)
        logger.info(f"Metadata saved to {metadata_path}")
        
        # Save configuration
        config = {
            'embedding_model': self.embedding_model,
            'embedding_dim': self.embedding_dim,
            'total_segments': len(self.all_texts),
            'content_files': self.content_files,
            'index_type': 'IndexFlatIP'
        }
        
        config_path = self.output_dir / "config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)
        logger.info(f"Configuration saved to {config_path}")
        
    def build_complete_index(self, batch_size: int = 100):
        """Complete pipeline: load content, generate embeddings, build index"""
        logger.info("=== Starting Scripture Embedding Pipeline ===")
        
        # Step 1: Load content
        self.load_content_files()
        
        # Step 2: Generate embeddings
        embeddings = self.generate_embeddings(batch_size=batch_size)
        
        # Step 3: Build FAISS index
        index = self.build_faiss_index(embeddings)
        
        # Step 4: Save everything
        self.save_index_and_metadata(index)
        
        logger.info("=== Scripture Embedding Pipeline Complete ===")
        logger.info(f"Index saved to: {self.output_dir}")
        logger.info(f"Total segments indexed: {len(self.all_texts)}")


def main():
    parser = argparse.ArgumentParser(description='Build scripture embeddings and FAISS index')
    parser.add_argument('--content-dir', default='../scripts/content', 
                        help='Directory containing JSON content files')
    parser.add_argument('--output-dir', default='./indexes',
                        help='Directory to save FAISS index and metadata')
    parser.add_argument('--batch-size', type=int, default=100,
                        help='Batch size for embedding generation')
    parser.add_argument('--openai-key', 
                        help='OpenAI API key (or set OPENAI_API_KEY env var)')
    
    args = parser.parse_args()
    
    # Check for OpenAI API key
    if not args.openai_key and not os.getenv('OPENAI_API_KEY'):
        logger.error("Please provide OpenAI API key via --openai-key or OPENAI_API_KEY env var")
        return
    
    # Build embeddings
    builder = ScriptureEmbeddingBuilder(
        content_dir=args.content_dir,
        output_dir=args.output_dir,
        openai_api_key=args.openai_key
    )
    
    try:
        builder.build_complete_index(batch_size=args.batch_size)
        logger.info("✅ Scripture embedding index built successfully!")
        
    except Exception as e:
        logger.error(f"❌ Error building embeddings: {e}")
        raise


if __name__ == "__main__":
    main()