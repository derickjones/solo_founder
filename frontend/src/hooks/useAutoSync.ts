'use client';

import { useEffect, useRef } from 'react';
import { useUser } from '@clerk/nextjs';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://gospel-app-backend-273320302933.us-central1.run.app';

/**
 * Hook that automatically syncs a user's subscription status when they sign in
 * Runs only once per session to avoid redundant API calls
 */
export function useAutoSync() {
  const { isSignedIn, isLoaded, user } = useUser();
  const hasAttemptedSync = useRef(false);

  useEffect(() => {
    // Only sync if:
    // 1. Clerk has loaded
    // 2. User is signed in
    // 3. We have a user object
    // 4. We haven't already attempted sync this session
    if (isLoaded && isSignedIn && user && !hasAttemptedSync.current) {
      hasAttemptedSync.current = true;
      
      const syncUserSubscription = async () => {
        try {
          console.log(`🔄 Auto-syncing subscription status for user: ${user.id}`);
          
          const response = await fetch(`${API_BASE_URL}/api/admin/sync-user-subscription`, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              userId: user.id,
              email: user.primaryEmailAddress?.emailAddress
            }),
          });

          if (response.ok) {
            const result = await response.json();
            console.log('✅ Auto-sync completed:', result);
          } else {
            console.warn('⚠️ Auto-sync failed:', response.status, response.statusText);
          }
        } catch (error) {
          console.warn('⚠️ Auto-sync error:', error);
          // Silently fail - don't disrupt user experience
        }
      };

      // Run sync with a small delay to avoid blocking initial page load
      const timeoutId = setTimeout(syncUserSubscription, 1000);
      
      return () => clearTimeout(timeoutId);
    }
  }, [isLoaded, isSignedIn, user]);

  // Reset sync flag when user signs out
  useEffect(() => {
    if (isLoaded && !isSignedIn) {
      hasAttemptedSync.current = false;
    }
  }, [isLoaded, isSignedIn]);
}