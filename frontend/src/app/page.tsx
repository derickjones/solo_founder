'use client';

import { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import ChatInterface from '@/components/ChatInterface';
import VideoLogo from '@/components/VideoLogo';
import HamburgerMenu from '@/components/HamburgerMenu';
import UpgradeModal from '@/components/UpgradeModal';
import { useUsageLimit } from '@/hooks/useUsageLimit';
import { getCurrentCFMWeek, CFMWeek, CFM_2026_SCHEDULE } from '@/utils/comeFollowMe';
import { MicrophoneIcon, AcademicCapIcon, ClipboardDocumentListIcon, BookOpenIcon, ChatBubbleLeftRightIcon, SunIcon, ChevronLeftIcon } from '@heroicons/react/24/outline';

// Voice type
type VoiceOption = 'alnilam' | 'achird' | 'enceladus' | 'aoede' | 'autonoe' | 'erinome';

// Feature tile type
type FeatureTile = {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  mode: 'Q&A' | 'Come Follow Me';
  studyType?: 'deep-dive' | 'lesson-plans' | 'audio-summary' | 'core-content';
  special?: 'daily-thought';
};

// Trigger redeploy - Dec 25, 2025 - Landing page redesign
export default function Home() {
  // Landing page state
  const [showLandingPage, setShowLandingPage] = useState(true);

  // Pre-select all available sources
  const allSources = [
    // General Conference
    'general-conference',
    // By Year
    'gc-year-2025', 'gc-year-2024', 'gc-year-2023', 'gc-year-2022', 'gc-year-2021',
    'gc-year-2020', 'gc-year-2019', 'gc-year-2018', 'gc-year-2017', 'gc-year-2016', 'gc-year-2015',
    // By Speaker
    'gc-speaker-russell-m-nelson', 'gc-speaker-dallin-h-oaks', 'gc-speaker-henry-b-eyring',
    'gc-speaker-jeffrey-r-holland', 'gc-speaker-dieter-f-uchtdorf', 'gc-speaker-david-a-bednar',
    'gc-speaker-quentin-l-cook', 'gc-speaker-d-todd-christofferson', 'gc-speaker-neil-l-andersen',
    'gc-speaker-ronald-a-rasband', 'gc-speaker-gary-e-stevenson', 'gc-speaker-dale-g-renlund',
    // Standard Works
    'book-of-mormon', 'doctrine-and-covenants', 'pearl-of-great-price', 'old-testament', 'new-testament'
  ];
  
  const [selectedSources, setSelectedSources] = useState<string[]>(allSources);
  const [sourceCount, setSourceCount] = useState(10);
  const [sidebarOpen, setSidebarOpen] = useState(false); // Start closed, will be set based on screen size
  
  // Set sidebar state based on screen size
  useEffect(() => {
    const handleResize = () => {
      const isDesktop = window.innerWidth >= 1024; // lg breakpoint
      setSidebarOpen(isDesktop);
    };
    
    // Set initial state
    handleResize();
    
    // Listen for resize events
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);
  
  // Shared mode state - controlled by sidebar, used by chat
  const [mode, setMode] = useState('Q&A'); // 'Q&A' or 'Come Follow Me'
  
  // Daily Thought state
  const [showDailyThought, setShowDailyThought] = useState(false);
  const [dailyThoughtData, setDailyThoughtData] = useState<any>(null);
  // getDay() returns 0=Sunday, 1=Monday, etc. JSON uses 1=Sunday, 2=Monday, etc.
  const [selectedDay, setSelectedDay] = useState(() => {
    const jsDay = new Date().getDay(); // 0=Sunday, 1=Monday, etc.
    return jsDay === 0 ? 1 : jsDay + 1; // Convert to 1=Sunday, 2=Monday, etc.
  });
  
  // CFM state - get current week based on today's date
  const currentCfmWeek = getCurrentCFMWeek();
  const currentWeekNumber = parseInt(currentCfmWeek.id.replace('cfm-2026-week-', ''));
  const [selectedWeek, setSelectedWeek] = useState(currentWeekNumber);
  
  const [cfmAudience, setCfmAudience] = useState('Family');
  const [cfmWeek, setCfmWeek] = useState<CFMWeek>(currentCfmWeek);
  const [cfmStudyType, setCfmStudyType] = useState<'deep-dive' | 'lesson-plans' | 'audio-summary' | 'core-content'>('deep-dive');
  const [cfmStudyLevel, setCfmStudyLevel] = useState<'essential' | 'connected' | 'scholarly'>('essential');
  const [cfmLessonPlanLevel, setCfmLessonPlanLevel] = useState<'adult' | 'youth' | 'older-primary' | 'younger-primary'>('adult');
  const [cfmAudioSummaryLevel, setCfmAudioSummaryLevel] = useState<'short' | 'medium' | 'long'>('medium');
  const [selectedVoice, setSelectedVoice] = useState<VoiceOption>('alnilam');

  // Usage limit tracking
  const { 
    actionsUsed, 
    dailyLimit, 
    recordAction, 
    showUpgradeModal, 
    setShowUpgradeModal 
  } = useUsageLimit();

  // Feature tiles configuration
  const featureTiles: FeatureTile[] = [
    {
      id: 'daily-thought',
      title: 'Daily Thought',
      description: 'Start your day with a brief scripture insight and reflection question',
      icon: <SunIcon className="w-8 h-8" />,
      color: 'from-slate-500 to-slate-600',
      mode: 'Come Follow Me',
      special: 'daily-thought'
    },
    {
      id: 'podcast',
      title: 'Podcast',
      description: 'Listen to AI-generated audio summaries of Come Follow Me lessons',
      icon: <MicrophoneIcon className="w-8 h-8" />,
      color: 'from-violet-400 to-violet-500',
      mode: 'Come Follow Me',
      studyType: 'audio-summary'
    },
    {
      id: 'deep-dive',
      title: 'Deep Dive',
      description: 'In-depth scripture study with Essential, Connected, or Scholarly insights',
      icon: <AcademicCapIcon className="w-8 h-8" />,
      color: 'from-sky-400 to-sky-500',
      mode: 'Come Follow Me',
      studyType: 'deep-dive'
    },
    {
      id: 'lesson-plans',
      title: 'Lesson Plans',
      description: 'Generate teaching materials for adults, youth, or children',
      icon: <ClipboardDocumentListIcon className="w-8 h-8" />,
      color: 'from-emerald-400 to-emerald-500',
      mode: 'Come Follow Me',
      studyType: 'lesson-plans'
    },
    {
      id: 'core-content',
      title: 'Core Content',
      description: 'Access the raw Come Follow Me curriculum materials',
      icon: <BookOpenIcon className="w-8 h-8" />,
      color: 'from-orange-400 to-orange-500',
      mode: 'Come Follow Me',
      studyType: 'core-content'
    },
    {
      id: 'qa',
      title: 'Q&A',
      description: 'Ask any gospel question and get AI-powered answers with citations',
      icon: <ChatBubbleLeftRightIcon className="w-8 h-8" />,
      color: 'from-pink-400 to-pink-500',
      mode: 'Q&A'
    }
  ];

  // Load daily thought data
  const loadDailyThought = async (week: number) => {
    try {
      const response = await fetch(`/daily_thoughts/daily_thoughts_week_${week.toString().padStart(2, '0')}.json`);
      const data = await response.json();
      setDailyThoughtData(data);
    } catch (error) {
      console.error('Failed to load daily thought:', error);
    }
  };

  // Handle tile click - check usage limit first
  const handleTileClick = async (tile: FeatureTile) => {
    // Determine activity type based on tile
    const activityType = tile.special === 'daily-thought' 
      ? 'daily_thought' 
      : tile.mode === 'Come Follow Me' 
        ? 'core_content'
        : 'tile_click';
    
    // Check if user can perform action
    const allowed = await recordAction(activityType, { 
      tile: tile.title, 
      mode: tile.mode || 'unknown' 
    });
    if (!allowed) {
      return; // Modal will be shown by the hook
    }

    if (tile.special === 'daily-thought') {
      setShowDailyThought(true);
      setShowLandingPage(false);
      loadDailyThought(selectedWeek);
      return;
    }
    setMode(tile.mode);
    if (tile.studyType) {
      setCfmStudyType(tile.studyType);
    }
    setShowLandingPage(false);
  };

  // Landing page view
  if (showLandingPage) {
    return (
      <div className="min-h-screen bg-neutral-900 text-white relative">
        {/* Top-right hamburger menu */}
        <div className="absolute top-4 right-4 z-50">
          <HamburgerMenu
            mode={mode}
            setMode={setMode}
            selectedVoice={selectedVoice}
            setSelectedVoice={setSelectedVoice}
          />
        </div>

        {/* Header with logo */}
        <div className="flex flex-col items-center justify-center pt-12 lg:pt-20 pb-8 lg:pb-12 px-4">
          <VideoLogo size="large" className="mb-6" />
          <h1 className="text-4xl lg:text-6xl font-bold text-white mb-3 text-center bg-gradient-to-r from-white via-blue-100 to-white bg-clip-text text-transparent drop-shadow-lg" 
              style={{ 
                textShadow: '0 2px 4px rgba(0,0,0,0.5), 0 0 20px rgba(59,130,246,0.3)',
                WebkitTextStroke: '1px rgba(255,255,255,0.1)'
              }}>
            Gospel Study App
          </h1>
          <p className="text-lg lg:text-2xl text-neutral-400 text-center">
            Your daily companion for meaningful gospel study
          </p>
        </div>

        {/* Feature tiles grid */}
        <div className="max-w-5xl mx-auto px-4 pb-12">
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 lg:gap-6">
            {featureTiles.map((tile) => (
              <button
                key={tile.id}
                onClick={() => handleTileClick(tile)}
                className={`group relative overflow-hidden rounded-2xl p-6 lg:p-8 bg-gradient-to-br ${tile.color} 
                  transform transition-all duration-300 hover:scale-105 hover:shadow-2xl hover:shadow-${tile.color.split('-')[1]}-500/25
                  text-left focus:outline-none focus:ring-2 focus:ring-white/50`}
              >
                <div className="absolute inset-0 bg-black/20 group-hover:bg-black/10 transition-colors duration-300" />
                <div className="relative z-10">
                  <div className="mb-4 p-3 bg-white/20 rounded-xl w-fit">
                    {tile.icon}
                  </div>
                  <h3 className="text-xl lg:text-2xl font-bold mb-2">{tile.title}</h3>
                  <p className="text-sm lg:text-base text-white/80 leading-relaxed">
                    {tile.description}
                  </p>
                </div>
                <div className="absolute bottom-4 right-4 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </div>
              </button>
            ))}
          </div>

          {/* Current week indicator */}
          <div className="mt-8 text-center">
            <p className="text-neutral-500 text-sm">
              Current Week: <span className="text-neutral-300">{cfmWeek?.lesson}</span>
            </p>
          </div>
        </div>

        {/* Upgrade Modal */}
        <UpgradeModal
          isOpen={showUpgradeModal}
          onClose={() => setShowUpgradeModal(false)}
          actionsUsed={actionsUsed}
          dailyLimit={dailyLimit}
        />
      </div>
    );
  }

  // Daily Thought view
  if (showDailyThought) {
    const currentThought = dailyThoughtData?.days?.[selectedDay - 1];
    
    return (
      <div className="min-h-screen bg-neutral-900 text-white">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-neutral-800">
          <button
            onClick={() => {
              setShowDailyThought(false);
              setShowLandingPage(true);
            }}
            className="flex items-center gap-2 px-4 py-2 rounded-lg bg-neutral-800/50 hover:bg-neutral-700/50 text-neutral-300 hover:text-white transition-all"
          >
            <ChevronLeftIcon className="w-5 h-5" />
            <span>Back</span>
          </button>
          <h1 className="text-xl font-bold flex items-center gap-2">
            <SunIcon className="w-6 h-6 text-cyan-400" />
            Daily Thought
          </h1>
          <HamburgerMenu
            mode={mode}
            setMode={setMode}
            selectedVoice={selectedVoice}
            setSelectedVoice={setSelectedVoice}
          />
        </div>

        {/* Week and Day Picker */}
        <div className="max-w-2xl mx-auto px-4 py-6">
          <div className="flex flex-col sm:flex-row gap-4 mb-8">
            {/* Week Picker */}
            <div className="flex-1">
              <label className="block text-sm text-neutral-400 mb-2">Week</label>
              <select
                value={selectedWeek}
                onChange={(e) => {
                  const week = parseInt(e.target.value);
                  setSelectedWeek(week);
                  loadDailyThought(week);
                }}
                className="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-4 py-2 text-white focus:outline-none focus:ring-2 focus:ring-cyan-500"
              >
                {CFM_2026_SCHEDULE.map((cfmWeek, index) => (
                  <option key={index + 1} value={index + 1}>
                    Week {index + 1}: {cfmWeek.dates}
                  </option>
                ))}
              </select>
            </div>

            {/* Day Picker */}
            <div className="flex-1">
              <label className="block text-sm text-neutral-400 mb-2">Day</label>
              <div className="flex gap-1">
                {['S', 'M', 'T', 'W', 'T', 'F', 'S'].map((day, index) => (
                  <button
                    key={index}
                    onClick={() => setSelectedDay(index + 1)}
                    className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                      selectedDay === index + 1
                        ? 'bg-cyan-500 text-white'
                        : 'bg-neutral-800 text-neutral-400 hover:bg-neutral-700'
                    }`}
                  >
                    {day}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Daily Thought Content */}
          {currentThought ? (
            <div className="space-y-6 animate-fade-in">
              {/* Theme Badge */}
              <div className="flex items-center gap-2">
                <span className="px-3 py-1 bg-cyan-500/20 text-cyan-400 rounded-full text-sm">
                  {currentThought.theme}
                </span>
                <span className="text-neutral-500 text-sm">
                  {currentThought.day_name}
                </span>
              </div>

              {/* Title */}
              <h2 className="text-2xl lg:text-3xl font-bold text-white">
                {currentThought.title}
              </h2>

              {/* Scripture */}
              <div className="bg-neutral-800/50 border-l-4 border-cyan-500 p-4 rounded-r-lg">
                <p className="text-lg text-white italic mb-2">
                  &ldquo;{currentThought.scripture?.text}&rdquo;
                </p>
                <p className="text-cyan-400 text-sm font-medium">
                  — {currentThought.scripture?.reference}
                </p>
              </div>

              {/* Thought */}
              <div>
                <h3 className="text-sm font-semibold text-neutral-400 uppercase tracking-wider mb-2">
                  Today&apos;s Thought
                </h3>
                <p className="text-neutral-200 leading-relaxed text-lg">
                  {currentThought.thought}
                </p>
              </div>

              {/* Historical Context (if present) */}
              {currentThought.historical_context && (
                <div className="bg-amber-500/10 border border-amber-500/30 rounded-lg p-4">
                  <h3 className="text-sm font-semibold text-amber-400 uppercase tracking-wider mb-2">
                    Historical Context
                  </h3>
                  <p className="text-neutral-300 leading-relaxed">
                    {currentThought.historical_context}
                  </p>
                </div>
              )}

              {/* Application */}
              <div className="bg-green-500/10 border border-green-500/30 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-green-400 uppercase tracking-wider mb-2">
                  Today&apos;s Application
                </h3>
                <p className="text-neutral-200 leading-relaxed">
                  {currentThought.application}
                </p>
              </div>

              {/* Reflection Question */}
              <div className="bg-purple-500/10 border border-purple-500/30 rounded-lg p-4">
                <h3 className="text-sm font-semibold text-purple-400 uppercase tracking-wider mb-2">
                  Reflection Question
                </h3>
                <p className="text-neutral-200 leading-relaxed text-lg">
                  {currentThought.question}
                </p>
              </div>
            </div>
          ) : (
            <div className="flex items-center justify-center h-64">
              <div className="text-neutral-500">Loading...</div>
            </div>
          )}
        </div>

        {/* Upgrade Modal */}
        <UpgradeModal
          isOpen={showUpgradeModal}
          onClose={() => setShowUpgradeModal(false)}
          actionsUsed={actionsUsed}
          dailyLimit={dailyLimit}
        />
      </div>
    );
  }

  // Main app view (existing functionality)
  return (
    <div className="flex h-screen bg-gray-900 text-white relative">
      {/* Mobile backdrop */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-50 z-20 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}
      
      <Sidebar 
        selectedSources={selectedSources}
        setSelectedSources={setSelectedSources}
        sourceCount={sourceCount}
        setSourceCount={setSourceCount}
        isOpen={sidebarOpen}
        setIsOpen={setSidebarOpen}
        mode={mode}
        setMode={setMode}
        cfmWeek={cfmWeek}
        setCfmWeek={setCfmWeek}
        selectedVoice={selectedVoice}
        setSelectedVoice={setSelectedVoice}
      />
      <ChatInterface 
        selectedSources={selectedSources}
        sourceCount={sourceCount}
        sidebarOpen={sidebarOpen}
        setSidebarOpen={setSidebarOpen}
        mode={mode}
        setMode={setMode}
        cfmAudience={cfmAudience}
        setCfmAudience={setCfmAudience}
        cfmWeek={cfmWeek}
        setCfmWeek={setCfmWeek}
        cfmStudyType={cfmStudyType}
        setCfmStudyType={setCfmStudyType}
        cfmStudyLevel={cfmStudyLevel}
        setCfmStudyLevel={setCfmStudyLevel}
        cfmLessonPlanLevel={cfmLessonPlanLevel}
        setCfmLessonPlanLevel={setCfmLessonPlanLevel}
        cfmAudioSummaryLevel={cfmAudioSummaryLevel}
        setCfmAudioSummaryLevel={setCfmAudioSummaryLevel}
        selectedVoice={selectedVoice}
        setSelectedVoice={setSelectedVoice}
        onBackToLanding={() => setShowLandingPage(true)}
        recordAction={recordAction}
      />

      {/* Upgrade Modal */}
      <UpgradeModal
        isOpen={showUpgradeModal}
        onClose={() => setShowUpgradeModal(false)}
        actionsUsed={actionsUsed}
        dailyLimit={dailyLimit}
      />
    </div>
  );
}