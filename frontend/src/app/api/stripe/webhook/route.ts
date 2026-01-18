import { NextRequest, NextResponse } from 'next/server';import { NextRequest, NextResponse } from 'next/server';

import Stripe from 'stripe';

// This is a placeholder API routeimport { clerkClient } from '@clerk/nextjs/server';

// The actual stripe webhook logic is handled by the backend

export async function POST(request: NextRequest) {// Initialize Stripe only if API key is available

  return NextResponse.json(let stripe: Stripe | null = null;

    { error: 'This endpoint has been moved to the backend' },let webhookSecret: string | null = null;

    { status: 410 } // Gone

  );if (process.env.STRIPE_SECRET_KEY && process.env.STRIPE_SECRET_KEY !== 'your_stripe_secret_key_here') {

}  stripe = new Stripe(process.env.STRIPE_SECRET_KEY);
  webhookSecret = process.env.STRIPE_WEBHOOK_SECRET || null;
}

// Helper to update user subscription status in Clerk
async function updateUserSubscription(clerkUserId: string, status: 'active' | 'canceled' | 'past_due') {
  try {
    const client = await clerkClient();
    await client.users.updateUserMetadata(clerkUserId, {
      publicMetadata: {
        subscriptionStatus: status,
        isPremium: status === 'active',
        updatedAt: new Date().toISOString(),
      },
    });
    console.log(`Updated Clerk user ${clerkUserId} subscription status to: ${status}`);
  } catch (error) {
    console.error(`Failed to update Clerk user ${clerkUserId}:`, error);
    throw error;
  }
}

export async function POST(request: NextRequest) {
  // Check if Stripe is configured
  if (!stripe || !webhookSecret) {
    return NextResponse.json(
      { 
        error: 'Stripe webhook not configured',
        code: 'STRIPE_NOT_CONFIGURED'
      }, 
      { status: 503 }
    );
  }

  const body = await request.text();
  const signature = request.headers.get('stripe-signature')!;

  let event: Stripe.Event;

  try {
    event = stripe.webhooks.constructEvent(body, signature, webhookSecret);
  } catch (error) {
    console.error('Webhook signature verification failed:', error);
    return NextResponse.json({ error: 'Webhook signature verification failed' }, { status: 400 });
  }

  try {
    switch (event.type) {
      case 'customer.subscription.created':
      case 'customer.subscription.updated': {
        const subscription = event.data.object as Stripe.Subscription;
        const clerkUserId = subscription.metadata.clerkUserId;
        
        if (clerkUserId) {
          const status = subscription.status === 'active' ? 'active' : 
                        subscription.status === 'past_due' ? 'past_due' : 'canceled';
          await updateUserSubscription(clerkUserId, status);
        }
        console.log('Subscription event:', subscription.id, subscription.status);
        break;
      }

      case 'customer.subscription.deleted': {
        const deletedSubscription = event.data.object as Stripe.Subscription;
        const clerkUserId = deletedSubscription.metadata.clerkUserId;
        
        if (clerkUserId) {
          await updateUserSubscription(clerkUserId, 'canceled');
        }
        console.log('Subscription canceled:', deletedSubscription.id);
        break;
      }

      case 'invoice.payment_succeeded': {
        const invoice = event.data.object as Stripe.Invoice;
        console.log('Payment succeeded:', invoice.id);
        break;
      }

      case 'invoice.payment_failed': {
        const failedInvoice = event.data.object as Stripe.Invoice;
        const subscriptionId = (failedInvoice as any).subscription as string;
        
        // Get subscription to find clerk user
        if (subscriptionId) {
          const subscription = await stripe.subscriptions.retrieve(subscriptionId);
          const clerkUserId = subscription.metadata.clerkUserId;
          if (clerkUserId) {
            await updateUserSubscription(clerkUserId, 'past_due');
          }
        }
        console.log('Payment failed:', failedInvoice.id);
        break;
      }

      default:
        console.log(`Unhandled event type: ${event.type}`);
    }

    return NextResponse.json({ received: true });
  } catch (error) {
    console.error('Error processing webhook:', error);
    return NextResponse.json({ error: 'Webhook processing failed' }, { status: 500 });
  }
}