#!/usr/bin/env python3
"""
Test script for OpenAI TTS integration in audio summary endpoint
"""

import requests
import json
import base64

# Test the audio summary endpoint with TTS
def test_audio_summary_with_tts():
    url = "http://localhost:8000/cfm/audio-summary"
    
    # Test data
    payload = {
        "week_number": 4,
        "study_level": "basic",
        "voice": "alloy"  # Optional voice parameter for TTS
    }
    
    print("Testing audio summary with TTS...")
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success! Status: {response.status_code}")
            print(f"Week: {data.get('week_number')} - {data.get('week_title')}")
            print(f"Study Level: {data.get('study_level')}")
            print(f"Script Length: {len(data.get('audio_script', ''))} characters")
            
            # Check if audio files were generated
            audio_files = data.get('audio_files')
            if audio_files:
                print(f"🎵 Audio Files Generated: {list(audio_files.keys())}")
                
                # Save a sample audio file for testing
                if 'combined' in audio_files:
                    try:
                        audio_data = base64.b64decode(audio_files['combined'])
                        with open('test_audio_output.mp3', 'wb') as f:
                            f.write(audio_data)
                        print(f"✅ Audio file saved as 'test_audio_output.mp3' ({len(audio_data)} bytes)")
                    except Exception as e:
                        print(f"❌ Error saving audio file: {e}")
            else:
                print("ℹ️ No audio files generated (TTS may not be configured)")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out (this is expected for large content generation)")
    except Exception as e:
        print(f"❌ Error: {e}")

# Test without TTS (text only)
def test_audio_summary_text_only():
    url = "http://localhost:8000/cfm/audio-summary"
    
    # Test data without voice parameter
    payload = {
        "week_number": 4,
        "study_level": "basic"
        # No voice parameter = text only
    }
    
    print("\n" + "="*50)
    print("Testing audio summary without TTS (text only)...")
    print(f"Request: {json.dumps(payload, indent=2)}")
    
    try:
        response = requests.post(url, json=payload, timeout=120)
        
        if response.status_code == 200:
            data = response.json()
            print(f"\n✅ Success! Status: {response.status_code}")
            print(f"Week: {data.get('week_number')} - {data.get('week_title')}")
            print(f"Study Level: {data.get('study_level')}")
            print(f"Script Length: {len(data.get('audio_script', ''))} characters")
            print(f"Script Preview: {data.get('audio_script', '')[:200]}...")
            
            # Check if audio files were generated
            audio_files = data.get('audio_files')
            if audio_files:
                print(f"🎵 Audio Files: {list(audio_files.keys())}")
            else:
                print("ℹ️ No audio files generated (text-only mode)")
                
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("🎤 Testing Audio Summary with OpenAI TTS Integration")
    print("="*60)
    
    # Test with TTS
    test_audio_summary_with_tts()
    
    # Test without TTS
    test_audio_summary_text_only()