#!/usr/bin/env python3
import json
import os

files = sorted([f for f in os.listdir('.') if f.startswith('week_') and f.endswith('.json')])

print('📚 CFM 2026 Old Testament - Sources Summary')
print('=' * 100)
print(f'{"Week":<5} | {"Date":<12} | {"Scripture":<20} | {"CFM":<6} | {"Script":<6} | {"Seminary":<8} | {"Total":<6}')
print('-' * 5 + ' | ' + '-' * 12 + ' | ' + '-' * 20 + ' | ' + '-' * 6 + ' | ' + '-' * 6 + ' | ' + '-' * 8 + ' | ' + '-' * 6)

total_weeks = 0
total_sources = 0
total_chars = 0

for file in files:
    week = int(file.split('_')[1])
    parts = file.replace('.json', '').split('_')
    if len(parts) >= 4:
        dates = f'{parts[2]}-{parts[3]}'[:12]
    else:
        dates = 'TBD'
    
    try:
        with open(file, 'r') as f:
            data = json.load(f)
            date_range = data.get('date_range', '')
            content_sources = data.get('content_sources', [])
            
            # Count sources by type
            cfm_count = 0
            scripture_count = 0
            seminary_count = 0
            
            cfm_chars = 0
            scripture_chars = 0
            seminary_chars = 0
            
            for source in content_sources:
                source_type = source.get('source_type', 'unknown')
                content_len = len(source.get('content', ''))
                
                if source_type == 'cfm':
                    cfm_count += 1
                    cfm_chars += content_len
                elif source_type == 'scripture':
                    scripture_count += 1
                    scripture_chars += content_len
                elif source_type == 'seminary_teacher':
                    seminary_count += 1
                    seminary_chars += content_len
            
            # Format scripture reference
            scripture = date_range[:20] if date_range else '—'
            
            # Format counts
            cfm_display = f'{cfm_count}({cfm_chars//1000}k)' if cfm_count > 0 else '—'
            script_display = f'{scripture_count}({scripture_chars//1000}k)' if scripture_count > 0 else '—'
            seminary_display = f'{seminary_count}({seminary_chars//1000}k)' if seminary_count > 0 else '—'
            
            total_content = sum(len(source.get('content', '')) for source in content_sources)
            total_display = f'{len(content_sources)}({total_content//1000}k)'
            
            print(f'{week:>4} | {dates:<12} | {scripture:<20} | {cfm_display:<6} | {script_display:<6} | {seminary_display:<8} | {total_display:<6}')
            
            total_weeks += 1
            total_sources += len(content_sources)
            total_chars += total_content
            
    except Exception as e:
        print(f'{week:>4} | {dates:<12} | {"ERROR":<20} | {"—":<6} | {"—":<6} | {"—":<8} | {"—":<6}')

print('=' * 100)
print(f'📊 SUMMARY: {total_weeks} weeks, {total_sources} total sources, {total_chars:,} characters ({total_chars//1000}k total)')
print()
print('📝 Legend:')
print('  • CFM: Come Follow Me lessons (🏠)')
print('  • Script: Full scripture text chapters (📖)') 
print('  • Seminary: Seminary Teacher manual lessons (🎓)')
print('  • Format: Count(Size in k characters)')
print()
print('✨ Each bundle provides comprehensive study materials combining official CFM content,')
print('   complete scripture text, and detailed Seminary Teacher guidance!')