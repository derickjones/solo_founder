#!/usr/bin/env python3
"""
Pearl of Great Price Scraper for GospelGuide
Scrapes all Pearl of Great Price content from churchofjesuschrist.org

Usage:
    python scrape_pearl_great_price.py [--limit N] [--output filename.json]
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

class PearlOfGreatPriceScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_url = "https://www.churchofjesuschrist.org"

    def scrape_pearl_of_great_price(self, limit: Optional[int] = None) -> List[Dict]:
        """Scrape Pearl of Great Price books"""
        content = []
        logger.info("Scraping Pearl of Great Price...")
        
        # Pearl of Great Price books
        pogp_books = [
            {"name": "Moses", "code": "moses", "chapters": 8},
            {"name": "Abraham", "code": "abr", "chapters": 5},
            {"name": "Joseph Smith—Matthew", "code": "js-m", "chapters": 1},
            {"name": "Joseph Smith—History", "code": "js-h", "chapters": 1},
            {"name": "Articles of Faith", "code": "a-of-f", "chapters": 1},
        ]
        
        verse_count = 0
        
        for book in pogp_books:
            logger.info(f"  Scraping {book['name']}...")
            
            for chapter_num in range(1, book["chapters"] + 1):
                if limit and verse_count >= limit:
                    logger.info(f"Reached limit of {limit} verses")
                    return content
                    
                chapter_url = f"{self.base_url}/study/scriptures/pgp/{book['code']}/{chapter_num}?lang=eng"
                
                try:
                    response = self.session.get(chapter_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    verses = self._extract_pogp_verses(soup, book["name"], chapter_num, chapter_url)
                    content.extend(verses)
                    verse_count += len(verses)
                    
                    if verses:
                        logger.info(f"    {book['name']} {chapter_num}: {len(verses)} verses")
                        
                    time.sleep(0.3)
                    
                except Exception as e:
                    logger.error(f"Error scraping {book['name']} {chapter_num}: {e}")
                    
        return content

    def _extract_pogp_verses(self, soup: BeautifulSoup, book_name: str, chapter_num: int, url: str) -> List[Dict]:
        """Extract verses from Pearl of Great Price chapter using modern LDS.org structure"""
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
                
                verse_data = {
                    "citation": citation,
                    "content": verse_text,
                    "source_type": "scripture",
                    "book": book_name,
                    "chapter": chapter_num,
                    "verse": verse_num,
                    "url": url,
                    "mode_tags": ["default", "scholar"],
                    "standard_work": "Pearl of Great Price",
                    "word_count": len(verse_text.split()),
                    "id": f"pogp-{book_name.lower().replace(' ', '-').replace('—', '-')}-{chapter_num}-{verse_num}"
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
    parser = argparse.ArgumentParser(description='Scrape Pearl of Great Price content')
    parser.add_argument('--limit', type=int, help='Limit number of verses to scrape')
    parser.add_argument('--output', default='pearl_of_great_price.json', help='Output filename')
    parser.add_argument('--test', action='store_true', help='Test mode - scrape only first chapter of each book')
    
    args = parser.parse_args()
    
    logger.info("=== Starting Pearl of Great Price Scraping ===")
    logger.info(f"Limit: {args.limit or 'No limit'}")
    
    scraper = PearlOfGreatPriceScraper()
    
    # Test mode limits to first chapter of each book
    if args.test:
        logger.info("Test mode: scraping first chapter of each book")
        content = scraper.scrape_pearl_of_great_price(limit=50)  # Reasonable test limit
    else:
        content = scraper.scrape_pearl_of_great_price(limit=args.limit)
    
    scraper.save_content(content, args.output)
    
    logger.info("=== Pearl of Great Price Scraping Complete ===")
    logger.info(f"Total verses scraped: {len(content)}")

if __name__ == "__main__":
    main()