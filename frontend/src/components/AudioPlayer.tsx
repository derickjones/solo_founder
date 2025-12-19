'use client';

import { useState, useRef, useEffect } from 'react';
import { PlayIcon, PauseIcon, SpeakerWaveIcon, UserIcon } from '@heroicons/react/24/outline';

interface AudioPlayerProps {
  audioFiles: {
    combined?: string;
    host_only?: string;
    guest_only?: string;
  };
  title: string;
}

interface AudioTrack {
  id: string;
  label: string;
  icon: React.ComponentType<any>;
  base64Data: string;
}

export default function AudioPlayer({ audioFiles, title }: AudioPlayerProps) {
  const [currentTrack, setCurrentTrack] = useState<string | null>(null);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [volume, setVolume] = useState(1);
  const audioRef = useRef<HTMLAudioElement>(null);

  // Prepare tracks from available audio files
  const tracks: AudioTrack[] = [];
  
  if (audioFiles.combined) {
    tracks.push({
      id: 'combined',
      label: 'Full Conversation',
      icon: SpeakerWaveIcon,
      base64Data: audioFiles.combined
    });
  }
  
  if (audioFiles.host_only) {
    tracks.push({
      id: 'host_only',
      label: 'Host Only',
      icon: UserIcon,
      base64Data: audioFiles.host_only
    });
  }
  
  if (audioFiles.guest_only) {
    tracks.push({
      id: 'guest_only', 
      label: 'Guest Only',
      icon: UserIcon,
      base64Data: audioFiles.guest_only
    });
  }

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

  // Load and play selected track
  const playTrack = (trackId: string) => {
    const track = tracks.find(t => t.id === trackId);
    if (!track || !audioRef.current) return;

    const audioUrl = getAudioUrl(track.base64Data);
    audioRef.current.src = audioUrl;
    setCurrentTrack(trackId);
    
    audioRef.current.play();
    setIsPlaying(true);
  };

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
  }, [currentTrack]);

  // Seek to position
  const seek = (e: React.ChangeEvent<HTMLInputElement>) => {
    const audio = audioRef.current;
    if (!audio) return;
    
    const seekTime = (parseFloat(e.target.value) / 100) * duration;
    audio.currentTime = seekTime;
    setCurrentTime(seekTime);
  };

  // Format time display
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = Math.floor(seconds % 60);
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (tracks.length === 0) {
    return (
      <div className="bg-gray-50 border border-gray-200 rounded-lg p-4">
        <p className="text-gray-500 text-center">Audio files are being generated...</p>
      </div>
    );
  }

  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 space-y-4">
      <h3 className="text-lg font-semibold text-gray-900 mb-4">🎧 Audio Summary - {title}</h3>
      
      {/* Track Selection */}
      <div className="space-y-2">
        <h4 className="text-sm font-medium text-gray-700">Select Audio Track:</h4>
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
          {tracks.map((track) => {
            const IconComponent = track.icon;
            const isActive = currentTrack === track.id;
            
            return (
              <button
                key={track.id}
                onClick={() => playTrack(track.id)}
                className={`flex items-center space-x-2 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActive 
                    ? 'bg-blue-100 text-blue-700 border border-blue-300' 
                    : 'bg-gray-50 text-gray-600 border border-gray-200 hover:bg-gray-100'
                }`}
              >
                <IconComponent className="h-4 w-4" />
                <span>{track.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Audio Controls */}
      {currentTrack && (
        <div className="space-y-3">
          <div className="flex items-center space-x-3">
            <button
              onClick={togglePlayPause}
              className="flex items-center justify-center w-10 h-10 bg-blue-500 hover:bg-blue-600 text-white rounded-full transition-colors"
            >
              {isPlaying ? (
                <PauseIcon className="h-5 w-5" />
              ) : (
                <PlayIcon className="h-5 w-5 ml-0.5" />
              )}
            </button>
            
            <div className="flex-1 space-y-1">
              <input
                type="range"
                min="0"
                max="100"
                value={duration ? (currentTime / duration) * 100 : 0}
                onChange={seek}
                className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer slider"
              />
              <div className="flex justify-between text-xs text-gray-500">
                <span>{formatTime(currentTime)}</span>
                <span>{formatTime(duration)}</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <SpeakerWaveIcon className="h-4 w-4 text-gray-400" />
              <input
                type="range"
                min="0"
                max="1"
                step="0.1"
                value={volume}
                onChange={(e) => {
                  const newVolume = parseFloat(e.target.value);
                  setVolume(newVolume);
                  if (audioRef.current) {
                    audioRef.current.volume = newVolume;
                  }
                }}
                className="w-16 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
              />
            </div>
          </div>
          
          <p className="text-sm text-gray-600">
            Now playing: {tracks.find(t => t.id === currentTrack)?.label}
          </p>
        </div>
      )}

      <audio ref={audioRef} preload="metadata" />
      
      <style jsx>{`
        .slider::-webkit-slider-thumb {
          appearance: none;
          height: 16px;
          width: 16px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          box-shadow: 0 0 2px 0 #555;
          transition: background 0.15s ease-in-out;
        }
        
        .slider::-webkit-slider-thumb:hover {
          background: #2563eb;
        }
        
        .slider::-moz-range-thumb {
          height: 16px;
          width: 16px;
          border-radius: 50%;
          background: #3b82f6;
          cursor: pointer;
          border: none;
          box-shadow: 0 0 2px 0 #555;
        }
      `}</style>
    </div>
  );
}