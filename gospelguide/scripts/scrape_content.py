#!/usr/bin/env python3
"""
GospelGuide Content Scraper
Scrapes LDS Standard Works and General Conference talks from LDS.org
Outputs structured JSON files with verse-level granularity for AI processing
"""

import requests
import json
import time
import re
from typing import List, Dict, Any
from pathlib import Path
from urllib.parse import urljoin
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LDSContentScraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
        
        # Output directories
        self.output_dir = Path("content")
        self.output_dir.mkdir(exist_ok=True)
        
    def scrape_book_of_mormon(self) -> List[Dict[str, Any]]:
        """Scrape Book of Mormon verses with complete metadata"""
        logger.info("Starting Book of Mormon scrape...")
        
        verses = []
        
        # Book of Mormon structure (simplified - you'll need complete list)
        bom_books = [
            {"name": "1 Nephi", "chapters": 22},
            {"name": "2 Nephi", "chapters": 33}, 
            {"name": "Jacob", "chapters": 7},
            {"name": "Enos", "chapters": 1},
            {"name": "Jarom", "chapters": 1},
            {"name": "Omni", "chapters": 1},
            {"name": "Words of Mormon", "chapters": 1},
            {"name": "Mosiah", "chapters": 29},
            {"name": "Alma", "chapters": 63},
            {"name": "Helaman", "chapters": 16},
            {"name": "3 Nephi", "chapters": 30},
            {"name": "4 Nephi", "chapters": 1},
            {"name": "Mormon", "chapters": 9},
            {"name": "Ether", "chapters": 15},
            {"name": "Moroni", "chapters": 10}
        ]
        
        for book in bom_books:
            for chapter in range(1, book["chapters"] + 1):
                chapter_verses = self.scrape_chapter(book["name"], chapter)
                verses.extend(chapter_verses)
                time.sleep(0.5)  # Be respectful to LDS.org servers
                
        logger.info(f"Scraped {len(verses)} Book of Mormon verses")
        return verses
    
    def scrape_chapter(self, book_name: str, chapter_num: int) -> List[Dict[str, Any]]:
        """Scrape individual chapter and return verse-level data"""
        try:
            # Construct LDS.org URL for the chapter
            book_slug = book_name.lower().replace(" ", "-")
            url = f"{self.base_url}/study/scriptures/bofm/{book_slug}/{chapter_num}"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            # You'll need to parse the HTML structure here
            # LDS.org uses specific CSS classes for verses
            verses = self.parse_chapter_html(response.text, book_name, chapter_num)
            
            return verses
            
        except Exception as e:
            logger.error(f"Error scraping {book_name} {chapter_num}: {e}")
            return []
    
    def parse_chapter_html(self, html: str, book_name: str, chapter_num: int) -> List[Dict[str, Any]]:
        """Parse HTML and extract verse data"""
        from bs4 import BeautifulSoup
        
        soup = BeautifulSoup(html, 'html.parser')
        verses = []
        
        # Find all verse elements (you'll need to inspect LDS.org HTML structure)
        verse_elements = soup.find_all('p', class_='verse')
        
        for verse_elem in verse_elements:
            verse_num = self.extract_verse_number(verse_elem)
            if verse_num:
                verse_text = self.clean_verse_text(verse_elem.get_text())
                
                verse_data = {
                    "id": f"{book_name.lower().replace(' ', '-')}-{chapter_num}-{verse_num}",
                    "content": verse_text,
                    "source_type": "scripture",
                    "book": book_name,
                    "chapter": chapter_num,
                    "verse_start": verse_num,
                    "verse_end": verse_num,
                    "scripture_ref": f"{book_name} {chapter_num}:{verse_num}",
                    "citation": f"({book_name} {chapter_num}:{verse_num})",
                    "word_count": len(verse_text.split()),
                    "standard_work": "Book of Mormon"
                }
                
                verses.append(verse_data)
        
        return verses
    
    def extract_verse_number(self, verse_elem) -> int:
        """Extract verse number from HTML element"""
        # Look for verse number span or data attribute
        verse_span = verse_elem.find('span', class_='verse-number')
        if verse_span:
            # Extract number from text like "7 "
            match = re.search(r'(\d+)', verse_span.get_text())
            if match:
                return int(match.group(1))
        return None
    
    def clean_verse_text(self, text: str) -> str:
        """Clean and normalize verse text"""
        # Remove verse numbers, extra whitespace, etc.
        text = re.sub(r'^\d+\s+', '', text)  # Remove leading verse number
        text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
        return text.strip()
    
    def scrape_doctrine_and_covenants(self) -> List[Dict[str, Any]]:
        """Scrape D&C with section-level granularity"""
        logger.info("Starting Doctrine & Covenants scrape...")
        
        verses = []
        
        # D&C has 138 sections plus Official Declarations
        for section in range(1, 139):
            section_verses = self.scrape_dc_section(section)
            verses.extend(section_verses)
            time.sleep(0.5)
            
        # Add Official Declarations
        for od_num in [1, 2]:
            od_data = self.scrape_official_declaration(od_num)
            verses.extend(od_data)
            
        logger.info(f"Scraped {len(verses)} D&C verses")
        return verses
    
    def scrape_dc_section(self, section_num: int) -> List[Dict[str, Any]]:
        """Scrape individual D&C section"""
        try:
            url = f"{self.base_url}/study/scriptures/dc-testament/dc/{section_num}"
            response = self.session.get(url)
            response.raise_for_status()
            
            return self.parse_dc_html(response.text, section_num)
            
        except Exception as e:
            logger.error(f"Error scraping D&C {section_num}: {e}")
            return []
    
    def scrape_general_conference(self, start_year: int = 1971, end_year: int = 2025) -> List[Dict[str, Any]]:
        """Scrape General Conference talks with speaker/date metadata"""
        logger.info(f"Starting General Conference scrape ({start_year}-{end_year})...")
        
        talks = []
        
        for year in range(start_year, end_year + 1):
            for session in ["april", "october"]:
                year_talks = self.scrape_conference_session(year, session)
                talks.extend(year_talks)
                time.sleep(1)  # Be extra respectful for conference content
                
        logger.info(f"Scraped {len(talks)} conference talk chunks")
        return talks
    
    def scrape_conference_session(self, year: int, session: str) -> List[Dict[str, Any]]:
        """Scrape all talks from a conference session"""
        try:
            # Get session index page
            url = f"{self.base_url}/study/general-conference/{year}/{session}"
            response = self.session.get(url)
            response.raise_for_status()
            
            # Parse talk links from session page
            talk_urls = self.extract_talk_urls(response.text, year, session)
            
            talks = []
            for talk_url in talk_urls:
                talk_data = self.scrape_individual_talk(talk_url, year, session)
                if talk_data:
                    talks.extend(talk_data)
                time.sleep(0.3)
                    
            return talks
            
        except Exception as e:
            logger.error(f"Error scraping {session} {year} conference: {e}")
            return []
    
    def save_content(self, content: List[Dict[str, Any]], filename: str):
        """Save scraped content to JSON file"""
        filepath = self.output_dir / f"{filename}.json"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
            
        logger.info(f"Saved {len(content)} items to {filepath}")

def main():
    """Main scraping workflow"""
    scraper = LDSContentScraper()
    
    # Scrape Standard Works
    logger.info("=== Starting Standard Works Scraping ===")
    
    # Book of Mormon
    bom_verses = scraper.scrape_book_of_mormon()
    scraper.save_content(bom_verses, "book_of_mormon")
    
    # Doctrine & Covenants  
    dc_verses = scraper.scrape_doctrine_and_covenants()
    scraper.save_content(dc_verses, "doctrine_and_covenants")
    
    # Pearl of Great Price (you'd implement similar methods)
    # pogp_verses = scraper.scrape_pearl_of_great_price()
    # scraper.save_content(pogp_verses, "pearl_of_great_price")
    
    # Bible (if needed - this would be massive)
    # bible_verses = scraper.scrape_bible()
    # scraper.save_content(bible_verses, "bible")
    
    # General Conference
    logger.info("=== Starting General Conference Scraping ===")
    conference_talks = scraper.scrape_general_conference(1971, 2025)
    scraper.save_content(conference_talks, "general_conference")
    
    # Combine all content
    all_content = bom_verses + dc_verses + conference_talks
    scraper.save_content(all_content, "all_lds_content")
    
    logger.info(f"=== Scraping Complete ===")
    logger.info(f"Total items: {len(all_content)}")

if __name__ == "__main__":
    main()