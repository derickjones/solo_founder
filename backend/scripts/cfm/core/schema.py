#!/usr/bin/env python3
"""
Shared schema definitions for CFM pipeline system
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from datetime import date

class CFMStandardWork(Enum):
    """Standard Works covered in CFM rotation"""
    DOCTRINE_COVENANTS = "doctrine_covenants"
    OLD_TESTAMENT = "old_testament"
    BOOK_OF_MORMON = "book_of_mormon"  
    NEW_TESTAMENT = "new_testament"

class ContentSourceType(Enum):
    """Types of content sources for CFM bundles"""
    CFM_MANUAL = "cfm_manual"
    SCRIPTURE = "scripture"
    SEMINARY_TEACHER = "seminary_teacher"
    SEMINARY_STUDENT = "seminary_student"

@dataclass
class ScriptureReference:
    """Scripture reference with book, chapter, and verse range"""
    book: str
    start_chapter: int
    end_chapter: Optional[int] = None
    start_verse: Optional[int] = None
    end_verse: Optional[int] = None
    
    def __str__(self) -> str:
        if self.end_chapter and self.end_chapter != self.start_chapter:
            return f"{self.book} {self.start_chapter}–{self.end_chapter}"
        return f"{self.book} {self.start_chapter}"

@dataclass 
class ContentSource:
    """A single content source within a weekly bundle"""
    source_type: ContentSourceType
    title: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    character_count: int = 0
    
    def __post_init__(self):
        if self.character_count == 0:
            self.character_count = len(self.content)

@dataclass
class WeeklyBundle:
    """Complete CFM content bundle for a specific week"""
    week_number: int
    title: str
    scripture_references: List[ScriptureReference] = field(default_factory=list)
    date_range: str = ""
    sources: List[ContentSource] = field(default_factory=list)
    total_characters: int = 0
    
    def __post_init__(self):
        if self.total_characters == 0:
            self.total_characters = sum(source.character_count for source in self.sources)
    
    def get_filename(self) -> str:
        """Generate filename for this bundle"""
        scripture_ref = "_".join(str(ref).replace(" ", "_") for ref in self.scripture_references)
        if self.date_range:
            # Convert date range to filename-safe format
            date_part = self.date_range.replace("–", "-").replace(" ", "_").replace(",", "")
            return f"week_{self.week_number:02d}_{date_part}_{scripture_ref}.json"
        return f"week_{self.week_number:02d}_{scripture_ref}.json"

@dataclass
class CFMScheduleWeek:
    """Schedule information for a CFM week"""
    week_number: int
    start_date: date
    end_date: date
    title: str
    scripture_references: List[ScriptureReference] = field(default_factory=list)
    
    @property 
    def date_range_str(self) -> str:
        """Format date range as string"""
        start_month = self.start_date.strftime("%B")
        end_month = self.end_date.strftime("%B")
        
        if start_month == end_month:
            return f"{start_month} {self.start_date.day}–{self.end_date.day}"
        else:
            return f"{start_month} {self.start_date.day}–{end_month} {self.end_date.day}"

@dataclass
class CFMYear:
    """Configuration for a specific CFM year"""
    year: int
    standard_work: CFMStandardWork
    title: str
    start_date: date
    seminary_mapping: Dict[int, List[int]] = field(default_factory=dict)
    schedule: List[CFMScheduleWeek] = field(default_factory=list)
    
    def get_week_by_number(self, week_number: int) -> Optional[CFMScheduleWeek]:
        """Get schedule week by week number"""
        for week in self.schedule:
            if week.week_number == week_number:
                return week
        return None

@dataclass
class CFMDataset:
    """Complete dataset for a CFM year"""
    year_config: CFMYear
    weekly_bundles: Dict[int, WeeklyBundle] = field(default_factory=dict)
    
    def get_total_characters(self) -> int:
        """Get total characters across all bundles"""
        return sum(bundle.total_characters for bundle in self.weekly_bundles.values())
    
    def get_total_sources(self) -> int:
        """Get total number of sources across all bundles"""
        return sum(len(bundle.sources) for bundle in self.weekly_bundles.values())