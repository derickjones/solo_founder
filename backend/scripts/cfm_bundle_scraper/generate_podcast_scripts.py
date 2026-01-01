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
# CONVERSATION PODCAST PROMPT STRUCTURE
# ============================================================================

TAGLINE = "Welcome to the Come Follow Me Podcast by Gospel Study App."

# Speaker configuration
HOST_NAME = "Sarah"  # Female voice (aoede)
GUEST_NAME = "David"  # Male voice (alnilam)

BASE_PODCAST_PROMPT = """You are creating an ADDICTIVE, story-driven conversation between two Latter-day Saint scripture teachers that hooks listeners immediately and keeps them engaged. This dialogue podcast should feel like two brilliant professors discovering profound connections together—combining the intrigue of a mystery podcast with deep scriptural insight.

**SPEAKERS**:
- Sarah (host): Engaging, curious female teacher - poses intriguing questions, builds anticipation
- David (guest): Insightful male teacher - reveals surprising connections, provides scholarly depth

**MANDATORY OPENING**: Begin EXACTLY with Sarah saying: "{tagline} I'm Sarah." Then David responds: "And I'm {guest_name}."

**HOOK STRUCTURE (CRITICAL - First 3-5 segments after greeting):**
Start with ONE of these compelling hook types:
1. **Mystery Hook**: Pose a puzzling question that demands resolution (e.g., "Why did the Jews try to stone Jesus for three simple words?")
2. **Shocking Discovery**: Share an unexpected archaeological or historical finding
3. **Pattern Reveal Setup**: "I'm going to show you something hidden in plain sight across four different prophets..."
4. **Multi-Perspective Twist**: "What if I told you there are three completely different ways to read this same story?"
5. **"What Most People Miss"**: Start with something overlooked that transforms understanding

The hook should create curiosity that MUST be satisfied by listening further.

**CONVERSATION STYLE**:
- Natural back-and-forth dialogue with 2-4 sentences per speaking turn
- Build tension and anticipation—don't give everything away at once
- Use "Mystery Architecture": Set up intriguing questions early, explore, then provide satisfying reveals
- Sarah guides with curiosity: "Wait, what?", "That's fascinating, but how does...", "I need to understand..."
- David provides "aha moments": "Here's what shifts everything...", "Notice this pattern...", "Watch what happens..."
- Include moments of genuine discovery: "I never saw that!", "That's remarkable!", "This changes how I read..."
- Vary speaking turn length - quick exchanges for excitement, longer explanations for depth

**EDUCATIONAL SCAFFOLDING (Weave naturally into dialogue):**
- **Multi-Perspective Analysis**: Show ancient Israel's view, Christ's view, modern restoration view
- **Pattern Recognition**: Trace ONE theme across 2-4 dispensations (e.g., divine light: Psalms → Moses → Christ → D&C)
- **Historical Context**: Include 1-2 archaeological/cultural insights that create "time collapse moments"
- **Hidden Connections**: Reveal surprising cross-references most people miss
- **Plan of Salvation Links**: Connect symbols and covenants to the eternal plan
- **Prophetic Echoes**: Show how modern prophets mirror ancient revelations

**ENGAGEMENT TECHNIQUES**:
- Use "Notice this..." to draw attention to patterns
- Build with "Here's where it gets powerful..." before reveals
- Create anticipation: "Hold that question, we'll come back to it..."
- Surprise with "What most people don't know is..."
- Validate discovery: "Exactly! You just uncovered something profound."

**MANDATES**:
- Output ONLY a JSON array of dialogue segments ready for multi-voice TTS
- Each segment: {{"speaker": "Sarah" or "David", "text": "what they say"}}
- The tagline opening MUST be the first segment from Sarah
- No meta commentary, no stage directions, no [pause] markers
- No personal testimony ("I testify", "I bear witness")
- No references to previous/next weeks - focus only on this week's content
- Stay strictly within provided bundle content and official Church sources
- Quote scriptures verbatim with references when discussed

**DIALOGUE STRUCTURE**:
1. **Opening**: Tagline + greeting (1-2 segments)
2. **Hook**: Compelling mystery/discovery that demands attention (2-4 segments)
3. **Multi-Perspective Setup**: Frame the topic from multiple viewpoints (2-4 segments)
4. **Pattern Exploration**: Trace themes across dispensations with building excitement (4-8 segments)
5. **Historical Deep Dive**: Archaeological/cultural context creating "aha moments" (2-4 segments)
6. **Mystery Resolution**: Satisfy the opening hook with profound insight (2-3 segments)
7. **Hidden Connections**: Reveal surprising cross-references (3-5 segments)
8. **Modern Application**: How ancient patterns apply today (2-4 segments)
9. **Closing**: Powerful invitation based on discoveries made (2-3 segments)

**RETURN FORMAT**: Pure JSON array, no markdown, no code fences:
[
  {{"speaker": "Sarah", "text": "{tagline} I'm Sarah."}},
  {{"speaker": "David", "text": "And I'm {guest_name}. Happy to be here!"}},
  {{"speaker": "Sarah", "text": "David, I have to start with a question that's puzzled scholars for centuries..."}}
]
""".format(tagline=TAGLINE, guest_name=GUEST_NAME)

# Level-specific prompt additions
CFM_PODCAST_PROMPTS = {
    'essential': BASE_PODCAST_PROMPT + """

**ESSENTIAL LEVEL**: Accessible yet intriguing — like a captivating story for curious learners.

**HOOK REQUIREMENTS**:
- Start with a simple but compelling question or discovery
- Use "What most people miss..." or "Here's something surprising..."
- Make complex ideas feel accessible through story and wonder

**EDUCATIONAL WEAVING**:
- One clear multi-perspective moment (e.g., "From Moses' view... but from God's view...")
- Trace ONE simple pattern across 2-3 scriptures (e.g., "manna → bread of life → sacrament")
- Include ONE fascinating historical detail that creates connection
- Show how one symbol points to Christ in an unexpected way

**DIALOGUE FLOW**:
- Sarah asks curious questions that listeners would ask
- David reveals insights in simple, wonder-filled language
- Build one "aha moment" around a hidden connection
- Close with one clear, actionable invitation

**TARGET**: 20-30 dialogue segments (~7-10 minutes total)

**EXAMPLE HOOK**:
Sarah: "David, what if I told you that every time the Israelites ate breakfast in the wilderness, they were actually learning about Jesus Christ? Most people read right past this."
David: "That's exactly right, Sarah. Let me show you what's hidden in the manna story..."
""",

    'connected': BASE_PODCAST_PROMPT + """

**CONNECTED LEVEL**: Deeply engaging with mystery and revelation — like two professors making breakthrough discoveries together.

**HOOK REQUIREMENTS**:
- Open with an intriguing mystery or shocking archaeological discovery
- Use "Mystery Architecture": Set up tension that builds throughout the conversation
- Create a "Wait, what?" moment in the first 30 seconds

**EDUCATIONAL WEAVING**:
- Multi-perspective analysis: Show how ancient Israel, Christ, and modern Saints see the same truth differently
- Pattern Recognition Web: Trace ONE theme across 3-4 dispensations with building excitement
- Historical Deep Dive: Include 2-3 archaeological/cultural insights that transform understanding
- Hidden Connections: Reveal at least 2 surprising cross-references most people miss
- Plan of Salvation Link: Show how symbols connect to the eternal plan
- Prophetic Echoes: Demonstrate how modern prophets mirror ancient revelations

**DIALOGUE FLOW**:
- Sarah builds anticipation with progressive questions
- David provides escalating revelations
- Use "Notice this pattern..." repeatedly to build the web
- Create multiple "That's remarkable!" moments of genuine discovery
- Resolve the opening mystery with a powerful insight
- Include one "time collapse moment" where ancient and modern merge

**TARGET**: 35-50 dialogue segments (~12-17 minutes total)

**EXAMPLE HOOK**:
Sarah: "David, I'm going to start with something that puzzled me for years. In John 8:58, Jesus says three simple words—'Before Abraham was, I am'—and the Jews immediately pick up stones to kill Him. Why such an extreme reaction?"
David: "That's the perfect mystery to unlock the entire Old Testament, Sarah. To understand it, we need to go back 1,400 years to a burning bush..."
""",

    'scholarly': BASE_PODCAST_PROMPT + """

**SCHOLARLY LEVEL**: Intellectually addictive with layered mysteries — like a masterclass in scriptural detective work.

**HOOK REQUIREMENTS**:
- Open with a profound mystery, contradiction, or paradigm-shifting discovery
- Use multiple hook layers: historical puzzle → theological question → modern application mystery
- Create irresistible curiosity that demands resolution

**EDUCATIONAL WEAVING**:
- **Theological Framework**: Multi-layered perspective analysis revealing how doctrines develop across dispensations
- **Pattern Recognition Mastery**: Trace themes across 4+ dispensations showing divine consistency
- **Exegetical Insights**: Hebrew/Greek terms, JST context, literary structures creating paradigm shifts
- **Archaeological Deep Dives**: 2-3 historical/cultural discoveries that create "time collapse moments"
- **Cross-Reference Web Matrix**: Reveal extensive hidden connections across all standard works
- **Contradiction Resolution**: Address apparent conflicts that reveal profound truth when understood
- **Prophetic Pattern Architecture**: Demonstrate divine patterns of revelation, covenant-making, redemption
- **Plan of Salvation Integration**: Connect everything to the eternal plan with surprising parallels
- **Modern Prophetic Convergence**: Show contemporary teachings mirroring ancient revelations
- **Teaching Applications**: Include strategies for educators to share these discoveries

**DIALOGUE FLOW**:
- Sarah orchestrates multiple mystery layers with sophisticated questions
- David provides scholarly revelations with accessible explanations
- Build tension through "Contradiction Resolution" - apparent conflicts revealing deeper truth
- Use "Multiple Perspective Convergence" - same truth from various prophetic viewpoints
- Create "Generational Pattern Mapping" - connect ancient covenants to pioneer sacrifices to modern discipleship
- Include substantive exchanges with Hebrew/Greek insights, JST additions, typology
- Resolve mysteries with multiple satisfying revelations
- Both speakers contribute advanced observations and discoveries

**TARGET**: 50-70 dialogue segments (~17-24 minutes total)

**EXAMPLE HOOK**:
Sarah: "David, I want to start with a contradiction that troubled early Christian theologians. Genesis 1 says God created everything in six days and rested. But Moses 7:30 in the Pearl of Great Price shows Enoch weeping because entire worlds are being destroyed and recreated. How can God rest if He's constantly creating? And here's the deeper question: what does this apparent contradiction reveal about the nature of divine work that most people never see?"
David: "Sarah, that's brilliant—because resolving this contradiction unlocks the entire theology of eternal progression. Let me show you a pattern that connects Abraham 3, the temple, and President Nelson's recent teachings on eternal life..."
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

**RETURN ONLY A JSON ARRAY** of dialogue segments in this exact format:
[
  {{"speaker": "Sarah", "text": "{TAGLINE} I'm Sarah."}},
  {{"speaker": "David", "text": "And I'm {GUEST_NAME}. Happy to be here!"}}
]
"""
    
    return prompt


def clean_script_text(script_text: str) -> tuple:
    """
    Post-process the generated conversation script:
    - Strip markdown/code fences
    - Parse JSON array
    - Validate structure
    - Check for forbidden phrases
    
    Returns: (parsed_script_array, list_of_warnings)
    """
    warnings = []
    
    # Strip any accidental markdown or code fences
    script_text = re.sub(r'^```(?:json|text)?\n?', '', script_text)
    script_text = re.sub(r'\n?```$', '', script_text)
    script_text = script_text.strip()
    
    # Try to parse as JSON
    try:
        script_array = json.loads(script_text)
    except json.JSONDecodeError as e:
        warnings.append(f"⚠️  JSON parse error: {e}")
        # Try to find JSON array in the text
        json_match = re.search(r'\[.*\]', script_text, re.DOTALL)
        if json_match:
            try:
                script_array = json.loads(json_match.group(0))
                warnings.append("⚠️  Fixed: Extracted JSON from surrounding text")
            except:
                raise ValueError(f"Could not parse conversation script as JSON: {e}")
        else:
            raise ValueError(f"No JSON array found in response: {script_text[:200]}")
    
    # Validate structure
    if not isinstance(script_array, list):
        raise ValueError("Script must be a JSON array")
    
    if len(script_array) == 0:
        raise ValueError("Script array is empty")
    
    # Check first segment has tagline
    first_segment = script_array[0]
    if not isinstance(first_segment, dict) or 'speaker' not in first_segment or 'text' not in first_segment:
        warnings.append("⚠️  Warning: First segment missing speaker/text fields")
    elif TAGLINE not in first_segment.get('text', ''):
        warnings.append(f"⚠️  Warning: First segment missing tagline: {first_segment.get('text', '')[:50]}")
    
    # Check for forbidden phrases in all dialogue
    full_text = " ".join(seg.get('text', '') for seg in script_array)
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in full_text.lower():
            warnings.append(f"⚠️  Warning: Found forbidden phrase '{phrase}'")
    
    return script_array, warnings


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
                    "content": f"You are creating natural podcast conversations between Sarah (host) and David (guest). Return ONLY a pure JSON array of dialogue segments. Each segment: {{\"speaker\": \"Sarah\" or \"David\", \"text\": \"what they say\"}}. First segment MUST be Sarah saying: \"{TAGLINE} I'm Sarah.\" No markdown, no code fences, just the JSON array."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=8000
        )
        
        raw_script = completion.choices[0].message.content.strip()
        
        # Post-process: parse and validate the conversation script
        script_array, warnings = clean_script_text(raw_script)
        
        # Print any warnings
        for warning in warnings:
            print(f"   {warning}")
        
        # Calculate stats
        total_chars = sum(len(seg.get('text', '')) for seg in script_array)
        total_words = sum(len(seg.get('text', '').split()) for seg in script_array)
        segment_count = len(script_array)
        
        # Average speaking rate: ~150 words per minute
        estimated_minutes = round(total_words / 150, 1)
        
        # Create result object
        result = {
            "week_number": week_number,
            "title": title,
            "date_range": date_range,
            "study_level": study_level,
            "duration_estimate": f"~{estimated_minutes} minutes",
            "word_count": total_words,
            "character_count": total_chars,
            "segment_count": segment_count,
            "script": script_array,  # Array of {"speaker": "...", "text": "..."}
            "voices": {
                "Sarah": "aoede",  # Female host
                "David": "alnilam"  # Male guest
            },
            "generated_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "source_week_file": str(week_file.name)
        }
        
        print(f"✅ Generated {study_level} conversation: {segment_count} segments, {total_words} words, ~{estimated_minutes} min")
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
    
    print(f"\n🎙️ Podcast Script Generator (v3 - Conversation Format)")
    print(f"=" * 60)
    print(f"Format: Two-speaker conversation (Sarah + David)")
    print(f"Voices: Sarah (aoede/female), David (alnilam/male)")
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
