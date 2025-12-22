#!/usr/bin/env python3
"""
CFM 2026 Complete Year Scraper - All 52 weeks with accurate official data

This script scrapes all 52 weeks of Come Follow Me Old Testament 2026 lessons
including both CFM lesson content and complete scripture chapters.

Features:
- Uses official dates and scripture references from churchofjesuschrist.org
- Enhanced complex scripture reference parsing (e.g., "Exodus 19–20; 24; 31–34")
- Comprehensive content extraction with detailed analytics
- Individual JSON bundles for each week plus summary file
- Production-ready for Deep Dive generation system

Usage:
    python3 scrape_2026_cfm.py

Output:
    - 52 individual JSON files (cfm_2026_week_01.json through cfm_2026_week_52.json)
    - Complete year summary file with statistics
"""

import sys
import os
from pathlib import Path
from datetime import datetime
sys.path.append(os.path.dirname(__file__))

from cfm_weekly_scraper import CFMWeeklyScraper
import json
import time

def scrape_all_52_weeks():
    """Scrape all 52 weeks of CFM 2026 with detailed analysis"""
    scraper = CFMWeeklyScraper()
    
    # All 52 weeks of CFM Old Testament 2026 - OFFICIAL dates and scriptures
    weeks_to_scrape = [
        {
            "week_number": 1,
            "date_range": "December 29–January 4",
            "title": "Week 1: December 29–January 4 - Introduction to the Old Testament"
        },
        {
            "week_number": 2, 
            "date_range": "January 5–11",
            "title": "Week 2: January 5–11 - Moses 1; Abraham 3"
        },
        {
            "week_number": 3,
            "date_range": "January 12–18", 
            "title": "Week 3: January 12–18 - Genesis 1–2; Moses 2–3; Abraham 4–5"
        },
        {
            "week_number": 4,
            "date_range": "January 19–25",
            "title": "Week 4: January 19–25 - Genesis 3–4; Moses 4–5"
        },
        {
            "week_number": 5,
            "date_range": "January 26–February 1",
            "title": "Week 5: January 26–February 1 - Genesis 5; Moses 6"
        },
        {
            "week_number": 6,
            "date_range": "February 2–8",
            "title": "Week 6: February 2–8 - Moses 7"
        },
        {
            "week_number": 7,
            "date_range": "February 9–15",
            "title": "Week 7: February 9–15 - Genesis 6–11; Moses 8"
        },
        {
            "week_number": 8,
            "date_range": "February 16–22",
            "title": "Week 8: February 16–22 - Genesis 12–17; Abraham 1–2"
        },
        {
            "week_number": 9,
            "date_range": "February 23–March 1",
            "title": "Week 9: February 23–March 1 - Genesis 18–23"
        },
        {
            "week_number": 10,
            "date_range": "March 2–8",
            "title": "Week 10: March 2–8 - Genesis 24–33"
        },
        {
            "week_number": 11,
            "date_range": "March 9–15",
            "title": "Week 11: March 9–15 - Genesis 37–41"
        },
        {
            "week_number": 12,
            "date_range": "March 16–22",
            "title": "Week 12: March 16–22 - Genesis 42–50"
        },
        {
            "week_number": 13,
            "date_range": "March 23–29",
            "title": "Week 13: March 23–29 - Exodus 1–6"
        },
        {
            "week_number": 14,
            "date_range": "March 30–April 5",
            "title": "Week 14: March 30–April 5 - Easter"
        },
        {
            "week_number": 15,
            "date_range": "April 6–12",
            "title": "Week 15: April 6–12 - Exodus 7–13"
        },
        {
            "week_number": 16,
            "date_range": "April 13–19",
            "title": "Week 16: April 13–19 - Exodus 14–18"
        },
        {
            "week_number": 17,
            "date_range": "April 20–26",
            "title": "Week 17: April 20–26 - Exodus 19–20; 24; 31–34"
        },
        {
            "week_number": 18,
            "date_range": "April 27–May 3",
            "title": "Week 18: April 27–May 3 - Exodus 35–40; Leviticus 1; 4; 16; 19"
        },
        {
            "week_number": 19,
            "date_range": "May 4–10",
            "title": "Week 19: May 4–10 - Numbers 11–14; 20–24; 27"
        },
        {
            "week_number": 20,
            "date_range": "May 11–17",
            "title": "Week 20: May 11–17 - Deuteronomy 6–8; 15; 18; 29–30; 34"
        },
        {
            "week_number": 21,
            "date_range": "May 18–24",
            "title": "Week 21: May 18–24 - Joshua 1–8; 23–24"
        },
        {
            "week_number": 22,
            "date_range": "May 25–31",
            "title": "Week 22: May 25–31 - Judges 2–4; 6–8; 13–16"
        },
        {
            "week_number": 23,
            "date_range": "June 1–7",
            "title": "Week 23: June 1–7 - Ruth; 1 Samuel 1–7"
        },
        {
            "week_number": 24,
            "date_range": "June 8–14",
            "title": "Week 24: June 8–14 - 1 Samuel 8–10; 13; 15–16"
        },
        {
            "week_number": 25,
            "date_range": "June 15–21",
            "title": "Week 25: June 15–21 - 1 Samuel 17–18; 24–26; 2 Samuel 5–7"
        },
        {
            "week_number": 26,
            "date_range": "June 22–28",
            "title": "Week 26: June 22–28 - 2 Samuel 11–12; 1 Kings 3; 6–9; 11"
        },
        {
            "week_number": 27,
            "date_range": "June 29–July 5",
            "title": "Week 27: June 29–July 5 - 1 Kings 12–13; 17–22"
        },
        {
            "week_number": 28,
            "date_range": "July 6–12",
            "title": "Week 28: July 6–12 - 2 Kings 2–7"
        },
        {
            "week_number": 29,
            "date_range": "July 13–19",
            "title": "Week 29: July 13–19 - 2 Kings 16–25"
        },
        {
            "week_number": 30,
            "date_range": "July 20–26",
            "title": "Week 30: July 20–26 - 2 Chronicles 14–20; 26; 30"
        },
        {
            "week_number": 31,
            "date_range": "July 27–August 2",
            "title": "Week 31: July 27–August 2 - Ezra 1; 3–7; Nehemiah 2; 4–6; 8"
        },
        {
            "week_number": 32,
            "date_range": "August 3–9",
            "title": "Week 32: August 3–9 - Esther"
        },
        {
            "week_number": 33,
            "date_range": "August 10–16",
            "title": "Week 33: August 10–16 - Job 1–3; 12–14; 19; 21–24; 38–40; 42"
        },
        {
            "week_number": 34,
            "date_range": "August 17–23",
            "title": "Week 34: August 17–23 - Psalms 1–2; 8; 19–33; 40; 46"
        },
        {
            "week_number": 35,
            "date_range": "August 24–30",
            "title": "Week 35: August 24–30 - Psalms 49–51; 61–66; 69–72; 77–78; 85–86"
        },
        {
            "week_number": 36,
            "date_range": "August 31–September 6",
            "title": "Week 36: August 31–September 6 - Psalms 102–3; 110; 116–19; 127–28; 135–39; 146–50"
        },
        {
            "week_number": 37,
            "date_range": "September 7–13",
            "title": "Week 37: September 7–13 - Proverbs 1–4; 15–16; 22; 31; Ecclesiastes 1–3; 11–12"
        },
        {
            "week_number": 38,
            "date_range": "September 14–20",
            "title": "Week 38: September 14–20 - Isaiah 1–12"
        },
        {
            "week_number": 39,
            "date_range": "September 21–27",
            "title": "Week 39: September 21–27 - Isaiah 13–14; 22; 24–30; 35"
        },
        {
            "week_number": 40,
            "date_range": "September 28–October 4",
            "title": "Week 40: September 28–October 4 - Isaiah 40–49"
        },
        {
            "week_number": 41,
            "date_range": "October 5–11",
            "title": "Week 41: October 5–11 - Isaiah 50–57"
        },
        {
            "week_number": 42,
            "date_range": "October 12–18",
            "title": "Week 42: October 12–18 - Isaiah 58–66"
        },
        {
            "week_number": 43,
            "date_range": "October 19–25",
            "title": "Week 43: October 19–25 - Jeremiah 1–3; 7; 16–18; 20"
        },
        {
            "week_number": 44,
            "date_range": "October 26–November 1",
            "title": "Week 44: October 26–November 1 - Jeremiah 31–33; 36–38; Lamentations 1; 3"
        },
        {
            "week_number": 45,
            "date_range": "November 2–8",
            "title": "Week 45: November 2–8 - Ezekiel 1–3; 33–34; 36–37; 47"
        },
        {
            "week_number": 46,
            "date_range": "November 9–15",
            "title": "Week 46: November 9–15 - Daniel 1–7"
        },
        {
            "week_number": 47,
            "date_range": "November 16–22",
            "title": "Week 47: November 16–22 - Hosea 1–6; 10–14; Joel"
        },
        {
            "week_number": 48,
            "date_range": "November 23–29",
            "title": "Week 48: November 23–29 - Amos; Obadiah; Jonah"
        },
        {
            "week_number": 49,
            "date_range": "November 30–December 6",
            "title": "Week 49: November 30–December 6 - Micah; Nahum; Habakkuk; Zephaniah"
        },
        {
            "week_number": 50,
            "date_range": "December 7–13",
            "title": "Week 50: December 7–13 - Haggai 1–2; Zechariah 1–4; 7–14"
        },
        {
            "week_number": 51,
            "date_range": "December 14–20",
            "title": "Week 51: December 14–20 - Malachi"
        },
        {
            "week_number": 52,
            "date_range": "December 21–27",
            "title": "Week 52: December 21–27 - Christmas"
        }
    ]
    
    # Setup output directory - save in 2026 folder under cfm_bundle_scraper
    output_dir = Path("/Users/derickjones/Documents/VS-Code/solo_founder/backend/scripts/cfm_bundle_scraper/2026")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    successful_weeks = []
    failed_weeks = []
    
    for week_info in weeks_to_scrape:
        print(f"\n{'='*80}")
        print(f"SCRAPING WEEK {week_info['week_number']}: {week_info['title']}")
        print(f"{'='*80}")
        
        try:
            bundle = scraper.scrape_week(
                week_number=week_info["week_number"],
                date_range=week_info["date_range"],
                title=week_info["title"]
            )
            
            if bundle and (bundle.get('cfm_lesson_content') or bundle.get('cfm_content')):
                # Add metadata
                bundle['metadata'] = {
                    'week_number': week_info['week_number'],
                    'title': week_info['title'],
                    'date_range': week_info['date_range'],
                    'scraped_at': datetime.now().isoformat(),
                    'scraper_version': '2.0.0'
                }
                
                results.append(bundle)
                successful_weeks.append(week_info['week_number'])
                
                # Save individual JSON bundle
                filename = f"cfm_2026_week_{week_info['week_number']:02d}.json"
                filepath = output_dir / filename
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    json.dump(bundle, f, indent=2, ensure_ascii=False)
                
                # Detailed analysis
                analyze_week_content(bundle)
                
                print(f"💾 Saved: {filename}")
                
            else:
                print(f"❌ Week {week_info['week_number']} failed: No content scraped")
                failed_weeks.append(week_info['week_number'])
            
            # Brief pause between requests
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error scraping Week {week_info['week_number']}: {str(e)}")
            failed_weeks.append(week_info['week_number'])
            import traceback
            traceback.print_exc()
    
    # Overall summary with JSON saving stats
    print(f"\n📊 CFM 2026 COMPLETE YEAR SUMMARY:")
    print(f"   ✅ Successfully scraped: {len(successful_weeks)}/52 weeks")
    print(f"   ❌ Failed scrapes: {len(failed_weeks)} weeks")
    if failed_weeks:
        print(f"   Failed weeks: {failed_weeks}")
    print(f"   📁 Output directory: {output_dir}")
    print(f"   💾 JSON files created: {len(successful_weeks)}")
    
    # Save comprehensive summary
    summary = {
        'scraping_completed_at': datetime.now().isoformat(),
        'total_weeks': 52,
        'successful_scrapes': len(successful_weeks),
        'failed_scrapes': len(failed_weeks),
        'successful_weeks': successful_weeks,
        'failed_weeks': failed_weeks,
        'output_directory': str(output_dir)
    }
    
    summary_file = output_dir / "complete_year_summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"   📊 Summary saved to: {summary_file}")
    
    print_overall_summary(results)
    
    return results

def analyze_week_content(bundle):
    """Detailed analysis of a single week's content"""
    week_num = bundle.get('week_number')
    title = bundle.get('title', 'Unknown')
    cfm_content = bundle.get('cfm_lesson_content', {})
    scripture_content = bundle.get('scripture_content', [])
    
    print(f"✅ Week {week_num} Complete: {title}")
    print(f"🔗 CFM URL: {bundle.get('cfm_lesson_url', 'No URL')}")
    
    # CFM Content Analysis
    print(f"\n📄 CFM LESSON CONTENT:")
    print(f"   • Scripture references: '{cfm_content.get('scripture_references', 'None')}'")
    print(f"   • Introduction: {len(cfm_content.get('introduction', '')):,} characters")
    print(f"   • Learning sections: {len(cfm_content.get('learning_at_home_church', []))} sections")
    print(f"   • Teaching children: {len(cfm_content.get('teaching_children', []))} sections")
    print(f"   • Study helps: {len(cfm_content.get('study_helps', []))} items")
    print(f"   • Total CFM content: {len(cfm_content.get('raw_text', '')):,} characters")
    
    # Learning sections detail
    learning_sections = cfm_content.get('learning_at_home_church', [])
    if learning_sections:
        print(f"   📚 Learning section details:")
        for i, section in enumerate(learning_sections, 1):
            title_sec = section.get('title', 'No title')[:50]
            content_len = len(section.get('content', ''))
            print(f"      {i}. {title_sec}{'...' if len(section.get('title', '')) > 50 else ''} ({content_len:,} chars)")
    
    # Teaching children detail  
    children_sections = cfm_content.get('teaching_children', [])
    if children_sections:
        print(f"   👨‍👩‍👧‍👦 Teaching children details:")
        for i, section in enumerate(children_sections, 1):
            title_sec = section.get('title', 'No title')[:50]
            content_len = len(section.get('content', ''))
            print(f"      {i}. {title_sec}{'...' if len(section.get('title', '')) > 50 else ''} ({content_len:,} chars)")
    
    # Scripture Content Analysis
    if scripture_content:
        total_verses = sum(len(s.get('verses', [])) for s in scripture_content)
        total_chars = sum(len(s.get('full_text', '')) for s in scripture_content)
        
        print(f"\n📜 SCRIPTURE CONTENT:")
        print(f"   • Total chapters: {len(scripture_content)}")
        print(f"   • Total verses: {total_verses:,}")
        print(f"   • Total scripture characters: {total_chars:,}")
        
        print(f"   📖 Individual chapter details:")
        for i, scripture in enumerate(scripture_content, 1):
            ref = scripture.get('reference', 'Unknown')
            verses = len(scripture.get('verses', []))
            chars = len(scripture.get('full_text', ''))
            summary_len = len(scripture.get('summary', ''))
            print(f"      {i}. {ref}: {verses} verses, {chars:,} chars, {summary_len} char summary")
    else:
        print(f"\n📜 SCRIPTURE CONTENT:")
        print(f"   • No scripture chapters (Introduction week)")
    
    # Total bundle size
    cfm_chars = len(cfm_content.get('raw_text', ''))
    scripture_chars = sum(len(s.get('full_text', '')) for s in scripture_content)
    total_chars = cfm_chars + scripture_chars
    print(f"\n🎯 TOTAL BUNDLE: {total_chars:,} characters (CFM: {cfm_chars:,} + Scripture: {scripture_chars:,})")

def print_overall_summary(results):
    """Print comprehensive summary of all weeks"""
    print(f"\n{'='*80}")
    print(f"COMPREHENSIVE SUMMARY - ALL 52 WEEKS")
    print(f"{'='*80}")
    
    total_cfm_chars = 0
    total_scripture_chars = 0
    total_chapters = 0
    total_verses = 0
    successful_weeks = len(results)
    
    print(f"\n📊 WEEK-BY-WEEK SUMMARY:")
    print("-" * 80)
    print(f"{'Week':<4} {'Title':<40} {'Chap':<4} {'Verses':<6} {'CFM Chars':<9} {'Scripture Chars':<13}")
    print("-" * 80)
    
    for bundle in results:
        week_num = bundle.get('week_number')
        title = bundle.get('title', 'Unknown')[:38]
        cfm_content = bundle.get('cfm_lesson_content', {})
        scripture_content = bundle.get('scripture_content', [])
        
        chapters = len(scripture_content)
        verses = sum(len(s.get('verses', [])) for s in scripture_content)
        cfm_chars = len(cfm_content.get('raw_text', ''))
        scripture_chars = sum(len(s.get('full_text', '')) for s in scripture_content)
        
        total_cfm_chars += cfm_chars
        total_scripture_chars += scripture_chars
        total_chapters += chapters
        total_verses += verses
        
        print(f"{week_num:<4} {title:<40} {chapters:<4} {verses:<6} {cfm_chars:<9,} {scripture_chars:<13,}")
    
    print("-" * 80)
    print(f"{'TOTAL':<4} {'52 weeks scraped':<40} {total_chapters:<4} {total_verses:<6} {total_cfm_chars:<9,} {total_scripture_chars:<13,}")
    
    print(f"\n🎯 FINAL STATISTICS:")
    print(f"   ✅ Successfully scraped: {successful_weeks}/52 weeks")
    print(f"   📚 Total scripture chapters: {total_chapters}")
    print(f"   📖 Total verses extracted: {total_verses:,}")
    print(f"   📄 Total CFM content: {total_cfm_chars:,} characters")
    print(f"   📜 Total scripture content: {total_scripture_chars:,} characters")
    print(f"   🎯 Grand total: {total_cfm_chars + total_scripture_chars:,} characters")
    if successful_weeks > 0:
        print(f"   📈 Average per week: {(total_cfm_chars + total_scripture_chars) / successful_weeks:,.0f} characters")
    else:
        print(f"   📈 Average per week: 0 characters (no successful weeks)")

def save_results(results):
    """Save detailed results"""
    output_file = "first_10_weeks_detailed.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Detailed results saved to: {output_file}")
    return output_file

if __name__ == "__main__":
    print("🚀 CFM 2026 COMPLETE YEAR SCRAPER - ALL 52 WEEKS")
    print("=" * 80)
    print("This will scrape all 52 weeks and save them as individual JSON bundles")
    print("Including character counts, verse counts, and content structure analysis")
    print("=" * 80)
    
    try:
        results = scrape_all_52_weeks()
        
        if results:
            print(f"\n🎉 COMPLETE! Successfully scraped {len(results)} weeks")
            print("✅ CFM 2026 Complete Year Bundle Generation Finished!")
        else:
            print("\n❌ No weeks were successfully scraped.")
            
    except KeyboardInterrupt:
        print("\n\n⚠️  Scraping interrupted by user.")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {str(e)}")
        raise