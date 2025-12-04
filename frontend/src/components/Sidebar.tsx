'use client';

import { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon, XMarkIcon } from '@heroicons/react/24/outline';
import { getCurrentCFMWeek, CFM_2025_SCHEDULE, CFM_AUDIENCES, formatCFMWeekDisplay, CFMWeek } from '@/utils/comeFollowMe';

interface SidebarProps {
  selectedSources: string[];
  setSelectedSources: (sources: string[]) => void;
  sourceCount: number;
  setSourceCount: (count: number) => void;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
  mode: string;
  setMode: (mode: string) => void;
  cfmAudience: string;
  setCfmAudience: (audience: string) => void;
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
  cfmAudience,
  setCfmAudience,
  cfmWeek,
  setCfmWeek,
}: SidebarProps) {
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
      w-72 lg:w-80 bg-neutral-800 border-r border-neutral-700 flex flex-col
      fixed lg:relative top-0 left-0 h-full z-30 transition-transform duration-300 ease-in-out
      ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
    `}>
      {/* Header */}
      <div className="p-6 border-b border-neutral-700">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg overflow-hidden border border-neutral-600">
              <img 
                src="/christ.jpeg" 
                alt="Gospel Study Logo" 
                className="w-full h-full object-cover"
              />
            </div>
            <h1 className="text-xl font-semibold text-white">Gospel Study</h1>
          </div>
          {/* Mobile close button */}
          <button
            onClick={() => setIsOpen(false)}
            className="lg:hidden text-neutral-400 hover:text-white p-1"
          >
            <XMarkIcon className="w-6 h-6" />
          </button>
        </div>
        
        {/* Mode Picker */}
        <div className="space-y-2">
          <label className="text-sm text-neutral-400">Study Mode:</label>
          <div className="grid grid-cols-2 gap-2">
            <button
              onClick={() => setMode('Q&A')}
              className={`text-sm px-3 py-2 rounded transition-colors ${
                mode === 'Q&A'
                  ? 'bg-blue-600 text-white'
                  : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'
              }`}
            >
              Q&A
            </button>
            <button
              onClick={() => setMode('Come Follow Me')}
              className={`text-sm px-3 py-2 rounded transition-colors ${
                mode === 'Come Follow Me'
                  ? 'bg-blue-600 text-white'
                  : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'
              }`}
            >
              Come Follow Me
            </button>
          </div>
        </div>
      </div>

      {/* Come Follow Me section */}
      {mode === 'Come Follow Me' && (
        <div className="p-4 lg:p-6 space-y-4 overflow-y-auto flex-1">
          {/* Week Selector */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-sm text-neutral-400">Select lesson:</label>
            </div>
            <select
              value={cfmWeek?.id || ''}
              onChange={(e) => {
                const selectedWeek = CFM_2025_SCHEDULE.find(w => w.id === e.target.value);
                setCfmWeek(selectedWeek || CFM_2025_SCHEDULE[0]);
              }}
              className="w-full p-3 bg-neutral-700 border border-neutral-600 rounded-lg text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {CFM_2025_SCHEDULE.map((week) => (
                <option key={week.id} value={week.id}>
                  {week.dates}: {week.lesson}
                </option>
              ))}
            </select>
            <div className="p-3 bg-neutral-700 rounded-lg">
              <div className="text-white text-sm font-medium">{cfmWeek?.lesson || 'Select a lesson'}</div>
              <div className="text-neutral-300 text-xs">{cfmWeek?.reference || 'Doctrine & Covenants'}</div>
              {cfmWeek?.dates && (
                <div className="text-blue-400 text-xs mt-1">{cfmWeek.dates}</div>
              )}
            </div>
          </div>

          {/* Study Audience */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="text-sm text-neutral-400">Study audience:</label>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {CFM_AUDIENCES.map((audience) => (
                <button
                  key={audience.id}
                  onClick={() => setCfmAudience(audience.id)}
                  className={`text-xs px-3 py-1 rounded transition-colors ${
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
        </div>
      )}

      {/* Sources to search section - only show in Q&A mode */}
      {mode === 'Q&A' && (
      <div className="p-4 lg:p-6 space-y-4 overflow-y-auto flex-1">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-sm text-neutral-400">Sources to search:</label>
          </div>

          {/* Quick filter buttons */}
          <div className="flex flex-wrap gap-2">
            <button
              onClick={handleToggleSelectAll}
              className={`text-xs px-3 py-1 rounded transition-colors ${
                isAllSelected()
                  ? 'bg-blue-600 text-white'
                  : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'
              }`}
            >
              Select All
            </button>
            <button
              onClick={handleSelectGeneralConference}
              className={`text-xs px-3 py-1 rounded transition-colors ${
                isOnlyConferenceSelected()
                  ? 'bg-blue-600 text-white'
                  : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'
              }`}
            >
              General Conference
            </button>
            <button
              onClick={handleSelectStandardWorks}
              className={`text-xs px-3 py-1 rounded transition-colors ${
                isOnlyScripturesSelected()
                  ? 'bg-blue-600 text-white'
                  : 'bg-neutral-700 hover:bg-neutral-600 text-neutral-300'
              }`}
            >
              Scriptures
            </button>
          </div>

          <div className="text-2xl font-bold text-white">{sourceCount}</div>
          
          {/* Range slider */}
          <div className="relative">
            <input
              type="range"
              min="1"
              max="20"
              value={sourceCount}
              onChange={(e) => setSourceCount(parseInt(e.target.value))}
              className="w-full h-2 bg-neutral-700 rounded-lg appearance-none cursor-pointer slider"
              style={{
                background: `linear-gradient(to right, #525252 0%, #525252 ${(sourceCount - 1) * 5.26}%, #374151 ${(sourceCount - 1) * 5.26}%, #374151 100%)`
              }}
            />
            <div className="flex justify-between text-xs text-neutral-500 mt-1">
              <span>1</span>
              <span>20</span>
            </div>
          </div>
        </div>

        <div className="text-sm text-neutral-400 mt-4">
          Select your sources
        </div>

        {/* General Conference dropdown */}
        <div className="space-y-2">
          <button
            onClick={() => setGeneralConferenceOpen(!generalConferenceOpen)}
            className="w-full flex items-center justify-between p-3 bg-neutral-700 rounded-lg hover:bg-neutral-600 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <span className="text-white text-sm">General Conference</span>
            </div>
            {generalConferenceOpen ? (
              <ChevronUpIcon className="w-4 h-4 text-neutral-400" />
            ) : (
              <ChevronDownIcon className="w-4 h-4 text-neutral-400" />
            )}
          </button>

          {generalConferenceOpen && (
            <div className="ml-6 space-y-3">
              {/* All General Conference */}
              <label className="flex items-center space-x-2 text-sm text-neutral-300">
                <input
                  type="checkbox"
                  checked={selectedSources.includes('general-conference')}
                  onChange={() => handleSourceToggle('general-conference')}
                  className="rounded"
                />
                <span>All Sessions (2015-2025)</span>
              </label>

              {/* By Year */}
              <div className="space-y-1">
                <div className="text-xs text-neutral-400 font-medium">By Year:</div>
                <div className="grid grid-cols-2 gap-1">
                  {[2025, 2024, 2023, 2022, 2021, 2020, 2019, 2018, 2017, 2016, 2015].map(year => (
                    <label key={year} className="flex items-center space-x-1 text-xs text-neutral-300">
                      <input
                        type="checkbox"
                        checked={selectedSources.includes(`gc-year-${year}`)}
                        onChange={() => handleSourceToggle(`gc-year-${year}`)}
                        className="rounded text-xs"
                      />
                      <span>{year}</span>
                    </label>
                  ))}
                </div>
              </div>

              {/* By Speaker */}
              <div className="space-y-1">
                <div className="text-xs text-neutral-400 font-medium">By Speaker:</div>
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
                      <label key={speaker} className="flex items-center space-x-1 text-xs text-neutral-300">
                        <input
                          type="checkbox"
                          checked={selectedSources.includes(speakerKey)}
                          onChange={() => handleSourceToggle(speakerKey)}
                          className="rounded text-xs"
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
            className="w-full flex items-center justify-between p-3 bg-neutral-700 rounded-lg hover:bg-neutral-600 transition-colors"
          >
            <div className="flex items-center space-x-3">
              <span className="text-white text-sm">Standard Works</span>
            </div>
            {standardWorksOpen ? (
              <ChevronUpIcon className="w-4 h-4 text-neutral-400" />
            ) : (
              <ChevronDownIcon className="w-4 h-4 text-neutral-400" />
            )}
          </button>

          {standardWorksOpen && (
            <div className="ml-6 space-y-2">
              {[
                'Book of Mormon',
                'Doctrine & Covenants',
                'Pearl of Great Price',
                'Old Testament',
                'New Testament'
              ].map((work) => (
                <label key={work} className="flex items-center space-x-2 text-sm text-neutral-300">
                  <input
                    type="checkbox"
                    checked={selectedSources.includes(work.toLowerCase().replace(/\s+/g, '-').replace('&', 'and'))}
                    onChange={() => handleSourceToggle(work.toLowerCase().replace(/\s+/g, '-').replace('&', 'and'))}
                    className="rounded"
                  />
                  <span>{work}</span>
                </label>
              ))}
            </div>
          )}
        </div>
      </div>
      )}
    </div>
  );
}