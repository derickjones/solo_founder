#!/usr/bin/env python3
"""
Study Helps Scraper for GospelGuide
Scrapes Study Helps (Bible Dictionary, Guide to Scriptures, Topical Guide) from churchofjesuschrist.org

Usage:
    python scrape_study_helps.py [--limit LIMIT]
    
Examples:
    python scrape_study_helps.py              # Scrape all study helps
    python scrape_study_helps.py --limit 100  # Limit to 100 entries for testing
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
import argparse

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class StudyHelpsScraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def scrape_study_helps(self, limit: Optional[int] = None) -> List[Dict]:
        """Scrape all Study Helps content"""
        content = []
        logger.info("Scraping Study Helps...")
        
        # Study helps sources
        study_helps = [
            {
                "name": "Bible Dictionary",
                "code": "bd",
                "url": f"{self.base_url}/study/scriptures/bd?lang=eng",
                "type": "bible-dictionary"
            },
            {
                "name": "Guide to the Scriptures",
                "code": "gs", 
                "url": f"{self.base_url}/study/scriptures/gs?lang=eng",
                "type": "guide-to-scriptures"
            },
            {
                "name": "Topical Guide",
                "code": "tg",
                "url": f"{self.base_url}/study/scriptures/tg?lang=eng", 
                "type": "topical-guide"
            }
        ]
        
        for help_source in study_helps:
            logger.info(f"  Scraping {help_source['name']}...")
            help_content = self._scrape_study_help_source(help_source, limit)
            content.extend(help_content)
            
        return content

    def _scrape_study_help_source(self, source: Dict, limit: Optional[int] = None) -> List[Dict]:
        """Scrape a specific study help source"""
        content = []
        
        try:
            response = self.session.get(source["url"])
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find entry links
            entry_links = self._extract_entry_links(soup, source)
            
            if limit:
                entry_links = entry_links[:limit]
                
            logger.info(f"    Found {len(entry_links)} entries")
            
            for link in entry_links:
                entry_content = self._scrape_study_help_entry(link, source)
                if entry_content:
                    content.extend(entry_content)
                    
                time.sleep(0.2)  # Rate limiting
                
        except Exception as e:
            logger.error(f"Error scraping {source['name']}: {e}")
            
        return content

    def _extract_entry_links(self, soup: BeautifulSoup, source: Dict) -> List[str]:
        """Extract entry links from study help index page"""
        links = []
        
        # Look for entry links - these are individual entries within the study helps
        link_elements = soup.find_all('a', href=True)
        
        for link in link_elements:
            href = link.get('href')
            
            # Study help entry URLs contain the source code and specific entries
            if href and f'/scriptures/{source["code"]}/' in href:
                # Skip navigation links, introduction pages, and other non-entry links
                if not any(skip in href for skip in [
                    '#', 'javascript', 'introduction', 'next', 'prev'
                ]):
                    # Make sure it's an actual entry (has specific entry identifier after the source code)
                    path_parts = href.strip('/').split('/')
                    if len(path_parts) >= 4 and path_parts[-1]:  # /study/scriptures/bd/aaron?lang=eng
                        # Remove the query parameters for processing
                        clean_path = href.split('?')[0] if '?' in href else href
                        if clean_path.strip('/').split('/')[-1]:  # Make sure there's an entry name
                            full_url = urljoin(self.base_url, clean_path)
                            if full_url not in links:
                                links.append(full_url)
        
        return links

    def _scrape_study_help_entry(self, entry_url: str, source: Dict) -> List[Dict]:
        """Scrape individual study help entry"""
        content = []
        
        try:
            response = self.session.get(entry_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract entry metadata
            title = self._extract_entry_title(soup)
            entry_text = self._extract_entry_content(soup)
            
            if not title or not entry_text:
                return content
            
            # Create content entry
            citation = f"({source['name']}: {title})"
            
            entry_data = {
                "citation": citation,
                "content": entry_text,
                "source_type": "study-help",
                "study_help_type": source["type"],
                "study_help_name": source["name"],
                "title": title,
                "url": entry_url,
                "mode_tags": ["default", "scholar", "study-mode"],
                "standard_work": "Study Helps",
                "word_count": len(entry_text.split()),
                "id": f"sh-{source['code']}-{self._slugify(title)}"
            }
            
            content.append(entry_data)
            
            if len(content) % 50 == 0:
                logger.info(f"    Scraped {len(content)} entries...")
            
        except Exception as e:
            logger.error(f"Error scraping entry {entry_url}: {e}")
            
        return content

    def _extract_entry_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract entry title"""
        title_elem = (soup.find('h1') or 
                     soup.find('title') or
                     soup.find('meta', {'property': 'og:title'}))
        
        if title_elem:
            if title_elem.name == 'meta':
                title = title_elem.get('content', '').strip()
            else:
                title = title_elem.get_text().strip()
                
            # Clean up title
            if title.startswith('Study Help: '):
                title = title[12:].strip()
                
            return title
        return None

    def _extract_entry_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract entry content"""
        content_area = (soup.find('div', class_='body-block') or 
                       soup.find('main') or 
                       soup.find('article') or
                       soup.find('div', class_='content') or
                       soup)
        
        # Collect all text content
        paragraphs = []
        
        # Get paragraphs
        p_elements = content_area.find_all('p')
        for p in p_elements:
            text = p.get_text(strip=True)
            if len(text) > 20:  # Filter out very short paragraphs
                paragraphs.append(text)
        
        # Get list items if present
        li_elements = content_area.find_all('li')
        for li in li_elements:
            text = li.get_text(strip=True)
            if len(text) > 20:
                paragraphs.append(text)
        
        if paragraphs:
            full_content = ' '.join(paragraphs)
            return self._clean_text(full_content)
        
        return None

    def _clean_text(self, text: str) -> str:
        """Clean and normalize text content"""
        # Remove extra whitespace and normalize
        text = ' '.join(text.split())
        
        # Remove unwanted characters
        text = text.replace('\u00a0', ' ')  # Non-breaking space
        text = text.replace('\u2019', "'")  # Smart apostrophe
        text = text.replace('\u201c', '"')  # Smart quote
        text = text.replace('\u201d', '"')  # Smart quote
        
        return text.strip()

    def _slugify(self, text: str) -> str:
        """Convert text to URL-safe slug"""
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')

    def save_content(self, content: List[Dict], filename: str) -> None:
        """Save scraped content to JSON file"""
        content_dir = "content"
        if not os.path.exists(content_dir):
            os.makedirs(content_dir)
        
        filepath = os.path.join(content_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=2)
        
        logger.info(f"Saved {len(content)} items to {filepath}")

def main():
    parser = argparse.ArgumentParser(description='Scrape Study Helps content')
    parser.add_argument('--limit', type=int, help='Limit number of entries per source (for testing)')
    parser.add_argument('--output', type=str, default='study_helps.json', help='Output filename')
    
    args = parser.parse_args()
    
    scraper = StudyHelpsScraper()
    
    logger.info("=== Starting Study Helps Scraping ===")
    if args.limit:
        logger.info(f"Limit: {args.limit} entries per source")
    
    content = scraper.scrape_study_helps(args.limit)
    scraper.save_content(content, args.output)
    
    logger.info(f"=== Study Helps Scraping Complete ===")
    logger.info(f"Total entries scraped: {len(content)}")
    
    # Summary by type
    types = {}
    for item in content:
        help_type = item['study_help_type']
        types[help_type] = types.get(help_type, 0) + 1
    
    for help_type in sorted(types.keys()):
        logger.info(f"  {help_type}: {types[help_type]} entries")

if __name__ == "__main__":
    main()