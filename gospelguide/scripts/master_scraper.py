#!/usr/bin/env python3
"""
Master LDS Content Scraper for GospelGuide
Orchestrates all individual scrapers and creates master dataset

Usage:
    python master_scraper.py [options]
    
Examples:
    python master_scraper.py                           # Run all scrapers
    python master_scraper.py --only general-conference # Run only General Conference
    python master_scraper.py --only standard-works     # Run only Standard Works
    python master_scraper.py --skip study-helps        # Skip Study Helps
    python master_scraper.py --test                    # Test mode with limited data
"""

import subprocess
import json
import logging
import argparse
import os
import time
from typing import Dict, List, Optional

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class MasterScraper:
    def __init__(self, test_mode: bool = False):
        self.test_mode = test_mode
        self.content_dir = "content"
        self.scraped_files = []
        
        # Ensure content directory exists
        if not os.path.exists(self.content_dir):
            os.makedirs(self.content_dir)

    def run_all_scrapers(self, skip: List[str] = None, only: List[str] = None):
        """Run all available scrapers"""
        skip = skip or []
        only = only or []
        
        logger.info("=== Starting Master LDS Content Scraping ===")
        if self.test_mode:
            logger.info("🧪 TEST MODE - Limited data will be scraped")
        
        # Define all available scrapers
        scrapers = {
            "standard-works": {
                "description": "All four Standard Works",
                "scripts": {
                    "book-of-mormon": {
                        "script": "scrape_book_of_mormon.py",
                        "args": ["--limit", "500"] if self.test_mode else [],
                        "output": "real_book_of_mormon.json"
                    },
                    "old-testament": {
                        "script": "scrape_old_testament.py", 
                        "args": ["--limit", "300"] if self.test_mode else [],
                        "output": "old_testament.json"
                    },
                    "new-testament": {
                        "script": "scrape_new_testament.py",
                        "args": ["--limit", "300"] if self.test_mode else [],
                        "output": "new_testament.json"
                    },
                    "doctrine-covenants": {
                        "script": "scrape_doctrine_covenants.py",
                        "args": ["--limit", "200"] if self.test_mode else [],
                        "output": "doctrine_covenants.json"
                    },
                    "pearl-great-price": {
                        "script": "scrape_pearl_great_price.py",
                        "args": ["--limit", "100"] if self.test_mode else [],
                        "output": "pearl_of_great_price.json"
                    }
                },
                "action": "run_all_scripts"
            },
            "general-conference": {
                "description": "General Conference talks (2015-2025)",
                "script": "scrape_general_conference.py",
                "args": ["--start-year", "2015"],
                "output": "general_conference.json"
            },
            "study-helps": {
                "description": "Study Helps (Bible Dictionary, Guide to Scriptures, Topical Guide)",
                "script": "scrape_study_helps.py", 
                "args": ["--limit", "50"] if self.test_mode else [],
                "output": "study_helps.json"
            },
            "come-follow-me": {
                "description": "Come Follow Me content (already complete)",
                "files": ["come_follow_me.json"],
                "action": "verify_existing"
            }
        }
        
        # Filter scrapers based on only/skip parameters
        active_scrapers = {}
        for name, config in scrapers.items():
            if only and name not in only:
                continue
            if name in skip:
                continue
            active_scrapers[name] = config
        
        logger.info(f"Active scrapers: {', '.join(active_scrapers.keys())}")
        
        # Run each scraper
        for name, config in active_scrapers.items():
            self._run_scraper(name, config)
        
        # Create master dataset
        self._create_master_dataset()
        
        logger.info("=== Master LDS Content Scraping Complete ===")

    def _run_scraper(self, name: str, config: Dict):
        """Run an individual scraper"""
        logger.info(f"📚 {name.upper()}: {config['description']}")
        
        if config.get("action") == "verify_existing":
            # Check if files already exist
            for filename in config["files"]:
                filepath = os.path.join(self.content_dir, filename)
                if os.path.exists(filepath):
                    logger.info(f"  ✅ {filename} already exists")
                    self.scraped_files.append(filepath)
                else:
                    logger.warning(f"  ❌ {filename} missing - run appropriate scraper")
            return
            
        elif config.get("action") == "run_all_scripts":
            # Run all individual scripts for Standard Works
            for sub_name, sub_config in config["scripts"].items():
                logger.info(f"  📖 Running {sub_name}...")
                try:
                    script_path = sub_config["script"]
                    args = sub_config.get("args", [])
                    
                    cmd = ["python", script_path] + args
                    logger.info(f"    🚀 {' '.join(cmd)}")
                    
                    # Run the scraper
                    result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
                    
                    if result.returncode == 0:
                        output_file = os.path.join(self.content_dir, sub_config["output"])
                        if os.path.exists(output_file):
                            logger.info(f"    ✅ {sub_config['output']} created successfully")
                            self.scraped_files.append(output_file)
                        else:
                            logger.error(f"    ❌ Expected output file {sub_config['output']} not found")
                    else:
                        logger.error(f"    ❌ {sub_name} failed with return code {result.returncode}")
                        if result.stderr:
                            logger.error(f"    Error: {result.stderr}")
                        
                except Exception as e:
                    logger.error(f"    ❌ Error running {sub_name}: {e}")
            return

        # Run Python scraper script
        try:
            script_path = config["script"]
            args = config.get("args", [])
            
            cmd = ["python", script_path] + args
            logger.info(f"  🚀 Running: {' '.join(cmd)}")
            
            # Run the scraper
            result = subprocess.run(cmd, capture_output=True, text=True, cwd=".")
            
            if result.returncode == 0:
                output_file = os.path.join(self.content_dir, config["output"])
                if os.path.exists(output_file):
                    logger.info(f"  ✅ {config['output']} created successfully")
                    self.scraped_files.append(output_file)
                else:
                    logger.error(f"  ❌ Expected output file {config['output']} not found")
            else:
                logger.error(f"  ❌ Scraper failed with return code {result.returncode}")
                logger.error(f"  Error: {result.stderr}")
                
        except Exception as e:
            logger.error(f"  ❌ Error running {name} scraper: {e}")

    def _create_master_dataset(self):
        """Combine all scraped content into master dataset"""
        logger.info("📦 Creating master dataset...")
        
        all_content = []
        file_stats = {}
        
        # Load all individual files
        for filepath in self.scraped_files:
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = json.load(f)
                    
                filename = os.path.basename(filepath)
                file_stats[filename] = len(content)
                all_content.extend(content)
                
                logger.info(f"  📄 {filename}: {len(content):,} items")
                
            except Exception as e:
                logger.error(f"  ❌ Error loading {filepath}: {e}")
        
        # Also check for existing files that weren't just created
        existing_files = [
            "real_book_of_mormon.json",
            "old_testament.json", 
            "new_testament.json",
            "doctrine_covenants.json", 
            "pearl_of_great_price.json",
            "come_follow_me.json"
        ]
        
        for filename in existing_files:
            filepath = os.path.join(self.content_dir, filename)
            if os.path.exists(filepath) and filepath not in self.scraped_files:
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = json.load(f)
                        file_stats[filename] = len(content)
                        all_content.extend(content)
                        logger.info(f"  📄 {filename}: {len(content):,} items (existing)")
                except Exception as e:
                    logger.error(f"  ❌ Error loading existing file {filepath}: {e}")
        
        # Save master dataset
        master_file = os.path.join(self.content_dir, "complete_lds_content.json")
        with open(master_file, 'w', encoding='utf-8') as f:
            json.dump(all_content, f, ensure_ascii=False, indent=2)
        
        logger.info(f"📦 Master dataset saved: {master_file}")
        logger.info(f"📊 Total items: {len(all_content):,}")
        
        # Summary statistics
        logger.info("📈 Content Summary:")
        for filename, count in sorted(file_stats.items()):
            source = filename.replace('.json', '').replace('_', ' ').title()
            logger.info(f"  {source}: {count:,} items")

def main():
    parser = argparse.ArgumentParser(description='Master LDS Content Scraper')
    parser.add_argument('--only', choices=['standard-works', 'general-conference', 'study-helps', 'come-follow-me'], 
                       help='Run only specific scraper')
    parser.add_argument('--skip', action='append', 
                       choices=['standard-works', 'general-conference', 'study-helps', 'come-follow-me'],
                       help='Skip specific scraper (can be used multiple times)')
    parser.add_argument('--test', action='store_true', help='Test mode with limited data')
    
    args = parser.parse_args()
    
    scraper = MasterScraper(test_mode=args.test)
    
    only_list = [args.only] if args.only else []
    skip_list = args.skip or []
    
    scraper.run_all_scrapers(skip=skip_list, only=only_list)

if __name__ == "__main__":
    main()