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
import random
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

# Speaker configuration - will be randomly assigned per script generation
# Female voice (aoede), Male voice (alnilam)
SPEAKERS = {
    "Sarah": "aoede",   # Female voice
    "David": "alnilam"  # Male voice
}


def get_random_host_guest():
    """Randomly select host and guest to alternate gender roles (50/50 chance)"""
    if random.random() < 0.5:
        return "Sarah", "David"  # Sarah hosts, David is guest
    else:
        return "David", "Sarah"  # David hosts, Sarah is guest


def get_base_podcast_prompt(host_name: str, guest_name: str) -> str:
    """Generate the base podcast prompt with dynamic host/guest assignment"""
    return f"""You are creating a natural, engaging conversation between two Latter-day Saint scripture teachers that captivates listeners with profound insights. This dialogue should feel like two knowledgeable friends discovering meaningful connections together—combining genuine curiosity with deep scriptural understanding.

**SPEAKERS**:
- {host_name} (host): Engaging, curious teacher - poses thoughtful questions, guides discovery
- {guest_name} (guest): Insightful teacher - shares meaningful connections, provides scholarly depth

**MANDATORY OPENING**: Begin EXACTLY with {host_name} saying: "{TAGLINE} I'm {host_name}." Then {guest_name} responds: "And I'm {guest_name}."

**CONVERSATION FLOW**:
Start with a compelling question or insight that naturally draws listeners in:
1. **Intriguing Opening**: Pose a meaningful question that creates genuine curiosity
2. **Discovery Pattern**: Share something profound that transforms understanding  
3. **Multi-Perspective Insight**: "What's fascinating is how this looks different when viewed from..."
4. **Connection Reveal**: "There's something remarkable happening across several scriptures..."
5. **"Often Overlooked"**: Point out significant details most readers miss

The opening should create natural curiosity and anticipation for meaningful discovery.

**CONVERSATION STYLE**:
- Natural, flowing dialogue with varied speaking turn lengths (2-6 sentences typically)
- Build understanding progressively—don't rush to conclusions
- Create organic discovery moments where insights emerge naturally
- {host_name} guides with genuine curiosity: "That's fascinating—help me understand...", "I'm intrigued by...", "What strikes me about this..."
- {guest_name} shares discoveries thoughtfully: "What I find remarkable...", "Here's what I think is significant...", "Notice how this connects..."
- Include authentic moments of realization: "I hadn't thought of it that way", "That's a profound connection", "This really deepens my understanding"
- Vary speaking patterns - sometimes quick exchanges, sometimes deeper explanations
- AVOID formulaic back-and-forth scripture citing - weave references naturally into the conversation

**EDUCATIONAL APPROACH (Integrate naturally into dialogue):**
- **Multi-Perspective Analysis**: Explore how different people/times understood the same truth
- **Pattern Recognition**: Trace meaningful themes across time periods naturally  
- **Historical Context**: Include relevant cultural/archaeological insights that illuminate the text
- **Meaningful Connections**: Reveal significant cross-references that enhance understanding
- **Gospel Integration**: Connect symbols and covenants to the plan of salvation
- **Prophetic Continuity**: Show how modern revelation builds on ancient foundations

**ENGAGEMENT TECHNIQUES**:
- Use "What strikes me..." to invite deeper consideration
- Build understanding with "Here's what I find meaningful..." 
- Create anticipation naturally: "There's something significant here that..."
- Surprise with "What many don't realize is..."
- Validate insights: "That's exactly right—you've uncovered something profound"

**MANDATES**:
- Output ONLY a JSON array of dialogue segments ready for multi-voice TTS
- Each segment: {{"speaker": "{host_name}" or "{guest_name}", "text": "what they say"}}
- The tagline opening MUST be the first segment from {host_name}
- No meta commentary, no stage directions, no [pause] markers
- No personal testimony ("I testify", "I bear witness")
- No references to previous/next weeks - focus only on this week's content
- Stay strictly within provided bundle content and official Church sources
- Quote scriptures verbatim with references when discussed
- COMPLETELY AVOID these specific words and phrases in ALL dialogue: "echoes", "echo", "aha moment", "fresh insight", "hook", "hooks", "kid activities", "children's activities", "time collapse"
- Make the conversation flow naturally - avoid rote scripture exchanges
- Use alternative phrasing: instead of "echoes" use "reflects" or "mirrors"; instead of "aha moment" use "realization" or "insight"; instead of "hook" use "opening" or "beginning"

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
  {{"speaker": "{host_name}", "text": "{TAGLINE} I'm {host_name}."}},
  {{"speaker": "{guest_name}", "text": "And I'm {guest_name}. Happy to be here!"}},
  {{"speaker": "{host_name}", "text": "{guest_name}, I have to start with a question that's puzzled scholars for centuries..."}}
]
"""


def get_level_specific_prompt(host_name: str, guest_name: str, study_level: str) -> str:
    """Get the complete prompt for a specific study level with dynamic host/guest names"""
    base_prompt = get_base_podcast_prompt(host_name, guest_name)
    
    level_additions = {
        'essential': f"""

**ESSENTIAL LEVEL**: Accessible yet meaningful — like a thoughtful conversation for curious learners.

**OPENING APPROACH**:
- Start with a simple but compelling question or observation
- Use "What's remarkable about this..." or "I've always wondered about..."
- Make complex ideas accessible through natural conversation and wonder

**EDUCATIONAL APPROACH**:
- One clear multi-perspective moment (e.g., "From Moses' view... but from God's perspective...")
- Trace ONE meaningful pattern across 2-3 scriptures naturally
- Include ONE fascinating historical detail that creates connection
- Show how one symbol points to Christ in a meaningful way

**CONVERSATION FLOW**:
- {host_name} asks questions that listeners naturally would ask
- {guest_name} shares insights in clear, wonder-filled language
- Build one moment of genuine realization around a meaningful connection
- Close with one clear, actionable invitation
- NEVER use the words: "echoes", "echo", "aha moment", "hook", "fresh insight"
- Use alternatives: "reflects", "mirrors", "realization", "insight", "opening", "beginning"

**TARGET**: 20-30 dialogue segments (~7-10 minutes total)

**EXAMPLE OPENING**:
{host_name}: "{guest_name}, I've been thinking about something. Every time the Israelites ate breakfast in the wilderness, there was actually a profound lesson about Jesus Christ happening. Most people read right past this."
{guest_name}: "That's such a beautiful observation, {host_name}. Let me share what I've discovered about the manna story..."
""",

        'connected': f"""

**CONNECTED LEVEL**: Deeply engaging with meaningful discovery — like two teachers making genuine breakthroughs together.

**OPENING APPROACH**:
- Open with an intriguing question or thoughtful archaeological discovery
- Create genuine curiosity that builds throughout the conversation
- Start with something that makes listeners think "I never considered that"

**EDUCATIONAL APPROACH**:
- Multi-perspective analysis: Show how ancient Israel, Christ, and modern Saints see the same truth differently
- Pattern Recognition: Trace ONE theme across 3-4 dispensations with building understanding
- Historical Insight: Include 2-3 archaeological/cultural insights that transform understanding
- Meaningful Connections: Reveal at least 2 significant cross-references most people miss
- Gospel Integration: Show how symbols connect to the plan of salvation
- Prophetic Continuity: Demonstrate how modern prophets build on ancient revelations

**CONVERSATION FLOW**:
- {host_name} builds understanding with progressive questions
- {guest_name} provides escalating insights and revelations
- Use "What I find fascinating..." to build the understanding web
- Create multiple moments of genuine discovery and realization
- Resolve the opening question with a profound insight
- Include one moment where ancient and modern feel immediately connected
- NEVER use the words: "echoes", "echo", "aha moment", "hook", "fresh insight"
- Use alternatives: "reflects", "mirrors", "realization", "insight", "opening", "beginning"

**TARGET**: 35-50 dialogue segments (~12-17 minutes total)

**EXAMPLE OPENING**:
{host_name}: "{guest_name}, I want to start with something that has puzzled me. In John 8:58, Jesus says three simple words—'Before Abraham was, I am'—and the Jews immediately pick up stones to kill Him. Why such an extreme reaction?"
{guest_name}: "That's the perfect question to unlock so much understanding about the Old Testament, {host_name}. To really grasp this, we need to go back 1,400 years to a burning bush..."
""",

        'scholarly': f"""

**SCHOLARLY LEVEL**: Intellectually engaging with layered understanding — like a masterclass in scriptural analysis.

**OPENING APPROACH**:
- Open with a profound question, apparent contradiction, or paradigm-shifting discovery
- Create multiple layers of curiosity: historical puzzle → theological question → modern application
- Generate compelling intellectual curiosity that demands deeper exploration

**EDUCATIONAL APPROACH**:
- **Theological Framework**: Multi-layered perspective analysis showing how doctrines develop across dispensations
- **Pattern Recognition Mastery**: Trace themes across 4+ dispensations showing divine consistency
- **Exegetical Insights**: Hebrew/Greek terms, JST context, literary structures creating paradigm shifts
- **Archaeological Deep Analysis**: 2-3 historical/cultural discoveries that make ancient events immediate and real
- **Cross-Reference Integration**: Reveal extensive meaningful connections across all standard works
- **Apparent Contradiction Resolution**: Address seeming conflicts that reveal profound truth when understood
- **Prophetic Pattern Architecture**: Demonstrate divine patterns of revelation, covenant-making, redemption
- **Plan of Salvation Integration**: Connect everything to the eternal plan with sophisticated parallels
- **Modern Prophetic Convergence**: Show contemporary teachings building on ancient revelations
- **Adult Learning Focus**: Maintain sophisticated discussion without children's activities or simplifications

**CONVERSATION FLOW**:
- {host_name} orchestrates multiple layers of understanding with sophisticated questions
- {guest_name} provides scholarly insights with accessible explanations
- Build understanding through "Apparent Contradiction Resolution" - seeming conflicts revealing deeper truth
- Use "Multi-Perspective Convergence" - same truth from various prophetic viewpoints
- Create "Historical Pattern Mapping" - connect ancient covenants to modern discipleship
- Include substantial exchanges with Hebrew/Greek insights, JST additions, typology
- Resolve questions with multiple satisfying layers of understanding
- Both speakers contribute advanced observations and discoveries
- Focus exclusively on adult-level content and application
- NEVER use the words: "echoes", "echo", "aha moment", "hook", "fresh insight", "kid activities"
- Use alternatives: "reflects", "mirrors", "realization", "insight", "opening", "beginning", "adult applications"

**TARGET**: 50-70 dialogue segments (~17-24 minutes total)

**EXAMPLE OPENING**:
{host_name}: "{guest_name}, I want to start with something that troubled early Christian theologians. Genesis 1 says God created everything in six days and rested. But Moses 7:30 in the Pearl of Great Price shows Enoch weeping because entire worlds are being destroyed and recreated. How can God rest if He's constantly creating? And what does this apparent contradiction reveal about divine work that most people never consider?"
{guest_name}: "{host_name}, that's brilliant—because resolving this contradiction unlocks the entire theology of eternal progression. Let me share a pattern that connects Abraham 3, the temple, and President Nelson's recent teachings on eternal life..."
"""
    }
    
    return base_prompt + level_additions.get(study_level, level_additions['essential'])

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
    "time collapse moment",
    "time collapse",
    "echoes",
    "echo", 
    "hook",
    "hooks",
    "kid activities",
    "children's activities",
    "family activities"
]


def get_podcast_prompt(week_number: int, title: str, date_range: str,
                       cfm_lesson_content: dict, scripture_content: list,
                       study_level: str, host_name: str, guest_name: str) -> str:
    """Build the prompt for generating podcast script using new structure"""
    
    # Get level-specific prompt with dynamic host/guest names
    level_prompt = get_level_specific_prompt(host_name, guest_name, study_level)
    
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
        
        # Teaching children sections - exclude for scholarly level
        teaching_sections = cfm_lesson_content.get('teaching_children', [])
        if teaching_sections and study_level != 'scholarly':
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
  {{"speaker": "{host_name}", "text": "{TAGLINE} I'm {host_name}."}},
  {{"speaker": "{guest_name}", "text": "And I'm {guest_name}. Happy to be here!"}}
]
"""
    
    return prompt


def clean_script_text(script_text: str) -> tuple:
    """
    Post-process the generated conversation script:
    - Strip markdown/code fences
    - Parse JSON array
    - Validate structure
    - Check for forbidden phrases and auto-replace them
    
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
    
    # Auto-replace forbidden phrases with alternatives
    replacements_made = []
    phrase_replacements = {
        "echoes": "reflects",
        "echo": "reflect", 
        "aha moment": "realization",
        "aha moments": "realizations",
        "fresh insight": "meaningful insight",
        "fresh insights": "meaningful insights", 
        "hook": "opening",
        "hooks": "openings",
        "kid activities": "family applications",
        "children's activities": "family applications",
        "time collapse": "connection across time",
        "here's something interesting": "what's remarkable is",
        "here's a fresh insight": "here's a meaningful insight"
    }
    
    for segment in script_array:
        if 'text' in segment:
            original_text = segment['text']
            updated_text = original_text
            
            # Replace forbidden phrases (case insensitive)
            for forbidden, replacement in phrase_replacements.items():
                pattern = re.compile(re.escape(forbidden), re.IGNORECASE)
                if pattern.search(updated_text):
                    updated_text = pattern.sub(replacement, updated_text)
                    replacements_made.append(f"'{forbidden}' → '{replacement}'")
            
            segment['text'] = updated_text
    
    # Report replacements
    if replacements_made:
        warnings.append(f"✅ Auto-replaced forbidden phrases: {', '.join(set(replacements_made))}")
    
    # Check for any remaining forbidden phrases after replacement
    full_text = " ".join(seg.get('text', '') for seg in script_array)
    remaining_issues = []
    for phrase in FORBIDDEN_PHRASES:
        if phrase.lower() in full_text.lower():
            remaining_issues.append(phrase)
    
    if remaining_issues:
        warnings.append(f"⚠️  Still found forbidden phrases after cleanup: {', '.join(remaining_issues)}")
    
    return script_array, warnings


def generate_podcast_script(week_number: int, study_level: str) -> dict:
    """Generate podcast script for a single week and study level"""
    
    # Randomly select host and guest (50/50 chance to alternate gender roles)
    host_name, guest_name = get_random_host_guest()
    print(f"🎭 Role assignment: {host_name} (host) / {guest_name} (guest)")
    
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
        study_level=study_level,
        host_name=host_name,
        guest_name=guest_name
    )
    
    print(f"🎙️ Generating {study_level} episode for Week {week_number}: {title[:50]}...")
    
    try:
        # Call Grok API
        completion = client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[
                {
                    "role": "system",
                    "content": f"You are creating natural podcast conversations between {host_name} (host) and {guest_name} (guest). Return ONLY a pure JSON array of dialogue segments. Each segment: {{\"speaker\": \"{host_name}\" or \"{guest_name}\", \"text\": \"what they say\"}}. First segment MUST be {host_name} saying: \"{TAGLINE} I'm {host_name}.\" No markdown, no code fences, just the JSON array."
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
            "host": host_name,
            "guest": guest_name,
            "voices": {
                "Sarah": SPEAKERS["Sarah"],
                "David": SPEAKERS["David"]
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
