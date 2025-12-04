#!/usr/bin/env python3
"""
Debug script to test search engine timing
"""

import sys
import os
import time

# Load environment variables
with open('/Users/derickjones/Documents/VS-Code/solo_founder/backend/.env', 'r') as f:
    for line in f:
        if line.strip() and not line.startswith('#') and '=' in line:
            key, value = line.strip().split('=', 1)
            os.environ[key] = value

# Add the search directory to the path
sys.path.append('/Users/derickjones/Documents/VS-Code/solo_founder/backend/search')

from scripture_search import ScriptureSearchEngine

def test_search_timing():
    """Test search engine performance"""
    
    print("🔍 Testing Search Engine Performance...")
    print("-" * 60)
    
    # Initialize search engine
    start_init = time.time()
    search_engine = ScriptureSearchEngine()
    init_time = time.time() - start_init
    print(f"Search engine init: {init_time:.3f}s")
    
    # Test search query
    query = "What is faith?"
    print(f"Query: {query}")
    
    start_search = time.time()
    results = search_engine.search(
        query=query,
        top_k=10,
        source_filter=None,
        min_score=0.0
    )
    search_time = time.time() - start_search
    
    print(f"Search completed: {search_time:.3f}s")
    print(f"Results found: {len(results)}")
    
    if search_time > 2:
        print("⚠️  WARNING: Search time > 2 seconds!")
    elif search_time > 1:
        print("🔸 NOTICE: Search time > 1 second")
    else:
        print("✅ Search timing looks good")
    
    # Test context building
    if results:
        from prompts import build_context_prompt, get_system_prompt
        
        start_context = time.time()
        context = build_context_prompt(query, results, "default")
        system_prompt = get_system_prompt("default")
        context_time = time.time() - start_context
        
        print(f"Context building: {context_time:.3f}s")
        print(f"Context length: {len(context)} chars")
        print(f"System prompt length: {len(system_prompt)} chars")
        
        if context_time > 0.5:
            print("⚠️  WARNING: Context building > 0.5 seconds!")
        else:
            print("✅ Context building timing looks good")

if __name__ == "__main__":
    test_search_timing()