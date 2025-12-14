#!/usr/bin/env python3
import json
import os

files = sorted([f for f in os.listdir('.') if f.startswith('week_') and f.endswith('.json')])

print('📚 CFM 2026 Old Testament - Content Sources by Week')
print('=' * 120)

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
            content_sources = data.get('content_sources', [])
            
            # Header for each week
            scripture = date_range if date_range else title
            print(f'\n📅 WEEK {week:2d} ({dates}) - {scripture}')
            print('-' * 120)
            
            # Group sources by type
            sources_by_type = {}
            for i, source in enumerate(content_sources):
                source_type = source.get('source_type', 'unknown')
                if source_type not in sources_by_type:
                    sources_by_type[source_type] = []
                sources_by_type[source_type].append({
                    'title': source.get('title', f'Source {i+1}'),
                    'content_length': len(source.get('content', '')),
                    'purpose': source.get('purpose', 'No description')
                })
            
            # Display each source type
            for source_type in ['cfm', 'scripture', 'seminary_teacher']:
                if source_type in sources_by_type:
                    type_emoji = {'cfm': '🏠', 'scripture': '📖', 'seminary_teacher': '🎓'}.get(source_type, '📝')
                    type_name = {
                        'cfm': 'Come Follow Me',
                        'scripture': 'Scripture Text', 
                        'seminary_teacher': 'Seminary Teacher'
                    }.get(source_type, source_type.title())
                    
                    print(f'  {type_emoji} {type_name}:')
                    
                    for source in sources_by_type[source_type]:
                        content_kb = f'{source["content_length"]/1000:.1f}k'
                        print(f'    • {source["title"]:<35} ({content_kb:>6} chars) - {source["purpose"]}')
            
            # Calculate totals
            total_sources = len(content_sources)
            total_chars = sum(len(source.get('content', '')) for source in content_sources)
            print(f'  📊 TOTALS: {total_sources} sources, {total_chars:,} characters ({total_chars/1000:.1f}k)')
            
    except Exception as e:
        print(f'Week {week:2d} ({dates}) - Error reading file: {e}')

print('\n' + '=' * 120)
print('📝 Legend: 🏠 CFM Lesson | 📖 Scripture Text | 🎓 Seminary Teacher Manual')
print('✨ Each bundle contains comprehensive materials for deep gospel study!')