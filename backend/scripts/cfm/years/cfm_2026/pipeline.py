#!/usr/bin/env python3
"""
Unified CFM Content Pipeline - Single pipeline compiles all sources
"""

import json
import argparse
import logging
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any

# Add the core module to the path
sys.path.append(str(Path(__file__).parent.parent.parent / 'core'))
from schema import CFMYear, WeeklyBundle, ContentSource, ScriptureReference
from base_pipeline import BaseCFMPipeline

# Also import from config for the 2026 year configuration
from config import CFM_2026_CONFIG

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class CFM2026Pipeline(BaseCFMPipeline):
    """CFM 2026 Old Testament pipeline that compiles all content sources"""
    
    def __init__(self, content_dir: str = "../../content/sources"):
        super().__init__(content_dir)
        self.config = CFM_2026_CONFIG
        
        # CFM week to seminary lesson mapping (from config)
        self.cfm_to_seminary_mapping = self.config.get('seminary_mapping', {})
    
    def load_all_content(self) -> Dict[str, Dict]:
        """Load all content sources"""
        logger.info("Loading all content sources...")
        
        content = {}
        
        # Load CFM content
        cfm_file = self.content_dir / "cfm_2026_basic.json"
        if cfm_file.exists():
            with open(cfm_file, 'r', encoding='utf-8') as f:
                cfm_data = json.load(f)
                content['cfm'] = {}
                for lesson in cfm_data.get('lessons', []):
                    week_num = lesson.get('week_number')
                    if week_num:
                        content['cfm'][week_num] = lesson
                logger.info(f"Loaded {len(content['cfm'])} CFM lessons")
        
        # Load Seminary Teacher content
        teacher_file = self.content_dir / "seminary_teacher_2026_enhanced.json"
        if teacher_file.exists():
            with open(teacher_file, 'r', encoding='utf-8') as f:
                teacher_data = json.load(f)
                content['seminary_teacher'] = teacher_data.get('cfm_weeks', {})
                logger.info(f"Loaded {len(content['seminary_teacher'])} Seminary Teacher weeks")
        else:
            content['seminary_teacher'] = {}
        
        # Load Pearl of Great Price content (for Moses and Abraham)
        pogp_file = self.content_dir / "pearl_of_great_price.json"
        if pogp_file.exists():
            with open(pogp_file, 'r', encoding='utf-8') as f:
                pogp_data = json.load(f)
                # Convert list format to book/chapter structure
                content['pearl_of_great_price'] = {}
                for verse_data in pogp_data:
                    book = verse_data.get('book')
                    chapter = verse_data.get('chapter')
                    verse = verse_data.get('verse')
                    
                    if book and chapter is not None and verse is not None:
                        if book not in content['pearl_of_great_price']:
                            content['pearl_of_great_price'][book] = {}
                        if chapter not in content['pearl_of_great_price'][book]:
                            content['pearl_of_great_price'][book][chapter] = {'verses': {}}
                        
                        content['pearl_of_great_price'][book][chapter]['verses'][verse] = {
                            'text': verse_data.get('content', ''),
                            'citation': verse_data.get('citation', '')
                        }
                
                pogp_books = len(content['pearl_of_great_price'])
                logger.info(f"Loaded Pearl of Great Price content for {pogp_books} books")
        else:
            content['pearl_of_great_price'] = {}
        
        # Load Old Testament content
        ot_file = self.content_dir / "old_testament.json"
        if ot_file.exists():
            with open(ot_file, 'r', encoding='utf-8') as f:
                ot_data = json.load(f)
                # Convert list of verses to book/chapter structure
                content['old_testament'] = {}
                for verse_data in ot_data:
                    book = verse_data.get('book')
                    chapter = verse_data.get('chapter')
                    verse = verse_data.get('verse')
                    
                    if book and chapter is not None and verse is not None:
                        if book not in content['old_testament']:
                            content['old_testament'][book] = {}
                        if chapter not in content['old_testament'][book]:
                            content['old_testament'][book][chapter] = {'verses': {}}
                        
                        content['old_testament'][book][chapter]['verses'][verse] = {
                            'text': verse_data.get('content', ''),
                            'citation': verse_data.get('citation', '')
                        }
                
                ot_books = len(content['old_testament'])
                logger.info(f"Loaded Old Testament content for {ot_books} books")
        else:
            content['old_testament'] = {}
        
        return content
    
    def extract_scripture_refs(self, cfm_data: Dict) -> List[ScriptureReference]:
        """Extract scripture references from CFM data"""
        refs = []
        
        # First try the parsed primary_scriptures
        for ref_data in cfm_data.get('primary_scriptures', []):
            refs.append(ScriptureReference(
                book=ref_data['book'],
                chapters=ref_data['chapters'],
                verses=ref_data.get('verses'),
                book_type=ref_data.get('book_type', 'old_testament')
            ))
        
        # If no parsed refs, try to parse from date_range or title
        if not refs:
            # Try both date_range and title fields
            text_to_parse = f"{cfm_data.get('date_range', '')} {cfm_data.get('title', '')}"
            refs = self.parse_scripture_references_from_text(text_to_parse)
        
        return refs
    
    def parse_scripture_references_from_text(self, text: str) -> List[ScriptureReference]:
        """Parse scripture references from text using improved regex patterns"""
        import re
        refs = []
        
        # Common scripture books in Old Testament
        books_pattern = (
            r'\b(Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|'
            r'1 Samuel|2 Samuel|1 Kings|2 Kings|1 Chronicles|2 Chronicles|'
            r'Ezra|Nehemiah|Esther|Job|Psalms?|Proverbs|Ecclesiastes|'
            r'Song of Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|'
            r'Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|'
            r'Haggai|Zechariah|Malachi|Moses|Abraham)\b'
        )
        
        # Pattern to match "Book Chapter" or "Book Chapter-Chapter"
        patterns = [
            rf'{books_pattern}\s+(\d+(?:[–-]\d+)?)',
            rf'{books_pattern}\s+(\d+(?:[–-]\d+)?(?:;\s*\d+(?:[–-]\d+)?)*)'
        ]
        
        for pattern in patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                book = match.group(1)
                chapters_str = match.group(2)
                
                # Parse chapters (handle ranges like "1-3" and lists like "1;3;5")
                chapters = []
                for part in re.split(r'[;,]', chapters_str):
                    part = part.strip()
                    if '–' in part or '-' in part:
                        # Handle ranges
                        start, end = re.split(r'[–-]', part)
                        chapters.extend([str(i) for i in range(int(start), int(end) + 1)])
                    elif part.isdigit():
                        chapters.append(part)
                
                if chapters:
                    book_type = "pearl_of_great_price" if book.lower() in ['moses', 'abraham'] else "old_testament"
                    refs.append(ScriptureReference(
                        book=book,
                        chapters=chapters,
                        verses=None,
                        book_type=book_type
                    ))
        
        return refs
    
    def get_scripture_content(self, scripture_refs: List[ScriptureReference], 
                            ot_content: Dict, pogp_content: Dict) -> Dict[str, Any]:
        """Get full scripture text for referenced chapters"""
        scripture_content = {}
        
        for ref in scripture_refs:
            book_name = ref.book
            
            # Check Pearl of Great Price first (Moses, Abraham, etc.)
            if ref.book_type == "pearl_of_great_price" and book_name in pogp_content:
                book_data = pogp_content[book_name]
                scripture_content[book_name] = {}
                
                for chapter_num in ref.chapters:
                    chapter_key = int(chapter_num)
                    if chapter_key in book_data:
                        scripture_content[book_name][chapter_num] = book_data[chapter_key]
            
            # Check Old Testament
            elif book_name in ot_content:
                book_data = ot_content[book_name]
                scripture_content[book_name] = {}
                
                for chapter_num in ref.chapters:
                    chapter_key = int(chapter_num)
                    if chapter_key in book_data:
                        scripture_content[book_name][chapter_num] = book_data[chapter_key]
        
        return scripture_content
    
    def extract_all_elements(self, content_sources: List[ContentSource]) -> Dict:
        """Extract all teaching elements from content sources"""
        elements = {
            'subsections': [],
            'teaching_ideas': [],
            'discussion_questions': [],
            'themes': [],
            'cross_references': [],
            'doctrinal_mastery': []
        }
        
        for source in content_sources:
            # Extract from source content - this would need more sophisticated parsing
            # For now, using any structured data available in the sources
            if hasattr(source, 'subsections'):
                elements['subsections'].extend(getattr(source, 'subsections', []))
            if hasattr(source, 'teaching_ideas'):
                elements['teaching_ideas'].extend(getattr(source, 'teaching_ideas', []))
            if hasattr(source, 'discussion_questions'):
                elements['discussion_questions'].extend(getattr(source, 'discussion_questions', []))
            if hasattr(source, 'themes'):
                elements['themes'].extend(getattr(source, 'themes', []))
        
        # Remove duplicates
        elements['themes'] = list(set(elements['themes']))
        
        return elements
    
    def build_weekly_content(self, week_number: int, all_content: Dict) -> Optional[WeeklyBundle]:
        """Build comprehensive weekly content from all sources"""
        logger.info(f"Building unified content for week {week_number}")
        
        # Get CFM content for this week
        cfm_data = all_content['cfm'].get(week_number)
        if not cfm_data:
            logger.warning(f"No CFM content found for week {week_number}")
            return None
        
        # Create WeeklyBundle
        scripture_refs = self.extract_scripture_refs(cfm_data)
        
        weekly_content = WeeklyBundle(
            week_number=week_number,
            date_range=cfm_data.get('date_range', ''),
            title=cfm_data.get('title', ''),
            scripture_references=scripture_refs,
            sources=[]  # Will be populated below
        )
        
        # Add CFM content source
        basic_tier = cfm_data.get('basic_tier', {})
        cfm_source = ContentSource(
            source_type="cfm",
            title=cfm_data.get('title', ''),
            content=basic_tier.get('content', ''),
            purpose="Come Follow Me home and church study"
        )
        weekly_content.add_content_source(cfm_source)
        
        # Add Seminary content for this week
        # Seminary Teacher content
        teacher_week_data = all_content['seminary_teacher'].get(str(week_number))
        if teacher_week_data:
            teacher_source = ContentSource(
                source_type="seminary_teacher",
                title=teacher_week_data.get('title', ''),
                content=teacher_week_data.get('content', ''),
                purpose="Seminary teacher manual content"
            )
            weekly_content.add_content_source(teacher_source)
        
        # Add scripture content
        weekly_content.scripture_content = self.get_scripture_content(
            scripture_refs, all_content['old_testament'], all_content['pearl_of_great_price']
        )
        
        # Add scripture text to combined content
        for book_name, book_chapters in weekly_content.scripture_content.items():
            for chapter_num, chapter_data in book_chapters.items():
                scripture_text = ""
                verses = chapter_data.get('verses', {})
                
                # Build verse text
                for verse_num in sorted(verses.keys(), key=lambda x: int(x)):
                    verse_data = verses[verse_num]
                    verse_text = verse_data.get('text', '')
                    if verse_text:
                        scripture_text += f"{verse_num}. {verse_text}\n"
                
                if scripture_text:
                    scripture_source = ContentSource(
                        source_type="scripture",
                        title=f"{book_name} {chapter_num}",
                        content=scripture_text.strip(),
                        purpose="Full scripture text"
                    )
                    weekly_content.add_content_source(scripture_source)
                    logger.debug(f"Added scripture: {book_name} {chapter_num} ({len(scripture_text)} chars)")
        
        # Extract all teaching elements
        elements = self.extract_all_elements(weekly_content.content_sources)
        weekly_content.subsections = elements['subsections']
        weekly_content.teaching_ideas = elements['teaching_ideas']
        weekly_content.discussion_questions = elements['discussion_questions']
        weekly_content.themes = elements['themes']
        weekly_content.cross_references = elements['cross_references']
        weekly_content.doctrinal_mastery = elements['doctrinal_mastery']
        
        return weekly_content
    
    def build_week(self, week_number: int, output_dir: Optional[str] = None):
        """Build unified content for a specific week"""
        all_content = self.load_all_content()
        weekly_content = self.build_weekly_content(week_number, all_content)
        
        if not weekly_content:
            return
        
        self.dataset.add_week(weekly_content)
        
        # Save individual weekly file
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
            
            # Get calendar dates for the week
            calendar_dates = self.get_cfm_2026_dates(week_number)
            
            # Clean the scripture reference for filename
            clean_scripture = weekly_content.date_range.replace('–', '_').replace(' ', '_').replace(',', '').replace(':', '').replace(';', '')
            
            # Create filename with calendar dates and scripture reference
            bundle_file = output_path / f"week_{week_number:02d}_{calendar_dates}_{clean_scripture}.json"
            
            with open(bundle_file, 'w', encoding='utf-8') as f:
                json.dump(weekly_content.to_dict(), f, indent=2, ensure_ascii=False)
            
            logger.info(f"💾 Saved unified bundle: {bundle_file}")
        
        logger.info(f"✅ Built unified content for Week {week_number}")
        logger.info(f"   📅 {weekly_content.date_range}")
        logger.info(f"   📖 {weekly_content.title}")
        logger.info(f"   📚 Sources: {weekly_content.total_sources}")
        logger.info(f"   📊 Total content: {weekly_content.total_content_length:,} characters")
    
    def build_all_weeks(self, output_dir: str = "../content/unified_bundles"):
        """Build unified content for all available weeks"""
        logger.info("Building unified content for all weeks...")
        
        all_content = self.load_all_content()
        cfm_weeks = list(all_content.get('cfm', {}).keys())
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        for week_num in cfm_weeks:
            weekly_content = self.build_weekly_content(week_num, all_content)
            if weekly_content:
                self.dataset.add_week(weekly_content)
                
                # Save individual weekly file
                # Get calendar dates for the week
                calendar_dates = self.get_cfm_2026_dates(week_num)
                
                # Clean the scripture reference for filename
                clean_scripture = weekly_content.date_range.replace('–', '_').replace(' ', '_').replace(',', '').replace(':', '').replace(';', '')
                
                # Create filename with calendar dates and scripture reference
                bundle_file = output_path / f"week_{week_num:02d}_{calendar_dates}_{clean_scripture}.json"
                
                with open(bundle_file, 'w', encoding='utf-8') as f:
                    json.dump(weekly_content.to_dict(), f, indent=2, ensure_ascii=False)
        
        # Save complete dataset
        dataset_file = output_path / "unified_cfm_dataset.json"
        self.dataset.save_to_file(str(dataset_file))
        
        logger.info(f"✅ Built unified content for {len(self.dataset.weekly_content)} weeks")
        logger.info(f"💾 Complete dataset: {dataset_file}")

    def get_cfm_2026_dates(self, week_number: int) -> str:
        """Get calendar dates for CFM 2026 weeks starting from Week 2"""
        from datetime import datetime, timedelta
        
        # CFM 2026 starts with Week 2 on January 6, 2026 (first full week of January)
        week_2_start = datetime(2026, 1, 6)  # Monday, January 6, 2026
        
        # Calculate the start date for the requested week
        weeks_offset = week_number - 2  # Week 2 is our baseline (offset 0)
        week_start = week_2_start + timedelta(weeks=weeks_offset)
        week_end = week_start + timedelta(days=6)  # Sunday
        
        # Format as "Jan_6-12"
        start_month = week_start.strftime("%b")
        start_day = week_start.day
        end_day = week_end.day
        
        # Handle month transitions
        if week_start.month == week_end.month:
            return f"{start_month}_{start_day}-{end_day}"
        else:
            end_month = week_end.strftime("%b")
            return f"{start_month}_{start_day}-{end_month}_{end_day}"

def main():
    parser = argparse.ArgumentParser(description="Unified CFM Content Pipeline")
    parser.add_argument("--week", type=int, help="Build content for specific week")
    parser.add_argument("--build-all", action="store_true", help="Build content for all weeks")
    parser.add_argument("--output-dir", default="../content/unified_bundles", 
                       help="Output directory for unified content")
    
    args = parser.parse_args()
    
    pipeline = CFM2026Pipeline()
    
    if args.week:
        pipeline.build_week(args.week, args.output_dir)
    elif args.build_all:
        pipeline.build_all_weeks(args.output_dir)
    else:
        # Default: build week 2
        pipeline.build_week(2, args.output_dir)

if __name__ == "__main__":
    main()