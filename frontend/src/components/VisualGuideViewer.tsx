'use client';

import { useState, useEffect } from 'react';
import Image from 'next/image';
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/24/outline';
import { getCurrentCFMWeek, CFMWeek, CFM_2026_SCHEDULE } from '@/utils/comeFollowMe';

interface VisualGuideViewerProps {
  className?: string;
}

export default function VisualGuideViewer({ className = '' }: VisualGuideViewerProps) {
  const [currentWeek, setCurrentWeek] = useState<CFMWeek>(getCurrentCFMWeek());
  const [imageExists, setImageExists] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Check if image exists for current week
  useEffect(() => {
    const checkImageExists = async () => {
      setIsLoading(true);
      try {
        // Generate filename from week ID: cfm-2026-week-03 -> week_3.png
        const weekNumber = currentWeek.id.replace('cfm-2026-week-', '').replace(/^0+/, ''); // Remove leading zeros
        const response = await fetch(`/visual_guides/week_${weekNumber}.png`);
        setImageExists(response.ok);
      } catch (error) {
        setImageExists(false);
      }
      setIsLoading(false);
    };

    checkImageExists();
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

  // Get current week display info
  const currentIndex = CFM_2026_SCHEDULE.findIndex(week => week.id === currentWeek.id);
  const weekNumber = currentWeek.id.replace('cfm-2026-week-', '').replace(/^0+/, '');

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
          className="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          {CFM_2026_SCHEDULE.map((week, index) => (
            <option key={week.id} value={week.id}>
              {week.lesson}
            </option>
          ))}
        </select>
      </div>

      {/* Visual Guide Content */}
      <div className="p-6">
        {imageExists ? (
          <div className="relative aspect-video rounded-lg overflow-hidden bg-neutral-800">
            <Image
              src={`/visual_guides/week_${weekNumber}.png`}
              alt={`Visual Guide for ${currentWeek.lesson}`}
              fill
              className="object-contain"
              sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
            />
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