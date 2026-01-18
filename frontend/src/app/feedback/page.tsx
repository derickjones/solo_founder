'use client';

import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import Link from 'next/link';
import { ArrowLeftIcon, CheckCircleIcon } from '@heroicons/react/24/outline';

type FeedbackType = 'bug' | 'feature' | 'general' | 'praise';

// Backend API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://gospel-app-backend-273320302933.us-central1.run.app';

const FEEDBACK_TYPES: { id: FeedbackType; label: string; emoji: string }[] = [
  { id: 'bug', label: 'Bug Report', emoji: '🐛' },
  { id: 'feature', label: 'Feature Request', emoji: '💡' },
  { id: 'general', label: 'General Feedback', emoji: '💬' },
  { id: 'praise', label: 'Something I Love', emoji: '❤️' },
];

export default function FeedbackPage() {
  const { user, isSignedIn } = useUser();
  const [feedbackType, setFeedbackType] = useState<FeedbackType>('general');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!message.trim()) {
      setError('Please enter your feedback');
      return;
    }

    setIsSubmitting(true);
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/feedback`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: feedbackType,
          message: message.trim(),
          email: isSignedIn ? user?.emailAddresses[0]?.emailAddress : email,
          userId: user?.id || null,
          userName: user?.firstName || user?.username || null,
        }),
      });

      if (!response.ok) {
        throw new Error('Failed to submit feedback');
      }

      setIsSubmitted(true);
    } catch (err) {
      console.error('Error submitting feedback:', err);
      setError('Failed to submit feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  if (isSubmitted) {
    return (
      <div className="min-h-screen bg-neutral-900 flex items-center justify-center p-6">
        <div className="max-w-md w-full text-center">
          <div className="mb-6">
            <CheckCircleIcon className="w-16 h-16 text-green-500 mx-auto" />
          </div>
          <h1 className="text-2xl font-bold text-white mb-3">Thank You!</h1>
          <p className="text-neutral-400 mb-8">
            Your feedback has been submitted. We appreciate you taking the time to help us improve.
          </p>
          <Link href="/">
            <button className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-lg font-medium transition-colors">
              Back to App
            </button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-neutral-900 text-white">
      <div className="max-w-2xl mx-auto p-6">
        {/* Header */}
        <div className="flex items-center gap-4 mb-8">
          <Link href="/" className="text-neutral-400 hover:text-white transition-colors">
            <ArrowLeftIcon className="w-6 h-6" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold">Submit Feedback</h1>
            <p className="text-neutral-400 text-sm">Help us improve Gospel Study App</p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Feedback Type */}
          <div>
            <label className="block text-sm font-medium text-neutral-300 mb-3">
              What type of feedback?
            </label>
            <div className="grid grid-cols-2 gap-3">
              {FEEDBACK_TYPES.map((type) => (
                <button
                  key={type.id}
                  type="button"
                  onClick={() => setFeedbackType(type.id)}
                  className={`p-4 rounded-xl border-2 transition-all text-left ${
                    feedbackType === type.id
                      ? 'border-blue-500 bg-blue-500/10'
                      : 'border-neutral-700 bg-neutral-800 hover:border-neutral-600'
                  }`}
                >
                  <span className="text-2xl">{type.emoji}</span>
                  <p className="text-sm font-medium mt-2">{type.label}</p>
                </button>
              ))}
            </div>
          </div>

          {/* Message */}
          <div>
            <label htmlFor="message" className="block text-sm font-medium text-neutral-300 mb-2">
              Your Feedback
            </label>
            <textarea
              id="message"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder={
                feedbackType === 'bug'
                  ? "Please describe the bug and steps to reproduce it..."
                  : feedbackType === 'feature'
                  ? "What feature would you like to see?"
                  : feedbackType === 'praise'
                  ? "What do you love about the app?"
                  : "Share your thoughts with us..."
              }
              rows={6}
              className="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-3 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
            />
          </div>

          {/* Email (only for anonymous users) */}
          {!isSignedIn && (
            <div>
              <label htmlFor="email" className="block text-sm font-medium text-neutral-300 mb-2">
                Email <span className="text-neutral-500">(optional, for follow-up)</span>
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="your@email.com"
                className="w-full bg-neutral-800 border border-neutral-700 rounded-xl px-4 py-3 text-white placeholder-neutral-500 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          )}

          {/* Error message */}
          {error && (
            <div className="p-4 bg-red-500/10 border border-red-500/50 rounded-xl">
              <p className="text-red-400 text-sm">{error}</p>
            </div>
          )}

          {/* Submit button */}
          <button
            type="submit"
            disabled={isSubmitting || !message.trim()}
            className="w-full py-3 px-6 bg-blue-600 hover:bg-blue-500 disabled:bg-neutral-700 disabled:cursor-not-allowed text-white rounded-xl font-medium transition-colors flex items-center justify-center gap-2"
          >
            {isSubmitting ? (
              <>
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                Submitting...
              </>
            ) : (
              <>
                <span>📨</span>
                Submit Feedback
              </>
            )}
          </button>
        </form>

        {/* Privacy note */}
        <p className="text-neutral-500 text-xs text-center mt-6">
          Your feedback helps us build a better experience. We read every submission.
        </p>
      </div>
    </div>
  );
}
