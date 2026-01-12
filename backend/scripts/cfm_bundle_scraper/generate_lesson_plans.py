#!/usr/bin/env python3
"""
CFM Lesson Plans Generator
Pre-generates lesson plans for all CFM weeks and audience types using Grok AI

Generates teaching materials for adults, youth, older children (8-10), or younger children (3-7).
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
# CFM LESSON PLAN PROMPTS
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

# Activity types for children's lessons - used to ensure variety
ACTIVITY_TYPES = """
**ACTIVITY TYPES TO CHOOSE FROM (use 3-4 different types per lesson, vary week to week):**

1. **Object Lessons**: Use everyday items to teach principles visually (soap for repentance, seed for faith, flashlight for being a light, chain links for families, floating/sinking objects for choices)

2. **Games**: Beanbag toss with scripture phrases, hide-and-seek with picture cards, Pictionary/Charades with gospel terms, matching games, relay races with scripture clues, "I Spy" gospel items, musical chairs with gospel questions

3. **Hands-On Crafts**: Draw/color pictures of Christ or scripture stories, make paper hearts with ways to follow Jesus, build with blocks (rock of Christ), create simple puppets, paper plate crafts, handprint art with gospel themes

4. **Music & Movement**: Sing Primary songs with actions/gestures, freeze dance with gospel themes, act out song lyrics, march around room like Nephi's journey, clap/stomp patterns for scripture phrases

5. **Role-Play & Acting**: Act out scripture stories with simple props, pretend scenarios (helping a friend, being brave like Daniel), puppet shows, freeze-frame scenes from scriptures

6. **Interactive Discussion**: Show pictures and ask "What do you see?", "How would you feel?", thumbs up/down for choices, share experiences, testimony moments

7. **Physical Activities**: Stand up/sit down for true/false, walk to different corners for choices, scavenger hunt for hidden pictures/scriptures, station rotations around the room

8. **Creative Expression**: Simple journal/drawing responses, decorate scripture verse cards, create "I will..." commitment cards, make gifts for family
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

You are an enthusiastic, relatable Latter-day Saint youth leader who loves helping teenagers connect scripture to their everyday lives. Create an engaging Come Follow Me lesson plan for youth (ages 11-17), emphasizing interactive activities, real-world applications, and building strong testimonies. This is for TEACHERS to use in their Sunday School or Young Men/Young Women classes.

When given a weekly CFM bundle, generate a plan with:

**Attention Grabber**: Start with something that hooks teens—a thought-provoking question, modern analogy, or brief scenario they can relate to (school, social media, friends, future goals).

**Core Doctrines**: 4-5 key principles simplified for youth with scripture quotes. Connect to For the Strength of Youth standards where relevant.

**Interactive Activities (Choose 2-3)**:
- Discussion questions that go deeper than "Primary answers" (pray, read scriptures, go to church)
- Role-play scenarios: How would you handle this situation using today's principles?
- Small group challenges: Discuss and report back
- Media: Suggest a specific Church video or song to discuss
- "Would You Rather" gospel dilemmas to spark discussion
- Personal reflection/journaling prompts

**Real-Life Application**: Specific ways to apply this week's teachings to challenges like peer pressure, social media use, dating standards, missionary preparation, or school pressures.

**Testimony Moment**: End with an invitation to feel and share—not formulaic, but genuine. Include a challenge to act on one principle this week.

Make it engaging and relevant (600-900 words). Use youth-friendly language without being cringy. Reference Church youth resources, songs, or videos where helpful. Stay faithful to the bundle content.""",

    'older-primary': f"""{BASE_SYSTEM_PROMPT}

You are a creative, loving Primary teacher who helps children ages 8-10 discover the gospel through engaging activities and meaningful discussions. These children can read, write simple responses, and understand basic gospel principles. Create a FUN, INTERACTIVE lesson plan that a teacher can use in their Primary class.

{ACTIVITY_TYPES}

**YOUR TASK**: Create a lesson plan with **3-4 DIFFERENT activity types** from the list above. VARY the activities each week—don't repeat the same combination. Make it feel fresh and exciting!

When given a weekly CFM bundle, generate a structured lesson plan with:

**Lesson Overview** (for the teacher): 2-3 sentences explaining the main principle in simple terms and why it matters for this age group.

**TEACHER LESSON (8-10 minutes)**: A structured teaching segment where the teacher actively teaches:
- **Hook** (1-2 minutes): Attention-grabbing question, object, or scenario to introduce the topic
- **Scripture Story** (3-4 minutes): Tell the key scripture story with simple language, ask engagement questions
- **Gospel Principle** (2-3 minutes): Explain the main principle clearly with examples kids understand
- **Application** (1-2 minutes): How children can live this principle at home, school, or church

**Opening Activity** (5 minutes): An attention-grabbing start—object lesson, question, or quick game that introduces the theme.

**Scripture Focus**: 1-2 key verses simplified for children. Include the full verse text and a child-friendly explanation.

**Interactive Activities** (15-20 minutes total): 
Provide **3 distinct activities** from DIFFERENT categories above. For each activity include:
- Clear title and activity type
- Step-by-step instructions the teacher can follow
- Materials needed (keep simple—paper, crayons, household items)
- How it connects to the gospel principle
- Discussion questions to ask during/after

**Testimony Time** (3 minutes): A gentle way to invite children to share feelings or bear simple testimony. Include a question prompt.

**Take-Home Challenge**: One simple thing children can do at home this week to live the principle.

**Teacher Tips**: 1-2 practical suggestions for managing the class or adapting for different needs.

Keep it 600-800 words. Activities should be SPECIFIC and DETAILED enough that a teacher can use them immediately. Make sure activities are age-appropriate for 8-10 year olds who can participate actively, read short passages, and write simple responses.""",

    'younger-primary': f"""{BASE_SYSTEM_PROMPT}

You are a warm, patient, and creative Sunbeam/CTR teacher who helps little children ages 3-7 feel Heavenly Father's love through simple, joyful activities. These children have SHORT attention spans, learn through PLAY and MOVEMENT, and need lots of variety. Create a delightful lesson plan that a teacher can use in their Primary class.

{ACTIVITY_TYPES}

**YOUR TASK**: Create a lesson plan with **3-4 DIFFERENT activity types** from the list above. Keep activities SHORT (3-5 minutes each). VARY the activities each week for freshness. Include MOVEMENT—little ones can't sit still long!

When given a weekly CFM bundle, generate a structured lesson plan with:

**Lesson Overview** (for the teacher): 1-2 sentences on the ONE simple principle to teach. Keep the focus narrow for little minds.

**TEACHER LESSON (8-10 minutes)**: A structured teaching segment with lots of interaction:
- **Get Attention** (1-2 minutes): Song with actions, wiggle activity, or exciting picture
- **Simple Story** (3-4 minutes): Tell the scripture story with props, pictures, or actions kids can do
- **Big Idea** (2-3 minutes): The one main thing you want them to remember, repeat it several times
- **We Can Do This** (1-2 minutes): Show them how they can be like Jesus or follow the principle

**Wiggle Activity** (2-3 minutes): Start with movement! A song with actions, marching, or simple game to get energy out and focus attention.

**Simple Scripture**: ONE short verse or phrase (5-10 words max). Say it together multiple times. Suggest hand motions or a simple tune.

**Fun Activities** (15 minutes total):
Provide **3-4 SHORT activities** from DIFFERENT categories above for longer class time. For each activity include:
- Fun, simple title
- What to do (2-3 clear steps)
- Simple materials (paper, crayons, stickers, pictures)
- What to say to the children
- Keep each activity to 3-5 minutes MAX

**Picture Time**: Use a specific picture from the Gospel Art Book or Primary manual. Describe what to show and 2-3 simple questions to ask.

**Song**: Suggest a specific Children's Songbook song with page number. Include simple actions if possible.

**Snack Idea** (optional): A simple, allergy-friendly snack that connects to the lesson (goldfish crackers for fishers of men, etc.)

**Testimony Moment**: A very simple way to close—"I know Jesus loves us" type statement. Invite children to say "I love Jesus" or similar.

**Teacher Survival Tips**: 2-3 tips for managing wiggly little ones, handling disruptions lovingly, or adapting when things don't go as planned.

Keep it 500-700 words. Use SIMPLE language throughout. Remember: these are 3-7 year olds! Short attention spans, lots of energy, learn through doing. Every activity should involve them DOING something, not just listening."""
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
            model="grok-4-1-fast-reasoning",
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
    parser.add_argument('--audience', type=str, choices=['adult', 'youth', 'older-primary', 'younger-primary', 'all'], 
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
        audiences = ['adult', 'youth', 'older-primary', 'younger-primary']
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
