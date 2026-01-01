#!/usr/bin/env python3
"""
CFM Core Content Generator
Extracts and formats raw Come Follow Me curriculum materials from weekly bundles.

This does NOT use AI - it simply reformats the existing bundle data into
a clean, frontend-ready JSON structure for direct display.
"""

import os
import json
import argparse
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
CFM_2026_DIR = SCRIPT_DIR / "2026"
# Output directly to frontend/public/core_content for instant loading
OUTPUT_DIR = SCRIPT_DIR.parent.parent.parent / "frontend" / "public" / "core_content"


def extract_core_content(week_number: int) -> dict:
    """Extract core content from a CFM bundle"""
    
    week_file = CFM_2026_DIR / f"cfm_2026_week_{week_number:02d}.json"
    
    if not week_file.exists():
        print(f"❌ Week {week_number} file not found: {week_file}")
        return None
    
    with open(week_file, 'r', encoding='utf-8') as f:
        bundle = json.load(f)
    
    title = bundle.get('title', f'Week {week_number}')
    date_range = bundle.get('date_range', '')
    
    print(f"📄 Extracting core content for Week {week_number}: {title[:50]}...")
    
    # Extract CFM lesson content
    cfm_lesson = bundle.get('cfm_lesson_content', {})
    
    # Format learning sections
    learning_sections = []
    raw_learning = cfm_lesson.get('learning_at_home_church', [])
    if raw_learning:
        for section in raw_learning:
            learning_sections.append({
                "title": section.get('title', ''),
                "content": section.get('content', '')
            })
    
    # Format teaching children sections
    teaching_children = []
    raw_teaching = cfm_lesson.get('teaching_children', [])
    if raw_teaching:
        for section in raw_teaching:
            teaching_children.append({
                "title": section.get('title', ''),
                "content": section.get('content', '')
            })
    
    # Format scripture content
    scriptures = []
    raw_scriptures = bundle.get('scripture_content', [])
    if raw_scriptures:
        for scripture in raw_scriptures:
            if isinstance(scripture, dict):
                scriptures.append({
                    "reference": scripture.get('reference', ''),
                    "text": scripture.get('text', '')
                })
            elif isinstance(scripture, str):
                scriptures.append({
                    "reference": "",
                    "text": scripture
                })
    
    # Extract seminary content if available
    seminary_content = bundle.get('seminary_content', {})
    
    # Build the core content structure
    result = {
        "week_number": week_number,
        "title": title,
        "date_range": date_range,
        "scripture_block": bundle.get('scripture_block', ''),
        
        "introduction": cfm_lesson.get('introduction', ''),
        
        "learning_at_home_church": learning_sections,
        "teaching_children": teaching_children,
        
        "scriptures": scriptures,
        "scripture_count": len(scriptures),
        
        "seminary_content": seminary_content if seminary_content else None,
        
        "additional_resources": bundle.get('additional_resources', []),
        
        "source_week_file": str(week_file.name),
        "extracted_timestamp": __import__('time').strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # Calculate content stats
    total_chars = len(result.get('introduction', ''))
    for section in learning_sections:
        total_chars += len(section.get('content', ''))
    for section in teaching_children:
        total_chars += len(section.get('content', ''))
    
    result["total_character_count"] = total_chars
    result["total_word_count"] = total_chars // 5  # Rough estimate
    
    print(f"✅ Extracted core content: {len(learning_sections)} learning sections, {len(teaching_children)} children sections, {len(scriptures)} scriptures")
    
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
