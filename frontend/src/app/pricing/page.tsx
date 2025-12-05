'use client';

import { useState } from 'react';
import { useUser } from '@clerk/nextjs';
import { loadStripe } from '@stripe/stripe-js';
import { CheckIcon } from '@heroicons/react/24/outline';
import { SUBSCRIPTION_PLANS } from '@/lib/stripe';
import Link from 'next/link';

// Only load Stripe if publishable key is available
const stripePromise = process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY && 
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY !== 'your_stripe_publishable_key_here'
  ? loadStripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY)
  : null;

export default function PricingPage() {
  const { isSignedIn } = useUser();
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
      const response = await fetch('/api/stripe/checkout', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ priceId }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        if (errorData.code === 'STRIPE_NOT_CONFIGURED') {
          alert('Payment processing is being set up. Please check back soon!');
          return;
        }
        throw new Error('Failed to create checkout session');
      }

      const { sessionId, url } = await response.json();
      
      if (url) {
        // Redirect to Stripe Checkout
        window.location.href = url;
      }
    } catch (error) {
      console.error('Error creating checkout session:', error);
      alert('There was an error processing your request. Please try again.');
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
            ← Back to Gospel Study Assistant
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
              <p className="text-neutral-400">Perfect for getting started</p>
            </div>

            <ul className="space-y-4 mb-8">
              {SUBSCRIPTION_PLANS.FREE.features.map((feature, index) => (
                <li key={index} className="flex items-center space-x-3">
                  <CheckIcon className="w-5 h-5 text-blue-400 flex-shrink-0" />
                  <span className="text-neutral-300">{feature}</span>
                </li>
              ))}
            </ul>

            <button
              disabled={true}
              className="w-full bg-neutral-700 text-neutral-400 py-3 px-6 rounded-lg font-medium cursor-not-allowed"
            >
              Current Plan
            </button>
          </div>

          {/* Premium Plan */}
          <div className="bg-gradient-to-br from-blue-900/30 to-blue-800/30 border-2 border-blue-500/50 rounded-2xl p-8 relative">
            {/* Popular badge */}
            <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
              <span className="bg-blue-600 text-white px-4 py-1 rounded-full text-sm font-medium">
                Most Popular
              </span>
            </div>

            <div className="text-center mb-6">
              <h3 className="text-2xl font-bold text-white mb-2">Premium</h3>
              <div className="text-4xl font-bold text-white mb-4">
                $4.99<span className="text-lg text-neutral-400">/month</span>
              </div>
              <p className="text-neutral-400">Unlimited gospel study power</p>
            </div>

            <ul className="space-y-4 mb-8">
              {SUBSCRIPTION_PLANS.PREMIUM.features.map((feature, index) => (
                <li key={index} className="flex items-center space-x-3">
                  <CheckIcon className="w-5 h-5 text-blue-400 flex-shrink-0" />
                  <span className="text-neutral-300">{feature}</span>
                </li>
              ))}
            </ul>

            <button
              onClick={() => handleSubscribe(SUBSCRIPTION_PLANS.PREMIUM.priceId!, 'premium')}
              disabled={loading === 'premium'}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 px-6 rounded-lg font-medium transition-colors disabled:opacity-50"
            >
              {loading === 'premium' ? 'Loading...' : 'Start Premium'}
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