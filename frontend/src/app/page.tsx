'use client';

import { useState, useEffect } from 'react';
import Sidebar from '@/components/Sidebar';
import ChatInterface from '@/components/ChatInterface';
import { getCurrentCFMWeek, CFMWeek } from '@/utils/comeFollowMe';

// Trigger redeploy with Clerk environment variables
export default function Home() {
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
  const [cfmStudyLevel, setCfmStudyLevel] = useState<'basic' | 'intermediate' | 'advanced'>('basic');

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
        cfmAudience={cfmAudience}
        setCfmAudience={setCfmAudience}
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
        cfmStudyLevel={cfmStudyLevel}
        setCfmStudyLevel={setCfmStudyLevel}
      />
    </div>
  );
}