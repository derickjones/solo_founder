#!/usr/bin/env python3
"""
Test script for the new CFM Male voice configuration
Tests voice initialization and configuration locally
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the backend directory to Python path
sys.path.append(str(Path(__file__).parent))

from search.elevenlabs_tts import create_elevenlabs_client

def test_cfm_voice_config():
    """Test the CFM Male voice configuration"""
    print("🎵 Testing CFM Male Voice Configuration")
    print("=" * 50)
    
    # Check if ElevenLabs API key is available
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        print("❌ ELEVENLABS_API_KEY not found in environment")
        print("   Set the API key to test voice generation")
        return False
    
    print(f"✅ ElevenLabs API key found: {api_key[:8]}...")
    
    try:
        # Create ElevenLabs client
        print("\n🔧 Creating ElevenLabs TTS client...")
        client = create_elevenlabs_client()
        
        if not client:
            print("❌ Failed to create ElevenLabs client")
            return False
        
        print("✅ ElevenLabs client created successfully")
        
        # Test connection
        print("\n🌐 Testing connection...")
        if client.test_connection():
            print("✅ ElevenLabs connection successful")
        else:
            print("❌ ElevenLabs connection failed")
            return False
        
        # Check voice configuration
        print("\n🎤 Checking voice configuration...")
        print(f"Default voice: {client.default_voice}")
        print(f"Available voices: {list(client.voice_options.keys())}")
        
        # Verify CFM Male voice is in options
        if "cfm_male" in client.voice_options:
            cfm_voice_id = client.voice_options["cfm_male"]
            print(f"✅ CFM Male voice found: {cfm_voice_id}")
        else:
            print("❌ CFM Male voice not found in voice options")
            return False
        
        # Test voice ID resolution
        print("\n🔍 Testing voice ID resolution...")
        resolved_id = client.get_voice_id("cfm_male")
        expected_id = "dmD3jHmyT4TJHfjKXGI2"
        
        if resolved_id == expected_id:
            print(f"✅ Voice ID resolution correct: {resolved_id}")
        else:
            print(f"❌ Voice ID mismatch. Expected: {expected_id}, Got: {resolved_id}")
            return False
        
        # Test default voice resolution
        default_resolved = client.get_voice_id(None)  # Should use default
        if default_resolved == expected_id:
            print(f"✅ Default voice resolution correct: {default_resolved}")
        else:
            print(f"❌ Default voice mismatch. Expected: {expected_id}, Got: {default_resolved}")
            return False
        
        print("\n🎉 All voice configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        import traceback
        print(traceback.format_exc())
        return False

def test_audio_generation():
    """Test actual audio generation with CFM Male voice"""
    print("\n\n🎙️  Testing Audio Generation")
    print("=" * 50)
    
    try:
        client = create_elevenlabs_client()
        if not client:
            print("❌ ElevenLabs client not available")
            return False
        
        test_text = "This is a test of the CFM Male voice for Come Follow Me audio summaries. The voice should sound clear and professional for gospel study content."
        
        print(f"📝 Test text: {test_text[:50]}...")
        print(f"📏 Text length: {len(test_text)} characters")
        
        # Test audio generation
        print("\n🔊 Generating audio with CFM Male voice...")
        audio_bytes = client.generate_audio(test_text, voice="cfm_male")
        
        if audio_bytes:
            print(f"✅ Audio generated successfully: {len(audio_bytes)} bytes")
            
            # Test base64 encoding
            audio_b64 = client.generate_audio_base64(test_text, voice="cfm_male")
            if audio_b64:
                print(f"✅ Base64 encoding successful: {len(audio_b64)} characters")
                return True
            else:
                print("❌ Base64 encoding failed")
                return False
        else:
            print("❌ Audio generation failed")
            return False
            
    except Exception as e:
        print(f"❌ Audio generation error: {e}")
        import traceback
        print(traceback.format_exc())
        return False

if __name__ == "__main__":
    print("🚀 Starting CFM Voice Tests\n")
    
    # Test 1: Voice configuration
    config_success = test_cfm_voice_config()
    
    # Test 2: Audio generation (only if config test passes)
    if config_success:
        audio_success = test_audio_generation()
        
        if audio_success:
            print("\n🎉 All tests passed! CFM Male voice is ready for deployment.")
        else:
            print("\n⚠️  Voice configuration is correct, but audio generation failed.")
            print("   This might be due to API permissions or network issues.")
    else:
        print("\n❌ Voice configuration tests failed. Please check the setup.")