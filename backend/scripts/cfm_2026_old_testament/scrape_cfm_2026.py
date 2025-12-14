#!/usr/bin/env python3
"""
Come Follow Me 2026 Old Testament Scraper
Scrapes weekly lessons from Come, Follow Me—For Home and Church: Old Testament 2026

Usage:
    python scrape_cfm_2026.py [--test] [--limit N]
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import Dict, List, Optional
import os
import re
from urllib.parse import urljoin, urlparse
import argparse
from dataclasses import dataclass
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CFM2026Scraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.cfm_url = "https://www.churchofjesuschrist.org/study/manual/come-follow-me-for-home-and-church-old-testament-2026"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def get_weekly_lesson_links(self) -> List[Dict[str, str]]:
        """Get all weekly lesson links - systematically check weeks 2-52"""
        logger.info("Getting weekly lesson links...")
        
        lesson_links = []
        
        # Systematically check each week from 2 to 52
        for week_num in range(2, 53):
            try:
                # Construct URL for this week
                week_url = f"{self.cfm_url}/{week_num:02d}?lang=eng"
                
                # Try to access the page
                response = self.session.get(week_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Try to extract date range and title from the page
                    title_elem = soup.find('h1') or soup.find('title')
                    if title_elem:
                        full_title = title_elem.get_text(strip=True)
                        
                        # Extract date range (look for pattern like "January 5–11" or "March 30–April 5")
                        date_match = re.search(r'([A-Za-z]+ \d+–\d+|[A-Za-z]+ \d+–[A-Za-z]+ \d+)', full_title)
                        if date_match:
                            date_range = date_match.group(1)
                        else:
                            # Fallback - use the beginning of title as date range
                            date_range = full_title.split(':')[0].strip() if ':' in full_title else full_title.strip()
                        
                        # Extract lesson title (after date, colon, and quotes)
                        title_parts = full_title.split('"')
                        if len(title_parts) >= 3:
                            lesson_title = title_parts[1].strip()  # Content between first pair of quotes
                        else:
                            # Fallback to splitting by colon
                            title_parts = full_title.split(':')
                            if len(title_parts) > 1:
                                lesson_title = ':'.join(title_parts[1:]).strip()
                            else:
                                lesson_title = full_title.strip()
                        
                        lesson_links.append({
                            'week_number': week_num,
                            'date_range': date_range,
                            'title': lesson_title,
                            'url': week_url
                        })
                        
                        logger.info(f"Found Week {week_num}: {date_range} - {lesson_title}")
                else:
                    logger.debug(f"Week {week_num} not found (status: {response.status_code})")
                    
            except Exception as e:
                logger.debug(f"Error checking week {week_num}: {e}")
                continue
        
        # Sort by week number
        lesson_links.sort(key=lambda x: x['week_number'])
        
        logger.info(f"Found {len(lesson_links)} weekly lessons total")
        return lesson_links

    def parse_scripture_references(self, text: str) -> List[ScriptureReference]:
        """Parse scripture references from text"""
        references = []
        
        # Common scripture reference patterns
        patterns = [
            r'(Moses|Abraham|Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1 Samuel|2 Samuel|1 Kings|2 Kings|1 Chronicles|2 Chronicles|Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|Ecclesiastes|Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi)\s+(\d+(?:[–-]\d+)?)',
            r'(JST|Joseph Smith Translation)\s+(Genesis|Exodus|Leviticus|Numbers|Deuteronomy)\s+(\d+(?:[–-]\d+)?)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                if len(match.groups()) == 2:
                    book, chapters = match.groups()
                elif len(match.groups()) == 3:
                    prefix, book, chapters = match.groups()
                    book = f"{prefix} {book}" if prefix else book
                else:
                    continue
                
                # Parse chapter ranges
                chapter_list = []
                if '–' in chapters or '-' in chapters:
                    # Handle ranges like "1-3" or "1–3"
                    start, end = re.split('[–-]', chapters)
                    chapter_list = [str(i) for i in range(int(start), int(end) + 1)]
                else:
                    chapter_list = [chapters]
                
                # Determine book type
                book_type = "standard_works"
                if book.lower() in ['moses', 'abraham']:
                    book_type = "pearl_of_great_price"
                elif book.startswith('JST'):
                    book_type = "jst"
                
                references.append(ScriptureReference(
                    book=book,
                    chapters=chapter_list,
                    book_type=book_type
                ))
        
        return references

    def scrape_lesson_content(self, lesson_info: Dict) -> Optional[WeeklyLesson]:
        """Scrape content for a specific lesson"""
        logger.info(f"Scraping lesson {lesson_info['week_number']}: {lesson_info['title']}")
        
        try:
            response = self.session.get(lesson_info['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content
            main_content = soup.find('div', class_='body-block') or soup.find('main')
            if not main_content:
                logger.warning(f"Could not find main content for lesson {lesson_info['week_number']}")
                return None
            
            # Extract title and scripture references
            title_elem = soup.find('h1') or soup.find('title')
            title = title_elem.get_text(strip=True) if title_elem else lesson_info['title']
            
            # Clean up title to extract just the lesson title
            title_parts = title.split('—')
            if len(title_parts) > 1:
                lesson_title = title_parts[-1].strip()
            else:
                lesson_title = title.strip()
            
            # Extract scripture references from title
            primary_scriptures = self.parse_scripture_references(title)
            
            # Extract main content sections
            content_text = ""
            teaching_ideas = []
            discussion_questions = []
            subsections = []
            
            # Get all paragraphs and sections
            for elem in main_content.find_all(['p', 'h2', 'h3', 'h4', 'li', 'blockquote']):
                text = elem.get_text(strip=True)
                if not text:
                    continue
                
                # Categorize content
                if elem.name in ['h2', 'h3', 'h4']:
                    subsections.append({
                        'type': 'heading',
                        'level': elem.name,
                        'text': text
                    })
                elif 'idea' in text.lower() or 'activity' in text.lower():
                    teaching_ideas.append(text)
                elif '?' in text and len(text) < 200:
                    discussion_questions.append(text)
                else:
                    content_text += text + "\n\n"
            
            # Extract cross-references
            cross_references = []
            for link in main_content.find_all('a', href=True):
                href = link.get('href', '')
                if '/study/' in href and any(book in href.lower() for book in ['genesis', 'exodus', 'moses', 'abraham']):
                    ref_text = link.get_text(strip=True)
                    refs = self.parse_scripture_references(ref_text)
                    cross_references.extend(refs)
            
            # Create content section
            basic_tier = ContentSection(
                title=lesson_title,
                content=content_text.strip(),
                subsections=subsections,
                teaching_ideas=teaching_ideas,
                discussion_questions=discussion_questions,
                cross_references=cross_references
            )
            
            # Extract themes from content
            themes = []
            theme_keywords = ['jesus christ', 'savior', 'atonement', 'covenant', 'faith', 'repentance', 'baptism', 'holy ghost', 'temple', 'family', 'prophecy']
            content_lower = content_text.lower()
            for keyword in theme_keywords:
                if keyword in content_lower:
                    themes.append(keyword.title())
            
            # Create weekly lesson
            lesson = WeeklyLesson(
                week_number=lesson_info['week_number'],
                date_range=lesson_info['date_range'],
                title=lesson_title,
                primary_scriptures=primary_scriptures,
                basic_tier=basic_tier,
                intermediate_tier=ContentSection(
                    title=f"Teaching {lesson_title}",
                    content="",  # Will be filled by seminary teacher manual scraper
                    subsections=[],
                    teaching_ideas=[],
                    discussion_questions=[],
                    cross_references=[]
                ),
                advanced_tier=ContentSection(
                    title=f"Scholarly Study of {lesson_title}",
                    content="",  # Will be filled by seminary student manual scraper
                    subsections=[],
                    teaching_ideas=[],
                    discussion_questions=[],
                    cross_references=[]
                ),
                themes=list(set(themes))  # Remove duplicates
            )
            
            time.sleep(1)  # Be respectful to the server
            return lesson
            
        except Exception as e:
            logger.error(f"Error scraping lesson {lesson_info['week_number']}: {e}")
            return None

    def scrape_all_lessons(self, limit: Optional[int] = None, test_mode: bool = False) -> CFMDeepDiveDataset:
        """Scrape all weekly lessons"""
        logger.info("Starting CFM 2026 Old Testament scraping...")
        
        # Get lesson links
        lesson_links = self.get_weekly_lesson_links()
        
        if test_mode:
            lesson_links = lesson_links[:3]  # Only first 3 lessons in test mode
        elif limit:
            lesson_links = lesson_links[:limit]
        
        lessons = []
        for lesson_info in lesson_links:
            lesson = self.scrape_lesson_content(lesson_info)
            if lesson:
                lessons.append(lesson)
            else:
                logger.warning(f"Failed to scrape lesson {lesson_info['week_number']}")
        
        # Create dataset
        dataset = CFMDeepDiveDataset(
            year=2026,
            testament="Old Testament",
            lessons=lessons,
            metadata={
                "description": "Come Follow Me Deep Dive for Old Testament 2026",
                "sources": [
                    "Come, Follow Me—For Home and Church: Old Testament 2026"
                ],
                "scraped_date": time.strftime("%Y-%m-%d"),
                "total_lessons_scraped": len(lessons),
                "scraper_version": "1.0"
            }
        )
        
        return dataset

def main():
    parser = argparse.ArgumentParser(description="Scrape CFM 2026 Old Testament lessons")
    parser.add_argument("--test", action="store_true", help="Test mode - only scrape first 3 lessons")
    parser.add_argument("--limit", type=int, help="Limit number of lessons to scrape")
    parser.add_argument("--output", default="content/cfm_2026_basic.json", help="Output file path")
    
    args = parser.parse_args()
    
    scraper = CFM2026Scraper()
    dataset = scraper.scrape_all_lessons(limit=args.limit, test_mode=args.test)
    
    # Save to file
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    dataset.save_to_json(args.output)
    
    logger.info(f"✅ CFM 2026 scraping complete!")
    logger.info(f"   📚 Scraped {len(dataset.lessons)} lessons")
    logger.info(f"   💾 Saved to {args.output}")
    
    # Show sample lesson
    if dataset.lessons:
        sample = dataset.lessons[0]
        logger.info(f"   📖 Sample: Week {sample.week_number} - {sample.title}")
        logger.info(f"   📜 Primary scriptures: {[f'{ref.book} {ref.chapters}' for ref in sample.primary_scriptures]}")

if __name__ == "__main__":
    main()