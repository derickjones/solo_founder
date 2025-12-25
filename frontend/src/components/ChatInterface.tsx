'use client';

import { useState, useEffect, useRef } from 'react';
import { ChevronDownIcon, PaperAirplaneIcon, Bars3Icon, ArrowDownTrayIcon, ClipboardDocumentIcon, CheckIcon, ChevronRightIcon, UserCircleIcon } from '@heroicons/react/24/outline';
import { searchScriptures, SearchResult, askQuestionStream, StreamChunk, generateCFMDeepDiveStream, CFMStreamChunk, CFMDeepDiveRequest, generateCFMLessonPlan, CFMLessonPlanRequest, generateCFMAudioSummary, CFMAudioSummaryRequest, generateCFMCoreContent, CFMCoreContentRequest, generateTTS } from '@/services/api';
import ReactMarkdown from 'react-markdown';
import { generateLessonPlanPDF, LessonPlanData } from '@/utils/pdfGenerator';
import { CFM_AUDIENCES, CFM_2026_SCHEDULE, CFMWeek } from '@/utils/comeFollowMe';
import Link from 'next/link';
import AudioPlayer from './AudioPlayer';

// Add study type definition
type CFMStudyType = 'deep-dive' | 'lesson-plans' | 'audio-summary' | 'core-content';
type StudyLevel = 'essential' | 'connected' | 'scholarly';
type LessonPlanLevel = 'adult' | 'youth' | 'children';
type AudioSummaryLevel = 'short' | 'medium' | 'long';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  results?: SearchResult[];
  searchTime?: number;
  isStreaming?: boolean;
  audioFiles?: {
    combined?: string;
    host_only?: string;
    guest_only?: string;
  };
  audioTitle?: string;
}

interface ChatInterfaceProps {
  selectedSources: string[];
  sourceCount: number;
  sidebarOpen: boolean;
  setSidebarOpen: (open: boolean) => void;
  mode: string;
  setMode: (mode: string) => void;
  cfmAudience: string;
  setCfmAudience: (audience: string) => void;
  cfmWeek: CFMWeek;
  setCfmWeek: (week: CFMWeek) => void;
  cfmStudyType: CFMStudyType;
  setCfmStudyType: (type: CFMStudyType) => void;
  // Deep Dive Study levels
  cfmStudyLevel: StudyLevel;
  setCfmStudyLevel: (level: StudyLevel) => void;
  // Lesson Plan levels  
  cfmLessonPlanLevel: LessonPlanLevel;
  setCfmLessonPlanLevel: (level: LessonPlanLevel) => void;
  // Audio Summary levels
  cfmAudioSummaryLevel: AudioSummaryLevel;
  setCfmAudioSummaryLevel: (level: AudioSummaryLevel) => void;
}

export default function ChatInterface({ 
  selectedSources, 
  sourceCount, 
  sidebarOpen, 
  setSidebarOpen, 
  mode, 
  setMode, 
  cfmAudience, 
  setCfmAudience, 
  cfmWeek, 
  setCfmWeek, 
  cfmStudyType, 
  setCfmStudyType,
  cfmStudyLevel, 
  setCfmStudyLevel,
  cfmLessonPlanLevel,
  setCfmLessonPlanLevel,
  cfmAudioSummaryLevel,
  setCfmAudioSummaryLevel
}: ChatInterfaceProps) {
  const [query, setQuery] = useState('');
  const [modeDropdownOpen, setModeDropdownOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const [streamingMessageId, setStreamingMessageId] = useState<number | null>(null);
  const [copiedMessageId, setCopiedMessageId] = useState<number | null>(null);
  const [showProductTiles, setShowProductTiles] = useState(true);
  const [currentTileIndex, setCurrentTileIndex] = useState(0);
  const [generatingAudioForMessage, setGeneratingAudioForMessage] = useState<number | null>(null);
  
  // Ref for scrolling to bottom of messages
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Scroll behavior state
  const [isControlsVisible, setIsControlsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

  // Handle Listen button click - generate TTS for message content
  const handleListenToContent = async (messageId: number, content: string) => {
    setGeneratingAudioForMessage(messageId);
    try {
      const result = await generateTTS({
        text: content,
        voice: 'cfm_male',
        title: 'Deep Dive Audio'
      });
      
      // Update the message with audio data
      setMessages(prev => prev.map(msg => 
        msg.id === messageId 
          ? { 
              ...msg, 
              audioFiles: { combined: result.audio_base64 },
              audioTitle: result.title
            }
          : msg
      ));
    } catch (error) {
      console.error('Failed to generate audio:', error);
      alert('Failed to generate audio. Please try again.');
    } finally {
      setGeneratingAudioForMessage(null);
    }
  };

  // Copy to clipboard handler
  const handleCopyToClipboard = async (content: string, messageId: number) => {
    try {
      await navigator.clipboard.writeText(content);
      setCopiedMessageId(messageId);
      // Reset after 2 seconds
      setTimeout(() => setCopiedMessageId(null), 2000);
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
    }
  };

  // Scroll to bottom of messages
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Auto-scroll when content is generated - scroll detection handles hiding controls
  useEffect(() => {
    if (messages.length > 0 && !isLoading) {
      // Scroll to show the content - this will trigger the scroll handler to hide controls
      setTimeout(scrollToBottom, 100);
    }
  }, [messages, isLoading]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl+/ or Cmd+/ to toggle sidebar
      if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        setSidebarOpen(!sidebarOpen);
      }
      
      // Escape to close mode dropdown
      if (e.key === 'Escape') {
        if (modeDropdownOpen) {
          setModeDropdownOpen(false);
        }
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [sidebarOpen, setSidebarOpen, modeDropdownOpen]);

  // Scroll behavior for hiding/showing controls
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      
      // On all devices: scroll up reveals controls, scroll down hides them (when there's content)
      if (messages.length > 0) {
        if (currentScrollY > lastScrollY && currentScrollY > 100) {
          // Scrolling down and past threshold - hide controls
          setIsControlsVisible(false);
        } else if (currentScrollY < lastScrollY || currentScrollY <= 50) {
          // Scrolling up or near top - show controls
          setIsControlsVisible(true);
        }
      }
      
      setLastScrollY(currentScrollY);
    };

    const throttledHandleScroll = () => {
      requestAnimationFrame(handleScroll);
    };

    window.addEventListener('scroll', throttledHandleScroll, { passive: true });
    return () => window.removeEventListener('scroll', throttledHandleScroll);
  }, [lastScrollY, messages.length]);

  // Product tiles data
  const productTiles = [
    {
      title: "Reliable Gospel Study",
      content: [
        "Q&A mode for instant answers to gospel questions",
        "Come Follow Me mode for lesson planning", 
        "Search Standard Works, General Conference, and CFM curriculum",
        "All answers include exact citations for verification"
      ],
      action: "Try Q&A"
    },
    {
      title: "Customize Your Study",
      content: [
        "Select specific Come Follow Me weeks from sidebar",
        "Choose target audience: adults, families, youth, or children",
        "Switch seamlessly between Q&A and lesson planning modes",
        "Tailor content to your teaching needs"
      ],
      action: "Explore Sidebar"
    },
    {
      title: "Unlimited Study Power",
      content: [
        "Free: Basic Q&A with daily question limits",
        "Premium ($4.99/month): Unlimited questions and lesson plans",
        "Generate PDF exports for offline use",
        "Save hours of preparation time each week"
      ],
      action: "Start Free Trial"
    }
  ];

  // Auto-hide product tiles after 30 seconds and auto-scroll
  useEffect(() => {
    if (!showProductTiles) return;

    // Auto-scroll tiles every 4 seconds
    const scrollInterval = setInterval(() => {
      setCurrentTileIndex((prev) => (prev + 1) % productTiles.length);
    }, 4000);

    // Hide tiles after 30 seconds
    const hideTimer = setTimeout(() => {
      setShowProductTiles(false);
    }, 30000);

    return () => {
      clearInterval(scrollInterval);
      clearTimeout(hideTimer);
    };
  }, [showProductTiles, productTiles.length]);

  // Hide tiles when user starts interacting (typing or sending messages)
  useEffect(() => {
    if (messages.length > 0 || query.length > 0) {
      setShowProductTiles(false);
    }
  }, [messages.length, query.length]);

  // PDF download handler
  const handleDownloadPDF = async (messageContent: string) => {
    try {
      // Extract lesson plan details from the message content or current state
      const lessonData: LessonPlanData = {
        title: `${cfmAudience} Lesson Plan`,
        date: cfmWeek?.dates || '',
        audience: cfmAudience,
        content: messageContent,
        scripture: cfmWeek?.reference || '' // Using week reference as scripture
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
        if (cfmStudyType === 'deep-dive') {
          // Handle CFM deep dive generation with streaming
          
          // Get week number from CFM schedule
          const weekIndex = CFM_2026_SCHEDULE.findIndex((w: CFMWeek) => w.id === cfmWeek?.id);
          const weekNumber = weekIndex >= 0 ? weekIndex + 1 : 1;
          
          let fullContent = '';
          
          try {
            console.log('Starting CFM Deep Dive streaming...');
            await generateCFMDeepDiveStream(
              {
                week_number: weekNumber,
                study_level: cfmStudyLevel
              },
              (chunk: CFMStreamChunk) => {
                console.log('CFM Stream chunk received:', chunk);
                if (chunk.type === 'content' && chunk.content) {
                  fullContent += chunk.content;
                  
                  // Update streaming state immediately
                  setStreamingContent(fullContent);
                  
                  // Update the message with streaming content
                  setMessages(prev => prev.map(msg => 
                    msg.id === assistantMessageId 
                      ? { ...msg, content: fullContent, isStreaming: true }
                      : msg
                  ));
                }
              }
            );
            console.log('CFM Deep Dive streaming completed');
          } catch (error) {
            console.error('CFM Deep Dive streaming error:', error);
            
            // Update the message with error
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { ...msg, content: `Sorry, I encountered an error generating the study guide: ${error}`, isStreaming: false }
                : msg
            ));
          }
          
          // Finalize the message
          setMessages(prev => prev.map(msg => 
            msg.id === assistantMessageId 
              ? { ...msg, isStreaming: false }
              : msg
          ));
          
          // Auto-hide controls to give full screen to content
          setIsControlsVisible(false);
          
          setStreamingMessageId(null);
          setStreamingContent('');
          setIsLoading(false);
        } else {
          // Handle lesson plans and audio summaries with actual API calls
          
          // Get week number from CFM schedule
          const weekIndex = CFM_2026_SCHEDULE.findIndex((w: CFMWeek) => w.id === cfmWeek?.id);
          const weekNumber = weekIndex >= 0 ? weekIndex + 1 : 1;
          
          if (cfmStudyType === 'lesson-plans') {
            const response = await generateCFMLessonPlan({
              week_number: weekNumber,
              audience: cfmLessonPlanLevel
            });
            
            // Update the message with the lesson plan
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { ...msg, content: response.lesson_plan, isStreaming: false }
                : msg
            ));
            
            // Auto-hide controls to give full screen to content
            setIsControlsVisible(false);
          } else if (cfmStudyType === 'audio-summary') {
            // Map our frontend types to backend study level
            const studyLevelMap = {
              'short': 'essential' as const,
              'medium': 'connected' as const,
              'long': 'scholarly' as const
            };
            
            const response = await generateCFMAudioSummary({
              week_number: weekNumber,
              study_level: studyLevelMap[cfmAudioSummaryLevel]
              // No voice parameter - just generate the script, audio generated on Listen click
            });
            
            // Update the message with the audio summary transcript
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { 
                    ...msg, 
                    content: response.audio_script, // Show the audio script text
                    audioFiles: undefined, // Audio will be generated when Listen is clicked
                    audioTitle: `Week ${response.week_number} Audio Summary (${studyLevelMap[cfmAudioSummaryLevel]})`,
                    isStreaming: false 
                  }
                : msg
            ));
            
            // Auto-hide controls to give full screen to content
            setIsControlsVisible(false);
          } else if (cfmStudyType === 'core-content') {
            const response = await generateCFMCoreContent({
              week_number: weekNumber
            });
            
            // Update the message with the organized core content
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { ...msg, content: response.core_content, isStreaming: false }
                : msg
            ));
            
            // Auto-hide controls to give full screen to content
            setIsControlsVisible(false);
          }
          
          setStreamingMessageId(null);
          setStreamingContent('');
          setIsLoading(false);
        }
      } else {
        // Handle regular Q&A streaming
        let fullAnswer = '';
        let sources: SearchResult[] = [];
        let searchTime = 0;

        const startTime = Date.now();
        
        await askQuestionStream({
          query: searchQuery,
          mode,
          max_results: sourceCount,
          selectedSources
        }, (chunk: StreamChunk) => {
          const elapsed = Date.now() - startTime;
          
          switch (chunk.type) {
            case 'search_complete':
              searchTime = (chunk.search_time_ms || 0) / 1000;
              break;
              
            case 'content':
              if (chunk.content) {
                fullAnswer += chunk.content;
                
                // Update streaming state immediately
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
      {/* Desktop sidebar toggle button - only show when sidebar is closed */}
      {!sidebarOpen && (
        <button
          onClick={() => setSidebarOpen(true)}
          className="hidden lg:block fixed top-6 left-6 z-20 text-neutral-400 hover:text-neutral-200 p-2 rounded-lg hover:bg-neutral-700/50 bg-neutral-800/90 backdrop-blur-sm border border-neutral-600/50 transition-all"
          title="Open sidebar"
        >
          <Bars3Icon className="w-5 h-5" />
        </button>
      )}
      
      {/* Top-right mode selector */}
      <div className="absolute top-4 right-4 lg:top-6 lg:right-8 z-10">
        <div className="relative">
          <button
            type="button"
            onClick={() => setModeDropdownOpen(!modeDropdownOpen)}
            className={`flex items-center justify-center space-x-2 backdrop-blur-sm px-3 py-2 rounded-lg transition-all duration-200 shadow-lg ${
              mode === 'Come Follow Me'
                ? 'bg-blue-500/20 hover:bg-blue-500/30 border border-blue-400/50 text-blue-300'
                : 'bg-neutral-700/90 hover:bg-neutral-600/90 border border-neutral-600/50 text-white'
            }`}
          >
            <span className="text-sm font-medium whitespace-nowrap">{mode}</span>
            <ChevronDownIcon className={`w-4 h-4 flex-shrink-0 ${
              mode === 'Come Follow Me' ? 'text-blue-400' : 'text-neutral-400'
            }`} />
          </button>
          
          {modeDropdownOpen && (
            <div className="absolute top-full right-0 mt-2 bg-neutral-800/95 backdrop-blur-sm rounded-xl shadow-xl border border-neutral-700/50 py-2 min-w-40 z-50">
              {modes.map((modeOption) => (
                <button
                  key={modeOption}
                  type="button"
                  onClick={() => {
                    setMode(modeOption);
                    setModeDropdownOpen(false);
                  }}
                  className={`relative block w-full px-4 py-2.5 text-left transition-all duration-200 text-sm whitespace-nowrap ${
                    mode === modeOption
                      ? 'bg-blue-500/20 text-blue-300 shadow-lg shadow-blue-500/20 border-l-2 border-blue-400'
                      : 'text-neutral-300 hover:bg-neutral-700/50 hover:text-white/80'
                  }`}
                >
                  {modeOption}
                </button>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* Mobile hamburger menu */}
      <div className={`lg:hidden flex items-center justify-between p-4 border-b border-neutral-700 transition-all duration-300 ease-in-out ${
        !isControlsVisible && messages.length > 0 ? 'max-h-0 opacity-0 overflow-hidden py-0 border-b-0' : 'max-h-20 opacity-100'
      }`}>
        <button
          onClick={() => setSidebarOpen(true)}
          className="text-neutral-400 hover:text-white p-2"
        >
          <Bars3Icon className="w-6 h-6" />
        </button>
        <div className="w-10"></div> {/* Spacer */}
        <div className="w-10"></div> {/* Spacer for centering */}
      </div>

      {/* Header with logo - always visible, compact when content is shown */}
      <div className={`relative flex items-center justify-center px-4 transition-all duration-300 ease-in-out shrink-0 ${
        messages.length > 0 ? 'pt-3 pb-2 lg:pt-4 lg:pb-3' : 'pt-6 lg:pt-12 pb-4 lg:pb-6'
      }`}>
        <div className={`flex items-center transition-all duration-300 ${
          messages.length > 0 ? 'flex-row space-x-3 lg:space-x-4' : 'flex-col space-y-4 lg:space-y-6'
        }`}>
          <div className={`rounded-full overflow-hidden border-2 border-neutral-700 transition-all duration-300 ${
            messages.length > 0 ? 'w-10 h-10 lg:w-12 lg:h-12' : 'w-16 h-16 lg:w-24 lg:h-24'
          }`}>
            <img 
              src="/christ.jpeg" 
              alt="Gospel Study Assistant Logo" 
              className="w-full h-full object-cover"
            />
          </div>
          <div className={messages.length > 0 ? '' : 'text-center'}>
            <button 
              onClick={resetChat}
              className={`font-bold text-white hover:text-blue-300 transition-colors cursor-pointer ${
                messages.length > 0 ? 'text-lg lg:text-xl' : 'text-2xl lg:text-4xl mb-2'
              }`}
            >
              Gospel Study Assistant
            </button>
            {messages.length === 0 && (
              <p className="text-sm lg:text-xl text-neutral-400 px-4">Ask questions. Find answers. Build faith.</p>
            )}
          </div>
        </div>
      </div>

      {/* Input area below header - collapses when content is shown or loading */}
      <div className={`px-4 lg:px-8 pb-2 transition-all duration-300 ease-in-out overflow-hidden shrink-0 ${
        (isLoading || (!isControlsVisible && messages.length > 0)) ? 'max-h-0 opacity-0' : 'opacity-100'
      }`}>
        <div className="max-w-6xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            <div className="flex flex-col sm:flex-row items-stretch sm:items-center bg-neutral-800 border-2 border-neutral-700 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20 rounded-2xl p-3 lg:p-4 transition-all duration-200 gap-3 sm:gap-0">
              
              {mode === 'Come Follow Me' ? (
                // CFM Mode: Enhanced Study Guide Interface
                <div className="w-full space-y-4 md:space-y-6 max-h-[70vh] md:max-h-none overflow-y-auto md:overflow-visible">
                  {/* Study Controls */}
                  <div className="grid grid-cols-1 gap-4 md:gap-6">
                    {/* Week Selection */}
                    <div className="space-y-2 md:space-y-3">
                      <label className="text-xs font-medium text-neutral-400 uppercase tracking-wider">Current Week</label>
                      <select
                        value={cfmWeek?.id || ''}
                        onChange={(e) => {
                          const selectedWeek = CFM_2026_SCHEDULE.find((w: CFMWeek) => w.id === e.target.value);
                          setCfmWeek(selectedWeek || CFM_2026_SCHEDULE[0]);
                        }}
                        className="w-full p-2 md:p-3 bg-neutral-700/50 border border-neutral-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 appearance-none cursor-pointer"
                      >
                        {CFM_2026_SCHEDULE.map((week: CFMWeek, index: number) => (
                          <option key={week.id} value={week.id} className="bg-neutral-800">
                            {week.lesson}
                          </option>
                        ))}
                      </select>
                      <div className="text-xs text-neutral-500 space-y-1">
                        <div>{cfmWeek?.dates}</div>
                        <div className="font-medium text-neutral-400">{cfmWeek?.reference}</div>
                      </div>
                    </div>

                    {/* Study Type Selection */}
                    <div className="space-y-2 md:space-y-3">
                      <label className="text-xs font-medium text-neutral-400 uppercase tracking-wider">Study Type</label>
                      <div className="grid grid-cols-2 lg:grid-cols-4 gap-2">
                        <button
                          type="button"
                          onClick={() => setCfmStudyType('deep-dive')}
                          className={`p-2 md:p-3 rounded-lg text-xs md:text-sm font-medium transition-all duration-200 border ${
                            cfmStudyType === 'deep-dive'
                              ? 'bg-blue-600/80 border-blue-500 text-white shadow-lg shadow-blue-500/30'
                              : 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-blue-600/20 hover:border-blue-500/50'
                          }`}
                        >
                          Deep Dive
                        </button>
                        <button
                          type="button"
                          onClick={() => setCfmStudyType('lesson-plans')}
                          className={`p-2 md:p-3 rounded-lg text-xs md:text-sm font-medium transition-all duration-200 border ${
                            cfmStudyType === 'lesson-plans'
                              ? 'bg-purple-600/80 border-purple-500 text-white shadow-lg shadow-purple-500/30'
                              : 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-purple-600/20 hover:border-purple-500/50'
                          }`}
                        >
                          Lesson Plans
                        </button>
                        <button
                          type="button"
                          onClick={() => setCfmStudyType('audio-summary')}
                          className={`p-2 md:p-3 rounded-lg text-xs md:text-sm font-medium transition-all duration-200 border ${
                            cfmStudyType === 'audio-summary'
                              ? 'bg-emerald-600/80 border-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                              : 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-emerald-600/20 hover:border-emerald-500/50'
                          }`}
                        >
                          Audio
                        </button>
                        <button
                          type="button"
                          onClick={() => setCfmStudyType('core-content')}
                          className={`p-2 md:p-3 rounded-lg text-xs md:text-sm font-medium transition-all duration-200 border ${
                            cfmStudyType === 'core-content'
                              ? 'bg-amber-600/80 border-amber-500 text-white shadow-lg shadow-amber-500/30'
                              : 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-amber-600/20 hover:border-amber-500/50'
                          }`}
                        >
                          Core
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Dynamic Level Selection Based on Study Type - Centered */}
                  <div className="max-w-2xl mx-auto">
                    <div className="space-y-3">
                      {cfmStudyType === 'deep-dive' && (
                        <>
                          <label className="text-xs font-medium text-neutral-400 uppercase tracking-wider text-center block">Study Level</label>
                          <div className="bg-neutral-700/30 p-2 md:p-4 rounded-lg">
                            <div className="grid grid-cols-3 gap-2">
                              {[
                                { level: 'essential', label: 'Essential', color: 'emerald' },
                                { level: 'connected', label: 'Connected', color: 'purple' },
                                { level: 'scholarly', label: 'Scholarly', color: 'amber' }
                              ].map(({ level, label, color }) => (
                                <button
                                  key={level}
                                  type="button"
                                  onClick={() => setCfmStudyLevel(level as StudyLevel)}
                                  className={`p-2 md:p-3 rounded-lg text-xs md:text-sm font-medium transition-all duration-200 border ${
                                    cfmStudyLevel === level
                                      ? color === 'emerald' 
                                        ? 'bg-emerald-600/80 border-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                                        : color === 'purple'
                                        ? 'bg-purple-600/80 border-purple-500 text-white shadow-lg shadow-purple-500/30'
                                        : 'bg-amber-600/80 border-amber-500 text-white shadow-lg shadow-amber-500/30'
                                      : color === 'emerald'
                                        ? 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-emerald-600/20 hover:border-emerald-500/50'
                                        : color === 'purple'
                                        ? 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-purple-600/20 hover:border-purple-500/50'
                                        : 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-amber-600/20 hover:border-amber-500/50'
                                  }`}
                                >
                                  {label}
                                </button>
                              ))}
                            </div>
                          </div>
                        </>
                      )}
                      
                      {cfmStudyType === 'lesson-plans' && (
                        <>
                          <label className="text-xs font-medium text-neutral-400 uppercase tracking-wider text-center block">Audience</label>
                          <div className="bg-neutral-700/30 p-2 md:p-4 rounded-lg">
                            <div className="grid grid-cols-3 gap-2">
                              {[
                                { level: 'adult', color: 'purple' },
                                { level: 'youth', color: 'blue' },
                                { level: 'children', color: 'emerald' }
                              ].map(({ level, color }) => (
                                <button
                                  key={level}
                                  type="button"
                                  onClick={() => setCfmLessonPlanLevel(level as LessonPlanLevel)}
                                  className={`p-2 md:p-3 rounded-lg text-xs md:text-sm font-medium transition-all duration-200 border capitalize ${
                                    cfmLessonPlanLevel === level
                                      ? color === 'purple'
                                        ? 'bg-purple-600/80 border-purple-500 text-white shadow-lg shadow-purple-500/30'
                                        : color === 'blue'
                                        ? 'bg-blue-600/80 border-blue-500 text-white shadow-lg shadow-blue-500/30'
                                        : 'bg-emerald-600/80 border-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                                      : color === 'purple'
                                        ? 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-purple-600/20 hover:border-purple-500/50'
                                        : color === 'blue'
                                        ? 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-blue-600/20 hover:border-blue-500/50'
                                        : 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-emerald-600/20 hover:border-emerald-500/50'
                                  }`}
                                >
                                  {level}
                                </button>
                              ))}
                            </div>
                          </div>
                        </>
                      )}
                      
                      {cfmStudyType === 'audio-summary' && (
                        <>
                          <label className="text-xs font-medium text-neutral-400 uppercase tracking-wider text-center block">Study Level</label>
                          <div className="bg-neutral-700/30 p-2 md:p-4 rounded-lg">
                            <div className="grid grid-cols-3 gap-2">
                              {[
                                { level: 'short', label: 'Essential', color: 'emerald' },
                                { level: 'medium', label: 'Connected', color: 'purple' },
                                { level: 'long', label: 'Scholarly', color: 'amber' }
                              ].map(({ level, label, color }) => (
                                <button
                                  key={level}
                                  type="button"
                                  onClick={() => setCfmAudioSummaryLevel(level as AudioSummaryLevel)}
                                  className={`p-2 md:p-3 rounded-lg text-xs md:text-sm font-medium transition-all duration-200 border ${
                                    cfmAudioSummaryLevel === level
                                      ? color === 'emerald' 
                                        ? 'bg-emerald-600/80 border-emerald-500 text-white shadow-lg shadow-emerald-500/30'
                                        : color === 'purple'
                                        ? 'bg-purple-600/80 border-purple-500 text-white shadow-lg shadow-purple-500/30'
                                        : 'bg-amber-600/80 border-amber-500 text-white shadow-lg shadow-amber-500/30'
                                      : color === 'emerald'
                                        ? 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-emerald-600/20 hover:border-emerald-500/50'
                                        : color === 'purple'
                                        ? 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-purple-600/20 hover:border-purple-500/50'
                                        : 'bg-neutral-700/50 border-neutral-600 text-neutral-300 hover:bg-amber-600/20 hover:border-amber-500/50'
                                  }`}
                                >
                                  {label}
                                </button>
                              ))}
                            </div>
                          </div>
                        </>
                      )}

                      {cfmStudyType === 'core-content' && (
                        <></>
                      )}
                    </div>
                  </div>

                  {/* Generate Button */}
                  <button
                    type="submit"
                    disabled={!cfmWeek || isLoading}
                    className="w-full relative bg-blue-600/80 hover:bg-blue-600 disabled:bg-neutral-800/50 disabled:cursor-not-allowed px-6 py-4 rounded-xl transition-all duration-200 font-medium text-white hover:text-blue-50 disabled:text-neutral-500 shadow-lg shadow-blue-500/30 hover:shadow-blue-500/40 border border-blue-500/50 hover:border-blue-400 disabled:border-neutral-700/30 disabled:shadow-none"
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center space-x-2">
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent" />
                        <span>
                          {cfmStudyType === 'deep-dive' && `Generating Deep Dive...`}
                          {cfmStudyType === 'lesson-plans' && `Creating ${cfmLessonPlanLevel.charAt(0).toUpperCase() + cfmLessonPlanLevel.slice(1)} Lesson Plan...`}
                          {cfmStudyType === 'audio-summary' && `Generating ${
                            cfmAudioSummaryLevel === 'short' ? 'Essential' :
                            cfmAudioSummaryLevel === 'medium' ? 'Connected' :
                            cfmAudioSummaryLevel === 'long' ? 'Scholarly' : 'Essential'
                          } Audio Summary...`}
                          {cfmStudyType === 'core-content' && `Organizing Core Content...`}
                        </span>
                      </div>
                    ) : (
                      <>
                        <span className="text-lg">
                          {cfmStudyType === 'deep-dive' && `Generate Deep Dive`}
                          {cfmStudyType === 'lesson-plans' && `Create ${cfmLessonPlanLevel.charAt(0).toUpperCase() + cfmLessonPlanLevel.slice(1)} Lesson Plan`}
                          {cfmStudyType === 'audio-summary' && `Generate ${
                            cfmAudioSummaryLevel === 'short' ? 'Essential' :
                            cfmAudioSummaryLevel === 'medium' ? 'Connected' :
                            cfmAudioSummaryLevel === 'long' ? 'Scholarly' : 'Essential'
                          } Audio Summary`}
                          {cfmStudyType === 'core-content' && `Organize Core Content`}
                        </span>
                      </>
                    )}
                  </button>

                  {/* Mobile collapse button - only show when controls are visible on mobile */}
                  {isControlsVisible && (
                    <button
                      type="button"
                      onClick={() => setIsControlsVisible(false)}
                      className="md:hidden w-full mt-2 bg-neutral-700/50 hover:bg-neutral-600/50 text-neutral-300 py-2 px-4 rounded-lg transition-all duration-200 text-sm flex items-center justify-center space-x-2"
                    >
                      <ChevronDownIcon className="w-4 h-4" />
                      <span>Hide Controls</span>
                    </button>
                  )}
                </div>
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
        </div>
      </div>

      {/* Messages area */}
      <div className="flex-1 min-h-0 px-4 lg:px-6 pb-2 lg:pb-4 overflow-y-auto">
        {messages.length > 0 ? (
          <div className="max-w-6xl mx-auto space-y-6">
            {messages.map((message) => (
              <div key={message.id} className="space-y-4">
                {/* Show user messages, assistant messages with content, or assistant messages that are loading */}
                {(message.type === 'user' || (message.type === 'assistant' && (message.content || message.audioFiles || message.isStreaming))) && (
                  <div
                    className={`${
                      message.type === 'user'
                        ? 'bg-neutral-600 text-white ml-auto max-w-sm lg:max-w-lg p-3 lg:p-4 rounded-lg'
                        : 'bg-neutral-800 text-white max-w-full p-6 rounded-lg'
                    }`}
                  >
                    {/* CFM Study Guide Header */}
                    {message.type === 'assistant' && mode === 'Come Follow Me' && message.content && (
                      <div className="mb-6 pb-4 border-b border-neutral-600">
                        <div className="flex items-center justify-between mb-3">
                          <div>
                            <h2 className="text-xl font-bold text-neutral-200 mb-2">
                              {cfmStudyType === 'deep-dive' && `${cfmStudyLevel.charAt(0).toUpperCase() + cfmStudyLevel.slice(1)} Deep Dive`}
                              {cfmStudyType === 'lesson-plans' && `${cfmLessonPlanLevel.charAt(0).toUpperCase() + cfmLessonPlanLevel.slice(1)} Lesson Plan`}
                              {cfmStudyType === 'audio-summary' && `${
                                cfmAudioSummaryLevel === 'short' ? 'Essential' :
                                cfmAudioSummaryLevel === 'medium' ? 'Connected' :
                                cfmAudioSummaryLevel === 'long' ? 'Scholarly' : 'Essential'
                              } Audio Summary`}
                              {cfmStudyType === 'core-content' && `Core Content`}
                            </h2>
                            <div className="text-sm text-neutral-300">
                              {cfmWeek?.lesson} • {cfmWeek?.dates}
                            </div>
                            <div className="text-xs text-neutral-400 mt-1">
                              {cfmWeek?.reference}
                            </div>
                          </div>
                        </div>
                      </div>
                    )}
                    {message.type === 'assistant' ? (
                      message.content ? (
                        <div className="space-y-6 leading-relaxed text-neutral-100 max-w-none">
                          {/* Audio Player - shown when audio has been generated */}
                          {message.audioFiles?.combined && (
                            <div className="mb-6">
                              <AudioPlayer 
                                audioFiles={message.audioFiles}
                                title={message.audioTitle || 'Audio'}
                              />
                            </div>
                          )}
                          
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
                                  <h1 className={`text-xl font-semibold mb-4 mt-6 ${mode === 'Come Follow Me' ? 'text-blue-200' : 'text-white'}`}>
                                    {children}
                                  </h1>
                                ),
                                h2: ({ children }) => (
                                  <h2 className={`text-lg font-semibold mb-3 mt-5 ${mode === 'Come Follow Me' ? 'text-blue-300' : 'text-white'}`}>
                                    {children}
                                  </h2>
                                ),
                                h3: ({ children }) => (
                                  <h3 className={`text-base font-semibold mb-3 mt-4 ${mode === 'Come Follow Me' ? 'text-yellow-300' : 'text-white'}`}>
                                    {children}
                                  </h3>
                                ),
                                h4: ({ children }) => (
                                  <h4 className={`text-base font-medium mb-2 mt-4 ${mode === 'Come Follow Me' ? 'text-yellow-200' : 'text-white'}`}>
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
                                  <blockquote className={`border-l-2 pl-4 my-4 italic ${
                                    mode === 'Come Follow Me' 
                                    ? 'border-blue-400 text-blue-200 bg-blue-900/20 py-3 rounded-r-lg' 
                                    : 'border-neutral-600 text-neutral-400'
                                  }`}>
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
                      ) : message.isStreaming ? (
                        // Show loading indicator when streaming but no content yet
                        <div className="flex flex-col items-center justify-center py-12 space-y-4">
                          <div className="relative">
                            <div className="w-16 h-16 border-4 border-neutral-600 border-t-blue-500 rounded-full animate-spin"></div>
                          </div>
                          <div className="text-center">
                            <p className="text-lg font-medium text-neutral-200">
                              {cfmStudyType === 'deep-dive' && 'Generating Deep Dive Study...'}
                              {cfmStudyType === 'lesson-plans' && `Creating ${cfmLessonPlanLevel.charAt(0).toUpperCase() + cfmLessonPlanLevel.slice(1)} Lesson Plan...`}
                              {cfmStudyType === 'audio-summary' && 'Generating Audio Summary...'}
                              {cfmStudyType === 'core-content' && 'Organizing Core Content...'}
                              {mode !== 'Come Follow Me' && 'Thinking...'}
                            </p>
                            <p className="text-sm text-neutral-400 mt-2">This may take a moment</p>
                          </div>
                        </div>
                      ) : null
                    ) : (
                      message.content
                    )}
                  </div>
                )}
                
                {/* Action buttons for assistant messages */}
                {message.type === 'assistant' && message.content && !message.isStreaming && (
                  <div className="flex flex-wrap justify-end gap-3 mt-6 pt-4 border-t border-neutral-700">
                    {/* Listen button - for all CFM content types (Deep Dive, Lesson Plans, Audio Summary, Core Content) */}
                    {/* Show when: CFM mode AND no audio files yet generated */}
                    {mode === 'Come Follow Me' && !message.audioFiles?.combined && (
                      <button
                        onClick={() => handleListenToContent(message.id, message.content)}
                        disabled={generatingAudioForMessage === message.id}
                        className="inline-flex items-center px-4 py-2 text-sm text-neutral-300 hover:text-white bg-emerald-700/80 hover:bg-emerald-600 disabled:bg-emerald-800/50 disabled:cursor-wait rounded-lg transition-all duration-200"
                      >
                        {generatingAudioForMessage === message.id ? (
                          <>
                            <svg className="animate-spin w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24">
                              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                            </svg>
                            Generating Audio...
                          </>
                        ) : (
                          <>
                            <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z" />
                            </svg>
                            🎧 Listen
                          </>
                        )}
                      </button>
                    )}
                    
                    {/* Copy button */}
                    <button
                      onClick={() => handleCopyToClipboard(message.content, message.id)}
                      className="relative inline-flex items-center px-4 py-2 text-sm font-medium rounded-lg transition-all duration-200 bg-neutral-800/30 text-neutral-400 hover:text-white/80 hover:bg-neutral-800/50 border border-neutral-700/30"
                    >
                      {copiedMessageId === message.id ? (
                        <>
                          <CheckIcon className="w-4 h-4 mr-2 text-green-400" />
                          Copied!
                        </>
                      ) : (
                        <>
                          <ClipboardDocumentIcon className="w-4 h-4 mr-2" />
                          Copy
                        </>
                      )}
                    </button>
                    
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
            
            {/* Scroll anchor - this element is used to scroll to the bottom */}
            <div ref={messagesEndRef} />
          </div>
        ) : (
          // Empty state with product explanation tiles
          <div className="flex-1 flex items-center justify-center px-4">
            {showProductTiles && (
              <div className="max-w-6xl mx-auto">
                {/* Desktop: 3-column grid */}
                <div className="hidden lg:grid lg:grid-cols-3 gap-6">
                  {productTiles.map((tile, index) => {
                    const tileColors = [
                      { bg: "bg-blue-900/20", border: "border-blue-700/30", hover: "hover:bg-blue-800/30", hoverBorder: "hover:border-blue-500/50", accent: "text-blue-400", hoverAccent: "text-blue-300" },
                      { bg: "bg-purple-900/20", border: "border-purple-700/30", hover: "hover:bg-purple-800/30", hoverBorder: "hover:border-purple-500/50", accent: "text-purple-400", hoverAccent: "text-purple-300" },
                      { bg: "bg-emerald-900/20", border: "border-emerald-700/30", hover: "hover:bg-emerald-800/30", hoverBorder: "hover:border-emerald-500/50", accent: "text-emerald-400", hoverAccent: "text-emerald-300" }
                    ];
                    const colors = tileColors[index];
                    
                    return (
                      <div
                        key={index}
                        className={`${colors.bg} border ${colors.border} rounded-xl p-6 ${colors.hover} transition-all duration-300 ${colors.hoverBorder} group`}
                      >
                        <h3 className={`text-lg font-semibold text-white mb-4 group-hover:${colors.hoverAccent} transition-colors`}>
                          {tile.title}
                        </h3>
                        <ul className="text-neutral-400 text-sm leading-relaxed mb-6 space-y-2 group-hover:text-neutral-300 transition-colors">
                          {tile.content.map((item, i) => (
                            <li key={i} className="flex items-start">
                              <span className={`${colors.accent} mr-2 mt-1`}>•</span>
                              <span>{item}</span>
                            </li>
                          ))}
                        </ul>
                        <button className={`${colors.accent} hover:${colors.hoverAccent} text-sm font-medium transition-colors`}>
                          {tile.action} →
                        </button>
                      </div>
                    );
                  })}
                </div>

                {/* Mobile: Scrolling carousel */}
                <div className="lg:hidden">
                  <div className="relative">
                    {(() => {
                      const tileColors = [
                        { bg: "bg-blue-900/20", border: "border-blue-700/30", accent: "text-blue-400", hoverAccent: "text-blue-300" },
                        { bg: "bg-purple-900/20", border: "border-purple-700/30", accent: "text-purple-400", hoverAccent: "text-purple-300" },
                        { bg: "bg-emerald-900/20", border: "border-emerald-700/30", accent: "text-emerald-400", hoverAccent: "text-emerald-300" }
                      ];
                      const colors = tileColors[currentTileIndex];
                      
                      return (
                        <div className={`${colors.bg} border ${colors.border} rounded-xl p-6 min-h-[320px] flex flex-col`}>
                          <h3 className={`text-lg font-semibold text-white mb-4 ${colors.hoverAccent}`}>
                            {productTiles[currentTileIndex].title}
                          </h3>
                          <ul className="text-neutral-400 text-sm leading-relaxed mb-6 space-y-2 flex-grow">
                            {productTiles[currentTileIndex].content.map((item, i) => (
                              <li key={i} className="flex items-start">
                                <span className={`${colors.accent} mr-2 mt-1`}>•</span>
                                <span>{item}</span>
                              </li>
                            ))}
                          </ul>
                          <button className={`${colors.accent} hover:${colors.hoverAccent} text-sm font-medium transition-colors self-start`}>
                            {productTiles[currentTileIndex].action} →
                          </button>
                        </div>
                      );
                    })()}

                    {/* Navigation dots */}
                    <div className="flex justify-center space-x-2 mt-4">
                      {productTiles.map((_, index) => (
                        <button
                          key={index}
                          onClick={() => setCurrentTileIndex(index)}
                          className={`w-2 h-2 rounded-full transition-colors ${
                            index === currentTileIndex
                              ? 'bg-blue-400'
                              : 'bg-neutral-600 hover:bg-neutral-500'
                          }`}
                        />
                      ))}
                    </div>
                  </div>
                </div>

                {/* Dismiss button */}
                <div className="flex justify-center mt-6">
                  <button
                    onClick={() => setShowProductTiles(false)}
                    className="text-neutral-500 hover:text-neutral-400 text-xs transition-colors"
                  >
                    Hide this introduction
                  </button>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="shrink-0 px-6 py-3 border-t border-neutral-700">
        <div className="max-w-6xl mx-auto text-sm text-neutral-400">
          <div className="flex justify-center items-center">
            <div className="flex space-x-8">
              <Link href="/pricing" className="hover:text-white transition-colors">
                Pricing
              </Link>
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
    </div>
  );
}