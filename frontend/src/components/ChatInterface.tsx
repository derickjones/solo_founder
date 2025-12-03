'use client';

import { useState } from 'react';
import { ChevronDownIcon, PaperAirplaneIcon } from '@heroicons/react/24/outline';
import { searchScriptures, SearchResult, askQuestionStream, StreamChunk } from '@/services/api';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  results?: SearchResult[];
  searchTime?: number;
}

interface ChatInterfaceProps {
  selectedSources: string[];
  sourceCount: number;
}

export default function ChatInterface({ selectedSources, sourceCount }: ChatInterfaceProps) {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('AI Q&A');
  const [modeDropdownOpen, setModeDropdownOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Format text for better readability
  const formatText = (text: string) => {
    return text
      // Split on sentence endings followed by capitals (new topics)
      .replace(/(\. )([A-Z][a-z])/g, '$1\n\n$2')
      // Split on numbered points
      .replace(/(\d+\. )/g, '\n\n$1')
      // Split on quotes that start new thoughts  
      .replace(/(") ([A-Z])/g, '$1\n\n$2')
      // Split on scripture citations in parentheses followed by new thoughts
      .replace(/(\([^)]+\)\. )([A-Z])/g, '$1\n\n$2')
      // Split on long sentences for readability
      .replace(/([.!?]) ([A-Z][^.!?]{50,})/g, '$1\n\n$2')
      // Clean up extra spaces and normalize
      .replace(/\n{3,}/g, '\n\n')
      .trim();
  };

  const modes = [
    'AI Q&A',
    'Scripture Study',
    'General Conference',
    'Book of Mormon',
    'Come Follow Me',
    'Youth Mode',
    'Scholar Mode'
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim() || isLoading) return;

    // Add user message
    const userMessage: Message = { id: Date.now(), type: 'user', content: query };
    setMessages(prev => [...prev, userMessage]);

    setIsLoading(true);
    const searchQuery = query;
    setQuery('');

    // Create assistant message that will be updated as we stream
    const assistantMessageId = Date.now() + 1;
    const initialAssistantMessage: Message = {
      id: assistantMessageId,
      type: 'assistant',
      content: '',
      results: [],
      searchTime: 0
    };
    setMessages(prev => [...prev, initialAssistantMessage]);

    try {
      let fullAnswer = '';
      let sources: SearchResult[] = [];
      let searchTime = 0;

      await askQuestionStream({
        query: searchQuery,
        mode,
        max_results: sourceCount,
        selectedSources
      }, (chunk: StreamChunk) => {
        switch (chunk.type) {
          case 'search_complete':
            searchTime = (chunk.search_time_ms || 0) / 1000;
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { ...msg, content: `✅ Found ${chunk.total_sources || 0} sources. Generating response...`, searchTime }
                : msg
            ));
            break;
            
          case 'content':
            if (chunk.content) {
              fullAnswer += chunk.content;
              setMessages(prev => prev.map(msg => 
                msg.id === assistantMessageId 
                  ? { ...msg, content: fullAnswer }
                  : msg
              ));
            }
            break;
            
          case 'sources':
            if (chunk.sources) {
              sources = chunk.sources;
              setMessages(prev => prev.map(msg => 
                msg.id === assistantMessageId 
                  ? { ...msg, results: sources }
                  : msg
              ));
            }
            break;
            
          case 'done':
            setIsLoading(false);
            break;
            
          case 'error':
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { ...msg, content: `Sorry, I encountered an error: ${chunk.error}` }
                : msg
            ));
            setIsLoading(false);
            break;
        }
      });
      
    } catch (error) {
      setMessages(prev => prev.map(msg => 
        msg.id === assistantMessageId 
          ? { ...msg, content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}` }
          : msg
      ));
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-neutral-900">
      {/* Header with logo */}
      <div className="flex items-center justify-center pt-16 pb-8">
        <div className="flex flex-col items-center space-y-6">
          <div className="w-24 h-24 rounded-full overflow-hidden border-2 border-neutral-700">
            <img 
              src="/christ.jpeg" 
              alt="Gospel Study Assistant Logo" 
              className="w-full h-full object-cover"
            />
          </div>
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white mb-2">Gospel Study Assistant</h1>
            <p className="text-xl text-neutral-400">Ask any question and get intelligent answers with scripture citations</p>
          </div>
        </div>
      </div>

      {/* Input area below header */}
      <div className="px-8 pb-4">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <div className="flex items-center bg-neutral-800 border-2 border-neutral-700 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20 rounded-2xl p-4 transition-all duration-200">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask any gospel question..."
                className="flex-1 bg-transparent text-white placeholder-neutral-400 outline-none text-lg"
              />
              
              {/* Mode selector */}
              <div className="relative mx-4">
                <button
                  type="button"
                  onClick={() => setModeDropdownOpen(!modeDropdownOpen)}
                  className="flex items-center space-x-2 bg-neutral-700 hover:bg-neutral-600 px-4 py-2 rounded-lg transition-colors"
                >
                  <span className="text-white text-sm">{mode}</span>
                  <ChevronDownIcon className="w-4 h-4 text-neutral-400" />
                </button>
                
                {modeDropdownOpen && (
                  <div className="absolute top-full right-0 mt-2 bg-neutral-700 rounded-lg shadow-lg border border-neutral-600 py-2 min-w-40">
                    {modes.map((modeOption) => (
                      <button
                        key={modeOption}
                        type="button"
                        onClick={() => {
                          setMode(modeOption);
                          setModeDropdownOpen(false);
                        }}
                        className="block w-full px-4 py-2 text-left text-white hover:bg-neutral-600 transition-colors text-sm"
                      >
                        {modeOption}
                      </button>
                    ))}
                  </div>
                )}
              </div>

              <button
                type="submit"
                disabled={!query.trim() || isLoading}
                className="bg-neutral-600 hover:bg-neutral-500 disabled:bg-neutral-700 disabled:cursor-not-allowed p-3 rounded-full transition-colors"
              >
                {isLoading ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                ) : (
                  <PaperAirplaneIcon className="w-5 h-5 text-white" />
                )}
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 px-8 pb-8 overflow-y-auto">
        {messages.length > 0 ? (
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.map((message) => (
              <div key={message.id} className="space-y-4">
                {(message.type === 'user' || (message.type === 'assistant' && message.content)) && (
                  <div
                    className={`p-4 rounded-lg ${
                      message.type === 'user'
                        ? 'bg-neutral-600 text-white ml-auto max-w-lg'
                        : 'bg-neutral-700 text-white max-w-full'
                    }`}
                  >
                    {message.type === 'assistant' ? (
                      message.content ? (
                        <div className="space-y-4 leading-relaxed text-neutral-100 prose prose-invert max-w-none [&>*]:text-neutral-100">
                          <ReactMarkdown 
                            components={{
                              strong: ({ children }) => <strong className="font-bold text-white">{children}</strong>,
                              em: ({ children }) => <em className="italic">{children}</em>,
                              p: ({ children }) => <p className="text-base leading-7 mb-4 text-neutral-100">{children}</p>
                            }}
                          >
                            {formatText(message.content)}
                          </ReactMarkdown>
                        </div>
                      ) : null
                    ) : (
                      message.content
                    )}
                  </div>
                )}
                
                {/* Display search results */}
                {message.type === 'assistant' && message.results && message.results.length > 0 && (
                  <div className="space-y-3 ml-4">
                    {message.results.map((result, index) => (
                      <div key={index} className="bg-neutral-800 p-4 rounded-lg border border-neutral-600">
                        <div className="flex justify-between items-start mb-2">
                          <div className="text-sm text-neutral-300 font-medium">
                            {result.source}
                            {result.book && ` - ${result.book}`}
                            {result.chapter && result.verse && ` ${result.chapter}:${result.verse}`}
                          </div>
                          <div className="text-xs text-neutral-400">
                            Score: {(result.score * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div className="text-neutral-200 leading-relaxed">
                          {result.content}
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            
            {/* Loading indicator */}
            {isLoading && (
              <div className="flex items-center justify-center p-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-neutral-500"></div>
                <span className="ml-3 text-neutral-400">Searching scriptures...</span>
              </div>
            )}
          </div>
        ) : (
          <div className="flex-1" />
        )}
      </div>

      {/* Footer */}
      <div className="px-8 py-4 border-t border-neutral-700">
        <div className="max-w-4xl mx-auto flex items-center justify-between text-sm text-neutral-400">
          <div>© 2025 Gospel Study Assistant • AI-powered gospel study</div>
          <div className="flex space-x-6">
            <span>Terms of Use</span>
            <span>About</span>
          </div>
        </div>
      </div>
    </div>
  );
}