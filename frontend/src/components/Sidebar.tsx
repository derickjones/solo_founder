'use client';

import { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface SidebarProps {
  selectedSources: string[];
  setSelectedSources: (sources: string[]) => void;
  sourceCount: number;
  setSourceCount: (count: number) => void;
  isOpen: boolean;
  setIsOpen: (open: boolean) => void;
}

export default function Sidebar({
  selectedSources,
  setSelectedSources,
  sourceCount,
  setSourceCount,
  isOpen,
  setIsOpen,
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

  const handleUnselectAllConference = () => {
    const conferenceSourcesToRemove = [
      'general-conference',
      'gc-year-2025', 'gc-year-2024', 'gc-year-2023', 'gc-year-2022', 'gc-year-2021',
      'gc-year-2020', 'gc-year-2019', 'gc-year-2018', 'gc-year-2017', 'gc-year-2016', 'gc-year-2015',
      'gc-speaker-russell-m-nelson', 'gc-speaker-dallin-h-oaks', 'gc-speaker-henry-b-eyring',
      'gc-speaker-jeffrey-r-holland', 'gc-speaker-dieter-f-uchtdorf', 'gc-speaker-david-a-bednar',
      'gc-speaker-quentin-l-cook', 'gc-speaker-d-todd-christofferson', 'gc-speaker-neil-l-andersen',
      'gc-speaker-ronald-a-rasband', 'gc-speaker-gary-e-stevenson', 'gc-speaker-dale-g-renlund'
    ];
    setSelectedSources(selectedSources.filter(source => !conferenceSourcesToRemove.includes(source)));
  };

  const handleUnselectAllScriptures = () => {
    const scriptureSourcesToRemove = [
      'book-of-mormon', 'doctrine-and-covenants', 'pearl-of-great-price', 'old-testament', 'new-testament'
    ];
    setSelectedSources(selectedSources.filter(source => !scriptureSourcesToRemove.includes(source)));
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
    return selectedSources.length >= allSources.length * 0.8;
  };

  return (
    <div className={`
      w-72 lg:w-80 bg-neutral-800 border-r border-neutral-700 flex flex-col
      fixed lg:relative top-0 left-0 h-full z-30 transition-transform duration-300 ease-in-out
      ${isOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
    `}>
      {/* Header */}
      <div className="p-6 border-b border-neutral-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 bg-neutral-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">G</span>
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
      </div>

      {/* Sources to search section */}
      <div className="p-4 lg:p-6 space-y-4 overflow-y-auto flex-1">
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <label className="text-sm text-neutral-400">Sources to search:</label>
            <button
              onClick={handleToggleSelectAll}
              className={`text-xs px-3 py-1 rounded transition-colors ${
                isAllSelected()
                  ? 'bg-red-600 hover:bg-red-500 text-white'
                  : 'bg-blue-600 hover:bg-blue-500 text-white'
              }`}
            >
              {isAllSelected() ? 'Deselect All' : 'Select All'}
            </button>
          </div>
          <div className="text-2xl font-bold text-white">{sourceCount}</div>
          
          {/* Range slider */}
          <div className="relative">
            <input
              type="range"
              min="1"
              max="10"
              value={sourceCount}
              onChange={(e) => setSourceCount(parseInt(e.target.value))}
              className="w-full h-2 bg-neutral-700 rounded-lg appearance-none cursor-pointer slider"
              style={{
                background: `linear-gradient(to right, #525252 0%, #525252 ${(sourceCount - 1) * 11.11}%, #374151 ${(sourceCount - 1) * 11.11}%, #374151 100%)`
              }}
            />
            <div className="flex justify-between text-xs text-neutral-500 mt-1">
              <span>1</span>
              <span>10</span>
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
              <div className="w-6 h-6 bg-neutral-600 rounded flex items-center justify-center">
                <span className="text-white text-xs">GC</span>
              </div>
              <span className="text-white text-sm">General Conference</span>
              <span className="bg-neutral-600 text-white text-xs px-2 py-1 rounded">1</span>
            </div>
            {generalConferenceOpen ? (
              <ChevronUpIcon className="w-4 h-4 text-neutral-400" />
            ) : (
              <ChevronDownIcon className="w-4 h-4 text-neutral-400" />
            )}
          </button>

          {generalConferenceOpen && (
            <div className="ml-6 space-y-3">
              {/* Unselect All Button */}
              <button
                onClick={handleUnselectAllConference}
                className="text-xs text-red-400 hover:text-red-300 transition-colors underline"
              >
                Unselect All Conference
              </button>

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
              <div className="w-6 h-6 bg-neutral-600 rounded flex items-center justify-center">
                <span className="text-white text-xs">SW</span>
              </div>
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
              {/* Unselect All Button */}
              <button
                onClick={handleUnselectAllScriptures}
                className="text-xs text-red-400 hover:text-red-300 transition-colors underline mb-2"
              >
                Unselect All Scriptures
              </button>

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
    </div>
  );
}