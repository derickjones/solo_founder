#!/usr/bin/env python3
"""
Test script for CFM Deep Dive API endpoint
"""

import requests
import json
import time

# API base URL - adjust for local testing or production
API_BASE = "http://localhost:8080"  # Change to your API URL

def test_cfm_deep_dive(week_number=2, study_level="basic"):
    """Test the CFM Deep Dive endpoint"""
    
    print(f"Testing CFM Deep Dive API for Week {week_number} at {study_level} level...")
    
    # Test the endpoint
    url = f"{API_BASE}/cfm/deep-dive"
    payload = {
        "week_number": week_number,
        "study_level": study_level
    }
    
    try:
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=60)
        request_time = time.time() - start_time
        
        print(f"Response Status: {response.status_code}")
        print(f"Request Time: {request_time:.2f}s")
        
        if response.status_code == 200:
            data = response.json()
            
            print("\n=== CFM DEEP DIVE RESPONSE ===")
            print(f"Week: {data.get('week_number')} - {data.get('week_title')}")
            print(f"Date Range: {data.get('date_range')}")
            print(f"Study Level: {data.get('study_level')}")
            print(f"Bundle Sources: {data.get('bundle_sources')}")
            print(f"Total Characters: {data.get('total_characters'):,}")
            print(f"Generation Time: {data.get('generation_time_ms')}ms")
            print(f"\nStudy Guide Length: {len(data.get('study_guide', ''))}")
            print(f"\nFirst 300 chars of study guide:")
            print(data.get('study_guide', '')[:300] + "...")
            
            return True
            
        else:
            print(f"Error: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def test_config():
    """Test if the config endpoint shows CFM Deep Dive as available"""
    
    print("Checking API configuration...")
    
    try:
        response = requests.get(f"{API_BASE}/config")
        
        if response.status_code == 200:
            config = response.json()
            deep_dive_available = config.get('available_endpoints', {}).get('cfm_deep_dive', False)
            
            print(f"CFM Deep Dive Available: {deep_dive_available}")
            print(f"OpenAI Client: {config.get('openai_client', {}).get('available', False)}")
            
            return deep_dive_available
        else:
            print(f"Config check failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Config check error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 CFM Deep Dive API Test")
    print("=" * 40)
    
    # Check configuration
    if test_config():
        print("\n✅ Configuration looks good!")
        
        # Test basic level
        print(f"\n📚 Testing Basic Study Guide...")
        if test_cfm_deep_dive(week_number=2, study_level="basic"):
            print("✅ Basic test passed!")
        else:
            print("❌ Basic test failed!")
            
        # Test intermediate level
        print(f"\n📖 Testing Intermediate Study Guide...")
        if test_cfm_deep_dive(week_number=10, study_level="intermediate"):
            print("✅ Intermediate test passed!")
        else:
            print("❌ Intermediate test failed!")
            
        # Test advanced level
        print(f"\n📜 Testing Advanced Study Guide...")
        if test_cfm_deep_dive(week_number=38, study_level="advanced"):
            print("✅ Advanced test passed!")
        else:
            print("❌ Advanced test failed!")
    
    else:
        print("❌ Configuration not ready for CFM Deep Dive testing")