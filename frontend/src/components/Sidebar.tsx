'use client';

import { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon, XMarkIcon, ChevronLeftIcon } from '@heroicons/react/24/outline';
import { useUser, SignInButton, SignUpButton, UserButton } from '@clerk/nextjs';
import Link from 'next/link';
import { getCurrentCFMWeek, CFM_2026_SCHEDULE, formatCFMWeekDisplay, CFMWeek } from '@/utils/comeFollowMe';

interface SidebarProps {
  selectedSources: string[];
  setSelectedSources: (sources: string[]) => void;
  sourceCount: number;
  setSourceCount: (count: number) => void;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  mode: string;
  setMode: (mode: string) => void;
  cfmWeek: CFMWeek;
  setCfmWeek: (week: CFMWeek) => void;
}

export default function Sidebar({
  selectedSources,
  setSelectedSources,
  sourceCount,
  setSourceCount,
  isOpen,
  setIsOpen,
  mode,
  setMode,
  cfmWeek,
  setCfmWeek,
}: SidebarProps) {
  const { isSignedIn, user } = useUser();
  const [generalConferenceOpen, setGeneralConferenceOpen] = useState(false); // Collapsed by default
  const [standardWorksOpen, setStandardWorksOpen] = useState(false); // Collapsed by default

  const handleSourceToggle = (source: string) => {
    if (selectedSources.includes(source)) {
      setSelectedSources(selectedSources.filter(s => s !== source));
    } else {
      setSelectedSources([...selectedSources, source]);
    }
  };

  const getConferenceSources = () => [
    'general-conference',
    'gc-year-2025', 'gc-year-2024', 'gc-year-2023', 'gc-year-2022', 'gc-year-2021',
    'gc-year-2020', 'gc-year-2019', 'gc-year-2018', 'gc-year-2017', 'gc-year-2016', 'gc-year-2015',
    'gc-speaker-russell-m-nelson', 'gc-speaker-dallin-h-oaks', 'gc-speaker-henry-b-eyring',
    'gc-speaker-jeffrey-r-holland', 'gc-speaker-dieter-f-uchtdorf', 'gc-speaker-david-a-bednar',
    'gc-speaker-quentin-l-cook', 'gc-speaker-d-todd-christofferson', 'gc-speaker-neil-l-andersen',
    'gc-speaker-ronald-a-rasband', 'gc-speaker-gary-e-stevenson', 'gc-speaker-dale-g-renlund'
  ];

  const isAllConferenceSelected = () => {
    const conferenceSources = getConferenceSources();
    const selectedConferenceSources = selectedSources.filter(source => conferenceSources.includes(source));
    return selectedConferenceSources.length >= conferenceSources.length * 0.8;
  };

  const handleToggleAllConference = () => {
    const conferenceSources = getConferenceSources();
    
    if (isAllConferenceSelected()) {
      // Deselect all conference sources
      setSelectedSources(selectedSources.filter(source => !conferenceSources.includes(source)));
    } else {
      // Select all conference sources
      const otherSources = selectedSources.filter(source => !conferenceSources.includes(source));
      setSelectedSources([...otherSources, ...conferenceSources]);
    }
  };

  const getScriptureSources = () => [
    'book-of-mormon', 'doctrine-and-covenants', 'pearl-of-great-price', 'old-testament', 'new-testament'
  ];

  const isAllScripturesSelected = () => {
    const scriptureSources = getScriptureSources();
    const selectedScriptureSources = selectedSources.filter(source => scriptureSources.includes(source));
    return selectedScriptureSources.length >= scriptureSources.length * 0.8;
  };

  const isOnlyConferenceSelected = () => {
    const conferenceSources = getConferenceSources();
    const scriptureSources = getScriptureSources();
    const allSources = [...conferenceSources, ...scriptureSources];
    
    // Check if only conference sources are selected
    const selectedConferenceSources = selectedSources.filter(source => conferenceSources.includes(source));
    const selectedScriptureSources = selectedSources.filter(source => scriptureSources.includes(source));
    
    return selectedConferenceSources.length > 0 && selectedScriptureSources.length === 0;
  };

  const isOnlyScripturesSelected = () => {
    const conferenceSources = getConferenceSources();
    const scriptureSources = getScriptureSources();
    
    // Check if only scripture sources are selected
    const selectedConferenceSources = selectedSources.filter(source => conferenceSources.includes(source));
    const selectedScriptureSources = selectedSources.filter(source => scriptureSources.includes(source));
    
    return selectedScriptureSources.length > 0 && selectedConferenceSources.length === 0;
  };

  const handleToggleAllScriptures = () => {
    const scriptureSources = getScriptureSources();
    
    if (isAllScripturesSelected()) {
      // Deselect all scripture sources
      setSelectedSources(selectedSources.filter(source => !scriptureSources.includes(source)));
    } else {
      // Select all scripture sources
      const otherSources = selectedSources.filter(source => !scriptureSources.includes(source));
      setSelectedSources([...otherSources, ...scriptureSources]);
    }
  };

  const handleSelectGeneralConference = () => {
    const conferenceSources = getConferenceSources();
    setSelectedSources(conferenceSources);
  };

  const handleSelectStandardWorks = () => {
    const scriptureSources = getScriptureSources();
    setSelectedSources(scriptureSources);
  };

  const handleSelectBoth = () => {
    const conferenceSources = getConferenceSources();
    const scriptureSources = getScriptureSources();
    setSelectedSources([...conferenceSources, ...scriptureSources]);
  };

  const handleToggleSelectAll = () => {
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

    // If most sources are selected, deselect all. Otherwise, select all.
    if (selectedSources.length >= allSources.length * 0.8) {
      setSelectedSources([]);
    } else {
      setSelectedSources(allSources);
    }
  };

  const isAllSelected = () => {
    const allSources = [
      'general-conference',
      'gc-year-2025', 'gc-year-2024', 'gc-year-2023', 'gc-year-2022', 'gc-year-2021',
      'gc-year-2020', 'gc-year-2019', 'gc-year-2018', 'gc-year-2017', 'gc-year-2016', 'gc-year-2015',
      'gc-speaker-russell-m-nelson', 'gc-speaker-dallin-h-oaks', 'gc-speaker-henry-b-eyring',
      'gc-speaker-jeffrey-r-holland', 'gc-speaker-dieter-f-uchtdorf', 'gc-speaker-david-a-bednar',
      'gc-speaker-quentin-l-cook', 'gc-speaker-d-todd-christofferson', 'gc-speaker-neil-l-andersen',
      'gc-speaker-ronald-a-rasband', 'gc-speaker-gary-e-stevenson', 'gc-speaker-dale-g-renlund',
      'book-of-mormon', 'doctrine-and-covenants', 'pearl-of-great-price', 'old-testament', 'new-testament'
    ];
    
    // Check if we have both conference and scripture sources selected
    const conferenceSources = getConferenceSources();
    const scriptureSources = getScriptureSources();
    
    const selectedConferenceSources = selectedSources.filter(source => conferenceSources.includes(source));
    const selectedScriptureSources = selectedSources.filter(source => scriptureSources.includes(source));
    
    // Only "all selected" if we have a good representation from BOTH categories
    const hasSignificantConference = selectedConferenceSources.length >= conferenceSources.length * 0.3;
    const hasSignificantScriptures = selectedScriptureSources.length >= scriptureSources.length * 0.8;
    
    return hasSignificantConference && hasSignificantScriptures && selectedSources.length >= allSources.length * 0.6;
  };

  return (
    <div className={`
      w-72 lg:w-80 bg-neutral-900/95 backdrop-blur-sm border-r border-neutral-800/50 flex flex-col
      fixed lg:relative top-0 left-0 h-full z-30 transition-all duration-300 ease-in-out
      ${isOpen ? 'translate-x-0' : '-translate-x-full lg:-translate-x-full'}
      ${isOpen ? 'lg:w-80' : 'lg:hidden'}
    `}>
      {/* Header */}
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-xl overflow-hidden ring-1 ring-neutral-700/50">
              <img 
                src="/christ.jpeg" 
                alt="Gospel Study Logo" 
                className="w-full h-full object-cover"
              />
            </div>
            <h1 className="text-lg font-medium text-white/90">Gospel Study</h1>
          </div>
          {/* Desktop collapse button */}
          <button
            onClick={() => setIsOpen(false)}
            className="hidden lg:block text-neutral-400 hover:text-white/80 p-1.5 rounded-lg hover:bg-neutral-800/50 transition-all"
            title="Collapse sidebar"
          >
            <ChevronLeftIcon className="w-5 h-5" />
          </button>
          {/* Mobile close button */}
          <button
            onClick={() => setIsOpen(false)}
            className="lg:hidden text-neutral-400 hover:text-white/80 p-1.5 rounded-lg hover:bg-neutral-800/50 transition-all"
          >
            <XMarkIcon className="w-5 h-5" />
          </button>
        </div>
        
        {/* Mode Picker */}
        <div className="space-y-3">
          <span className="text-xs font-medium text-neutral-500 uppercase tracking-wider">Study Mode</span>
          <div className="flex bg-neutral-800/50 rounded-xl p-1">
            <button
              onClick={() => setMode('Q&A')}
              className={`relative flex-1 text-sm py-2.5 rounded-lg font-medium transition-all duration-200 ${
                mode === 'Q&A'
                  ? 'bg-blue-500/20 text-blue-300 shadow-lg shadow-blue-500/20 border-l-2 border-blue-400'
                  : 'text-neutral-400 hover:text-white/80'
              }`}
            >
              Q&A
            </button>
            <button
              onClick={() => setMode('Come Follow Me')}
              className={`relative flex-1 text-sm py-2.5 rounded-lg font-medium transition-all duration-200 ${
                mode === 'Come Follow Me'
                  ? 'bg-blue-500/20 text-blue-300 shadow-lg shadow-blue-500/20 border-l-2 border-blue-400'
                  : 'text-neutral-400 hover:text-white/80'
              }`}
            >
              Come Follow Me
            </button>
          </div>
        </div>
      </div>

      {/* Come Follow Me section */}
      {mode === 'Come Follow Me' && (
        <div className="px-6 pb-6 space-y-6 overflow-y-auto flex-1">
          {/* Week Selector */}
          <div className="space-y-3">
            <span className="text-xs font-medium text-neutral-500 uppercase tracking-wider">Lesson</span>
            <select
              value={cfmWeek?.id || ''}
              onChange={(e) => {
                const selectedWeek = CFM_2026_SCHEDULE.find((w: CFMWeek) => w.id === e.target.value);
                setCfmWeek(selectedWeek || CFM_2026_SCHEDULE[0]);
              }}
              className="w-full p-3 bg-neutral-800/50 border-0 rounded-xl text-white text-sm focus:outline-none focus:ring-2 focus:ring-white/20 appearance-none cursor-pointer"
            >
              {CFM_2026_SCHEDULE.map((week: CFMWeek) => (
                <option key={week.id} value={week.id} className="bg-neutral-800">
                  {week.dates}: {week.lesson}
                </option>
              ))}
            </select>
            <div className="p-3 bg-neutral-800/30 rounded-xl border border-neutral-700/30">
              <div className="text-white text-sm font-medium">{cfmWeek?.lesson || 'Select a lesson'}</div>
              <div className="text-neutral-400 text-xs">{cfmWeek?.reference || 'Doctrine & Covenants'}</div>
              {cfmWeek?.dates && (
                <div className="text-neutral-500 text-xs mt-1">{cfmWeek.dates}</div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* Sources to search section - only show in Q&A mode */}
      {mode === 'Q&A' && (
      <div className="px-6 pb-6 space-y-6 overflow-y-auto flex-1">
        <div className="space-y-3">
          <span className="text-xs font-medium text-neutral-500 uppercase tracking-wider">Sources</span>

          {/* Quick filter buttons */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={handleToggleSelectAll}
              className={`relative text-xs px-3 py-2 rounded-lg font-medium transition-all duration-200 ${
                isAllSelected()
                  ? 'bg-blue-500/20 text-blue-300 shadow-lg shadow-blue-500/20 border-l-2 border-blue-400'
                  : 'bg-neutral-800/30 text-neutral-400 hover:text-white/80 hover:bg-neutral-800/50 border border-neutral-700/30'
              }`}
            >
              Select All
            </button>
            <button
              onClick={handleSelectGeneralConference}
              className={`relative text-xs px-3 py-2 rounded-lg font-medium transition-all duration-200 ${
                isOnlyConferenceSelected()
                  ? 'bg-blue-500/20 text-blue-300 shadow-lg shadow-blue-500/20 border-l-2 border-blue-400'
                  : 'bg-neutral-800/30 text-neutral-400 hover:text-white/80 hover:bg-neutral-800/50 border border-neutral-700/30'
              }`}
            >
              Conference
            </button>
            <button
              onClick={handleSelectStandardWorks}
              className={`relative text-xs px-3 py-2 rounded-lg font-medium transition-all duration-200 ${
                isOnlyScripturesSelected()
                  ? 'bg-blue-500/20 text-blue-300 shadow-lg shadow-blue-500/20 border-l-2 border-blue-400'
                  : 'bg-neutral-800/30 text-neutral-400 hover:text-white/80 hover:bg-neutral-800/50 border border-neutral-700/30'
              }`}
            >
              Scriptures
            </button>
          </div>

          {/* Sources count */}
          <div className="bg-neutral-800/30 rounded-xl p-4 border border-neutral-700/30">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-neutral-400">Results per query</span>
              <span className="text-lg font-medium text-white">{sourceCount}</span>
            </div>
            <input
              type="range"
              min="1"
              max="20"
              value={sourceCount}
              onChange={(e) => setSourceCount(parseInt(e.target.value))}
              className="w-full h-2 bg-neutral-700/50 rounded-lg appearance-none cursor-pointer slider"
              style={{
                background: `linear-gradient(to right, #404040 0%, #404040 ${(sourceCount - 1) * 5.26}%, #262626 ${(sourceCount - 1) * 5.26}%, #262626 100%)`
              }}
            />
            <div className="flex justify-between text-xs text-neutral-500 mt-2">
              <span>1</span>
              <span>20</span>
            </div>
          </div>
        </div>

        {/* General Conference dropdown */}
        <div className="space-y-2">
          <button
            onClick={() => setGeneralConferenceOpen(!generalConferenceOpen)}
            className="w-full flex items-center justify-between p-3 bg-neutral-800/30 rounded-xl hover:bg-neutral-800/50 transition-all duration-200 border border-neutral-700/30"
          >
            <div className="flex items-center space-x-3">
              <span className="text-white text-sm font-medium">General Conference</span>
            </div>
            {generalConferenceOpen ? (
              <ChevronUpIcon className="w-4 h-4 text-neutral-400" />
            ) : (
              <ChevronDownIcon className="w-4 h-4 text-neutral-400" />
            )}
          </button>

          {generalConferenceOpen && (
            <div className="ml-3 space-y-2">
              {/* All General Conference */}
              <label className="flex items-center space-x-3 text-sm text-neutral-300 p-2 rounded-lg hover:bg-neutral-800/30 cursor-pointer transition-colors">
                <input
                  type="checkbox"
                  checked={selectedSources.includes('general-conference')}
                  onChange={() => handleSourceToggle('general-conference')}
                  className="w-4 h-4 text-blue-400 bg-neutral-700 border-neutral-600 rounded focus:ring-blue-500/50 focus:ring-2 checked:bg-blue-500 checked:border-blue-400 checked:shadow-lg checked:shadow-blue-500/30"
                />
                <span>All Sessions (2015-2025)</span>
              </label>

              {/* By Year */}
              <div className="space-y-2">
                <div className="text-xs text-neutral-500 font-medium uppercase tracking-wider">By Year</div>
                <div className="grid grid-cols-3 gap-1">
                  {[2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015].map(year => (
                    <label key={year} className="flex items-center space-x-2 text-xs text-neutral-300 p-1.5 rounded-lg hover:bg-neutral-800/30 cursor-pointer transition-colors">
                      <input
                        type="checkbox"
                        checked={selectedSources.includes(`gc-year-${year}`)}
                        onChange={() => handleSourceToggle(`gc-year-${year}`)}
                        className="w-3.5 h-3.5 text-blue-400 bg-neutral-700 border-neutral-600 rounded focus:ring-blue-500/50 focus:ring-1 checked:bg-blue-500 checked:border-blue-400 checked:shadow-sm checked:shadow-blue-500/30"
                      />
                      <span>{year}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* By Speaker */}
              <div className="space-y-2">
                <div className="text-xs text-neutral-500 font-medium uppercase tracking-wider">By Speaker</div>
                <div className="space-y-1">
                  {[
                    'Russell M. Nelson',
                    'Dallin H. Oaks',
                    'Henry B. Eyring',
                    'Jeffrey R. Holland',
                    'Dieter F. Uchtdorf',
                    'David A. Bednar',
                    'Quentin L. Cook',
                    'D. Todd Christofferson',
                    'Neil L. Andersen',
                    'Ronald A. Rasband',
                    'Gary E. Stevenson',
                    'Dale G. Renlund'
                  ].map(speaker => {
                    const speakerKey = `gc-speaker-${speaker.toLowerCase().replace(/\s+/g, '-').replace('.', '')}`;
                    return (
                      <label key={speaker} className="flex items-center space-x-2 text-xs text-neutral-300 p-1.5 rounded-lg hover:bg-neutral-800/30 cursor-pointer transition-colors">
                        <input
                          type="checkbox"
                          checked={selectedSources.includes(speakerKey)}
                          onChange={() => handleSourceToggle(speakerKey)}
                          className="w-3.5 h-3.5 text-blue-400 bg-neutral-700 border-neutral-600 rounded focus:ring-blue-500/50 focus:ring-1 checked:bg-blue-500 checked:border-blue-400 checked:shadow-sm checked:shadow-blue-500/30"
                        />
                        <span>{speaker}</span>
                      </label>
                    );
                  })}
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Standard Works dropdown */}
        <div className="space-y-2">
          <button
            onClick={() => setStandardWorksOpen(!standardWorksOpen)}
            className="w-full flex items-center justify-between p-3 bg-neutral-800/30 rounded-xl hover:bg-neutral-800/50 transition-all duration-200 border border-neutral-700/30"
          >
            <div className="flex items-center space-x-3">
              <span className="text-white text-sm font-medium">Standard Works</span>
            </div>
            {standardWorksOpen ? (
              <ChevronUpIcon className="w-4 h-4 text-neutral-400" />
            ) : (
              <ChevronDownIcon className="w-4 h-4 text-neutral-400" />
            )}
          </button>

          {standardWorksOpen && (
            <div className="ml-3 space-y-2">
              {[
                'Book of Mormon',
                'Doctrine & Covenants',
                'Pearl of Great Price',
                'Old Testament',
                'New Testament'
              ].map((work) => (
                <label key={work} className="flex items-center space-x-3 text-sm text-neutral-300 p-2 rounded-lg hover:bg-neutral-800/30 cursor-pointer transition-colors">
                  <input
                    type="checkbox"
                    checked={selectedSources.includes(work.toLowerCase().replace(/\s+/g, '-').replace('&', 'and'))}
                    onChange={() => handleSourceToggle(work.toLowerCase().replace(/\s+/g, '-').replace('&', 'and'))}
                    className="w-4 h-4 text-blue-400 bg-neutral-700 border-neutral-600 rounded focus:ring-blue-500/50 focus:ring-2 checked:bg-blue-500 checked:border-blue-400 checked:shadow-lg checked:shadow-blue-500/30"
                  />
                  <span>{work}</span>
                </label>
              ))}
            </div>
          )}
        </div>
      </div>
      )}

      {/* Authentication section at bottom */}
      <div className="mt-auto border-t border-neutral-700 p-6">
        {isSignedIn ? (
          <div className="space-y-4">
            {/* User Profile */}
            <div className="flex items-center space-x-3 p-3 bg-neutral-800/30 rounded-lg border border-neutral-700/50">
              <UserButton 
                appearance={{
                  elements: {
                    avatarBox: "w-10 h-10",
                    userButtonPopoverCard: "bg-neutral-800 border border-neutral-700",
                    userButtonPopoverActionButton: "text-neutral-300 hover:text-white hover:bg-neutral-700"
                  }
                }}
              />
              <div className="flex-1 min-w-0">
                <p className="text-sm font-medium text-white truncate">
                  {user?.firstName || user?.emailAddresses[0]?.emailAddress}
                </p>
                <p className="text-xs text-neutral-400">Free Plan • 10 questions/day</p>
              </div>
            </div>
            
            {/* Upgrade to Premium */}
            <Link 
              href="/pricing"
              className="block w-full bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white text-center py-3 px-4 rounded-lg transition-all duration-200 font-medium shadow-lg shadow-blue-500/25"
            >
              ⚡ Upgrade to Premium
            </Link>
          </div>
        ) : (
          <div className="space-y-3">
            {/* Sign In/Sign Up */}
            <SignInButton mode="modal">
              <button className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg transition-colors font-medium">
                Get Started
              </button>
            </SignInButton>
            
            {/* Pricing Link */}
            <Link 
              href="/pricing"
              className="block w-full text-center py-2 px-4 bg-neutral-800/30 hover:bg-neutral-700/50 text-neutral-300 hover:text-white rounded-lg transition-colors text-sm border border-neutral-700/50"
            >
              View Pricing Plans
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}