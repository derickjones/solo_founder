#!/usr/bin/env python3
import json
import os

files = sorted([f for f in os.listdir('.') if f.startswith('week_') and f.endswith('.json')])

print('📅 CFM 2026 Old Testament - Complete Schedule')
print('=' * 80)
print(f"{'Week':<4} | {'Dates':<12} | {'Scripture Focus':<25} | {'Content':<10}")
print('-' * 4 + ' | ' + '-' * 12 + ' | ' + '-' * 25 + ' | ' + '-' * 10)

for file in files:
    week = int(file.split('_')[1])
    parts = file.replace('.json', '').split('_')
    if len(parts) >= 4:
        dates = f'{parts[2]}-{parts[3]}'
    else:
        dates = 'TBD'
    
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            title = data.get('title', '')
            date_range = data.get('date_range', '')
            total_chars = sum(len(source.get('content', '')) for source in data.get('content_sources', []))
            content_kb = f'{total_chars/1000:.1f}k'
            
            if date_range:
                scripture = date_range[:25]
            elif title:
                scripture = title[:25]
            else:
                scripture = 'Various'
                
            print(f'{week:>4} | {dates:<12} | {scripture:<25} | {content_kb:>8}')
    except Exception as e:
        print(f'{week:>4} | {dates:<12} | {"Error reading":<25} | {"N/A":>8}')

print('=' * 80)
print('Total: 51 weeks of comprehensive CFM content')