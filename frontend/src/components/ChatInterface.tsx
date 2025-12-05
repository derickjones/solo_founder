'use client';

import { useState, useRef, startTransition } from 'react';
import { flushSync } from 'react-dom';
import { ChevronDownIcon, PaperAirplaneIcon, Bars3Icon, ArrowDownTrayIcon } from '@heroicons/react/24/outline';
import { searchScriptures, SearchResult, askQuestionStream, StreamChunk, generateCFMLessonPlan, CFMLessonPlanRequest } from '@/services/api';
import ReactMarkdown from 'react-markdown';
import { generateLessonPlanPDF, LessonPlanData } from '@/utils/pdfGenerator';
import { CFM_AUDIENCES } from '@/utils/comeFollowMe';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  results?: SearchResult[];
  searchTime?: number;
  isStreaming?: boolean;
}

import Link from 'next/link';

interface ChatInterfaceProps {
  selectedSources: string[];
  sourceCount: number;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  mode: string;
  setMode: (mode: string) => void;
  cfmAudience: string;
  setCfmAudience: (audience: string) => void;
  cfmWeek: string;
}

export default function ChatInterface({ selectedSources, sourceCount, sidebarOpen, setSidebarOpen, mode, setMode, cfmAudience, setCfmAudience, cfmWeek }: ChatInterfaceProps) {
  const [query, setQuery] = useState('');
  const [modeDropdownOpen, setModeDropdownOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const [streamingMessageId, setStreamingMessageId] = useState<number | null>(null);

  // PDF download handler
  const handleDownloadPDF = async (messageContent: string) => {
    try {
      // Extract lesson plan details from the message content or current state
      const lessonData: LessonPlanData = {
        title: `${cfmAudience} Lesson Plan`,
        date: cfmWeek,
        audience: cfmAudience,
        content: messageContent,
        scripture: cfmWeek // Using week as scripture reference for now
      };

      await generateLessonPlanPDF(lessonData);
    } catch (error) {
      console.error('Error downloading PDF:', error);
      // Could add toast notification here
      alert('Error generating PDF. Please try again.');
    }
  };

  // Reset chat function
  const resetChat = () => {
    setMessages([]);
    setQuery('');
    setIsLoading(false);
    setStreamingContent('');
    setStreamingMessageId(null);
  };

  // Dynamic placeholder text based on mode
  const getPlaceholderText = () => {
    if (mode === 'Come Follow Me') {
      return 'Click the button to generate your lesson plan →';
    }
    return 'Ask any gospel question...';
  };

  // Format citations from individual metadata fields
  const formatCitation = (result: SearchResult) => {
    if (result.speaker && result.title) {
      // Conference talk format: Speaker, "Title", Session Year, ¶#
      let citation = `${result.speaker}, "${result.title}"`;
      if (result.session && result.year) {
        citation += `, ${result.session} ${result.year}`;
      }
      if (result.paragraph) {
        citation += `, ¶${result.paragraph}`;
      }
      return citation;
    } else if (result.book && result.chapter) {
      // Scripture format: Standard Work Book Chapter:Verse
      return `${result.source} ${result.book} ${result.chapter}${result.verse ? `:${result.verse}` : ''}`;
    } else if (result.source) {
      // Fallback to source name
      return result.source;
    }
    // Last resort - use cleaned original citation
    return result.citation?.replace(/^\((.+)\)$/, '$1') || 'Unknown Source';
  };

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
    'Q&A',
    'Come Follow Me'
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (isLoading) return;

    // For CFM mode, we don't need a query - just generate the lesson plan
    if (mode === 'Come Follow Me') {
      if (!cfmWeek) {
        // Show error message as assistant message
        const errorMessage: Message = { 
          id: Date.now(), 
          type: 'assistant', 
          content: 'Please select a Come Follow Me week in the sidebar before generating a lesson plan.'
        };
        setMessages(prev => [...prev, errorMessage]);
        return;
      }
      
      // Add a system message showing what we're generating
      const systemMessage: Message = { 
        id: Date.now(), 
        type: 'user', 
        content: `Generate ${cfmAudience} lesson plan for ${cfmWeek}`
      };
      setMessages(prev => [...prev, systemMessage]);
    } else {
      // For Q&A mode, require a question
      if (!query.trim()) return;
      
      // Add user message
      const userMessage: Message = { id: Date.now(), type: 'user', content: query };
      setMessages(prev => [...prev, userMessage]);
    }

    setIsLoading(true);
    const searchQuery = query;
    setQuery('');

    // Create assistant message that will be updated
    const assistantMessageId = Date.now() + 1;
    const initialAssistantMessage: Message = {
      id: assistantMessageId,
      type: 'assistant',
      content: '',
      results: [],
      searchTime: 0,
      isStreaming: true
    };
    setMessages(prev => [...prev, initialAssistantMessage]);

    // Initialize streaming state
    setStreamingContent('');
    setStreamingMessageId(assistantMessageId);

    try {
      if (mode === 'Come Follow Me') {
        // Handle CFM lesson plan generation
        console.log('Generating CFM lesson plan with:', { week: cfmWeek, audience: cfmAudience.toLowerCase() });
        
        const response = await generateCFMLessonPlan({
          week: cfmWeek,
          audience: cfmAudience.toLowerCase() === 'adult' ? 'adults' : cfmAudience.toLowerCase() as 'youth' | 'family' | 'children'
        });
        
        // Update the message with the lesson plan
        setMessages(prev => prev.map(msg => 
          msg.id === assistantMessageId 
            ? { ...msg, content: response.lesson_plan, isStreaming: false }
            : msg
        ));
        
        setStreamingMessageId(null);
        setStreamingContent('');
        setIsLoading(false);
      } else {
        // Handle regular Q&A streaming
        let fullAnswer = '';
        let sources: SearchResult[] = [];
        let searchTime = 0;

        console.log('Starting askQuestionStream with:', { query: searchQuery, mode, selectedSources });
        const startTime = Date.now();
        
        await askQuestionStream({
          query: searchQuery,
          mode,
          max_results: sourceCount,
          selectedSources
        }, (chunk: StreamChunk) => {
          const elapsed = Date.now() - startTime;
          console.log('🔥 Chunk received in ChatInterface:', chunk.type, chunk.content ? `"${chunk.content.slice(0, 30)}..."` : '', 'elapsed:', elapsed + 'ms');
          
          switch (chunk.type) {
            case 'search_complete':
              console.log('✅ Search complete, found', chunk.total_sources, 'sources');
              searchTime = (chunk.search_time_ms || 0) / 1000;
              // Don't show "Found X sources" message - just continue to content
              break;
              
            case 'content':
              if (chunk.content) {
                fullAnswer += chunk.content;
                console.log('📝 Content chunk added, fullAnswer length:', fullAnswer.length);
                
                // Update streaming state immediately
                console.log('🔄 Updating streaming content immediately:', fullAnswer.slice(-20));
                
                setStreamingContent(fullAnswer);
                
                // Also update React state (for final rendering)
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
              console.log('✅ Streaming done, final answer length:', fullAnswer.length);
              // Make sure final content is displayed and mark streaming as complete
              setMessages(prev => prev.map(msg => 
                msg.id === assistantMessageId 
                  ? { ...msg, content: fullAnswer, isStreaming: false }
                  : msg
              ));
              // Clear streaming state
              setStreamingMessageId(null);
              setStreamingContent('');
              setIsLoading(false);
              break;
              
            case 'error':
              setMessages(prev => prev.map(msg => 
                msg.id === assistantMessageId 
                  ? { ...msg, content: `Sorry, I encountered an error: ${chunk.error}`, isStreaming: false }
                  : msg
              ));
              setIsLoading(false);
              break;
          }
        });
      }
      
    } catch (error) {
      setMessages(prev => prev.map(msg => 
        msg.id === assistantMessageId 
          ? { ...msg, content: `Sorry, I encountered an error: ${error instanceof Error ? error.message : 'Unknown error'}`, isStreaming: false }
          : msg
      ));
      setStreamingMessageId(null);
      setStreamingContent('');
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-neutral-900 lg:ml-0">
      {/* Top-right mode selector */}
      <div className="absolute top-4 right-4 lg:top-6 lg:right-8 z-10">
        <div className="relative">
          <button
            type="button"
            onClick={() => setModeDropdownOpen(!modeDropdownOpen)}
            className="flex items-center justify-center space-x-2 bg-neutral-700/90 backdrop-blur-sm hover:bg-neutral-600/90 px-3 py-2 rounded-lg transition-colors shadow-lg border border-neutral-600/50"
          >
            <span className="text-white text-sm font-medium whitespace-nowrap">{mode}</span>
            <ChevronDownIcon className="w-4 h-4 text-neutral-400 flex-shrink-0" />
          </button>
          
          {modeDropdownOpen && (
            <div className="absolute top-full right-0 mt-2 bg-neutral-700 rounded-lg shadow-xl border border-neutral-600 py-2 min-w-40 z-50">
              {modes.map((modeOption) => (
                <button
                  key={modeOption}
                  type="button"
                  onClick={() => {
                    setMode(modeOption);
                    setModeDropdownOpen(false);
                  }}
                  className="block w-full px-4 py-2 text-left text-white hover:bg-neutral-600 transition-colors text-sm whitespace-nowrap"
                >
                  {modeOption}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Mobile hamburger menu */}
      <div className="lg:hidden flex items-center justify-between p-4 pr-20 border-b border-neutral-700">
        <button
          onClick={() => setSidebarOpen(true)}
          className="text-neutral-400 hover:text-white p-2"
        >
          <Bars3Icon className="w-6 h-6" />
        </button>
        <h1 className="text-lg font-semibold text-white">Gospel Study</h1>
        <div className="w-10"></div> {/* Spacer for centering */}
      </div>

      {/* Header with logo */}
      <div className="flex items-center justify-center pt-6 lg:pt-12 pb-4 lg:pb-6 px-4">
        <div className="flex flex-col items-center space-y-4 lg:space-y-6">
          <div className="w-16 h-16 lg:w-24 lg:h-24 rounded-full overflow-hidden border-2 border-neutral-700">
            <img 
              src="/christ.jpeg" 
              alt="Gospel Study Assistant Logo" 
              className="w-full h-full object-cover"
            />
          </div>
          <div className="text-center">
            <button 
              onClick={resetChat}
              className="text-2xl lg:text-4xl font-bold text-white mb-2 hover:text-blue-300 transition-colors cursor-pointer"
            >
              Gospel Study Assistant
            </button>
            <p className="text-sm lg:text-xl text-neutral-400 px-4">Ask questions. Find answers. Build faith.</p>
          </div>
        </div>
      </div>

      {/* Input area below header */}
      <div className="px-4 lg:px-8 pb-2">
        <div className="max-w-6xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center bg-neutral-800 border-2 border-neutral-700 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20 rounded-2xl p-3 lg:p-4 transition-all duration-200 gap-3 sm:gap-0">
              
              {mode === 'Come Follow Me' ? (
                // CFM Mode: Show lesson plan generation button
                <>
                  <div className="flex-1 flex items-center text-neutral-300 text-base lg:text-lg">
                    {cfmWeek ? (
                      <>Generate {cfmAudience} lesson plan for {cfmWeek}</>
                    ) : (
                      <>Select a week and audience in the sidebar to generate a lesson plan</>
                    )}
                  </div>
                  
                  <button
                    type="submit"
                    disabled={!cfmWeek || isLoading}
                    className="bg-blue-600 hover:bg-blue-500 disabled:bg-neutral-700 disabled:cursor-not-allowed px-6 py-2 lg:py-3 rounded-full transition-colors font-medium text-white"
                  >
                    {isLoading ? (
                      <div className="flex items-center space-x-2">
                        <div className="animate-spin rounded-full h-4 w-4 lg:h-5 lg:w-5 border-2 border-white border-t-transparent" />
                        <span>Generating...</span>
                      </div>
                    ) : (
                      'Generate Lesson Plan'
                    )}
                  </button>
                </>
              ) : (
                // Q&A Mode: Show text input
                <div className="flex items-center gap-3 w-full">
                  <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder={getPlaceholderText()}
                    className="flex-1 bg-transparent text-white placeholder-neutral-400 outline-none text-base lg:text-lg min-w-0"
                  />

                  <button
                    type="submit"
                    disabled={!query.trim() || isLoading}
                    className="bg-neutral-600 hover:bg-neutral-500 disabled:bg-neutral-700 disabled:cursor-not-allowed p-2 lg:p-3 rounded-full transition-colors flex-shrink-0"
                  >
                    {isLoading ? (
                      <div className="animate-spin rounded-full h-4 w-4 lg:h-5 lg:w-5 border-2 border-white border-t-transparent" />
                    ) : (
                      <PaperAirplaneIcon className="w-4 h-4 lg:w-5 lg:h-5 text-white" />
                    )}
                  </button>
                </div>
              )}
            </div>
          </form>
          
          {/* Audience selection - only show in Come Follow Me mode */}
          {mode === 'Come Follow Me' && (
            <div className="mt-4 flex justify-center">
              <div className="flex flex-wrap gap-2 justify-center">
                <span className="text-sm text-neutral-400 mr-2 flex items-center">Study audience:</span>
                {CFM_AUDIENCES.map((audience) => (
                  <button
                    key={audience.id}
                    onClick={() => setCfmAudience(audience.id)}
                    className={`px-3 py-1.5 text-sm rounded-lg transition-colors ${
                      cfmAudience === audience.id
                        ? 'bg-blue-600 text-white'
                        : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'
                    }`}
                  >
                    {audience.label}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 px-4 lg:px-6 pb-2 lg:pb-4 overflow-y-auto">
        {messages.length > 0 ? (
          <div className="max-w-6xl mx-auto space-y-6">
            {messages.map((message) => (
              <div key={message.id} className="space-y-4">
                {(message.type === 'user' || (message.type === 'assistant' && message.content)) && (
                  <div
                    className={`${
                      message.type === 'user'
                        ? 'bg-neutral-600 text-white ml-auto max-w-sm lg:max-w-lg p-3 lg:p-4 rounded-lg'
                        : 'bg-neutral-800 text-white max-w-full p-6 rounded-lg'
                    }`}
                  >
                    {message.type === 'assistant' ? (
                      message.content ? (
                        <div className="space-y-6 leading-relaxed text-neutral-100 max-w-none">
                          {message.isStreaming && message.id === streamingMessageId ? (
                            // During streaming, show the streaming content state
                            <div className="text-base leading-7 text-neutral-100 whitespace-pre-wrap">
                              {streamingContent}
                              <span className="inline-block w-2 h-4 bg-green-400 animate-pulse ml-1">|</span>
                            </div>
                          ) : (
                            // After streaming is complete, use full markdown rendering
                            <ReactMarkdown 
                              components={{
                                h1: ({ children }) => (
                                  <h1 className="text-xl font-semibold text-white mb-4 mt-6">
                                    {children}
                                  </h1>
                                ),
                                h2: ({ children }) => (
                                  <h2 className="text-lg font-semibold text-white mb-3 mt-5">
                                    {children}
                                  </h2>
                                ),
                                h3: ({ children }) => (
                                  <h3 className="text-base font-semibold text-white mb-3 mt-4">
                                    {children}
                                  </h3>
                                ),
                                h4: ({ children }) => (
                                  <h4 className="text-base font-medium text-white mb-2 mt-4">
                                    {children}
                                  </h4>
                                ),
                                p: ({ children }) => (
                                  <p className="text-neutral-300 leading-relaxed mb-4">
                                    {children}
                                  </p>
                                ),
                                strong: ({ children }) => (
                                  <strong className="font-semibold text-white">
                                    {children}
                                  </strong>
                                ),
                                em: ({ children }) => (
                                  <em className="italic text-neutral-300">
                                    {children}
                                  </em>
                                ),
                                ul: ({ children }) => (
                                  <ul className="space-y-2 mb-4 ml-4">
                                    {children}
                                  </ul>
                                ),
                                ol: ({ children }) => (
                                  <ol className="space-y-2 mb-4 ml-4 list-decimal list-inside">
                                    {children}
                                  </ol>
                                ),
                                li: ({ children }) => (
                                  <li className="text-neutral-300 leading-relaxed">
                                    {children}
                                  </li>
                                ),
                                blockquote: ({ children }) => (
                                  <blockquote className="border-l-2 border-neutral-600 pl-4 my-4 italic text-neutral-400">
                                    {children}
                                  </blockquote>
                                ),
                                code: ({ children }) => (
                                  <code className="bg-neutral-800 text-neutral-300 px-2 py-1 rounded text-sm">
                                    {children}
                                  </code>
                                ),
                                hr: () => (
                                  <hr className="border-neutral-600 my-6" />
                                )
                              }}
                            >
                              {message.content}
                            </ReactMarkdown>
                          )}
                        </div>
                      ) : null
                    ) : (
                      message.content
                    )}
                  </div>
                )}
                
                {/* Action buttons for assistant messages */}
                {message.type === 'assistant' && message.content && !message.isStreaming && (
                  <div className="flex justify-end gap-3 mt-6 pt-4 border-t border-neutral-700">
                    {/* Download PDF button - only show for Come Follow Me mode */}
                    {mode === 'Come Follow Me' && (
                      <button
                        onClick={() => handleDownloadPDF(message.content)}
                        className="inline-flex items-center px-4 py-2 text-sm text-neutral-300 hover:text-white bg-neutral-700 hover:bg-neutral-600 rounded-lg transition-all duration-200"
                      >
                        <ArrowDownTrayIcon className="w-4 h-4 mr-2" />
                        Download PDF
                      </button>
                    )}
                    
                    <button
                      onClick={resetChat}
                      className="inline-flex items-center px-4 py-2 text-sm text-neutral-300 hover:text-white bg-neutral-700 hover:bg-neutral-600 rounded-lg transition-all duration-200"
                    >
                      <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      Start New Conversation
                    </button>
                  </div>
                )}
                
                {/* Display search results */}
                {message.type === 'assistant' && message.results && message.results.length > 0 && (
                  <div className="space-y-3 ml-4">
                    <div className="text-sm text-neutral-400 font-medium mb-3 border-b border-neutral-700 pb-2">
                      References ({message.results.length})
                    </div>
                    {message.results.map((result, index) => (
                      <div key={index} className="bg-neutral-800 p-4 rounded-lg border border-neutral-600 hover:border-neutral-500 transition-colors">
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1">
                            {/* Citation */}
                            <div className="text-sm text-neutral-200 font-medium mb-2">
                              {formatCitation(result)}
                            </div>
                            
                            {/* URL Link */}
                            {result.url && (
                              <a 
                                href={result.url} 
                                target="_blank" 
                                rel="noopener noreferrer"
                                className="inline-flex items-center text-xs text-blue-400 hover:text-blue-300 transition-colors"
                              >
                                🔗 Read Full Text
                                <svg className="w-3 h-3 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                                </svg>
                              </a>
                            )}
                          </div>
                          
                          {/* Relevancy Indicator */}
                          <div className="flex flex-col items-end">
                            <div className="text-xs text-neutral-400 mb-1">Relevance</div>
                            <div className="flex items-center gap-2">
                              <div className="w-16 h-2 bg-neutral-700 rounded-full overflow-hidden">
                                <div 
                                  className={`h-full rounded-full transition-all ${
                                    result.score >= 0.8 ? 'bg-green-500' :
                                    result.score >= 0.6 ? 'bg-yellow-500' : 'bg-red-500'
                                  }`}
                                  style={{ width: `${Math.max(result.score * 100, 5)}%` }}
                                />
                              </div>
                              <span className="text-xs text-neutral-400 font-mono">
                                {(result.score * 100).toFixed(0)}%
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ))}
            
            {/* Loading indicator - only show for Q&A mode */}
            {isLoading && mode === 'Q&A' && (
              <div className="flex items-center justify-center p-4">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-neutral-500"></div>
                <span className="ml-3 text-neutral-400">Searching scriptures...</span>
              </div>
            )}
          </div>
        ) : (
          // Empty state - just take up minimal space
          <div className="flex-1"></div>
        )}
      </div>

      {/* Footer */}
      <div className="px-6 py-2 border-t border-neutral-700">
        <div className="max-w-6xl mx-auto flex items-center justify-between text-sm text-neutral-400">
          <div>© 2025 Gospel Study Assistant • AI-powered gospel study</div>
          <div className="flex space-x-6">
            <Link href="/terms" className="hover:text-white transition-colors">
              Terms of Use
            </Link>
            <Link href="/about" className="hover:text-white transition-colors">
              About
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}