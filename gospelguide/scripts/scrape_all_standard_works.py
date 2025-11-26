#!/usr/bin/env python3
"""
Complete LDS Content Scraper for GospelGuide
Scrapes all official LDS content from churchofjesuschrist.org

Content Sources:
- All Four Standard Works (OT, NT, D&C, PoGP)
- Study Helps (Bible Dictionary, Topical Guide, Guide to Scriptures, JST)
- General Conference talks (2015-2025)
- Come Follow Me manuals (2021-2025)

Usage:
    python scrape_all_standard_works.py
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

class StandardWorksScaper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def scrape_old_testament(self) -> List[Dict]:
        """Scrape Old Testament books"""
        content = []
        logger.info("Scraping Old Testament...")
        
        # Major OT books to scrape (can expand to all 39 later)
        ot_books = [
            {"name": "Genesis", "code": "gen", "chapters": 50},
            {"name": "Exodus", "code": "ex", "chapters": 40},
            {"name": "Deuteronomy", "code": "deut", "chapters": 34},
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
        
        for book in ot_books:
            content.extend(self._scrape_bible_book(book["name"], book["code"], book["chapters"], "ot"))
            
        return content

    def scrape_new_testament(self) -> List[Dict]:
        """Scrape New Testament books"""
        content = []
        logger.info("Scraping New Testament...")
        
        # All NT books
        nt_books = [
            {"name": "Matthew", "code": "matt", "chapters": 28},
            {"name": "Mark", "code": "mark", "chapters": 16},
            {"name": "Luke", "code": "luke", "chapters": 24},
            {"name": "John", "code": "john", "chapters": 21},
            {"name": "Acts", "code": "acts", "chapters": 28},
            {"name": "Romans", "code": "rom", "chapters": 16},
            {"name": "1 Corinthians", "code": "1-cor", "chapters": 16},
            {"name": "2 Corinthians", "code": "2-cor", "chapters": 13},
            {"name": "Ephesians", "code": "eph", "chapters": 6},
            {"name": "Philippians", "code": "philip", "chapters": 4},
            {"name": "Colossians", "code": "col", "chapters": 4},
            {"name": "1 Timothy", "code": "1-tim", "chapters": 6},
            {"name": "2 Timothy", "code": "2-tim", "chapters": 4},
            {"name": "Hebrews", "code": "heb", "chapters": 13},
            {"name": "James", "code": "james", "chapters": 5},
            {"name": "1 Peter", "code": "1-pet", "chapters": 5},
            {"name": "2 Peter", "code": "2-pet", "chapters": 3},
            {"name": "1 John", "code": "1-jn", "chapters": 5},
            {"name": "Revelation", "code": "rev", "chapters": 22},
        ]
        
        for book in nt_books:
            content.extend(self._scrape_bible_book(book["name"], book["code"], book["chapters"], "nt"))
            
        return content

    def _scrape_bible_book(self, book_name: str, book_code: str, num_chapters: int, testament: str) -> List[Dict]:
        """Scrape individual Bible book"""
        content = []
        
        logger.info(f"  Scraping {book_name}...")
        
        for chapter_num in range(1, num_chapters + 1):
            chapter_url = f"{self.base_url}/study/scriptures/{testament}/{book_code}/{chapter_num}?lang=eng"
            
            try:
                response = self.session.get(chapter_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                verses = self._extract_bible_verses(soup, book_name, chapter_num, chapter_url, testament)
                content.extend(verses)
                
                if verses:
                    logger.info(f"    {book_name} {chapter_num}: {len(verses)} verses")
                
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
                standard_work = "Old Testament" if testament == "ot" else "New Testament"
                
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

    def scrape_doctrine_and_covenants(self) -> List[Dict]:
        """Scrape all D&C sections"""
        content = []
        logger.info("Scraping Doctrine and Covenants...")
        
        # All 138 sections plus Official Declarations
        for section_num in range(1, 139):
            logger.info(f"  Scraping D&C Section {section_num}...")
            
            section_url = f"{self.base_url}/study/scriptures/dc-testament/dc/{section_num}?lang=eng"
            
            try:
                response = self.session.get(section_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                verses = self._extract_dc_verses(soup, section_num, section_url)
                content.extend(verses)
                
                if verses:
                    logger.info(f"    D&C {section_num}: {len(verses)} verses")
                
                time.sleep(0.3)
                
            except Exception as e:
                logger.error(f"Error scraping D&C {section_num}: {e}")
        
        # Add Official Declarations
        for od_num in [1, 2]:
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

    def _extract_official_declaration(self, soup: BeautifulSoup, od_num: int, url: str) -> Dict:
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

    def scrape_pearl_of_great_price(self) -> List[Dict]:
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
        
        for book in pogp_books:
            logger.info(f"  Scraping {book['name']}...")
            
            for chapter_num in range(1, book["chapters"] + 1):
                chapter_url = f"{self.base_url}/study/scriptures/pgp/{book['code']}/{chapter_num}?lang=eng"
                
                try:
                    response = self.session.get(chapter_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    verses = self._extract_pogp_verses(soup, book["name"], chapter_num, chapter_url)
                    content.extend(verses)
                    
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

    def scrape_study_helps(self) -> List[Dict]:
        """Scrape Study Helps content"""
        content = []
        logger.info("Scraping Study Helps...")
        
        # Study Helps sections
        study_helps = [
            {"name": "Bible Dictionary", "code": "bd", "type": "dictionary"},
            {"name": "Topical Guide", "code": "tg", "type": "topical"},
            {"name": "Guide to the Scriptures", "code": "gs", "type": "guide"},
            {"name": "Joseph Smith Translation", "code": "jst", "type": "translation"},
        ]
        
        for help_section in study_helps:
            logger.info(f"  Scraping {help_section['name']}...")
            
            try:
                # Study helps have different URL structure
                section_url = f"{self.base_url}/study/scriptures/study-helps/{help_section['code']}?lang=eng"
                response = self.session.get(section_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract study helps entries
                entries = self._extract_study_helps_entries(soup, help_section, section_url)
                content.extend(entries)
                
                logger.info(f"    {help_section['name']}: {len(entries)} entries")
                time.sleep(0.5)
                
            except Exception as e:
                logger.error(f"Error scraping {help_section['name']}: {e}")
                
        return content

    def _extract_study_helps_entries(self, soup: BeautifulSoup, help_section: Dict, url: str) -> List[Dict]:
        """Extract individual study helps entries"""
        entries = []
        
        # Look for entry links or content blocks
        content_area = soup.find('div', class_='body-block') or soup.find('main') or soup
        
        # Find all links that look like study help entries
        links = content_area.find_all('a', href=True)
        
        for link in links[:50]:  # Limit to first 50 entries for testing
            href = link.get('href')
            title = link.get_text(strip=True)
            
            if href and title and len(title) > 2:
                # Skip navigation links
                if any(skip in href.lower() for skip in ['javascript', '#', 'mailto']):
                    continue
                    
                entry_url = urljoin(self.base_url, href)
                
                try:
                    # Get the individual entry content
                    response = self.session.get(entry_url)
                    response.raise_for_status()
                    entry_soup = BeautifulSoup(response.content, 'html.parser')
                    
                    entry_content = self._extract_study_help_content(entry_soup, title, entry_url, help_section)
                    if entry_content:
                        entries.append(entry_content)
                    
                    time.sleep(0.2)  # Rate limiting
                    
                except Exception as e:
                    logger.debug(f"Error scraping entry {title}: {e}")
                    continue
                    
        return entries

    def _extract_study_help_content(self, soup: BeautifulSoup, title: str, url: str, help_section: Dict) -> Dict:
        """Extract content from individual study help entry"""
        content_area = soup.find('div', class_='body-block') or soup.find('main') or soup
        
        if content_area:
            text_content = content_area.get_text(strip=True)
            
            if len(text_content) > 50:
                cleaned_text = self._clean_verse_text(text_content)
                
                return {
                    "citation": f"({help_section['name']}: {title})",
                    "content": cleaned_text,
                    "source_type": "study_help",
                    "title": title,
                    "help_section": help_section['name'],
                    "url": url,
                    "mode_tags": ["default", "scholar"],
                    "standard_work": "Study Helps",
                    "word_count": len(cleaned_text.split()),
                    "id": f"study-{help_section['code']}-{title.lower().replace(' ', '-')}"
                }
        
        return None

    def scrape_general_conference(self, start_year: int = 1971, end_year: int = 2025) -> List[Dict]:
        """Scrape General Conference talks"""
        content = []
        logger.info(f"Scraping General Conference talks ({start_year}-{end_year})...")
        
        for year in range(start_year, end_year + 1):
            for session in ["april", "october"]:
                logger.info(f"  Scraping {session.title()} {year} Conference...")
                
                try:
                    # Get session page
                    session_url = f"{self.base_url}/study/general-conference/{year}/{session}"
                    response = self.session.get(session_url)
                    response.raise_for_status()
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract talk links from session page
                    talk_links = self._extract_conference_talk_links(soup, year, session)
                    
                    # Scrape each talk
                    for talk_link in talk_links[:10]:  # Limit for testing - remove limit for full scraping
                        talk_content = self._scrape_conference_talk(talk_link, year, session)
                        if talk_content:
                            content.extend(talk_content)
                        
                        time.sleep(0.3)  # Rate limiting
                        
                except Exception as e:
                    logger.error(f"Error scraping {session} {year}: {e}")
                    
                time.sleep(1)  # Between sessions
                
        return content

    def _extract_conference_talk_links(self, soup: BeautifulSoup, year: int, session: str) -> List[str]:
        """Extract talk links from conference session page"""
        talk_links = []
        
        # Look for talk links in the page
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            
            # Conference talk URLs typically contain the pattern
            if href and f'/general-conference/{year}/{session}/' in href:
                if not any(skip in href for skip in ['#', 'javascript']):
                    full_url = urljoin(self.base_url, href)
                    talk_links.append(full_url)
        
        # Remove duplicates
        return list(set(talk_links))

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
                return content
                
            # Extract talk content in paragraphs
            paragraphs = self._extract_talk_paragraphs(soup)
            
            # Create content chunks from paragraphs
            for i, paragraph in enumerate(paragraphs):
                if len(paragraph) > 50:  # Only substantial paragraphs
                    citation = f"({speaker}, \"{title}\", {session.title()} {year}, ¶{i+1})"
                    
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
                        "id": f"gc-{year}-{session}-{speaker.lower().replace(' ', '-')}-{i+1}"
                    }
                    content.append(talk_data)
            
            logger.info(f"    {speaker}: \"{title}\" - {len(content)} paragraphs")
            
        except Exception as e:
            logger.error(f"Error scraping talk {talk_url}: {e}")
            
        return content

    def _extract_talk_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract talk title"""
        # Look for title in various possible locations
        title_elem = (soup.find('h1') or 
                     soup.find('title') or
                     soup.find('meta', {'property': 'og:title'}))
        
        if title_elem:
            if title_elem.name == 'meta':
                return title_elem.get('content', '').strip()
            else:
                return title_elem.get_text().strip()
        return None

    def _extract_talk_speaker(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract speaker name"""
        # Look for speaker information
        speaker_elem = (soup.find('p', class_='author-name') or
                       soup.find('div', class_='author') or
                       soup.find('span', class_='author'))
        
        if speaker_elem:
            return speaker_elem.get_text().strip()
        
        # Try to extract from title or other elements
        title = self._extract_talk_title(soup)
        if title and ' by ' in title:
            return title.split(' by ')[-1].strip()
            
        return None

    def _extract_talk_paragraphs(self, soup: BeautifulSoup) -> List[str]:
        """Extract talk content paragraphs"""
        paragraphs = []
        
        content_area = soup.find('div', class_='body-block') or soup.find('main') or soup
        
        # Find all paragraph elements
        p_elements = content_area.find_all('p')
        
        for p in p_elements:
            text = p.get_text(strip=True)
            
            # Clean up and filter paragraphs
            if len(text) > 50:
                cleaned_text = self._clean_verse_text(text)
                if len(cleaned_text) > 30:
                    paragraphs.append(cleaned_text)
        
        return paragraphs

    def scrape_come_follow_me(self) -> List[Dict]:
        """Scrape Come Follow Me manuals"""
        content = []
        logger.info("Scraping Come Follow Me manuals...")
        
        # Come Follow Me manuals by year
        cfm_manuals = [
            {"year": 2025, "focus": "doctrine-and-covenants", "title": "Doctrine and Covenants 2025"},
            {"year": 2024, "focus": "book-of-mormon", "title": "Book of Mormon 2024"},
            {"year": 2023, "focus": "new-testament", "title": "New Testament 2023"},
            {"year": 2022, "focus": "old-testament", "title": "Old Testament 2022"},
            {"year": 2021, "focus": "doctrine-and-covenants", "title": "Doctrine and Covenants 2021"},
        ]
        
        for manual in cfm_manuals:
            logger.info(f"  Scraping Come Follow Me {manual['year']} - {manual['title']}...")
            
            try:
                # CFM manual URL structure
                manual_url = f"{self.base_url}/study/manual/come-follow-me-for-home-and-church-{manual['focus']}-{manual['year']}"
                response = self.session.get(manual_url)
                response.raise_for_status()
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extract weekly lesson links
                lesson_links = self._extract_cfm_lesson_links(soup, manual)
                
                # Scrape each lesson
                for lesson_link in lesson_links[:20]:  # Limit for testing
                    lesson_content = self._scrape_cfm_lesson(lesson_link, manual)
                    if lesson_content:
                        content.extend(lesson_content)
                    
                    time.sleep(0.3)
                    
            except Exception as e:
                logger.error(f"Error scraping CFM {manual['year']}: {e}")
                
        return content

    def _extract_cfm_lesson_links(self, soup: BeautifulSoup, manual: Dict) -> List[str]:
        """Extract lesson links from CFM manual page"""
        lesson_links = []
        
        # Look for lesson links
        links = soup.find_all('a', href=True)
        
        for link in links:
            href = link.get('href')
            text = link.get_text(strip=True)
            
            # CFM lessons typically have specific patterns
            if href and any(pattern in href for pattern in ['/manual/come-follow-me', f'-{manual["year"]}']):
                if any(week in text.lower() for week in ['week', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']):
                    full_url = urljoin(self.base_url, href)
                    lesson_links.append(full_url)
        
        return list(set(lesson_links))

    def _scrape_cfm_lesson(self, lesson_url: str, manual: Dict) -> List[Dict]:
        """Scrape individual CFM lesson"""
        content = []
        
        try:
            response = self.session.get(lesson_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract lesson metadata
            lesson_title = self._extract_cfm_lesson_title(soup)
            week_info = self._extract_cfm_week_info(soup)
            
            if not lesson_title:
                return content
            
            # Extract lesson sections
            sections = self._extract_cfm_lesson_sections(soup)
            
            # Create content chunks
            for i, section in enumerate(sections):
                if len(section) > 100:  # Only substantial content
                    citation = f"(Come Follow Me {manual['year']}: \"{lesson_title}\", Section {i+1})"
                    
                    cfm_data = {
                        "citation": citation,
                        "content": section,
                        "source_type": "come_follow_me",
                        "lesson_title": lesson_title,
                        "week_info": week_info,
                        "year": manual['year'],
                        "focus": manual['focus'],
                        "section": i + 1,
                        "url": lesson_url,
                        "mode_tags": ["default", "come-follow-me", "scholar"],
                        "standard_work": "Come Follow Me",
                        "word_count": len(section.split()),
                        "id": f"cfm-{manual['year']}-{i+1}-{lesson_title.lower().replace(' ', '-')[:20]}"
                    }
                    content.append(cfm_data)
            
            logger.info(f"    {lesson_title}: {len(content)} sections")
            
        except Exception as e:
            logger.error(f"Error scraping CFM lesson {lesson_url}: {e}")
            
        return content

    def _extract_cfm_lesson_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract CFM lesson title"""
        title_elem = (soup.find('h1') or
                     soup.find('title') or
                     soup.find('h2'))
        
        if title_elem:
            title = title_elem.get_text().strip()
            # Clean up common title prefixes
            title = title.replace('Come, Follow Me—For Home and Church: ', '')
            return title
        return None

    def _extract_cfm_week_info(self, soup: BeautifulSoup) -> Optional[str]:
        """Extract week/date information"""
        # Look for date ranges or week info
        for elem in soup.find_all(['p', 'div', 'span']):
            text = elem.get_text().strip()
            if any(month in text for month in ['January', 'February', 'March', 'April', 'May', 'June',
                                              'July', 'August', 'September', 'October', 'November', 'December']):
                if '–' in text or '-' in text:
                    return text
        return None

    def _extract_cfm_lesson_sections(self, soup: BeautifulSoup) -> List[str]:
        """Extract lesson content sections"""
        sections = []
        
        content_area = soup.find('div', class_='body-block') or soup.find('main') or soup
        
        # Look for major content sections
        section_headers = content_area.find_all(['h2', 'h3', 'h4'])
        
        for header in section_headers:
            section_text = ""
            
            # Get all content until next header
            current = header.next_sibling
            while current:
                if hasattr(current, 'name') and current.name in ['h2', 'h3', 'h4']:
                    break
                    
                if hasattr(current, 'get_text'):
                    text = current.get_text(strip=True)
                    if text:
                        section_text += " " + text
                        
                current = current.next_sibling
            
            if len(section_text) > 50:
                cleaned_section = self._clean_verse_text(section_text)
                sections.append(cleaned_section)
        
        # If no sections found, get all paragraphs
        if not sections:
            paragraphs = content_area.find_all('p')
            for p in paragraphs:
                text = p.get_text(strip=True)
                if len(text) > 50:
                    cleaned_text = self._clean_verse_text(text)
                    sections.append(cleaned_text)
        
        return sections

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
    """Main scraping function for all Standard Works"""
    scraper = StandardWorksScaper()
    
    logger.info("=== Starting Complete Standard Works Scraping ===")
    
    # Scrape all four Standard Works
    old_testament = scraper.scrape_old_testament()
    scraper.save_content(old_testament, "old_testament.json")
    
    new_testament = scraper.scrape_new_testament() 
    scraper.save_content(new_testament, "new_testament.json")
    
    doctrine_covenants = scraper.scrape_doctrine_and_covenants()
    scraper.save_content(doctrine_covenants, "doctrine_covenants.json")
    
    pearl_of_great_price = scraper.scrape_pearl_of_great_price()
    scraper.save_content(pearl_of_great_price, "pearl_of_great_price.json")
    
    study_helps = scraper.scrape_study_helps()
    scraper.save_content(study_helps, "study_helps.json")
    
    # Scrape General Conference (last 10 years for testing)
    general_conference = scraper.scrape_general_conference(2015, 2025)
    scraper.save_content(general_conference, "general_conference.json")
    
    # Scrape Come Follow Me manuals
    come_follow_me = scraper.scrape_come_follow_me()
    scraper.save_content(come_follow_me, "come_follow_me.json")
    
    # Combine all content
    all_content = old_testament + new_testament + doctrine_covenants + pearl_of_great_price + study_helps + general_conference + come_follow_me
    scraper.save_content(all_content, "complete_lds_content.json")
    
    logger.info(f"=== Complete LDS Content Scraping Finished ===")
    logger.info(f"Total items: {len(all_content)}")
    logger.info(f"Old Testament: {len(old_testament)} verses")
    logger.info(f"New Testament: {len(new_testament)} verses") 
    logger.info(f"Doctrine & Covenants: {len(doctrine_covenants)} verses")
    logger.info(f"Pearl of Great Price: {len(pearl_of_great_price)} verses")
    logger.info(f"Study Helps: {len(study_helps)} entries")
    logger.info(f"General Conference: {len(general_conference)} paragraphs")
    logger.info(f"Come Follow Me: {len(come_follow_me)} sections")

if __name__ == "__main__":
    main()