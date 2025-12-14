#!/usr/bin/env python3
"""
CFM Date Calculator - Handles date calculations for CFM years
"""

from datetime import date, timedelta
from typing import List, Tuple
from .schema import CFMScheduleWeek

class CFMDateCalculator:
    """Calculates CFM weekly date ranges for any year"""
    
    def __init__(self, year: int, start_date: date):
        """
        Initialize calculator for a specific CFM year
        
        Args:
            year: CFM year (e.g., 2026)
            start_date: Date when Week 1 begins (usually first Sunday of January)
        """
        self.year = year
        self.start_date = start_date
    
    def get_week_dates(self, week_number: int) -> Tuple[date, date]:
        """
        Get start and end dates for a specific CFM week
        
        Args:
            week_number: Week number (1-52)
            
        Returns:
            Tuple of (start_date, end_date) for the week
        """
        # CFM weeks run Sunday to Saturday
        week_start = self.start_date + timedelta(weeks=week_number - 1)
        week_end = week_start + timedelta(days=6)
        return week_start, week_end
    
    def format_date_range(self, start_date: date, end_date: date) -> str:
        """
        Format date range as string (e.g., "January 6-12" or "January 27-February 2")
        
        Args:
            start_date: Week start date
            end_date: Week end date
            
        Returns:
            Formatted date range string
        """
        start_month = start_date.strftime("%B")
        end_month = end_date.strftime("%B")
        
        if start_month == end_month:
            # Same month: "January 6-12"
            return f"{start_month} {start_date.day}-{end_date.day}"
        else:
            # Different months: "January 27-February 2"  
            return f"{start_month} {start_date.day}-{end_month} {end_date.day}"
    
    def get_week_date_range_str(self, week_number: int) -> str:
        """
        Get formatted date range string for a CFM week
        
        Args:
            week_number: Week number (1-52)
            
        Returns:
            Formatted date range string
        """
        start_date, end_date = self.get_week_dates(week_number)
        return self.format_date_range(start_date, end_date)
    
    def generate_schedule_weeks(self, week_configs: List[dict]) -> List[CFMScheduleWeek]:
        """
        Generate CFMScheduleWeek objects with calculated dates
        
        Args:
            week_configs: List of week configuration dicts with week_number, title, etc.
            
        Returns:
            List of CFMScheduleWeek objects with calculated dates
        """
        schedule_weeks = []
        
        for config in week_configs:
            week_number = config['week_number']
            start_date, end_date = self.get_week_dates(week_number)
            
            schedule_week = CFMScheduleWeek(
                week_number=week_number,
                start_date=start_date,
                end_date=end_date,
                title=config['title'],
                scripture_references=config.get('scripture_references', [])
            )
            schedule_weeks.append(schedule_week)
            
        return schedule_weeks

# Standard CFM start dates for common years
CFM_START_DATES = {
    2025: date(2025, 1, 5),   # First Sunday of January 2025
    2026: date(2026, 1, 4),   # First Sunday of January 2026  
    2027: date(2027, 1, 3),   # First Sunday of January 2027
    2028: date(2028, 1, 2),   # First Sunday of January 2028
}