#!/usr/bin/env python3
"""
Doctrine and Covenants Scraper for GospelGuide
Scrapes all D&C content from churchofjesuschrist.org

Usage:
    python scrape_doctrine_covenants.py [--limit N] [--output filename.json]
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

class DoctrineCovenantsScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        self.base_url = "https://www.churchofjesuschrist.org"

    def scrape_doctrine_and_covenants(self, limit: Optional[int] = None) -> List[Dict]:
        """Scrape all D&C sections"""
        content = []
        logger.info("Scraping Doctrine and Covenants...")
        
        verse_count = 0
        
        # All 138 sections plus Official Declarations
        for section_num in range(1, 139):
            if limit and verse_count >= limit:
                logger.info(f"Reached limit of {limit} verses")
                break
                
            logger.info(f"  Scraping D&C Section {section_num}...")
            
            section_url = f"{self.base_url}/study/scriptures/dc-testament/dc/{section_num}?lang=eng"
            
            try:
                response = self.session.get(section_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                verses = self._extract_dc_verses(soup, section_num, section_url)
                content.extend(verses)
                verse_count += len(verses)
                
                if verses:
                    logger.info(f"    D&C {section_num}: {len(verses)} verses")
                
                time.sleep(0.3)
                
            except Exception as e:
                logger.error(f"Error scraping D&C {section_num}: {e}")
        
        # Add Official Declarations if not at limit
        for od_num in [1, 2]:
            if limit and verse_count >= limit:
                break
                
            logger.info(f"  Scraping Official Declaration {od_num}...")
            od_url = f"{self.base_url}/study/scriptures/dc-testament/od/{od_num}?lang=eng"
            
            try:
                response = self.session.get(od_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Official Declarations are handled as single content blocks
                od_content = self._extract_official_declaration(soup, od_num, od_url)
                if od_content:
                    content.append(od_content)
                    verse_count += 1
                    logger.info(f"    Official Declaration {od_num}: Added")
                    
            except Exception as e:
                logger.error(f"Error scraping Official Declaration {od_num}: {e}")
                
        return content

    def _extract_dc_verses(self, soup: BeautifulSoup, section_num: int, url: str) -> List[Dict]:
        """Extract verses from D&C section using modern LDS.org structure"""
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

    def _extract_official_declaration(self, soup: BeautifulSoup, od_num: int, url: str) -> Optional[Dict]:
        """Extract Official Declaration content"""
        content_area = soup.find('div', class_='body-block') or soup.find('main') or soup
        full_text = content_area.get_text(strip=True)
        
        if len(full_text) > 50:
            cleaned_text = self._clean_verse_text(full_text)
            citation = f"(Official Declaration {od_num})"
            
            return {
                "citation": citation,
                "content": cleaned_text,
                "source_type": "scripture",
                "book": "Doctrine and Covenants",
                "section": f"Official Declaration {od_num}",
                "url": url,
                "mode_tags": ["default", "scholar"],
                "standard_work": "Doctrine and Covenants",
                "word_count": len(cleaned_text.split()),
                "id": f"dc-od-{od_num}"
            }
        return None

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
    parser = argparse.ArgumentParser(description='Scrape Doctrine and Covenants content')
    parser.add_argument('--limit', type=int, help='Limit number of verses to scrape')
    parser.add_argument('--output', default='doctrine_covenants.json', help='Output filename')
    parser.add_argument('--test', action='store_true', help='Test mode - scrape only first 10 sections')
    
    args = parser.parse_args()
    
    logger.info("=== Starting Doctrine and Covenants Scraping ===")
    logger.info(f"Limit: {args.limit or 'No limit'}")
    
    scraper = DoctrineCovenantsScraper()
    
    # Test mode limits to first 10 sections
    if args.test:
        logger.info("Test mode: scraping first 10 sections")
        content = scraper.scrape_doctrine_and_covenants(limit=200)  # Reasonable test limit
    else:
        content = scraper.scrape_doctrine_and_covenants(limit=args.limit)
    
    scraper.save_content(content, args.output)
    
    logger.info("=== Doctrine and Covenants Scraping Complete ===")
    logger.info(f"Total items scraped: {len(content)}")

if __name__ == "__main__":
    main()