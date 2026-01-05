#!/usr/bin/env python3
"""
CFM Core Content Generator
Extracts and formats raw Come Follow Me curriculum materials from weekly bundles.

Uses XAI API for proofreading and organization while keeping all text verbatim.
"""

import os
import json
import argparse
from pathlib import Path
from openai import OpenAI

# Paths
SCRIPT_DIR = Path(__file__).parent
CFM_2026_DIR = SCRIPT_DIR / "2026"
# Output directly to frontend/public/core_content for instant loading
OUTPUT_DIR = SCRIPT_DIR.parent.parent.parent / "frontend" / "public" / "core_content"

# Initialize XAI client (using OpenAI client with XAI endpoint)
xai_client = OpenAI(
    api_key=os.environ.get("XAI_API_KEY"),
    base_url="https://api.x.ai/v1",
)


def proofread_with_xai(content: dict, week_number: int) -> dict:
    """
    Use XAI API to proofread and organize content while keeping all text verbatim
    """
    if not os.environ.get("XAI_API_KEY"):
        print("⚠️  No XAI_API_KEY found, skipping proofreading")
        return content
    
    print(f"🤖 Proofreading and organizing content with XAI...")
    
    # Create a prompt that emphasizes keeping text verbatim
    prompt = f"""You are a careful editor proofreading Come Follow Me content for Week {week_number}.

CRITICAL REQUIREMENTS:
1. Keep ALL text completely VERBATIM - do not change, rewrite, or paraphrase ANY content
2. Only fix obvious typos, spacing issues, and formatting problems
3. Organize content into proper sections while preserving original structure
4. Keep all scripture references, quotes, and verse numbers exactly as written
5. Maintain all President/Apostle quotes word-for-word
6. Preserve all URLs, citations, and cross-references exactly

ALLOWED CHANGES ONLY:
- Fix obvious typos (like "hte" → "the")
- Normalize whitespace and line breaks
- Organize sections cleanly
- Fix punctuation errors
- Ensure consistent formatting

FORBIDDEN CHANGES:
- Rewording or paraphrasing any content
- Adding new content or explanations  
- Removing any existing content
- Changing scripture verse numbers or references
- Modifying quotes or citations

Please proofread and organize this content, returning the same JSON structure with improved formatting but completely verbatim text:

{json.dumps(content, indent=2)}
"""

    try:
        response = xai_client.chat.completions.create(
            model="grok-4-1-fast-reasoning",
            messages=[
                {
                    "role": "system", 
                    "content": "You are a careful proofreader who keeps all text completely verbatim while fixing only formatting and obvious errors."
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # Very low temperature for minimal changes
            max_tokens=16000
        )
        
        ai_response = response.choices[0].message.content
        
        # Try to extract JSON from the response
        try:
            # Look for JSON in the response
            import re
            json_match = re.search(r'\{.*\}', ai_response, re.DOTALL)
            if json_match:
                proofread_content = json.loads(json_match.group(0))
                print("✅ Content proofread and organized successfully")
                return proofread_content
            else:
                print("⚠️  Could not extract JSON from AI response, using original")
                return content
        except json.JSONDecodeError as e:
            print(f"⚠️  Error parsing AI response JSON: {e}")
            return content
            
    except Exception as e:
        print(f"⚠️  Error with XAI proofreading: {e}")
        return content


def clean_text(text: str) -> str:
    """Clean and normalize text content"""
    if not text:
        return ""
    
    # Strip whitespace and normalize line breaks
    text = text.strip()
    
    # Remove excessive whitespace but preserve paragraph breaks
    import re
    text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Max 2 consecutive newlines
    text = re.sub(r' +', ' ', text)  # Multiple spaces to single space
    text = re.sub(r'\t+', ' ', text)  # Tabs to single space
    
    return text


def fix_scripture_spacing(text: str) -> str:
    """Fix common spacing issues in scripture text that come from scraped data"""
    if not text:
        return ""
    
    import re
    
    # Fix common run-together words by adding spaces in specific patterns
    # This is specifically for fixing malformed scripture text from scraped data
    
    # Fix words that commonly run together
    fixes = [
        # Common word patterns that get mashed together
        (r'hespake(\w)', r'he spake \1'),
        (r'hesaw(\w)', r'he saw \1'),
        (r'hetalked(\w)', r'he talked \1'),
        (r'theglory(\w)', r'the glory \1'),
        (r'andEndless(\w)', r'and Endless \1'),
        (r'whereforelook', r'wherefore look'),
        (r'theworkmanship(\w)', r'the workmanship \1'),
        (r'minehands', r'mine hands'),
        (r'myworks(\w)', r'my works \1'),
        (r'withoutend', r'without end'),
        (r'mywords', r'my words'),
        (r'canbeholdall', r'can behold all'),
        (r'myglory', r'my glory'),
        (r'thesimilitude(\w)', r'the similitude \1'),
        (r'mineOnly(\w)', r'mine Only \1'),
        (r'theSavior', r'the Savior'),
        (r'ofgraceand(\w)', r'of grace and \1'),
        (r'thereisno(\w)', r'there is no \1'),
        (r'Iknowthem', r'I know them'),
        (r'onething(\w)', r'one thing \1'),
        (r'theworldupon', r'the world upon'),
        (r'Mosesbeheld(\w)', r'Moses beheld \1'),
        (r'greatlymarveledand', r'greatly marveled and'),
        (r'thepresence(\w)', r'the presence \1'),
        (r'hisglorywas', r'his glory was'),
        (r'hefellunto', r'he fell unto'),
        (r'naturalstrength(\w)', r'natural strength \1'),
        (r'manisnothing', r'man is nothing'),
        (r'myspiritualеyes', r'my spiritual eyes'),
        (r'mynaturaleyes', r'my natural eyes'),
        (r'withereddied', r'withered and died'),
        (r'wastransfigured(\w)', r'was transfigured \1'),
        (r'Satancame(\w)', r'Satan came \1'),
        (r'temptinghim', r'tempting him'),
        (r'asonof(\w)', r'a son of \1'),
        (r'hisSpirithath', r'his Spirit hath'),
        (r'Satancried(\w)', r'Satan cried \1'),
        (r'beginningof(\w)', r'beginning of \1'),
        (r'endof(\w)', r'end of \1'),
        (r'GodAlmighty', r'God Almighty'),
        (r'LordGod(\w)', r'Lord God \1'),
        (r'tellme(\w)', r'tell me \1'),
        (r'theheavens', r'the heavens'),
        (r'noendto', r'no end to'),
        (r'myworkand(\w)', r'my work and \1'),
        (r'theimmortality(\w)', r'the immortality \1'),
        (r'eternallif(\w)', r'eternal life \1'),
        (r'eternallifeof', r'eternal life of'),
        (r'thoushaltwrite(\w)', r'thou shalt write \1'),
        (r'anotherlikeunto', r'another like unto'),
        (r'hadagain(\w)', r'had again \1'),
        (r'amongasmany', r'among as many'),
        (r'spokenunto(\w)', r'spoken unto \1'),
        (r'myname(\W)', r'my name\1'),
        (r'highmountain(\W)', r'high mountain\1'),
        (r'Godface(\w)', r'God face \1'),
        (r'therefor(\w)', r'therefore \1'),
        (r'behold(\w)', r'behold \1'),
        (r'withoutbeginning', r'without beginning'),
        (r'endof(\w)', r'end of \1'),
    ]
    
    for pattern, replacement in fixes:
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    # General pattern: fix missing spaces before common words
    common_words = ['unto', 'with', 'and', 'the', 'of', 'in', 'to', 'for', 'by', 'he', 'she', 'it', 'was', 'were', 'are', 'is', 'be', 'been', 'have', 'had', 'has', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'shall']
    
    for word in common_words:
        # Add space before word if it's mashed with previous word (but not if it's already spaced)
        pattern = rf'([a-z]){word}(\W|$)'
        replacement = rf'\1 {word}\2'
        text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
    
    return text


def extract_core_content(week_number: int) -> dict:
    """Extract comprehensive core content from a CFM bundle"""
    
    week_file = CFM_2026_DIR / f"cfm_2026_week_{week_number:02d}.json"
    
    if not week_file.exists():
        print(f"❌ Week {week_number} file not found: {week_file}")
        return None
    
    with open(week_file, 'r', encoding='utf-8') as f:
        bundle = json.load(f)
    
    title = bundle.get('title', f'Week {week_number}')
    date_range = bundle.get('date_range', '')
    
    print(f"📄 Extracting comprehensive core content for Week {week_number}: {title[:50]}...")
    
    # Extract CFM lesson content
    cfm_lesson = bundle.get('cfm_lesson_content', {})
    
    # Format learning sections with full content
    learning_sections = []
    raw_learning = cfm_lesson.get('learning_at_home_church', [])
    if raw_learning:
        for section in raw_learning:
            learning_sections.append({
                "title": clean_text(section.get('title', '')),
                "content": clean_text(section.get('content', ''))
            })
    
    # Format teaching children sections with full content
    teaching_children = []
    raw_teaching = cfm_lesson.get('teaching_children', [])
    if raw_teaching:
        for section in raw_teaching:
            teaching_children.append({
                "title": clean_text(section.get('title', '')),
                "content": clean_text(section.get('content', ''))
            })
    
    # Format comprehensive scripture content with full text
    scriptures = []
    raw_scriptures = bundle.get('scripture_content', [])
    if raw_scriptures:
        for scripture in raw_scriptures:
            if isinstance(scripture, dict):
                # Extract full scripture text with verses
                reference = clean_text(scripture.get('reference', ''))
                
                # Get full text from either full_text field or verses array
                full_text = ""
                if 'full_text' in scripture and scripture['full_text']:
                    full_text = fix_scripture_spacing(clean_text(scripture['full_text']))
                elif 'verses' in scripture and scripture['verses']:
                    # Reconstruct full text from verses with verse numbers
                    verses = scripture['verses']
                    verse_texts = []
                    for i, verse in enumerate(verses, 1):
                        verse_text = fix_scripture_spacing(clean_text(str(verse)))
                        if verse_text:
                            verse_texts.append(f"{i} {verse_text}")
                    full_text = " ".join(verse_texts)
                
                scriptures.append({
                    "reference": reference,
                    "title": clean_text(scripture.get('title', '')),
                    "summary": clean_text(scripture.get('summary', '')),
                    "url": scripture.get('url', ''),
                    "text": full_text,
                    "verse_count": len(scripture.get('verses', [])) if 'verses' in scripture else 0
                })
            elif isinstance(scripture, str):
                scriptures.append({
                    "reference": "",
                    "title": "",
                    "summary": "",
                    "url": "",
                    "text": clean_text(scripture),
                    "verse_count": 0
                })
    
    # Extract seminary content if available
    seminary_content = bundle.get('seminary_content')
    if seminary_content:
        # Clean seminary content recursively
        def clean_seminary_content(content):
            if isinstance(content, dict):
                return {k: clean_seminary_content(v) for k, v in content.items()}
            elif isinstance(content, list):
                return [clean_seminary_content(item) for item in content]
            elif isinstance(content, str):
                return clean_text(content)
            else:
                return content
        
        seminary_content = clean_seminary_content(seminary_content)
    
    # Extract study helps if available
    study_helps = bundle.get('study_helps', [])
    if study_helps:
        study_helps = [clean_text(help_item) if isinstance(help_item, str) else help_item for help_item in study_helps]
    
    # Build the comprehensive core content structure
    result = {
        "week_number": week_number,
        "title": clean_text(title),
        "date_range": clean_text(date_range),
        "scripture_block": clean_text(bundle.get('scripture_block', '')),
        
        # Full lesson introduction
        "introduction": clean_text(cfm_lesson.get('introduction', '')),
        
        # Comprehensive learning sections
        "learning_at_home_church": learning_sections,
        "teaching_children": teaching_children,
        
        # Complete scripture content with full text
        "scriptures": scriptures,
        "scripture_count": len(scriptures),
        
        # Additional content sections
        "seminary_content": seminary_content,
        "study_helps": study_helps,
        "additional_resources": bundle.get('additional_resources', []),
        
        # Metadata
        "cfm_lesson_url": cfm_lesson.get('url', ''),
        "source_week_file": str(week_file.name),
        "extracted_timestamp": __import__('time').strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Calculate comprehensive content stats
    total_chars = len(result.get('introduction', ''))
    
    # Count learning section content
    for section in learning_sections:
        total_chars += len(section.get('content', ''))
        total_chars += len(section.get('title', ''))
    
    # Count teaching children content
    for section in teaching_children:
        total_chars += len(section.get('content', ''))
        total_chars += len(section.get('title', ''))
    
    # Count scripture text
    for scripture in scriptures:
        total_chars += len(scripture.get('text', ''))
        total_chars += len(scripture.get('title', ''))
        total_chars += len(scripture.get('summary', ''))
    
    result["total_character_count"] = total_chars
    result["total_word_count"] = len(result.get('introduction', '').split()) + sum(
        len(section.get('content', '').split()) for section in learning_sections
    ) + sum(
        len(section.get('content', '').split()) for section in teaching_children
    ) + sum(
        len(scripture.get('text', '').split()) for scripture in scriptures
    )
    
    # Use XAI to proofread and organize content while keeping text verbatim
    result = proofread_with_xai(result, week_number)
    
    print(f"✅ Extracted comprehensive core content:")
    print(f"   - {len(learning_sections)} learning sections")
    print(f"   - {len(teaching_children)} children sections")
    print(f"   - {len(scriptures)} scripture blocks")
    print(f"   - {result['total_word_count']:,} words total")
    
    return result


def save_core_content(week_number: int, content_data: dict):
    """Save core content to a JSON file"""
    
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    output_file = OUTPUT_DIR / f"core_content_week_{week_number:02d}.json"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(content_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Saved: {output_file.name}")


def main():
    parser = argparse.ArgumentParser(description='Extract core content from CFM bundles')
    parser.add_argument('--week', type=int, help='Extract for a single week')
    parser.add_argument('--start', type=int, default=1, help='Start week (inclusive)')
    parser.add_argument('--end', type=int, default=52, help='End week (inclusive)')
    parser.add_argument('--force', action='store_true', help='Regenerate even if file exists')
    
    args = parser.parse_args()
    
    if args.week:
        weeks = [args.week]
    else:
        weeks = list(range(args.start, args.end + 1))
    
    print(f"\n📄 CFM Core Content Extractor")
    print(f"=" * 60)
    print(f"Weeks: {weeks[0]} - {weeks[-1]} ({len(weeks)} weeks)")
    print(f"Force regenerate: {args.force}")
    print(f"=" * 60 + "\n")
    
    extracted = 0
    failed = 0
    skipped = 0
    
    for week in weeks:
        output_file = OUTPUT_DIR / f"core_content_week_{week:02d}.json"
        if output_file.exists() and not args.force:
            print(f"⏭️  Skipping Week {week} (already exists, use --force to regenerate)")
            skipped += 1
            continue
        
        content_data = extract_core_content(week)
        
        if content_data:
            save_core_content(week, content_data)
            extracted += 1
        else:
            failed += 1
    
    print(f"\n{'=' * 60}")
    print(f"✅ Extraction complete!")
    print(f"   Extracted: {extracted}")
    print(f"   Skipped: {skipped}")
    print(f"   Failed: {failed}")
    print(f"   Output directory: {OUTPUT_DIR}")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()
