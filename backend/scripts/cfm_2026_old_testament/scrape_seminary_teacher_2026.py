#!/usr/bin/env python3
"""
Old Testament Seminary Teacher Manual 2026 Scraper
Scrapes teaching content and lesson plans for intermediate tier CFM Deep Dive

Usage:
    python scrape_seminary_teacher_2026.py [--test] [--limit N]
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

class SeminaryTeacher2026Scraper:
    def __init__(self):
        self.base_url = "https://www.churchofjesuschrist.org"
        self.manual_url = "https://www.churchofjesuschrist.org/study/manual/old-testament-seminary-manual-2026"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
        
        # Mapping CFM weeks to Seminary lesson ranges
        self.cfm_to_seminary_mapping = self._create_cfm_seminary_mapping()

    def _create_cfm_seminary_mapping(self) -> Dict[int, List[int]]:
        """Create mapping between CFM weeks and Seminary lesson numbers"""
        # This maps CFM week numbers to corresponding seminary lesson numbers
        # Based on the scripture coverage overlap
        return {
            1: [1, 2],  # Introduction to Old Testament
            2: [3, 4, 5, 6],  # Moses 1; Abraham 3
            3: [7, 8, 9],  # Genesis 1-2; Moses 2-3; Abraham 4-5
            4: [10, 11, 12],  # Genesis 3-4; Moses 4-5
            5: [13, 14],  # Genesis 5; Moses 6
            6: [16, 17, 18],  # Moses 7
            7: [19, 20, 21],  # Genesis 6-11; Moses 8
            8: [22, 23, 24],  # Genesis 12-17; Abraham 1-2
            9: [25, 26, 27, 28],  # Genesis 18-23
            10: [29, 30, 31, 32],  # Genesis 24-33
            11: [33, 34],  # Genesis 37-41
            12: [35, 36, 37],  # Genesis 42-50
            13: [38, 39, 40],  # Exodus 1-6
            14: [41, 42, 43, 44],  # Exodus 7-13 + Easter
            15: [45, 46, 47],  # Exodus 14-18
            16: [48, 49, 50, 51],  # Exodus 19-20; 24; 31-34
            17: [52, 53, 54, 55],  # Exodus 35-40; Leviticus
            18: [56, 57],  # Numbers 11-14; 20-24; 27
            19: [58, 59, 60],  # Deuteronomy 6-8; 15; 18; 29-30; 34
            20: [61, 62, 63, 64],  # Joshua 1-8; 23-24
            # Continue mapping for all 52 weeks...
        }

    def get_seminary_lesson_links(self) -> List[Dict[str, str]]:
        """Get all seminary lesson links from the main manual page"""
        logger.info("Getting seminary lesson links...")
        
        try:
            response = self.session.get(f"{self.manual_url}?lang=eng")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            lesson_links = []
            
            # Find all lesson links
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                text = link.get_text(strip=True)
                
                # Match lesson pattern (e.g., "Lesson 1—Introduction to the Old Testament")
                lesson_match = re.match(r'Lesson (\d+)—(.+)', text)
                if lesson_match and 'old-testament-seminary-manual-2026' in href:
                    lesson_num = int(lesson_match.group(1))
                    lesson_title = lesson_match.group(2)
                    
                    lesson_links.append({
                        'lesson_number': lesson_num,
                        'title': lesson_title,
                        'url': urljoin(self.base_url, href)
                    })
            
            # Sort by lesson number
            lesson_links.sort(key=lambda x: x['lesson_number'])
            
            logger.info(f"Found {len(lesson_links)} seminary lessons")
            return lesson_links
            
        except Exception as e:
            logger.error(f"Error getting lesson links: {e}")
            return []

    def parse_teaching_content(self, soup: BeautifulSoup) -> Dict[str, List[str]]:
        """Extract teaching-specific content from lesson page"""
        teaching_ideas = []
        discussion_questions = []
        activities = []
        doctrinal_mastery = []
        
        # Look for teaching suggestions and activities
        for elem in soup.find_all(['div', 'p', 'li', 'blockquote']):
            text = elem.get_text(strip=True)
            if not text:
                continue
            
            text_lower = text.lower()
            
            # Categorize content based on keywords
            if any(keyword in text_lower for keyword in ['teaching idea', 'suggestion', 'consider', 'you might']):
                teaching_ideas.append(text)
            elif any(keyword in text_lower for keyword in ['question', 'ask students', 'discuss', 'how', 'why', 'what']):
                if '?' in text:
                    discussion_questions.append(text)
            elif any(keyword in text_lower for keyword in ['activity', 'object lesson', 'demonstration', 'role play']):
                activities.append(text)
            elif 'doctrinal mastery' in text_lower:
                doctrinal_mastery.append(text)
        
        return {
            'teaching_ideas': teaching_ideas,
            'discussion_questions': discussion_questions,
            'activities': activities,
            'doctrinal_mastery': doctrinal_mastery
        }

    def scrape_seminary_lesson(self, lesson_info: Dict) -> Optional[Dict]:
        """Scrape content for a specific seminary lesson"""
        logger.info(f"Scraping seminary lesson {lesson_info['lesson_number']}: {lesson_info['title']}")
        
        try:
            response = self.session.get(lesson_info['url'])
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract main content
            main_content = soup.find('div', class_='body-block') or soup.find('main')
            if not main_content:
                logger.warning(f"Could not find main content for lesson {lesson_info['lesson_number']}")
                return None
            
            # Extract lesson purpose/objective
            purpose = ""
            purpose_elem = main_content.find(['p', 'div'], string=re.compile(r'purpose|objective|help students', re.I))
            if purpose_elem:
                purpose = purpose_elem.get_text(strip=True)
            
            # Extract main content text
            content_paragraphs = []
            for p in main_content.find_all('p'):
                text = p.get_text(strip=True)
                if text and len(text) > 20:  # Filter out very short paragraphs
                    content_paragraphs.append(text)
            
            main_text = "\n\n".join(content_paragraphs)
            
            # Extract teaching-specific content
            teaching_content = self.parse_teaching_content(soup)
            
            # Extract scripture references
            scripture_refs = []
            for link in main_content.find_all('a', href=True):
                href = link.get('href', '')
                if '/study/' in href and any(book in href.lower() for book in 
                    ['genesis', 'exodus', 'leviticus', 'numbers', 'deuteronomy', 'joshua', 'judges', 'moses', 'abraham']):
                    ref_text = link.get_text(strip=True)
                    scripture_refs.append(ref_text)
            
            # Extract subsections
            subsections = []
            for heading in main_content.find_all(['h2', 'h3', 'h4']):
                subsections.append({
                    'type': 'heading',
                    'level': heading.name,
                    'text': heading.get_text(strip=True)
                })
            
            time.sleep(1)  # Be respectful to the server
            
            return {
                'lesson_number': lesson_info['lesson_number'],
                'title': lesson_info['title'],
                'purpose': purpose,
                'content': main_text,
                'teaching_ideas': teaching_content['teaching_ideas'],
                'discussion_questions': teaching_content['discussion_questions'],
                'activities': teaching_content['activities'],
                'doctrinal_mastery': teaching_content['doctrinal_mastery'],
                'scripture_references': scripture_refs,
                'subsections': subsections
            }
            
        except Exception as e:
            logger.error(f"Error scraping seminary lesson {lesson_info['lesson_number']}: {e}")
            return None

    def group_lessons_by_cfm_week(self, seminary_lessons: List[Dict]) -> Dict[int, List[Dict]]:
        """Group seminary lessons by CFM week based on scripture coverage"""
        grouped = {}
        
        for cfm_week, seminary_lesson_nums in self.cfm_to_seminary_mapping.items():
            cfm_lessons = []
            for lesson_num in seminary_lesson_nums:
                # Find matching seminary lesson
                matching_lesson = next((l for l in seminary_lessons if l['lesson_number'] == lesson_num), None)
                if matching_lesson:
                    cfm_lessons.append(matching_lesson)
            
            if cfm_lessons:
                grouped[cfm_week] = cfm_lessons
        
        return grouped

    def create_intermediate_tier_content(self, cfm_week: int, seminary_lessons: List[Dict]) -> ContentSection:
        """Create intermediate tier content from seminary lessons"""
        if not seminary_lessons:
            return ContentSection(
                title=f"Teaching Week {cfm_week}",
                content="",
                subsections=[],
                teaching_ideas=[],
                discussion_questions=[],
                cross_references=[]
            )
        
        # Combine content from all relevant seminary lessons
        combined_title = f"Teaching Week {cfm_week}: " + ", ".join([lesson['title'] for lesson in seminary_lessons[:2]])  # Limit title length
        
        # Combine main content
        combined_content = []
        all_teaching_ideas = []
        all_discussion_questions = []
        all_activities = []
        all_subsections = []
        
        for lesson in seminary_lessons:
            if lesson.get('purpose'):
                combined_content.append(f"Lesson Purpose: {lesson['purpose']}")
            
            if lesson.get('content'):
                combined_content.append(lesson['content'])
            
            all_teaching_ideas.extend(lesson.get('teaching_ideas', []))
            all_discussion_questions.extend(lesson.get('discussion_questions', []))
            all_activities.extend(lesson.get('activities', []))
            all_subsections.extend(lesson.get('subsections', []))
        
        # Combine teaching ideas and activities
        combined_teaching_ideas = all_teaching_ideas + all_activities
        
        return ContentSection(
            title=combined_title,
            content="\n\n".join(combined_content),
            subsections=all_subsections,
            teaching_ideas=combined_teaching_ideas[:15],  # Limit to avoid overwhelming
            discussion_questions=all_discussion_questions[:10],
            cross_references=[]  # Will be populated separately
        )

    def scrape_all_lessons(self, limit: Optional[int] = None, test_mode: bool = False) -> Dict[int, ContentSection]:
        """Scrape all seminary lessons and organize by CFM week"""
        logger.info("Starting Seminary Teacher Manual 2026 scraping...")
        
        # Get lesson links
        lesson_links = self.get_seminary_lesson_links()
        
        if test_mode:
            lesson_links = lesson_links[:10]  # First 10 lessons in test mode
        elif limit:
            lesson_links = lesson_links[:limit]
        
        # Scrape individual lessons
        seminary_lessons = []
        for lesson_info in lesson_links:
            lesson_data = self.scrape_seminary_lesson(lesson_info)
            if lesson_data:
                seminary_lessons.append(lesson_data)
        
        # Group by CFM weeks
        grouped_lessons = self.group_lessons_by_cfm_week(seminary_lessons)
        
        # Create intermediate tier content for each CFM week
        intermediate_content = {}
        for cfm_week, lessons in grouped_lessons.items():
            intermediate_content[cfm_week] = self.create_intermediate_tier_content(cfm_week, lessons)
        
        logger.info(f"✅ Created intermediate content for {len(intermediate_content)} CFM weeks")
        return intermediate_content

def main():
    parser = argparse.ArgumentParser(description="Scrape Seminary Teacher Manual 2026")
    parser.add_argument("--test", action="store_true", help="Test mode - only scrape first 10 lessons")
    parser.add_argument("--limit", type=int, help="Limit number of lessons to scrape")
    parser.add_argument("--output", default="../content/seminary_teacher_2026.json", help="Output file path")
    
    args = parser.parse_args()
    
    scraper = SeminaryTeacher2026Scraper()
    intermediate_content = scraper.scrape_all_lessons(limit=args.limit, test_mode=args.test)
    
    # Save to file
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    
    # Convert to JSON serializable format
    output_data = {
        'type': 'intermediate_tier_content',
        'source': 'Old Testament Seminary Teacher Manual 2026',
        'scraped_date': time.strftime("%Y-%m-%d"),
        'cfm_weeks': {}
    }
    
    for week_num, content_section in intermediate_content.items():
        output_data['cfm_weeks'][str(week_num)] = {
            'title': content_section.title,
            'content': content_section.content,
            'subsections': content_section.subsections,
            'teaching_ideas': content_section.teaching_ideas,
            'discussion_questions': content_section.discussion_questions
        }
    
    with open(args.output, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    logger.info(f"✅ Seminary Teacher Manual scraping complete!")
    logger.info(f"   📚 Created content for {len(intermediate_content)} CFM weeks")
    logger.info(f"   💾 Saved to {args.output}")

if __name__ == "__main__":
    main()