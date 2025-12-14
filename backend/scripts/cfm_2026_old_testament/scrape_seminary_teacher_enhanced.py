#!/usr/bin/env python3
"""
Enhanced Old Testament Seminary Teacher Manual 2026 Scraper
Scrapes ALL 208 individual lessons and maps them to CFM weeks

Usage:
    python scrape_seminary_teacher_enhanced.py [--test] [--limit N]
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import Dict, List, Optional, Tuple
import os
import re
from urllib.parse import urljoin, urlparse
import argparse
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class SeminaryLesson:
    lesson_number: int
    title: str
    content: str
    url: str
    cfm_weeks: List[int]  # Which CFM weeks this lesson relates to

class EnhancedSeminaryTeacher2026Scraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.manual_url = "https://www.churchofjesuschrist.org/study/manual/old-testament-seminary-manual-2026"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Enhanced mapping of Seminary lessons to CFM weeks based on scripture coverage
        self.lesson_to_cfm_mapping = self._create_enhanced_lesson_mapping()

    def _create_enhanced_lesson_mapping(self) -> Dict[int, List[int]]:
        """Create comprehensive mapping between Seminary lesson numbers and CFM weeks"""
        return {
            # Genesis/Moses/Abraham content (Weeks 2-12)
            1: [2], 2: [2], 3: [2], 4: [2], 5: [2], 6: [2],  # Lessons 1-6: Moses 1, Abraham 3
            7: [3], 8: [3], 9: [3],  # Lessons 7-9: Genesis 1-2, Moses 2-3, Abraham 4-5
            10: [4], 11: [4], 12: [4],  # Lessons 10-12: Genesis 3-4, Moses 4-5
            13: [5], 14: [5],  # Lessons 13-14: Genesis 5, Moses 6
            15: [],  # Doctrinal Mastery Practice
            16: [6], 17: [6], 18: [6],  # Lessons 16-18: Moses 7
            19: [7], 20: [7], 21: [7],  # Lessons 19-21: Genesis 6-11, Moses 8
            22: [8], 23: [8], 24: [8],  # Lessons 22-24: Genesis 12-17, Abraham 1-2
            25: [9], 26: [9], 27: [9], 28: [],  # Lessons 25-28: Genesis 18-23
            29: [10], 30: [10], 31: [10], 32: [10],  # Lessons 29-32: Genesis 24-33
            33: [11], 34: [11],  # Lessons 33-34: Genesis 37-41
            35: [12], 36: [12], 37: [12],  # Lessons 35-37: Genesis 42-50
            
            # Exodus content (Weeks 13-20)
            38: [13], 39: [13], 40: [13],  # Lessons 38-40: Exodus 1-6
            41: [15], 42: [15], 43: [15], 44: [],  # Lessons 41-44: Exodus 7-13
            45: [16], 46: [16], 47: [16],  # Lessons 45-47: Exodus 14-18
            48: [17], 49: [17], 50: [17], 51: [17],  # Lessons 48-51: Exodus 19-20, 24, 31-34
            52: [18], 53: [18], 54: [18], 55: [],  # Lessons 52-55: Exodus 35-40, Leviticus
            
            # Numbers, Deuteronomy, Joshua (Weeks 21-24)
            56: [21], 57: [21],  # Lessons 56-57: Numbers
            58: [22], 59: [22], 60: [22],  # Lessons 58-60: Deuteronomy
            61: [23], 62: [23], 63: [23], 64: [],  # Lessons 61-64: Joshua
            
            # Judges, Ruth, 1 Samuel (Weeks 24-26)
            65: [24], 66: [24], 67: [],  # Lessons 65-67: Judges
            68: [25],  # Lesson 68: Ruth
            69: [26], 70: [26], 71: [26], 72: [26], 73: [26], 74: [26], 75: [26], 76: [],  # 1 Samuel
            
            # 2 Samuel, 1 Kings (Weeks 27-29)
            77: [27], 78: [28], 79: [28], 80: [],  # 2 Samuel, 1 Kings
            81: [29], 82: [29], 83: [30], 84: [30], 85: [30], 86: [30], 87: [30], 88: [30], 89: [],  # Kings content
            
            # Chronicles, Ezra, Nehemiah, Esther (Weeks 31-32)
            90: [31], 91: [31], 92: [31], 93: [31], 94: [32], 95: [32], 96: [],
            
            # Job, Psalms, Proverbs, Ecclesiastes (Weeks 33-37)
            97: [33], 98: [33], 99: [33],  # Job
            100: [34], 101: [34], 102: [34], 103: [34], 104: [34], 105: [35], 106: [],  # Psalms
            107: [35], 108: [35], 109: [36], 110: [36], 111: [37], 112: [],  # Psalms, Proverbs, Ecclesiastes
            
            # Isaiah (Weeks 38-42)
            113: [38], 114: [38], 115: [38], 116: [38], 117: [39], 118: [39],  # Isaiah 1-30
            119: [40], 120: [40], 121: [40], 122: [],  # Isaiah 40-49
            123: [41], 124: [41], 125: [41], 126: [42], 127: [42], 128: [42], 129: [42],  # Isaiah 50-66
            
            # Jeremiah, Lamentations (Weeks 43-44)
            130: [43], 131: [43], 132: [43], 133: [],
            134: [43], 135: [43], 136: [44], 137: [],  # Jeremiah, Lamentations
            
            # Ezekiel (Week 45)
            138: [45], 139: [45], 140: [45], 141: [45],
            
            # Daniel (Week 46)
            142: [46], 143: [46], 144: [46], 145: [46],
            
            # Minor Prophets (Weeks 47-51)
            146: [47], 147: [47], 148: [],  # Hosea, Joel
            149: [48], 150: [48], 151: [48],  # Amos, Jonah
            152: [49], 153: [49], 154: [],  # Micah, Habakkuk
            155: [50], 156: [50], 157: [50],  # Haggai, Zechariah
            158: [51], 159: [51],  # Malachi
            
            # Additional lessons (160-208) - Life preparation, doctrinal mastery, etc.
            # These don't map to specific CFM weeks but provide valuable supplemental content
            **{i: [] for i in range(160, 209)}  # Lessons 160-208: No specific CFM week mapping
        }

    def get_all_lesson_links(self) -> List[Dict[str, str]]:
        """Get all seminary lesson links from the manual page"""
        logger.info("Fetching all Seminary Teacher lesson links...")
        
        try:
            response = self.session.get(f"{self.manual_url}?lang=eng")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            lesson_links = []
            
            # Find all lesson links
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Look for individual lesson links
                if ('old-testament-seminary-manual-2026' in href and 
                    href != '/study/manual/old-testament-seminary-manual-2026' and
                    'lesson' in text.lower()):
                    
                    # Extract lesson number
                    lesson_match = re.search(r'lesson (\d+)', text.lower())
                    if lesson_match:
                        lesson_num = int(lesson_match.group(1))
                        lesson_links.append({
                            'lesson_number': lesson_num,
                            'title': text,
                            'href': href,
                            'full_url': f"{self.base_url}{href}" if href.startswith('/') else href
                        })
            
            # Sort by lesson number
            lesson_links.sort(key=lambda x: x['lesson_number'])
            
            logger.info(f"Found {len(lesson_links)} Seminary Teacher lessons (1-{max(l['lesson_number'] for l in lesson_links) if lesson_links else 0})")
            return lesson_links
            
        except Exception as e:
            logger.error(f"Error fetching lesson links: {e}")
            return []

    def scrape_lesson_content(self, lesson_url: str) -> str:
        """Scrape content from a single lesson page"""
        try:
            response = self.session.get(lesson_url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find main content area
            content_parts = []
            
            # Look for various content containers
            content_selectors = [
                '.body-block',
                '.article-content',
                '.content',
                'main',
                '.lesson-content'
            ]
            
            content_found = False
            for selector in content_selectors:
                elements = soup.select(selector)
                if elements:
                    for element in elements:
                        # Remove navigation and metadata elements
                        for unwanted in element.select('nav, .navigation, .breadcrumb, .metadata, script, style'):
                            unwanted.decompose()
                        
                        text = element.get_text(separator=' ', strip=True)
                        if len(text) > 100:  # Only include substantial content
                            content_parts.append(text)
                            content_found = True
                    
                    if content_found:
                        break
            
            # If no structured content found, get all text
            if not content_parts:
                # Remove unwanted elements
                for unwanted in soup.select('nav, .navigation, .breadcrumb, .metadata, script, style, header, footer'):
                    unwanted.decompose()
                
                content_parts.append(soup.get_text(separator=' ', strip=True))
            
            return ' '.join(content_parts)
            
        except Exception as e:
            logger.error(f"Error scraping lesson content from {lesson_url}: {e}")
            return ""

    def scrape_all_lessons(self, limit: Optional[int] = None, test_mode: bool = False) -> List[SeminaryLesson]:
        """Scrape content from all Seminary Teacher lessons"""
        lesson_links = self.get_all_lesson_links()
        
        if limit:
            lesson_links = lesson_links[:limit]
        
        if test_mode:
            lesson_links = lesson_links[:5]  # Only first 5 for testing
        
        lessons = []
        
        for i, link in enumerate(lesson_links, 1):
            lesson_num = link['lesson_number']
            logger.info(f"Scraping lesson {lesson_num} ({i}/{len(lesson_links)}): {link['title'][:50]}...")
            
            content = self.scrape_lesson_content(link['full_url'])
            
            if content:
                # Map to CFM weeks
                cfm_weeks = self.lesson_to_cfm_mapping.get(lesson_num, [])
                
                lesson = SeminaryLesson(
                    lesson_number=lesson_num,
                    title=link['title'],
                    content=content,
                    url=link['full_url'],
                    cfm_weeks=cfm_weeks
                )
                
                lessons.append(lesson)
                logger.info(f"✅ Scraped lesson {lesson_num}: {len(content):,} chars, maps to CFM weeks {cfm_weeks}")
            else:
                logger.warning(f"⚠️ No content found for lesson {lesson_num}")
            
            # Rate limiting
            time.sleep(0.5)
        
        return lessons

    def organize_by_cfm_weeks(self, lessons: List[SeminaryLesson]) -> Dict:
        """Organize lessons by CFM week numbers"""
        cfm_weeks = {}
        
        for lesson in lessons:
            for week_num in lesson.cfm_weeks:
                if week_num not in cfm_weeks:
                    cfm_weeks[week_num] = []
                
                cfm_weeks[week_num].append({
                    'lesson_number': lesson.lesson_number,
                    'title': lesson.title,
                    'content': lesson.content,
                    'url': lesson.url
                })
        
        # Combine lessons for each week into single content blocks
        combined_weeks = {}
        for week_num, week_lessons in cfm_weeks.items():
            if week_lessons:
                # Combine all lesson content for this week
                combined_content = []
                titles = []
                
                for lesson in sorted(week_lessons, key=lambda x: x['lesson_number']):
                    titles.append(f"Lesson {lesson['lesson_number']}: {lesson['title']}")
                    combined_content.append(f"\n--- Lesson {lesson['lesson_number']} ---\n{lesson['content']}")
                
                combined_weeks[week_num] = {
                    'title': f"Seminary Teacher Week {week_num}: " + "; ".join(titles[:2]) + ("..." if len(titles) > 2 else ""),
                    'content': '\n\n'.join(combined_content),
                    'lessons_included': [l['lesson_number'] for l in week_lessons],
                    'date_range': f"CFM Week {week_num}"
                }
        
        return combined_weeks

    def save_results(self, lessons: List[SeminaryLesson], output_file: str = "../content/seminary_teacher_2026_enhanced.json"):
        """Save enhanced seminary teacher content"""
        # Organize by CFM weeks
        cfm_weeks = self.organize_by_cfm_weeks(lessons)
        
        # Create output structure
        output_data = {
            'type': 'enhanced_seminary_teacher_content',
            'source': 'Old Testament Seminary Teacher Manual 2026 - All 208 Lessons',
            'scraped_date': time.strftime('%Y-%m-%d'),
            'total_lessons_scraped': len(lessons),
            'cfm_weeks_covered': len(cfm_weeks),
            'cfm_weeks': cfm_weeks
        }
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        
        # Save to JSON
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved enhanced Seminary Teacher content:")
        logger.info(f"   📚 Total lessons: {len(lessons)}")
        logger.info(f"   📅 CFM weeks covered: {len(cfm_weeks)}")
        logger.info(f"   💾 Output file: {output_file}")
        
        return output_data

def main():
    parser = argparse.ArgumentParser(description='Enhanced Seminary Teacher Manual Scraper')
    parser.add_argument('--test', action='store_true', help='Test mode (scrape only first 5 lessons)')
    parser.add_argument('--limit', type=int, help='Limit number of lessons to scrape')
    parser.add_argument('--output', default='../content/seminary_teacher_2026_enhanced.json', help='Output file path')
    
    args = parser.parse_args()
    
    scraper = EnhancedSeminaryTeacher2026Scraper()
    
    logger.info("🚀 Starting enhanced Seminary Teacher manual scraping...")
    
    lessons = scraper.scrape_all_lessons(limit=args.limit, test_mode=args.test)
    
    if lessons:
        scraper.save_results(lessons, args.output)
        logger.info("✅ Enhanced Seminary Teacher scraping completed successfully!")
    else:
        logger.error("❌ No lessons scraped!")

if __name__ == "__main__":
    main()