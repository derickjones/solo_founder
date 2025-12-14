#!/usr/bin/env python3
"""
Display utility for unified CFM content
"""

import json
import argparse
from pathlib import Path

def display_unified_content(week_number: int, content_dir: str = "../content/unified_bundles"):
    """Display unified weekly content"""
    
    content_path = Path(content_dir)
    bundle_files = list(content_path.glob(f"week_{week_number:02d}_*.json"))
    
    if not bundle_files:
        print(f"❌ No unified content found for week {week_number}")
        return
    
    bundle_file = bundle_files[0]
    
    try:
        with open(bundle_file, 'r', encoding='utf-8') as f:
            content = json.load(f)
        
        print("=" * 80)
        print(f"📅 CFM Unified Content - Week {content['week_number']}")
        print(f"📆 {content['date_range']}")
        print(f"📖 {content['title']}")
        print("=" * 80)
        
        # Content sources
        sources = content.get('content_sources', [])
        print(f"\n📚 CONTENT SOURCES ({len(sources)})")
        print("-" * 50)
        
        for source in sources:
            print(f"🔹 {source['source_type'].upper()}: {source['title']}")
            print(f"   Content: {len(source['content']):,} characters")
            if source.get('purpose'):
                print(f"   Purpose: {source['purpose']}")
        
        # Primary scriptures
        scriptures = content.get('primary_scriptures', [])
        if scriptures:
            print(f"\n📜 PRIMARY SCRIPTURES ({len(scriptures)})")
            print("-" * 50)
            for scripture in scriptures:
                chapters = ', '.join(scripture['chapters'])
                print(f"📖 {scripture['book']} {chapters}")
        
        # Scripture content
        scripture_content = content.get('scripture_content', {})
        if scripture_content:
            print(f"\n📝 SCRIPTURE CONTENT")
            print("-" * 50)
            for book_name, chapters in scripture_content.items():
                print(f"📖 {book_name}")
                for chapter_num, chapter_data in chapters.items():
                    verses = len(chapter_data.get('verses', {}))
                    total_text = sum(len(v.get('text', '')) for v in chapter_data.get('verses', {}).values())
                    print(f"   Chapter {chapter_num}: {verses} verses, {total_text:,} characters")
        
        # Combined content preview
        all_content = content.get('all_content', '')
        if all_content:
            print(f"\n📄 COMBINED CONTENT PREVIEW")
            print("-" * 50)
            preview = all_content[:500] + "..." if len(all_content) > 500 else all_content
            print(preview)
        
        # Statistics
        print("\n" + "=" * 80)
        print("📊 CONTENT STATISTICS")
        print(f"Total sources: {content.get('total_sources', 0)}")
        print(f"Total content: {content.get('total_content_length', 0):,} characters")
        print(f"Teaching ideas: {len(content.get('teaching_ideas', []))}")
        print(f"Discussion questions: {len(content.get('discussion_questions', []))}")
        print(f"Themes: {len(content.get('themes', []))}")
        if content.get('themes'):
            print(f"   {', '.join(content['themes'])}")
        print(f"Bundle file: {bundle_file.name}")
        print("=" * 80)
        
    except Exception as e:
        print(f"❌ Error loading unified content: {e}")

def main():
    parser = argparse.ArgumentParser(description="Display unified CFM content")
    parser.add_argument("week", type=int, help="Week number to display")
    parser.add_argument("--content-dir", default="../content/unified_bundles", 
                       help="Unified content directory path")
    
    args = parser.parse_args()
    display_unified_content(args.week, args.content_dir)

if __name__ == "__main__":
    main()