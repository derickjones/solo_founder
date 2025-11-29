#!/usr/bin/env python3
"""
Test the streaming /ask endpoint
"""

import os
import sys
sys.path.append('.')

# OpenAI API key should be set as environment variable
# export OPENAI_API_KEY="your-api-key-here"
if not os.environ.get('OPENAI_API_KEY'):
    print("Error: OPENAI_API_KEY environment variable is required")
    sys.exit(1)

import asyncio
from api import ask_question_stream, AskRequest

async def test_streaming():
    print("🔄 Testing streaming AI response...")
    
    request = AskRequest(
        query="What is faith?",
        mode="default",
        top_k=3
    )
    
    # Test the streaming generator
    generator = ask_question_stream(request)
    
    print("\n📡 Streaming response:")
    print("-" * 50)
    
    async for chunk in generator():
        print(chunk, end='', flush=True)
    
    print("\n" + "-" * 50)
    print("✅ Streaming test completed!")

if __name__ == "__main__":
    asyncio.run(test_streaming())