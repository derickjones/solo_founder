'use client';

import { useState } from 'react';
import { useUser, useSession } from '@clerk/nextjs';
import { loadStripe } from '@stripe/stripe-js';
import { CheckIcon } from '@heroicons/react/24/outline';
import { SUBSCRIPTION_PLANS } from '@/lib/stripe';
import Link from 'next/link';

// Backend API base URL
const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://gospel-app-backend-273320302933.us-central1.run.app';

// Only load Stripe if publishable key is available
const stripePromise = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY && 
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY !== 'your_stripe_publishable_key_here'
  ? loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY)
  : null;

export default function PricingPage() {
  const { isSignedIn } = useUser();
  const { session } = useSession();
  const [loading, setLoading] = useState<string | null>(null);

  const handleSubscribe = async (priceId: string, planId: string) => {
    if (!isSignedIn) {
      // Redirect to sign up if not signed in
      window.location.href = '/sign-up';
      return;
    }

    // Check if Stripe is configured
    if (!stripePromise) {
      alert('Payment processing is not available yet. Please check back soon!');
      return;
    }

    setLoading(planId);

    try {
      // Get auth token for backend API
      const token = await session?.getToken();
      const headers: Record<string, string> = { 'Content-Type': 'application/json' };
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }

      console.log('Stripe checkout request:', {
        url: `${API_BASE_URL}/api/stripe/checkout`,
        priceId,
        hasToken: !!token
      });

      const response = await fetch(`${API_BASE_URL}/api/stripe/checkout`, {
        method: 'POST',
        headers,
        body: JSON.stringify({ priceId }),
      });

      if (!response.ok) {
        let errorMessage = `Server error: ${response.status}`;
        try {
          const errorData = await response.json();
          console.error('Backend error response:', errorData);
          
          if (errorData.code === 'STRIPE_NOT_CONFIGURED') {
            alert('Payment processing is being set up. Please check back soon!');
            return;
          }
          
          errorMessage = errorData.detail || errorData.message || errorMessage;
        } catch (parseError) {
          console.error('Failed to parse error response:', parseError);
          const errorText = await response.text();
          console.error('Error response text:', errorText);
          errorMessage = `${errorMessage} - ${errorText}`;
        }
        
        throw new Error(errorMessage);
      }

      const { sessionId, url } = await response.json();
      
      if (url) {
        // Redirect to Stripe Checkout
        window.location.href = url;
      }
    } catch (error) {
      console.error('Error creating checkout session:', error);
      const errorMessage = error instanceof Error ? error.message : 'Unknown error';
      alert(`There was an error processing your request: ${errorMessage}`);
    } finally {
      setLoading(null);
    }
  };

  return (
    <div className="min-h-screen bg-neutral-900 text-white">
      <div className="max-w-6xl mx-auto px-4 py-12">
        {/* Header */}
        <div className="text-center mb-12">
          <Link 
            href="/" 
            className="inline-flex items-center text-blue-400 hover:text-blue-300 mb-8"
          >
            ← Back to Gospel Study App
          </Link>
          <h1 className="text-4xl lg:text-5xl font-bold text-white mb-4">
            Choose Your Plan
          </h1>
          <p className="text-xl text-neutral-400 max-w-2xl mx-auto">
            Unlock the full power of AI-powered gospel study with our premium features
          </p>
        </div>

        {/* Pricing Cards */}
        <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
          {/* Free Plan */}
          <div className="bg-neutral-800 border border-neutral-700 rounded-2xl p-8 relative">
            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Free</h3>
              <div className="text-4xl font-bold text-white mb-4">
                $0<span className="text-lg text-neutral-400">/month</span>
              </div>
              <p className="text-neutral-400">Try everything, limited daily use</p>
            </div>

            <ul className="space-y-4 mb-8">
              <li className="flex items-center space-x-3">
                <CheckIcon className="w-5 h-5 text-blue-400 flex-shrink-0" />
                <span className="text-neutral-300">10 actions per day</span>
              </li>
              <li className="flex items-center space-x-3">
                <CheckIcon className="w-5 h-5 text-blue-400 flex-shrink-0" />
                <span className="text-neutral-300">Full access to all features</span>
              </li>
              <li className="flex items-center space-x-3">
                <CheckIcon className="w-5 h-5 text-blue-400 flex-shrink-0" />
                <span className="text-neutral-300">Q&A, Study Guides, Audio</span>
              </li>
              <li className="flex items-center space-x-3">
                <CheckIcon className="w-5 h-5 text-blue-400 flex-shrink-0" />
                <span className="text-neutral-300">Resets daily at midnight</span>
              </li>
            </ul>

            <button
              disabled={true}
              className="w-full bg-neutral-700 text-neutral-400 py-3 px-6 rounded-lg font-medium cursor-not-allowed"
            >
              Current Plan
            </button>
          </div>

          {/* Premium Plan */}
          <div className="bg-gradient-to-br from-amber-900/30 to-orange-800/30 border-2 border-amber-500/50 rounded-2xl p-8 relative">
            {/* Popular badge */}
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span className="bg-gradient-to-r from-amber-500 to-orange-500 text-white px-4 py-1 rounded-full text-sm font-medium">
                Unlimited
              </span>
            </div>

            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Premium</h3>
              <div className="text-4xl font-bold text-white mb-4">
                $3.99<span className="text-lg text-neutral-400">/month</span>
              </div>
              <p className="text-neutral-400">Unlimited gospel study</p>
            </div>

            <ul className="space-y-4 mb-8">
              <li className="flex items-center space-x-3">
                <CheckIcon className="w-5 h-5 text-amber-400 flex-shrink-0" />
                <span className="text-neutral-300 font-semibold">Unlimited actions</span>
              </li>
              <li className="flex items-center space-x-3">
                <CheckIcon className="w-5 h-5 text-amber-400 flex-shrink-0" />
                <span className="text-neutral-300">Full access to all features</span>
              </li>
              <li className="flex items-center space-x-3">
                <CheckIcon className="w-5 h-5 text-amber-400 flex-shrink-0" />
                <span className="text-neutral-300">Q&A, Study Guides, Audio</span>
              </li>
            </ul>

            <button
              onClick={() => handleSubscribe(SUBSCRIPTION_PLANS.PREMIUM.priceId!, 'premium')}
              disabled={loading === 'premium'}
              className="w-full bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-400 hover:to-orange-400 text-white py-3 px-6 rounded-lg font-medium transition-all disabled:opacity-50"
            >
              {loading === 'premium' ? 'Loading...' : 'Upgrade to Premium'}
            </button>
          </div>
        </div>

        {/* FAQ Section */}
        <div className="mt-16">
          <h2 className="text-3xl font-bold text-center text-white mb-8">
            Frequently Asked Questions
          </h2>
          <div className="max-w-3xl mx-auto space-y-6">
            <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-2">
                Can I cancel anytime?
              </h3>
              <p className="text-neutral-400">
                Yes, you can cancel your subscription at any time. You'll continue to have access to premium features until the end of your current billing period.
              </p>
            </div>
            <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-2">
                What payment methods do you accept?
              </h3>
              <p className="text-neutral-400">
                We accept all major credit cards, debit cards, and digital wallets through our secure payment processor Stripe.
              </p>
            </div>
            <div className="bg-neutral-800 border border-neutral-700 rounded-lg p-6">
              <h3 className="text-lg font-semibold text-white mb-2">
                Is my data secure?
              </h3>
              <p className="text-neutral-400">
                Absolutely. We use industry-standard encryption and security practices to protect your data and payment information.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}