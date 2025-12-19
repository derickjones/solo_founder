'use client';

import { useState, useEffect } from 'react';
import { getCurrentCFMWeek, CFMWeek, formatCFMWeekDisplay, CFM_2026_SCHEDULE } from '@/utils/comeFollowMe';
import StudyLevelSlider from '@/components/StudyLevelSlider';
import { generateCFMDeepDive, CFMDeepDiveRequest } from '@/services/api';
import { ChevronLeftIcon, ArrowDownTrayIcon, ClipboardDocumentIcon, CheckIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import ReactMarkdown from 'react-markdown';
import { generateLessonPlanPDF, LessonPlanData } from '@/utils/pdfGenerator';

type StudyLevel = 'basic' | 'intermediate' | 'advanced';

export default function ComeFollowMePage() {
  const [currentWeek, setCurrentWeek] = useState<CFMWeek>(getCurrentCFMWeek());
  const [studyLevel, setStudyLevel] = useState<StudyLevel>('basic');
  const [studyGuide, setStudyGuide] = useState<string | null>(null);
  const [isGenerating, setIsGenerating] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [generationTime, setGenerationTime] = useState<number | null>(null);
  const [copiedToClipboard, setCopiedToClipboard] = useState(false);

  // Reset study guide when study level or week changes
  useEffect(() => {
    setStudyGuide(null);
    setError(null);
    setGenerationTime(null);
  }, [studyLevel, currentWeek]);

  // Get week number from CFM schedule
  const getWeekNumber = (week: CFMWeek): number => {
    const index = CFM_2026_SCHEDULE.findIndex((w: CFMWeek) => w.id === week.id);
    return index >= 0 ? index + 1 : 1;
  };

  const generateStudyGuide = async () => {
    try {
      setIsGenerating(true);
      setError(null);
      setStudyGuide(null);
      setGenerationTime(null);

      const weekNumber = getWeekNumber(currentWeek);
      const request: CFMDeepDiveRequest = {
        week_number: weekNumber,
        study_level: studyLevel,
      };

      const response = await generateCFMDeepDive(request);
      setStudyGuide(response.study_guide);
      setGenerationTime(response.generation_time);
    } catch (err) {
      console.error('Error generating study guide:', err);
      setError(err instanceof Error ? err.message : 'Failed to generate study guide');
    } finally {
      setIsGenerating(false);
    }
  };

  // Copy to clipboard handler
  const handleCopyToClipboard = async () => {
    if (!studyGuide) return;
    
    try {
      await navigator.clipboard.writeText(studyGuide);
      setCopiedToClipboard(true);
      setTimeout(() => setCopiedToClipboard(false), 2000);
    } catch (error) {
      console.error('Failed to copy to clipboard:', error);
    }
  };

  // PDF download handler
  const handleDownloadPDF = async () => {
    if (!studyGuide) return;
    
    try {
      const lessonData: LessonPlanData = {
        title: `${studyLevel.charAt(0).toUpperCase() + studyLevel.slice(1)} Study Guide`,
        date: currentWeek.dates,
        audience: studyLevel,
        content: studyGuide,
        scripture: currentWeek.reference
      };

      await generateLessonPlanPDF(lessonData);
    } catch (error) {
      console.error('Error downloading PDF:', error);
      alert('Error generating PDF. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      {/* Header */}
      <header className="bg-gray-800 border-b border-gray-700">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <Link 
                href="/" 
                className="inline-flex items-center text-gray-400 hover:text-white transition-colors"
              >
                <ChevronLeftIcon className="h-5 w-5 mr-2" />
                Back to Study Assistant
              </Link>
              <div className="h-6 w-px bg-gray-600" />
              <h1 className="text-xl font-semibold">Come Follow Me Study Guide</h1>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - Current Week & Controls */}
          <div className="lg:col-span-1 space-y-6">
            {/* Current Week Card */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-lg font-semibold mb-4 text-blue-400">Current Week</h2>
              <div className="space-y-3">
                <div className="text-sm text-gray-400">Week {getWeekNumber(currentWeek)}</div>
                <div className="text-lg font-medium">{formatCFMWeekDisplay(currentWeek)}</div>
                <div className="text-sm text-gray-400">{currentWeek.reference}</div>
                <div className="text-xs text-gray-500 bg-gray-900 px-3 py-2 rounded">
                  {currentWeek.dates}
                </div>
              </div>

              {/* Week Selector */}
              <div className="mt-4">
                <label className="block text-sm font-medium text-gray-400 mb-2">
                  Change Week (Optional)
                </label>
                <select
                  value={currentWeek.id}
                  onChange={(e) => {
                    const selected = CFM_2026_SCHEDULE.find((w: CFMWeek) => w.id === e.target.value);
                    if (selected) setCurrentWeek(selected);
                  }}
                  className="w-full bg-gray-900 border border-gray-600 rounded-lg px-3 py-2 text-sm text-white focus:border-blue-500 focus:ring-1 focus:ring-blue-500"
                >
                  {CFM_2026_SCHEDULE.map((week: CFMWeek, index: number) => (
                    <option key={week.id} value={week.id}>
                      Week {index + 1}: {week.lesson}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {/* Study Level Slider */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
              <h2 className="text-lg font-semibold mb-4 text-blue-400">Study Level</h2>
              <StudyLevelSlider 
                selectedLevel={studyLevel} 
                onLevelChange={setStudyLevel}
              />

              {/* Generate Button */}
              <button
                onClick={generateStudyGuide}
                disabled={isGenerating}
                className="w-full mt-6 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-700 disabled:text-gray-400 text-white font-medium py-3 px-4 rounded-lg transition-colors"
              >
                {isGenerating ? (
                  <div className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-2"></div>
                    Generating Study Guide...
                  </div>
                ) : (
                  'Generate Study Guide'
                )}
              </button>

              {error && (
                <div className="mt-4 p-3 bg-red-900 border border-red-700 rounded-lg text-red-200 text-sm">
                  {error}
                </div>
              )}

              {generationTime && (
                <div className="mt-4 text-xs text-gray-500 text-center">
                  Generated in {generationTime.toFixed(1)}s
                </div>
              )}
            </div>

            {/* Audio Summary Placeholder */}
            <div className="bg-gray-800 rounded-lg p-6 border border-gray-700 border-dashed opacity-60">
              <h2 className="text-lg font-semibold mb-4 text-gray-400">🎵 Audio Summary</h2>
              <div className="text-center space-y-3">
                <div className="text-gray-500 text-sm">Coming Soon!</div>
                <div className="text-xs text-gray-600">
                  Listen to AI-generated audio summaries of your study guides
                </div>
                <button
                  disabled
                  className="w-full bg-gray-700 text-gray-500 py-2 px-4 rounded-lg cursor-not-allowed"
                >
                  🎧 Generate Audio Summary
                </button>
              </div>
            </div>
          </div>

          {/* Right Column - Study Guide */}
          <div className="lg:col-span-2">
            <div className="bg-gray-800 rounded-lg border border-gray-700">
              {/* Header */}
              <div className="flex items-center justify-between p-6 border-b border-gray-700">
                <h2 className="text-xl font-semibold text-white">
                  {studyGuide ? `${studyLevel.charAt(0).toUpperCase() + studyLevel.slice(1)} Study Guide` : 'Study Guide'}
                </h2>
                
                {studyGuide && (
                  <div className="flex items-center space-x-2">
                    <button
                      onClick={handleCopyToClipboard}
                      className="flex items-center space-x-1 px-3 py-1.5 text-gray-400 hover:text-white bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                    >
                      {copiedToClipboard ? (
                        <>
                          <CheckIcon className="h-4 w-4" />
                          <span className="text-sm">Copied!</span>
                        </>
                      ) : (
                        <>
                          <ClipboardDocumentIcon className="h-4 w-4" />
                          <span className="text-sm">Copy</span>
                        </>
                      )}
                    </button>
                    
                    <button
                      onClick={handleDownloadPDF}
                      className="flex items-center space-x-1 px-3 py-1.5 text-gray-400 hover:text-white bg-gray-700 hover:bg-gray-600 rounded-lg transition-colors"
                    >
                      <ArrowDownTrayIcon className="h-4 w-4" />
                      <span className="text-sm">PDF</span>
                    </button>
                  </div>
                )}
              </div>

              {/* Content */}
              <div className="p-6">
                {!studyGuide && !isGenerating && (
                  <div className="text-center py-16">
                    <div className="text-gray-400 mb-4">
                      <svg className="w-16 h-16 mx-auto mb-4 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253" />
                      </svg>
                    </div>
                    <h3 className="text-lg font-medium text-gray-300 mb-2">Ready to Generate Your Study Guide</h3>
                    <p className="text-gray-500 mb-6 max-w-md mx-auto">
                      Select your preferred study level and click "Generate Study Guide" to create a personalized study guide for this week's Come Follow Me lesson.
                    </p>
                  </div>
                )}

                {studyGuide && (
                  <div className="prose prose-invert max-w-none">
                    <ReactMarkdown
                      components={{
                        h1: ({ children }) => <h1 className="text-2xl font-bold text-white mb-6">{children}</h1>,
                        h2: ({ children }) => <h2 className="text-xl font-semibold text-blue-400 mb-4 mt-8">{children}</h2>,
                        h3: ({ children }) => <h3 className="text-lg font-medium text-yellow-400 mb-3 mt-6">{children}</h3>,
                        p: ({ children }) => <p className="text-gray-300 mb-4 leading-relaxed">{children}</p>,
                        ul: ({ children }) => <ul className="text-gray-300 mb-4 space-y-2">{children}</ul>,
                        ol: ({ children }) => <ol className="text-gray-300 mb-4 space-y-2">{children}</ol>,
                        li: ({ children }) => <li className="ml-4">{children}</li>,
                        strong: ({ children }) => <strong className="text-white font-semibold">{children}</strong>,
                        em: ({ children }) => <em className="text-yellow-200">{children}</em>,
                        blockquote: ({ children }) => (
                          <blockquote className="border-l-4 border-blue-500 pl-6 py-2 my-4 bg-gray-900 rounded-r-lg">
                            <div className="text-blue-200 italic">{children}</div>
                          </blockquote>
                        ),
                      }}
                    >
                      {studyGuide}
                    </ReactMarkdown>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  );
}