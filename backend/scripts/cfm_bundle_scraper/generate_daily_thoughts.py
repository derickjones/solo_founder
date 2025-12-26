#!/usr/bin/env python3
"""
Daily Spiritual Thought Generator
Generates 7 daily spiritual thoughts for each CFM week using Grok AI
"""

import os
import json
import time
import re
from pathlib import Path
from openai import OpenAI

# Initialize Grok client
client = OpenAI(
    api_key=os.environ.get("XAI_API_KEY"),
    base_url="https://api.x.ai/v1",
)

# Paths
SCRIPT_DIR = Path(__file__).parent
CFM_2026_DIR = SCRIPT_DIR / "2026"
OUTPUT_DIR = SCRIPT_DIR / "2026_daily_thoughts"


def get_generation_prompt(week_number: int, title: str, date_range: str, 
                          cfm_lesson_content: dict, scripture_content: list) -> str:
    """Build the prompt for generating daily thoughts"""
    
    # Format CFM lesson content
    cfm_text = ""
    if cfm_lesson_content:
        cfm_text += f"Title: {cfm_lesson_content.get('title', '')}\n\n"
        cfm_text += f"Introduction: {cfm_lesson_content.get('introduction', '')}\n\n"
        
        # Learning at home/church sections
        learning_sections = cfm_lesson_content.get('learning_at_home_church', [])
        if learning_sections:
            cfm_text += "LEARNING AT HOME AND CHURCH:\n"
            for section in learning_sections:
                cfm_text += f"\n{section.get('title', '')}:\n{section.get('content', '')}\n"
        
        # Teaching children sections
        teaching_sections = cfm_lesson_content.get('teaching_children', [])
        if teaching_sections:
            cfm_text += "\nTEACHING CHILDREN:\n"
            for section in teaching_sections:
                cfm_text += f"\n{section.get('title', '')}:\n{section.get('content', '')}\n"
    
    # Format scripture content
    scripture_text = ""
    if scripture_content:
        for scripture in scripture_content:
            if isinstance(scripture, dict):
                scripture_text += f"\n{scripture.get('reference', '')}: {scripture.get('text', '')}\n"
            elif isinstance(scripture, str):
                scripture_text += f"\n{scripture}\n"
    
    prompt = f"""You are a scripture study assistant creating daily spiritual thoughts for Latter-day Saint families studying Come Follow Me.

TASK: Generate 7 daily spiritual thoughts for CFM Week {week_number}: "{title}" covering {date_range}.

SOURCE CONTENT (use ONLY this material - do not invent or hallucinate):
---
CFM LESSON:
{cfm_text}

SCRIPTURES:
{scripture_text if scripture_text else "Scripture content is embedded in the CFM lesson above. Extract scripture references and quotes from there."}
---

STRUCTURE:
- Day 1 (Sunday): Week Overview - introduce the week's main themes
- Days 2-6 (Monday-Friday): Daily themes based on content (choose from: Identity, Challenges, Growth, Faith, Covenant, Service, Repentance, Revelation, Obedience, Hope, Purpose, Deliverance, Grace, Worship, Relationships, Blessings)
- Day 7 (Saturday): Week Summary - tie together the week's learning

FOR EACH DAY, PROVIDE:
- day: (1-7)
- day_name: (Sunday-Saturday)
- theme: (as described above)
- title: (engaging 3-6 word title)
- scripture:
  - reference: (exact scripture reference from the week's reading)
  - text: (verbatim quote - 1-3 verses, copy exactly from source)
- thought: (4-6 sentences connecting the scripture to daily life, drawn from CFM content)
- application: (one specific, actionable suggestion for the day)
- question: (one reflective question for personal pondering or family discussion)
- historical_context: (OPTIONAL - include ONLY if the CFM lesson explicitly provides historical background about this scripture or time period. If no historical context exists in the source material, omit this field entirely. Never invent historical facts.)

GUIDELINES:
- Each day's content should take ~3 minutes to read
- Mix well-known scriptures with lesser-known gems from the week's reading
- Make applications practical and achievable
- Questions should invite genuine reflection, not yes/no answers
- Write in a warm, inviting tone suitable for all ages
- All content must be traceable to the provided source material

OUTPUT FORMAT:
Return ONLY valid JSON with no additional text or markdown formatting:
{{
  "week_number": {week_number},
  "title": "{title}",
  "date_range": "{date_range}",
  "days": [
    {{
      "day": 1,
      "day_name": "Sunday",
      "theme": "Week Overview",
      "title": "...",
      "scripture": {{
        "reference": "...",
        "text": "..."
      }},
      "thought": "...",
      "application": "...",
      "question": "..."
    }}
  ]
}}"""
    
    return prompt


def generate_daily_thoughts(week_number: int) -> dict:
    """Generate daily thoughts for a single week"""
    
    # Load the CFM bundle for this week
    week_file = CFM_2026_DIR / f"cfm_2026_week_{week_number:02d}.json"
    
    if not week_file.exists():
        print(f"❌ Week {week_number} file not found: {week_file}")
        return None
    
    with open(week_file, 'r', encoding='utf-8') as f:
        bundle = json.load(f)
    
    # Extract content from bundle
    title = bundle.get('title', f'Week {week_number}')
    date_range = bundle.get('date_range', '')
    cfm_lesson_content = bundle.get('cfm_lesson_content', {})
    scripture_content = bundle.get('scripture_content', [])
    
    # Build prompt
    prompt = get_generation_prompt(
        week_number=week_number,
        title=title,
        date_range=date_range,
        cfm_lesson_content=cfm_lesson_content,
        scripture_content=scripture_content
    )
    
    print(f"🔄 Generating daily thoughts for Week {week_number}: {title[:50]}...")
    
    try:
        # Call Grok API
        completion = client.chat.completions.create(
            model="grok-3-latest",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful scripture study assistant. Return only valid JSON with no markdown formatting or code blocks."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=4000
        )
        
        response_text = completion.choices[0].message.content.strip()
        
        # Clean up response - remove markdown code blocks if present
        if response_text.startswith("```"):
            response_text = re.sub(r'^```(?:json)?\n?', '', response_text)
            response_text = re.sub(r'\n?```$', '', response_text)
        
        # Parse JSON
        daily_thoughts = json.loads(response_text)
        
        # Add metadata
        daily_thoughts['generated_timestamp'] = time.strftime("%Y-%m-%d %H:%M:%S")
        daily_thoughts['source_week_file'] = str(week_file.name)
        
        print(f"✅ Generated {len(daily_thoughts.get('days', []))} daily thoughts for Week {week_number}")
        return daily_thoughts
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing error for Week {week_number}: {e}")
        print(f"Response was: {response_text[:500]}...")
        return None
    except Exception as e:
        print(f"❌ Error generating Week {week_number}: {e}")
        return None


def save_daily_thoughts(week_number: int, daily_thoughts: dict):
    """Save daily thoughts to a JSON file"""
    
    # Create output directory if it doesn't exist
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    output_file = OUTPUT_DIR / f"daily_thoughts_week_{week_number:02d}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(daily_thoughts, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved: {output_file}")


def generate_all_weeks(start_week: int = 1, end_week: int = 52, delay: float = 2.0):
    """Generate daily thoughts for all weeks"""
    
    print(f"🚀 Starting generation for weeks {start_week} to {end_week}")
    print(f"   Output directory: {OUTPUT_DIR}")
    print("-" * 50)
    
    successful = 0
    failed = []
    
    for week in range(start_week, end_week + 1):
        daily_thoughts = generate_daily_thoughts(week)
        
        if daily_thoughts:
            save_daily_thoughts(week, daily_thoughts)
            successful += 1
        else:
            failed.append(week)
        
        # Rate limiting - be respectful to the API
        if week < end_week:
            print(f"⏳ Waiting {delay}s before next request...")
            time.sleep(delay)
    
    print("-" * 50)
    print(f"✅ Successfully generated: {successful} weeks")
    if failed:
        print(f"❌ Failed weeks: {failed}")
    
    return successful, failed


def generate_single_week(week_number: int):
    """Generate daily thoughts for a single week"""
    
    daily_thoughts = generate_daily_thoughts(week_number)
    
    if daily_thoughts:
        save_daily_thoughts(week_number, daily_thoughts)
        print(f"\n📖 Preview of Week {week_number}:")
        print(json.dumps(daily_thoughts['days'][0], indent=2))
        return True
    
    return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate Daily Spiritual Thoughts for CFM')
    parser.add_argument('--week', type=int, help='Generate for a single week (1-52)')
    parser.add_argument('--start', type=int, default=1, help='Start week (default: 1)')
    parser.add_argument('--end', type=int, default=52, help='End week (default: 52)')
    parser.add_argument('--delay', type=float, default=2.0, help='Delay between API calls in seconds (default: 2.0)')
    
    args = parser.parse_args()
    
    # Check for API key
    if not os.environ.get("XAI_API_KEY"):
        print("❌ XAI_API_KEY environment variable not set")
        print("   Set it with: export XAI_API_KEY='your-api-key'")
        exit(1)
    
    if args.week:
        # Generate single week
        generate_single_week(args.week)
    else:
        # Generate all weeks in range
        generate_all_weeks(args.start, args.end, args.delay)
