'use client';

import { useState, useEffect, useRef } from 'react';
import { getCurrentCFMWeek, CFMWeek, formatCFMWeekDisplay, CFM_2026_SCHEDULE } from '@/utils/comeFollowMe';
import StudyLevelSlider from '@/components/StudyLevelSlider';
import AudioPlayer from '@/components/AudioPlayer';
import { generateTTS } from '@/services/api';
import { ChevronLeftIcon, ArrowDownTrayIcon, ClipboardDocumentIcon, CheckIcon, SpeakerWaveIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import { generateLessonPlanPDF, LessonPlanData } from '@/utils/pdfGenerator';

type StudyLevel = 'essential' | 'connected' | 'scholarly';
type CFMTab = 'study-guide' | 'core-content' | 'lesson-plan' | 'audio-summary';
type LessonAudience = 'adult' | 'youth' | 'children';

export default function ComeFollowMePage() {
  const [currentWeek, setCurrentWeek] = useState<CFMWeek>(getCurrentCFMWeek());
  const [activeTab, setActiveTab] = useState<CFMTab>('study-guide');
  const [studyLevel, setStudyLevel] = useState<StudyLevel>('essential');
  const [lessonAudience, setLessonAudience] = useState<LessonAudience>('adult');
  
  // Study Guide states
  const [studyGuide, setStudyGuide] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  
  // Core Content states
  const [coreContent, setCoreContent] = useState<string | null>(null);
  const [isLoadingCore, setIsLoadingCore] = useState(false);
  
  // Lesson Plan states
  const [lessonPlan, setLessonPlan] = useState<string | null>(null);
  const [isGeneratingLesson, setIsGeneratingLesson] = useState(false);
  
  // Audio Summary states
  const [audioScript, setAudioScript] = useState<any>(null); // Can be string or conversation array
  const [audioVoices, setAudioVoices] = useState<Record<string, string> | null>(null);
  const [audioFiles, setAudioFiles] = useState<{ combined?: string } | null>(null);
  const [isGeneratingAudio, setIsGeneratingAudio] = useState(false);
  const [isGeneratingTTS, setIsGeneratingTTS] = useState(false);
  const [shouldAutoPlay, setShouldAutoPlay] = useState(false);
  
  // Common states
  const [error, setError] = useState<string | null>(null);
  const [generationTime, setGenerationTime] = useState<number | null>(null);
  const [copiedToClipboard, setCopiedToClipboard] = useState(false);

  // Reset study guide when study level or week changes
  useEffect(() => {
    setStudyGuide(null);
    setError(null);
    setGenerationTime(null);
  }, [studyLevel, currentWeek]);

  // Reset audio script when week or study level changes
  useEffect(() => {
    setAudioScript(null);
    setAudioFiles(null);
    setError(null);
  }, [currentWeek, studyLevel]);

  // Get week number from CFM schedule
  const getWeekNumber = (week: CFMWeek): number => {
    const index = CFM_2026_SCHEDULE.findIndex((w: CFMWeek) => w.id === week.id);
    return index >= 0 ? index + 1 : 1;
  };

  const generateStudyGuide = async () => {
    try {
      setIsGenerating(true);
      setError(null);
      setStudyGuide(null);
      setGenerationTime(null);

      // Save current scroll position
      const scrollY = window.scrollY;

      const weekNumber = getWeekNumber(currentWeek);
      const startTime = Date.now();

      // Load from static JSON file (instant loading, no API call)
      const response = await fetch(`/study_guides/study_guide_week_${weekNumber.toString().padStart(2, '0')}_${studyLevel}.json`);
      
      if (!response.ok) {
        throw new Error(`Study guide not available yet for Week ${weekNumber} (${studyLevel})`);
      }
      
      const data = await response.json();
      setStudyGuide(data.content);

      const endTime = Date.now();
      setGenerationTime((endTime - startTime) / 1000);

      // Restore scroll position after content loads
      setTimeout(() => {
        window.scrollTo(0, scrollY);
      }, 0);
    } catch (err) {
      console.error('Error loading study guide:', err);
      setError(err instanceof Error ? err.message : 'Failed to load study guide');
    } finally {
      setIsGenerating(false);
    }
  };

  // Copy to clipboard handler
  const handleCopyToClipboard = async () => {
    if (!studyGuide) return;
    
    try {
      await navigator.clipboard.writeText(studyGuide);
      setCopiedToClipboard(true);
      setTimeout(() => setCopiedToClipboard(false), 2000);
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
    }
  };

  // PDF download handler
  const handleDownloadPDF = async () => {
    if (!studyGuide) return;
    
    try {
      const lessonData: LessonPlanData = {
        title: `${studyLevel.charAt(0).toUpperCase() + studyLevel.slice(1)} Study Guide`,
        date: currentWeek.dates,
        audience: studyLevel,
        content: studyGuide,
        scripture: currentWeek.reference
      };

      await generateLessonPlanPDF(lessonData);
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Error generating PDF. Please try again.');
    }
  };

  // Load podcast script from static JSON (like daily_thoughts pattern)
  const handleGenerateAudioSummary = async () => {
    if (isGeneratingAudio) return;

    setIsGeneratingAudio(true);
    setError(null);
    setAudioFiles(null);
    const startTime = Date.now();

    // Save current scroll position
    const scrollY = window.scrollY;

    try {
      // Extract week number from lesson string (e.g., "Week 32: ..." -> 32)
      const weekMatch = currentWeek.lesson.match(/Week (\d+):/);
      const weekNumber = weekMatch ? parseInt(weekMatch[1]) : 1;

      // Load from static JSON file (instant loading, no API call)
      const response = await fetch(`/podcasts/podcast_week_${weekNumber.toString().padStart(2, '0')}_${studyLevel}.json`);
      
      if (!response.ok) {
        throw new Error(`Podcast script not available yet for Week ${weekNumber} (${studyLevel})`);
      }
      
      const data = await response.json();
      setAudioScript(data.script);
      setAudioVoices(data.voices || null); // Store voices mapping if present
      setGenerationTime(Date.now() - startTime);
      
      console.log('Script loaded successfully');
      setIsGeneratingAudio(false); // Script loaded
      
      // Set a placeholder for audioFiles to show the player immediately
      // The actual audio will be generated when user clicks play
      setAudioFiles({ combined: 'placeholder' });

      // Restore scroll position after audio loads
      setTimeout(() => {
        window.scrollTo(0, scrollY);
      }, 0);
    } catch (error) {
      console.error('Error loading podcast script:', error);
      setError(error instanceof Error ? error.message : 'Failed to load podcast script');
      setIsGeneratingAudio(false);
    }
  };

  // Generate TTS audio (called automatically after script loads or manually)
  // Returns true if audio was cached (fast response)
  const generateTTSFromScript = async (script?: any, voices?: Record<string, string> | null): Promise<boolean> => {
    const scriptToUse = script || audioScript;
    const voicesToUse = voices !== undefined ? voices : audioVoices;
    
    console.log('generateTTSFromScript called', { isGeneratingTTS, hasScript: !!scriptToUse });
    
    if (isGeneratingTTS) {
      console.log('Already generating TTS, skipping...');
      return false;
    }
    
    if (!scriptToUse) {
      console.log('No script available, skipping...');
      return false;
    }

    // Save current scroll position
    const scrollY = window.scrollY;

    console.log('Starting TTS generation...');
    setIsGeneratingTTS(true);
    setError(null);
    const ttsStartTime = Date.now();

    try {
      // Check if we have conversation format (array) or old format (string)
      const isConversation = Array.isArray(scriptToUse);
      const weekNumber = getWeekNumber(currentWeek);
      
      const requestBody: any = {
        title: `${studyLevel.charAt(0).toUpperCase() + studyLevel.slice(1)} Audio Summary`,
        // Add caching metadata
        content_type: 'podcast',
        week_number: weekNumber,
        study_level: studyLevel
      };

      if (isConversation && voicesToUse) {
        // New conversation format
        requestBody.script = scriptToUse;
        requestBody.voices = voicesToUse;
      } else {
        // Old single-speaker format (fallback)
        requestBody.text = typeof scriptToUse === 'string' ? scriptToUse : JSON.stringify(scriptToUse);
        requestBody.voice = 'aoede';
      }

      const response = await generateTTS(requestBody);
      const ttsEndTime = Date.now();
      const ttsGenerationTime = (ttsEndTime - ttsStartTime) / 1000;
      
      console.log(`TTS generation time: ${ttsGenerationTime.toFixed(2)}s`);
      
      // Check if cached (fast response)
      const wasCached = ttsGenerationTime < 3;
      
      if (wasCached) {
        console.log('Cache hit detected - will enable auto-play');
        // Set auto-play BEFORE setting audio files so it's ready when player renders
        setShouldAutoPlay(true);
      } else {
        console.log('Fresh generation - auto-play disabled');
        setShouldAutoPlay(false);
      }
      
      console.log('Setting audio files...', { hasAudio: !!response.audio_base64 });
      setAudioFiles({ combined: response.audio_base64 });
      console.log('Audio files set, player should appear now');
      
      // Restore scroll position after state updates
      setTimeout(() => {
        window.scrollTo(0, scrollY);
      }, 0);
      
      return wasCached;
    } catch (error) {
      console.error('Error generating TTS audio:', error);
      setError(error instanceof Error ? error.message : 'Failed to generate audio');
      return false;
    } finally {
      console.log('TTS generation finished, setting isGeneratingTTS to false');
      setIsGeneratingTTS(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white lg:pl-64">
      {/* Header - Account for sidebar on desktop */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4 flex-1">
              <Link 
                href="/" 
                className="inline-flex items-center text-gray-400 hover:text-white transition-colors flex-shrink-0"
              >
                <ChevronLeftIcon className="h-5 w-5 mr-2" />
                <span className="hidden sm:inline">Back to Study Assistant</span>
                <span className="sm:hidden">Back</span>
              </Link>
              <div className="h-6 w-px bg-gray-600 flex-shrink-0" />
              <h1 className="text-xl font-semibold truncate">Come Follow Me Study Guide</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Current Week & Controls */}
          <div className="lg:col-span-1 space-y-6">
            {/* Current Week Card */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-lg font-semibold mb-4 text-blue-400">Current Week</h2>
              <div className="space-y-3">
                <div className="text-sm text-gray-400">Week {getWeekNumber(currentWeek)}</div>
                <div className="text-lg font-medium">{formatCFMWeekDisplay(currentWeek)}</div>
                <div className="text-sm text-gray-400">{currentWeek.reference}</div>
                <div className="text-xs text-gray-500 bg-gray-900 px-3 py-2 rounded">
                  {currentWeek.dates}
                </div>
              </div>

              {/* Week Selector */}
              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Change Week (Optional)
                </label>
                <select
                  value={currentWeek.id}
                  onChange={(e) => {
                    const selected = CFM_2026_SCHEDULE.find((w: CFMWeek) => w.id === e.target.value);
                    if (selected) setCurrentWeek(selected);
                  }}
                  className="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                >
                  {CFM_2026_SCHEDULE.map((week: CFMWeek, index: number) => (
                    <option key={week.id} value={week.id}>
                      {week.lesson}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Study Level Slider */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-lg font-semibold mb-4 text-blue-400">Study Level</h2>
              <StudyLevelSlider 
                selectedLevel={studyLevel} 
                onLevelChange={setStudyLevel}
              />

              {/* Generate Button */}
              <button
                onClick={generateStudyGuide}
                disabled={isGenerating}
                className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:text-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors"
              >
                {isGenerating ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Generating Study Guide...
                  </div>
                ) : (
                  'Generate Study Guide'
                )}
              </button>

              {error && (
                <div className="mt-4 p-3 bg-red-900 border border-red-700 rounded-lg text-red-200 text-sm">
                  {error}
                </div>
              )}

              {generationTime && (
                <div className="mt-4 text-xs text-gray-500 text-center">
                  Generated in {generationTime.toFixed(1)}s
                </div>
              )}
            </div>

            {/* Audio Summary */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-lg font-semibold mb-4 text-white">🎵 Audio Summary</h2>
              
              {/* Study Level Info */}
              <div className="mb-4 p-3 bg-gray-900 rounded-lg border border-gray-600">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-300">Study Level:</span>
                  <span className="text-sm font-medium text-blue-400">
                    {studyLevel.charAt(0).toUpperCase() + studyLevel.slice(1)}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-1">
                  Uses the same study level as your main study guide
                </p>
              </div>

              {/* Generate Button */}
              <button
                onClick={handleGenerateAudioSummary}
                disabled={isGeneratingAudio || isGeneratingTTS}
                className={`w-full py-3 px-4 rounded-lg font-medium transition-all ${
                  isGeneratingAudio || isGeneratingTTS
                    ? 'bg-gray-700 text-gray-400 cursor-not-allowed'
                    : 'bg-blue-600 hover:bg-blue-700 text-white'
                }`}
              >
                {isGeneratingAudio || isGeneratingTTS ? (
                  <div className="flex items-center justify-center space-x-2">
                    <div className="w-4 h-4 border-2 border-gray-400 border-t-transparent rounded-full animate-spin"></div>
                    <span>{isGeneratingAudio ? 'Loading Script...' : 'Generating Audio...'}</span>
                  </div>
                ) : (
                  'Generate'
                )}
              </button>

              {/* Audio Player - Show when audio is ready */}
              {audioFiles?.combined ? (
                <div className="mt-6">
                  <AudioPlayer 
                    audioFiles={audioFiles}
                    title={`${studyLevel.charAt(0).toUpperCase() + studyLevel.slice(1)} Audio Summary`}
                    autoPlay={shouldAutoPlay}
                    onPlayStart={() => {
                      console.log('Audio started playing, setting shouldAutoPlay to false');
                      setShouldAutoPlay(false);
                    }}
                    onGenerateAudio={async () => {
                      // generateTTSFromScript handles setting shouldAutoPlay based on cache
                      await generateTTSFromScript();
                    }}
                  />
                </div>
              ) : audioScript && isGeneratingTTS ? (
                <div className="mt-6 p-4 bg-gray-900 rounded-lg border border-gray-600 flex items-center justify-center">
                  <div className="flex items-center space-x-3">
                    <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin"></div>
                    <span className="text-gray-300">Generating Audio...</span>
                  </div>
                </div>
              ) : null}

              {/* Audio Script Display */}
              {audioScript && (
                <div className="mt-6 space-y-4">
                  {/* Script Preview */}
                  <div className="p-4 bg-gray-900 rounded-lg border border-gray-600">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="text-sm font-medium text-gray-300">📝 Audio Script</h3>
                      <span className="text-xs text-gray-500">
                        {studyLevel} • {generationTime && `${Math.round(generationTime / 1000)}s`}
                      </span>
                    </div>
                    <div className="text-gray-300 text-sm leading-relaxed max-h-48 overflow-y-auto">
                      {audioScript}
                    </div>
                  </div>
                </div>
              )}

              {error && (
                <div className="mt-4 p-3 bg-red-900/50 border border-red-700 rounded-lg">
                  <p className="text-red-200 text-sm">{error}</p>
                </div>
              )}
            </div>
          </div>

          {/* Right Column - Study Guide */}
          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-lg border border-gray-700">
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-700">
                <h2 className="text-xl font-semibold text-white">
                  {studyGuide ? `${studyLevel.charAt(0).toUpperCase() + studyLevel.slice(1)} Study Guide` : 'Study Guide'}
                </h2>
                
                {studyGuide && (
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={handleCopyToClipboard}
                      className="flex items-center space-x-1 px-3 py-1.5 text-gray-400 hover:text-white bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                    >
                      {copiedToClipboard ? (
                        <>
                          <CheckIcon className="h-4 w-4" />
                          <span className="text-sm">Copied!</span>
                        </>
                      ) : (
                        <>
                          <ClipboardDocumentIcon className="h-4 w-4" />
                          <span className="text-sm">Copy</span>
                        </>
                      )}
                    </button>
                    
                    <button
                      onClick={handleDownloadPDF}
                      className="flex items-center space-x-1 px-3 py-1.5 text-gray-400 hover:text-white bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                    >
                      <ArrowDownTrayIcon className="h-4 w-4" />
                      <span className="text-sm">PDF</span>
                    </button>
                  </div>
                )}
              </div>

              {/* Content */}
              <div className="p-6">
                {!studyGuide && !isGenerating && (
                  <div className="text-center py-16">
                    <div className="text-gray-400 mb-4">
                      <svg className="w-16 h-16 mx-auto mb-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium text-gray-300 mb-2">Ready to Generate Your Study Guide</h3>
                    <p className="text-gray-500 mb-6 max-w-md mx-auto">
                      Select your preferred study level and click "Generate Study Guide" to create a personalized study guide for this week's Come Follow Me lesson.
                    </p>
                  </div>
                )}

                {studyGuide && (
                  <div className="prose prose-invert max-w-none">
                    <ReactMarkdown
                      components={{
                        h1: ({ children }) => <h1 className="text-2xl font-bold text-white mb-6">{children}</h1>,
                        h2: ({ children }) => <h2 className="text-xl font-semibold text-blue-400 mb-4 mt-8">{children}</h2>,
                        h3: ({ children }) => <h3 className="text-lg font-medium text-yellow-400 mb-3 mt-6">{children}</h3>,
                        p: ({ children }) => <p className="text-gray-300 mb-4 leading-relaxed">{children}</p>,
                        ul: ({ children }) => <ul className="text-gray-300 mb-4 space-y-2">{children}</ul>,
                        ol: ({ children }) => <ol className="text-gray-300 mb-4 space-y-2">{children}</ol>,
                        li: ({ children }) => <li className="ml-4">{children}</li>,
                        strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
                        em: ({ children }) => <em className="text-yellow-200">{children}</em>,
                        blockquote: ({ children }) => (
                          <blockquote className="border-l-4 border-blue-500 pl-6 py-2 my-4 bg-gray-900 rounded-r-lg">
                            <div className="text-blue-200 italic">{children}</div>
                          </blockquote>
                        ),
                      }}
                    >
                      {studyGuide}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}