#!/usr/bin/env python3
"""
General Conference Scraper for GospelGuide
Scrapes General Conference talks from churchofjesuschrist.org

Usage:
    python scrape_general_conference.py [--start-year YEAR] [--end-year YEAR]
    
Examples:
    python scrape_general_conference.py                    # Scrape 2015-2025 (default)
    python scrape_general_conference.py --start-year 2020  # Scrape 2020-2025
    python scrape_general_conference.py --start-year 2010 --end-year 2019  # Custom range
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

class GeneralConferenceScraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def scrape_general_conference(self, start_year: int = 2015, end_year: int = 2025) -> List[Dict]:
        """Scrape General Conference talks"""
        content = []
        logger.info(f"Scraping General Conference talks ({start_year}-{end_year})...")
        
        for year in range(start_year, end_year + 1):
            for session in ["04", "10"]:  # April and October
                session_name = "April" if session == "04" else "October"
                logger.info(f"  Scraping {session_name} {year} Conference...")
                
                try:
                    # Get session page
                    session_url = f"{self.base_url}/study/general-conference/{year}/{session}?lang=eng"
                    response = self.session.get(session_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract talk links from session page
                    talk_links = self._extract_conference_talk_links(soup, year, session)
                    
                    # Scrape each talk
                    for talk_link in talk_links:
                        talk_content = self._scrape_conference_talk(talk_link, year, session_name)
                        if talk_content:
                            content.extend(talk_content)
                        
                        time.sleep(0.3)  # Rate limiting
                        
                except Exception as e:
                    logger.error(f"Error scraping {session_name} {year}: {e}")
                    
                time.sleep(1)  # Between sessions
                
        return content

    def _extract_conference_talk_links(self, soup: BeautifulSoup, year: int, session: str) -> List[str]:
        """Extract talk links from conference session page"""
        talk_links = []
        
        # Look for talk links in the page
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            
            # Conference talk URLs typically contain the pattern /general-conference/{year}/{session}/{talk-id}
            if href and f'/general-conference/{year}/{session}/' in href:
                # Exclude navigation links and other non-talk URLs
                if not any(skip in href for skip in [
                    '#', 'javascript', 'session?', 
                    'saturday-morning-session', 'saturday-afternoon-session', 'saturday-evening-session',
                    'sunday-morning-session', 'sunday-afternoon-session', 'priesthood-session'
                ]):
                    # Only include URLs that look like individual talks
                    # Individual talks end with either:
                    # - Number+name pattern like "19oaks" or "12stevenson" (2019+)
                    # - Descriptive title pattern like "the-heart-of-a-prophet" (2015-2018)
                    parts = href.split('/')
                    if len(parts) > 5 and parts[-1]:  # Has a talk identifier
                        talk_id = parts[-1].split('?')[0]  # Remove query parameters
                        # Check if it looks like a talk ID:
                        # - Starts with number followed by letters (2019+): "19oaks"
                        # - Contains hyphens and letters (2015-2018): "the-heart-of-a-prophet"
                        if re.match(r'^\d+[a-z]', talk_id) or re.match(r'^[a-z].*-.*[a-z]$', talk_id):
                            full_url = urljoin(self.base_url, href)
                            if full_url not in talk_links:
                                talk_links.append(full_url)
        
        # Remove duplicates and sort
        unique_links = list(set(talk_links))
        logger.info(f"    Found {len(unique_links)} talks for {session} {year}")
        return unique_links

    def _scrape_conference_talk(self, talk_url: str, year: int, session: str) -> List[Dict]:
        """Scrape individual conference talk"""
        content = []
        
        try:
            response = self.session.get(talk_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract talk metadata
            title = self._extract_talk_title(soup)
            speaker = self._extract_talk_speaker(soup)
            
            if not title or not speaker:
                logger.warning(f"Missing title or speaker for {talk_url}")
                return content
                
            # Extract talk content in paragraphs
            paragraphs = self._extract_talk_paragraphs(soup)
            
            # Create content chunks from paragraphs
            for i, paragraph in enumerate(paragraphs):
                if len(paragraph) > 50:  # Only substantial paragraphs
                    citation = f"({speaker}, \"{title}\", {session} {year}, ¶{i+1})"
                    
                    talk_data = {
                        "citation": citation,
                        "content": paragraph,
                        "source_type": "conference",
                        "speaker": speaker,
                        "title": title,
                        "year": year,
                        "session": session,
                        "paragraph": i + 1,
                        "url": talk_url,
                        "mode_tags": ["default", "general-conference-only", "scholar"],
                        "standard_work": "General Conference",
                        "word_count": len(paragraph.split()),
                        "id": f"gc-{year}-{session.lower()}-{self._slugify(speaker)}-{i+1}"
                    }
                    content.append(talk_data)
            
            logger.info(f"    {speaker}: \"{title}\" - {len(content)} paragraphs")
            
        except Exception as e:
            logger.error(f"Error scraping talk {talk_url}: {e}")
            
        return content

    def _extract_talk_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract talk title"""
        # Look for title in various possible locations (modern LDS.org structure)
        title_elem = (soup.find('h1') or 
                     soup.find('title') or
                     soup.find('meta', {'property': 'og:title'}))
        
        if title_elem:
            if title_elem.name == 'meta':
                title = title_elem.get('content', '').strip()
            else:
                title = title_elem.get_text().strip()
            
            # Clean up title (remove "By [Name]" suffix if present)
            if ' - ' in title:
                title = title.split(' - ')[0].strip()
            if title.startswith('By '):
                title = title[3:].strip()
                
            return title
        return None

    def _extract_talk_speaker(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract speaker name"""
        # Look for speaker information in modern structure
        speaker_elem = (soup.find('p', class_='author-name') or
                       soup.find('div', class_='author') or
                       soup.find('span', class_='author') or
                       soup.find('p', {'class': 'byline'}) or
                       soup.find('div', {'class': 'byline'}))
        
        if speaker_elem:
            speaker = speaker_elem.get_text().strip()
            # Clean up speaker name
            if speaker.startswith('By '):
                speaker = speaker[3:].strip()
            return speaker
        
        # Try to extract from subtitle or other elements  
        subtitle = soup.find('p', class_='subtitle')
        if subtitle:
            text = subtitle.get_text().strip()
            if text.startswith('By '):
                return text[3:].strip()
        
        # Look for "By [Name]" pattern in the page
        content = soup.get_text()
        by_match = re.search(r'By ([A-Z][a-zA-Z\s\.]+)', content)
        if by_match:
            return by_match.group(1).strip()
            
        return "Unknown Speaker"

    def _extract_talk_paragraphs(self, soup: BeautifulSoup) -> List[str]:
        """Extract talk content paragraphs"""
        paragraphs = []
        
        # Look for the main content area
        content_area = (soup.find('div', class_='body-block') or 
                       soup.find('main') or 
                       soup.find('article') or
                       soup.find('div', class_='content') or
                       soup)
        
        # Find all paragraph elements
        p_elements = content_area.find_all('p')
        
        for p in p_elements:
            text = p.get_text(strip=True)
            
            # Skip common non-content paragraphs
            if any(skip in text.lower() for skip in [
                'we value your privacy',
                'cookies', 'privacy notice',
                'feedback', 'employment',
                'social pages', 'church social',
                'all rights reserved',
                'note:', 'notes:'
            ]):
                continue
            
            # Clean up and filter paragraphs
            if len(text) > 50:  # Only substantial paragraphs
                cleaned_text = self._clean_text(text)
                if len(cleaned_text) > 30:
                    paragraphs.append(cleaned_text)
        
        # Also look for content in section headers (h2, h3) which often contain key quotes
        headers = content_area.find_all(['h2', 'h3'])
        for header in headers:
            header_text = header.get_text(strip=True)
            if len(header_text) > 20 and len(header_text) < 200:  # Reasonable header length
                cleaned_text = self._clean_text(header_text)
                if cleaned_text not in [p[:len(cleaned_text)] for p in paragraphs]:  # Avoid duplicates
                    paragraphs.append(cleaned_text)
        
        return paragraphs

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
    parser = argparse.ArgumentParser(description='Scrape General Conference talks')
    parser.add_argument('--start-year', type=int, default=2015, help='Start year (default: 2015)')
    parser.add_argument('--end-year', type=int, default=2025, help='End year (default: 2025)')
    parser.add_argument('--output', type=str, default='general_conference.json', help='Output filename')
    
    args = parser.parse_args()
    
    scraper = GeneralConferenceScraper()
    
    logger.info("=== Starting General Conference Scraping ===")
    logger.info(f"Years: {args.start_year}-{args.end_year}")
    
    content = scraper.scrape_general_conference(args.start_year, args.end_year)
    scraper.save_content(content, args.output)
    
    logger.info(f"=== General Conference Scraping Complete ===")
    logger.info(f"Total talks scraped: {len(content)} paragraphs")
    
    # Summary by year
    years = {}
    for item in content:
        year = item['year']
        years[year] = years.get(year, 0) + 1
    
    for year in sorted(years.keys()):
        logger.info(f"  {year}: {years[year]} paragraphs")

if __name__ == "__main__":
    main()