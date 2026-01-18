#!/usr/bin/env python3
"""
Comprehensive Stripe-Clerk Synchronization Script
Fixes subscription status mismatches between Stripe and Clerk
"""

import os
import asyncio
import stripe
import httpx
import json
from datetime import datetime
from typing import List, Dict, Optional

# Configuration
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY") 
CLERK_API_BASE = "https://api.clerk.com/v1"

if STRIPE_SECRET_KEY:
    stripe.api_key = STRIPE_SECRET_KEY

async def get_all_stripe_subscriptions() -> List[Dict]:
    """Get all active subscriptions from Stripe"""
    print("📡 Fetching all Stripe subscriptions...")
    
    subscriptions = []
    has_more = True
    starting_after = None
    
    while has_more:
        params = {"limit": 100, "status": "all"}
        if starting_after:
            params["starting_after"] = starting_after
            
        subs = stripe.Subscription.list(**params)
        subscriptions.extend(subs.data)
        
        has_more = subs.has_more
        if has_more and subs.data:
            starting_after = subs.data[-1].id
    
    print(f"✅ Found {len(subscriptions)} total subscriptions")
    return subscriptions

async def get_clerk_user(user_id: str) -> Optional[Dict]:
    """Get user from Clerk API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CLERK_API_BASE}/users/{user_id}",
                headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"}
            )
            if response.status_code == 200:
                return response.json()
            return None
    except Exception as e:
        print(f"❌ Error fetching Clerk user {user_id}: {e}")
        return None

async def update_clerk_user_metadata(user_id: str, metadata: Dict) -> bool:
    """Update Clerk user metadata"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{CLERK_API_BASE}/users/{user_id}/metadata",
                headers={
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json"
                },
                json={"public_metadata": metadata}
            )
            return response.status_code == 200
    except Exception as e:
        print(f"❌ Error updating user {user_id}: {e}")
        return False

async def sync_subscription_status():
    """Sync all subscription statuses between Stripe and Clerk"""
    if not STRIPE_SECRET_KEY or not CLERK_SECRET_KEY:
        print("❌ Missing required environment variables:")
        print(f"   STRIPE_SECRET_KEY: {'✅' if STRIPE_SECRET_KEY else '❌'}")
        print(f"   CLERK_SECRET_KEY: {'✅' if CLERK_SECRET_KEY else '❌'}")
        return
    
    print("🚀 Starting Stripe-Clerk synchronization...")
    print("=" * 60)
    
    # Get all subscriptions from Stripe
    subscriptions = await get_all_stripe_subscriptions()
    
    updates_needed = []
    active_users = []
    
    for sub in subscriptions:
        clerk_user_id = sub.metadata.get("clerkUserId")
        if not clerk_user_id:
            continue
            
        stripe_status = sub.status
        customer = stripe.Customer.retrieve(sub.customer)
        customer_email = customer.email
        
        # Determine what the Clerk status should be
        should_be_premium = stripe_status == "active"
        subscription_status = "active" if stripe_status == "active" else (
            "past_due" if stripe_status == "past_due" else "canceled"
        )
        
        # Get current Clerk user data
        clerk_user = await get_clerk_user(clerk_user_id)
        if not clerk_user:
            print(f"⚠️  Clerk user not found: {clerk_user_id} (email: {customer_email})")
            continue
            
        current_metadata = clerk_user.get("public_metadata", {})
        current_is_premium = current_metadata.get("isPremium") == True
        current_sub_status = current_metadata.get("subscriptionStatus")
        
        print(f"\n👤 User: {customer_email}")
        print(f"   Clerk ID: {clerk_user_id}")
        print(f"   Stripe Status: {stripe_status}")
        print(f"   Current Clerk Premium: {current_is_premium}")
        print(f"   Current Clerk Sub Status: {current_sub_status}")
        print(f"   Should Be Premium: {should_be_premium}")
        
        # Check if update is needed
        if current_is_premium != should_be_premium or current_sub_status != subscription_status:
            updates_needed.append({
                "user_id": clerk_user_id,
                "email": customer_email,
                "stripe_status": stripe_status,
                "should_be_premium": should_be_premium,
                "subscription_status": subscription_status,
                "current_is_premium": current_is_premium,
                "current_sub_status": current_sub_status
            })
            print(f"   🔄 UPDATE NEEDED!")
        else:
            print(f"   ✅ Already in sync")
            
        if should_be_premium:
            active_users.append(customer_email)
    
    print(f"\n📊 Summary:")
    print(f"   Total subscriptions checked: {len([s for s in subscriptions if s.metadata.get('clerkUserId')])}")
    print(f"   Updates needed: {len(updates_needed)}")
    print(f"   Active premium users: {len(active_users)}")
    
    if updates_needed:
        print(f"\n🔄 Applying {len(updates_needed)} updates...")
        
        for update in updates_needed:
            print(f"\n   Updating {update['email']}...")
            success = await update_clerk_user_metadata(
                update["user_id"],
                {
                    "subscriptionStatus": update["subscription_status"],
                    "isPremium": update["should_be_premium"],
                    "updatedAt": datetime.utcnow().isoformat(),
                    "syncedAt": datetime.utcnow().isoformat()
                }
            )
            
            if success:
                print(f"   ✅ Updated {update['email']}")
            else:
                print(f"   ❌ Failed to update {update['email']}")
    
    print(f"\n🎉 Synchronization complete!")
    print(f"📧 Active premium users:")
    for email in active_users:
        print(f"   • {email}")

async def test_webhook_endpoint():
    """Test if the webhook endpoint is accessible"""
    webhook_url = "https://gospel-app-backend-273320302933.us-central1.run.app/api/stripe/webhook"
    
    print(f"🧪 Testing webhook endpoint: {webhook_url}")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook_url,
                json={"test": "webhook_test"},
                timeout=10.0
            )
            
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:200]}")
            
            if response.status_code == 400:
                print("   ✅ Webhook endpoint is accessible (400 expected for test data)")
            else:
                print(f"   ⚠️  Unexpected status code: {response.status_code}")
                
    except Exception as e:
        print(f"   ❌ Error testing webhook: {e}")

async def main():
    """Main execution function"""
    print("🔧 Stripe-Clerk Synchronization Tool")
    print("=" * 50)
    
    # Test webhook endpoint
    await test_webhook_endpoint()
    print()
    
    # Sync subscription statuses
    await sync_subscription_status()
    
    print("\n" + "=" * 50)
    print("✅ All done! Users should see their premium status now.")
    print("💡 Ask users to refresh their browser/app or sign out and back in.")

if __name__ == "__main__":
    asyncio.run(main())