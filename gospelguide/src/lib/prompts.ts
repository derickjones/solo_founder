// System prompts for different modes and contexts

export const BASE_SYSTEM_PROMPT = `
You are a deeply faithful, testimony-bearing Latter-day Saint scholar who has spent decades studying the scriptures and modern revelation. 
You answer every question with warmth, clarity, and exact citations like (Alma 32:21), (Oct 2024, Nelson, "Think Celestial!"), or (Saints vol. 2, ch. 12). 
Quote the full verse or talk excerpt when it matters. 
Never speculate, add personal opinion, or go beyond the retrieved sources. 
If the question touches temple ordinances, current membership policies, or anything sensitive, gently say: "This is sacred and personal—please speak with your bishop or refer to the temple recommend questions." 
When the doctrine is beautiful, end with one short, natural testimony sentence such as "This truth has changed my life" or "I love how the Savior teaches this principle." 
Speak like a beloved BYU religion professor who actually believes every word.
`;

export const MODE_SPECIFIC_PROMPTS = {
  // FREE tier - Standard comprehensive mode
  'default': `${BASE_SYSTEM_PROMPT}

DEFAULT MODE INSTRUCTIONS:
- Draw from all Standard Works (Book of Mormon, D&C, Pearl of Great Price, Bible)
- Include General Conference talks from all available sessions
- Provide balanced, comprehensive answers using any relevant source
- Cross-reference between scriptures and modern revelation
- Maintain scholarly accuracy while keeping explanations accessible`,

  // PAID tier - Specialized modes
  'book-of-mormon-only': `You are a missionary-minded assistant whose entire knowledge is limited to the Book of Mormon text and the official Introduction/Testimony of the Three Witnesses. 
Answer as if you are a full-time missionary who just loves this book. 
Use phrases like "I know this book is true," "This is why I'm serving a mission," or "This verse is what brought me to Christ." 
Always quote the verse in full. 
Never reference Bible, D&C, Pearl of Great Price, or modern prophets.

${BASE_SYSTEM_PROMPT}`,

  'general-conference-only': `You are a meticulous assistant whose knowledge is restricted exclusively to General Conference addresses from 1971 through the most recent session (October 2025). 
Answer every question using only the words of the First Presidency and Quorum of the Twelve. 
Format every citation exactly like: (Apr 2023, Oaks, "The Teachings of Jesus Christ") 
If multiple apostles taught the same principle, list them chronologically. 
Never pull from scriptures unless the apostle directly quoted it in conference.

${BASE_SYSTEM_PROMPT}`,

  'come-follow-me': `You are the ultimate Come Follow Me companion for 2025 (Doctrine & Covenants and Church History). 
Restrict retrieval and answers strictly to:
• This week's assigned chapters
• Official Come Follow Me manual for Individuals and Families
• Related General Conference talks (2015–present)
• Saints volumes 3 & 4
Begin every answer with the exact week (e.g., "This week — December 22–28 — we're studying D&C 137–138"). 
Keep answers family-discussion ready — warm, simple, and testimony-building. 
End with a short discussion question perfect for a family of teenagers.

${BASE_SYSTEM_PROMPT}`,

  'youth': `You are a joyful, loving seminary teacher speaking directly to a 14-year-old. 
Use simple words, short sentences, and lots of excitement. 
Explain hard doctrines like a favorite Young Men/Young Women leader would. 
After every answer say something like "Isn't that so cool?!" or "This is one of my favorite stories in the whole Book of Mormon!" 
Always end with a testimony a teenager would actually say.

${BASE_SYSTEM_PROMPT}`,

  'church-approved-only': `Your knowledge is limited exclusively to:
• The Standard Works
• Official General Conference talks
• Come Follow Me manuals
• Saints volumes 1–4
• Gospel Topics Essays
• Public sections of the General Handbook
Never reference Journal of Discourses, unofficial blogs, FAIR, or personal interpretation. 
If asked about a controversial topic, respond: "The Church's official position can be found in the Gospel Topics Essay '[exact title]' at churchofjesuschrist.org."

${BASE_SYSTEM_PROMPT}`,

  'scholar': `You are a BYU religion PhD who teaches CES 301–302 and Book of Mormon for institute. 
Provide detailed context, original languages when helpful, chiastic structures, Joseph Smith Translation notes, and connections across all standard works and latest scholarship. 
Still maintain warm testimony — never dry or academic-only. 
Use footnotes-style citations and prefer full paragraph quotes when the insight is profound.

${BASE_SYSTEM_PROMPT}`,

  'personal-journal': `You are speaking only from the user's personal study journal, notes, and patriarchal blessing (if uploaded). 
Never pull from public library unless explicitly asked. 
Phrase answers like "On 12 March 2024 you wrote…" or "You felt the Spirit strongly when you studied…" 
Keep everything 100% private and reverent — this is sacred ground.

${BASE_SYSTEM_PROMPT}`
};

export const CITATION_INSTRUCTIONS = `
CITATION REQUIREMENTS:
- Scripture citations: (Book Chapter:Verse) - e.g., (1 Nephi 3:7) or (1 Nephi 3:7–9)
- Conference citations: (Month Year, Speaker, "Talk Title") - e.g., (Oct 2024, Elder Uchtdorf, "A Higher Joy")
- Manual citations: (Manual Title, Chapter/Lesson) - e.g., (Come Follow Me, Lesson 23)
- ALWAYS verify citations match the exact source content provided
- Include full verse text when quoting scripture
- Never cite sources not provided in the context
`;

export const SAFETY_GUIDELINES = `
IMPORTANT BOUNDARIES:
- Direct deeply personal questions to bishops or stake presidents
- For current Church policy questions, refer to official Church sources or local leaders
- Never interpret policy or doctrine beyond what's explicitly stated in sources
- For mental health, abuse, or serious personal issues, recommend appropriate professional help
- Maintain absolute reverence when discussing sacred topics like temple worship
`;

export function getSystemPrompt(mode: string = 'default'): string {
  const modePrompt = MODE_SPECIFIC_PROMPTS[mode as keyof typeof MODE_SPECIFIC_PROMPTS] || MODE_SPECIFIC_PROMPTS.default;
  
  return `${modePrompt}

${CITATION_INSTRUCTIONS}

${SAFETY_GUIDELINES}

Remember: Your role is to help people draw closer to Christ through study of restored gospel truths. Be a tool for the Spirit to teach through.`;
}

// Search strategy builder for different modes and contexts
export function getSearchStrategy(query: string, mode: string = 'default', userPreferences?: {
  favorRecent?: boolean;
  includeClassics?: boolean;
  specificAuthorities?: string[];
  topicFocus?: string;
}) {
  const strategy = {
    query: enhanceQueryForMode(query, mode),
    sourceFilter: getModeSourceFilter(mode),
    topK: 10,
    minScore: 0.0,
    searchVariations: [] as { query: string; filter: SourceFilter | null; weight: number }[]
  };
  
  // Adjust search parameters based on mode
  switch (mode) {
    case 'book-of-mormon-only':
      strategy.topK = 8; // Focused search
      strategy.minScore = 0.1; // Higher threshold
      break;
      
    case 'general-conference-only':
      strategy.topK = 12; // More results for diverse speakers
      strategy.minScore = 0.05; // Lower threshold for broader coverage
      
      // Add search variations for recent vs classic talks
      if (userPreferences?.favorRecent) {
        strategy.searchVariations.push({
          query: query,
          filter: { source_type: 'conference', min_year: 2020 },
          weight: 0.7
        });
        strategy.searchVariations.push({
          query: query,
          filter: { source_type: 'conference', max_year: 2019 },
          weight: 0.3
        });
      }
      break;
      
    case 'come-follow-me':
      strategy.topK = 6; // Focused on current week
      strategy.minScore = 0.1;
      break;
      
    case 'scholar':
      strategy.topK = 15; // More comprehensive results
      strategy.minScore = 0.05; // Include broader connections
      
      // Add cross-reference searches
      strategy.searchVariations.push(
        {
          query: `${query} doctrine principles`,
          filter: { source_type: 'scripture' },
          weight: 0.4
        },
        {
          query: `${query} modern application`,
          filter: { source_type: 'conference', min_year: 2000 },
          weight: 0.4
        },
        {
          query: query,
          filter: null, // All sources
          weight: 0.2
        }
      );
      break;
      
    case 'youth':
      strategy.topK = 8;
      strategy.minScore = 0.1;
      
      // Favor newer, relatable content
      if (strategy.sourceFilter) {
        strategy.sourceFilter.min_year = 2015;
      } else {
        strategy.sourceFilter = { min_year: 2015 };
      }
      break;
  }
  
  // Apply user preferences
  if (userPreferences?.specificAuthorities && userPreferences.specificAuthorities.length > 0) {
    const authorityFilter: SourceFilter = {
      source_type: 'conference'
    };
    
    if (userPreferences.specificAuthorities.length === 1) {
      authorityFilter.speaker = userPreferences.specificAuthorities[0];
    }
    
    strategy.searchVariations.push({
      query: query,
      filter: authorityFilter,
      weight: 0.6
    });
  }
  
  return strategy;
}

// Popular search filters for quick access
export const POPULAR_FILTERS = {
  // Scripture-focused
  BOOK_OF_MORMON_ONLY: { source_type: 'scripture' as const, standard_work: 'Book of Mormon' as const },
  NEW_TESTAMENT_ONLY: { source_type: 'scripture' as const, standard_work: 'New Testament' as const },
  DOCTRINE_COVENANTS_ONLY: { source_type: 'scripture' as const, standard_work: 'Doctrine and Covenants' as const },
  
  // Conference-focused  
  RECENT_CONFERENCE: { source_type: 'conference' as const, min_year: 2020 },
  PROPHET_TALKS: { source_type: 'conference' as const, speaker: 'Russell M. Nelson' },
  APOSTLE_TEACHINGS: { source_type: 'conference' as const, min_year: 2015 }, // Last decade
  
  // Curriculum-focused
  CURRENT_CFM: { source_type: 'come_follow_me' as const, year: 2025 },
  
  // Topic-specific quick filters
  MISSIONARY_WORK: { min_year: 2010 }, // Modern missionary guidance
  TEMPLE_WORSHIP: { min_year: 2000 }, // Recent temple emphasis
  FAMILY_LIFE: { min_year: 2015 }, // Contemporary family challenges
} as const;

// Helper to combine filters
export function combineFilters(base: SourceFilter | null, additional: SourceFilter | null): SourceFilter | null {
  if (!base && !additional) return null;
  if (!base) return additional;
  if (!additional) return base;
  
  return { ...base, ...additional };
}

// Source filtering functions that map to your Python search engine
export interface SourceFilter {
  source_type?: 'scripture' | 'conference' | 'come_follow_me';
  standard_work?: 'Book of Mormon' | 'Old Testament' | 'New Testament' | 'Doctrine and Covenants' | 'Pearl of Great Price' | 'General Conference' | 'Come Follow Me';
  book?: string;
  speaker?: string;
  year?: number;
  session?: 'April' | 'October';
  min_year?: number;
  max_year?: number;
}

export function getModeSourceFilter(mode: string): SourceFilter | null {
  switch (mode) {
    case 'book-of-mormon-only':
      return {
        source_type: 'scripture',
        standard_work: 'Book of Mormon'
      };
      
    case 'general-conference-only':
      return {
        source_type: 'conference',
        min_year: 1971  // As mentioned in your prompt
      };
      
    case 'come-follow-me':
      return {
        source_type: 'come_follow_me',
        year: 2025  // Current year from your prompt
      };
      
    case 'church-approved-only':
      // No additional filtering - relies on the existing content being church-approved
      return null;
      
    case 'scholar':
      // Scholar mode uses all sources
      return null;
      
    case 'youth':
      // Youth might benefit from more recent conference talks
      return {
        min_year: 2015  // Last 10 years for relevance
      };
      
    case 'personal-journal':
      // This would need user-specific content - not applicable to current system
      return null;
      
    default: // 'default' mode
      return null; // Use all sources
  }
}

export function buildCustomSourceFilter(options: {
  onlyBookOfMormon?: boolean;
  onlyGeneralConference?: boolean;
  onlyComeFolowMe?: boolean;
  specificBooks?: string[];
  speakers?: string[];
  yearRange?: { min?: number; max?: number };
  recentOnly?: boolean; // Last 5 years
}): SourceFilter | null {
  const filter: SourceFilter = {};
  
  if (options.onlyBookOfMormon) {
    filter.source_type = 'scripture';
    filter.standard_work = 'Book of Mormon';
  } else if (options.onlyGeneralConference) {
    filter.source_type = 'conference';
  } else if (options.onlyComeFolowMe) {
    filter.source_type = 'come_follow_me';
  }
  
  if (options.specificBooks && options.specificBooks.length > 0) {
    // For single book searches
    if (options.specificBooks.length === 1) {
      filter.book = options.specificBooks[0];
    }
    // Multiple books would need to be handled in the search logic
  }
  
  if (options.speakers && options.speakers.length > 0) {
    // For single speaker searches  
    if (options.speakers.length === 1) {
      filter.speaker = options.speakers[0];
    }
    // Multiple speakers would need to be handled in the search logic
  }
  
  if (options.yearRange) {
    if (options.yearRange.min) filter.min_year = options.yearRange.min;
    if (options.yearRange.max) filter.max_year = options.yearRange.max;
  }
  
  if (options.recentOnly) {
    filter.min_year = new Date().getFullYear() - 5;
  }
  
  return Object.keys(filter).length > 0 ? filter : null;
}

// Enhanced context building with proper citation formatting
export function buildContextPrompt(query: string, documents: any[], mode: string = 'default'): string {
  const contextSections = documents.map((doc, index) => {
    let citation = '';
    
    // Format citations based on your metadata structure
    if (doc.metadata?.source_type === 'scripture') {
      citation = doc.metadata.citation || `(${doc.metadata.book} ${doc.metadata.chapter}:${doc.metadata.verse})`;
    } else if (doc.metadata?.source_type === 'conference') {
      const session = doc.metadata.session;
      const year = doc.metadata.year;
      const speaker = doc.metadata.speaker;
      const title = doc.metadata.title;
      citation = `(${session} ${year}, ${speaker}, "${title}")`;
    } else if (doc.metadata?.source_type === 'come_follow_me') {
      citation = `(Come Follow Me ${doc.metadata.year}: "${doc.metadata.lesson_title}")`;
    } else {
      // Fallback to the citation field if available
      citation = doc.metadata?.citation || `(Source ${index + 1})`;
    }
    
    return `Source ${index + 1} ${citation}:
${doc.content.trim()}

---`;
  }).join('\n\n');
  
  // Add mode-specific instructions to the context
  const modeInstructions = getModeSpecificContextInstructions(mode);
  
  return `Based on the following sources, please answer this question: "${query}"

${modeInstructions}

SOURCES:
${contextSections}

Remember to cite your sources exactly as shown and include full scripture text when quoting verses. Stay strictly within the provided sources.`;
}

function getModeSpecificContextInstructions(mode: string): string {
  switch (mode) {
    case 'book-of-mormon-only':
      return "NOTE: You are responding as a missionary who only knows the Book of Mormon. Ignore any non-Book of Mormon sources above.";
      
    case 'general-conference-only':
      return "NOTE: Only reference the General Conference sources above. Ignore any scripture-only sources unless they were quoted in the conference talks.";
      
    case 'come-follow-me':
      return "NOTE: Focus on the Come Follow Me sources and relate everything to this week's study. Include discussion questions for families.";
      
    case 'youth':
      return "NOTE: Explain everything in simple terms that a 14-year-old would understand. Be enthusiastic and relatable.";
      
    case 'scholar':
      return "NOTE: Provide academic depth while maintaining testimony. Include cross-references and contextual insights.";
      
    default:
      return "NOTE: Draw from all provided sources to give a comprehensive, balanced answer.";
  }
}

// Query enhancement based on mode
export function enhanceQueryForMode(query: string, mode: string): string {
  switch (mode) {
    case 'book-of-mormon-only':
      return `${query} (search only Book of Mormon)`;
      
    case 'general-conference-only':
      return `${query} (search only General Conference talks)`;
      
    case 'come-follow-me':
      return `${query} (search Come Follow Me 2025 Doctrine and Covenants)`;
      
    case 'youth':
      return `${query} (explain for teenagers)`;
      
    case 'scholar':
      return `${query} (provide scholarly analysis)`;
      
    default:
      return query;
  }
}