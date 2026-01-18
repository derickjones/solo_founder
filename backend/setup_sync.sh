#!/bin/bash
# Setup script to run the Stripe-Clerk sync

echo "🚀 Setting up Stripe-Clerk Sync Environment"
echo "=========================================="

# Check if we're in the backend directory
if [[ ! -f "requirements.txt" ]]; then
    echo "❌ Not in backend directory. Please run from backend folder."
    exit 1
fi

# Install dependencies if needed
echo "📦 Installing Python dependencies..."
pip3 install stripe httpx python-dotenv

# Check for environment variables
echo "🔍 Checking environment variables..."

if [[ -z "$STRIPE_SECRET_KEY" ]]; then
    echo "⚠️  STRIPE_SECRET_KEY not set"
    echo "   Please set: export STRIPE_SECRET_KEY=sk_your_key_here"
fi

if [[ -z "$CLERK_SECRET_KEY" ]]; then
    echo "⚠️  CLERK_SECRET_KEY not set" 
    echo "   Please set: export CLERK_SECRET_KEY=sk_your_key_here"
fi

if [[ -z "$STRIPE_WEBHOOK_SECRET" ]]; then
    echo "⚠️  STRIPE_WEBHOOK_SECRET not set"
    echo "   Please set: export STRIPE_WEBHOOK_SECRET=whsec_your_key_here"
fi

echo ""
echo "✅ Setup complete!"
echo "🔧 Run the sync with: python3 scripts/sync_stripe_clerk.py"