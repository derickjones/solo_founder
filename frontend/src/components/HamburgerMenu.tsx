'use client';

import { useState, useRef, useEffect } from 'react';
import { Bars3Icon, XMarkIcon } from '@heroicons/react/24/outline';
import { useUser, SignInButton, SignUpButton, UserButton } from '@clerk/nextjs';
import Link from 'next/link';
import { useUsageLimit } from '@/hooks/useUsageLimit';
import VideoLogo from './VideoLogo';

// Voice type and options
type VoiceOption = 'alnilam' | 'achird' | 'enceladus' | 'aoede' | 'autonoe' | 'erinome';

const VOICE_OPTIONS = {
  male: [
    { id: 'alnilam', name: 'David', desc: 'Male' },
    { id: 'achird', name: 'Michael', desc: 'Male' },
    { id: 'enceladus', name: 'James', desc: 'Male' },
  ],
  female: [
    { id: 'aoede', name: 'Sarah', desc: 'Female' },
    { id: 'autonoe', name: 'Emma', desc: 'Female' },
    { id: 'erinome', name: 'Rachel', desc: 'Female' },
  ]
};

interface HamburgerMenuProps {
  mode: string;
  setMode: (mode: string) => void;
  selectedVoice: VoiceOption;
  setSelectedVoice: (voice: VoiceOption) => void;
  onOpenSidebar?: () => void;
}

export default function HamburgerMenu({
  mode,
  setMode,
  selectedVoice,
  setSelectedVoice,
  onOpenSidebar,
}: HamburgerMenuProps) {
  const [isOpen, setIsOpen] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);
  const { isSignedIn, user } = useUser();
  const { actionsUsed, dailyLimit, isPremium } = useUsageLimit();

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('mousedown', handleClickOutside);
    }
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, [isOpen]);

  // Close on escape key
  useEffect(() => {
    const handleEscape = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener('keydown', handleEscape);
    }
    return () => {
      document.removeEventListener('keydown', handleEscape);
    };
  }, [isOpen]);

  return (
    <div className="relative" ref={menuRef}>
      {/* Hamburger button */}
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 rounded-lg bg-neutral-800/80 hover:bg-neutral-700 text-neutral-300 hover:text-white transition-all backdrop-blur-sm border border-neutral-700/50"
        aria-label="Open menu"
      >
        {isOpen ? (
          <XMarkIcon className="w-6 h-6" />
        ) : (
          <Bars3Icon className="w-6 h-6" />
        )}
      </button>

      {/* Dropdown menu */}
      {isOpen && (
        <>
          {/* Backdrop for mobile */}
          <div 
            className="fixed inset-0 bg-black/50 z-40 lg:hidden"
            onClick={() => setIsOpen(false)}
          />
          
          {/* Menu panel */}
          <div className="absolute right-0 top-12 w-72 bg-neutral-900 border border-neutral-700 rounded-xl shadow-2xl z-50 overflow-hidden">
            {/* Header */}
            <div className="p-4 border-b border-neutral-800 flex items-center gap-3">
              <VideoLogo size="small" className="ring-0 bg-transparent" />
              <span className="font-semibold text-white">Gospel Study</span>
            </div>

            {/* Study Mode */}
            <div className="p-4 border-b border-neutral-800">
              <label className="block text-xs font-medium text-neutral-400 uppercase tracking-wider mb-3">
                Study Mode
              </label>
              <div className="flex bg-neutral-800 rounded-lg p-1">
                <button
                  onClick={() => {
                    setMode('Q&A');
                    if (onOpenSidebar) {
                      onOpenSidebar();
                      setIsOpen(false);
                    }
                  }}
                  className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-all ${
                    mode === 'Q&A'
                      ? 'bg-neutral-700 text-white'
                      : 'text-neutral-400 hover:text-white'
                  }`}
                >
                  Q&A
                </button>
                <button
                  onClick={() => setMode('Come Follow Me')}
                  className={`flex-1 py-2 px-3 rounded-md text-sm font-medium transition-all ${
                    mode === 'Come Follow Me'
                      ? 'bg-neutral-700 text-white'
                      : 'text-neutral-400 hover:text-white'
                  }`}
                >
                  Come Follow Me
                </button>
              </div>
            </div>

            {/* Podcast Voice */}
            <div className="p-4 border-b border-neutral-800">
              <label className="block text-xs font-medium text-neutral-400 uppercase tracking-wider mb-3">
                Podcast Voice
              </label>
              <select
                value={selectedVoice}
                onChange={(e) => setSelectedVoice(e.target.value as VoiceOption)}
                className="w-full bg-neutral-800 border border-neutral-700 rounded-lg px-3 py-2 text-white text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <optgroup label="Male Voices">
                  {VOICE_OPTIONS.male.map((voice) => (
                    <option key={voice.id} value={voice.id}>
                      {voice.name}
                    </option>
                  ))}
                </optgroup>
                <optgroup label="Female Voices">
                  {VOICE_OPTIONS.female.map((voice) => (
                    <option key={voice.id} value={voice.id}>
                      {voice.name}
                    </option>
                  ))}
                </optgroup>
              </select>
            </div>

            {/* User section */}
            <div className="p-4">
              {isSignedIn ? (
                <div className="flex items-center gap-3">
                  <UserButton 
                    afterSignOutUrl="/"
                    appearance={{
                      elements: {
                        avatarBox: "w-10 h-10"
                      }
                    }}
                  />
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium text-white truncate">
                      {user?.firstName || user?.username || 'User'}
                    </p>
                    <p className="text-xs text-neutral-500">
                      {isPremium ? (
                        <span className="text-amber-400">Premium • Unlimited</span>
                      ) : (
                        <span>{actionsUsed}/{dailyLimit} actions today</span>
                      )}
                    </p>
                  </div>
                </div>
              ) : (
                <div className="space-y-3">
                  {/* Usage indicator for anonymous users */}
                  <div className="text-center pb-2 border-b border-neutral-700">
                    <p className="text-sm text-neutral-300">
                      <span className="font-medium">{actionsUsed}/{dailyLimit}</span> free actions left
                    </p>
                    <p className="text-xs text-neutral-500 mt-1">Sign in to save progress</p>
                  </div>
                  <SignInButton mode="modal">
                    <button className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-500 text-white rounded-lg text-sm font-medium transition-colors">
                      Sign In
                    </button>
                  </SignInButton>
                  <SignUpButton mode="modal">
                    <button className="w-full py-2 px-4 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 rounded-lg text-sm font-medium transition-colors border border-neutral-700">
                      Create Account
                    </button>
                  </SignUpButton>
                </div>
              )}
            </div>

            {/* Upgrade button - only when signed in and not premium */}
            {isSignedIn && !isPremium && (
              <div className="p-4 pt-0">
                <Link href="/pricing">
                  <button className="w-full py-2.5 px-4 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-white rounded-lg text-sm font-medium transition-all flex items-center justify-center gap-2">
                    <span>⚡</span>
                    Upgrade to Premium
                  </button>
                </Link>
              </div>
            )}

            {/* Submit Feedback */}
            <div className="p-4 pt-0 border-t border-neutral-800">
              <Link href="/feedback" onClick={() => setIsOpen(false)}>
                <button className="w-full py-2 px-4 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 hover:text-white rounded-lg text-sm font-medium transition-colors">
                  Submit Feedback
                </button>
              </Link>
            </div>
          </div>
        </>
      )}
    </div>
  );
}
