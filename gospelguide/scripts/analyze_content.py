#!/usr/bin/env python3
"""
Simple test of OpenAI embeddings - no dependencies needed yet
Just validates the content structure and shows next steps
"""

import json
from pathlib import Path

def analyze_content():
    """Analyze the sample content structure"""
    
    content_file = Path("content/sample_content.json")
    
    with open(content_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    print(f"=== Content Analysis ===")
    print(f"Total items: {len(content)}")
    
    # Analyze by source type
    source_types = {}
    books = {}
    
    for item in content:
        source_type = item.get('source_type', 'unknown')
        source_types[source_type] = source_types.get(source_type, 0) + 1
        
        if 'book' in item:
            book = item['book']
            books[book] = books.get(book, 0) + 1
    
    print(f"\nSource types: {source_types}")
    print(f"Books: {books}")
    
    # Show sample items
    print(f"\n=== Sample Items ===")
    for i, item in enumerate(content[:2]):
        print(f"\nItem {i+1}:")
        print(f"  Citation: {item.get('citation', 'N/A')}")
        print(f"  Content: {item['content'][:100]}...")
        print(f"  Word count: {item.get('word_count', 'N/A')}")
    
    # Test mode filtering
    print(f"\n=== Mode Filtering Test ===")
    
    bom_items = [item for item in content if item.get('standard_work') == 'Book of Mormon']
    conf_items = [item for item in content if item['source_type'] == 'conference']
    
    print(f"Book of Mormon only: {len(bom_items)} items")
    print(f"Conference only: {len(conf_items)} items")
    
    return content

def show_next_steps():
    """Show what's needed for embeddings"""
    
    print(f"\n=== Next Steps ===")
    print("1. Get OpenAI API key: https://platform.openai.com/api-keys")
    print("2. Set environment variable: export OPENAI_API_KEY='sk-your-key'")
    print("3. Install dependencies: pip install openai faiss-cpu numpy tqdm")
    print("4. Run: python3 create_embeddings.py")
    print("\nFor now, the content structure is ready for AI processing!")

def main():
    try:
        content = analyze_content()
        show_next_steps()
        
        print(f"\n=== Content Ready! ===")
        print("Your verse-level granularity is perfect for citations.")
        print(f"Each item has:")
        print("- Exact citation (e.g., '(1 Nephi 3:7)')")
        print("- Source metadata (book, chapter, verse)")
        print("- Mode filtering capability")
        print("- Clean content text")
        
    except FileNotFoundError:
        print("Sample content not found. Run create_sample_content.py first.")

if __name__ == "__main__":
    main()