#!/usr/bin/env python3
"""
Unified CFM Content Schema - Simple comprehensive structure
Single pipeline compiles all sources - API handles response generation
"""

from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Any
import json
from datetime import datetime

@dataclass
class ScriptureReference:
    """Scripture reference with book, chapters, verses"""
    book: str
    chapters: List[str]
    verses: Optional[List[str]] = None
    book_type: str = "old_testament"

@dataclass
class ContentSource:
    """Individual source of content"""
    source_type: str  # "cfm", "seminary_teacher"
    title: str
    content: str
    url: Optional[str] = None
    purpose: Optional[str] = None

@dataclass
class WeeklyContent:
    """Comprehensive weekly content bundle"""
    week_number: int
    date_range: str
    title: str
    primary_scriptures: List[ScriptureReference]
    
    # All content combined
    all_content: str = ""  # Combined text from all sources
    content_sources: List[ContentSource] = field(default_factory=list)
    
    # Full scripture text
    scripture_content: Dict[str, Any] = field(default_factory=dict)
    
    # Extracted elements for API use
    subsections: List[Dict[str, Any]] = field(default_factory=list)
    teaching_ideas: List[str] = field(default_factory=list)
    discussion_questions: List[str] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    cross_references: List[ScriptureReference] = field(default_factory=list)
    doctrinal_mastery: List[str] = field(default_factory=list)
    
    # Statistics
    total_content_length: int = 0
    total_sources: int = 0
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def add_content_source(self, source: ContentSource):
        """Add a content source and update combined content"""
        self.content_sources.append(source)
        self.all_content += f"\n\n--- {source.source_type.upper()}: {source.title} ---\n{source.content}"
        self.total_sources = len(self.content_sources)
        self.total_content_length = len(self.all_content)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

@dataclass
class CFMDataset:
    """Complete unified CFM dataset"""
    year: int = 2026
    testament: str = "Old Testament"
    total_weeks: int = 48
    weekly_content: Dict[int, WeeklyContent] = field(default_factory=dict)
    generated_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def add_week(self, week_content: WeeklyContent):
        """Add weekly content to the dataset"""
        self.weekly_content[week_content.week_number] = week_content
    
    def get_week(self, week_number: int) -> Optional[WeeklyContent]:
        """Get content for a specific week"""
        return self.weekly_content.get(week_number)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def save_to_file(self, filepath: str):
        """Save dataset to JSON file"""
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())
    
    @classmethod
    def from_json_file(cls, filepath: str) -> 'CFMDataset':
        """Load dataset from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        dataset = cls(
            year=data.get('year', 2026),
            testament=data.get('testament', 'Old Testament'),
            total_weeks=data.get('total_weeks', 48),
            generated_at=data.get('generated_at', datetime.utcnow().isoformat())
        )
        
        # Convert weekly content
        for week_num, week_data in data.get('weekly_content', {}).items():
            week_content = WeeklyContent(
                week_number=week_data['week_number'],
                date_range=week_data['date_range'],
                title=week_data['title'],
                primary_scriptures=[ScriptureReference(**ref) for ref in week_data.get('primary_scriptures', [])],
                all_content=week_data.get('all_content', ''),
                content_sources=[ContentSource(**source) for source in week_data.get('content_sources', [])],
                scripture_content=week_data.get('scripture_content', {}),
                subsections=week_data.get('subsections', []),
                teaching_ideas=week_data.get('teaching_ideas', []),
                discussion_questions=week_data.get('discussion_questions', []),
                themes=week_data.get('themes', []),
                cross_references=[ScriptureReference(**ref) for ref in week_data.get('cross_references', [])],
                doctrinal_mastery=week_data.get('doctrinal_mastery', []),
                total_content_length=week_data.get('total_content_length', 0),
                total_sources=week_data.get('total_sources', 0),
                generated_at=week_data.get('generated_at', datetime.utcnow().isoformat())
            )
            dataset.add_week(week_content)
        
        return dataset