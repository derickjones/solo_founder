#!/usr/bin/env python3
"""
System prompts and response generation for Gospel Guide AI
Translated from prompts.ts for backend use
"""

from typing import Dict, List, Any, Optional
from datetime import datetime

# Base system prompt for all modes
BASE_SYSTEM_PROMPT = """
You are a deeply faithful, testimony-bearing Latter-day Saint scholar who has spent decades studying the scriptures and modern revelation. 
You answer every question with warmth, clarity, and exact citations like (Alma 32:21), (Oct 2024, Nelson, "Think Celestial!"), or (Saints vol. 2, ch. 12). 
Quote the full verse or talk excerpt when it matters. 
Never speculate, add personal opinion, or go beyond the retrieved sources. 
If the question touches temple ordinances, current membership policies, or anything sensitive, gently say: "This is sacred and personal—please speak with your bishop or refer to the temple recommend questions." 
When appropriate, share your testimony naturally without formulaic endings or repetitive phrases.
NEVER use phrases like "In conclusion", "In summary", "This truth has changed my life", or other formulaic testimony language.
Speak like a beloved BYU religion professor who actually believes every word.
"""

# Mode-specific prompt templates - Free tier only
MODE_SPECIFIC_PROMPTS = {
    # FREE tier - Standard comprehensive mode
    'default': f"""{BASE_SYSTEM_PROMPT}

DEFAULT MODE INSTRUCTIONS:
- Draw from all Standard Works (Book of Mormon, D&C, Pearl of Great Price, Bible)
- Include General Conference talks from all available sessions
- Provide balanced, comprehensive answers using any relevant source
- Cross-reference between scriptures and modern revelation
- Maintain scholarly accuracy while keeping explanations accessible"""
}

CITATION_INSTRUCTIONS = """
CITATION REQUIREMENTS:
- Scripture citations: (Book Chapter:Verse) - e.g., (1 Nephi 3:7) or (1 Nephi 3:7–9)
- Conference citations: (Month Year, Speaker, "Talk Title") - e.g., (Oct 2024, Elder Uchtdorf, "A Higher Joy")
- Manual citations: (Manual Title, Chapter/Lesson) - e.g., (Come Follow Me, Lesson 23)
- ALWAYS verify citations match the exact source content provided
- Include full verse text when quoting scripture
- Never cite sources not provided in the context

CRITICAL ANTI-HALLUCINATION SAFEGUARDS:
- QUOTE ONLY from provided bundle content - NEVER create, paraphrase, or approximate quotes
- CITE ONLY prophets/apostles whose exact words appear in the bundle materials
- REFERENCE ONLY historical facts, archaeological insights, or cultural context from bundle sources
- USE "This pattern suggests..." or "This appears to indicate..." for interpretive analysis without explicit source support
- NEVER fabricate conference talks, prophetic statements, or scholarly works not included in bundle
- IF no modern prophetic connection exists in bundle, acknowledge limitation rather than invent
- ALWAYS use verbatim quotes with exact source attribution when citing any authority
- MARK clearly when making interpretive connections vs. citing authoritative sources
"""

SAFETY_GUIDELINES = """
IMPORTANT BOUNDARIES:
- Direct deeply personal questions to bishops or stake presidents
- For current Church policy questions, refer to official Church sources or local leaders
- Never interpret policy or doctrine beyond what's explicitly stated in sources
- For mental health, abuse, or serious personal issues, recommend appropriate professional help
- Maintain absolute reverence when discussing sacred topics like temple worship
"""

def get_system_prompt(mode: str = 'default') -> str:
    """Get the complete system prompt for a given mode"""
    mode_prompt = MODE_SPECIFIC_PROMPTS.get(mode, MODE_SPECIFIC_PROMPTS['default'])
    
    return f"""{mode_prompt}

{CITATION_INSTRUCTIONS}

{SAFETY_GUIDELINES}

Remember: Your role is to help people draw closer to Christ through study of restored gospel truths. Be a tool for the Spirit to teach through."""

def build_context_prompt(query: str, search_results: List[Dict[str, Any]], mode: str = 'default') -> str:
    """
    Build the context prompt with search results and mode-specific instructions
    
    Args:
        query: The user's question
        search_results: List of search results from scripture_search.py
        mode: The selected mode (default, book-of-mormon-only, etc.)
    """
    
    # Format search results into context sections
    context_sections = []
    for i, result in enumerate(search_results, 1):
        metadata = result.get('metadata', {})
        content = result.get('content', '').strip()
        
        # Format citations based on source type
        citation = format_citation(metadata)
        
        context_section = f"""Source {i} {citation}:
{content}

---"""
        context_sections.append(context_section)
    
    # Join all context sections
    all_contexts = "\n\n".join(context_sections)
    
    # Get mode-specific instructions
    mode_instructions = get_mode_specific_context_instructions(mode)
    
    return f"""Based on the following sources, please answer this question: "{query}"

{mode_instructions}

SOURCES:
{all_contexts}

Remember to cite your sources exactly as shown and include full scripture text when quoting verses. Stay strictly within the provided sources."""

def format_citation(metadata: Dict[str, Any]) -> str:
    """Format citation based on metadata structure"""
    source_type = metadata.get('source_type', '')
    
    if source_type == 'scripture':
        # Scripture citation: (Book Chapter:Verse)
        if 'citation' in metadata:
            return metadata['citation']
        else:
            book = metadata.get('book', '')
            chapter = metadata.get('chapter', '')
            verse = metadata.get('verse', '')
            if book and chapter and verse:
                return f"({book} {chapter}:{verse})"
            return "(Scripture)"
            
    elif source_type == 'conference':
        # Conference citation: (Month Year, Speaker, "Title")
        session = metadata.get('session', '')
        year = metadata.get('year', '')
        speaker = metadata.get('speaker', '')
        title = metadata.get('title', '')
        
        if session and year and speaker and title:
            return f"({session} {year}, {speaker}, \"{title}\")"
        elif 'citation' in metadata:
            return metadata['citation']
        return "(General Conference)"
        
    elif source_type == 'come_follow_me':
        # Come Follow Me citation
        year = metadata.get('year', '')
        lesson_title = metadata.get('lesson_title', metadata.get('title', ''))
        
        if year and lesson_title:
            return f"(Come Follow Me {year}: \"{lesson_title}\")"
        return "(Come Follow Me)"
        
    else:
        # Fallback to citation field if available
        return metadata.get('citation', '(Source)')

def get_mode_specific_context_instructions(mode: str) -> str:
    """Get mode-specific instructions for interpreting the context"""
    instructions = {
        'book-of-mormon-only': "NOTE: You are responding as a missionary who only knows the Book of Mormon. Ignore any non-Book of Mormon sources above.",
        
        'general-conference-only': "NOTE: Only reference the General Conference sources above. Ignore any scripture-only sources unless they were quoted in the conference talks.",
        
        'come-follow-me': "NOTE: Focus on the Come Follow Me sources and relate everything to this week's study. Include discussion questions for families.",
        
        'youth': "NOTE: Explain everything in simple terms that a 14-year-old would understand. Be enthusiastic and relatable.",
        
        'scholar': "NOTE: Provide academic depth while maintaining testimony. Include cross-references and contextual insights.",
        
        'default': "NOTE: Draw from all provided sources to give a comprehensive, balanced answer."
    }
    
    return instructions.get(mode, instructions['default'])

def enhance_query_for_mode(query: str, mode: str) -> str:
    """Enhance the search query based on the mode"""
    enhancements = {
        'book-of-mormon-only': f"{query} (search only Book of Mormon)",
        'general-conference-only': f"{query} (search only General Conference talks)",
        'come-follow-me': f"{query} (search Come Follow Me 2025 Doctrine and Covenants)",
        'youth': f"{query} (explain for teenagers)",
        'scholar': f"{query} (provide scholarly analysis)"
    }
    
    return enhancements.get(mode, query)

# Source filtering helpers that map to the existing search engine
def get_mode_source_filter(mode: str) -> Optional[Dict[str, Any]]:
    """Get source filter based on mode"""
    filters = {
        'book-of-mormon-only': {
            'source_type': 'scripture',
            'standard_work': 'Book of Mormon'
        },
        'general-conference-only': {
            'source_type': 'conference',
            'min_year': 1971
        },
        'come-follow-me': {
            'source_type': 'come_follow_me',
            'year': 2025
        },
        'youth': {
            'min_year': 2015  # Last 10 years for relevance
        }
    }
    
    return filters.get(mode, None)

# Popular filters for quick access
POPULAR_FILTERS = {
    'BOOK_OF_MORMON_ONLY': {'source_type': 'scripture', 'standard_work': 'Book of Mormon'},
    'NEW_TESTAMENT_ONLY': {'source_type': 'scripture', 'standard_work': 'New Testament'},
    'DOCTRINE_COVENANTS_ONLY': {'source_type': 'scripture', 'standard_work': 'Doctrine and Covenants'},
    'RECENT_CONFERENCE': {'source_type': 'conference', 'min_year': 2020},
    'PROPHET_TALKS': {'source_type': 'conference', 'speaker': 'Russell M. Nelson'},
    'APOSTLE_TEACHINGS': {'source_type': 'conference', 'min_year': 2015},
    'CURRENT_CFM': {'source_type': 'come_follow_me', 'year': 2025},
}

if __name__ == "__main__":
    # Test the system
    test_query = "What is faith?"
    test_results = [
        {
            'content': 'Faith is to hope for things which are not seen, which are true.',
            'metadata': {
                'source_type': 'scripture',
                'book': 'Alma',
                'chapter': 32,
                'verse': 21,
                'citation': '(Alma 32:21)'
            }
        }
    ]
    
    context = build_context_prompt(test_query, test_results, 'default')
    system = get_system_prompt('default')
    
    print("System Prompt:")
    print(system[:200] + "...")
    print("\nContext Prompt:")
    print(context)

