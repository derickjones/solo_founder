'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { ChevronLeftIcon, ChevronRightIcon, DocumentIcon } from '@heroicons/react/24/outline';
import { getCurrentCFMWeek, CFMWeek, CFM_2026_SCHEDULE } from '@/utils/comeFollowMe';
import { useUsageLimit } from '@/hooks/useUsageLimit';

interface VisualGuideViewerProps {
  className?: string;
}

type GuideType = 'infographic' | 'slides';

interface AvailableGuides {
  infographic: boolean;
  slides: boolean;
}

export default function VisualGuideViewer({ className = '' }: VisualGuideViewerProps) {
  const [currentWeek, setCurrentWeek] = useState<CFMWeek>(getCurrentCFMWeek());
  const [availableGuides, setAvailableGuides] = useState<AvailableGuides>({ infographic: false, slides: false });
  const [currentGuideType, setCurrentGuideType] = useState<GuideType>('infographic');
  const [isLoading, setIsLoading] = useState(true);
  const { recordAction } = useUsageLimit();

  // Track usage when component mounts
  useEffect(() => {
    recordAction('visual_guide', { week: currentWeek.lesson });
  }, []); // Only run once on mount

  // Check if guides exist for current week
  useEffect(() => {
    const checkGuidesExist = async () => {
      setIsLoading(true);
      try {
        // Generate filename from week ID: cfm-2026-week-03 -> 3
        const weekNumber = currentWeek.id.replace('cfm-2026-week-', '').replace(/^0+/, ''); // Remove leading zeros
        
        // Check for infographic
        const infographicResponse = await fetch(`/visual_guides/infographic_${weekNumber}.png`);
        const infographicExists = infographicResponse.ok;
        
        // Check for slides
        const slidesResponse = await fetch(`/visual_guides/slides_${weekNumber}.pdf`);
        const slidesExists = slidesResponse.ok;
        
        setAvailableGuides({ infographic: infographicExists, slides: slidesExists });
        
        // Set default guide type to infographic if available, otherwise slides
        if (infographicExists) {
          setCurrentGuideType('infographic');
        } else if (slidesExists) {
          setCurrentGuideType('slides');
        }
      } catch (error) {
        setAvailableGuides({ infographic: false, slides: false });
      }
      setIsLoading(false);
    };

    checkGuidesExist();
  }, [currentWeek]);

  const handlePreviousWeek = () => {
    const currentIndex = CFM_2026_SCHEDULE.findIndex(week => week.id === currentWeek.id);
    if (currentIndex > 0) {
      setCurrentWeek(CFM_2026_SCHEDULE[currentIndex - 1]);
    }
  };

  const handleNextWeek = () => {
    const currentIndex = CFM_2026_SCHEDULE.findIndex(week => week.id === currentWeek.id);
    if (currentIndex < CFM_2026_SCHEDULE.length - 1) {
      setCurrentWeek(CFM_2026_SCHEDULE[currentIndex + 1]);
    }
  };

  const handleWeekSelect = (weekId: string) => {
    const selectedWeek = CFM_2026_SCHEDULE.find(week => week.id === weekId);
    if (selectedWeek) {
      setCurrentWeek(selectedWeek);
    }
  };

  const handleGuideTypeChange = (type: GuideType) => {
    if (availableGuides[type]) {
      setCurrentGuideType(type);
    }
  };

  // Get current week display info
  const currentIndex = CFM_2026_SCHEDULE.findIndex(week => week.id === currentWeek.id);
  const weekNumber = currentWeek.id.replace('cfm-2026-week-', '').replace(/^0+/, '');
  const hasAnyGuides = availableGuides.infographic || availableGuides.slides;

  if (isLoading) {
    return (
      <div className={`bg-neutral-900 rounded-xl p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-8 bg-neutral-700 rounded mb-4"></div>
          <div className="aspect-video bg-neutral-700 rounded"></div>
        </div>
      </div>
    );
  }

  return (
    <div className={`bg-neutral-900 rounded-xl overflow-hidden ${className}`}>
      {/* Header */}
      <div className="p-6 border-b border-neutral-800">
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-xl font-semibold text-white">Visual Guides</h2>
          <div className="flex items-center gap-2">
            <button
              onClick={handlePreviousWeek}
              disabled={currentIndex === 0}
              className="p-2 rounded-lg bg-neutral-800 hover:bg-neutral-700 disabled:opacity-50 disabled:cursor-not-allowed text-neutral-300 hover:text-white transition-all"
            >
              <ChevronLeftIcon className="w-4 h-4" />
            </button>
            <span className="text-sm text-neutral-400 min-w-[80px] text-center">
              Week {weekNumber}
            </span>
            <button
              onClick={handleNextWeek}
              disabled={currentIndex === CFM_2026_SCHEDULE.length - 1}
              className="p-2 rounded-lg bg-neutral-800 hover:bg-neutral-700 disabled:opacity-50 disabled:cursor-not-allowed text-neutral-300 hover:text-white transition-all"
            >
              <ChevronRightIcon className="w-4 h-4" />
            </button>
          </div>
        </div>

        {/* Week selector dropdown */}
        <select
          value={currentWeek.id}
          onChange={(e) => handleWeekSelect(e.target.value)}
          className="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 mb-4"
        >
          {CFM_2026_SCHEDULE.map((week, index) => (
            <option key={week.id} value={week.id}>
              {week.lesson}
            </option>
          ))}
        </select>

        {/* Guide type selector - only show if we have guides */}
        {hasAnyGuides && (
          <div className="flex gap-2">
            {availableGuides.infographic && (
              <button
                onClick={() => handleGuideTypeChange('infographic')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  currentGuideType === 'infographic'
                    ? 'bg-blue-600 text-white'
                    : 'bg-neutral-800 text-neutral-300 hover:bg-neutral-700 hover:text-white'
                }`}
              >
                📊 Infographic
              </button>
            )}
            {availableGuides.slides && (
              <button
                onClick={() => handleGuideTypeChange('slides')}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  currentGuideType === 'slides'
                    ? 'bg-blue-600 text-white'
                    : 'bg-neutral-800 text-neutral-300 hover:bg-neutral-700 hover:text-white'
                }`}
              >
                <DocumentIcon className="w-4 h-4 inline mr-1" />
                Slides
              </button>
            )}
          </div>
        )}
      </div>

      {/* Visual Guide Content */}
      <div className="p-6">
        {hasAnyGuides && availableGuides[currentGuideType] ? (
          <div className="relative aspect-video rounded-lg overflow-hidden bg-neutral-800">
            {currentGuideType === 'infographic' ? (
              <Image
                src={`/visual_guides/infographic_${weekNumber}.png`}
                alt={`Visual Guide Infographic for ${currentWeek.lesson}`}
                fill
                className="object-contain"
                sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
              />
            ) : (
              <div className="w-full h-full flex flex-col">
                <iframe
                  src={`/visual_guides/slides_${weekNumber}.pdf`}
                  className="w-full h-full border-0"
                  title={`Slides for ${currentWeek.lesson}`}
                />
                <div className="absolute top-4 right-4">
                  <a
                    href={`/visual_guides/slides_${weekNumber}.pdf`}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="px-3 py-1 bg-blue-600 text-white text-xs rounded-md hover:bg-blue-700 transition-colors"
                  >
                    Open PDF
                  </a>
                </div>
              </div>
            )}
          </div>
        ) : (
          <div className="aspect-video rounded-lg bg-neutral-800 border-2 border-dashed border-neutral-600 flex items-center justify-center">
            <div className="text-center text-neutral-500">
              <div className="text-2xl mb-2">📊</div>
              <p className="text-sm">{currentWeek.lesson}</p>
              <p className="text-xs mt-1">Visual Guide Coming Soon</p>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}