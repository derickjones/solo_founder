#!/usr/bin/env python3
"""
Debug script to test OpenAI API response times and identify delays
"""

import os
import time
import openai
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/derickjones/Documents/VS-Code/solo_founder/backend/.env')

def test_openai_streaming():
    """Test OpenAI API streaming response times"""
    
    # Initialize OpenAI client
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("❌ OPENAI_API_KEY not found")
        return
    
    client = openai.OpenAI(api_key=api_key)
    
    # Test prompt
    system_prompt = "You are a helpful assistant that provides thoughtful answers about religious topics."
    user_prompt = "What is faith? Please provide a thoughtful explanation."
    
    print("🧪 Testing OpenAI streaming response times...")
    print(f"Model: gpt-4o-mini")
    print(f"Prompt: {user_prompt}")
    print("-" * 60)
    
    start_time = time.time()
    
    try:
        # Create streaming completion
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=2000,
            temperature=0.3,
            stream=True
        )
        
        first_chunk_time = None
        chunk_count = 0
        full_response = ""
        
        print("⏱️  Timing Results:")
        print(f"Stream created at: {time.time() - start_time:.3f}s")
        
        for chunk in stream:
            chunk_count += 1
            current_time = time.time() - start_time
            
            if chunk.choices[0].delta.content is not None:
                content = chunk.choices[0].delta.content
                full_response += content
                
                if first_chunk_time is None:
                    first_chunk_time = current_time
                    print(f"🎯 First content chunk at: {first_chunk_time:.3f}s")
                
                if chunk_count <= 5:  # Show first 5 chunks
                    print(f"Chunk {chunk_count:2d} at {current_time:.3f}s: '{content[:20]}...'")
        
        total_time = time.time() - start_time
        
        print("-" * 60)
        print("📊 Summary:")
        print(f"Time to first chunk: {first_chunk_time:.3f}s")
        print(f"Total response time: {total_time:.3f}s")
        print(f"Total chunks: {chunk_count}")
        print(f"Response length: {len(full_response)} chars")
        print(f"Average chunk size: {len(full_response)/max(chunk_count,1):.1f} chars")
        
        if first_chunk_time > 5:
            print("⚠️  WARNING: Time to first chunk is > 5 seconds!")
        elif first_chunk_time > 2:
            print("🔸 NOTICE: Time to first chunk is > 2 seconds")
        else:
            print("✅ First chunk timing looks good")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_openai_streaming()