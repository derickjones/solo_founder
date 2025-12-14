#!/usr/bin/env python3
"""
CFM 2026 Old Testament Configuration
"""

from datetime import date
from ...core.schema import CFMYear, CFMStandardWork, CFMScheduleWeek, ScriptureReference
from ...core.date_calculator import CFM_START_DATES

def get_cfm_2026_config() -> CFMYear:
    """Get CFM 2026 Old Testament configuration"""
    
    # CFM 2026 starts on January 5, 2026 (Week 1, but we start with Week 2)
    start_date = CFM_START_DATES[2026]
    
    # Define the weekly schedule based on your existing bundle structure
    weekly_schedule_config = [
        # Week 2: Abraham 3; Moses 1
        {'week_number': 2, 'title': 'Abraham 3; Moses 1', 'scripture_refs': [
            ScriptureReference('Abraham', 3), ScriptureReference('Moses', 1)
        ]},
        # Week 3: Genesis 1–2; Moses 2–3; Abraham 4–5
        {'week_number': 3, 'title': 'Genesis 1–2; Moses 2–3; Abraham 4–5', 'scripture_refs': [
            ScriptureReference('Genesis', 1, 2), ScriptureReference('Moses', 2, 3), ScriptureReference('Abraham', 4, 5)
        ]},
        # Week 4: Genesis 3–4
        {'week_number': 4, 'title': 'Genesis 3–4', 'scripture_refs': [
            ScriptureReference('Genesis', 3, 4)
        ]},
        # Week 5: Genesis 5; Moses 6
        {'week_number': 5, 'title': 'Genesis 5; Moses 6', 'scripture_refs': [
            ScriptureReference('Genesis', 5), ScriptureReference('Moses', 6)
        ]},
        # Week 6: Moses 7
        {'week_number': 6, 'title': 'Moses 7', 'scripture_refs': [
            ScriptureReference('Moses', 7)
        ]},
        # Week 7: Genesis 6–11; Moses 8
        {'week_number': 7, 'title': 'Genesis 6–11; Moses 8', 'scripture_refs': [
            ScriptureReference('Genesis', 6, 11), ScriptureReference('Moses', 8)
        ]},
        # Week 8: Genesis 12–17; Abraham 1–2
        {'week_number': 8, 'title': 'Genesis 12–17; Abraham 1–2', 'scripture_refs': [
            ScriptureReference('Genesis', 12, 17), ScriptureReference('Abraham', 1, 2)
        ]},
        # Week 9: Genesis 18–23
        {'week_number': 9, 'title': 'Genesis 18–23', 'scripture_refs': [
            ScriptureReference('Genesis', 18, 23)
        ]},
        # Week 10: Genesis 24–33
        {'week_number': 10, 'title': 'Genesis 24–33', 'scripture_refs': [
            ScriptureReference('Genesis', 24, 33)
        ]},
        # Week 11: Genesis 37–41
        {'week_number': 11, 'title': 'Genesis 37–41', 'scripture_refs': [
            ScriptureReference('Genesis', 37, 41)
        ]},
        # Week 12: Genesis 42–50
        {'week_number': 12, 'title': 'Genesis 42–50', 'scripture_refs': [
            ScriptureReference('Genesis', 42, 50)
        ]},
        # Week 13: Exodus 1–6
        {'week_number': 13, 'title': 'Exodus 1–6', 'scripture_refs': [
            ScriptureReference('Exodus', 1, 6)
        ]},
        # Week 14: General Conference
        {'week_number': 14, 'title': 'General Conference', 'scripture_refs': []},
        # Week 15: Exodus 7–13
        {'week_number': 15, 'title': 'Exodus 7–13', 'scripture_refs': [
            ScriptureReference('Exodus', 7, 13)
        ]},
        # Week 16: Exodus 14–18
        {'week_number': 16, 'title': 'Exodus 14–18', 'scripture_refs': [
            ScriptureReference('Exodus', 14, 18)
        ]},
        # Week 17: Exodus 19–20
        {'week_number': 17, 'title': 'Exodus 19–20', 'scripture_refs': [
            ScriptureReference('Exodus', 19, 20)
        ]},
        # Week 18: Exodus 35–40
        {'week_number': 18, 'title': 'Exodus 35–40', 'scripture_refs': [
            ScriptureReference('Exodus', 35, 40)
        ]},
        # Week 19: Numbers 11–14
        {'week_number': 19, 'title': 'Numbers 11–14', 'scripture_refs': [
            ScriptureReference('Numbers', 11, 14)
        ]},
        # Week 20: Deuteronomy 6–8
        {'week_number': 20, 'title': 'Deuteronomy 6–8', 'scripture_refs': [
            ScriptureReference('Deuteronomy', 6, 8)
        ]},
        # Week 21: Joshua 1–8
        {'week_number': 21, 'title': 'Joshua 1–8', 'scripture_refs': [
            ScriptureReference('Joshua', 1, 8)
        ]},
        # Week 22: Judges 2–4
        {'week_number': 22, 'title': 'Judges 2–4', 'scripture_refs': [
            ScriptureReference('Judges', 2, 4)
        ]},
        # Week 23: 1 Samuel 1–7; Ruth
        {'week_number': 23, 'title': '1 Samuel 1–7; Ruth', 'scripture_refs': [
            ScriptureReference('1 Samuel', 1, 7), ScriptureReference('Ruth', 1, 4)
        ]},
        # Week 24: Judges 6–8; 1 Samuel 8–10
        {'week_number': 24, 'title': 'Judges 6–8; 1 Samuel 8–10', 'scripture_refs': [
            ScriptureReference('Judges', 6, 8), ScriptureReference('1 Samuel', 8, 10)
        ]},
        # Week 25: 1 Samuel 17–18
        {'week_number': 25, 'title': '1 Samuel 17–18', 'scripture_refs': [
            ScriptureReference('1 Samuel', 17, 18)
        ]},
        # Week 26: 2 Samuel 11–12
        {'week_number': 26, 'title': '2 Samuel 11–12', 'scripture_refs': [
            ScriptureReference('2 Samuel', 11, 12)
        ]},
        # Week 27: 1 Kings 1–2; 1 Chronicles 13
        {'week_number': 27, 'title': '1 Kings 1–2; 1 Chronicles 13', 'scripture_refs': [
            ScriptureReference('1 Kings', 1, 2), ScriptureReference('1 Chronicles', 13)
        ]},
        # Week 28: 1 Kings 2–7
        {'week_number': 28, 'title': '1 Kings 2–7', 'scripture_refs': [
            ScriptureReference('1 Kings', 2, 7)
        ]},
        # Week 29: 1 Kings 16–25
        {'week_number': 29, 'title': '1 Kings 16–25', 'scripture_refs': [
            ScriptureReference('1 Kings', 16, 25)
        ]},
        # Week 30: 2 Chronicles 14–20
        {'week_number': 30, 'title': '2 Chronicles 14–20', 'scripture_refs': [
            ScriptureReference('2 Chronicles', 14, 20)
        ]},
        # Week 31: Ezra 1
        {'week_number': 31, 'title': 'Ezra 1', 'scripture_refs': [
            ScriptureReference('Ezra', 1)
        ]},
        # Week 32: Esther
        {'week_number': 32, 'title': 'Esther', 'scripture_refs': [
            ScriptureReference('Esther', 1, 10)
        ]},
        # Week 33: Job 1–3
        {'week_number': 33, 'title': 'Job 1–3', 'scripture_refs': [
            ScriptureReference('Job', 1, 3)
        ]},
        # Week 34: Psalms 1–2
        {'week_number': 34, 'title': 'Psalms 1–2', 'scripture_refs': [
            ScriptureReference('Psalms', 1, 2)
        ]},
        # Week 35: Psalms 49–51
        {'week_number': 35, 'title': 'Psalms 49–51', 'scripture_refs': [
            ScriptureReference('Psalms', 49, 51)
        ]},
        # Week 36: Psalms 102–103
        {'week_number': 36, 'title': 'Psalms 102–103', 'scripture_refs': [
            ScriptureReference('Psalms', 102, 103)
        ]},
        # Week 37: Proverbs 1–4
        {'week_number': 37, 'title': 'Proverbs 1–4', 'scripture_refs': [
            ScriptureReference('Proverbs', 1, 4)
        ]},
        # Week 38: Isaiah 1–12
        {'week_number': 38, 'title': 'Isaiah 1–12', 'scripture_refs': [
            ScriptureReference('Isaiah', 1, 12)
        ]},
        # Week 39: Isaiah 13–14
        {'week_number': 39, 'title': 'Isaiah 13–14', 'scripture_refs': [
            ScriptureReference('Isaiah', 13, 14)
        ]},
        # Week 40: Isaiah 40–49
        {'week_number': 40, 'title': 'Isaiah 40–49', 'scripture_refs': [
            ScriptureReference('Isaiah', 40, 49)
        ]},
        # Week 41: Isaiah 50–57
        {'week_number': 41, 'title': 'Isaiah 50–57', 'scripture_refs': [
            ScriptureReference('Isaiah', 50, 57)
        ]},
        # Week 42: Isaiah 58–66
        {'week_number': 42, 'title': 'Isaiah 58–66', 'scripture_refs': [
            ScriptureReference('Isaiah', 58, 66)
        ]},
        # Week 43: Jeremiah 1–3
        {'week_number': 43, 'title': 'Jeremiah 1–3', 'scripture_refs': [
            ScriptureReference('Jeremiah', 1, 3)
        ]},
        # Week 44: Jeremiah 31–33
        {'week_number': 44, 'title': 'Jeremiah 31–33', 'scripture_refs': [
            ScriptureReference('Jeremiah', 31, 33)
        ]},
        # Week 45: Ezekiel 1–3
        {'week_number': 45, 'title': 'Ezekiel 1–3', 'scripture_refs': [
            ScriptureReference('Ezekiel', 1, 3)
        ]},
        # Week 46: Daniel 1–7
        {'week_number': 46, 'title': 'Daniel 1–7', 'scripture_refs': [
            ScriptureReference('Daniel', 1, 7)
        ]},
        # Week 47: Hosea 1–6
        {'week_number': 47, 'title': 'Hosea 1–6', 'scripture_refs': [
            ScriptureReference('Hosea', 1, 6)
        ]},
        # Week 48: Amos
        {'week_number': 48, 'title': 'Amos', 'scripture_refs': [
            ScriptureReference('Amos', 1, 9)
        ]},
        # Week 49: Micah
        {'week_number': 49, 'title': 'Micah', 'scripture_refs': [
            ScriptureReference('Micah', 1, 7)
        ]},
        # Week 50: Haggai 1–2
        {'week_number': 50, 'title': 'Haggai 1–2', 'scripture_refs': [
            ScriptureReference('Haggai', 1, 2)
        ]},
        # Week 51: Christmas
        {'week_number': 51, 'title': 'Christmas', 'scripture_refs': []},
        # Week 52: Christmas
        {'week_number': 52, 'title': 'Christmas', 'scripture_refs': []},
    ]
    
    # Seminary Teacher lesson mapping (based on your enhanced scraper results)
    seminary_mapping = {
        2: [3, 4, 5, 6],      # Week 2: Abraham 3; Moses 1
        3: [7, 8, 9, 10],     # Week 3: Genesis 1–2; Moses 2–3; Abraham 4–5
        4: [11, 12, 13],      # Week 4: Genesis 3–4
        5: [14, 15],          # Week 5: Genesis 5; Moses 6
        6: [16, 17],          # Week 6: Moses 7
        7: [18, 19, 20],      # Week 7: Genesis 6–11; Moses 8
        8: [21, 22, 23, 24],  # Week 8: Genesis 12–17; Abraham 1–2
        9: [25, 26, 27],      # Week 9: Genesis 18–23
        10: [28, 29, 30, 31, 32, 33, 34, 35], # Week 10: Genesis 24–33
        11: [36, 37, 38, 39], # Week 11: Genesis 37–41
        12: [40, 41, 42, 43], # Week 12: Genesis 42–50
        13: [44, 45, 46],     # Week 13: Exodus 1–6
        15: [47, 48, 49],     # Week 15: Exodus 7–13
        16: [50, 51, 52, 53], # Week 16: Exodus 14–18
        17: [54, 55, 56],     # Week 17: Exodus 19–20
        18: [57, 58],         # Week 18: Exodus 35–40
        19: [59, 60],         # Week 19: Numbers 11–14
        20: [61, 62],         # Week 20: Deuteronomy 6–8
        21: [63, 64],         # Week 21: Joshua 1–8
        22: [65, 66],         # Week 22: Judges 2–4
        23: [68, 69, 70, 71], # Week 23: 1 Samuel 1–7; Ruth
        24: [65, 66, 72, 73], # Week 24: Judges 6–8; 1 Samuel 8–10
        25: [74, 75],         # Week 25: 1 Samuel 17–18
        26: [76, 77],         # Week 26: 2 Samuel 11–12
        27: [78],             # Week 27: 1 Kings 1–2; 1 Chronicles 13
        28: [79],             # Week 28: 1 Kings 2–7
        29: [81, 82],         # Week 29: 1 Kings 16–25
        30: [83, 84, 85, 86, 87, 88], # Week 30: 2 Chronicles 14–20
        31: [90, 91, 92, 93], # Week 31: Ezra 1
        32: [94, 95],         # Week 32: Esther
        33: [97, 98, 99],     # Week 33: Job 1–3
        34: [100, 101, 102, 103, 104], # Week 34: Psalms 1–2
        35: [105, 107, 108],  # Week 35: Psalms 49–51
        36: [109, 110],       # Week 36: Psalms 102–103
        37: [111],            # Week 37: Proverbs 1–4
        38: [113, 114, 115, 116], # Week 38: Isaiah 1–12
        39: [117, 118],       # Week 39: Isaiah 13–14
        40: [119, 120, 121],  # Week 40: Isaiah 40–49
        41: [123, 124, 125],  # Week 41: Isaiah 50–57
        42: [126, 127, 128, 129], # Week 42: Isaiah 58–66
        43: [130, 131, 132, 134, 135], # Week 43: Jeremiah 1–3
        44: [136],            # Week 44: Jeremiah 31–33
        45: [138, 139, 140, 141], # Week 45: Ezekiel 1–3
        46: [142, 143, 144, 145], # Week 46: Daniel 1–7
        47: [146, 147],       # Week 47: Hosea 1–6
        48: [149, 150, 151],  # Week 48: Amos
        49: [152, 153],       # Week 49: Micah
        50: [155, 156, 157],  # Week 50: Haggai 1–2
        51: [158, 159],       # Week 51: Christmas
    }
    
    # Create CFM year configuration
    from ...core.date_calculator import CFMDateCalculator
    calculator = CFMDateCalculator(2026, start_date)
    
    schedule = []
    for week_config in weekly_schedule_config:
        week_num = week_config['week_number']
        start_date_week, end_date_week = calculator.get_week_dates(week_num)
        
        schedule_week = CFMScheduleWeek(
            week_number=week_num,
            start_date=start_date_week,
            end_date=end_date_week,
            title=week_config['title'],
            scripture_references=week_config['scripture_refs']
        )
        schedule.append(schedule_week)
    
    cfm_year = CFMYear(
        year=2026,
        standard_work=CFMStandardWork.OLD_TESTAMENT,
        title="Old Testament 2026",
        start_date=start_date,
        seminary_mapping=seminary_mapping,
        schedule=schedule
    )
    
    return cfm_year