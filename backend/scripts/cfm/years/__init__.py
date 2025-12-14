"""
CFM Years Module - Year-specific configurations and pipelines
"""

from .cfm_2026 import CFM2026Pipeline, get_cfm_2026_config
from .cfm_2025 import CFM2025Pipeline, get_cfm_2025_config  
from .cfm_2027 import CFM2027Pipeline, get_cfm_2027_config
from .cfm_2028 import CFM2028Pipeline, get_cfm_2028_config

# Registry of available CFM years
CFM_YEAR_REGISTRY = {
    2025: {
        'pipeline_class': CFM2025Pipeline,
        'config_function': get_cfm_2025_config,
        'title': 'Doctrine and Covenants 2025'
    },
    2026: {
        'pipeline_class': CFM2026Pipeline, 
        'config_function': get_cfm_2026_config,
        'title': 'Old Testament 2026'
    },
    2027: {
        'pipeline_class': CFM2027Pipeline,
        'config_function': get_cfm_2027_config, 
        'title': 'Book of Mormon 2027'
    },
    2028: {
        'pipeline_class': CFM2028Pipeline,
        'config_function': get_cfm_2028_config,
        'title': 'New Testament 2028'
    }
}

__all__ = [
    'CFM2025Pipeline', 'get_cfm_2025_config',
    'CFM2026Pipeline', 'get_cfm_2026_config', 
    'CFM2027Pipeline', 'get_cfm_2027_config',
    'CFM2028Pipeline', 'get_cfm_2028_config',
    'CFM_YEAR_REGISTRY'
]