#!/usr/bin/env python3
"""
Podcast Script Generator
Pre-generates podcast scripts for all CFM weeks and study levels using Grok AI

Updated with improved prompts for cohesive, engaging solo monologue podcasts.
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
# Output directly to frontend/public/podcasts for instant loading (no copying needed)
OUTPUT_DIR = SCRIPT_DIR.parent.parent.parent / "frontend" / "public" / "podcasts"

# ============================================================================
# NEW PODCAST PROMPT STRUCTURE
# ============================================================================

TAGLINE = "Welcome to the Come Follow Me Podcast by Gospel Study App."

BASE_PODCAST_PROMPT = """You are a warm, experienced Latter-day Saint gospel teacher delivering a captivating solo monologue podcast episode, like an engaging seminary class, institute lesson, or BYU religion lecture. Your goal is to draw listeners into the scriptures through vivid storytelling, thoughtful questions, and seamless doctrinal connections that spark spiritual insight and leave them eager for more.

**MANDATORY OPENING**: Begin every script EXACTLY with: "{tagline}" followed immediately by a vivid hook — no additional greetings or preamble.

**STYLE AND FLOW**:
- Speak conversationally and reverently, directly to the listener ("you", "your").
- Build a cohesive narrative arc: start with an immersive scene or question, develop themes inductively, connect scriptures organically, and close reflectively.
- Use smooth transitions ("This truth leads us to...", "Building on that vision...", "Notice how this pattern continues in...").
- Weave in bundle content naturally — quote scriptures verbatim with references, but integrate them into the flow.
- Reveal insights organically through questions and connections — NEVER use phrases like "fresh insight", "aha moment", "here's something interesting", "here's a fresh insight".
- Vary pause phrasing naturally (e.g., "Pause to let that resonate.", "Take a quiet moment.", "Let that truth settle in your heart.", "Reflect on that for a second.").
- End with a reflective summary and specific invitations to act/ponder.

**MANDATES**:
- Output ONLY the pure spoken script — continuous prose, ready for text-to-speech.
- No meta commentary, no headings, no bullet points, no JSON, no word counts.
- No personal testimony ("I testify", "I know", "I bear witness").
- No references to previous weeks or next week — focus only on this week's content.
- Stay strictly within the provided bundle content and official Church sources.

**STRUCTURE** (unified story arc):
1. Tagline + vivid opening hook (scene, question, or restored context from Joseph Smith).
2. Develop core themes with seamless scripture integration and connections.
3. Deepen understanding through cross-references and applications.
4. Close with reflection and invitations to apply what was learned.
""".format(tagline=TAGLINE)

# Level-specific prompt additions
CFM_PODCAST_PROMPTS = {
    'essential': BASE_PODCAST_PROMPT + """

**ESSENTIAL LEVEL**: Simple, clear, inspiring — like a warm seminary teacher.
- Focus on foundational principles, relatable stories, and personal/family application.
- Use gentle language and shorter sentences.
- One main invitation at the end.
- Target: ~800-1,200 words (~5-8 minutes).
""",

    'connected': BASE_PODCAST_PROMPT + """

**CONNECTED LEVEL**: Balanced depth with beautiful scriptural patterns — like an experienced institute teacher.
- Emphasize cross-references across standard works and modern prophetic teachings.
- Build excitement through pattern recognition and connections.
- Use 2-3 specific invitations (individual, family, journaling).
- Target: ~1,200-1,800 words (~8-12 minutes).
""",

    'scholarly': BASE_PODCAST_PROMPT + """

**SCHOLARLY LEVEL**: Layered doctrinal and historical depth — like a revered BYU religion professor.
- Include typology, linguistic notes (only if in bundle), JST context, and prophetic patterns.
- Use elevated but accessible language.
- Multiple invitations (personal study, prayer, family discussion, temple reflection).
- Target: ~1,800-2,500 words (~12-17 minutes).
"""
}

# Forbidden phrases to check and warn about
FORBIDDEN_PHRASES = [
    "fresh insight",
    "aha moment",
    "here's something interesting",
    "here's a fresh insight",
    "I testify",
    "I bear testimony",
    "I bear witness",
    "this script",
    "in this episode",
    "next week",
    "last week",
    "previous week",
]


def get_podcast_prompt(week_number: int, title: str, date_range: str,
                       cfm_lesson_content: dict, scripture_content: list,
                       study_level: str) -> str:
    """Build the prompt for generating podcast script using new structure"""
    
    # Get level-specific prompt
    level_prompt = CFM_PODCAST_PROMPTS.get(study_level, CFM_PODCAST_PROMPTS['essential'])
    
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
        for scripture in scripture_content[:20]:  # Limit to first 20 to avoid token overflow
            if isinstance(scripture, dict):
                scripture_text += f"\n{scripture.get('reference', '')}: {scripture.get('text', '')}\n"
            elif isinstance(scripture, str):
                scripture_text += f"\n{scripture}\n"
    
    prompt = f"""{level_prompt}

SOURCE CONTENT FOR WEEK {week_number}: "{title}" ({date_range})
================================================================================

CFM LESSON:
{cfm_text}

SCRIPTURES:
{scripture_text if scripture_text else "Scripture content is embedded in the CFM lesson above."}

================================================================================

**ACCURACY**: Quote ONLY from bundle content with exact references. Never add or fabricate.

**RETURN ONLY THE SPOKEN SCRIPT TEXT** — beginning with the tagline: "{TAGLINE}"
"""
    
    return prompt


def clean_script_text(script_text: str) -> tuple[str, list]:
    """
    Post-process the generated script:
    - Strip markdown/code fences
    - Ensure starts with tagline
    - Check for forbidden phrases
    
    Returns: (cleaned_text, list_of_warnings)
    """
    warnings = []
    
    # Strip any accidental markdown or code fences
    script_text = re.sub(r'^```(?:text)?\n?', '', script_text)
    script_text = re.sub(r'\n?```$', '', script_text)
    script_text = script_text.strip()
    
    # Check if script starts with tagline
    if not script_text.startswith(TAGLINE):
        # Try to find and fix if tagline is close to the start
        if TAGLINE in script_text[:200]:
            idx = script_text.index(TAGLINE)
            script_text = script_text[idx:]
            warnings.append(f"⚠️  Fixed: Removed {idx} chars before tagline")
        else:
            # Prepend tagline if missing entirely
            script_text = TAGLINE + " " + script_text
            warnings.append("⚠️  Fixed: Prepended missing tagline")
    
    # Check for forbidden phrases
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in script_text.lower():
            warnings.append(f"⚠️  Warning: Found forbidden phrase '{phrase}'")
    
    return script_text, warnings


def generate_podcast_script(week_number: int, study_level: str) -> dict:
    """Generate podcast script for a single week and study level"""
    
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
    
    # Build prompt with new structure
    prompt = get_podcast_prompt(
        week_number=week_number,
        title=title,
        date_range=date_range,
        cfm_lesson_content=cfm_lesson_content,
        scripture_content=scripture_content,
        study_level=study_level
    )
    
    print(f"🎙️ Generating {study_level} episode for Week {week_number}: {title[:50]}...")
    
    try:
        # Call Grok API
        completion = client.chat.completions.create(
            model="grok-3-latest",
            messages=[
                {
                    "role": "system",
                    "content": f"You are an engaging scripture study podcast host. Begin every response with exactly: \"{TAGLINE}\" then immediately continue with your content. Return only the spoken script text, ready for text-to-speech. No formatting, no JSON, no meta commentary."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=6000
        )
        
        raw_script = completion.choices[0].message.content.strip()
        
        # Post-process: clean and validate the script
        script_text, warnings = clean_script_text(raw_script)
        
        # Print any warnings
        for warning in warnings:
            print(f"   {warning}")
        
        # Calculate character count and estimate duration
        char_count = len(script_text)
        word_count = len(script_text.split())
        # Average speaking rate: ~150 words per minute
        estimated_minutes = round(word_count / 150, 1)
        
        # Create result object
        result = {
            "week_number": week_number,
            "title": title,
            "date_range": date_range,
            "study_level": study_level,
            "duration_estimate": f"~{estimated_minutes} minutes",
            "word_count": word_count,
            "character_count": char_count,
            "script": script_text,
            "generated_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source_week_file": str(week_file.name)
        }
        
        print(f"✅ Generated {study_level} script: {word_count} words, ~{estimated_minutes} min")
        return result
        
    except Exception as e:
        print(f"❌ Error generating Week {week_number} {study_level}: {e}")
        return None


def save_podcast_script(week_number: int, study_level: str, podcast_data: dict):
    """Save podcast script to a JSON file"""
    
    # Ensure output directory exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save individual file
    output_file = OUTPUT_DIR / f"podcast_week_{week_number:02d}_{study_level}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(podcast_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved: {output_file.name}")


def main():
    parser = argparse.ArgumentParser(description='Generate podcast scripts for CFM weeks')
    parser.add_argument('--week', type=int, help='Generate for a single week')
    parser.add_argument('--level', type=str, choices=['essential', 'connected', 'scholarly', 'all'], 
                        default='all', help='Study level to generate')
    parser.add_argument('--start', type=int, default=1, help='Start week (inclusive)')
    parser.add_argument('--end', type=int, default=8, help='End week (inclusive)')
    parser.add_argument('--force', action='store_true', help='Regenerate even if file exists')
    
    args = parser.parse_args()
    
    # Determine which weeks to generate
    if args.week:
        weeks = [args.week]
    else:
        weeks = list(range(args.start, args.end + 1))
    
    # Determine which levels to generate
    if args.level == 'all':
        levels = ['essential', 'connected', 'scholarly']
    else:
        levels = [args.level]
    
    print(f"\n🎙️ Podcast Script Generator (v2 - Improved Prompts)")
    print(f"=" * 60)
    print(f"Weeks: {weeks[0]} - {weeks[-1]} ({len(weeks)} weeks)")
    print(f"Levels: {', '.join(levels)}")
    print(f"Total scripts to generate: {len(weeks) * len(levels)}")
    print(f"Force regenerate: {args.force}")
    print(f"=" * 60 + "\n")
    
    # Generate podcasts
    generated = 0
    failed = 0
    skipped = 0
    
    for week in weeks:
        for level in levels:
            # Check if already exists
            output_file = OUTPUT_DIR / f"podcast_week_{week:02d}_{level}.json"
            if output_file.exists() and not args.force:
                print(f"⏭️  Skipping Week {week} {level} (already exists, use --force to regenerate)")
                skipped += 1
                continue
            
            podcast_data = generate_podcast_script(week, level)
            
            if podcast_data:
                save_podcast_script(week, level, podcast_data)
                generated += 1
            else:
                failed += 1
            
            # Rate limiting - pause between API calls
            if week != weeks[-1] or level != levels[-1]:
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
