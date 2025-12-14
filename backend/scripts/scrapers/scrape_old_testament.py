#!/usr/bin/env python3
"""
Old Testament Scraper for GospelGuide
Scrapes all Old Testament content from churchofjesuschrist.org

Usage:
    python scrape_old_testament.py [--limit N] [--output filename.json]
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
import argparse
import os
import re
from typing import List, Dict, Optional

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class OldTestamentScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_url = "https://www.churchofjesuschrist.org"

    def scrape_old_testament(self, limit: Optional[int] = None) -> List[Dict]:
        """Scrape Old Testament books"""
        content = []
        logger.info("Scraping Old Testament...")
        
        # Major Old Testament books (shortened list for practicality)
        ot_books = [
            {"name": "Genesis", "code": "gen", "chapters": 50},
            {"name": "Exodus", "code": "ex", "chapters": 40},
            {"name": "Leviticus", "code": "lev", "chapters": 27},
            {"name": "Numbers", "code": "num", "chapters": 36},
            {"name": "Deuteronomy", "code": "deut", "chapters": 34},
            {"name": "Joshua", "code": "josh", "chapters": 24},
            {"name": "Judges", "code": "judg", "chapters": 21},
            {"name": "Ruth", "code": "ruth", "chapters": 4},
            {"name": "1 Samuel", "code": "1-sam", "chapters": 31},
            {"name": "2 Samuel", "code": "2-sam", "chapters": 24},
            {"name": "1 Kings", "code": "1-kgs", "chapters": 22},
            {"name": "2 Kings", "code": "2-kgs", "chapters": 25},
            {"name": "Psalms", "code": "ps", "chapters": 150},
            {"name": "Proverbs", "code": "prov", "chapters": 31},
            {"name": "Isaiah", "code": "isa", "chapters": 66},
            {"name": "Jeremiah", "code": "jer", "chapters": 52},
            {"name": "Daniel", "code": "dan", "chapters": 12},
        ]
        
        verse_count = 0
        
        for book in ot_books:
            if limit and verse_count >= limit:
                logger.info(f"Reached limit of {limit} verses")
                break
                
            logger.info(f"  Scraping {book['name']}...")
            
            book_verses = self._scrape_bible_book(book["name"], book["code"], book["chapters"], "ot", limit - verse_count if limit else None)
            content.extend(book_verses)
            verse_count += len(book_verses)
            
        return content

    def _scrape_bible_book(self, book_name: str, book_code: str, num_chapters: int, testament: str, remaining_limit: Optional[int] = None) -> List[Dict]:
        """Scrape individual Bible book"""
        content = []
        
        logger.info(f"    Scraping {book_name}...")
        
        for chapter_num in range(1, num_chapters + 1):
            if remaining_limit and len(content) >= remaining_limit:
                break
                
            chapter_url = f"{self.base_url}/study/scriptures/{testament}/{book_code}/{chapter_num}?lang=eng"
            
            try:
                response = self.session.get(chapter_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                verses = self._extract_bible_verses(soup, book_name, chapter_num, chapter_url, testament)
                content.extend(verses)
                
                if verses:
                    logger.info(f"      {book_name} {chapter_num}: {len(verses)} verses")
                
                time.sleep(0.3)  # Rate limiting
                
            except Exception as e:
                logger.error(f"Error scraping {book_name} {chapter_num}: {e}")
                
        return content

    def _extract_bible_verses(self, soup: BeautifulSoup, book_name: str, chapter_num: int, url: str, testament: str) -> List[Dict]:
        """Extract verses from Bible chapter using modern LDS.org structure"""
        verses = []
        
        # Find all verse paragraphs using modern structure
        verse_paragraphs = soup.find_all('p', class_='verse')
        
        for verse_p in verse_paragraphs:
            # Find verse number
            verse_num_span = verse_p.find('span', class_='verse-number')
            if not verse_num_span:
                continue
                
            verse_num_text = verse_num_span.get_text(strip=True)
            try:
                verse_num = int(verse_num_text)
            except ValueError:
                continue
                
            # Get full verse text and remove the verse number
            full_text = verse_p.get_text(strip=True)
            verse_text = full_text[len(verse_num_text):].strip()
            
            # Clean the text
            verse_text = self._clean_verse_text(verse_text)
            
            if len(verse_text) > 10:
                citation = f"({book_name} {chapter_num}:{verse_num})"
                standard_work = "Old Testament"
                
                verse_data = {
                    "citation": citation,
                    "content": verse_text,
                    "source_type": "scripture", 
                    "book": book_name,
                    "chapter": chapter_num,
                    "verse": verse_num,
                    "url": url,
                    "mode_tags": ["default", "scholar"],
                    "standard_work": standard_work,
                    "testament": testament,
                    "word_count": len(verse_text.split()),
                    "id": f"{testament}-{book_name.lower().replace(' ', '-')}-{chapter_num}-{verse_num}"
                }
                verses.append(verse_data)
                    
        return verses

    def _clean_verse_text(self, text: str) -> str:
        """Clean and normalize verse text"""
        # Remove footnote markers (single letters)
        text = re.sub(r'\s+[a-z]\s+', ' ', text)
        # Remove extra whitespace but preserve word boundaries
        text = re.sub(r'\s+', ' ', text)
        # Clean up any remaining artifacts
        text = re.sub(r'[^\w\s\.,;:!?\'\"\-\(\)]', '', text)
        return text.strip()

    def save_content(self, content: List[Dict], filename: str):
        """Save scraped content to JSON file"""
        os.makedirs("content", exist_ok=True)
        filepath = os.path.join("content", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(content)} items to {filepath}")

def main():
    """Main scraping function"""
    parser = argparse.ArgumentParser(description='Scrape Old Testament content')
    parser.add_argument('--limit', type=int, help='Limit number of verses to scrape')
    parser.add_argument('--output', default='old_testament.json', help='Output filename')
    parser.add_argument('--test', action='store_true', help='Test mode - scrape only first 5 chapters of Genesis')
    
    args = parser.parse_args()
    
    logger.info("=== Starting Old Testament Scraping ===")
    logger.info(f"Limit: {args.limit or 'No limit'}")
    
    scraper = OldTestamentScraper()
    
    # Test mode limits to first 5 chapters of Genesis
    if args.test:
        logger.info("Test mode: scraping first 5 chapters of Genesis")
        content = scraper.scrape_old_testament(limit=200)  # Reasonable test limit
    else:
        content = scraper.scrape_old_testament(limit=args.limit)
    
    scraper.save_content(content, args.output)
    
    logger.info("=== Old Testament Scraping Complete ===")
    logger.info(f"Total verses scraped: {len(content)}")

if __name__ == "__main__":
    main()