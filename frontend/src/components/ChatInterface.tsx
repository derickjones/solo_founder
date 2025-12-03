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
      content: '🔍 Searching scriptures...',
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
    <div className="flex-1 flex flex-col bg-gray-900">
      {/* Header with logo */}
      <div className="flex items-center justify-center pt-16 pb-8">
        <div className="flex flex-col items-center space-y-6">
          <div className="w-24 h-24 bg-blue-800 rounded-full flex items-center justify-center">
            <div className="w-16 h-16 bg-blue-600 rounded-full flex items-center justify-center">
              <svg className="w-10 h-10 text-white" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/>
              </svg>
            </div>
          </div>
          <div className="text-center">
            <h1 className="text-4xl font-bold text-white mb-2">Gospel Study Assistant</h1>
            <p className="text-xl text-gray-400">Ask any question and get intelligent answers with scripture citations</p>
          </div>
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 px-8 pb-4 overflow-y-auto">
        {messages.length > 0 ? (
          <div className="max-w-4xl mx-auto space-y-6">
            {messages.map((message) => (
              <div key={message.id} className="space-y-4">
                <div
                  className={`p-4 rounded-lg ${
                    message.type === 'user'
                      ? 'bg-blue-600 text-white ml-auto max-w-lg'
                      : 'bg-gray-700 text-white max-w-full'
                  }`}
                >
                  {message.type === 'assistant' ? (
                    <div className="prose prose-invert max-w-none prose-gray">
                      <ReactMarkdown 
                        components={{
                          p: ({children}) => <p className="text-gray-100 leading-7 mb-4">{children}</p>,
                          strong: ({children}) => <strong className="text-white font-semibold">{children}</strong>,
                          em: ({children}) => <em className="text-gray-200 italic">{children}</em>,
                          h1: ({children}) => <h1 className="text-xl font-bold text-white mb-3">{children}</h1>,
                          h2: ({children}) => <h2 className="text-lg font-semibold text-white mb-2">{children}</h2>,
                          h3: ({children}) => <h3 className="text-base font-semibold text-white mb-2">{children}</h3>,
                          ul: ({children}) => <ul className="list-disc ml-6 text-gray-100 space-y-1">{children}</ul>,
                          ol: ({children}) => <ol className="list-decimal ml-6 text-gray-100 space-y-1">{children}</ol>,
                          li: ({children}) => <li className="text-gray-100">{children}</li>,
                          blockquote: ({children}) => <blockquote className="border-l-4 border-blue-400 pl-4 italic text-gray-200">{children}</blockquote>,
                          code: ({children}) => <code className="bg-gray-800 px-2 py-1 rounded text-gray-200">{children}</code>
                        }}
                      >
                        {message.content}
                      </ReactMarkdown>
                    </div>
                  ) : (
                    message.content
                  )}
                </div>
                
                {/* Display search results */}
                {message.type === 'assistant' && message.results && message.results.length > 0 && (
                  <div className="space-y-3 ml-4">
                    {message.results.map((result, index) => (
                      <div key={index} className="bg-gray-800 p-4 rounded-lg border border-gray-600">
                        <div className="flex justify-between items-start mb-2">
                          <div className="text-sm text-blue-400 font-medium">
                            {result.source}
                            {result.book && ` - ${result.book}`}
                            {result.chapter && result.verse && ` ${result.chapter}:${result.verse}`}
                          </div>
                          <div className="text-xs text-gray-400">
                            Score: {(result.score * 100).toFixed(1)}%
                          </div>
                        </div>
                        <div className="text-gray-200 leading-relaxed">
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
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
                <span className="ml-3 text-gray-400">Searching scriptures...</span>
              </div>
            )}
          </div>
        ) : (
          <div className="flex-1" />
        )}
      </div>

      {/* Input area */}
      <div className="px-8 pb-8">
        <div className="max-w-4xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <div className="flex items-center bg-gray-800 border-2 border-blue-500 rounded-2xl p-4">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask any gospel question..."
                className="flex-1 bg-transparent text-white placeholder-gray-400 outline-none text-lg"
              />
              
              {/* Mode selector */}
              <div className="relative mx-4">
                <button
                  type="button"
                  onClick={() => setModeDropdownOpen(!modeDropdownOpen)}
                  className="flex items-center space-x-2 bg-gray-700 hover:bg-gray-600 px-4 py-2 rounded-lg transition-colors"
                >
                  <span className="text-white text-sm">{mode}</span>
                  <ChevronDownIcon className="w-4 h-4 text-gray-400" />
                </button>
                
                {modeDropdownOpen && (
                  <div className="absolute bottom-full right-0 mb-2 bg-gray-700 rounded-lg shadow-lg border border-gray-600 py-2 min-w-40">
                    {modes.map((modeOption) => (
                      <button
                        key={modeOption}
                        type="button"
                        onClick={() => {
                          setMode(modeOption);
                          setModeDropdownOpen(false);
                        }}
                        className="block w-full px-4 py-2 text-left text-white hover:bg-gray-600 transition-colors text-sm"
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
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-600 disabled:cursor-not-allowed p-3 rounded-full transition-colors"
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
    </div>
  );
}