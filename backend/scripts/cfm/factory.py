#!/usr/bin/env python3
"""
CFM Pipeline Factory - Creates appropriate pipeline based on year
"""

import sys
from pathlib import Path
from typing import Optional

# Add year-specific modules to path
sys.path.append(str(Path(__file__).parent / 'years' / 'cfm_2026'))

def create_cfm_pipeline(year: int):
    """Create appropriate CFM pipeline based on year"""
    if year == 2026:
        from pipeline import CFM2026Pipeline
        return CFM2026Pipeline()
    else:
        raise ValueError(f"No pipeline available for year {year}")

def get_available_years():
    """Get list of available CFM years"""
    return [2026]  # Add more as implemented