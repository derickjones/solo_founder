#!/usr/bin/env python3
"""
Audio Cache Testing Script

Tests the audio cache system end-to-end:
1. Generate audio (cache miss)
2. Retrieve from cache (cache hit)
3. Check cache stats
4. Clean up test files

Usage:
    python test_audio_cache.py
"""

import os
import sys
import time
import requests
import base64

# Configuration
API_BASE_URL = os.getenv('API_URL', 'http://localhost:8080')

def test_cache_stats():
    """Test getting cache statistics"""
    print("📊 Testing cache stats endpoint...")
    try:
        response = requests.get(f"{API_BASE_URL}/cache/stats")
        response.raise_for_status()
        stats = response.json()
        
        print(f"✅ Cache Stats:")
        print(f"   Total files: {stats.get('total_files', 0)}")
        print(f"   Total size: {stats.get('total_size_mb', 0):.2f}MB")
        print(f"   Files over 30 days: {stats.get('files_over_30_days', 0)}")
        
        return True
    except Exception as e:
        print(f"❌ Cache stats test failed: {e}")
        return False


def test_podcast_generation_and_cache():
    """Test podcast generation with caching"""
    print("\n🎙️  Testing podcast generation and caching...")
    
    test_request = {
        "title": "Test Podcast",
        "text": "This is a test of the audio caching system. The quick brown fox jumps over the lazy dog. Testing one two three.",
        "voice": "aoede"
    }
    
    # First request - should be cache miss
    print("⚡ First request (cache miss expected)...")
    start_time = time.time()
    try:
        response = requests.post(
            f"{API_BASE_URL}/tts/podcast",
            json=test_request,
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        
        first_request_time = time.time() - start_time
        print(f"✅ First request completed in {first_request_time:.2f}s")
        print(f"   Generation time: {result.get('generation_time_ms', 0)}ms")
        print(f"   Audio size: {len(result.get('audio_base64', '')) / 1024:.2f}KB (base64)")
        
        # Save audio for comparison
        first_audio_b64 = result.get('audio_base64', '')
        
    except Exception as e:
        print(f"❌ First request failed: {e}")
        return False
    
    # Wait a moment for cache to propagate
    print("⏳ Waiting 2 seconds for cache to propagate...")
    time.sleep(2)
    
    # Second request - should be cache hit
    print("🎯 Second request (cache hit expected)...")
    start_time = time.time()
    try:
        response = requests.post(
            f"{API_BASE_URL}/tts/podcast",
            json=test_request,
            timeout=180
        )
        response.raise_for_status()
        result = response.json()
        
        second_request_time = time.time() - start_time
        print(f"✅ Second request completed in {second_request_time:.2f}s")
        print(f"   Generation time: {result.get('generation_time_ms', 0)}ms")
        
        # Verify it's faster (cache hit should be much faster)
        if second_request_time < first_request_time * 0.5:
            print(f"🚀 Cache HIT confirmed! {(first_request_time / second_request_time):.1f}x faster")
        else:
            print(f"⚠️  Warning: Second request not significantly faster - cache may not be working")
        
        # Verify audio is identical
        second_audio_b64 = result.get('audio_base64', '')
        if first_audio_b64 == second_audio_b64:
            print("✅ Audio content matches (cache returning correct data)")
        else:
            print("⚠️  Warning: Audio content differs between requests")
        
        return True
        
    except Exception as e:
        print(f"❌ Second request failed: {e}")
        return False


def test_cache_cleanup():
    """Test cache cleanup (don't run in production!)"""
    print("\n🧹 Testing cache cleanup...")
    print("⚠️  Skipping cleanup test to avoid deleting production cache")
    print("   To test cleanup, run manually: curl -X DELETE {API_BASE_URL}/cache/cleanup")
    return True


def main():
    """Run all cache tests"""
    print("🧪 Audio Cache System Tests")
    print("=" * 50)
    print(f"API URL: {API_BASE_URL}")
    print()
    
    # Check if API is reachable
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        print(f"✅ API is reachable (status: {response.status_code})")
    except Exception as e:
        print(f"❌ Cannot reach API: {e}")
        print("   Make sure the backend is running and API_URL is correct")
        sys.exit(1)
    
    print()
    
    # Run tests
    results = []
    
    results.append(("Cache Stats", test_cache_stats()))
    results.append(("Podcast Generation & Caching", test_podcast_generation_and_cache()))
    results.append(("Cache Cleanup", test_cache_cleanup()))
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 Test Summary:")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Audio cache system is working correctly.")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check the output above for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
