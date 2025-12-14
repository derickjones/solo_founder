# Scripture Scrapers

This directory contains all scripture and CFM content scrapers organized in a modular structure.

## Available Scrapers

- `scrape_old_testament.py` - Old Testament scriptures
- `scrape_new_testament.py` - New Testament scriptures  
- `scrape_book_of_mormon.py` - Book of Mormon scriptures
- `scrape_doctrine_covenants.py` - Doctrine & Covenants
- `scrape_pearl_great_price.py` - Pearl of Great Price
- `scrape_general_conference.py` - General Conference talks
- `scrape_cfm.py` - Come Follow Me lessons
- `scrape_seminary.py` - Seminary Teacher lessons

## Master Scraper

Use `master_scraper.py` to run any individual scraper:

```bash
python master_scraper.py old_testament
python master_scraper.py cfm
python master_scraper.py seminary
```

## Output

All scraped content is saved to `../content/sources/`