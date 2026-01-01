#!/usr/bin/env python3
"""
CFM Lesson Plans Generator
Pre-generates lesson plans for all CFM weeks and audience types using Grok AI

Generates teaching materials for adults, youth, or children.
"""

import os
import json
import time
import re
import argparse
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
# Output directly to frontend/public/lesson_plans for instant loading
OUTPUT_DIR = SCRIPT_DIR.parent.parent.parent / "frontend" / "public" / "lesson_plans"

# ============================================================================
# CFM LESSON PLAN PROMPTS (from prompts.py)
# ============================================================================

BASE_SYSTEM_PROMPT = """
You are a deeply faithful, testimony-bearing Latter-day Saint scholar who has spent decades studying the scriptures and modern revelation. 
You answer every question with warmth, clarity, and exact citations like (Alma 32:21), (Oct 2024, Nelson, "Think Celestial!"), or (Saints vol. 2, ch. 12). 
Quote the full verse or talk excerpt when it matters. 
Never speculate, add personal opinion, or go beyond the retrieved sources. 
If the question touches temple ordinances, current membership policies, or anything sensitive, gently say: "This is sacred and personal—please speak with your bishop or refer to the temple recommend questions." 
When appropriate, share your testimony naturally without formulaic endings or repetitive phrases.
NEVER use phrases like "In conclusion", "In summary", "This truth has changed my life", or other formulaic testimony language.
Speak like a beloved BYU religion professor who actually believes every word.
"""

CFM_LESSON_PLAN_PROMPTS = {
    'adult': f"""{BASE_SYSTEM_PROMPT}

You are a faithful, experienced Latter-day Saint gospel teacher with decades of study in the scriptures and modern revelation. Create a comprehensive Come Follow Me study plan tailored for adults, focusing on deepening doctrinal understanding, practical life applications, and building personal testimony. Use a warm, scholarly tone like a trusted institute instructor.

When given a weekly CFM bundle (including scriptures, manual sections, and related resources), generate a structured plan with:

**Weekly Overview**: 3-4 sentences summarizing the core themes, historical context, and modern relevance.
**Doctrinal Key Points**: 5-7 main principles with exact scripture citations (e.g., Alma 32:21) and brief explanations tied to prophetic teachings.
**Personal Study Guide**: Daily breakdown for 7 days, with reading assignments, reflection questions, and cross-references to General Conference talks or Gospel Topics Essays.
**Group Discussion Ideas**: 6-8 thoughtful questions for family or class settings, encouraging sharing experiences and applications.
**Application Challenges**: 3-4 practical ways to live the principles in daily life, work, or church service.
**Testimony Builder**: A short paragraph connecting the week's themes to Jesus Christ and the Restoration, inviting personal reflection.

Keep the plan uplifting, accurate, and within 800-1200 words. Base everything on the provided bundle—never speculate or add unsupported opinions. Include 2-3 relevant quotes from living prophets to enhance depth.""",

    'youth': f"""{BASE_SYSTEM_PROMPT}

You are an enthusiastic, relatable Latter-day Saint youth leader who loves helping teenagers connect scripture to their everyday lives. Create an engaging Come Follow Me study plan for youth (ages 12-18), emphasizing fun activities, real-world applications, and building strong testimonies in a fast-paced world.

When given a weekly CFM bundle, generate a plan with:

**Youth Kickoff**: 2-3 energetic sentences on why this week's topic matters for teens today, with a fun hook like a modern analogy or question.
**Core Truths**: 4-6 key doctrines simplified for youth, with scripture quotes and ties to For the Strength of Youth principles.
**Daily Dive**: 7-day schedule with short readings, quick activities (e.g., journaling, memes, or group texts), and questions about school, friends, or future goals.
**Activity Ideas**: 4-5 interactive suggestions for quorum/class meetings, like role-plays, videos, or service projects.
**Real-Life Connections**: Ways to apply teachings to challenges like social media, peer pressure, or missionary prep.
**Faith Boost**: An encouraging wrap-up with a testimony-sharing prompt and a challenge to act on one principle.

Make it exciting and concise (600-900 words), using youth-friendly language. Incorporate elements like songs from the Youth Music album or short videos from Church resources. Stay faithful to the bundle content.""",

    'children': f"""{BASE_SYSTEM_PROMPT}

You are a loving, creative Primary teacher who delights in helping children (ages 3-11) discover the gospel through simple stories, activities, and fun. Create a joyful Come Follow Me study plan for children, focusing on building basic understanding, love for Jesus, and simple testimonies.

When given a weekly CFM bundle, generate a plan with:

**Fun Start**: 1-2 simple sentences introducing the week's theme with a child-friendly story or question.
**Key Gospel Ideas**: 3-5 basic principles explained in easy words, with short scripture verses and pictures or coloring ideas.
**Daily Adventures**: 7-day family activities, like drawing, singing songs from the Children's Songbook, or easy crafts tied to the scriptures.
**Story Time**: Retell a key scripture story in 200-300 words, with questions for kids to answer.
**Play and Learn**: 3-4 games or hands-on activities (e.g., building with blocks, acting out scenes) for home or Primary class.
**Jesus Connection**: A gentle reminder of how the lesson shows Jesus's love, with a prayer or testimony prompt.

Keep it short and visual (400-700 words), using repetitive, positive language. Suggest age adaptations for younger/older kids. Draw only from the bundle for accuracy."""
}

# Forbidden phrases to check
FORBIDDEN_PHRASES = [
    "In conclusion",
    "In summary", 
    "This truth has changed my life",
    "I testify",
    "I bear testimony",
    "I bear witness",
]


def get_lesson_plan_prompt(week_number: int, title: str, date_range: str,
                           cfm_lesson_content: dict, scripture_content: list,
                           audience: str) -> str:
    """Build the prompt for generating lesson plan"""
    
    audience_prompt = CFM_LESSON_PLAN_PROMPTS.get(audience, CFM_LESSON_PLAN_PROMPTS['adult'])
    
    cfm_text = ""
    if cfm_lesson_content:
        cfm_text += f"Title: {cfm_lesson_content.get('title', '')}\n\n"
        cfm_text += f"Introduction: {cfm_lesson_content.get('introduction', '')}\n\n"
        
        learning_sections = cfm_lesson_content.get('learning_at_home_church', [])
        if learning_sections:
            cfm_text += "LEARNING AT HOME AND CHURCH:\n"
            for section in learning_sections:
                cfm_text += f"\n{section.get('title', '')}:\n{section.get('content', '')}\n"
        
        teaching_sections = cfm_lesson_content.get('teaching_children', [])
        if teaching_sections:
            cfm_text += "\nTEACHING CHILDREN:\n"
            for section in teaching_sections:
                cfm_text += f"\n{section.get('title', '')}:\n{section.get('content', '')}\n"
    
    scripture_text = ""
    if scripture_content:
        for scripture in scripture_content[:20]:
            if isinstance(scripture, dict):
                scripture_text += f"\n{scripture.get('reference', '')}: {scripture.get('text', '')}\n"
            elif isinstance(scripture, str):
                scripture_text += f"\n{scripture}\n"
    
    return f"""{audience_prompt}

SOURCE CONTENT FOR WEEK {week_number}: "{title}" ({date_range})
================================================================================

CFM LESSON:
{cfm_text}

SCRIPTURES:
{scripture_text if scripture_text else "Scripture content is embedded in the CFM lesson above."}

================================================================================

**ACCURACY**: Quote ONLY from bundle content with exact references. Never add or fabricate.

**RETURN A COMPLETE LESSON PLAN** with all required sections using markdown formatting.
"""


def clean_lesson_text(lesson_text: str) -> tuple[str, list]:
    """
    Post-process the generated lesson plan:
    - Strip markdown code fences
    - Check for forbidden phrases
    
    Returns: (cleaned_text, list_of_warnings)
    """
    warnings = []
    
    # Strip any accidental code fences
    lesson_text = re.sub(r'^```(?:markdown|text)?\n?', '', lesson_text)
    lesson_text = re.sub(r'\n?```$', '', lesson_text)
    lesson_text = lesson_text.strip()
    
    # Check for forbidden phrases
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in lesson_text.lower():
            warnings.append(f"⚠️  Warning: Found forbidden phrase '{phrase}'")
    
    return lesson_text, warnings


def generate_lesson_plan(week_number: int, audience: str) -> dict:
    """Generate lesson plan for a single week and audience"""
    
    week_file = CFM_2026_DIR / f"cfm_2026_week_{week_number:02d}.json"
    
    if not week_file.exists():
        print(f"❌ Week {week_number} file not found: {week_file}")
        return None
    
    with open(week_file, 'r', encoding='utf-8') as f:
        bundle = json.load(f)
    
    title = bundle.get('title', f'Week {week_number}')
    date_range = bundle.get('date_range', '')
    cfm_lesson_content = bundle.get('cfm_lesson_content', {})
    scripture_content = bundle.get('scripture_content', [])
    
    prompt = get_lesson_plan_prompt(
        week_number=week_number,
        title=title,
        date_range=date_range,
        cfm_lesson_content=cfm_lesson_content,
        scripture_content=scripture_content,
        audience=audience
    )
    
    print(f"📚 Generating {audience} lesson plan for Week {week_number}: {title[:50]}...")
    
    try:
        completion = client.chat.completions.create(
            model="grok-3-latest",
            messages=[
                {
                    "role": "system",
                    "content": "You are a faithful LDS gospel teacher creating lesson plans. Return a complete markdown-formatted lesson plan with all required sections. No meta commentary, no JSON wrapping."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=6000
        )
        
        raw_lesson = completion.choices[0].message.content.strip()
        
        # Post-process
        lesson_content, warnings = clean_lesson_text(raw_lesson)
        
        for warning in warnings:
            print(f"   {warning}")
        
        word_count = len(lesson_content.split())
        char_count = len(lesson_content)
        
        result = {
            "week_number": week_number,
            "title": title,
            "date_range": date_range,
            "audience": audience,
            "word_count": word_count,
            "character_count": char_count,
            "content": lesson_content,
            "generated_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source_week_file": str(week_file.name)
        }
        
        print(f"✅ Generated {audience} lesson plan: {word_count} words")
        return result
        
    except Exception as e:
        print(f"❌ Error generating Week {week_number} {audience}: {e}")
        return None


def save_lesson_plan(week_number: int, audience: str, lesson_data: dict):
    """Save lesson plan to a JSON file"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"lesson_plan_week_{week_number:02d}_{audience}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(lesson_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved: {output_file.name}")


def main():
    parser = argparse.ArgumentParser(description='Generate lesson plans for CFM weeks')
    parser.add_argument('--week', type=int, help='Generate for a single week')
    parser.add_argument('--audience', type=str, choices=['adult', 'youth', 'children', 'all'], 
                        default='all', help='Audience to generate for')
    parser.add_argument('--start', type=int, default=1, help='Start week (inclusive)')
    parser.add_argument('--end', type=int, default=8, help='End week (inclusive)')
    parser.add_argument('--force', action='store_true', help='Regenerate even if file exists')
    
    args = parser.parse_args()
    
    if args.week:
        weeks = [args.week]
    else:
        weeks = list(range(args.start, args.end + 1))
    
    if args.audience == 'all':
        audiences = ['adult', 'youth', 'children']
    else:
        audiences = [args.audience]
    
    print(f"\n📚 CFM Lesson Plan Generator")
    print(f"=" * 60)
    print(f"Weeks: {weeks[0]} - {weeks[-1]} ({len(weeks)} weeks)")
    print(f"Audiences: {', '.join(audiences)}")
    print(f"Total lesson plans to generate: {len(weeks) * len(audiences)}")
    print(f"Force regenerate: {args.force}")
    print(f"=" * 60 + "\n")
    
    generated = 0
    failed = 0
    skipped = 0
    
    for week in weeks:
        for audience in audiences:
            output_file = OUTPUT_DIR / f"lesson_plan_week_{week:02d}_{audience}.json"
            if output_file.exists() and not args.force:
                print(f"⏭️  Skipping Week {week} {audience} (already exists, use --force to regenerate)")
                skipped += 1
                continue
            
            lesson_data = generate_lesson_plan(week, audience)
            
            if lesson_data:
                save_lesson_plan(week, audience, lesson_data)
                generated += 1
            else:
                failed += 1
            
            if week != weeks[-1] or audience != audiences[-1]:
                print("⏳ Waiting 2 seconds before next request...")
                time.sleep(2)
    
    print(f"\n{'=' * 60}")
    print(f"✅ Generation complete!")
    print(f"   Generated: {generated}")
    print(f"   Skipped: {skipped}")
    print(f"   Failed: {failed}")
    print(f"   Output directory: {OUTPUT_DIR}")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
