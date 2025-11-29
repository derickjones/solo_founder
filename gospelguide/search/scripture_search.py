#!/usr/bin/env python3
"""
Scripture Search Interface with Source Filtering
Query the FAISS index with OpenAI embeddings and rich metadata filtering
"""

import json
import os
import logging
import argparse
from typing import List, Dict, Any, Optional, Union
from pathlib import Path
import numpy as np
import faiss
from openai import OpenAI
import pickle

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ScriptureSearchEngine:
    def __init__(self, index_dir: str = "indexes", openai_api_key: str = None):
        """
        Initialize the scripture search engine
        
        Args:
            index_dir: Directory containing FAISS index and metadata files
            openai_api_key: OpenAI API key (or set OPENAI_API_KEY env var)
        """
        self.index_dir = Path(index_dir)
        
        # Initialize OpenAI client
        if openai_api_key:
            self.client = OpenAI(api_key=openai_api_key)
        else:
            self.client = OpenAI()  # Uses OPENAI_API_KEY env var
        
        # Load configuration
        config_path = self.index_dir / "config.json"
        with open(config_path, 'r') as f:
            self.config = json.load(f)
        
        self.embedding_model = self.config["embedding_model"]
        self.embedding_dim = self.config["embedding_dim"]
        
        # Load FAISS index
        index_path = self.index_dir / "scripture_index.faiss"
        self.index = faiss.read_index(str(index_path))
        logger.info(f"Loaded FAISS index with {self.index.ntotal} vectors")
        
        # Load metadata
        metadata_path = self.index_dir / "scripture_metadata.pkl"
        with open(metadata_path, 'rb') as f:
            self.metadata = pickle.load(f)
        logger.info(f"Loaded metadata for {len(self.metadata)} segments")
        
        assert len(self.metadata) == self.index.ntotal, "Metadata count must match index size"
    
    def _embed_query(self, query: str) -> np.ndarray:
        """Generate embedding for search query using OpenAI"""
        response = self.client.embeddings.create(
            input=query,
            model=self.embedding_model
        )
        embedding = np.array(response.data[0].embedding, dtype=np.float32)
        
        # Normalize for cosine similarity (since we use IndexFlatIP)
        embedding = embedding / np.linalg.norm(embedding)
        return embedding.reshape(1, -1)
    
    def _filter_indices(self, source_filter: Dict[str, Any]) -> List[int]:
        """
        Filter metadata indices based on source criteria
        
        Args:
            source_filter: Dict with filtering criteria like:
                - source_type: "scripture", "conference", "come_follow_me"
                - standard_work: "Book of Mormon", "New Testament", etc.
                - book: "1 Nephi", "Matthew", etc.
                - speaker: "Russell M. Nelson", etc.
                - year: 2024, etc.
                - Any other metadata field
        
        Returns:
            List of indices that match the filter criteria
        """
        matching_indices = []
        
        for i, meta in enumerate(self.metadata):
            match = True
            
            for key, value in source_filter.items():
                meta_value = meta.get(key)
                
                if meta_value is None:
                    match = False
                    break
                
                # Handle different comparison types
                if isinstance(value, list):
                    if meta_value not in value:
                        match = False
                        break
                elif isinstance(value, str):
                    if isinstance(meta_value, str):
                        if value.lower() not in meta_value.lower():
                            match = False
                            break
                    else:
                        if str(meta_value).lower() != value.lower():
                            match = False
                            break
                elif isinstance(value, (int, float)):
                    if meta_value != value:
                        match = False
                        break
                else:
                    if meta_value != value:
                        match = False
                        break
            
            if match:
                matching_indices.append(i)
        
        return matching_indices
    
    def search(self, 
               query: str, 
               top_k: int = 10, 
               source_filter: Optional[Dict[str, Any]] = None,
               min_score: float = 0.0) -> List[Dict[str, Any]]:
        """
        Search scripture content with semantic similarity and source filtering
        
        Args:
            query: Natural language search query
            top_k: Number of results to return
            source_filter: Optional filtering criteria (see _filter_indices for options)
            min_score: Minimum similarity score (0.0 to 1.0)
        
        Returns:
            List of search results with content, metadata, and scores
        """
        logger.info(f"Searching for: '{query}'")
        
        # Generate query embedding
        query_embedding = self._embed_query(query)
        
        # Apply source filtering if specified
        if source_filter:
            filtered_indices = self._filter_indices(source_filter)
            logger.info(f"Source filter matched {len(filtered_indices)} segments")
            
            if not filtered_indices:
                logger.warning("No segments match the source filter")
                return []
            
            # Create a subset index for filtered search
            filtered_vectors = np.array([self.index.reconstruct(i) for i in filtered_indices])
            temp_index = faiss.IndexFlatIP(self.embedding_dim)
            temp_index.add(filtered_vectors)
            
            # Search the filtered index
            scores, temp_indices = temp_index.search(query_embedding, min(top_k, len(filtered_indices)))
            
            # Map back to original indices
            original_indices = [filtered_indices[i] for i in temp_indices[0]]
        else:
            # Search the full index
            scores, indices = self.index.search(query_embedding, top_k)
            original_indices = indices[0]
        
        scores = scores[0]
        
        # Build results
        results = []
        for i, (idx, score) in enumerate(zip(original_indices, scores)):
            if score < min_score:
                continue
                
            meta = self.metadata[idx].copy()
            
            # Reconstruct the text content (you might want to store this separately for efficiency)
            # For now, we'll include the full metadata
            result = {
                'rank': i + 1,
                'score': float(score),
                'content': meta.get('content', f"[Content for index {idx}] - {meta.get('citation', 'Unknown citation')}"),
                'metadata': meta
            }
            results.append(result)
        
        logger.info(f"Found {len(results)} results")
        return results
    
    def search_by_source(self, query: str, source_type: str, **kwargs) -> List[Dict[str, Any]]:
        """Convenience method to search within a specific source type"""
        source_filter = {"source_type": source_type}
        source_filter.update(kwargs)
        return self.search(query, source_filter=source_filter)
    
    def search_scripture(self, query: str, standard_work: str = None, book: str = None, **kwargs) -> List[Dict[str, Any]]:
        """Convenience method to search scripture content"""
        source_filter = {"source_type": "scripture"}
        if standard_work:
            source_filter["standard_work"] = standard_work
        if book:
            source_filter["book"] = book
        source_filter.update(kwargs)
        return self.search(query, source_filter=source_filter)
    
    def search_conference(self, query: str, speaker: str = None, year: int = None, **kwargs) -> List[Dict[str, Any]]:
        """Convenience method to search General Conference content"""
        source_filter = {"source_type": "conference"}
        if speaker:
            source_filter["speaker"] = speaker
        if year:
            source_filter["year"] = year
        source_filter.update(kwargs)
        return self.search(query, source_filter=source_filter)
    
    def get_available_sources(self) -> Dict[str, Any]:
        """Get summary of available sources for filtering"""
        sources = {
            "source_types": set(),
            "standard_works": set(),
            "books": set(),
            "speakers": set(),
            "years": set(),
            "total_segments": len(self.metadata)
        }
        
        for meta in self.metadata:
            if "source_type" in meta:
                sources["source_types"].add(meta["source_type"])
            if "standard_work" in meta:
                sources["standard_works"].add(meta["standard_work"])
            if "book" in meta:
                sources["books"].add(meta["book"])
            if "speaker" in meta:
                sources["speakers"].add(meta["speaker"])
            if "year" in meta:
                sources["years"].add(meta["year"])
        
        # Convert sets to sorted lists for JSON serialization
        for key in ["source_types", "standard_works", "books", "speakers", "years"]:
            sources[key] = sorted(list(sources[key]))
        
        return sources

def main():
    parser = argparse.ArgumentParser(description="Search LDS Scripture Content")
    parser.add_argument("query", nargs='?', help="Search query")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results to return")
    parser.add_argument("--source-type", help="Filter by source type (scripture, conference, come_follow_me)")
    parser.add_argument("--standard-work", help="Filter by standard work")
    parser.add_argument("--book", help="Filter by book")
    parser.add_argument("--speaker", help="Filter by speaker")
    parser.add_argument("--year", type=int, help="Filter by year")
    parser.add_argument("--min-score", type=float, default=0.0, help="Minimum similarity score")
    parser.add_argument("--list-sources", action="store_true", help="List available sources")
    
    args = parser.parse_args()
    
    # Initialize search engine
    try:
        engine = ScriptureSearchEngine()
    except Exception as e:
        logger.error(f"Failed to initialize search engine: {e}")
        return
    
    if args.list_sources:
        sources = engine.get_available_sources()
        print("\n=== Available Sources ===")
        print(json.dumps(sources, indent=2))
        return
    
    if not args.query:
        print("Error: Query is required when not using --list-sources")
        parser.print_help()
        return
    
    # Build source filter
    source_filter = {}
    if args.source_type:
        source_filter["source_type"] = args.source_type
    if args.standard_work:
        source_filter["standard_work"] = args.standard_work
    if args.book:
        source_filter["book"] = args.book
    if args.speaker:
        source_filter["speaker"] = args.speaker
    if args.year:
        source_filter["year"] = args.year
    
    # Perform search
    results = engine.search(
        args.query, 
        top_k=args.top_k,
        source_filter=source_filter if source_filter else None,
        min_score=args.min_score
    )
    
    # Display results
    print(f"\n=== Search Results for '{args.query}' ===")
    if source_filter:
        print(f"Filtered by: {source_filter}")
    print(f"Found {len(results)} results\n")
    
    for result in results:
        meta = result["metadata"]
        print(f"#{result['rank']} (Score: {result['score']:.3f})")
        print(f"Citation: {meta.get('citation', 'N/A')}")
        print(f"Source: {meta.get('standard_work', 'N/A')} ({meta.get('source_type', 'N/A')})")
        
        if meta.get("speaker"):
            print(f"Speaker: {meta['speaker']} ({meta.get('year', 'N/A')})")
        if meta.get("book"):
            print(f"Book: {meta['book']} {meta.get('chapter', '')}:{meta.get('verse', '')}")
        
        print(f"Content: {result['content']}")
        print("-" * 80)

if __name__ == "__main__":
    main()