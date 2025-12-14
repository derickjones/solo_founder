"""
CFM 2026 Old Testament Configuration and Pipeline
"""

from .config import get_cfm_2026_config
from .pipeline import CFM2026Pipeline

__all__ = ['CFM2026Pipeline', 'get_cfm_2026_config']