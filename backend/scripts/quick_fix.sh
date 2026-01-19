#!/bin/bash
# Quick fix script for gates jones specifically

echo "🚀 Quick Fix for gatesjones11@gmail.com"
echo "======================================"

# Check if environment variables are set
if [[ -z "$STRIPE_SECRET_KEY" || -z "$CLERK_SECRET_KEY" ]]; then
    echo "❌ Missing environment variables. Please set:"
    echo "   export STRIPE_SECRET_KEY=sk_your_key_here"
    echo "   export CLERK_SECRET_KEY=sk_your_key_here"
    echo ""
    echo "🔍 You can find these keys at:"
    echo "   Stripe: https://dashboard.stripe.com/apikeys"
    echo "   Clerk: https://dashboard.clerk.com/last-active?path=api-keys"
    exit 1
fi

echo "✅ Environment variables found"
echo "🔄 Running full synchronization..."
echo ""

cd "$(dirname "$0")"
python3 sync_stripe_clerk.py