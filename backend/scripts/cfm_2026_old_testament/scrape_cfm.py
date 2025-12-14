#!/usr/bin/env python3
"""
Come Follow Me 2026 Old Testament Scraper (Fixed Version)
Scrapes all weekly lessons including previously missing weeks 5, 14, and 49

Usage:
    python scrape_cfm_2026_fixed.py
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
import os
import re
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CFM2026ScraperFixed:
    """Fixed scraper that captures all 51 weeks (2-52) including missing weeks 5, 14, 49"""
    
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.cfm_url = "https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def scrape_lesson_content(self, week_number: int) -> Optional[Dict[str, Any]]:
        """Scrape content for a specific week"""
        logger.info(f"Scraping Week {week_number}...")
        
        try:
            # Construct URL for this week
            week_url = f"{self.cfm_url}/{week_number:02d}?lang=eng"
            
            response = self.session.get(week_url)
            if response.status_code != 200:
                logger.warning(f"Week {week_number} not found (status: {response.status_code})")
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract title
            title_elem = soup.find('h1') or soup.find('title')
            if not title_elem:
                logger.warning(f"No title found for week {week_number}")
                return None
                
            full_title = title_elem.get_text(strip=True)
            
            # Parse title to extract date range and lesson title
            date_range = ""
            lesson_title = ""
            
            # Extract date range (look for pattern like "January 5–11" or "March 30–April 5")
            date_match = re.search(r'([A-Za-z]+ \d+–\d+|[A-Za-z]+ \d+–[A-Za-z]+ \d+)', full_title)
            if date_match:
                date_range = date_match.group(1)
            
            # Extract lesson title (content between quotes or after colon)
            if '"' in full_title:
                title_parts = full_title.split('"')
                if len(title_parts) >= 3:
                    lesson_title = title_parts[1].strip()
            elif ':' in full_title:
                title_parts = full_title.split(':', 1)
                if len(title_parts) > 1:
                    lesson_title = title_parts[1].strip()
            else:
                lesson_title = full_title.strip()
            
            # Clean up lesson title
            lesson_title = lesson_title.replace(date_range, '').strip()
            if lesson_title.startswith(':'):
                lesson_title = lesson_title[1:].strip()
            if lesson_title.startswith('.'):
                lesson_title = lesson_title[1:].strip()
                
            # Extract main content
            main_content = ""
            content_sections = soup.find_all(['div', 'section'], class_=['body-block', 'content', 'study-content'])
            
            for section in content_sections:
                # Skip navigation and header elements
                if any(cls in str(section.get('class', [])) for cls in ['nav', 'header', 'footer', 'breadcrumb']):
                    continue
                text = section.get_text(separator='\n', strip=True)
                if text and len(text) > 50:  # Only include substantial content
                    main_content += text + "\n\n"
            
            # If no main content found, try to get all paragraph text
            if not main_content:
                paragraphs = soup.find_all(['p', 'li', 'div'], text=True)
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:
                        main_content += text + "\n"
            
            # Parse scripture references from title
            primary_scriptures = self.parse_scripture_references(lesson_title)
            
            # Identify themes from content
            themes = self.extract_themes(main_content + " " + lesson_title)
            
            lesson_data = {
                "week_number": week_number,
                "date_range": date_range + lesson_title.split(';')[0] if ';' in lesson_title else date_range,  # Include scripture refs
                "title": lesson_title,
                "primary_scriptures": primary_scriptures,
                "basic_tier": {
                    "title": lesson_title,
                    "content": main_content,
                    "subsections": [],
                    "teaching_ideas": [],
                    "discussion_questions": [],
                    "cross_references": []
                },
                "intermediate_tier": {
                    "title": f"Teaching {lesson_title}",
                    "content": "",
                    "subsections": [],
                    "teaching_ideas": [],
                    "discussion_questions": [],
                    "cross_references": []
                },
                "advanced_tier": {
                    "title": f"Scholarly Study of {lesson_title}",
                    "content": "",
                    "subsections": [],
                    "teaching_ideas": [],
                    "discussion_questions": [],
                    "cross_references": []
                },
                "themes": themes,
                "doctrinal_mastery": [],
                "related_content": []
            }
            
            logger.info(f"✅ Scraped Week {week_number}: {lesson_title}")
            time.sleep(1)  # Be respectful to the server
            return lesson_data
            
        except Exception as e:
            logger.error(f"Error scraping Week {week_number}: {e}")
            return None

    def parse_scripture_references(self, text: str) -> List[Dict[str, Any]]:
        """Parse scripture references from text"""
        references = []
        
        # Common scripture reference patterns
        patterns = [
            r'(Moses|Abraham|Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1 Samuel|2 Samuel|1 Kings|2 Kings|1 Chronicles|2 Chronicles|Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi)\s+(\d+(?:[–-]\d+)?)',
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                book, chapters = match.groups()
                
                # Parse chapter ranges
                chapter_list = []
                if '–' in chapters or '-' in chapters:
                    start, end = re.split('[–-]', chapters)
                    chapter_list = [str(i) for i in range(int(start), int(end) + 1)]
                else:
                    chapter_list = [chapters]
                
                # Determine book type
                book_type = "old_testament"
                if book.lower() in ['moses', 'abraham']:
                    book_type = "pearl_of_great_price"
                
                references.append({
                    "book": book,
                    "chapters": chapter_list,
                    "verses": None,
                    "book_type": book_type
                })
        
        return references

    def extract_themes(self, content: str) -> List[str]:
        """Extract themes from content"""
        themes = []
        content_lower = content.lower()
        
        theme_keywords = [
            'savior', 'jesus christ', 'atonement', 'redemption', 'salvation',
            'faith', 'repentance', 'baptism', 'holy ghost', 'prayer',
            'family', 'marriage', 'covenant', 'temple', 'priesthood',
            'obedience', 'service', 'charity', 'love', 'forgiveness'
        ]
        
        for keyword in theme_keywords:
            if keyword in content_lower:
                themes.append(keyword.title())
        
        return list(set(themes))  # Remove duplicates

    def scrape_all_lessons(self) -> Dict[str, Any]:
        """Scrape all weekly lessons (weeks 2-52)"""
        logger.info("Starting complete CFM 2026 Old Testament scraping...")
        
        lessons = []
        successful_scrapes = 0
        
        # Systematically check each week from 2 to 52
        for week_num in range(2, 53):
            lesson_data = self.scrape_lesson_content(week_num)
            if lesson_data:
                lessons.append(lesson_data)
                successful_scrapes += 1
            else:
                logger.warning(f"Failed to scrape Week {week_num}")
        
        # Create complete dataset
        dataset = {
            "year": 2026,
            "testament": "Old Testament",
            "metadata": {
                "description": "Come Follow Me Complete Dataset for Old Testament 2026",
                "sources": ["Come, Follow Me—For Home and Church: Old Testament 2026"],
                "scraped_date": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_lessons_expected": 51,  # Weeks 2-52
                "total_lessons_scraped": successful_scrapes,
                "missing_weeks": [i for i in range(2, 53) if not any(l['week_number'] == i for l in lessons)],
                "scraper_version": "2.0 (Fixed)"
            },
            "lessons": lessons,
            "total_lessons": len(lessons),
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        return dataset

def main():
    scraper = CFM2026ScraperFixed()
    dataset = scraper.scrape_all_lessons()
    
    # Save to file
    output_file = "../content/cfm_2026_basic.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dataset, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ CFM 2026 scraping complete!")
    logger.info(f"   📚 Expected: {dataset['metadata']['total_lessons_expected']} lessons")
    logger.info(f"   📚 Scraped: {dataset['metadata']['total_lessons_scraped']} lessons")
    logger.info(f"   💾 Saved to {output_file}")
    
    missing = dataset['metadata']['missing_weeks']
    if missing:
        logger.warning(f"   ⚠️  Missing weeks: {missing}")
    else:
        logger.info(f"   ✅ All weeks successfully scraped!")
    
    # Show sample lesson
    if dataset['lessons']:
        sample = dataset['lessons'][0]
        logger.info(f"   📖 Sample: Week {sample['week_number']} - {sample['title']}")

if __name__ == "__main__":
    main()