import { loadStripe } from '@stripe/stripe-js';

// Initialize Stripe
export const stripePromise = loadStripe(
  process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!
);

// Subscription plans configuration
export const SUBSCRIPTION_PLANS = {
  FREE: {
    id: 'free',
    name: 'Free',
    price: 0,
    priceId: null,
    features: [
      '4 actions per day',
      'Full access to all features',
      'Resets daily at midnight'
    ],
    limits: {
      dailyActions: 4,
    }
  },
  PREMIUM: {
    id: 'premium',
    name: 'Premium',
    price: 199, // $1.99 in cents
    priceId: process.env.NEXT_PUBLIC_STRIPE_PREMIUM_PRICE_ID,
    features: [
      'Unlimited actions',
      'Full access to all features',
      'Priority support'
    ],
    limits: {
      dailyActions: -1, // unlimited
    }
  }
} as const;

export type SubscriptionPlan = keyof typeof SUBSCRIPTION_PLANS;