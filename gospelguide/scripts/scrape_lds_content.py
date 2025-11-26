#!/usr/bin/env python3
"""
Real LDS Content Scraper for GospelGuide
Scrapes actual verse content from churchofjesuschrist.org with proper citations

Usage:
    python scrape_lds_content.py
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import Dict, List, Optional
import os
import re
from urllib.parse import urljoin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LDSContentScraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Book of Mormon URL mappings based on LDS.org structure
        self.book_mappings = {
            "1 Nephi": "1-ne",
            "2 Nephi": "2-ne", 
            "Jacob": "jacob",
            "Enos": "enos",
            "Jarom": "jarom",
            "Omni": "omni",
            "Words of Mormon": "w-of-m",
            "Mosiah": "mosiah",
            "Alma": "alma",
            "Helaman": "hel",
            "3 Nephi": "3-ne",
            "4 Nephi": "4-ne",
            "Mormon": "morm",
            "Ether": "ether",
            "Moroni": "moro"
        }
        
        # Chapter counts for each book
        self.chapter_counts = {
            "1 Nephi": 22, "2 Nephi": 33, "Jacob": 7, "Enos": 1, "Jarom": 1,
            "Omni": 1, "Words of Mormon": 1, "Mosiah": 29, "Alma": 63,
            "Helaman": 16, "3 Nephi": 30, "4 Nephi": 1, "Mormon": 9,
            "Ether": 15, "Moroni": 10
        }

    def scrape_book_of_mormon(self, test_mode=True) -> List[Dict]:
        """Scrape Book of Mormon content with verse-level granularity"""
        content = []
        
        # In test mode, scrape just 1 Nephi chapters 1-3
        books_to_process = ["1 Nephi"] if test_mode else list(self.book_mappings.keys())
        
        for book_name in books_to_process:
            logger.info(f"Scraping {book_name}...")
            book_code = self.book_mappings[book_name]
            
            # Limit chapters in test mode
            max_chapters = 3 if test_mode else self.chapter_counts[book_name]
            
            for chapter_num in range(1, max_chapters + 1):
                chapter_url = f"{self.base_url}/study/scriptures/bofm/{book_code}/{chapter_num}"
                logger.info(f"  Scraping {book_name} {chapter_num}...")
                
                chapter_content = self._scrape_chapter(chapter_url, book_name, chapter_num)
                content.extend(chapter_content)
                
                time.sleep(0.5)  # Rate limiting
        
        return content

    def _scrape_chapter(self, chapter_url: str, book_name: str, chapter_num: int) -> List[Dict]:
        """Scrape individual chapter content with verse-level extraction"""
        content = []
        
        try:
            response = self.session.get(chapter_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Method 1: Look for paragraphs with verse content
            verses_found = self._extract_verses_method1(soup, book_name, chapter_num, chapter_url)
            
            if not verses_found:
                # Method 2: Alternative parsing if method 1 fails
                verses_found = self._extract_verses_method2(soup, book_name, chapter_num, chapter_url)
            
            content.extend(verses_found)
            
            if verses_found:
                logger.info(f"    Found {len(verses_found)} verses in {book_name} {chapter_num}")
            else:
                logger.warning(f"    No verses found in {book_name} {chapter_num}")
                
        except Exception as e:
            logger.error(f"Error scraping {chapter_url}: {e}")
            
        return content

    def _extract_verses_method1(self, soup: BeautifulSoup, book_name: str, chapter_num: int, url: str) -> List[Dict]:
        """Primary method: Extract verses from paragraph elements"""
        verses = []
        
        # Look for the main content area
        content_area = soup.find('div', class_='body-block') or soup.find('main') or soup
        
        # Find all paragraphs that might contain verses
        paragraphs = content_area.find_all('p')
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            
            # Skip empty paragraphs or very short ones
            if len(text) < 20:
                continue
            
            # Look for verse pattern: number followed by content
            verse_match = re.match(r'^\s*(\d+)\s+(.+)', text, re.DOTALL)
            
            if verse_match:
                verse_num = int(verse_match.group(1))
                verse_text = verse_match.group(2).strip()
                
                # Clean up the verse text
                verse_text = self._clean_verse_text(verse_text)
                
                if len(verse_text) > 10:  # Only include substantial verses
                    verse_data = self._create_verse_data(
                        book_name, chapter_num, verse_num, verse_text, url
                    )
                    verses.append(verse_data)
        
        return verses

    def _extract_verses_method2(self, soup: BeautifulSoup, book_name: str, chapter_num: int, url: str) -> List[Dict]:
        """Alternative method: Extract from full text with regex"""
        verses = []
        
        # Get all text from the main content
        content_area = soup.find('div', class_='body-block') or soup.find('main') or soup
        full_text = content_area.get_text()
        
        # Split by verse numbers and extract content
        verse_pattern = r'\n\s*(\d+)\s+([^\n]+(?:\n(?!\s*\d+\s)[^\n]*)*)'
        
        for match in re.finditer(verse_pattern, full_text):
            verse_num = int(match.group(1))
            verse_text = match.group(2).strip()
            
            # Clean up verse text
            verse_text = self._clean_verse_text(verse_text)
            verse_text = re.sub(r'\s+', ' ', verse_text)  # Normalize whitespace
            
            if len(verse_text) > 10:
                verse_data = self._create_verse_data(
                    book_name, chapter_num, verse_num, verse_text, url
                )
                verses.append(verse_data)
        
        return verses

    def _clean_verse_text(self, text: str) -> str:
        """Clean and normalize verse text"""
        # Remove footnote markers that appear before words (like 'aborn', 'bgoodly')
        text = re.sub(r'\b[a-z](?=[A-Z][a-z])', '', text)
        
        # Remove standalone footnote markers (single letters)
        text = re.sub(r'\s+[a-z]\s+', ' ', text)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Clean up any remaining artifacts
        text = text.strip()
        
        return text

    def _create_verse_data(self, book_name: str, chapter_num: int, verse_num: int, verse_text: str, url: str) -> Dict:
        """Create standardized verse data structure"""
        citation = f"({book_name} {chapter_num}:{verse_num})"
        
        return {
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

    def scrape_doctrine_and_covenants(self, test_mode=True) -> List[Dict]:
        """Scrape Doctrine and Covenants sections"""
        content = []
        
        # In test mode, scrape just sections 1-3
        max_sections = 3 if test_mode else 138
        
        for section_num in range(1, max_sections + 1):
            logger.info(f"Scraping D&C Section {section_num}...")
            
            section_url = f"{self.base_url}/study/scriptures/dc-testament/dc/{section_num}"
            section_content = self._scrape_dc_section(section_url, section_num)
            content.extend(section_content)
            
            time.sleep(0.5)
        
        return content

    def _scrape_dc_section(self, section_url: str, section_num: int) -> List[Dict]:
        """Scrape individual D&C section"""
        content = []
        
        try:
            response = self.session.get(section_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract verses using similar methods as Book of Mormon
            verses_found = self._extract_dc_verses(soup, section_num, section_url)
            content.extend(verses_found)
            
            if verses_found:
                logger.info(f"    Found {len(verses_found)} verses in D&C {section_num}")
                
        except Exception as e:
            logger.error(f"Error scraping D&C {section_num}: {e}")
            
        return content

    def _extract_dc_verses(self, soup: BeautifulSoup, section_num: int, url: str) -> List[Dict]:
        """Extract verses from D&C section"""
        verses = []
        
        content_area = soup.find('div', class_='body-block') or soup.find('main') or soup
        paragraphs = content_area.find_all('p')
        
        for p in paragraphs:
            text = p.get_text(strip=True)
            
            if len(text) < 20:
                continue
            
            # D&C verse pattern
            verse_match = re.match(r'^\s*(\d+)\s+(.+)', text, re.DOTALL)
            
            if verse_match:
                verse_num = int(verse_match.group(1))
                verse_text = verse_match.group(2).strip()
                verse_text = self._clean_verse_text(verse_text)
                
                if len(verse_text) > 10:
                    citation = f"(D&C {section_num}:{verse_num})"
                    
                    verse_data = {
                        "citation": citation,
                        "content": verse_text,
                        "source_type": "scripture",
                        "book": "Doctrine and Covenants",
                        "section": section_num,
                        "verse": verse_num,
                        "url": url,
                        "mode_tags": ["default", "scholar"],
                        "standard_work": "Doctrine and Covenants",
                        "word_count": len(verse_text.split()),
                        "id": f"dc-{section_num}-{verse_num}"
                    }
                    verses.append(verse_data)
        
        return verses

    def save_content(self, content: List[Dict], filename: str):
        """Save scraped content to JSON file"""
        os.makedirs("content", exist_ok=True)
        filepath = os.path.join("content", filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Saved {len(content)} items to {filepath}")
        
        # Print sample for verification
        if content:
            logger.info("Sample scraped content:")
            for i, item in enumerate(content[:3]):
                logger.info(f"  {i+1}. {item['citation']}: {item['content'][:100]}...")

def main():
    """Main scraping function"""
    scraper = LDSContentScraper()
    
    logger.info("=== Starting LDS Content Scraping ===")
    
    # Scrape entire Book of Mormon
    logger.info("Scraping entire Book of Mormon...")
    bom_content = scraper.scrape_book_of_mormon(test_mode=False)
    scraper.save_content(bom_content, "real_book_of_mormon.json")
    
    # Scrape D&C (test mode - first 3 sections)
    logger.info("Scraping Doctrine and Covenants...")
    dc_content = scraper.scrape_doctrine_and_covenants(test_mode=True)
    scraper.save_content(dc_content, "real_doctrine_covenants.json")
    
    # Combine all content
    all_content = bom_content + dc_content
    scraper.save_content(all_content, "real_lds_scriptures.json")
    
    logger.info(f"=== Scraping Complete ===")
    logger.info(f"Total verses scraped: {len(all_content)}")
    
    # Print statistics
    bom_count = len([item for item in all_content if item['standard_work'] == 'Book of Mormon'])
    dc_count = len([item for item in all_content if item['standard_work'] == 'Doctrine and Covenants'])
    
    logger.info(f"Book of Mormon verses: {bom_count}")
    logger.info(f"D&C verses: {dc_count}")

if __name__ == "__main__":
    main()