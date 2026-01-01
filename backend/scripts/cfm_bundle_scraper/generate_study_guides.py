#!/usr/bin/env python3
"""
CFM Study Guide Generator
Pre-generates written study guides for all CFM weeks and study levels using Grok AI

Generates structured written guides with sections like Week Overview, Key Scripture Moments, etc.
Different from podcast scripts (audio) - these are text-based study guides.
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
# Output directly to frontend/public/study_guides for instant loading
OUTPUT_DIR = SCRIPT_DIR.parent.parent.parent / "frontend" / "public" / "study_guides"

# ============================================================================
# CFM STUDY GUIDE PROMPTS (from prompts.py)
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

CFM_STUDY_GUIDE_PROMPTS = {
    'essential': f"""{BASE_SYSTEM_PROMPT}

ESSENTIAL CFM STUDY GUIDE CREATOR:
You are creating a simple, accessible study guide for Come Follow Me 2026 Old Testament that fires neurons through pattern recognition and hidden connections while maintaining clarity and spiritual focus.

When given a complete CFM weekly bundle with scriptures, seminary content, and resources, create an engaging study guide with:

**Week Overview**: Start with a compelling question or insight directly from the bundle that creates intrigue (e.g., "What did Moses discover about his divine identity that changed everything?").
**Key Scripture Moments**: 3-4 most important verses with dramatic reveals - use phrases like "Notice what happens next..." or "Here's the remarkable moment when..." Show patterns across prophets (Moses → Nephi → Joseph Smith).
**Hidden Connections**: Reveal surprising cross-references that illuminate meaning, showing how ancient principles solve modern problems.
**Pattern Discovery**: Help readers see recurring themes that connect distant scriptures in powerful ways.
**Simple Questions**: 5-6 reflection questions that build anticipation and create "aha moments" through proper sequencing.
**One Big Idea**: The single most important principle with historical context that transforms understanding.
**Living It**: 2-3 practical applications connecting ancient examples to today's challenges.
**Faith Builder**: Show how recent prophetic teachings echo these ancient truths, with exact citations from bundle sources only.

**ENGAGEMENT TECHNIQUES**:
- Create anticipation with "Notice this pattern..." or "This becomes powerful when we see..."
- Use dramatic questions from bundle content to hook attention
- Reveal connections that most people miss
- Show how past, present, and future principles align

**STRICT ACCURACY REQUIREMENTS**:
- Quote ONLY from provided bundle content - NEVER fabricate or paraphrase quotes
- Use exact scripture references with full verse text
- Cite prophets/apostles ONLY when their exact words appear in the bundle
- Mark interpretations as "This suggests..." not "The prophet taught..."
- If no prophetic quote exists in bundle, don't include one

Keep everything simple, encouraging, and practical. Use everyday language that creates excitement about discovery. Help people feel the Spirit and want to live the gospel better. Stay within 600-800 words total. Base everything strictly on the provided bundle content.""",

    'connected': f"""{BASE_SYSTEM_PROMPT}

CONNECTED CFM STUDY GUIDE CREATOR:
You are developing a comprehensive study guide for Come Follow Me 2026 Old Testament that fires neurons through advanced pattern recognition, historical context, and cross-reference webs while balancing depth with accessibility.

When provided with a complete CFM weekly bundle, create a detailed study guide including:

**Doctrinal Foundation**: Start with multiple perspectives analysis (e.g., "From Moses' view... from God's view...") to reveal layers of meaning in core gospel principles.
**Scripture Deep Dive**: 6-8 key passages showing escalating connections - use "This pattern appears in Moses, then Alma, then Joseph Smith..." Reveal archaeological insights and cultural context that transforms understanding.
**Historical Context**: Rich ancient world background from bundle sources that creates "time collapse moments" where past and present align.
**Pattern Recognition Web**: Extensive cross-references showing how this week connects to prophetic patterns across all dispensations.
**Discussion Framework**: 8-10 questions that progress from "What most people miss..." to profound applications, building anticipation for deeper insights.
**Gospel Connections**: Show how principles connect to Plan of Salvation with surprising scriptural parallels across standard works.
**Teaching Moments**: 3-4 ways to share these discoveries, emphasizing hidden connections and "aha moments."
**Seminary Synthesis**: Highlight 2-3 specific insights from Seminary manual that reveal advanced patterns teachers can adapt for deeper study.
**Personal Reflection**: Questions that help readers discover patterns in their own spiritual journey.
**Prophetic Echoes**: Show how modern prophetic teachings from bundle sources mirror ancient revelations in striking ways.

**ADVANCED ENGAGEMENT TECHNIQUES**:
- Use "Contradiction Resolution": Address apparent conflicts that reveal deeper truth
- Create "Mystery Setup": Pose intriguing questions early, resolve with satisfying insights
- Show "Generational Connections": Link to pioneer experiences and modern challenges
- Employ "Hidden Connection Reveals": Surprise readers with distant scripture connections

**STRICT ACCURACY REQUIREMENTS**:
- Quote ONLY from provided bundle content - NEVER fabricate quotes or sources
- All prophetic citations must match exact words from bundle materials
- Use "This pattern suggests..." rather than definitive interpretations without sources
- Verify all cross-references exist in provided materials
- If citing living prophets, use ONLY those appearing in the bundle with exact quotes

Where appropriate, include 2-3 relevant quotes from living prophets ONLY if their exact words appear in the provided bundle sources. Maintain scholarly accuracy while creating excitement about discovery. Connect Old Testament principles to modern prophetic teachings through documented parallels. Length: 800-1200 words.""",

    'scholarly': f"""{BASE_SYSTEM_PROMPT}

SCHOLARLY CFM STUDY GUIDE CREATOR:
You are crafting a sophisticated study guide for Come Follow Me 2026 Old Testament that ignites neurons through comprehensive pattern recognition, prophetic parallels, and deep historical context while maintaining the highest scholarly and spiritual standards.

When given a complete CFM weekly bundle with all resources, develop an in-depth study guide featuring:

**Theological Framework**: Multi-layered analysis revealing how doctrinal themes develop across dispensations with "Pattern Recognition Mastery" - showing identical principles from Adam to modern prophets.
**Exegetical Insights**: Hebrew terms, literary structures, and archaeological discoveries from bundle sources that create paradigm shifts in understanding.
**Prophetic Pattern Architecture**: Demonstrate divine patterns of revelation, covenant-making, and redemption using "Time Collapse Analysis" where ancient and modern merge.
**Cross-Reference Web Matrix**: Extensive connections revealing hidden relationships across all standard works that most readers never see.
**Historical and Cultural Context**: Rich background creating "aha moments" about ancient world parallels to modern discipleship.
**Contradiction Resolution**: Address apparent conflicts between passages that reveal profound theological truths when properly understood.
**Seminary Synthesis**: Extract advanced insights from Seminary manual that teachers can adapt for sophisticated adult study, emphasizing pattern discovery.
**Teaching Applications**: Multi-level discussion questions using "Escalating Stakes" - building from understanding to transformation to testimony.
**Modern Prophetic Convergence**: Show how contemporary prophetic teachings mirror ancient revelations with documented precision from bundle sources.
**Testimony Development**: Demonstrate how pattern recognition and deep study create unshakeable conviction in revealed truth.
**Additional Study**: Recommend bundle-based resources for further pattern exploration and cross-reference discovery.

**MASTER ENGAGEMENT TECHNIQUES**:
- **Mystery Architecture**: Set up intriguing questions early, build tension, provide satisfying revelations
- **Multiple Perspective Convergence**: Show same truth from various prophetic viewpoints across time
- **Hidden Connection Reveals**: Surprise scholars with distant but profound scriptural relationships  
- **Generational Pattern Mapping**: Connect ancient covenants to pioneer sacrifices to modern discipleship

**ABSOLUTE ACCURACY REQUIREMENTS**:
- Quote EXCLUSIVELY from provided bundle content - ZERO fabrication or approximation
- All prophetic citations must be verbatim from bundle materials with exact source attribution
- Hebrew/archaeological insights ONLY from provided scholarly sources in bundle
- Use "This pattern indicates..." for interpretive analysis without explicit source support
- Never cite conference talks, prophetic statements, or scholarly works not included in bundle
- If no modern prophetic connection exists in bundle, acknowledge limitation rather than invent

Use clear markdown headings (### or ####) for each required section exactly as listed. Include 2-3 relevant quotes from living prophets ONLY if their exact words appear verbatim in the provided bundle sources. Maintain the highest scholarly standards while preserving spiritual power through documented pattern recognition. Include extensive verified citations and cross-references. Target length: 1200-1800 words."""
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


def get_study_guide_prompt(week_number: int, title: str, date_range: str,
                           cfm_lesson_content: dict, scripture_content: list,
                           study_level: str) -> str:
    """Build the prompt for generating study guide"""
    
    level_prompt = CFM_STUDY_GUIDE_PROMPTS.get(study_level, CFM_STUDY_GUIDE_PROMPTS['essential'])
    
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
    
    return f"""{level_prompt}

SOURCE CONTENT FOR WEEK {week_number}: "{title}" ({date_range})
================================================================================

CFM LESSON:
{cfm_text}

SCRIPTURES:
{scripture_text if scripture_text else "Scripture content is embedded in the CFM lesson above."}

================================================================================

**ACCURACY**: Quote ONLY from bundle content with exact references. Never add or fabricate.

**RETURN A COMPLETE STUDY GUIDE** with all required sections using markdown formatting.
"""


def clean_guide_text(guide_text: str) -> tuple[str, list]:
    """
    Post-process the generated guide:
    - Strip markdown code fences
    - Check for forbidden phrases
    
    Returns: (cleaned_text, list_of_warnings)
    """
    warnings = []
    
    # Strip any accidental code fences
    guide_text = re.sub(r'^```(?:markdown|text)?\n?', '', guide_text)
    guide_text = re.sub(r'\n?```$', '', guide_text)
    guide_text = guide_text.strip()
    
    # Check for forbidden phrases
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in guide_text.lower():
            warnings.append(f"⚠️  Warning: Found forbidden phrase '{phrase}'")
    
    return guide_text, warnings


def generate_study_guide(week_number: int, study_level: str) -> dict:
    """Generate study guide for a single week and study level"""
    
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
    
    prompt = get_study_guide_prompt(
        week_number=week_number,
        title=title,
        date_range=date_range,
        cfm_lesson_content=cfm_lesson_content,
        scripture_content=scripture_content,
        study_level=study_level
    )
    
    print(f"📖 Generating {study_level} study guide for Week {week_number}: {title[:50]}...")
    
    try:
        completion = client.chat.completions.create(
            model="grok-3-latest",
            messages=[
                {
                    "role": "system",
                    "content": "You are a faithful LDS scholar creating written study guides. Return a complete markdown-formatted study guide with all required sections. No meta commentary, no JSON wrapping."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=6000
        )
        
        raw_guide = completion.choices[0].message.content.strip()
        
        # Post-process
        guide_content, warnings = clean_guide_text(raw_guide)
        
        for warning in warnings:
            print(f"   {warning}")
        
        word_count = len(guide_content.split())
        char_count = len(guide_content)
        
        result = {
            "week_number": week_number,
            "title": title,
            "date_range": date_range,
            "study_level": study_level,
            "word_count": word_count,
            "character_count": char_count,
            "content": guide_content,
            "generated_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source_week_file": str(week_file.name)
        }
        
        print(f"✅ Generated {study_level} study guide: {word_count} words")
        return result
        
    except Exception as e:
        print(f"❌ Error generating Week {week_number} {study_level}: {e}")
        return None


def save_study_guide(week_number: int, study_level: str, guide_data: dict):
    """Save study guide to a JSON file"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"study_guide_week_{week_number:02d}_{study_level}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(guide_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved: {output_file.name}")


def main():
    parser = argparse.ArgumentParser(description='Generate study guides for CFM weeks')
    parser.add_argument('--week', type=int, help='Generate for a single week')
    parser.add_argument('--level', type=str, choices=['essential', 'connected', 'scholarly', 'all'], 
                        default='all', help='Study level to generate')
    parser.add_argument('--start', type=int, default=1, help='Start week (inclusive)')
    parser.add_argument('--end', type=int, default=8, help='End week (inclusive)')
    parser.add_argument('--force', action='store_true', help='Regenerate even if file exists')
    
    args = parser.parse_args()
    
    if args.week:
        weeks = [args.week]
    else:
        weeks = list(range(args.start, args.end + 1))
    
    if args.level == 'all':
        levels = ['essential', 'connected', 'scholarly']
    else:
        levels = [args.level]
    
    print(f"\n📖 CFM Study Guide Generator")
    print(f"=" * 60)
    print(f"Weeks: {weeks[0]} - {weeks[-1]} ({len(weeks)} weeks)")
    print(f"Levels: {', '.join(levels)}")
    print(f"Total study guides to generate: {len(weeks) * len(levels)}")
    print(f"Force regenerate: {args.force}")
    print(f"=" * 60 + "\n")
    
    generated = 0
    failed = 0
    skipped = 0
    
    for week in weeks:
        for level in levels:
            output_file = OUTPUT_DIR / f"study_guide_week_{week:02d}_{level}.json"
            if output_file.exists() and not args.force:
                print(f"⏭️  Skipping Week {week} {level} (already exists, use --force to regenerate)")
                skipped += 1
                continue
            
            guide_data = generate_study_guide(week, level)
            
            if guide_data:
                save_study_guide(week, level, guide_data)
                generated += 1
            else:
                failed += 1
            
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
