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
  const filters: any[] = [];
  
  for (const source of selectedSources) {
    if (source.startsWith('gc-year-')) {
      // Year-based General Conference filter: gc-year-2024
      const year = parseInt(source.replace('gc-year-', ''));
      filters.push({ source_type: 'conference', year });
    } else if (source.startsWith('gc-speaker-')) {
      // Speaker-based filter: gc-speaker-russell-m-nelson
      const speakerKey = source.replace('gc-speaker-', '');
      const speakerName = speakerKey.replace(/-/g, ' ')
        .replace(/\b\w/g, l => l.toUpperCase()); // Convert to Title Case
      filters.push({ source_type: 'conference', speaker: speakerName });
    } else {
      // Legacy source mappings
      const sourceMap: Record<string, any> = {
        'general-conference': { source_type: 'conference' },
        'book-of-mormon': { source_type: 'scripture', standard_work: 'Book of Mormon' },
        'doctrine-and-covenants': { source_type: 'scripture', standard_work: 'Doctrine and Covenants' },
        'pearl-of-great-price': { source_type: 'scripture', standard_work: 'Pearl of Great Price' },
        'old-testament': { source_type: 'scripture', standard_work: 'Old Testament' },
        'new-testament': { source_type: 'scripture', standard_work: 'New Testament' }
      };
      
      if (sourceMap[source]) {
        filters.push(sourceMap[source]);
      }
    }
  }
  
  return filters.length > 0 ? filters : undefined;
};

export const searchScriptures = async (request: SearchRequest & { selectedSources?: string[] }): Promise<SearchResponse> => {
  const apiMode = MODE_MAPPING[request.mode || 'AI Q&A'] || 'default';
  const sourceFilter = request.selectedSources ? getSourceFilter(request.selectedSources) : [];
  
  const body = {
    query: request.query,
    mode: apiMode,
    top_k: request.max_results || 5,
    ...(sourceFilter.length > 0 && { source_filter: sourceFilter })
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
      book: result.metadata?.title,
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
  const sourceFilter = request.selectedSources ? getSourceFilter(request.selectedSources) : [];
  
  const body = {
    query: request.query,
    mode: apiMode,
    top_k: request.max_results || 10,
    ...(sourceFilter.length > 0 && { source_filter: sourceFilter })
  };

  const response = await fetch(`${API_BASE_URL}/ask/stream`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    throw new Error(`Streaming request failed: ${response.statusText}`);
  }

  if (!response.body) {
    throw new Error('Response body is null');
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  try {
    while (true) {
      const { done, value } = await reader.read();
      
      if (done) break;
      
      // Add new chunk to buffer
      buffer += decoder.decode(value, { stream: true });
      
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
              
              // Transform sources to match our expected format
              if (data.type === 'sources' && data.sources) {
                data.sources = data.sources.map((source: any) => ({
                  content: source.content,
                  source: source.metadata?.standard_work || 'Unknown',
                  book: source.metadata?.title,
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
              console.error('Failed to parse SSE data:', e);
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