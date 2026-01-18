'use client';

import { useUser, useSession } from '@clerk/nextjs';
import { useState, useEffect, useCallback, useRef } from 'react';

const DAILY_LIMIT = 10;
const STORAGE_KEY = 'gospel_study_usage';

// Backend API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || '';

// Activity types for analytics
export type ActivityType = 
  | 'qa_question'      // Asked a Q&A question
  | 'study_guide'      // Generated a study guide
  | 'audio_summary'    // Played audio summary
  | 'tile_click'       // Clicked a landing page tile
  | 'podcast_play'     // Played a podcast
  | 'lesson_plan'      // Viewed lesson plan
  | 'core_content'     // Viewed core content
  | 'daily_thought';   // Viewed daily thought

interface ActivityLog {
  type: ActivityType;
  timestamp: string;
  metadata?: Record<string, string>; // Optional context (e.g., topic, source)
}

interface UsageData {
  count: number;
  date: string; // YYYY-MM-DD format
  activities?: ActivityLog[]; // Track what actions were taken
}

interface UseUsageLimitReturn {
  actionsUsed: number;
  actionsRemaining: number;
  dailyLimit: number;
  canPerformAction: boolean;
  isPremium: boolean;
  isLoading: boolean;
  isSignedIn: boolean;
  recordAction: (activityType: ActivityType, metadata?: Record<string, string>) => Promise<boolean>;
  showUpgradeModal: boolean;
  setShowUpgradeModal: (show: boolean) => void;
}

function getTodayString(): string {
  return new Date().toISOString().split('T')[0];
}

// localStorage helpers for anonymous users
function getStoredUsage(): UsageData {
  if (typeof window === 'undefined') {
    return { count: 0, date: getTodayString() };
  }
  
  try {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (stored) {
      const data = JSON.parse(stored) as UsageData;
      // Reset if it's a new day
      if (data.date !== getTodayString()) {
        return { count: 0, date: getTodayString() };
      }
      return data;
    }
  } catch (e) {
    console.error('Error reading usage from localStorage:', e);
  }
  
  return { count: 0, date: getTodayString() };
}

function setStoredUsage(data: UsageData): void {
  if (typeof window === 'undefined') return;
  
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
  } catch (e) {
    console.error('Error saving usage to localStorage:', e);
  }
}

export function useUsageLimit(): UseUsageLimitReturn {
  const { isSignedIn, user, isLoaded } = useUser();
  const { session } = useSession();
  const [actionsUsed, setActionsUsed] = useState(0);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  
  // Use ref to track current count to avoid stale closure issues
  const actionsUsedRef = useRef(actionsUsed);
  actionsUsedRef.current = actionsUsed;

  // Helper to get auth token for API calls
  const getAuthToken = useCallback(async (): Promise<string | null> => {
    if (!session) {
      console.log('[getAuthToken] No session');
      return null;
    }
    try {
      const token = await session.getToken();
      console.log('[getAuthToken] Got token length:', token?.length || 0, 'First 20 chars:', token?.substring(0, 20) || 'none');
      return token;
    } catch (e) {
      console.error('[getAuthToken] Failed to get auth token:', e);
      return null;
    }
  }, [session]);

  // Check if user has premium subscription (from Clerk public metadata)
  const isPremium = Boolean(
    user?.publicMetadata?.subscriptionStatus === 'active' ||
    user?.publicMetadata?.isPremium === true
  );

  // Debug logging
  console.log('[useUsageLimit] isPremium:', isPremium, 'publicMetadata:', user?.publicMetadata);

  // Get usage from Clerk metadata for signed-in users
  const getClerkUsage = useCallback((): UsageData => {
    if (!user?.publicMetadata) {
      return { count: 0, date: getTodayString() };
    }
    
    const usageDate = user.publicMetadata.usageDate as string | undefined;
    const usageCount = user.publicMetadata.usageCount as number | undefined;
    
    // Reset if it's a new day
    if (usageDate !== getTodayString()) {
      return { count: 0, date: getTodayString() };
    }
    
    return { count: usageCount || 0, date: usageDate || getTodayString() };
  }, [user?.publicMetadata]);

  // Track if we've initialized to avoid re-setting from stale Clerk data
  const hasInitialized = useRef(false);

  // Initialize usage on mount (only once per session)
  useEffect(() => {
    if (!isLoaded || hasInitialized.current) return;
    
    if (isSignedIn && user) {
      // Signed in: use Clerk metadata for initial load only
      const usage = getClerkUsage();
      setActionsUsed(usage.count);
      hasInitialized.current = true;
    } else if (!isSignedIn) {
      // Anonymous: use localStorage
      const usage = getStoredUsage();
      setActionsUsed(usage.count);
      hasInitialized.current = true;
    }
    setIsLoading(false);
  }, [isLoaded, isSignedIn, user, getClerkUsage]);

  const actionsRemaining = Math.max(0, DAILY_LIMIT - actionsUsed);
  const canPerformAction = isPremium || actionsUsed < DAILY_LIMIT;

  const recordAction = useCallback(async (
    activityType: ActivityType, 
    metadata?: Record<string, string>
  ): Promise<boolean> => {
    // Use ref to get current value and avoid stale closure
    const currentCount = actionsUsedRef.current;
    console.log('[recordAction] Called with isPremium:', isPremium, 'actionsUsed:', currentCount);
    
    // Always increment count for all users (premium and free)
    const newCount = currentCount + 1;
    const today = getTodayString();
    
    const newActivity: ActivityLog = {
      type: activityType,
      timestamp: new Date().toISOString(),
      metadata,
    };

    // Check if limit reached (for non-premium)
    if (!isPremium && currentCount >= DAILY_LIMIT) {
      setShowUpgradeModal(true);
      return false;
    }

    if (isSignedIn && user) {
      // Get auth token for backend API
      const token = await getAuthToken();
      console.log('[recordAction] Got token:', token ? 'yes' : 'no', 'API_BASE_URL:', API_BASE_URL);
      
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      // Fire-and-forget tracking for all users (non-blocking)
      // This ensures the UI remains responsive even if tracking fails
      fetch(`${API_BASE_URL}/api/usage/record`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ 
          count: newCount, 
          date: today,
          activity: newActivity,
          isPremium,
        }),
      })
        .then(res => {
          console.log('[recordAction] API response status:', res.status);
          if (!res.ok) {
            res.text().then(text => console.error('[recordAction] API error:', text));
          }
        })
        .catch(err => console.error('[recordAction] Background usage tracking failed:', err));
      
      // Update local state immediately for all users
      setActionsUsed(newCount);
      
      // Show upgrade modal if this was their last free action (non-premium only)
      if (!isPremium && newCount >= DAILY_LIMIT) {
        setTimeout(() => {
          setShowUpgradeModal(true);
        }, 2000);
      }
      
      return true;
    } else {
      // Anonymous: update localStorage with activity tracking
      const currentUsage = getStoredUsage();
      const activities = currentUsage.activities || [];
      activities.push(newActivity);
      setStoredUsage({ count: newCount, date: today, activities });
      
      // Update local state for all anonymous users
      setActionsUsed(newCount);

      // Show upgrade modal if this was their last free action (non-premium only)
      if (!isPremium && newCount >= DAILY_LIMIT) {
        setTimeout(() => {
          setShowUpgradeModal(true);
        }, 2000);
      }
    }

    return true;
  }, [isPremium, isSignedIn, user, getAuthToken]);

  return {
    actionsUsed,
    actionsRemaining,
    dailyLimit: DAILY_LIMIT,
    canPerformAction,
    isPremium,
    isLoading,
    isSignedIn: Boolean(isSignedIn),
    recordAction,
    showUpgradeModal,
    setShowUpgradeModal,
  };
}
