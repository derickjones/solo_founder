'use client';

import { useEffect, useState } from 'react';
import { useUser, useSession } from '@clerk/nextjs';
import Link from 'next/link';
import { ArrowLeftIcon, ArrowPathIcon } from '@heroicons/react/24/outline';

// Backend API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://gospel-app-backend-273320302933.us-central1.run.app';

interface UserDetail {
  id: string;
  email: string;
  isPremium: boolean;
  lifetimeActions: number;
  lastActivity: string | null;
  activityBreakdown: Record<string, number>;
}

interface Analytics {
  totalUsers: number;
  activeToday: number;
  premiumUsers: number;
  freeUsers: number;
  activityBreakdown: Record<string, number>;
  topActivities: Array<{ activity: string; count: number }>;
  conversionRate: number;
  userDetails: UserDetail[];
}

const ACTIVITY_LABELS: Record<string, string> = {
  qa_question: '❓ Q&A Questions',
  study_guide: '📖 Study Guides',
  audio_summary: '🎧 Audio Summaries',
  lesson_plan: '📝 Lesson Plans',
  tile_click: '🖱️ Tile Clicks',
  daily_thought: '💭 Daily Thoughts',
  core_content: '📚 Core Content',
  podcast_play: '🎙️ Podcasts',
  deep_dive: '🔍 Deep Dives',
  visual_guide: '🖼️ Visual Guides',
  totalActions: '📊 Total Actions',
};

function formatDate(dateString: string | null): string {
  if (!dateString) return 'Never';
  const date = new Date(dateString);
  const now = new Date();
  const diffMs = now.getTime() - date.getTime();
  const diffMins = Math.floor(diffMs / 60000);
  const diffHours = Math.floor(diffMs / 3600000);
  const diffDays = Math.floor(diffMs / 86400000);

  if (diffMins < 1) return 'Just now';
  if (diffMins < 60) return `${diffMins}m ago`;
  if (diffHours < 24) return `${diffHours}h ago`;
  if (diffDays < 7) return `${diffDays}d ago`;
  return date.toLocaleDateString();
}

export default function AdminDashboard() {
  const { isSignedIn, isLoaded } = useUser();
  const { session } = useSession();
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchAnalytics = async () => {
    setLoading(true);
    setError(null);
    try {
      // Get auth token for backend API
      const token = await session?.getToken();
      const headers: Record<string, string> = {};
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      const response = await fetch(`${API_BASE_URL}/api/analytics`, { headers });
      if (!response.ok) {
        if (response.status === 401) {
          setError('Unauthorized. Please sign in with an admin account.');
        } else if (response.status === 403) {
          setError('Access denied. Admin privileges required.');
        } else {
          setError('Failed to fetch analytics');
        }
        return;
      }
      const data = await response.json();
      setAnalytics(data);
    } catch (err) {
      setError('Failed to fetch analytics');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (isLoaded && isSignedIn) {
      fetchAnalytics();
    } else if (isLoaded && !isSignedIn) {
      setLoading(false);
      setError('Please sign in to view analytics');
    }
  }, [isLoaded, isSignedIn]);

  if (!isLoaded || loading) {
    return (
      <div className="min-h-screen bg-neutral-900 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-amber-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-neutral-900 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-400 text-lg mb-4">{error}</p>
          <Link href="/" className="text-amber-500 hover:text-amber-400">
            ← Back to Home
          </Link>
        </div>
      </div>
    );
  }

  if (!analytics) return null;

  return (
    <div className="min-h-screen bg-neutral-900 text-white p-6">
      {/* Header */}
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div className="flex items-center gap-4">
            <Link href="/" className="text-neutral-400 hover:text-white">
              <ArrowLeftIcon className="w-6 h-6" />
            </Link>
            <h1 className="text-3xl font-bold">Analytics Dashboard</h1>
          </div>
          <button
            onClick={fetchAnalytics}
            className="flex items-center gap-2 px-4 py-2 bg-neutral-800 hover:bg-neutral-700 rounded-lg transition-colors"
          >
            <ArrowPathIcon className="w-5 h-5" />
            Refresh
          </button>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-neutral-800 rounded-xl p-6">
            <p className="text-neutral-400 text-sm">Total Users</p>
            <p className="text-4xl font-bold text-white">{analytics.totalUsers}</p>
          </div>
          <div className="bg-neutral-800 rounded-xl p-6">
            <p className="text-neutral-400 text-sm">Active Today</p>
            <p className="text-4xl font-bold text-green-400">{analytics.activeToday}</p>
          </div>
          <div className="bg-neutral-800 rounded-xl p-6">
            <p className="text-neutral-400 text-sm">Premium Users</p>
            <p className="text-4xl font-bold text-amber-500">{analytics.premiumUsers}</p>
          </div>
          <div className="bg-neutral-800 rounded-xl p-6">
            <p className="text-neutral-400 text-sm">Conversion Rate</p>
            <p className="text-4xl font-bold text-blue-400">{analytics.conversionRate}%</p>
          </div>
        </div>

        {/* Two Column Layout */}
        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Activity Breakdown */}
          <div className="bg-neutral-800 rounded-xl p-6">
            <h2 className="text-xl font-semibold mb-4">📊 Activity Breakdown</h2>
            {analytics.topActivities.length === 0 ? (
              <p className="text-neutral-400">No activity data yet</p>
            ) : (
              <div className="space-y-3">
                {analytics.topActivities.map(({ activity, count }) => {
                  const maxCount = analytics.topActivities[0]?.count || 1;
                  const percentage = Math.round((count / maxCount) * 100);
                  return (
                    <div key={activity}>
                      <div className="flex justify-between text-sm mb-1">
                        <span>{ACTIVITY_LABELS[activity] || activity}</span>
                        <span className="text-neutral-400">{count}</span>
                      </div>
                      <div className="h-2 bg-neutral-700 rounded-full overflow-hidden">
                        <div
                          className="h-full bg-gradient-to-r from-amber-500 to-amber-600 rounded-full transition-all"
                          style={{ width: `${percentage}%` }}
                        />
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>

          {/* User Type Distribution */}
          <div className="bg-neutral-800 rounded-xl p-6">
            <h2 className="text-xl font-semibold mb-4">👥 User Distribution</h2>
            <div className="flex items-center justify-center h-48">
              <div className="relative w-40 h-40">
                {/* Simple pie chart visualization */}
                <svg viewBox="0 0 36 36" className="w-full h-full">
                  <circle
                    cx="18"
                    cy="18"
                    r="15.9"
                    fill="transparent"
                    stroke="#525252"
                    strokeWidth="3"
                  />
                  <circle
                    cx="18"
                    cy="18"
                    r="15.9"
                    fill="transparent"
                    stroke="#f59e0b"
                    strokeWidth="3"
                    strokeDasharray={`${analytics.conversionRate} ${100 - analytics.conversionRate}`}
                    strokeDashoffset="25"
                    className="transition-all duration-500"
                  />
                </svg>
                <div className="absolute inset-0 flex flex-col items-center justify-center">
                  <span className="text-2xl font-bold">{analytics.premiumUsers}</span>
                  <span className="text-xs text-neutral-400">Premium</span>
                </div>
              </div>
            </div>
            <div className="flex justify-center gap-6 mt-4">
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-amber-500 rounded-full"></div>
                <span className="text-sm">Premium ({analytics.premiumUsers})</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-3 h-3 bg-neutral-600 rounded-full"></div>
                <span className="text-sm">Free ({analytics.freeUsers})</span>
              </div>
            </div>
          </div>
        </div>

        {/* User Table */}
        <div className="bg-neutral-800 rounded-xl p-6">
          <h2 className="text-xl font-semibold mb-4">👤 User Details</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="text-left text-neutral-400 border-b border-neutral-700">
                  <th className="pb-3 pr-4">Email</th>
                  <th className="pb-3 pr-4">Status</th>
                  <th className="pb-3 pr-4">Lifetime Actions</th>
                  <th className="pb-3 pr-4">Last Active</th>
                  <th className="pb-3">Top Activities</th>
                </tr>
              </thead>
              <tbody>
                {analytics.userDetails.slice(0, 20).map((user) => {
                  // Get top 3 activities for this user
                  const topActivities = Object.entries(user.activityBreakdown)
                    .filter(([key]) => key !== 'totalActions')
                    .sort((a, b) => (b[1] as number) - (a[1] as number))
                    .slice(0, 3);

                  return (
                    <tr key={user.id} className="border-b border-neutral-700/50 hover:bg-neutral-700/30">
                      <td className="py-3 pr-4 font-mono text-xs">{user.email}</td>
                      <td className="py-3 pr-4">
                        {user.isPremium ? (
                          <span className="px-2 py-1 bg-amber-500/20 text-amber-500 rounded text-xs font-medium">
                            Premium
                          </span>
                        ) : (
                          <span className="px-2 py-1 bg-neutral-600/50 text-neutral-400 rounded text-xs font-medium">
                            Free
                          </span>
                        )}
                      </td>
                      <td className="py-3 pr-4 font-mono">{user.lifetimeActions}</td>
                      <td className="py-3 pr-4 text-neutral-400">{formatDate(user.lastActivity)}</td>
                      <td className="py-3">
                        <div className="flex gap-1 flex-wrap">
                          {topActivities.map(([activity, count]) => (
                            <span
                              key={activity}
                              className="px-2 py-0.5 bg-neutral-700 rounded text-xs"
                              title={ACTIVITY_LABELS[activity] || activity}
                            >
                              {activity.split('_')[0]}: {count}
                            </span>
                          ))}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {analytics.userDetails.length > 20 && (
              <p className="text-neutral-400 text-sm mt-4 text-center">
                Showing top 20 of {analytics.userDetails.length} users
              </p>
            )}
          </div>
        </div>

        {/* Footer */}
        <div className="mt-8 text-center text-neutral-500 text-sm">
          Last updated: {new Date().toLocaleString()}
        </div>
      </div>
    </div>
  );
}
