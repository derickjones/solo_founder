#!/usr/bin/env python3
"""
Quick test of the /ask endpoint functionality
"""

import os
import sys
sys.path.append('.')

# OpenAI API key should be set as environment variable
# export OPENAI_API_KEY="your-api-key-here"
if not os.environ.get('OPENAI_API_KEY'):
    print("Error: OPENAI_API_KEY environment variable is required")
    sys.exit(1)

from scripture_search import ScriptureSearchEngine
from prompts import build_context_prompt, get_system_prompt
import openai

def test_ai_response():
    print("🔍 Testing AI response generation...")
    
    # Initialize search engine
    search_engine = ScriptureSearchEngine()
    
    # Perform a search
    query = "What is faith?"
    results = search_engine.search(query, top_k=3)
    
    print(f"Found {len(results)} results for '{query}'")
    
    # Build context prompt
    context = build_context_prompt(query, results, 'default')
    system_prompt = get_system_prompt('default')
    
    print(f"\nContext length: {len(context)} chars")
    print(f"System prompt length: {len(system_prompt)} chars")
    
    # Test OpenAI response
    client = openai.OpenAI()
    
    print("\n🤖 Generating AI response...")
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context}
        ],
        max_tokens=1000,
        temperature=0.3
    )
    
    answer = response.choices[0].message.content
    
    print("\n✅ AI Response generated successfully!")
    print(f"\nAnswer length: {len(answer)} chars")
    print("\n" + "="*50)
    print("GENERATED ANSWER:")
    print("="*50)
    print(answer)
    print("="*50)
    
    return True

if __name__ == "__main__":
    try:
        test_ai_response()
        print("\n🎉 Test completed successfully!")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()