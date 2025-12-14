#!/usr/bin/env python3
"""
Content Loader - Utilities for loading various content sources
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class ContentLoader:
    """Loads and manages various content sources for CFM pipeline"""
    
    def __init__(self, content_dir: str = "../content"):
        """
        Initialize content loader
        
        Args:
            content_dir: Path to content directory containing source files
        """
        self.content_dir = Path(content_dir)
        self._content_cache = {}
    
    def load_json_file(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Load JSON file from content directory
        
        Args:
            filename: Name of JSON file to load
            
        Returns:
            Loaded JSON data or None if file not found
        """
        if filename in self._content_cache:
            return self._content_cache[filename]
            
        filepath = self.content_dir / filename
        if not filepath.exists():
            logger.warning(f"Content file not found: {filepath}")
            return None
            
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self._content_cache[filename] = data
                logger.info(f"Loaded content file: {filename}")
                return data
        except Exception as e:
            logger.error(f"Error loading {filename}: {e}")
            return None
    
    def load_cfm_content(self, year: int) -> Dict[int, Dict[str, Any]]:
        """
        Load CFM manual content for a specific year
        
        Args:
            year: CFM year to load
            
        Returns:
            Dictionary mapping week numbers to CFM lesson content
        """
        filename = f"cfm_{year}_basic.json"
        cfm_data = self.load_json_file(filename)
        
        if not cfm_data:
            return {}
            
        content = {}
        for lesson in cfm_data.get('lessons', []):
            week_num = lesson.get('week_number')
            if week_num:
                content[week_num] = lesson
                
        logger.info(f"Loaded {len(content)} CFM lessons for {year}")
        return content
    
    def load_seminary_teacher_content(self, year: int) -> Dict[int, List[Dict[str, Any]]]:
        """
        Load Seminary Teacher content mapped to CFM weeks
        
        Args:
            year: CFM year to load
            
        Returns:
            Dictionary mapping CFM week numbers to Seminary Teacher lessons
        """
        filename = f"seminary_teacher_{year}_enhanced.json"
        seminary_data = self.load_json_file(filename)
        
        if not seminary_data:
            return {}
            
        content = seminary_data.get('cfm_weeks', {})
        # Convert string keys to integers
        content = {int(k): v for k, v in content.items() if k.isdigit()}
        
        logger.info(f"Loaded Seminary Teacher content for {len(content)} CFM weeks")
        return content
    
    def load_scripture_content(self, standard_work: str) -> Dict[str, Any]:
        """
        Load scripture content for a standard work
        
        Args:
            standard_work: Name of standard work ('old_testament', 'book_of_mormon', etc.)
            
        Returns:
            Scripture content organized by book/chapter/verse
        """
        filename = f"{standard_work}.json"
        scripture_data = self.load_json_file(filename)
        
        if not scripture_data:
            return {}
            
        # Convert verse list to book/chapter structure if needed
        if isinstance(scripture_data, list):
            organized_content = {}
            for verse_data in scripture_data:
                book = verse_data.get('book')
                chapter = verse_data.get('chapter') 
                verse = verse_data.get('verse')
                
                if book and chapter is not None and verse is not None:
                    if book not in organized_content:
                        organized_content[book] = {}
                    if chapter not in organized_content[book]:
                        organized_content[book][chapter] = {'verses': {}}
                    
                    organized_content[book][chapter]['verses'][verse] = {
                        'text': verse_data.get('content', ''),
                        'citation': verse_data.get('citation', '')
                    }
            
            books = len(organized_content)
            logger.info(f"Loaded {standard_work} content for {books} books")
            return organized_content
        
        # Already organized content
        return scripture_data
    
    def extract_scripture_text(self, book: str, start_chapter: int, 
                              end_chapter: Optional[int] = None,
                              scripture_content: Optional[Dict] = None) -> str:
        """
        Extract scripture text for specified book and chapters
        
        Args:
            book: Book name
            start_chapter: Starting chapter number
            end_chapter: Ending chapter number (optional)
            scripture_content: Pre-loaded scripture content (optional)
            
        Returns:
            Complete scripture text for the specified range
        """
        if not scripture_content:
            return ""
            
        if book not in scripture_content:
            logger.warning(f"Book '{book}' not found in scripture content")
            return ""
        
        end_chapter = end_chapter or start_chapter
        full_text = []
        
        for chapter_num in range(start_chapter, end_chapter + 1):
            if chapter_num not in scripture_content[book]:
                logger.warning(f"Chapter {chapter_num} not found in {book}")
                continue
                
            chapter_data = scripture_content[book][chapter_num]
            verses = chapter_data.get('verses', {})
            
            chapter_text = f"\n=== {book} {chapter_num} ===\n"
            for verse_num in sorted(verses.keys(), key=int):
                verse_data = verses[verse_num]
                verse_text = verse_data.get('text', '')
                chapter_text += f"{verse_num}. {verse_text}\n"
            
            full_text.append(chapter_text)
        
        return "\n".join(full_text)
    
    def clear_cache(self):
        """Clear the content cache"""
        self._content_cache.clear()
        logger.info("Content cache cleared")