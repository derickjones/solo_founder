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
}

export interface SearchResponse {
  query: string;
  results: SearchResult[];
  total_found: number;
  search_time: number;
  mode: string;
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
const getSourceFilter = (selectedSources: string[]): string[] => {
  const sourceMap: Record<string, string> = {
    'general-conference': 'General Conference',
    'book-of-mormon': 'Book of Mormon',
    'doctrine-and-covenants': 'Doctrine and Covenants',
    'pearl-of-great-price': 'Pearl of Great Price',
    'old-testament': 'Old Testament',
    'new-testament': 'New Testament'
  };
  
  return selectedSources.map(source => sourceMap[source]).filter(Boolean);
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
      score: result.score
    })),
    total_found: data.total_found,
    search_time: data.search_time_ms / 1000, // Convert ms to seconds
    mode: data.mode
  };
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