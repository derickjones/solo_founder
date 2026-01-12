'use client';

import { useState, useEffect, useRef } from 'react';
import { ChevronDownIcon, PaperAirplaneIcon, Bars3Icon, ArrowDownTrayIcon, ClipboardDocumentIcon, CheckIcon, ChevronRightIcon, UserCircleIcon } from '@heroicons/react/24/outline';
import { searchScriptures, SearchResult, askQuestionStream, StreamChunk, generateTTS } from '@/services/api';
import ReactMarkdown from 'react-markdown';
import { generateLessonPlanPDF, LessonPlanData } from '@/utils/pdfGenerator';
import { CFM_AUDIENCES, CFM_2026_SCHEDULE, CFMWeek } from '@/utils/comeFollowMe';
import Link from 'next/link';
import AudioPlayer from './AudioPlayer';
import VideoLogo from './VideoLogo';
import HamburgerMenu from './HamburgerMenu';
import type { ActivityType } from '@/hooks/useUsageLimit';

// Add study type definition
type CFMStudyType = 'deep-dive' | 'lesson-plans' | 'audio-summary' | 'core-content';
type StudyLevel = 'essential' | 'connected' | 'scholarly';
type LessonPlanLevel = 'adult' | 'youth' | 'older-primary' | 'younger-primary';
type AudioSummaryLevel = 'short' | 'medium' | 'long';
type VoiceOption = 'alnilam' | 'achird' | 'enceladus' | 'aoede' | 'autonoe' | 'erinome';

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
  audioSubtitle?: string;
  audioScript?: any; // Original script for TTS (can be string or conversation array)
  audioVoices?: Record<string, string>; // Voice mappings for conversation format
  // Caching metadata for TTS
  cacheMetadata?: {
    content_type?: 'podcast' | 'study_guide' | 'lesson_plan' | 'core_content' | 'daily_thoughts';
    week_number?: number;
    study_level?: 'essential' | 'connected' | 'scholarly';
    audience?: 'adult' | 'youth' | 'older-primary' | 'younger-primary';
  };
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
  // Voice selection (from sidebar)
  selectedVoice: VoiceOption;
  setSelectedVoice: (voice: VoiceOption) => void;
  // Back to landing page
  onBackToLanding?: () => void;
  // Usage tracking
  recordAction: (activityType: ActivityType, metadata?: Record<string, string>) => Promise<boolean>;
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
  setCfmAudioSummaryLevel,
  selectedVoice,
  setSelectedVoice,
  onBackToLanding,
  recordAction
}: ChatInterfaceProps) {
  const [query, setQuery] = useState('');
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [streamingContent, setStreamingContent] = useState('');
  const [streamingMessageId, setStreamingMessageId] = useState<number | null>(null);
  const [copiedMessageId, setCopiedMessageId] = useState<number | null>(null);
  const [generatingAudioForMessage, setGeneratingAudioForMessage] = useState<number | null>(null);
  const [autoPlayMessageId, setAutoPlayMessageId] = useState<number | null>(null);
  
  // Ref for scrolling to bottom of messages
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  // Scroll behavior state
  const [isControlsVisible, setIsControlsVisible] = useState(true);
  const [lastScrollY, setLastScrollY] = useState(0);

  // Handle Listen button click - generate TTS for message content
  const handleListenToContent = async (messageId: number, content: string, cacheMetadata?: Message['cacheMetadata']) => {
    setGeneratingAudioForMessage(messageId);
    const startTime = Date.now();
    try {
      // Strip markdown formatting for cleaner TTS
      const cleanText = content
        .replace(/#{1,6}\s/g, '') // Remove headers
        .replace(/\*\*/g, '')     // Remove bold
        .replace(/\*/g, '')       // Remove italic
        .replace(/`/g, '')        // Remove code
        .replace(/\[([^\]]+)\]\([^)]+\)/g, '$1') // Convert links to text
        .replace(/\n{3,}/g, '\n\n') // Normalize line breaks
        .trim();
      
      console.log(`🎧 Generating TTS for ${cleanText.length} characters`);
      
      const result = await generateTTS({
        text: cleanText,
        voice: selectedVoice,
        title: 'Audio',
        // Pass caching metadata if available
        ...cacheMetadata
      });
      
      const generationTime = (Date.now() - startTime) / 1000;
      const wasCached = generationTime < 3;
      
      // If cached, enable auto-play for this message
      if (wasCached) {
        console.log('Audio was cached, enabling auto-play for message', messageId);
        setAutoPlayMessageId(messageId);
      }
      
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
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      alert(`Failed to generate audio: ${errorMessage}`);
    } finally {
      setGeneratingAudioForMessage(null);
    }
  };

  // Listen handler for conversation podcasts (multi-speaker)
  const handleListenToConversation = async (
    messageId: number, 
    script: Array<{ speaker: string; text: string }>, 
    voices: Record<string, string>,
    title: string,
    cacheMetadata?: Message['cacheMetadata']
  ) => {
    setGeneratingAudioForMessage(messageId);
    const startTime = Date.now();
    try {
      const result = await generateTTS({
        script: script,
        voices: voices,
        title: title,
        // Pass caching metadata if available
        ...cacheMetadata
      });
      
      const generationTime = (Date.now() - startTime) / 1000;
      const wasCached = generationTime < 3;
      
      // If cached, enable auto-play for this message
      if (wasCached) {
        console.log('Audio was cached, enabling auto-play for message', messageId);
        setAutoPlayMessageId(messageId);
      }
      
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
      console.error('Failed to generate conversation audio:', error);
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

  // Auto-scroll when content is generated - only for regular chat, not CFM content
  useEffect(() => {
    if (messages.length > 0 && !isLoading && mode !== 'Come Follow Me') {
      // Scroll to show the content - this will trigger the scroll handler to hide controls
      setTimeout(scrollToBottom, 100);
    }
  }, [messages, isLoading, mode]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      // Ctrl+/ or Cmd+/ to toggle sidebar
      if ((e.ctrlKey || e.metaKey) && e.key === '/') {
        e.preventDefault();
        setSidebarOpen(!sidebarOpen);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [sidebarOpen, setSidebarOpen]);

  // Scroll behavior for hiding/showing controls  
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const handleScroll = () => {
      const currentScrollY = window.scrollY;
      
      // Only respond to vertical scrolling on mobile to avoid horizontal scroll issues
      const isVerticalScroll = Math.abs(currentScrollY - lastScrollY) > 5;
      
      // On all devices: scroll up reveals controls, scroll down hides them (when there's content)
      if (messages.length > 0 && isVerticalScroll) {
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

  // PDF download handler
  const handleDownloadPDF = async (messageContent: string) => {
    try {
      // Determine title and audience based on study type
      let title = '';
      let audience = '';
      
      if (cfmStudyType === 'deep-dive') {
        const levelLabel = cfmStudyLevel === 'essential' ? 'Essential' : 
                          cfmStudyLevel === 'connected' ? 'Connected' : 'Scholarly';
        title = `${levelLabel} Study Guide`;
        audience = levelLabel;
      } else if (cfmStudyType === 'lesson-plans') {
        const audienceLabel = cfmLessonPlanLevel === 'adult' ? 'Adult' :
                             cfmLessonPlanLevel === 'youth' ? 'Youth (11-17)' :
                             cfmLessonPlanLevel === 'older-primary' ? 'Older Children (8-10)' :
                             'Younger Children (3-7)';
        title = `${audienceLabel} Lesson Plan`;
        audience = audienceLabel;
      } else if (cfmStudyType === 'audio-summary') {
        const levelLabel = cfmAudioSummaryLevel === 'short' ? 'Essential' :
                          cfmAudioSummaryLevel === 'medium' ? 'Connected' : 'Scholarly';
        title = `${levelLabel} Audio Summary`;
        audience = levelLabel;
      } else if (cfmStudyType === 'core-content') {
        title = 'Core Content';
        audience = 'All';
      } else {
        title = 'Study Guide';
        audience = 'General';
      }
      
      const lessonData: LessonPlanData = {
        title,
        date: cfmWeek?.dates || '',
        audience,
        content: messageContent,
        scripture: cfmWeek?.reference || ''
      };

      await generateLessonPlanPDF(lessonData);
    } catch (error) {
      console.error('Error downloading PDF:', error);
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

    // Determine activity type based on mode
    const activityType = mode === 'Come Follow Me' ? 'lesson_plan' : 'qa_question';
    const metadata: Record<string, string> = mode === 'Come Follow Me' 
      ? { week: cfmWeek?.lesson || 'unknown', studyType: cfmStudyType || 'unknown' }
      : { question: query.substring(0, 100) }; // Truncate long questions

    // Check usage limit before processing
    const allowed = await recordAction(activityType, metadata);
    if (!allowed) {
      return; // Modal will be shown by parent component
    }

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
          // Handle CFM deep dive generation - load from static JSON file
          
          // Get week number from CFM schedule
          const weekIndex = CFM_2026_SCHEDULE.findIndex((w: CFMWeek) => w.id === cfmWeek?.id);
          const weekNumber = weekIndex >= 0 ? weekIndex + 1 : 1;
          
          try {
            console.log('Loading CFM Study Guide from static file...');
            
            // Load from static JSON file (instant loading, no API call)
            const response = await fetch(`/study_guides/study_guide_week_${weekNumber.toString().padStart(2, '0')}_${cfmStudyLevel}.json`);
            
            if (!response.ok) {
              throw new Error(`Study guide not available yet for Week ${weekNumber} (${cfmStudyLevel})`);
            }
            
            const data = await response.json();
            
            // Update the message with the study guide content and enable audio
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { 
                    ...msg, 
                    content: data.content, 
                    audioFiles: { combined: 'placeholder' }, // Show player, generate on play
                    audioTitle: `Week ${weekNumber} Study Guide (${cfmStudyLevel})`,
                    isStreaming: false,
                    cacheMetadata: {
                      content_type: 'study_guide',
                      week_number: weekNumber,
                      study_level: cfmStudyLevel as 'essential' | 'connected' | 'scholarly'
                    }
                  }
                : msg
            ));
            
            console.log('CFM Study Guide loaded successfully');
          } catch (error) {
            console.error('CFM Study Guide loading error:', error);
            
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
            // Load from static JSON file (instant loading, no API call)
            const response = await fetch(`/lesson_plans/lesson_plan_week_${weekNumber.toString().padStart(2, '0')}_${cfmLessonPlanLevel}.json`);
            
            if (!response.ok) {
              throw new Error(`Lesson plan not available yet for Week ${weekNumber} (${cfmLessonPlanLevel})`);
            }
            
            const data = await response.json();
            
            // Update the message with the lesson plan and enable audio
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { 
                    ...msg, 
                    content: data.content, 
                    audioFiles: { combined: 'placeholder' }, // Show player, generate on play
                    audioTitle: `Week ${weekNumber} Lesson Plan (${cfmLessonPlanLevel})`,
                    isStreaming: false,
                    cacheMetadata: {
                      content_type: 'lesson_plan',
                      week_number: weekNumber,
                      audience: cfmLessonPlanLevel
                    }
                  }
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
            
            // Load from static JSON file (instant loading, no API call)
            const studyLevel = studyLevelMap[cfmAudioSummaryLevel];
            const response = await fetch(`/podcasts/podcast_week_${weekNumber.toString().padStart(2, '0')}_${studyLevel}.json`);
            
            if (!response.ok) {
              throw new Error(`Podcast script not available yet for Week ${weekNumber} (${studyLevel})`);
            }
            
            const data = await response.json();
            
            // Format conversation script for display
            let displayContent: string;
            if (Array.isArray(data.script)) {
              // Conversation format - format as readable dialogue
              displayContent = data.script.map((segment: any) => 
                `**${segment.speaker}:** ${segment.text}`
              ).join('\n\n');
            } else {
              // Old single-speaker format
              displayContent = data.script;
            }
            
            // Update the message with the audio summary transcript
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { 
                    ...msg, 
                    content: displayContent, // Show formatted dialogue
                    audioFiles: { combined: 'placeholder' }, // Show player immediately, generate on play
                    audioTitle: `Week ${weekNumber} Podcast`,
                    audioSubtitle: `${cfmWeek?.dates} • ${cfmWeek?.reference}`,
                    audioScript: data.script, // Store original script for TTS generation
                    audioVoices: data.voices, // Store voice mappings
                    isStreaming: false,
                    cacheMetadata: {
                      content_type: 'podcast',
                      week_number: weekNumber,
                      study_level: studyLevel
                    }
                  }
                : msg
            ));
            
            // Auto-hide controls to give full screen to content
            setIsControlsVisible(false);
          } else if (cfmStudyType === 'core-content') {
            // Load from static JSON file (instant loading, no API call)
            const response = await fetch(`/core_content/core_content_week_${weekNumber.toString().padStart(2, '0')}.json`);
            
            if (!response.ok) {
              throw new Error(`Core content not available yet for Week ${weekNumber}`);
            }
            
            const data = await response.json();
            
            // Format content in a user-friendly way
            let formattedContent = `# ${data.title}\n\n`;
            formattedContent += `**${data.date_range}**\n\n`;
            
            // Add introduction if available
            if (data.introduction) {
              formattedContent += `## Introduction\n\n${data.introduction}\n\n`;
            }
            
            // Add learning at home and church sections
            if (data.learning_at_home_church && data.learning_at_home_church.length > 0) {
              formattedContent += `## Learning at Home and Church\n\n`;
              data.learning_at_home_church.forEach((section: any) => {
                formattedContent += `### ${section.title}\n\n${section.content}\n\n`;
              });
            }
            
            // Add teaching children sections
            if (data.teaching_children && data.teaching_children.length > 0) {
              formattedContent += `## Teaching Children\n\n`;
              data.teaching_children.forEach((section: any) => {
                formattedContent += `### ${section.title}\n\n${section.content}\n\n`;
              });
            }
            
            // Add scriptures if available
            if (data.scriptures && data.scriptures.length > 0) {
              formattedContent += `## Scripture References\n\n`;
              data.scriptures.forEach((scripture: any) => {
                formattedContent += `### ${scripture.reference || scripture.title}\n\n`;
                if (scripture.summary) {
                  // Clean encoding issues in summary - handle UTF-8 display issues
                  const cleanSummary = scripture.summary
                    .replace(/—/g, '—')      // Fix em dashes
                    .replace(/–/g, '–')      // Fix en dashes  
                    .replace(/"/g, '"')      // Fix left quotes
                    .replace(/"/g, '"')      // Fix right quotes
                    .replace(/'/g, "'")      // Fix left apostrophes
                    .replace(/'/g, "'")      // Fix right apostrophes
                    .replace(/â€™/g, "'")    // Fix UTF-8 encoding issues
                    .replace(/â€œ/g, '"')    // Fix UTF-8 encoding issues
                    .replace(/â€/g, '"')     // Fix UTF-8 encoding issues
                    .replace(/â€"/g, '—');   // Fix UTF-8 encoding issues
                  formattedContent += `*${cleanSummary}*\n\n`;
                }
                if (scripture.text) {
                  // Clean encoding issues and format scripture text with proper verse breaks
                  let cleanText = scripture.text
                    .replace(/—/g, '—')      // Fix em dashes
                    .replace(/–/g, '–')      // Fix en dashes  
                    .replace(/"/g, '"')      // Fix left quotes
                    .replace(/"/g, '"')      // Fix right quotes
                    .replace(/'/g, "'")      // Fix left apostrophes
                    .replace(/'/g, "'")      // Fix right apostrophes
                    .replace(/â€™/g, "'")    // Fix UTF-8 encoding issues
                    .replace(/â€œ/g, '"')    // Fix UTF-8 encoding issues
                    .replace(/â€/g, '"')     // Fix UTF-8 encoding issues
                    .replace(/â€"/g, '—')    // Fix UTF-8 encoding issues
                    // Normalize whitespace
                    .replace(/\s+/g, ' ')    // Multiple spaces to single space
                    .trim();                 // Remove leading/trailing spaces
                    
                  const formattedScripture = cleanText
                    // Add line breaks before verse numbers (pattern: number followed by text)
                    .replace(/(\d+)\s*([A-Z])/g, '\n\n**$1** $2')
                    // Clean up any double line breaks at the start
                    .replace(/^\n+/, '')
                    // Ensure we start with the verse number formatted
                    .replace(/^(\d+)\s*/, '**$1** ');
                  
                  formattedContent += `${formattedScripture}\n\n`;
                }
                if (scripture.url) {
                  formattedContent += `[Read on ChurchofJesusChrist.org](${scripture.url})\n\n`;
                }
              });
            }
            
            // Add seminary content if available
            if (data.seminary_content && data.seminary_content.length > 0) {
              formattedContent += `## Seminary Content\n\n`;
              data.seminary_content.forEach((item: any) => {
                formattedContent += `### ${item.title}\n\n${item.content}\n\n`;
              });
            }
            
            // Add study helps if available
            if (data.study_helps && data.study_helps.length > 0) {
              formattedContent += `## Study Helps\n\n`;
              data.study_helps.forEach((help: any) => {
                formattedContent += `### ${help.title}\n\n${help.content}\n\n`;
              });
            }
            
            // Add additional resources if available
            if (data.additional_resources && data.additional_resources.length > 0) {
              formattedContent += `## Additional Resources\n\n`;
              data.additional_resources.forEach((resource: any) => {
                formattedContent += `- [${resource.title}](${resource.url})\n`;
              });
              formattedContent += '\n';
            }
            
            // Add source information at the bottom
            if (data.cfm_lesson_url) {
              formattedContent += `---\n\n**Original Source:** [Come, Follow Me Manual](${data.cfm_lesson_url})\n\n`;
            }
            
            // Update the message with the organized core content and enable audio
            setMessages(prev => prev.map(msg => 
              msg.id === assistantMessageId 
                ? { 
                    ...msg, 
                    content: formattedContent, 
                    audioFiles: { combined: 'placeholder' }, // Show player, generate on play
                    audioTitle: `Week ${weekNumber} Core Content`,
                    isStreaming: false,
                    cacheMetadata: {
                      content_type: 'core_content',
                      week_number: weekNumber
                    }
                  }
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
    <div className={`flex-1 flex flex-col bg-neutral-900 transition-all duration-300 ${sidebarOpen ? 'lg:ml-0' : 'lg:ml-0'}`}>
      {/* Top-left back button - responsive positioning */}
      {onBackToLanding && (
        <div className={`fixed top-4 z-30 transition-all duration-300 ${sidebarOpen ? 'left-4 lg:left-[22rem]' : 'left-4 lg:left-6'}`}>
          <button
            type="button"
            onClick={() => {
              resetChat();
              onBackToLanding();
            }}
            className="flex items-center gap-2 px-3 py-2 rounded-lg bg-neutral-800/95 hover:bg-neutral-700/95 border border-neutral-600/60 text-neutral-200 hover:text-white transition-all duration-200 backdrop-blur-md shadow-xl"
            title="Back"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2.5} stroke="currentColor" className="w-5 h-5">
              <path strokeLinecap="round" strokeLinejoin="round" d="M15.75 19.5 8.25 12l7.5-7.5" />
            </svg>
            <span className="text-sm lg:text-base font-semibold">Back</span>
          </button>
        </div>
      )}

      {/* Top-right hamburger menu - fixed position */}
      <div className="fixed top-4 right-4 z-30">
        <HamburgerMenu
          mode={mode}
          setMode={setMode}
          selectedVoice={selectedVoice}
          setSelectedVoice={setSelectedVoice}
          onOpenSidebar={() => setSidebarOpen(true)}
        />
      </div>

      {/* Header with logo - always visible, compact when content is shown */}
      <div className={`relative flex items-center justify-center px-4 transition-all duration-300 ease-in-out shrink-0 ${
        messages.length > 0 ? 'pt-2 pb-1 lg:pt-3 lg:pb-2' : 'pt-6 lg:pt-12 pb-4 lg:pb-6'
      }`}>
        <div className={`flex flex-col items-center transition-all duration-300 ${
          messages.length > 0 ? 'space-y-1' : 'space-y-4 lg:space-y-6'
        }`}>
          <VideoLogo size={messages.length > 0 ? 'small' : 'medium'} />
          <div className="text-center">
            <button 
              onClick={() => {
                resetChat();
                if (onBackToLanding) onBackToLanding();
              }}
              className={`font-bold text-white hover:text-blue-300 transition-colors cursor-pointer ${
                messages.length > 0 ? 'text-sm lg:text-base' : 'text-3xl lg:text-5xl mb-2'
              }`}
              style={messages.length === 0 ? { 
                textShadow: '0 2px 4px rgba(0,0,0,0.5), 0 0 15px rgba(59,130,246,0.2)',
                WebkitTextStroke: '0.5px rgba(255,255,255,0.1)'
              } : {}}
            >
              Gospel Study App
            </button>
            {messages.length === 0 && (
              <p className="text-sm lg:text-xl text-neutral-400 px-4">Your daily companion for meaningful gospel study</p>
            )}
          </div>
        </div>
      </div>

      {/* Input area below header - collapses when content is shown or loading */}
      <div className={`px-4 lg:px-8 pb-2 transition-all duration-300 ease-in-out overflow-hidden shrink-0 ${
        (isLoading || (!isControlsVisible && messages.length > 0)) ? 'max-h-0 opacity-0' : 'opacity-100'
      }`}>
        <div className="max-w-2xl mx-auto">
          <form onSubmit={handleSubmit} className="relative">
            {mode === 'Come Follow Me' ? (
              // CFM Mode: Clean layout matching Daily Thought page
              <div className="w-full space-y-6 max-h-[70vh] md:max-h-none overflow-y-auto md:overflow-visible py-4">
                {/* Week Selector */}
                <div className="space-y-3">
                  <label className="text-neutral-400 text-sm">Select Week</label>
                  <select
                    value={cfmWeek?.id || ''}
                    onChange={(e) => {
                      const selectedWeek = CFM_2026_SCHEDULE.find((w: CFMWeek) => w.id === e.target.value);
                      setCfmWeek(selectedWeek || CFM_2026_SCHEDULE[0]);
                    }}
                    className="w-full p-3 bg-neutral-800 border border-neutral-700 rounded-lg text-white text-sm font-medium focus:outline-none focus:ring-2 focus:ring-blue-500 appearance-none cursor-pointer transition-all"
                  >
                    {CFM_2026_SCHEDULE.map((week: CFMWeek, index: number) => (
                      <option key={week.id} value={week.id} className="bg-neutral-800">
                        {week.lesson}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Study Type Badge */}
                {onBackToLanding && (
                  <div className="flex justify-center">
                    <div className={`inline-flex items-center gap-2 px-5 py-2.5 rounded-full text-white font-medium ${
                      cfmStudyType === 'deep-dive' ? 'bg-blue-600' :
                      cfmStudyType === 'lesson-plans' ? 'bg-green-600' :
                      cfmStudyType === 'audio-summary' ? 'bg-purple-600' :
                      'bg-amber-600'
                    }`}>
                      {cfmStudyType === 'audio-summary' && (
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M12 18.75a6 6 0 0 0 6-6v-1.5m-6 7.5a6 6 0 0 1-6-6v-1.5m6 7.5v3.75m-3.75 0h7.5M12 15.75a3 3 0 0 1-3-3V4.5a3 3 0 1 1 6 0v8.25a3 3 0 0 1-3 3Z" />
                        </svg>
                      )}
                      {cfmStudyType === 'deep-dive' && (
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M4.26 10.147a60.438 60.438 0 0 0-.491 6.347A48.62 48.62 0 0 1 12 20.904a48.62 48.62 0 0 1 8.232-4.41 60.46 60.46 0 0 0-.491-6.347m-15.482 0a50.636 50.636 0 0 0-2.658-.813A59.906 59.906 0 0 1 12 3.493a59.903 59.903 0 0 1 10.399 5.84c-.896.248-1.783.52-2.658.814m-15.482 0A50.717 50.717 0 0 1 12 13.489a50.702 50.702 0 0 1 7.74-3.342M6.75 15a.75.75 0 1 0 0-1.5.75.75 0 0 0 0 1.5Zm0 0v-3.675A55.378 55.378 0 0 1 12 8.443m-7.007 11.55A5.981 5.981 0 0 0 6.75 15.75v-1.5" />
                        </svg>
                      )}
                      {cfmStudyType === 'lesson-plans' && (
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h3.75M9 15h3.75M9 18h3.75m3 .75H18a2.25 2.25 0 0 0 2.25-2.25V6.108c0-1.135-.845-2.098-1.976-2.192a48.424 48.424 0 0 0-1.123-.08m-5.801 0c-.065.21-.1.433-.1.664 0 .414.336.75.75.75h4.5a.75.75 0 0 0 .75-.75 2.25 2.25 0 0 0-.1-.664m-5.8 0A2.251 2.251 0 0 1 13.5 2.25H15c1.012 0 1.867.668 2.15 1.586m-5.8 0c-.376.023-.75.05-1.124.08C9.095 4.01 8.25 4.973 8.25 6.108V8.25m0 0H4.875c-.621 0-1.125.504-1.125 1.125v11.25c0 .621.504 1.125 1.125 1.125h9.75c.621 0 1.125-.504 1.125-1.125V9.375c0-.621-.504-1.125-1.125-1.125H8.25ZM6.75 12h.008v.008H6.75V12Zm0 3h.008v.008H6.75V15Zm0 3h.008v.008H6.75V18Z" />
                        </svg>
                      )}
                      {cfmStudyType === 'core-content' && (
                        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5">
                          <path strokeLinecap="round" strokeLinejoin="round" d="M12 6.042A8.967 8.967 0 0 0 6 3.75c-1.052 0-2.062.18-3 .512v14.25A8.987 8.987 0 0 1 6 18c2.305 0 4.408.867 6 2.292m0-14.25a8.966 8.966 0 0 1 6-2.292c1.052 0 2.062.18 3 .512v14.25A8.987 8.987 0 0 0 18 18a8.967 8.967 0 0 0-6 2.292m0-14.25v14.25" />
                        </svg>
                      )}
                      <span>
                        {cfmStudyType === 'deep-dive' && 'Deep Dive'}
                        {cfmStudyType === 'lesson-plans' && 'Lesson Plans'}
                        {cfmStudyType === 'audio-summary' && 'Podcast'}
                        {cfmStudyType === 'core-content' && 'Core Content'}
                      </span>
                    </div>
                  </div>
                )}

                  {/* Dynamic Level Selection Based on Study Type - Centered */}
                  <div className="max-w-2xl mx-auto">
                    <div className="space-y-4">
                      {cfmStudyType === 'deep-dive' && (
                        <>
                          <label className="text-sm font-medium text-neutral-400 uppercase tracking-wider text-center block">Study Level</label>
                          <div className="flex justify-center gap-3">
                            {[
                              { level: 'essential', label: 'Essential', color: 'emerald', desc: '~5 min read' },
                              { level: 'connected', label: 'Connected', color: 'purple', desc: '~10 min read' },
                              { level: 'scholarly', label: 'Scholarly', color: 'amber', desc: '~15 min read' }
                            ].map(({ level, label, color, desc }) => (
                              <button
                                key={level}
                                type="button"
                                onClick={() => setCfmStudyLevel(level as StudyLevel)}
                                className={`group py-3 px-5 rounded-xl text-sm font-semibold transition-all duration-200 flex flex-col items-center ${
                                  cfmStudyLevel === level
                                    ? color === 'emerald' 
                                      ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/25 scale-105'
                                      : color === 'purple'
                                      ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/25 scale-105'
                                      : 'bg-amber-600 text-white shadow-lg shadow-amber-500/25 scale-105'
                                    : 'text-neutral-400 hover:text-white hover:bg-neutral-700/50 hover:scale-102'
                                }`}
                              >
                                <span>{label}</span>
                                <span className={`text-xs mt-1 ${cfmStudyLevel === level ? 'text-white/70' : 'text-neutral-500'}`}>{desc}</span>
                              </button>
                            ))}
                          </div>
                        </>
                      )}
                      
                      {cfmStudyType === 'lesson-plans' && (
                        <>
                          <label className="text-sm font-medium text-neutral-400 uppercase tracking-wider text-center block">Audience</label>
                          <div className="grid grid-cols-2 gap-2 md:flex md:justify-center md:gap-3">
                            {[
                              { level: 'adult', label: 'Adult', color: 'purple', desc: '18+' },
                              { level: 'youth', label: 'Youth', color: 'blue', desc: '11-17' },
                              { level: 'older-primary', label: 'Older Children', color: 'emerald', desc: '8-10' },
                              { level: 'younger-primary', label: 'Younger Children', color: 'amber', desc: '3-7' }
                            ].map(({ level, label, color, desc }) => (
                              <button
                                key={level}
                                type="button"
                                onClick={() => setCfmLessonPlanLevel(level as LessonPlanLevel)}
                                className={`group py-3 px-4 rounded-xl text-sm font-semibold transition-all duration-200 flex flex-col items-center ${
                                  cfmLessonPlanLevel === level
                                    ? color === 'purple'
                                      ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/25 scale-105'
                                      : color === 'blue'
                                      ? 'bg-blue-600 text-white shadow-lg shadow-blue-500/25 scale-105'
                                      : color === 'emerald'
                                      ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/25 scale-105'
                                      : 'bg-amber-600 text-white shadow-lg shadow-amber-500/25 scale-105'
                                    : 'text-neutral-400 hover:text-white hover:bg-neutral-700/50 hover:scale-102'
                                }`}
                              >
                                <span>{label}</span>
                                <span className={`text-xs mt-1 ${cfmLessonPlanLevel === level ? 'text-white/70' : 'text-neutral-500'}`}>Ages {desc}</span>
                              </button>
                            ))}
                          </div>
                        </>
                      )}
                      
                      {cfmStudyType === 'audio-summary' && (
                        <>
                          <label className="text-sm font-medium text-neutral-400 uppercase tracking-wider text-center block">Study Level</label>
                          <div className="flex justify-center gap-3">
                            {[
                              { level: 'short', label: 'Essential', color: 'emerald', desc: '~5 min listen' },
                              { level: 'medium', label: 'Connected', color: 'purple', desc: '~10 min listen' },
                              { level: 'long', label: 'Scholarly', color: 'amber', desc: '~15 min listen' }
                            ].map(({ level, label, color, desc }) => (
                              <button
                                key={level}
                                type="button"
                                onClick={() => setCfmAudioSummaryLevel(level as AudioSummaryLevel)}
                                className={`group py-3 px-5 rounded-xl text-sm font-semibold transition-all duration-200 flex flex-col items-center ${
                                  cfmAudioSummaryLevel === level
                                    ? color === 'emerald' 
                                      ? 'bg-emerald-600 text-white shadow-lg shadow-emerald-500/25 scale-105'
                                      : color === 'purple'
                                      ? 'bg-purple-600 text-white shadow-lg shadow-purple-500/25 scale-105'
                                      : 'bg-amber-600 text-white shadow-lg shadow-amber-500/25 scale-105'
                                    : 'text-neutral-400 hover:text-white hover:bg-neutral-700/50 hover:scale-102'
                                }`}
                              >
                                <span>{label}</span>
                                <span className={`text-xs mt-1 ${cfmAudioSummaryLevel === level ? 'text-white/70' : 'text-neutral-500'}`}>{desc}</span>
                              </button>
                            ))}
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
                    className="w-full bg-blue-600 hover:bg-blue-500 disabled:bg-neutral-700 disabled:cursor-not-allowed px-4 py-3 rounded-lg transition-all duration-150 font-medium text-white disabled:text-neutral-500"
                  >
                    {isLoading ? (
                      <div className="flex items-center justify-center space-x-2">
                        <div className="animate-spin rounded-full h-4 w-4 border-2 border-white border-t-transparent" />
                        <span className="text-sm">
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
                      <span className="text-sm">
                        {cfmStudyType === 'deep-dive' && `Generate`}
                        {cfmStudyType === 'lesson-plans' && `Generate`}
                        {cfmStudyType === 'audio-summary' && `Generate`}
                        {cfmStudyType === 'core-content' && `Generate`}
                      </span>
                    )}
                  </button>
                </div>
              ) : (
                // Q&A Mode: Show text input
                <div className="flex items-center gap-3 w-full bg-neutral-800 border-2 border-neutral-700 focus-within:border-blue-500 focus-within:ring-2 focus-within:ring-blue-500/20 rounded-2xl p-4 lg:p-6">
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
          </form>
        </div>
      </div>

      {/* Mobile expand controls button - shows when controls are hidden */}
      {!isControlsVisible && messages.length > 0 && (
        <div className="md:hidden px-4 py-2 shrink-0">
          <button
            type="button"
            onClick={() => setIsControlsVisible(true)}
            className="w-full bg-neutral-700/50 hover:bg-neutral-600/50 text-neutral-300 py-2 px-4 rounded-lg transition-all duration-200 text-sm flex items-center justify-center space-x-2"
          >
            <ChevronDownIcon className="w-4 h-4 rotate-180" />
            <span>Show Controls</span>
          </button>
        </div>
      )}

      {/* Messages area */}
      <div className="flex-1 min-h-0 px-2 sm:px-4 lg:px-6 pb-2 lg:pb-4 overflow-y-auto overflow-x-hidden">
        {messages.length > 0 && (
          <div className="max-w-6xl mx-auto space-y-6 w-full">
            {messages.map((message) => (
              <div key={message.id} className="space-y-4 w-full">
                {/* Show user messages, assistant messages with content, or assistant messages that are loading */}
                {(message.type === 'user' || (message.type === 'assistant' && (message.content || message.audioFiles || message.isStreaming))) && (
                  <div
                    className={`w-full ${
                      message.type === 'user'
                        ? 'bg-neutral-600 text-white ml-auto max-w-[85%] sm:max-w-sm lg:max-w-lg p-3 lg:p-4 rounded-lg break-words'
                        : 'bg-neutral-800 text-white p-4 sm:p-6 rounded-lg break-words overflow-hidden'
                    }`}
                  >
                    {/* CFM Study Guide Header - Skip for audio-summary since AudioPlayer has its own header */}
                    {message.type === 'assistant' && mode === 'Come Follow Me' && message.content && cfmStudyType !== 'audio-summary' && (
                      <div className="mb-6 pb-4 border-b border-neutral-600">
                        <div className="flex items-center justify-between mb-3">
                          <div>
                            <h2 className="text-xl font-bold text-neutral-200 mb-2">
                              {cfmStudyType === 'deep-dive' && `${cfmStudyLevel.charAt(0).toUpperCase() + cfmStudyLevel.slice(1)} Deep Dive`}
                              {cfmStudyType === 'lesson-plans' && `${cfmLessonPlanLevel.charAt(0).toUpperCase() + cfmLessonPlanLevel.slice(1)} Lesson Plan`}
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
                        <div className="space-y-6 leading-relaxed text-neutral-100 w-full min-w-0 overflow-hidden break-words hyphens-auto">
                          {/* Audio Player - shown at top for CFM content */}
                          {mode === 'Come Follow Me' && message.audioFiles?.combined && (
                            <div className="mb-6 pb-6 border-b border-neutral-700">
                              <AudioPlayer 
                                audioFiles={message.audioFiles}
                                title={message.audioTitle || 'Audio'}
                                subtitle={message.audioSubtitle}
                                autoPlay={autoPlayMessageId === message.id}
                                onPlayStart={() => {
                                  console.log('Audio started playing, clearing autoPlayMessageId');
                                  setAutoPlayMessageId(null);
                                }}
                                onGenerateAudio={async () => {
                                  // Generate audio when play is clicked
                                  if (message.audioScript && message.audioVoices) {
                                    await handleListenToConversation(message.id, message.audioScript, message.audioVoices, message.audioTitle || 'Audio', message.cacheMetadata);
                                  } else {
                                    await handleListenToContent(message.id, message.content, message.cacheMetadata);
                                  }
                                }}
                              />
                            </div>
                          )}
                          
                          {message.isStreaming && message.id === streamingMessageId ? (
                            // During streaming, show the streaming content state
                            <div className="text-base leading-7 text-neutral-100 whitespace-pre-wrap break-words overflow-x-hidden">
                              {streamingContent}
                              <span className="inline-block w-2 h-4 bg-green-400 animate-pulse ml-1">|</span>
                            </div>
                          ) : (
                            // After streaming is complete, use full markdown rendering
                            <ReactMarkdown 
                              components={{
                                h1: ({ children }) => (
                                  <h1 className={`text-xl font-semibold mb-4 mt-6 break-words ${mode === 'Come Follow Me' ? 'text-blue-200' : 'text-white'}`}>
                                    {children}
                                  </h1>
                                ),
                                h2: ({ children }) => (
                                  <h2 className={`text-lg font-semibold mb-3 mt-5 break-words ${mode === 'Come Follow Me' ? 'text-blue-300' : 'text-white'}`}>
                                    {children}
                                  </h2>
                                ),
                                h3: ({ children }) => (
                                  <h3 className={`text-base font-semibold mb-3 mt-4 break-words ${mode === 'Come Follow Me' ? 'text-yellow-300' : 'text-white'}`}>
                                    {children}
                                  </h3>
                                ),
                                h4: ({ children }) => (
                                  <h4 className={`text-base font-medium mb-2 mt-4 break-words ${mode === 'Come Follow Me' ? 'text-yellow-200' : 'text-white'}`}>
                                    {children}
                                  </h4>
                                ),
                                p: ({ children }) => (
                                  <p className="text-neutral-300 leading-relaxed mb-4 break-words">
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
                                  <li className="text-neutral-300 leading-relaxed break-words">
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
                      ) : message.isStreaming && mode === 'Come Follow Me' ? (
                        // Show loading indicator when streaming but no content yet (CFM mode only)
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