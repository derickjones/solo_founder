#!/usr/bin/env python3
"""
Base CFM Pipeline - Abstract base class for year-specific pipelines
"""

import json
import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Optional

from .schema import CFMYear, WeeklyBundle, CFMDataset, ContentSource, ContentSourceType
from .date_calculator import CFMDateCalculator
from .content_loader import ContentLoader

logger = logging.getLogger(__name__)

class BaseCFMPipeline(ABC):
    """Abstract base class for CFM content pipelines"""
    
    def __init__(self, year_config: CFMYear, content_dir: str = "../content"):
        """
        Initialize pipeline with year configuration
        
        Args:
            year_config: CFM year configuration
            content_dir: Path to content directory
        """
        self.year_config = year_config
        self.content_dir = Path(content_dir)
        self.content_loader = ContentLoader(content_dir)
        self.date_calculator = CFMDateCalculator(year_config.year, year_config.start_date)
        self.dataset = CFMDataset(year_config=year_config)
    
    @abstractmethod
    def load_content_sources(self) -> Dict[str, Dict]:
        """
        Load all required content sources for this CFM year
        Must be implemented by year-specific pipelines
        
        Returns:
            Dictionary of loaded content sources
        """
        pass
    
    @abstractmethod  
    def get_week_scripture_references(self, week_number: int) -> List[str]:
        """
        Get scripture references for a specific week
        Must be implemented by year-specific pipelines
        
        Args:
            week_number: CFM week number
            
        Returns:
            List of scripture reference strings for the week
        """
        pass
    
    def create_weekly_bundle(self, week_number: int, content_sources: Dict[str, Dict]) -> Optional[WeeklyBundle]:
        """
        Create a complete weekly bundle for a CFM week
        
        Args:
            week_number: CFM week number
            content_sources: Loaded content sources
            
        Returns:
            WeeklyBundle object or None if week not found
        """
        schedule_week = self.year_config.get_week_by_number(week_number)
        if not schedule_week:
            logger.warning(f"No schedule found for week {week_number}")
            return None
        
        # Create bundle with basic info
        bundle = WeeklyBundle(
            week_number=week_number,
            title=schedule_week.title,
            scripture_references=schedule_week.scripture_references,
            date_range=schedule_week.date_range_str
        )
        
        # Add CFM manual content
        cfm_content = content_sources.get('cfm', {})
        if week_number in cfm_content:
            cfm_lesson = cfm_content[week_number]
            cfm_source = ContentSource(
                source_type=ContentSourceType.CFM_MANUAL,
                title=cfm_lesson.get('lesson_title', f'Week {week_number}'),
                content=cfm_lesson.get('content', ''),
                metadata=cfm_lesson
            )
            bundle.sources.append(cfm_source)
        
        # Add scripture content
        self._add_scripture_content(bundle, content_sources)
        
        # Add Seminary Teacher content
        self._add_seminary_content(bundle, content_sources)
        
        # Update total character count
        bundle.total_characters = sum(source.character_count for source in bundle.sources)
        
        return bundle
    
    def _add_scripture_content(self, bundle: WeeklyBundle, content_sources: Dict[str, Dict]):
        """Add scripture content to bundle"""
        scripture_content = content_sources.get('scripture', {})
        if not scripture_content:
            return
            
        for ref in bundle.scripture_references:
            if hasattr(ref, 'book'):  # ScriptureReference object
                text = self.content_loader.extract_scripture_text(
                    ref.book, ref.start_chapter, ref.end_chapter, scripture_content
                )
                if text:
                    scripture_source = ContentSource(
                        source_type=ContentSourceType.SCRIPTURE,
                        title=str(ref),
                        content=text,
                        metadata={'book': ref.book, 'chapter_range': f"{ref.start_chapter}-{ref.end_chapter or ref.start_chapter}"}
                    )
                    bundle.sources.append(scripture_source)
    
    def _add_seminary_content(self, bundle: WeeklyBundle, content_sources: Dict[str, Dict]):
        """Add Seminary Teacher content to bundle"""
        seminary_content = content_sources.get('seminary_teacher', {})
        if bundle.week_number in seminary_content:
            seminary_lessons = seminary_content[bundle.week_number]
            
            for lesson in seminary_lessons:
                seminary_source = ContentSource(
                    source_type=ContentSourceType.SEMINARY_TEACHER,
                    title=lesson.get('title', f'Seminary Lesson'),
                    content=lesson.get('content', ''),
                    metadata=lesson
                )
                bundle.sources.append(seminary_source)
    
    def generate_all_bundles(self) -> CFMDataset:
        """
        Generate all weekly bundles for the CFM year
        
        Returns:
            Complete CFMDataset with all weekly bundles
        """
        logger.info(f"Generating CFM bundles for {self.year_config.year} ({self.year_config.title})")
        
        # Load all content sources
        content_sources = self.load_content_sources()
        
        # Generate bundles for each scheduled week
        for schedule_week in self.year_config.schedule:
            bundle = self.create_weekly_bundle(schedule_week.week_number, content_sources)
            if bundle:
                self.dataset.weekly_bundles[schedule_week.week_number] = bundle
                logger.info(f"Generated Week {schedule_week.week_number}: {bundle.total_characters} chars, {len(bundle.sources)} sources")
        
        total_bundles = len(self.dataset.weekly_bundles)
        total_chars = self.dataset.get_total_characters()
        total_sources = self.dataset.get_total_sources()
        
        logger.info(f"✅ Generated {total_bundles} CFM bundles: {total_chars:,} chars, {total_sources} sources")
        
        return self.dataset
    
    def save_bundles(self, output_dir: str):
        """
        Save all weekly bundles to individual JSON files
        
        Args:
            output_dir: Directory to save bundle files
        """
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Save individual weekly bundles
        for week_number, bundle in self.dataset.weekly_bundles.items():
            filename = bundle.get_filename()
            filepath = output_path / filename
            
            # Convert bundle to dict for JSON serialization
            bundle_data = {
                'week_number': bundle.week_number,
                'title': bundle.title,
                'date_range': bundle.date_range,
                'scripture_references': [str(ref) for ref in bundle.scripture_references],
                'total_characters': bundle.total_characters,
                'sources': [
                    {
                        'source_type': source.source_type.value,
                        'title': source.title,
                        'content': source.content,
                        'character_count': source.character_count,
                        'metadata': source.metadata
                    }
                    for source in bundle.sources
                ]
            }
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(bundle_data, f, indent=2, ensure_ascii=False)
            
            logger.debug(f"Saved {filename}")
        
        # Save unified dataset
        unified_filename = f"unified_cfm_{self.year_config.year}_dataset.json"
        unified_filepath = output_path / unified_filename
        
        unified_data = {
            'year': self.year_config.year,
            'standard_work': self.year_config.standard_work.value,
            'title': self.year_config.title,
            'total_bundles': len(self.dataset.weekly_bundles),
            'total_characters': self.dataset.get_total_characters(),
            'total_sources': self.dataset.get_total_sources(),
            'weekly_bundles': {
                str(week_num): bundle_data
                for week_num, bundle_data in [
                    (week_num, {
                        'week_number': bundle.week_number,
                        'title': bundle.title,
                        'date_range': bundle.date_range,
                        'sources_count': len(bundle.sources),
                        'total_characters': bundle.total_characters
                    })
                    for week_num, bundle in self.dataset.weekly_bundles.items()
                ]
            }
        }
        
        with open(unified_filepath, 'w', encoding='utf-8') as f:
            json.dump(unified_data, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved {len(self.dataset.weekly_bundles)} bundles to {output_dir}")
        logger.info(f"📁 Unified dataset saved as {unified_filename}")