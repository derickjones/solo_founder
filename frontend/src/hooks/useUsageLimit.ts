'use client';

import { useUser } from '@clerk/nextjs';
import { useState, useEffect, useCallback } from 'react';

const DAILY_LIMIT = 4;
const STORAGE_KEY = 'gospel_study_usage';

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
  const [actionsUsed, setActionsUsed] = useState(0);
  const [showUpgradeModal, setShowUpgradeModal] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  // Check if user has premium subscription (from Clerk public metadata)
  const isPremium = Boolean(
    user?.publicMetadata?.subscriptionStatus === 'active' ||
    user?.publicMetadata?.isPremium === true
  );

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

  // Initialize usage on mount
  useEffect(() => {
    if (!isLoaded) return;
    
    if (isSignedIn && user) {
      // Signed in: use Clerk metadata
      const usage = getClerkUsage();
      setActionsUsed(usage.count);
    } else {
      // Anonymous: use localStorage
      const usage = getStoredUsage();
      setActionsUsed(usage.count);
    }
    setIsLoading(false);
  }, [isLoaded, isSignedIn, user, getClerkUsage]);

  const actionsRemaining = Math.max(0, DAILY_LIMIT - actionsUsed);
  const canPerformAction = isPremium || actionsUsed < DAILY_LIMIT;

  const recordAction = useCallback(async (
    activityType: ActivityType, 
    metadata?: Record<string, string>
  ): Promise<boolean> => {
    // Premium users always allowed (but still track activity)
    const newCount = isPremium ? actionsUsed : actionsUsed + 1;
    const today = getTodayString();
    
    const newActivity: ActivityLog = {
      type: activityType,
      timestamp: new Date().toISOString(),
      metadata,
    };

    // Check if limit reached (for non-premium)
    if (!isPremium && actionsUsed >= DAILY_LIMIT) {
      setShowUpgradeModal(true);
      return false;
    }

    if (isSignedIn && user) {
      // Signed in: update Clerk metadata via API
      try {
        const response = await fetch('/api/usage/record', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            count: newCount, 
            date: today,
            activity: newActivity,
            isPremium,
          }),
        });
        
        if (!response.ok) {
          console.error('Failed to record usage');
          return false;
        }
      } catch (error) {
        console.error('Error recording usage:', error);
        return false;
      }
    } else {
      // Anonymous: update localStorage with activity tracking
      const currentUsage = getStoredUsage();
      const activities = currentUsage.activities || [];
      activities.push(newActivity);
      setStoredUsage({ count: newCount, date: today, activities });
    }

    if (!isPremium) {
      setActionsUsed(newCount);

      // Show upgrade modal if this was their last free action
      if (newCount >= DAILY_LIMIT) {
        setTimeout(() => {
          setShowUpgradeModal(true);
        }, 2000);
      }
    }

    return true;
  }, [actionsUsed, isPremium, isSignedIn, user]);

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
