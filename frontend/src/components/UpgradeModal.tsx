'use client';

import { XMarkIcon } from '@heroicons/react/24/outline';
import Link from 'next/link';
import { useUser } from '@clerk/nextjs';

interface UpgradeModalProps {
  isOpen: boolean;
  onClose: () => void;
  actionsUsed: number;
  dailyLimit: number;
}

export default function UpgradeModal({ isOpen, onClose, actionsUsed, dailyLimit }: UpgradeModalProps) {
  const { isSignedIn } = useUser();

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-black/70 backdrop-blur-sm"
        onClick={onClose}
      />
      
      {/* Modal */}
      <div className="relative bg-neutral-900 border border-neutral-700 rounded-2xl max-w-md w-full p-6 shadow-2xl">
        {/* Close button */}
        <button
          onClick={onClose}
          className="absolute top-4 right-4 text-neutral-400 hover:text-white transition-colors"
        >
          <XMarkIcon className="w-6 h-6" />
        </button>

        {/* Content */}
        <div className="text-center">
          {/* Icon */}
          <div className="w-16 h-16 mx-auto mb-4 bg-gradient-to-br from-amber-500 to-orange-500 rounded-full flex items-center justify-center">
            <span className="text-3xl">⚡</span>
          </div>

          {/* Title */}
          <h2 className="text-2xl font-bold text-white mb-2">
            You've reached your daily limit
          </h2>

          {/* Usage indicator */}
          <p className="text-neutral-400 mb-6">
            You've used <span className="text-white font-semibold">{actionsUsed}/{dailyLimit}</span> free actions today
          </p>

          {/* Benefits */}
          <div className="bg-neutral-800/50 rounded-xl p-4 mb-6 text-left">
            <p className="text-sm text-neutral-300 mb-3">Upgrade to Premium for:</p>
            <ul className="space-y-2">
              <li className="flex items-center gap-2 text-sm text-neutral-300">
                <span className="text-green-400">✓</span>
                Unlimited daily actions
              </li>
              <li className="flex items-center gap-2 text-sm text-neutral-300">
                <span className="text-green-400">✓</span>
                All study guides & content
              </li>
              <li className="flex items-center gap-2 text-sm text-neutral-300">
                <span className="text-green-400">✓</span>
                Unlimited audio generation
              </li>
              <li className="flex items-center gap-2 text-sm text-neutral-300">
                <span className="text-green-400">✓</span>
                PDF lesson plan exports
              </li>
            </ul>
          </div>

          {/* Price */}
          <p className="text-neutral-400 text-sm mb-4">
            Only <span className="text-white font-bold text-lg">$1.99</span>/month
          </p>

          {/* CTA buttons */}
          <div className="space-y-3">
            <Link href="/pricing" className="block">
              <button className="w-full py-3 px-6 bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-white rounded-xl font-semibold transition-all transform hover:scale-[1.02]">
                Upgrade to Premium
              </button>
            </Link>
            
            <button
              onClick={onClose}
              className="w-full py-3 px-6 bg-neutral-800 hover:bg-neutral-700 text-neutral-300 rounded-xl font-medium transition-colors"
            >
              Maybe later
            </button>
          </div>

          {/* Reset notice */}
          <p className="text-neutral-500 text-xs mt-4">
            Free actions reset at midnight
          </p>
        </div>
      </div>
    </div>
  );
}
