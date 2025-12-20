'use client';

import { useState, useRef, useEffect } from 'react';
import { PlayIcon, PauseIcon, SpeakerWaveIcon } from '@heroicons/react/24/solid';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';

interface AudioPlayerProps {
  audioFiles: {
    combined?: string;
  };
  title: string;
}

export default function AudioPlayer({ audioFiles, title }: AudioPlayerProps) {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(0.8);
  const [playbackRate, setPlaybackRate] = useState(1.0);
  const [isLoaded, setIsLoaded] = useState(false);
  const [isExpanded, setIsExpanded] = useState(true);
  const audioRef = useRef<HTMLAudioElement>(null);

  // Use the combined audio file
  const audioData = audioFiles.combined;

  // Convert base64 to blob URL
  const getAudioUrl = (base64Data: string) => {
    const binaryString = atob(base64Data);
    const bytes = new Uint8Array(binaryString.length);
    for (let i = 0; i < binaryString.length; i++) {
      bytes[i] = binaryString.charCodeAt(i);
    }
    const blob = new Blob([bytes], { type: 'audio/mpeg' });
    return URL.createObjectURL(blob);
  };

  // Initialize audio when component loads
  useEffect(() => {
    if (audioRef.current && audioData && !isLoaded) {
      const audioUrl = getAudioUrl(audioData);
      audioRef.current.src = audioUrl;
      audioRef.current.volume = volume;
      audioRef.current.playbackRate = playbackRate;
      setIsLoaded(true);
    }
  }, [audioData, isLoaded, volume, playbackRate]);

  // Toggle play/pause
  const togglePlayPause = () => {
    if (!audioRef.current) return;

    if (isPlaying) {
      audioRef.current.pause();
    } else {
      audioRef.current.play();
    }
    setIsPlaying(!isPlaying);
  };

  // Handle time updates
  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => setCurrentTime(audio.currentTime);
    const updateDuration = () => setDuration(audio.duration);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', updateDuration);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateDuration);
      audio.removeEventListener('ended', handleEnded);
    };
  }, [isLoaded]);

  // Seek to position
  const seek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current;
    if (!audio) return;
    
    const seekTime = (parseFloat(e.target.value) / 100) * duration;
    audio.currentTime = seekTime;
    setCurrentTime(seekTime);
  };

  // Handle volume change
  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    if (audioRef.current) {
      audioRef.current.volume = newVolume;
    }
  };

  // Handle playback speed change
  const handlePlaybackRateChange = (rate: number) => {
    setPlaybackRate(rate);
    if (audioRef.current) {
      audioRef.current.playbackRate = rate;
    }
  };

  // Format time display
  const formatTime = (seconds: number) => {
    if (isNaN(seconds)) return '0:00';
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  return (
    <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-50 to-indigo-50 border-b border-slate-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full flex items-center justify-center shadow-lg">
              <span className="text-white text-lg">🎧</span>
            </div>
            <div>
              <h3 className="font-semibold text-slate-900">Gospel Summary</h3>
              <p className="text-sm text-slate-600">{title}</p>
            </div>
          </div>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 hover:bg-white/50 rounded-lg transition-colors"
          >
            {isExpanded ? (
              <ChevronUpIcon className="w-5 h-5 text-slate-500" />
            ) : (
              <ChevronDownIcon className="w-5 h-5 text-slate-500" />
            )}
          </button>
        </div>
      </div>

      {/* Player Controls */}
      {isExpanded && (
        <div className="p-6 space-y-4">
          {!audioData ? (
            /* Loading State */
            <div className="flex items-center space-x-3">
              <div className="w-14 h-14 bg-slate-200 rounded-full flex items-center justify-center animate-pulse">
                <div className="w-7 h-7 bg-slate-300 rounded-full"></div>
              </div>
              <div className="flex-1">
                <p className="text-slate-600 font-medium">Generating audio summary...</p>
                <p className="text-sm text-slate-500">This may take a few moments</p>
              </div>
            </div>
          ) : (
            <>
              {/* Main Controls */}
              <div className="flex items-center space-x-4">
                <button
                  onClick={togglePlayPause}
                  className="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-blue-500 to-indigo-500 hover:from-blue-600 hover:to-indigo-600 text-white rounded-full transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  {isPlaying ? (
                    <PauseIcon className="w-7 h-7" />
                  ) : (
                    <PlayIcon className="w-7 h-7 ml-0.5" />
                  )}
                </button>
                
                <div className="flex-1 space-y-2">
                  {/* Progress Bar */}
                  <div className="relative">
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={duration ? (currentTime / duration) * 100 : 0}
                      onChange={seek}
                      className="w-full h-2 bg-slate-200 rounded-full appearance-none cursor-pointer progress-slider"
                    />
                    <div 
                      className="absolute top-0 left-0 h-2 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-full pointer-events-none transition-all duration-75"
                      style={{ width: `${duration ? (currentTime / duration) * 100 : 0}%` }}
                    />
                  </div>
                  
                  {/* Time Display */}
                  <div className="flex justify-between text-sm text-slate-500 font-medium">
                    <span>{formatTime(currentTime)}</span>
                    <span>{formatTime(duration)}</span>
                  </div>
                </div>
                
                {/* Volume Control */}
                <div className="flex items-center space-x-3">
                  <SpeakerWaveIcon className="w-5 h-5 text-slate-400" />
                  <div className="relative w-20">
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={volume}
                      onChange={handleVolumeChange}
                      className="w-full h-2 bg-slate-200 rounded-full appearance-none cursor-pointer volume-slider"
                    />
                    <div 
                      className="absolute top-0 left-0 h-2 bg-gradient-to-r from-slate-400 to-slate-500 rounded-full pointer-events-none"
                      style={{ width: `${volume * 100}%` }}
                    />
                  </div>
                </div>
              </div>
              
              {/* Playback Speed Controls */}
              <div className="flex items-center justify-center space-x-2">
                <span className="text-sm text-slate-500 font-medium">Speed:</span>
                {[0.75, 1.0, 1.25, 1.5, 1.75, 2.0].map((rate) => (
                  <button
                    key={rate}
                    onClick={() => handlePlaybackRateChange(rate)}
                    className={`px-3 py-1 rounded-md text-sm font-medium transition-all ${
                      playbackRate === rate
                        ? 'bg-blue-500 text-white shadow-sm'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {rate === 1.0 ? '1×' : `${rate}×`}
                  </button>
                ))}
              </div>
            </>
          )}
        </div>
      )}

      <audio ref={audioRef} preload="metadata" />
      
      <style jsx>{`
        .progress-slider::-webkit-slider-thumb {
          appearance: none;
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: linear-gradient(135deg, #3b82f6, #6366f1);
          cursor: pointer;
          box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
          transition: all 0.15s ease-in-out;
          position: relative;
          z-index: 10;
        }
        
        .progress-slider::-webkit-slider-thumb:hover {
          box-shadow: 0 4px 12px rgba(59, 130, 246, 0.6);
          transform: scale(1.1);
        }
        
        .volume-slider::-webkit-slider-thumb {
          appearance: none;
          height: 16px;
          width: 16px;
          border-radius: 50%;
          background: #64748b;
          cursor: pointer;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.2);
          transition: all 0.15s ease-in-out;
        }
        
        .volume-slider::-webkit-slider-thumb:hover {
          background: #475569;
          transform: scale(1.1);
        }
        
        .progress-slider::-moz-range-thumb,
        .volume-slider::-moz-range-thumb {
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: none;
          box-shadow: 0 2px 8px rgba(59, 130, 246, 0.4);
        }
      `}</style>
    </div>
  );
}