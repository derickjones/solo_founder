'use client';

import { useState } from 'react';

export default function ManageSubscriptionButton() {
  const [isLoading, setIsLoading] = useState(false);

  const handleManageSubscription = async () => {
    if (isLoading) return;
    
    setIsLoading(true);
    try {
      const response = await fetch('/api/stripe/customer-portal', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({}),
      });

      const data = await response.json();
      
      if (!response.ok) {
        console.error('Error creating customer portal session:', data);
        alert('Failed to open subscription management. Please try again.');
        return;
      }

      // Redirect to Stripe customer portal
      window.location.href = data.url;
      
    } catch (error) {
      console.error('Error:', error);
      alert('Failed to open subscription management. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <button
      onClick={handleManageSubscription}
      disabled={isLoading}
      className="w-full py-2.5 px-4 bg-neutral-800 hover:bg-neutral-700 disabled:bg-neutral-800/50 text-neutral-300 hover:text-white disabled:text-neutral-500 rounded-lg text-sm font-medium transition-all flex items-center justify-center gap-2 border border-neutral-700"
    >
      {isLoading ? (
        <>
          <div className="w-4 h-4 border-2 border-neutral-500 border-t-transparent rounded-full animate-spin"></div>
          <span>Loading...</span>
        </>
      ) : (
        <>
          <span>⚙️</span>
          <span>Manage Subscription</span>
        </>
      )}
    </button>
  );
}