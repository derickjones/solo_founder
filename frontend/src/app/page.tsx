'use client';

import { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import ChatInterface from '@/components/ChatInterface';
import { getCurrentCFMWeek, CFMWeek } from '@/utils/comeFollowMe';
import { MicrophoneIcon, AcademicCapIcon, ClipboardDocumentListIcon, BookOpenIcon, ChatBubbleLeftRightIcon } from '@heroicons/react/24/outline';

// Feature tile type
type FeatureTile = {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  mode: 'Q&A' | 'Come Follow Me';
  studyType?: 'deep-dive' | 'lesson-plans' | 'audio-summary' | 'core-content';
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
  
  // CFM state
  const [cfmAudience, setCfmAudience] = useState('Family');
  const [cfmWeek, setCfmWeek] = useState<CFMWeek>(getCurrentCFMWeek());
  const [cfmStudyType, setCfmStudyType] = useState<'deep-dive' | 'lesson-plans' | 'audio-summary' | 'core-content'>('deep-dive');
  const [cfmStudyLevel, setCfmStudyLevel] = useState<'essential' | 'connected' | 'scholarly'>('essential');
  const [cfmLessonPlanLevel, setCfmLessonPlanLevel] = useState<'adult' | 'youth' | 'children'>('adult');
  const [cfmAudioSummaryLevel, setCfmAudioSummaryLevel] = useState<'short' | 'medium' | 'long'>('medium');

  // Feature tiles configuration
  const featureTiles: FeatureTile[] = [
    {
      id: 'podcast',
      title: 'Podcast',
      description: 'Listen to AI-generated audio summaries of Come Follow Me lessons',
      icon: <MicrophoneIcon className="w-8 h-8" />,
      color: 'from-purple-500 to-purple-700',
      mode: 'Come Follow Me',
      studyType: 'audio-summary'
    },
    {
      id: 'deep-dive',
      title: 'Deep Dive',
      description: 'In-depth scripture study with Essential, Connected, or Scholarly insights',
      icon: <AcademicCapIcon className="w-8 h-8" />,
      color: 'from-blue-500 to-blue-700',
      mode: 'Come Follow Me',
      studyType: 'deep-dive'
    },
    {
      id: 'lesson-plans',
      title: 'Lesson Plans',
      description: 'Generate teaching materials for adults, youth, or children',
      icon: <ClipboardDocumentListIcon className="w-8 h-8" />,
      color: 'from-green-500 to-green-700',
      mode: 'Come Follow Me',
      studyType: 'lesson-plans'
    },
    {
      id: 'core-content',
      title: 'Core Content',
      description: 'Access the raw Come Follow Me curriculum materials',
      icon: <BookOpenIcon className="w-8 h-8" />,
      color: 'from-amber-500 to-amber-700',
      mode: 'Come Follow Me',
      studyType: 'core-content'
    },
    {
      id: 'qa',
      title: 'Q&A',
      description: 'Ask any gospel question and get AI-powered answers with citations',
      icon: <ChatBubbleLeftRightIcon className="w-8 h-8" />,
      color: 'from-rose-500 to-rose-700',
      mode: 'Q&A'
    }
  ];

  // Handle tile click
  const handleTileClick = (tile: FeatureTile) => {
    setMode(tile.mode);
    if (tile.studyType) {
      setCfmStudyType(tile.studyType);
    }
    setShowLandingPage(false);
  };

  // Landing page view
  if (showLandingPage) {
    return (
      <div className="min-h-screen bg-gray-900 text-white">
        {/* Header with logo */}
        <div className="flex flex-col items-center justify-center pt-12 lg:pt-20 pb-8 lg:pb-12 px-4">
          <div className="w-20 h-20 lg:w-28 lg:h-28 rounded-full overflow-hidden border-2 border-neutral-700 mb-6">
            <img 
              src="/christ.jpeg" 
              alt="Gospel Study Assistant Logo" 
              className="w-full h-full object-cover"
            />
          </div>
          <h1 className="text-3xl lg:text-5xl font-bold text-white mb-3 text-center">
            Gospel Study Assistant
          </h1>
          <p className="text-lg lg:text-2xl text-neutral-400 text-center">
            Ask questions. Find answers. Build faith.
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
            <p className="text-neutral-600 text-xs mt-1">{cfmWeek?.dates}</p>
          </div>
        </div>
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
        onBackToLanding={() => setShowLandingPage(true)}
      />
    </div>
  );
}