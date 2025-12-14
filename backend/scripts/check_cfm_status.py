#!/usr/bin/env python3
"""
Simple CFM Bundle Status Checker
Quickly check if all 51 weeks of CFM 2026 bundles exist.
"""

import glob
import json
from pathlib import Path

def main():
    """Quick status check of all CFM bundles"""
    bundle_dir = "content/bundles/cfm_2026/old_testament_bundles"
    
    if not Path(bundle_dir).exists():
        print("❌ CFM 2026 bundle directory not found")
        print(f"   Expected: {bundle_dir}")
        return
    
    # Check for all 51 weeks (2-52, since there's no week 1 in Old Testament)
    expected_weeks = set(range(2, 53))
    found_weeks = set()
    
    bundle_files = glob.glob(f"{bundle_dir}/week_*.json")
    
    for file_path in bundle_files:
        try:
            # Extract week number from filename (e.g., week_02_Jan_6-12_Moses 1.json -> 2)
            filename = Path(file_path).name
            if filename.startswith("week_"):
                week_str = filename.split("_")[1]
                week_num = int(week_str)
                found_weeks.add(week_num)
        except (ValueError, IndexError):
            continue
    
    missing_weeks = expected_weeks - found_weeks
    extra_weeks = found_weeks - expected_weeks
    
    print(f"📊 CFM 2026 Old Testament Bundle Status:")
    print(f"   ✅ Found: {len(found_weeks)}/51 weeks")
    
    if missing_weeks:
        missing_list = sorted(missing_weeks)
        if len(missing_list) <= 10:
            print(f"   ❌ Missing: {missing_list}")
        else:
            print(f"   ❌ Missing: {len(missing_list)} weeks (first 10: {missing_list[:10]}...)")
    
    if extra_weeks:
        print(f"   ⚠️  Extra: {sorted(extra_weeks)}")
    
    if len(found_weeks) == 51 and not missing_weeks:
        print("   🎉 All CFM 2026 Old Testament bundles are present!")
    
    # For detailed analysis, use the API:
    print("\n💡 For detailed bundle analysis, use the CFM Deep Dive API:")
    print("   curl -X POST 'https://gospel-guide-api-273320302933.us-central1.run.app/cfm/deep-dive' \\")
    print("        -H 'Content-Type: application/json' \\") 
    print("        -d '{\"week_number\": 3, \"study_level\": \"basic\"}'")

if __name__ == "__main__":
    main()