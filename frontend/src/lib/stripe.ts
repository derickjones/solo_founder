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
      '10 questions per day',
      'Basic scripture search',
      'Come Follow Me lessons'
    ],
    limits: {
      dailyQuestions: 10,
      pdfExports: 0
    }
  },
  PREMIUM: {
    id: 'premium',
    name: 'Premium',
    price: 499, // $4.99 in cents
    priceId: process.env.NEXT_PUBLIC_STRIPE_PREMIUM_PRICE_ID,
    features: [
      'Unlimited questions',
      'Advanced scripture search',
      'Come Follow Me lessons',
      'PDF lesson plan exports',
      'Priority support'
    ],
    limits: {
      dailyQuestions: -1, // unlimited
      pdfExports: -1 // unlimited
    }
  }
} as const;

export type SubscriptionPlan = keyof typeof SUBSCRIPTION_PLANS;