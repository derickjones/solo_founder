#!/usr/bin/env python3

import requests
import json

# Test the new filter patterns
API_URL = "https://gospelguide-f5awjwifkq-uc.a.run.app"

def test_filter_pattern(source_filter, description):
    """Test a specific filter pattern"""
    payload = {
        "query": "faith",
        "mode": "default",
        "top_k": 3,
        "source_filter": source_filter
    }
    
    print(f"\n🔍 Testing: {description}")
    print(f"Filter: {json.dumps(source_filter, indent=2)}")
    
    try:
        response = requests.post(f"{API_URL}/search", json=payload, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            
            print(f"✅ Found {len(results)} results")
            for i, result in enumerate(results[:2], 1):  # Show first 2 results
                metadata = result.get('metadata', {})
                source_type = metadata.get('source_type')
                title = metadata.get('title', 'Unknown')
                year = metadata.get('year')
                speaker = metadata.get('speaker')
                
                print(f"  {i}. {source_type} - {title}")
                if year:
                    print(f"     Year: {year}")
                if speaker:
                    print(f"     Speaker: {speaker}")
        else:
            print(f"❌ Error {response.status_code}: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

# Test cases
print("=== Testing Gospel Guide Granular Filtering ===")

# 1. Test year-based filtering
test_filter_pattern(
    [{"source_type": "conference", "year": 2024}],
    "General Conference 2024"
)

# 2. Test speaker-based filtering  
test_filter_pattern(
    [{"source_type": "conference", "speaker": "Russell M. Nelson"}],
    "Russell M. Nelson talks"
)

# 3. Test combined year + scripture
test_filter_pattern(
    [
        {"source_type": "conference", "year": 2023},
        {"source_type": "scripture", "standard_work": "Book of Mormon"}
    ],
    "General Conference 2023 + Book of Mormon"
)

# 4. Test general conference (no specific filters)
test_filter_pattern(
    [{"source_type": "conference"}],
    "All General Conference"
)

print("\n=== Filter Testing Complete ===")