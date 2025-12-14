#!/usr/bin/env python3
"""
CFM Content Generator - Unified CLI for all CFM years
"""

import argparse
import sys
from pathlib import Path
from factory import create_cfm_pipeline, get_available_years

def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate CFM content bundles for any year"
    )
    
    parser.add_argument(
        "--year", 
        type=int, 
        choices=get_available_years(),
        default=2026,
        help="CFM year to generate content for"
    )
    
    parser.add_argument(
        "--week", 
        type=int, 
        help="Build content for specific week"
    )
    
    parser.add_argument(
        "--build-all", 
        action="store_true", 
        help="Build content for all weeks"
    )
    
    parser.add_argument(
        "--output-dir", 
        default="../content/bundles", 
        help="Output directory for generated content"
    )
    
    args = parser.parse_args()
    
    try:
        pipeline = create_cfm_pipeline(args.year)
        
        output_dir = f"{args.output_dir}/cfm_{args.year}"
        
        if args.week:
            pipeline.build_week(args.week, output_dir)
        elif args.build_all:
            pipeline.build_all_weeks(output_dir)
        else:
            # Default: build week 2 (first CFM week)
            pipeline.build_week(2, output_dir)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()