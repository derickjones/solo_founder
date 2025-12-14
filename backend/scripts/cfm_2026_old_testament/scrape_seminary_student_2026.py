#!/usr/bin/env python3
"""
Old Testament Seminary Student Manual 2026 Scraper
Scrapes scholarly and contextual content for advanced tier CFM Deep Dive

Usage:
    python scrape_seminary_student_2026.py [--test] [--limit N]
"""

import requests
from bs4 import BeautifulSoup
import json
import time
import logging
from typing import Dict, List, Optional, Tuple
import os
import re
from urllib.parse import urljoin, urlparse
import argparse
from cfm_deep_dive_schema import WeeklyLesson, ContentSection, ScriptureReference, CFMDeepDiveDataset

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SeminaryStudent2026Scraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.manual_url = "https://www.churchofjesuschrist.org/study/manual/old-testament-seminary-student-manual-2026"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Scripture mapping for advanced content
        self.scripture_to_cfm_mapping = self._create_scripture_cfm_mapping()

    def _create_scripture_cfm_mapping(self) -> Dict[str, int]:
        """Create mapping between scripture blocks and CFM week numbers"""
        # This maps scripture references to CFM weeks
        return {
            'introduction': 1,
            'moses-1': 2,
            'abraham-3': 2,
            'genesis-1-2': 3,
            'moses-2-3': 3,
            'abraham-4-5': 3,
            'genesis-3-4': 4,
            'moses-4-5': 4,
            'genesis-5': 5,
            'moses-6': 5,
            'moses-7': 6,
            'genesis-6-11': 7,
            'moses-8': 7,
            'genesis-12-17': 8,
            'abraham-1-2': 8,
            'genesis-18-23': 9,
            'genesis-24-33': 10,
            'genesis-37-41': 11,
            'genesis-42-50': 12,
            'exodus-1-6': 13,
            'exodus-7-13': 14,
            'exodus-14-18': 15,
            'exodus-19-20': 16,
            'exodus-24': 16,
            'exodus-31-34': 16,
            'exodus-35-40': 17,
            'leviticus-1': 17,
            'leviticus-4': 17,
            'leviticus-16': 17,
            'leviticus-19': 17,
            'numbers-11-14': 18,
            'numbers-20-24': 18,
            'numbers-27': 18,
            'deuteronomy-6-8': 19,
            'deuteronomy-15': 19,
            'deuteronomy-18': 19,
            'deuteronomy-29-30': 19,
            'deuteronomy-34': 19,
            'joshua-1-8': 20,
            'joshua-23-24': 20,
            # Continue for all scripture blocks...
        }

    def get_student_manual_sections(self) -> List[Dict[str, str]]:
        """Get all sections from the student manual"""
        logger.info("Getting student manual sections...")
        
        try:
            response = self.session.get(f"{self.manual_url}?lang=eng")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            sections = []
            
            # Find all section links
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Look for scripture-based sections
                if 'old-testament-seminary-student-manual-2026' in href and any(book in text.lower() for book in 
                    ['moses', 'abraham', 'genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges']):
                    
                    sections.append({
                        'title': text,
                        'url': urljoin(self.base_url, href),
                        'scripture_key': self._extract_scripture_key(text)
                    })
            
            logger.info(f"Found {len(sections)} student manual sections")
            return sections
            
        except Exception as e:
            logger.error(f"Error getting student manual sections: {e}")
            return []

    def _extract_scripture_key(self, title: str) -> str:
        """Extract a standardized scripture key from the title"""
        title_lower = title.lower()
        
        # Extract book and chapter patterns
        patterns = [
            (r'moses\s+(\d+)', 'moses-{}'),
            (r'abraham\s+(\d+)', 'abraham-{}'),
            (r'genesis\s+(\d+(?:[–-]\d+)?)', 'genesis-{}'),
            (r'exodus\s+(\d+(?:[–-]\d+)?)', 'exodus-{}'),
            (r'leviticus\s+(\d+(?:[–-]\d+)?)', 'leviticus-{}'),
            (r'numbers\s+(\d+(?:[–-]\d+)?)', 'numbers-{}'),
            (r'deuteronomy\s+(\d+(?:[–-]\d+)?)', 'deuteronomy-{}'),
            (r'joshua\s+(\d+(?:[–-]\d+)?)', 'joshua-{}'),
        ]
        
        for pattern, format_str in patterns:
            match = re.search(pattern, title_lower)
            if match:
                return format_str.format(match.group(1))
        
        # Default fallback
        return title_lower.replace(' ', '-').replace('–', '-')

    def parse_scholarly_content(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract scholarly and contextual content"""
        historical_context = []
        cultural_background = []
        scholarly_insights = []
        cross_references = []
        study_questions = []
        
        # Look for scholarly content patterns
        for elem in soup.find_all(['div', 'p', 'blockquote', 'aside']):
            text = elem.get_text(strip=True)
            if not text or len(text) < 20:
                continue
            
            text_lower = text.lower()
            
            # Categorize based on content type
            if any(keyword in text_lower for keyword in ['historical', 'ancient', 'context', 'background', 'time of']):
                historical_context.append(text)
            elif any(keyword in text_lower for keyword in ['culture', 'custom', 'tradition', 'society', 'practice']):
                cultural_background.append(text)
            elif any(keyword in text_lower for keyword in ['scholar', 'research', 'study', 'analysis', 'commentary']):
                scholarly_insights.append(text)
            elif any(keyword in text_lower for keyword in ['consider', 'ponder', 'reflect', 'think about']):
                study_questions.append(text)
            elif 'see also' in text_lower or 'compare' in text_lower:
                cross_references.append(text)
        
        return {
            'historical_context': historical_context,
            'cultural_background': cultural_background,
            'scholarly_insights': scholarly_insights,
            'study_questions': study_questions,
            'cross_references': cross_references
        }

    def scrape_student_section(self, section_info: Dict) -> Optional[Dict]:
        """Scrape content for a specific student manual section"""
        logger.info(f"Scraping student section: {section_info['title']}")
        
        try:
            response = self.session.get(section_info['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content
            main_content = soup.find('div', class_='body-block') or soup.find('main')
            if not main_content:
                logger.warning(f"Could not find main content for section: {section_info['title']}")
                return None
            
            # Extract overview/introduction
            overview = ""
            intro_elem = main_content.find(['div', 'p'], class_=lambda x: x and 'intro' in x.lower()) or \
                        main_content.find('p', string=re.compile(r'overview|introduction', re.I))
            
            if intro_elem:
                overview = intro_elem.get_text(strip=True)
            
            # Extract main content paragraphs
            content_paragraphs = []
            for p in main_content.find_all('p'):
                text = p.get_text(strip=True)
                if text and len(text) > 30:  # Filter out short paragraphs
                    content_paragraphs.append(text)
            
            main_text = "\n\n".join(content_paragraphs)
            
            # Extract scholarly content
            scholarly_content = self.parse_scholarly_content(soup)
            
            # Extract supplementary materials
            supplementary = []
            for elem in main_content.find_all(['aside', 'div'], class_=lambda x: x and any(cls in x.lower() for cls in ['note', 'sidebar', 'supplement'])):
                supp_text = elem.get_text(strip=True)
                if supp_text:
                    supplementary.append(supp_text)
            
            # Extract doctrinal emphasis
            doctrinal_points = []
            for strong in main_content.find_all(['strong', 'b', 'em']):
                text = strong.get_text(strip=True)
                if len(text) > 10 and len(text) < 200:
                    doctrinal_points.append(text)
            
            time.sleep(1)  # Be respectful to the server
            
            return {
                'title': section_info['title'],
                'scripture_key': section_info['scripture_key'],
                'overview': overview,
                'content': main_text,
                'historical_context': scholarly_content['historical_context'],
                'cultural_background': scholarly_content['cultural_background'],
                'scholarly_insights': scholarly_content['scholarly_insights'],
                'study_questions': scholarly_content['study_questions'],
                'cross_references': scholarly_content['cross_references'],
                'supplementary_materials': supplementary,
                'doctrinal_points': doctrinal_points
            }
            
        except Exception as e:
            logger.error(f"Error scraping student section {section_info['title']}: {e}")
            return None

    def group_sections_by_cfm_week(self, student_sections: List[Dict]) -> Dict[int, List[Dict]]:
        """Group student manual sections by CFM week"""
        grouped = {}
        
        for section in student_sections:
            scripture_key = section.get('scripture_key', '')
            cfm_week = self.scripture_to_cfm_mapping.get(scripture_key)
            
            if cfm_week:
                if cfm_week not in grouped:
                    grouped[cfm_week] = []
                grouped[cfm_week].append(section)
            else:
                # Try to match partial keys
                for key, week in self.scripture_to_cfm_mapping.items():
                    if key in scripture_key or scripture_key in key:
                        if week not in grouped:
                            grouped[week] = []
                        grouped[week].append(section)
                        break
        
        return grouped

    def create_advanced_tier_content(self, cfm_week: int, student_sections: List[Dict]) -> ContentSection:
        """Create advanced tier content from student manual sections"""
        if not student_sections:
            return ContentSection(
                title=f"Scholarly Study - Week {cfm_week}",
                content="",
                subsections=[],
                teaching_ideas=[],
                discussion_questions=[],
                cross_references=[]
            )
        
        # Combine content from all relevant sections
        combined_title = f"Scholarly Study - Week {cfm_week}: " + ", ".join([section['title'] for section in student_sections[:2]])
        
        # Combine all advanced content
        combined_content = []
        all_historical = []
        all_cultural = []
        all_scholarly = []
        all_study_questions = []
        all_doctrinal = []
        
        for section in student_sections:
            if section.get('overview'):
                combined_content.append(f"Overview: {section['overview']}")
            
            if section.get('content'):
                combined_content.append(section['content'])
            
            all_historical.extend(section.get('historical_context', []))
            all_cultural.extend(section.get('cultural_background', []))
            all_scholarly.extend(section.get('scholarly_insights', []))
            all_study_questions.extend(section.get('study_questions', []))
            all_doctrinal.extend(section.get('doctrinal_points', []))
        
        # Create structured subsections for advanced content
        subsections = []
        
        if all_historical:
            subsections.append({
                'type': 'section',
                'title': 'Historical Context',
                'content': all_historical[:5]  # Limit to avoid overwhelming
            })
        
        if all_cultural:
            subsections.append({
                'type': 'section', 
                'title': 'Cultural Background',
                'content': all_cultural[:5]
            })
        
        if all_scholarly:
            subsections.append({
                'type': 'section',
                'title': 'Scholarly Insights', 
                'content': all_scholarly[:5]
            })
        
        if all_doctrinal:
            subsections.append({
                'type': 'section',
                'title': 'Key Doctrinal Points',
                'content': all_doctrinal[:10]
            })
        
        # Combine teaching ideas (focus on deep study methods)
        advanced_teaching_ideas = [
            "Research historical and cultural context using scholarly resources",
            "Compare ancient Near Eastern parallels and influences",
            "Analyze literary patterns and structures in the text",
            "Study original Hebrew/Greek terms and their meanings",
            "Explore archaeological discoveries related to the scriptures",
            "Examine different manuscript traditions and textual variants",
            "Investigate prophetic and typological interpretations"
        ]
        
        return ContentSection(
            title=combined_title,
            content="\n\n".join(combined_content),
            subsections=subsections,
            teaching_ideas=advanced_teaching_ideas,
            discussion_questions=all_study_questions[:8],
            cross_references=[]  # Will be populated separately
        )

    def scrape_all_sections(self, limit: Optional[int] = None, test_mode: bool = False) -> Dict[int, ContentSection]:
        """Scrape all student manual sections and organize by CFM week"""
        logger.info("Starting Seminary Student Manual 2026 scraping...")
        
        # Get section links
        section_links = self.get_student_manual_sections()
        
        if test_mode:
            section_links = section_links[:5]  # First 5 sections in test mode
        elif limit:
            section_links = section_links[:limit]
        
        # Scrape individual sections
        student_sections = []
        for section_info in section_links:
            section_data = self.scrape_student_section(section_info)
            if section_data:
                student_sections.append(section_data)
        
        # Group by CFM weeks
        grouped_sections = self.group_sections_by_cfm_week(student_sections)
        
        # Create advanced tier content for each CFM week
        advanced_content = {}
        for cfm_week, sections in grouped_sections.items():
            advanced_content[cfm_week] = self.create_advanced_tier_content(cfm_week, sections)
        
        logger.info(f"✅ Created advanced content for {len(advanced_content)} CFM weeks")
        return advanced_content

def main():
    parser = argparse.ArgumentParser(description="Scrape Seminary Student Manual 2026")
    parser.add_argument("--test", action="store_true", help="Test mode - only scrape first 5 sections")
    parser.add_argument("--limit", type=int, help="Limit number of sections to scrape")
    parser.add_argument("--output", default="../content/seminary_student_2026.json", help="Output file path")
    
    args = parser.parse_args()
    
    scraper = SeminaryStudent2026Scraper()
    advanced_content = scraper.scrape_all_sections(limit=args.limit, test_mode=args.test)
    
    # Save to file
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Convert to JSON serializable format
    output_data = {
        'type': 'advanced_tier_content',
        'source': 'Old Testament Seminary Student Manual 2026',
        'scraped_date': time.strftime("%Y-%m-%d"),
        'cfm_weeks': {}
    }
    
    for week_num, content_section in advanced_content.items():
        output_data['cfm_weeks'][str(week_num)] = {
            'title': content_section.title,
            'content': content_section.content,
            'subsections': content_section.subsections,
            'teaching_ideas': content_section.teaching_ideas,
            'discussion_questions': content_section.discussion_questions
        }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Seminary Student Manual scraping complete!")
    logger.info(f"   📚 Created content for {len(advanced_content)} CFM weeks")
    logger.info(f"   💾 Saved to {args.output}")

if __name__ == "__main__":
    main()