const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'https://gospel-guide-api-273320302933.us-central1.run.app';

export interface SearchRequest {
  query: string;
  mode?: string;
  max_results?: number;
}

export interface SearchResult {
  content: string;
  source: string;
  book?: string;
  chapter?: number;
  verse?: number;
  score: number;
  citation?: string;
  url?: string;
  speaker?: string;
  year?: number;
  session?: string;
  title?: string;
  rank?: number;
  paragraph?: number;
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total_found: number;
  search_time: number;
  mode: string;
}

// New AI Q&A interfaces
export interface AskRequest {
  query: string;
  mode?: string;
  max_results?: number;
}

export interface AskResponse {
  query: string;
  mode: string;
  answer: string;
  sources: SearchResult[];
  total_sources: number;
  search_time: number;
  response_time: number;
}

// Come Follow Me interfaces
export interface CFMLessonPlanRequest {
  week: string;
  audience: 'adults' | 'youth' | 'family' | 'children';
}

export interface CFMLessonPlanResponse {
  week: string;
  audience: string;
  lesson_title: string;
  lesson_plan: string;
  sources_used: number;
  generation_time_ms: number;
}

// CFM Deep Dive interfaces (new optimized API)
export interface CFMDeepDiveRequest {
  week_number: number;
  study_level: 'basic' | 'intermediate' | 'advanced';
}

export interface CFMDeepDiveResponse {
  week_number: number;
  study_level: string;
  title: string;
  study_guide: string;
  generation_time: number;
  content_sources: number;
}

// Map frontend modes to API modes
const MODE_MAPPING: Record<string, string> = {
  'AI Q&A': 'default',
  'Scripture Study': 'default',
  'General Conference': 'general-conference-only',
  'Book of Mormon': 'book-of-mormon-only',
  'Come Follow Me': 'come-follow-me',
  'Youth Mode': 'youth',
  'Scholar Mode': 'scholar'
};

// Map selected sources to API source filters
const getSourceFilter = (selectedSources: string[]): any => {
  // If no sources selected, return undefined (search all)
  if (selectedSources.length === 0) {
    return undefined;
  }
  
  // If all sources are selected (common case), don't filter
  const allSources = [
    'general-conference',
    'gc-year-2025', 'gc-year-2024', 'gc-year-2023', 'gc-year-2022', 'gc-year-2021',
    'gc-year-2020', 'gc-year-2019', 'gc-year-2018', 'gc-year-2017', 'gc-year-2016', 'gc-year-2015',
    'gc-speaker-russell-m-nelson', 'gc-speaker-dallin-h-oaks', 'gc-speaker-henry-b-eyring',
    'gc-speaker-jeffrey-r-holland', 'gc-speaker-dieter-f-uchtdorf', 'gc-speaker-david-a-bednar',
    'gc-speaker-quentin-l-cook', 'gc-speaker-d-todd-christofferson', 'gc-speaker-neil-l-andersen',
    'gc-speaker-ronald-a-rasband', 'gc-speaker-gary-e-stevenson', 'gc-speaker-dale-g-renlund',
    'book-of-mormon', 'doctrine-and-covenants', 'pearl-of-great-price', 'old-testament', 'new-testament'
  ];
  
  if (selectedSources.length === allSources.length) {
    return undefined; // Search all sources
  }
  
  // For now, build a single filter from the most specific selection
  // Priority: specific year/speaker filters > general conference > scripture works
  
  // Check for specific General Conference filters first
  const yearFilters = selectedSources.filter(s => s.startsWith('gc-year-'));
  if (yearFilters.length === 1) {
    const year = parseInt(yearFilters[0].replace('gc-year-', ''));
    return { source_type: 'conference', year };
  }
  
  const speakerFilters = selectedSources.filter(s => s.startsWith('gc-speaker-'));
  if (speakerFilters.length === 1) {
    const speakerKey = speakerFilters[0].replace('gc-speaker-', '');
    const speakerName = speakerKey.replace(/-/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase()); // Convert to Title Case
    return { source_type: 'conference', speaker: speakerName };
  }
  
  // Check for general conference
  if (selectedSources.includes('general-conference')) {
    return { source_type: 'conference' };
  }
  
  // Check for specific scripture works
  const scriptureMap: Record<string, string> = {
    'book-of-mormon': 'Book of Mormon',
    'doctrine-and-covenants': 'Doctrine and Covenants',
    'pearl-of-great-price': 'Pearl of Great Price',
    'old-testament': 'Old Testament',
    'new-testament': 'New Testament'
  };
  
  const scriptureWorks = selectedSources.filter(s => scriptureMap[s]);
  if (scriptureWorks.length === 1) {
    return { source_type: 'scripture', standard_work: scriptureMap[scriptureWorks[0]] };
  }
  
  // If multiple scripture works selected, filter by scripture type only
  if (scriptureWorks.length > 1) {
    return { source_type: 'scripture' };
  }
  
  // Default: no filter (search all)
  return undefined;
};

export const searchScriptures = async (request: SearchRequest & { selectedSources?: string[] }): Promise<SearchResponse> => {
  const apiMode = MODE_MAPPING[request.mode || 'AI Q&A'] || 'default';
  const sourceFilter = request.selectedSources ? getSourceFilter(request.selectedSources) : undefined;
  
  const body = {
    query: request.query,
    mode: apiMode,
    top_k: request.max_results || 5,
    ...(sourceFilter && { source_filter: sourceFilter })
  };

  const response = await fetch(`${API_BASE_URL}/search`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Search failed: ${response.statusText} - ${errorText}`);
  }

  const data = await response.json();
  
  // Transform the API response to match our expected format
  return {
    query: data.query,
    results: data.results.map((result: any) => ({
      content: result.content,
      source: result.metadata?.standard_work || 'Unknown',
      book: result.metadata?.book || result.metadata?.title, // Use book for scriptures, title for conference talks
      chapter: result.metadata?.chapter,
      verse: result.metadata?.verse,
      score: result.score,
      citation: result.metadata?.citation,
      url: result.metadata?.url,
      speaker: result.metadata?.speaker,
      year: result.metadata?.year,
      session: result.metadata?.session,
      title: result.metadata?.title,
      paragraph: result.metadata?.paragraph,
      rank: result.rank
    })),
    total_found: data.total_found,
    search_time: data.search_time_ms / 1000, // Convert ms to seconds
    mode: data.mode
  };
};

// Streaming AI Q&A function
export interface StreamChunk {
  type: 'search_complete' | 'content' | 'sources' | 'timing' | 'done' | 'error';
  content?: string;
  search_time_ms?: number;
  total_sources?: number;
  sources?: SearchResult[];
  response_time_ms?: number;
  total_time_ms?: number;
  error?: string;
}

export const askQuestionStream = async (
  request: AskRequest & { selectedSources?: string[] },
  onChunk: (chunk: StreamChunk) => void
): Promise<void> => {
  const apiMode = MODE_MAPPING[request.mode || 'AI Q&A'] || 'default';
  const sourceFilter = request.selectedSources ? getSourceFilter(request.selectedSources) : undefined;
  
  const body = {
    query: request.query,
    mode: apiMode,
    top_k: request.max_results || 10,
    ...(sourceFilter && { source_filter: sourceFilter })
  };

  console.log('Streaming request body:', body);

  const requestStartTime = Date.now();
  const response = await fetch(`${API_BASE_URL}/ask/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  console.log('Streaming response status:', response.status, response.statusText, 'after', Date.now() - requestStartTime + 'ms');

  if (!response.ok) {
    throw new Error(`Streaming request failed: ${response.statusText}`);
  }

  if (!response.body) {
    throw new Error('Response body is null');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  console.log('Starting to read streaming response...');
  let chunkCount = 0;

  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) {
        console.log('Streaming complete, total chunks processed:', chunkCount);
        break;
      }
      
      chunkCount++;
      
      // Add new chunk to buffer
      buffer += decoder.decode(value, { stream: true });
      console.log('Raw chunk received:', buffer.slice(-100)); // Show last 100 chars
      
      // Split buffer on double newlines (SSE message boundaries)
      const messages = buffer.split('\n\n');
      
      // Keep the last partial message in buffer
      buffer = messages.pop() || '';
      
      // Process complete messages
      for (const message of messages) {
        const lines = message.split('\n');
        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6));
              console.log('Parsed chunk:', data.type, data.content ? `"${data.content.slice(0, 20)}..."` : '');
              
              // Transform sources to match our expected format
              if (data.type === 'sources' && data.sources) {
                data.sources = data.sources.map((source: any) => ({
                  content: source.content,
                  source: source.metadata?.standard_work || 'Unknown',
                  book: source.metadata?.book || source.metadata?.title, // Use book for scriptures, title for conference talks
                  chapter: source.metadata?.chapter,
                  verse: source.metadata?.verse,
                  score: source.score,
                  citation: source.metadata?.citation,
                  url: source.metadata?.url,
                  speaker: source.metadata?.speaker,
                  year: source.metadata?.year,
                  session: source.metadata?.session,
                  title: source.metadata?.title,
                  paragraph: source.metadata?.paragraph,
                  rank: source.rank
                }));
              }
              
              onChunk(data);
            } catch (e) {
              console.error('Failed to parse SSE data:', e, 'Line:', line);
            }
          }
        }
      }
    }
  } finally {
    reader.releaseLock();
  }
};

export const getAvailableSources = async (): Promise<{ standard_works: string[], speakers: string[] }> => {
  const response = await fetch(`${API_BASE_URL}/sources`);
  
  if (!response.ok) {
    throw new Error(`Failed to fetch sources: ${response.statusText}`);
  }

  return response.json();
};

export const getHealth = async (): Promise<{ status: string, segments_loaded: number }> => {
  const response = await fetch(`${API_BASE_URL}/health`);
  
  if (!response.ok) {
    throw new Error(`Health check failed: ${response.statusText}`);
  }

  const data = await response.json();
  return {
    status: data.status,
    segments_loaded: data.total_segments
  };
};

export const generateCFMLessonPlan = async (request: CFMLessonPlanRequest): Promise<CFMLessonPlanResponse> => {
  console.log('Generating CFM lesson plan:', request);
  
  const response = await fetch(`${API_BASE_URL}/cfm/lesson-plan`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to generate lesson plan: ${response.statusText}`);
  }

  return response.json();
};

// New CFM Deep Dive API function
export const generateCFMDeepDive = async (request: CFMDeepDiveRequest): Promise<CFMDeepDiveResponse> => {
  console.log('Generating CFM deep dive study guide:', request);
  
  const response = await fetch(`${API_BASE_URL}/cfm/deep-dive`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || `Failed to generate study guide: ${response.statusText}`);
  }

  return response.json();
};