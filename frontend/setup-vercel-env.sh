#!/bin/bash

# Vercel Environment Variables Setup Script
# Run this script to set up all Clerk environment variables

echo "Setting up Clerk environment variables for Vercel..."

cd /Users/derickjones/Documents/VS-Code/solo_founder/frontend

# Link to your existing Vercel project
echo "Linking to Vercel project..."
vercel link --yes

# Add environment variables
echo "Adding NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY..."
echo "pk_test_dXB3YXJkLXN0dXJnZW9uLTQyLmNsZXJrLmFjY291bnRzLmRldiQ" | vercel env add NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY production

echo "Adding CLERK_SECRET_KEY..."
echo "sk_test_zdKYFROYB8r7QFe2X6WSeGrD4AFGulHqEPQvIRU0UM" | vercel env add CLERK_SECRET_KEY production

echo "Adding NEXT_PUBLIC_CLERK_SIGN_IN_URL..."
echo "/sign-in" | vercel env add NEXT_PUBLIC_CLERK_SIGN_IN_URL production

echo "Adding NEXT_PUBLIC_CLERK_SIGN_UP_URL..."
echo "/sign-up" | vercel env add NEXT_PUBLIC_CLERK_SIGN_UP_URL production

echo "Adding NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL..."
echo "/" | vercel env add NEXT_PUBLIC_CLERK_AFTER_SIGN_IN_URL production

echo "Adding NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL..."
echo "/" | vercel env add NEXT_PUBLIC_CLERK_AFTER_SIGN_UP_URL production

echo "Done! Environment variables added successfully."
echo "Now triggering a new deployment..."

# Trigger new deployment
vercel --prod

echo "Deployment complete! Your app should now work with Clerk authentication."