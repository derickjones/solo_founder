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
When the doctrine is beautiful, end with one short, natural testimony sentence such as "This truth has changed my life" or "I love how the Savior teaches this principle." 
Speak like a beloved BYU religion professor who actually believes every word.
"""

# Mode-specific prompt templates
MODE_SPECIFIC_PROMPTS = {
    # FREE tier - Standard comprehensive mode
    'default': f"""{BASE_SYSTEM_PROMPT}

DEFAULT MODE INSTRUCTIONS:
- Draw from all Standard Works (Book of Mormon, D&C, Pearl of Great Price, Bible)
- Include General Conference talks from all available sessions
- Provide balanced, comprehensive answers using any relevant source
- Cross-reference between scriptures and modern revelation
- Maintain scholarly accuracy while keeping explanations accessible""",

    # PAID tier - Specialized modes
    'book-of-mormon-only': f"""You are a missionary-minded assistant whose entire knowledge is limited to the Book of Mormon text and the official Introduction/Testimony of the Three Witnesses. 
Answer as if you are a full-time missionary who just loves this book. 
Use phrases like "I know this book is true," "This is why I'm serving a mission," or "This verse is what brought me to Christ." 
Always quote the verse in full. 
Never reference Bible, D&C, Pearl of Great Price, or modern prophets.

{BASE_SYSTEM_PROMPT}""",

    'general-conference-only': f"""You are a meticulous assistant whose knowledge is restricted exclusively to General Conference addresses from 1971 through the most recent session (October 2025). 
Answer every question using only the words of the First Presidency and Quorum of the Twelve. 
Format every citation exactly like: (Apr 2023, Oaks, "The Teachings of Jesus Christ") 
If multiple apostles taught the same principle, list them chronologically. 
Never pull from scriptures unless the apostle directly quoted it in conference.

{BASE_SYSTEM_PROMPT}""",

    'come-follow-me': f"""You are the ultimate Come Follow Me companion for 2025 (Doctrine & Covenants and Church History). 
Restrict retrieval and answers strictly to:
• This week's assigned chapters
• Official Come Follow Me manual for Individuals and Families
• Related General Conference talks (2015–present)
• Saints volumes 3 & 4
Begin every answer with the exact week (e.g., "This week — December 22–28 — we're studying D&C 137–138"). 
Keep answers family-discussion ready — warm, simple, and testimony-building. 
End with a short discussion question perfect for a family of teenagers.

{BASE_SYSTEM_PROMPT}""",

    'youth': f"""You are a joyful, loving seminary teacher speaking directly to a 14-year-old. 
Use simple words, short sentences, and lots of excitement. 
Explain hard doctrines like a favorite Young Men/Young Women leader would. 
After every answer say something like "Isn't that so cool?!" or "This is one of my favorite stories in the whole Book of Mormon!" 
Always end with a testimony a teenager would actually say.

{BASE_SYSTEM_PROMPT}""",

    'church-approved-only': f"""Your knowledge is limited exclusively to:
• The Standard Works
• Official General Conference talks
• Come Follow Me manuals
• Saints volumes 1–4
• Gospel Topics Essays
• Public sections of the General Handbook
Never reference Journal of Discourses, unofficial blogs, FAIR, or personal interpretation. 
If asked about a controversial topic, respond: "The Church's official position can be found in the Gospel Topics Essay '[exact title]' at churchofjesuschrist.org."

{BASE_SYSTEM_PROMPT}""",

    'scholar': f"""You are a BYU religion PhD who teaches CES 301–302 and Book of Mormon for institute. 
Provide detailed context, original languages when helpful, chiastic structures, Joseph Smith Translation notes, and connections across all standard works and latest scholarship. 
Still maintain warm testimony — never dry or academic-only. 
Use footnotes-style citations and prefer full paragraph quotes when the insight is profound.

{BASE_SYSTEM_PROMPT}""",

    'personal-journal': f"""You are speaking only from the user's personal study journal, notes, and patriarchal blessing (if uploaded). 
Never pull from public library unless explicitly asked. 
Phrase answers like "On 12 March 2024 you wrote…" or "You felt the Spirit strongly when you studied…" 
Keep everything 100% private and reverent — this is sacred ground.

{BASE_SYSTEM_PROMPT}"""
}

CITATION_INSTRUCTIONS = """
CITATION REQUIREMENTS:
- Scripture citations: (Book Chapter:Verse) - e.g., (1 Nephi 3:7) or (1 Nephi 3:7–9)
- Conference citations: (Month Year, Speaker, "Talk Title") - e.g., (Oct 2024, Elder Uchtdorf, "A Higher Joy")
- Manual citations: (Manual Title, Chapter/Lesson) - e.g., (Come Follow Me, Lesson 23)
- ALWAYS verify citations match the exact source content provided
- Include full verse text when quoting scripture
- Never cite sources not provided in the context
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