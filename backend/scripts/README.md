# Scripts Directory Organization

The `/backend/scripts` directory has been organized into a modular structure that supports multiple CFM years and maintains all existing functionality.

## Directory Structure

```
scripts/
├── cfm/                              # Modular CFM system
│   ├── core/                         # Shared CFM infrastructure
│   │   ├── __init__.py
│   │   ├── base_pipeline.py         # Abstract base class for all CFM years
│   │   ├── schema.py                # Common data classes and schemas
│   │   ├── date_calculator.py       # CFM date calculation utilities
│   │   └── content_loader.py        # Content loading mechanisms
│   ├── years/                       # Year-specific configurations
│   │   └── cfm_2026/               # CFM 2026 Old Testament
│   │       ├── __init__.py
│   │       ├── config.py           # CFM 2026 schedule and configuration
│   │       ├── pipeline.py         # CFM2026Pipeline class
│   │       ├── display.py          # Display utilities
│   │       └── legacy_schema.py    # Original schema for reference
│   ├── factory.py                   # Pipeline factory for year selection
│   └── generate_cfm.py             # Unified CLI for all CFM years
├── scrapers/                        # All content scrapers
│   ├── README.md                   # Scraper documentation
│   ├── master_scraper.py          # Scraper coordinator
│   ├── scrape_cfm.py              # Come Follow Me scraper
│   ├── scrape_seminary.py         # Seminary Teacher scraper
│   ├── scrape_old_testament.py    # Old Testament scraper
│   ├── scrape_new_testament.py    # New Testament scraper
│   ├── scrape_book_of_mormon.py   # Book of Mormon scraper
│   ├── scrape_doctrine_covenants.py # D&C scraper
│   ├── scrape_pearl_great_price.py # Pearl of Great Price scraper
│   ├── scrape_general_conference.py # General Conference scraper
│   └── scrape_study_helps.py      # Study helps scraper
├── content/                         # Organized content storage
│   ├── sources/                    # Raw scraped content
│   │   ├── cfm_2026_basic.json
│   │   ├── seminary_teacher_2026_enhanced.json
│   │   ├── old_testament.json
│   │   ├── pearl_of_great_price.json
│   │   └── ...
│   └── bundles/                    # Generated CFM bundles by year
│       └── cfm_2026/
│           └── old_testament_bundles/  # Your existing 51 weekly bundles
│               ├── week_02_Jan_6-12_Abraham_3_Moses_1.json
│               ├── week_03_Jan_13-19_Genesis_1-2_Moses_2-3.json
│               └── ... (all 51 weeks)
├── cfm_2026_old_testament/         # Original working directory (preserved)
└── requirements.txt
```

## Key Features

### 🏗️ **Modular Architecture**
- **Core Infrastructure**: Shared base classes, schemas, and utilities
- **Year-Specific**: Each CFM year has its own configuration and pipeline
- **Factory Pattern**: Easy instantiation of appropriate pipeline by year

### 📚 **Organized Scrapers**
- All scripture and CFM scrapers in one directory
- Master scraper coordinator for easy execution
- Clear documentation and usage instructions

### 🗂️ **Content Organization**
- **Sources**: Raw scraped content files
- **Bundles**: Generated CFM content organized by year
- **Preserved Work**: All your existing 51 weekly bundles maintained

### 🚀 **Easy Usage**

```bash
# Generate CFM content for any year
python cfm/generate_cfm.py --year 2026 --build-all

# Run specific scrapers
python scrapers/master_scraper.py seminary
python scrapers/master_scraper.py old_testament

# Use existing 2026 pipeline directly
python cfm/years/cfm_2026/pipeline.py --week 5
```

## Migration Status

✅ **All existing functionality preserved**
✅ **51 weekly CFM 2026 bundles maintained**  
✅ **208 Seminary Teacher lessons preserved**
✅ **All scripture scrapers organized**
✅ **Modular structure ready for future years**

## Future Years

Adding new CFM years is now simple:
1. Create `/cfm/years/cfm_YYYY/` directory
2. Add configuration in `config.py`
3. Create `CFMYYYYP pipeline.py` inheriting from `BaseCFMPipeline`
4. Update factory.py to include the new year

Your working pipeline is preserved and organized for scalability!