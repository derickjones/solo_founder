#!/usr/bin/env python3
"""
Book of Mormon Scraper for GospelGuide
Scrapes all Book of Mormon content from churchofjesuschrist.org

Usage:
    python scrape_book_of_mormon.py [--limit N] [--output filename.json]
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

class BookOfMormonScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_url = "https://www.churchofjesuschrist.org"

    def scrape_book_of_mormon(self, limit: Optional[int] = None) -> List[Dict]:
        """Scrape all Book of Mormon books"""
        content = []
        logger.info("Scraping Book of Mormon...")
        
        # All Book of Mormon books with their chapters
        bom_books = [
            {"name": "1 Nephi", "code": "1-ne", "chapters": 22},
            {"name": "2 Nephi", "code": "2-ne", "chapters": 33},
            {"name": "Jacob", "code": "jacob", "chapters": 7},
            {"name": "Enos", "code": "enos", "chapters": 1},
            {"name": "Jarom", "code": "jarom", "chapters": 1},
            {"name": "Omni", "code": "omni", "chapters": 1},
            {"name": "Words of Mormon", "code": "w-of-m", "chapters": 1},
            {"name": "Mosiah", "code": "mosiah", "chapters": 29},
            {"name": "Alma", "code": "alma", "chapters": 63},
            {"name": "Helaman", "code": "hel", "chapters": 16},
            {"name": "3 Nephi", "code": "3-ne", "chapters": 30},
            {"name": "4 Nephi", "code": "4-ne", "chapters": 1},
            {"name": "Mormon", "code": "morm", "chapters": 9},
            {"name": "Ether", "code": "ether", "chapters": 15},
            {"name": "Moroni", "code": "moro", "chapters": 10}
        ]
        
        verse_count = 0
        
        for book in bom_books:
            logger.info(f"  Scraping {book['name']}...")
            
            for chapter_num in range(1, book["chapters"] + 1):
                if limit and verse_count >= limit:
                    logger.info(f"Reached limit of {limit} verses")
                    return content
                    
                chapter_url = f"{self.base_url}/study/scriptures/bofm/{book['code']}/{chapter_num}?lang=eng"
                
                try:
                    response = self.session.get(chapter_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    verses = self._extract_bom_verses(soup, book["name"], chapter_num, chapter_url)
                    content.extend(verses)
                    verse_count += len(verses)
                    
                    if verses:
                        logger.info(f"    {book['name']} {chapter_num}: {len(verses)} verses")
                    
                    time.sleep(0.3)  # Rate limiting
                    
                except Exception as e:
                    logger.error(f"Error scraping {book['name']} {chapter_num}: {e}")
                    
        return content

    def _extract_bom_verses(self, soup: BeautifulSoup, book_name: str, chapter_num: int, url: str) -> List[Dict]:
        """Extract verses from Book of Mormon chapter using modern LDS.org structure"""
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
                    "mode_tags": ["default", "book-of-mormon-only", "scholar"],
                    "standard_work": "Book of Mormon",
                    "word_count": len(verse_text.split()),
                    "id": f"bom-{book_name.lower().replace(' ', '-')}-{chapter_num}-{verse_num}"
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
    parser = argparse.ArgumentParser(description='Scrape Book of Mormon content')
    parser.add_argument('--limit', type=int, help='Limit number of verses to scrape')
    parser.add_argument('--output', default='book_of_mormon.json', help='Output filename')
    parser.add_argument('--test', action='store_true', help='Test mode - scrape only first 2 chapters of each book')
    
    args = parser.parse_args()
    
    logger.info("=== Starting Book of Mormon Scraping ===")
    logger.info(f"Limit: {args.limit or 'No limit'}")
    
    scraper = BookOfMormonScraper()
    
    # Test mode limits to first 2 chapters of each book
    if args.test:
        logger.info("Test mode: scraping first 2 chapters of each book")
        content = scraper.scrape_book_of_mormon(limit=100)  # Reasonable test limit
    else:
        content = scraper.scrape_book_of_mormon(limit=args.limit)
    
    scraper.save_content(content, args.output)
    
    logger.info("=== Book of Mormon Scraping Complete ===")
    logger.info(f"Total verses scraped: {len(content)}")

if __name__ == "__main__":
    main()