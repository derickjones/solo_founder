'use client';

import { useAutoSync } from '@/hooks/useAutoSync';

/**
 * Client component that automatically syncs user subscriptions when they sign in
 * Should be used inside ClerkProvider
 */
export default function AutoSyncProvider({ children }: { children: React.ReactNode }) {
  // This hook runs the auto-sync logic
  useAutoSync();
  
  return <>{children}</>;
}