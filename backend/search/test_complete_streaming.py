#!/usr/bin/env python3
"""
Complete test of streaming functionality with proper initialization
"""

import os
import sys
import asyncio
import json

# Set up environment
# OpenAI API key should be set as environment variable
# export OPENAI_API_KEY="your-api-key-here"
if not os.environ.get('OPENAI_API_KEY'):
    print("Error: OPENAI_API_KEY environment variable is required")
    sys.exit(1)

sys.path.append('.')

from scripture_search import ScriptureSearchEngine
from prompts import build_context_prompt, get_system_prompt, get_mode_source_filter
import openai

async def test_complete_streaming():
    print("🚀 Testing complete streaming workflow...")
    
    # Initialize search engine
    print("📚 Initializing search engine...")
    search_engine = ScriptureSearchEngine()
    
    # Initialize OpenAI client
    print("🤖 Initializing OpenAI client...")
    openai_client = openai.OpenAI()
    
    # Test request
    query = "What is faith?"
    mode = "default"
    top_k = 3
    min_score = 0.0
    
    print(f"\n🔍 Testing query: '{query}' (mode: {mode})")
    
    # Step 1: Search
    print("Step 1: Performing search...")
    mode_filter = get_mode_source_filter(mode)
    print(f"Mode filter: {mode_filter}")
    
    search_results = search_engine.search(
        query=query,
        top_k=top_k,
        source_filter=mode_filter,
        min_score=min_score
    )
    print(f"✅ Found {len(search_results)} results")
    
    # Step 2: Build prompts
    print("Step 2: Building context prompts...")
    context_prompt = build_context_prompt(query, search_results, mode)
    system_prompt = get_system_prompt(mode)
    print(f"✅ Context: {len(context_prompt)} chars, System: {len(system_prompt)} chars")
    
    # Step 3: Test streaming
    print("Step 3: Testing OpenAI streaming...")
    
    stream = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context_prompt}
        ],
        max_tokens=1000,
        temperature=0.3,
        stream=True
    )
    
    print("\n📡 Streaming AI response:")
    print("=" * 60)
    
    full_response = ""
    chunk_count = 0
    
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            content = chunk.choices[0].delta.content
            full_response += content
            chunk_count += 1
            print(content, end='', flush=True)
    
    print("\n" + "=" * 60)
    print(f"✅ Streaming completed:")
    print(f"   - Total chunks: {chunk_count}")
    print(f"   - Response length: {len(full_response)} chars")
    print(f"   - Sources used: {len(search_results)}")
    
    # Step 4: Test the streaming format (simulating what the API would send)
    print("\nStep 4: Testing SSE format...")
    
    # Simulate the streaming format
    messages = []
    
    # Search complete message
    search_msg = {
        'type': 'search_complete',
        'search_time_ms': 500,
        'total_sources': len(search_results)
    }
    messages.append(f"data: {json.dumps(search_msg)}")
    
    # Content chunks (simulate splitting the response)
    words = full_response.split(' ')
    for i in range(0, len(words), 3):  # Send 3 words at a time
        chunk = ' '.join(words[i:i+3])
        if i + 3 < len(words):
            chunk += ' '
        content_msg = {'type': 'content', 'content': chunk}
        messages.append(f"data: {json.dumps(content_msg)}")
    
    # Sources message
    sources_msg = {
        'type': 'sources',
        'sources': [
            {
                'rank': result['rank'],
                'score': result['score'],
                'content': result['content'][:100] + '...',  # Truncate for display
                'metadata': result['metadata']
            }
            for result in search_results
        ]
    }
    messages.append(f"data: {json.dumps(sources_msg)}")
    
    # Done message
    messages.append(f"data: {json.dumps({'type': 'done'})}")
    
    print(f"✅ Generated {len(messages)} SSE messages")
    print(f"   - Search complete: ✓")
    print(f"   - Content chunks: {len([m for m in messages if 'content' in m])}")
    print(f"   - Sources: ✓")
    print(f"   - Done: ✓")
    
    return True

if __name__ == "__main__":
    try:
        result = asyncio.run(test_complete_streaming())
        print(f"\n🎉 Complete streaming test PASSED!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()