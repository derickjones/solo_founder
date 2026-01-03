'use client';

import { useState, useRef, useEffect } from 'react';
import { PlayIcon, PauseIcon, SpeakerWaveIcon } from '@heroicons/react/24/solid';
import { ChevronDownIcon, ChevronUpIcon } from '@heroicons/react/24/outline';

interface AudioPlayerProps {
  audioFiles: {
    combined?: string;
  };
  title: string;
  autoPlay?: boolean;
  onPlayStart?: () => void;
}

export default function AudioPlayer({ audioFiles, title, autoPlay = false, onPlayStart }: AudioPlayerProps) {
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

  // Auto-play when cache exists (fast load)
  useEffect(() => {
    console.log('Auto-play effect:', { autoPlay, isLoaded, isPlaying, hasAudioRef: !!audioRef.current });
    
    if (autoPlay && isLoaded && audioRef.current) {
      // Small delay to ensure audio is fully ready
      const timer = setTimeout(() => {
        if (audioRef.current && !isPlaying) {
          console.log('Attempting auto-play...');
          audioRef.current.play()
            .then(() => {
              console.log('Auto-play successful!');
              setIsPlaying(true);
              onPlayStart?.();
            })
            .catch((error) => {
              console.error('Auto-play failed:', error);
              // Likely browser auto-play policy - user needs to interact first
            });
        }
      }, 200);
      
      return () => clearTimeout(timer);
    }
  }, [autoPlay, isLoaded, isPlaying, onPlayStart]);

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
    <div className="bg-neutral-800 border border-neutral-700 rounded-xl shadow-lg overflow-hidden">
      {/* Header */}
      <div className="bg-neutral-900/50 border-b border-neutral-700 px-6 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-full flex items-center justify-center shadow-lg">
              <span className="text-white text-lg">🎧</span>
            </div>
            <div>
              <h3 className="font-semibold text-white">Gospel Summary</h3>
              <p className="text-sm text-neutral-400">{title}</p>
            </div>
          </div>
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 hover:bg-neutral-700/50 rounded-lg transition-colors"
          >
            {isExpanded ? (
              <ChevronUpIcon className="w-5 h-5 text-neutral-400 hover:text-neutral-200" />
            ) : (
              <ChevronDownIcon className="w-5 h-5 text-neutral-400 hover:text-neutral-200" />
            )}
          </button>
        </div>
      </div>

      {/* Player Controls */}
      {isExpanded && (
        <div className="p-6 space-y-4">
          {!audioData ? (
            /* No Audio Available State */
            <div className="flex items-center space-x-3">
              <div className="w-14 h-14 bg-neutral-700 rounded-full flex items-center justify-center">
                <span className="text-neutral-400 text-xl">🎧</span>
              </div>
              <div className="flex-1">
                <p className="text-neutral-200 font-medium">Audio not available</p>
                <p className="text-sm text-neutral-400">The audio summary could not be generated at this time</p>
              </div>
            </div>
          ) : (
            <>
              {/* Main Controls */}
              <div className="flex items-center space-x-4">
                <button
                  onClick={togglePlayPause}
                  className="flex items-center justify-center w-14 h-14 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white rounded-full transition-all duration-200 transform hover:scale-105 shadow-lg"
                >
                  {isPlaying ? (
                    <PauseIcon className="w-7 h-7" />
                  ) : (
                    <PlayIcon className="w-7 h-7 ml-0.5" />
                  )}
                </button>
                
                <div className="flex-1 space-y-2">
                  {/* Single Progress Bar with Dot Scrubber */}
                  <div className="relative">
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={duration ? (currentTime / duration) * 100 : 0}
                      onChange={seek}
                      className="w-full h-2 bg-neutral-600 rounded-full appearance-none cursor-pointer progress-slider"
                    />
                  </div>
                  
                  {/* Time Display */}
                  <div className="flex justify-between text-sm text-neutral-400 font-medium">
                    <span>{formatTime(currentTime)}</span>
                    <span>{formatTime(duration)}</span>
                  </div>
                </div>
                
                {/* Volume Control */}
                <div className="flex items-center space-x-3">
                  <SpeakerWaveIcon className="w-5 h-5 text-neutral-400" />
                  <div className="relative w-20">
                    <input
                      type="range"
                      min="0"
                      max="1"
                      step="0.05"
                      value={volume}
                      onChange={handleVolumeChange}
                      className="w-full h-2 bg-neutral-600 rounded-full appearance-none cursor-pointer volume-slider"
                    />
                  </div>
                </div>
              </div>
              
              {/* Playback Speed Controls */}
              <div className="flex items-center justify-center space-x-2">
                <span className="text-sm text-neutral-400 font-medium">Speed:</span>
                {[0.75, 1.0, 1.25, 1.5, 1.75, 2.0].map((rate) => (
                  <button
                    key={rate}
                    onClick={() => handlePlaybackRateChange(rate)}
                    className={`px-3 py-1 rounded-md text-sm font-medium transition-all ${
                      playbackRate === rate
                        ? 'bg-blue-600 text-white shadow-sm'
                        : 'bg-neutral-700 text-neutral-300 hover:bg-neutral-600'
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
          background: linear-gradient(135deg, #2563eb, #4f46e5);
          cursor: pointer;
          box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4), 0 0 0 2px #1f2937;
          transition: all 0.15s ease-in-out;
          position: relative;
          z-index: 10;
        }
        
        .progress-slider::-webkit-slider-thumb:hover {
          box-shadow: 0 4px 12px rgba(37, 99, 235, 0.6), 0 0 0 2px #1f2937;
          transform: scale(1.1);
        }
        
        .volume-slider::-webkit-slider-thumb {
          appearance: none;
          height: 16px;
          width: 16px;
          border-radius: 50%;
          background: #6b7280;
          cursor: pointer;
          box-shadow: 0 1px 4px rgba(0, 0, 0, 0.3), 0 0 0 1px #374151;
          transition: all 0.15s ease-in-out;
        }
        
        .volume-slider::-webkit-slider-thumb:hover {
          background: #9ca3af;
          transform: scale(1.1);
        }
        
        .progress-slider::-moz-range-thumb,
        .volume-slider::-moz-range-thumb {
          height: 20px;
          width: 20px;
          border-radius: 50%;
          background: #2563eb;
          cursor: pointer;
          border: 2px solid #1f2937;
          box-shadow: 0 2px 8px rgba(37, 99, 235, 0.4);
        }
        
        /* Hide the default track styling */
        .progress-slider::-webkit-slider-track,
        .volume-slider::-webkit-slider-track {
          background: transparent;
        }
      `}</style>
    </div>
  );
}