#!/usr/bin/env python3
"""
Audio Generation Analysis Script
Uses the deployed API to generate all three audio durations and captures full context for Grok analysis
"""

import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Your deployed API endpoint
API_BASE_URL = "https://gospel-guide-api-273320302933.us-central1.run.app"

def analyze_audio_generation():
    """
    Generate audio summaries for all three durations using the deployed API
    """
    
    # Use Week 2 (The Creation) as test case
    test_week = 2
    voice = "alloy"
    
    print(f"🔍 Starting Audio Generation Analysis for Week {test_week}")
    print(f"📅 Analysis Date: {datetime.now().isoformat()}")
    print(f"🌐 Using API: {API_BASE_URL}")
    print("="*80)
    
    # Analysis results
    analysis_data = {
        "analysis_metadata": {
            "timestamp": datetime.now().isoformat(),
            "week_number": test_week,
            "week_title": "Week 2: The Creation",
            "api_endpoint": API_BASE_URL,
            "voice_used": voice
        },
        "audio_generations": {}
    }
    
    # Test all three durations
    durations = [
        {'key': '5min', 'frontend_name': 'short', 'description': 'Short (5 Min)'},
        {'key': '15min', 'frontend_name': 'medium', 'description': 'Medium (15 Min)'},
        {'key': '30min', 'frontend_name': 'long', 'description': 'Long (30 Min)'}
    ]
    
    for duration_info in durations:
        duration = duration_info['key']
        frontend_name = duration_info['frontend_name']
        description = duration_info['description']
        
        print(f"\n🎵 Generating {description} audio summary...")
        print("-" * 60)
        
        try:
            # Prepare API request
            request_data = {
                "week_number": test_week,
                "duration": duration,
                "voice": voice
            }
            
            print(f"� API Request: {request_data}")
            
            # Make API call
            start_time = time.time()
            
            response = requests.post(
                f"{API_BASE_URL}/cfm/audio-summary",
                json=request_data,
                headers={"Content-Type": "application/json"},
                timeout=300  # 5 minute timeout
            )
            
            generation_time = time.time() - start_time
            
            if response.status_code == 200:
                result = response.json()
                
                print(f"✅ Generated {description} successfully in {generation_time:.2f}s")
                print(f"📊 Response keys: {list(result.keys())}")
                
                # Extract and analyze the script if available
                script = result.get('audio_script', '') or result.get('script', '')
                audio_files = result.get('audio_files') or {}
                
                print(f"📊 Script length: {len(script)} characters")
                print(f"📊 Script word count: ~{len(script.split())} words")
                print(f"🎵 Audio files: {list(audio_files.keys()) if audio_files else 'None'}")
                
                # Store analysis data
                analysis_data["audio_generations"][frontend_name] = {
                    "request_data": request_data,
                    "response_data": result,
                    "script": script,
                    "audio_files_keys": list(audio_files.keys()) if audio_files else [],
                    "generation_time_seconds": round(generation_time, 2),
                    "script_character_count": len(script),
                    "script_word_count": len(script.split()),
                    "api_status_code": response.status_code,
                    "duration_key": duration,
                    "description": description
                }
                
                # Show a preview of the generated script
                if script:
                    preview = script[:300] + "..." if len(script) > 300 else script
                    print(f"📖 Script preview: {preview}")
                else:
                    print("⚠️  No script content in response")
                
            else:
                print(f"❌ API Error: {response.status_code}")
                error_text = response.text
                print(f"❌ Error details: {error_text}")
                
                analysis_data["audio_generations"][frontend_name] = {
                    "request_data": request_data,
                    "error": f"HTTP {response.status_code}: {error_text}",
                    "generation_time_seconds": round(generation_time, 2),
                    "script_character_count": 0,
                    "script_word_count": 0,
                    "api_status_code": response.status_code,
                    "duration_key": duration,
                    "description": description
                }
                
        except Exception as e:
            print(f"❌ Exception during {description} generation: {e}")
            analysis_data["audio_generations"][frontend_name] = {
                "request_data": request_data if 'request_data' in locals() else None,
                "error": str(e),
                "generation_time_seconds": None,
                "script_character_count": 0,
                "script_word_count": 0,
                "duration_key": duration,
                "description": description
            }
    
    # Load the system prompts for context (from local files)
    try:
        import sys
        sys.path.append('/Users/derickjones/Documents/VS-Code/solo_founder/backend')
        from search.prompts import CFM_AUDIO_SUMMARY_PROMPTS
        
        analysis_data["system_prompts"] = CFM_AUDIO_SUMMARY_PROMPTS
        print(f"\n📋 System prompts loaded: {list(CFM_AUDIO_SUMMARY_PROMPTS.keys())}")
    except Exception as e:
        print(f"⚠️  Could not load system prompts: {e}")
        analysis_data["system_prompts"] = {"error": str(e)}
    
    # Save analysis to file
    output_file = Path("/Users/derickjones/Documents/VS-Code/solo_founder/audio_generation_analysis.json")
    print(f"\n💾 Saving comprehensive analysis to {output_file}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(analysis_data, f, indent=2, ensure_ascii=False)
    
    print("✅ Analysis complete!")
    
    # Summary statistics
    print("\n📈 SUMMARY STATISTICS")
    print("="*50)
    for frontend_name in ['short', 'medium', 'long']:
        data = analysis_data["audio_generations"].get(frontend_name, {})
        if "error" not in data:
            print(f"{data.get('description', frontend_name.upper())}: "
                  f"{data.get('script_word_count', 0)} words, "
                  f"{data.get('script_character_count', 0)} chars, "
                  f"{data.get('generation_time_seconds', 0)}s")
        else:
            print(f"{data.get('description', frontend_name.upper())}: "
                  f"ERROR - {data.get('error', 'Unknown')}")
    
    print(f"\n🎯 Comprehensive analysis saved to: {output_file}")
    print("📋 File includes:")
    print("   • System prompts for all durations")
    print("   • Generated scripts and metadata")
    print("   • Audio generation timing data")
    print("   • API request/response details")
    print("   • Ready for Grok analysis!")
    
    return output_file

if __name__ == "__main__":
    analyze_audio_generation()