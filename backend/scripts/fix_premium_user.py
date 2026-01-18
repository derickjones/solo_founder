#!/usr/bin/env python3
"""
Manual script to update user subscription status in Clerk
Run this to manually fix the premium user issue
"""

import os
import httpx
import asyncio
import json
from datetime import datetime

# Clerk configuration
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_API_BASE = "https://api.clerk.com/v1"

async def update_user_to_premium(email: str, user_id: str = None):
    """Update user to premium status in Clerk"""
    if not CLERK_SECRET_KEY:
        print("❌ CLERK_SECRET_KEY not found in environment")
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            # First, find the user by email if user_id not provided
            if not user_id:
                print(f"🔍 Finding user with email: {email}")
                response = await client.get(
                    f"{CLERK_API_BASE}/users",
                    headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"},
                    params={"email_address": email}
                )
                
                if response.status_code != 200:
                    print(f"❌ Failed to find user: {response.status_code}")
                    return False
                
                users = response.json()
                if not users:
                    print(f"❌ No user found with email: {email}")
                    return False
                
                user_id = users[0]["id"]
                print(f"✅ Found user: {user_id}")
            
            # Update user metadata to premium
            print(f"🔄 Updating user {user_id} to premium...")
            metadata_response = await client.patch(
                f"{CLERK_API_BASE}/users/{user_id}/metadata",
                headers={
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "public_metadata": {
                        "subscriptionStatus": "active",
                        "isPremium": True,
                        "updatedAt": datetime.utcnow().isoformat(),
                        "manuallyUpdated": True  # Flag for tracking
                    }
                }
            )
            
            if metadata_response.status_code == 200:
                print(f"✅ Successfully updated user {email} to premium!")
                print(f"📋 Response: {json.dumps(metadata_response.json(), indent=2)}")
                return True
            else:
                print(f"❌ Failed to update metadata: {metadata_response.status_code}")
                print(f"📋 Error: {metadata_response.text}")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

async def main():
    """Main function to update the user"""
    email = "gatesjones11@gmail.com"
    
    print("🚀 Manual Premium User Update Script")
    print("=" * 50)
    print(f"Target user: {email}")
    print()
    
    success = await update_user_to_premium(email)
    
    if success:
        print("\n✅ SUCCESS! User has been updated to premium.")
        print("🔄 Ask the user to:")
        print("   1. Refresh their browser/app")
        print("   2. Sign out and sign back in")
        print("   3. Check their subscription status")
    else:
        print("\n❌ FAILED! Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())