'use client';

import { useState } from 'react';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';

interface SidebarProps {
  selectedSources: string[];
  setSelectedSources: (sources: string[]) => void;
  sourceCount: number;
  setSourceCount: (count: number) => void;
}

export default function Sidebar({
  selectedSources,
  setSelectedSources,
  sourceCount,
  setSourceCount,
}: SidebarProps) {
  const [generalConferenceOpen, setGeneralConferenceOpen] = useState(false);
  const [standardWorksOpen, setStandardWorksOpen] = useState(false);

  const handleSourceToggle = (source: string) => {
    if (selectedSources.includes(source)) {
      setSelectedSources(selectedSources.filter(s => s !== source));
    } else {
      setSelectedSources([...selectedSources, source]);
    }
  };

  return (
    <div className="w-80 bg-neutral-800 border-r border-neutral-700 flex flex-col">
      {/* Header */}
      <div className="p-6 border-b border-neutral-700">
        <div className="flex items-center space-x-3">
          <div className="w-8 h-8 bg-neutral-600 rounded-lg flex items-center justify-center">
            <span className="text-white font-bold text-sm">G</span>
          </div>
          <h1 className="text-xl font-semibold text-white">Gospel Study</h1>
        </div>
      </div>

      {/* Sources to search section */}
      <div className="p-6 space-y-4">
        <div className="space-y-3">
          <label className="text-sm text-neutral-400">Sources to search:</label>
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
                <span className="text-white text-xs">🎤</span>
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
                <span className="text-white text-xs">📖</span>
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