#!/usr/bin/env python3
"""
Come Follow Me Weekly Bundle Scraper
Scrapes individual CFM lessons with their associated scriptures
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import re
from urllib.parse import urljoin, urlparse
from typing import Dict, List, Any

class CFMWeeklyScraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.cfm_base = "/study/manual/come-follow-me-for-home-and-church-old-testament-2026"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_week_simple(self, url_date_range: str) -> Dict[str, Any]:
        """
        Scrape a CFM week using just the URL date range
        
        Args:
            url_date_range: URL date format (e.g., "december30-january5")
        """
        print(f"🔍 Scraping CFM week: {url_date_range}")
        
        # Scrape CFM lesson first to get title and other details
        cfm_content = self._scrape_cfm_lesson(url_date_range)
        
        if not cfm_content:
            print(f"❌ Failed to scrape CFM content for {url_date_range}")
            return {}
        
        # Extract scripture links from the CFM content
        scripture_links = self._extract_scripture_links(cfm_content)
        
        # Scrape all scripture chapters
        scripture_chapters = []
        for link_info in scripture_links:
            chapter_content = self._scrape_scripture_content(link_info['url'])
            if chapter_content:
                scripture_chapters.append(chapter_content)
        
        return {
            'cfm_content': cfm_content,
            'scripture_chapters': scripture_chapters,
            'total_scripture_links': len(scripture_links),
            'scraped_chapters': len(scripture_chapters)
        }

    def scrape_week(self, week_number: int, date_range: str, title: str) -> Dict[str, Any]:
        """
        Scrape a complete CFM week with its scriptures
        
        Args:
            week_number: Week number (1-52)
            date_range: Date range string (e.g., "January 26 - February 1")
            title: Lesson title (e.g., "Teach These Things Freely Unto Your Children")
        """
        print(f"🔍 Scraping Week {week_number}: {title}")
        
        # Format week number with leading zero if needed
        week_str = f"{week_number:02d}"
        cfm_url = f"{self.base_url}{self.cfm_base}/{week_str}?lang=eng"
        
        bundle = {
            "week_number": week_number,
            "date_range": date_range,
            "title": title,
            "bundle_title": f'Week {week_number}: {date_range}: "{title}"',
            "cfm_lesson_url": cfm_url,
            "cfm_lesson_content": {},
            "scripture_content": [],
            "scraped_timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            # Scrape CFM lesson content
            bundle["cfm_lesson_content"] = self._scrape_cfm_lesson(cfm_url)
            
            # Extract scripture links from CFM content
            scripture_links = self._extract_scripture_links(bundle["cfm_lesson_content"])
            
            # Scrape each scripture
            for scripture_link in scripture_links:
                scripture_content = self._scrape_scripture_content(scripture_link)
                if scripture_content:
                    bundle["scripture_content"].append(scripture_content)
                    time.sleep(0.5)  # Be respectful
            
            print(f"✅ Successfully scraped Week {week_number} with {len(bundle['scripture_content'])} scriptures")
            return bundle
            
        except Exception as e:
            print(f"❌ Error scraping Week {week_number}: {e}")
            return bundle
    
    def _scrape_cfm_lesson(self, url: str) -> Dict[str, Any]:
        """Scrape the main CFM lesson content"""
        response = self.session.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        
        content = {
            "url": url,
            "title": self._extract_title(soup),
            "scripture_references": self._extract_scripture_references(soup),
            "introduction": self._extract_introduction(soup),
            "learning_at_home_church": self._extract_learning_sections(soup),
            "teaching_children": self._extract_children_sections(soup),
            "study_helps": self._extract_study_helps(soup),
            "raw_text": soup.get_text(strip=True, separator='\n')
        }
        
        return content
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract lesson title"""
        title_elem = soup.find('h1') or soup.find('title')
        return title_elem.get_text(strip=True) if title_elem else ""
    
    def _extract_scripture_references(self, soup: BeautifulSoup) -> str:
        """Extract main scripture references from lesson"""
        # Look for scripture references in the title or header
        header = soup.find('h1') or soup.find('header')
        if header:
            # Find scripture links or references
            scripture_text = ""
            for link in header.find_all('a'):
                if '/scriptures/' in link.get('href', ''):
                    scripture_text += link.get_text(strip=True) + "; "
            return scripture_text.rstrip("; ")
        return ""
    
    def _extract_scripture_links(self, cfm_content: Dict[str, Any]) -> List[Dict[str, str]]:
        """Extract scripture links from CFM content"""
        scripture_links = []
        
        # Parse scripture references from the title/header
        scripture_refs = cfm_content.get("scripture_references", "")
        if scripture_refs:
            scripture_links = self._parse_scripture_references(scripture_refs)
        
        return scripture_links
    
    def _parse_scripture_references(self, references: str) -> List[Dict[str, str]]:
        """Parse scripture references and expand ranges"""
        scripture_links = []
        
        # Normalize spaces (replace non-breaking spaces with regular spaces)
        references = references.replace('\u00A0', ' ').replace('\xa0', ' ')
        
        # Split by semicolon for multiple books/ranges
        parts = references.split(";")
        
        current_book = None
        
        for part in parts:
            part = part.strip()
            if not part:
                continue
            
            # Check if this part contains a book name (has letters followed by numbers)
            if any(c.isalpha() for c in part) and any(c.isdigit() for c in part):
                # This part has both book name and chapter info
                if "–" in part or "-" in part:
                    # Range format: "Exodus 7-13" or "Exodus 19-20"
                    parsed_refs = self._parse_range(part)
                    scripture_links.extend(parsed_refs)
                    # Extract book name for subsequent parts
                    if parsed_refs:
                        current_book = parsed_refs[0]['book']
                else:
                    # Single chapter: "Genesis 5", "Moses 1", etc.
                    parsed_refs = self._parse_single_chapter(part)
                    scripture_links.extend(parsed_refs)
                    # Extract book name for subsequent parts
                    if parsed_refs:
                        current_book = parsed_refs[0]['book']
            elif any(c.isalpha() for c in part) and not any(c.isdigit() for c in part):
                # This is just a book name like "Esther", "Amos", "Obadiah"
                parsed_refs = self._parse_whole_book(part)
                scripture_links.extend(parsed_refs)
                # Set current book for subsequent parts
                current_book = part.strip()
            else:
                # This part only has chapter info, use current_book
                if current_book and part.strip():
                    if "–" in part or "-" in part:
                        # Range without book name: "31-34"
                        scripture_links.extend(self._parse_range_with_book(current_book, part))
                    else:
                        # Single chapter without book name: "24"
                        try:
                            chapter = int(part.strip())
                            url_info = self._create_scripture_url(current_book, chapter)
                            if url_info:
                                scripture_links.append(url_info)
                        except ValueError:
                            continue
        
        return scripture_links
    
    def _parse_range_with_book(self, book_name: str, range_part: str) -> List[Dict[str, str]]:
        """Parse range with known book name like 'Genesis' and '31-34'"""
        scripture_links = []
        
        try:
            # Handle en-dash or regular dash
            if "–" in range_part:
                start_str, end_str = range_part.split("–", 1)
            else:
                start_str, end_str = range_part.split("-", 1)
            
            start_chapter = int(start_str.strip())
            end_chapter = int(end_str.strip())
            
            # Generate URLs for each chapter in range
            for chapter in range(start_chapter, end_chapter + 1):
                url_info = self._create_scripture_url(book_name, chapter)
                if url_info:
                    scripture_links.append(url_info)
        except (ValueError, IndexError):
            pass
        
        return scripture_links
    
    def _parse_range(self, reference: str) -> List[Dict[str, str]]:
        """Parse range like 'Exodus 7-13' into individual chapters"""
        scripture_links = []
        
        try:
            # Extract book and range
            if "–" in reference:
                book_part, range_part = reference.split("–", 1)
            else:
                book_part, range_part = reference.split("-", 1)
                
            book_part = book_part.strip()
            range_part = range_part.strip()
            
            # Extract book name and start chapter
            parts = book_part.rsplit(" ", 1)
            if len(parts) != 2:
                return scripture_links
                
            book_name = parts[0].strip()
            start_chapter = int(parts[1])
            end_chapter = int(range_part)
            
            # Generate URLs for each chapter in range
            for chapter in range(start_chapter, end_chapter + 1):
                url_info = self._create_scripture_url(book_name, chapter)
                if url_info:
                    scripture_links.append(url_info)
        except (ValueError, IndexError):
            pass
        
        return scripture_links
    
    def _parse_single_chapter(self, reference: str) -> List[Dict[str, str]]:
        """Parse single chapter like 'Genesis 5' or 'Moses 6', or whole books like 'Esther'"""
        scripture_links = []
        
        try:
            # Check if this is just a book name (no chapter number)
            if not any(c.isdigit() for c in reference):
                # This is a whole book reference like "Esther", "Amos", etc.
                book_name = reference.strip()
                return self._parse_whole_book(book_name)
            
            # Standard parsing for book + chapter
            parts = reference.rsplit(" ", 1)
            if len(parts) == 2:
                book_name = parts[0].strip()
                chapter = int(parts[1])
                
                url_info = self._create_scripture_url(book_name, chapter)
                if url_info:
                    scripture_links.append(url_info)
        except (ValueError, IndexError):
            pass
        
        return scripture_links
    
    def _parse_whole_book(self, book_name: str) -> List[Dict[str, str]]:
        """Parse whole book references like 'Esther' and return all chapters"""
        scripture_links = []
        
        # Define chapter counts for books that are commonly referenced as whole books
        book_chapters = {
            "Esther": 10,
            "Job": 42,
            "Ruth": 4,
            "Ezra": 10,
            "Nehemiah": 13,
            "Ecclesiastes": 12,
            "Song of Solomon": 8,
            "Lamentations": 5,
            "Daniel": 12,
            "Hosea": 14,
            "Joel": 3,
            "Amos": 9,
            "Obadiah": 1,
            "Jonah": 4,
            "Micah": 7,
            "Nahum": 3,
            "Habakkuk": 3,
            "Zephaniah": 3,
            "Haggai": 2,
            "Zechariah": 14,
            "Malachi": 4,
            # Pearl of Great Price
            "Moses": 8,
            "Abraham": 5,
            "Joseph Smith—History": 1,
            "Joseph Smith—Matthew": 1
        }
        
        if book_name in book_chapters:
            chapter_count = book_chapters[book_name]
            for chapter in range(1, chapter_count + 1):
                url_info = self._create_scripture_url(book_name, chapter)
                if url_info:
                    scripture_links.append(url_info)
        
        return scripture_links
    
    def _create_scripture_url(self, book_name: str, chapter: int) -> Dict[str, str]:
        """Create scripture URL from book name and chapter"""
        # Map book names to URL abbreviations
        book_mapping = {
            # Old Testament  
            "Genesis": ("ot", "gen"),
            "Exodus": ("ot", "ex"), 
            "Leviticus": ("ot", "lev"),
            "Numbers": ("ot", "num"),
            "Deuteronomy": ("ot", "deut"),
            "Joshua": ("ot", "josh"),
            "Judges": ("ot", "judg"),
            "Ruth": ("ot", "ruth"),
            "1 Samuel": ("ot", "1-sam"),
            "2 Samuel": ("ot", "2-sam"),
            "1 Kings": ("ot", "1-kgs"),
            "2 Kings": ("ot", "2-kgs"),
            "1 Chronicles": ("ot", "1-chr"),
            "2 Chronicles": ("ot", "2-chr"),
            "Ezra": ("ot", "ezra"),
            "Nehemiah": ("ot", "neh"),
            "Esther": ("ot", "esth"),
            "Job": ("ot", "job"),
            "Psalms": ("ot", "ps"),
            "Proverbs": ("ot", "prov"),
            "Ecclesiastes": ("ot", "eccl"),
            "Song of Solomon": ("ot", "song"),
            "Isaiah": ("ot", "isa"),
            "Jeremiah": ("ot", "jer"),
            "Lamentations": ("ot", "lam"),
            "Ezekiel": ("ot", "ezek"),
            "Daniel": ("ot", "dan"),
            "Hosea": ("ot", "hosea"),
            "Joel": ("ot", "joel"),
            "Amos": ("ot", "amos"),
            "Obadiah": ("ot", "obad"),
            "Jonah": ("ot", "jonah"),
            "Micah": ("ot", "micah"),
            "Nahum": ("ot", "nahum"),
            "Habakkuk": ("ot", "hab"),
            "Zephaniah": ("ot", "zeph"),
            "Haggai": ("ot", "hag"),
            "Zechariah": ("ot", "zech"),
            "Malachi": ("ot", "mal"),
            # Pearl of Great Price
            "Moses": ("pgp", "moses"),
            "Abraham": ("pgp", "abr"),
            "Joseph Smith—Matthew": ("pgp", "js-m"),
            "Joseph Smith—History": ("pgp", "js-h"),
            "Articles of Faith": ("pgp", "a-of-f")
        }
        
        if book_name in book_mapping:
            section, abbrev = book_mapping[book_name]
            url = f"{self.base_url}/study/scriptures/{section}/{abbrev}/{chapter}?lang=eng"
            
            return {
                "reference": f"{book_name} {chapter}",
                "url": url,
                "book": book_name,
                "chapter": chapter
            }
        
        return None
    
    def _scrape_scripture_content(self, scripture_info: Dict[str, str]) -> Dict[str, Any]:
        """Scrape content from a scripture URL"""
        try:
            response = requests.get(scripture_info["url"], timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract chapter title
            title_element = soup.find('h1')
            title = title_element.get_text(strip=True) if title_element else scripture_info["reference"]
            
            # Extract verses - look for verse containers
            verses = []
            verse_elements = soup.find_all(['p', 'div'], class_=['verse', 'study-note-ref'])
            
            for verse_elem in verse_elements:
                verse_text = verse_elem.get_text(strip=True)
                if verse_text and len(verse_text) > 10:  # Filter out very short elements
                    verses.append(verse_text)
            
            # If no verses found with class, try alternate selectors
            if not verses:
                verse_elements = soup.find_all('p')
                for verse_elem in verse_elements:
                    verse_text = verse_elem.get_text(strip=True) 
                    if verse_text and len(verse_text) > 20:
                        verses.append(verse_text)
            
            # Extract chapter summary if available
            summary_element = soup.find(['div', 'p'], class_=['summary', 'chapter-summary', 'study-summary'])
            summary = summary_element.get_text(strip=True) if summary_element else ""
            
            return {
                "reference": scripture_info["reference"],
                "title": title,
                "url": scripture_info["url"],
                "summary": summary,
                "verses": verses[:50],  # Limit verses to avoid huge content
                "full_text": " ".join(verses)
            }
            
        except Exception as e:
            print(f"Error scraping scripture {scripture_info['reference']}: {str(e)}")
            return {
                "reference": scripture_info["reference"],
                "title": f"Error loading {scripture_info['reference']}",
                "url": scripture_info["url"],
                "summary": f"Could not load content: {str(e)}",
                "verses": [],
                "full_text": ""
            }
    
    def _extract_introduction(self, soup: BeautifulSoup) -> str:
        """Extract lesson introduction"""
        introduction_text = ""
        
        # Look for the main lesson introduction - typically the first few substantial paragraphs
        # after the title and before "Ideas for Learning" sections
        main_content = soup.find('main') or soup.find('article') or soup.find('div', class_='content')
        if not main_content:
            return ""
        
        # Find all paragraphs and get substantial ones
        paragraphs = main_content.find_all('p')
        
        # Look for introduction text before "Ideas for Learning"
        ideas_heading = soup.find(['h2', 'h3'], string=lambda text: text and 'Ideas for Learning' in text)
        
        for p in paragraphs:
            # Stop if we hit the "Ideas for Learning" section
            if ideas_heading and p.sourceline and ideas_heading.sourceline and p.sourceline >= ideas_heading.sourceline:
                break
                
            text = p.get_text(strip=True)
            if len(text) > 50:  # Substantial content
                # Skip navigation/header content
                if not any(skip_word in text.lower() for skip_word in ['contents', 'january', 'december', 'appendix']):
                    introduction_text += text + "\n\n"
        
        return introduction_text.strip()
    
    def _extract_learning_sections(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract 'Ideas for Learning at Home and at Church' sections"""
        sections = []
        
        # Find the "Ideas for Learning" heading
        learning_heading = soup.find(['h2', 'h3'], string=lambda text: text and 'Ideas for Learning' in text)
        if not learning_heading:
            return sections
        
        # Find the "Teaching Children" heading to know where to stop
        teaching_heading = soup.find(['h2', 'h3'], string=lambda text: text and 'Teaching Children' in text)
        
        # Find all h3 headings between learning and teaching sections
        all_h3 = soup.find_all('h3')
        learning_h3s = []
        
        found_learning = False
        for h3 in all_h3:
            # Start collecting after we find the learning section
            if not found_learning:
                if learning_heading in h3.find_all_previous(['h2']):
                    found_learning = True
                else:
                    continue
            
            # Stop when we hit the teaching section
            if teaching_heading and teaching_heading in h3.find_all_previous(['h2']):
                break
            
            learning_h3s.append(h3)
        
        # Extract content for each learning section h3
        for h3 in learning_h3s:
            section_title = h3.get_text(strip=True)
            
            # Skip "Study Helps" as it's handled separately
            if 'Study Helps' in section_title:
                continue
                
            section_content = ""
            
            # Get all following elements until next h3 or h2
            current = h3.find_next()
            while current:
                if current.name in ['h2', 'h3']:
                    break
                if current.name == 'p' and current.get_text(strip=True):
                    section_content += current.get_text(strip=True) + "\n\n"
                current = current.find_next()
            
            if section_content.strip():
                sections.append({
                    "title": section_title,
                    "content": section_content.strip()
                })
        
        return sections
    
    def _extract_children_sections(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract 'Ideas for Teaching Children' sections"""
        sections = []
        
        # Find the "Teaching Children" heading
        children_heading = soup.find(['h2', 'h3'], string=lambda text: text and 'Teaching Children' in text)
        if not children_heading:
            return sections
        
        # Find all h3 headings after the teaching children section
        all_h3 = soup.find_all('h3')
        children_h3s = []
        
        found_teaching = False
        for h3 in all_h3:
            # Start collecting after we find the teaching section
            if not found_teaching:
                if children_heading in h3.find_all_previous(['h2']):
                    found_teaching = True
                else:
                    continue
            
            children_h3s.append(h3)
        
        # Extract content for each teaching children section h3
        for h3 in children_h3s:
            section_title = h3.get_text(strip=True)
            section_content = ""
            
            # Get all following elements until next h3 or h2
            current = h3.find_next()
            while current:
                if current.name in ['h2', 'h3']:
                    break
                if current.name == 'p' and current.get_text(strip=True):
                    section_content += current.get_text(strip=True) + "\n\n"
                current = current.find_next()
            
            if section_content.strip():
                sections.append({
                    "title": section_title,
                    "content": section_content.strip()
                })
        
        return sections
    
    def _extract_study_helps(self, soup: BeautifulSoup) -> List[str]:
        """Extract study helps and supplementary materials"""
        helps = []
        
        # Look for "Study Helps" section
        study_heading = soup.find(['h2', 'h3'], string=lambda text: text and 'Study Helps' in text)
        if not study_heading:
            return helps
        
        # Get content after Study Helps heading
        current = study_heading.find_next_sibling()
        while current:
            if current.name in ['h2', 'h3']:
                break
            if current.name in ['p', 'li', 'div'] and current.get_text(strip=True):
                helps.append(current.get_text(strip=True))
            current = current.find_next_sibling()
        
        return helps
    
    def _extract_scripture_title(self, soup: BeautifulSoup) -> str:
        """Extract scripture chapter title"""
        title_elem = soup.find('h1') or soup.find('title')
        return title_elem.get_text(strip=True) if title_elem else ""
    
    def _extract_verses(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extract individual verses from scripture"""
        verses = []
        # Implementation will depend on scripture page structure
        return verses
    
    def _extract_chapter_summary(self, soup: BeautifulSoup) -> str:
        """Extract chapter summary if available"""
        return ""
    
    def save_bundle(self, bundle: Dict[str, Any], output_dir: str = "../../content/bundles/cfm_2026"):
        """Save bundle to JSON file"""
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        filename = f"cfm_2026_week_{bundle['week_number']:02d}.json"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(bundle, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved bundle: {filepath}")

def main():
    """Example usage"""
    scraper = CFMWeeklyScraper()
    
    # Example: Scrape Week 5
    bundle = scraper.scrape_week(
        week_number=5,
        date_range="January 26 - February 1",
        title="Teach These Things Freely Unto Your Children"
    )
    
    scraper.save_bundle(bundle)

if __name__ == "__main__":
    main()