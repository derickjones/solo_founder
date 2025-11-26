#!/usr/bin/env python3
"""
Create OpenAI embeddings and FAISS index for GospelGuide
Takes JSON content and creates searchable vector index
"""

import json
import os
import numpy as np
from pathlib import Path
from typing import List, Dict, Any
import time
from tqdm import tqdm

try:
    import openai
    import faiss
except ImportError as e:
    print(f"Missing dependencies: {e}")
    print("Run: pip install openai faiss-cpu numpy tqdm")
    exit(1)

class EmbeddingsBuilder:
    def __init__(self, api_key: str = None):
        # Initialize OpenAI client
        self.client = openai.OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        
        if not self.client.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter")
            
        self.embedding_model = "text-embedding-3-large"
        self.embedding_dim = 3072  # text-embedding-3-large dimension
        
    def create_embeddings(self, content: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create embeddings for all content items"""
        
        print(f"Creating embeddings for {len(content)} items...")
        
        embedded_content = []
        
        # Process in batches to respect rate limits
        batch_size = 100
        for i in tqdm(range(0, len(content), batch_size), desc="Creating embeddings"):
            batch = content[i:i + batch_size]
            
            # Extract text for embedding
            texts = [item['content'] for item in batch]
            
            try:
                # Create embeddings for batch
                response = self.client.embeddings.create(
                    model=self.embedding_model,
                    input=texts
                )
                
                # Add embeddings to content
                for j, item in enumerate(batch):
                    item_with_embedding = item.copy()
                    item_with_embedding['embedding'] = response.data[j].embedding
                    embedded_content.append(item_with_embedding)
                    
                # Rate limiting - be respectful
                if i + batch_size < len(content):
                    time.sleep(1)
                    
            except Exception as e:
                print(f"Error creating embeddings for batch {i}: {e}")
                # Add items without embeddings for now
                for item in batch:
                    embedded_content.append(item)
                    
        return embedded_content
    
    def build_faiss_index(self, embedded_content: List[Dict[str, Any]]) -> tuple:
        """Build FAISS index from embedded content"""
        
        print("Building FAISS index...")
        
        # Extract embeddings
        embeddings = []
        metadata = []
        
        for i, item in enumerate(embedded_content):
            if 'embedding' in item:
                embeddings.append(item['embedding'])
                
                # Store metadata without embedding for efficiency
                meta_item = {k: v for k, v in item.items() if k != 'embedding'}
                meta_item['index'] = i
                metadata.append(meta_item)
        
        if not embeddings:
            raise ValueError("No embeddings found in content")
            
        # Convert to numpy array
        embeddings_array = np.array(embeddings, dtype=np.float32)
        print(f"Embeddings shape: {embeddings_array.shape}")
        
        # Create FAISS index
        index = faiss.IndexFlatIP(self.embedding_dim)  # Inner product for cosine similarity
        
        # Normalize vectors for cosine similarity
        faiss.normalize_L2(embeddings_array)
        
        # Add vectors to index
        index.add(embeddings_array)
        
        print(f"FAISS index created with {index.ntotal} vectors")
        
        return index, metadata
    
    def save_index_and_metadata(self, index, metadata: List[Dict[str, Any]], output_dir: Path):
        """Save FAISS index and metadata files"""
        
        output_dir.mkdir(exist_ok=True)
        
        # Save FAISS index
        index_path = output_dir / "gospelguide.faiss"
        faiss.write_index(index, str(index_path))
        print(f"FAISS index saved to {index_path}")
        
        # Save metadata
        metadata_path = output_dir / "metadata.json" 
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, indent=2, ensure_ascii=False)
        print(f"Metadata saved to {metadata_path}")
        
        # Save summary stats
        stats = {
            "total_items": len(metadata),
            "embedding_model": self.embedding_model,
            "embedding_dimension": self.embedding_dim,
            "source_types": {},
            "books": {},
        }
        
        # Calculate stats
        for item in metadata:
            source_type = item.get('source_type', 'unknown')
            stats['source_types'][source_type] = stats['source_types'].get(source_type, 0) + 1
            
            if 'book' in item:
                book = item['book']
                stats['books'][book] = stats['books'].get(book, 0) + 1
        
        stats_path = output_dir / "index_stats.json"
        with open(stats_path, 'w', encoding='utf-8') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False)
        print(f"Index stats saved to {stats_path}")

def test_search(index, metadata: List[Dict[str, Any]], embeddings_builder: EmbeddingsBuilder, query: str = "faith"):
    """Test the search functionality"""
    
    print(f"\nTesting search with query: '{query}'")
    
    # Create query embedding
    response = embeddings_builder.client.embeddings.create(
        model=embeddings_builder.embedding_model,
        input=[query]
    )
    query_embedding = np.array([response.data[0].embedding], dtype=np.float32)
    faiss.normalize_L2(query_embedding)
    
    # Search
    k = 3  # Top 3 results
    scores, indices = index.search(query_embedding, k)
    
    print(f"\nTop {k} results:")
    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx < len(metadata):
            item = metadata[idx]
            print(f"\n{i+1}. Score: {score:.4f}")
            print(f"   Citation: {item.get('citation', 'N/A')}")
            print(f"   Content: {item['content'][:100]}...")

def main():
    # Check for OpenAI API key
    if not os.getenv('OPENAI_API_KEY'):
        print("Please set your OpenAI API key:")
        print("export OPENAI_API_KEY='sk-your-api-key-here'")
        return
    
    # Initialize builder
    builder = EmbeddingsBuilder()
    
    # Load content
    content_file = Path("content/sample_content.json")
    if not content_file.exists():
        print("No sample content found. Run create_sample_content.py first.")
        return
        
    with open(content_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    print(f"Loaded {len(content)} content items")
    
    # Create embeddings
    embedded_content = builder.create_embeddings(content)
    
    # Build FAISS index
    index, metadata = builder.build_faiss_index(embedded_content)
    
    # Save everything
    output_dir = Path("vector_index")
    builder.save_index_and_metadata(index, metadata, output_dir)
    
    # Test search
    test_search(index, metadata, builder, "faith")
    test_search(index, metadata, builder, "prophet")
    
    print("\n=== Embeddings and FAISS index created successfully! ===")
    print("Next step: Build the Google Cloud Run API to serve this index")

if __name__ == "__main__":
    main()