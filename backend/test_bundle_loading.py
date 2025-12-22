#!/usr/bin/env python3
"""
Test script to verify enhanced CFM bundle loading works correctly
"""
import json
import os
from search.api import load_cfm_2026_bundle

def test_bundle_loading():
    """Test loading enhanced CFM bundles for problematic weeks"""
    
    # Test Week 32 (Esther - was showing 0 chapters)
    print("=" * 60)
    print("Testing Week 32 (Esther) Bundle Loading")
    print("=" * 60)
    
    week_32_data = load_cfm_2026_bundle(32)
    if week_32_data:
        print(f"✅ Week 32 bundle loaded successfully")
        
        # Check cfm_lesson_content
        cfm_content = week_32_data.get('cfm_lesson_content', [])
        print(f"CFM Lesson Content sections: {len(cfm_content)}")
        
        # Check scripture_content
        scripture_content = week_32_data.get('scripture_content', [])
        print(f"Scripture Content sections: {len(scripture_content)}")
        
        # Analyze Esther chapters
        esther_chapters = [item for item in scripture_content if 'Esther' in item.get('title', '')]
        print(f"Esther chapters found: {len(esther_chapters)}")
        
        if esther_chapters:
            print("Esther chapters detected:")
            for chapter in esther_chapters[:3]:  # Show first 3
                title = chapter.get('title', 'No title')
                verses = chapter.get('verses', [])
                verses_count = len(verses)
                total_chars = sum(len(verse) for verse in verses)
                print(f"  - {title} ({verses_count} verses, {total_chars} chars)")
                
        print()
    else:
        print("❌ Week 32 bundle loading failed")
        print()
    
    # Test Week 48 (Amos/Obadiah/Jonah - was showing 0 chapters)  
    print("=" * 60)
    print("Testing Week 48 (Amos/Obadiah/Jonah) Bundle Loading")
    print("=" * 60)
    
    week_48_data = load_cfm_2026_bundle(48)
    if week_48_data:
        print(f"✅ Week 48 bundle loaded successfully")
        
        # Check cfm_lesson_content
        cfm_content = week_48_data.get('cfm_lesson_content', [])
        print(f"CFM Lesson Content sections: {len(cfm_content)}")
        
        # Check scripture_content
        scripture_content = week_48_data.get('scripture_content', [])
        print(f"Scripture Content sections: {len(scripture_content)}")
        
        # Analyze chapters for Amos, Obadiah, Jonah
        target_books = ['Amos', 'Obadiah', 'Jonah']
        for book in target_books:
            book_chapters = [item for item in scripture_content if book in item.get('title', '')]
            print(f"{book} chapters found: {len(book_chapters)}")
            
            if book_chapters:
                print(f"  {book} chapters detected:")
                for chapter in book_chapters[:2]:  # Show first 2
                    title = chapter.get('title', 'No title')
                    verses = chapter.get('verses', [])
                    verses_count = len(verses)
                    total_chars = sum(len(verse) for verse in verses)
                    print(f"    - {title} ({verses_count} verses, {total_chars} chars)")
        print()
    else:
        print("❌ Week 48 bundle loading failed")
        print()

    # Test a regular week for comparison (Week 1)
    print("=" * 60) 
    print("Testing Week 1 (Control Test) Bundle Loading")
    print("=" * 60)
    
    week_1_data = load_cfm_2026_bundle(1)
    if week_1_data:
        print(f"✅ Week 1 bundle loaded successfully")
        
        cfm_content = week_1_data.get('cfm_lesson_content', [])
        scripture_content = week_1_data.get('scripture_content', [])
        
        print(f"CFM Lesson Content sections: {len(cfm_content)}")
        print(f"Scripture Content sections: {len(scripture_content)}")
        
        if scripture_content:
            print("Sample scripture titles:")
            for item in scripture_content[:3]:
                title = item.get('title', 'No title')
                verses = item.get('verses', [])
                verses_count = len(verses)
                total_chars = sum(len(verse) for verse in verses)
                print(f"  - {title} ({verses_count} verses, {total_chars} chars)")
    else:
        print("❌ Week 1 bundle loading failed")

    # Test Week 2 (should have actual scripture content)
    print("\n" + "=" * 60) 
    print("Testing Week 2 (Genesis 1-2) Bundle Loading")
    print("=" * 60)
    
    week_2_data = load_cfm_2026_bundle(2)
    if week_2_data:
        print(f"✅ Week 2 bundle loaded successfully")
        
        cfm_content = week_2_data.get('cfm_lesson_content', [])
        scripture_content = week_2_data.get('scripture_content', [])
        
        print(f"CFM Lesson Content sections: {len(cfm_content) if isinstance(cfm_content, list) else 1}")
        print(f"Scripture Content sections: {len(scripture_content)}")
        
        if scripture_content:
            print("Genesis chapters found:")
            genesis_chapters = [item for item in scripture_content if 'Genesis' in item.get('title', '')]
            print(f"Genesis chapters: {len(genesis_chapters)}")
            
            for chapter in genesis_chapters[:2]:
                title = chapter.get('title', 'No title')
                verses = chapter.get('verses', [])
                verses_count = len(verses)
                total_chars = sum(len(verse) for verse in verses)
                print(f"  - {title} ({verses_count} verses, {total_chars} chars)")
    else:
        print("❌ Week 2 bundle loading failed")
    
    print("\n" + "=" * 60)
    print("Bundle Loading Test Complete")
    print("=" * 60)

if __name__ == "__main__":
    test_bundle_loading()