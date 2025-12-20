'use client';

import { useState } from 'react';

type StudyLevel = 'basic' | 'intermediate' | 'advanced';

interface StudyLevelSliderProps {
  selectedLevel: StudyLevel;
  onLevelChange: (level: StudyLevel) => void;
}

interface LevelInfo {
  id: StudyLevel;
  label: string;
  color: string;
  bgColor: string;
  borderColor: string;
  description: string;
  duration: string;
}

const STUDY_LEVELS: LevelInfo[] = [
  {
    id: 'basic',
    label: 'Basic',
    color: 'text-green-400',
    bgColor: 'bg-green-900/20',
    borderColor: 'border-green-500',
    description: 'Perfect for families and individuals',
    duration: '10-15 min'
  },
  {
    id: 'intermediate',
    label: 'Intermediate',
    color: 'text-yellow-400',
    bgColor: 'bg-yellow-900/20',
    borderColor: 'border-yellow-500',
    description: 'Great for Sunday School teachers',
    duration: '15-20 min'
  },
  {
    id: 'advanced',
    label: 'Advanced',
    color: 'text-red-400',
    bgColor: 'bg-red-900/20',
    borderColor: 'border-red-500',
    description: 'Designed for institute instructors',
    duration: '20-30 min'
  }
];

export default function StudyLevelSlider({ selectedLevel, onLevelChange }: StudyLevelSliderProps) {
  const selectedIndex = STUDY_LEVELS.findIndex(level => level.id === selectedLevel);
  
  return (
    <div className="space-y-4">
      {/* Slider Track */}
      <div className="relative">
        <div className="flex justify-between items-center bg-gray-700 rounded-full p-1">
          {STUDY_LEVELS.map((level, index) => {
            const isSelected = level.id === selectedLevel;
            
            return (
              <button
                key={level.id}
                onClick={() => onLevelChange(level.id)}
                className={`
                  flex-1 py-2 px-3 rounded-full text-sm font-medium transition-all duration-200
                  ${isSelected 
                    ? `${level.bgColor} ${level.color} ${level.borderColor} border shadow-lg` 
                    : 'text-gray-400 hover:text-gray-200 hover:bg-gray-600'
                  }
                `}
              >
                {level.label}
              </button>
            );
          })}
        </div>
        
        {/* Progress indicator */}
        <div className="absolute -bottom-1 left-0 right-0 h-1 bg-gray-600 rounded-full">
          <div 
            className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500 rounded-full transition-all duration-300"
            style={{ 
              width: `${((selectedIndex + 1) / STUDY_LEVELS.length) * 100}%` 
            }}
          />
        </div>
      </div>
      
      {/* Selected Level Info */}
      <div className="text-center">
        <div className={`text-lg font-semibold ${STUDY_LEVELS[selectedIndex].color}`}>
          {STUDY_LEVELS[selectedIndex].label} Study Guide
        </div>
      </div>
    </div>
  );
}