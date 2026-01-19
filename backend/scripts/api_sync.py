#!/usr/bin/env python3
"""
Server-deployable version of Stripe-Clerk sync
Can be triggered via API endpoint for systematic fixes
"""

import os
import asyncio
import json
from fastapi import APIRouter, HTTPException, Header
from typing import Dict, List
import stripe
import httpx
from datetime import datetime
import logging

# Add to your existing user_api.py router
logger = logging.getLogger(__name__)

# Use existing configuration from user_api.py
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_API_BASE = "https://api.clerk.com/v1"

if stripe_secret_key:
    stripe.api_key = stripe_secret_key

async def sync_all_subscriptions() -> Dict:
    """Sync all Stripe subscriptions with Clerk - systematic fix"""
    if not stripe_secret_key or not CLERK_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe or Clerk not configured"
        )
    
    logger.info("Starting systematic subscription sync...")
    
    # Get all subscriptions
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
    
    logger.info(f"Found {len(subscriptions)} total subscriptions")
    
    # Process each subscription
    updates_made = []
    errors = []
    
    for sub in subscriptions:
        clerk_user_id = sub.metadata.get("clerkUserId")
        if not clerk_user_id:
            continue
            
        try:
            # Get customer email
            customer = stripe.Customer.retrieve(sub.customer)
            customer_email = customer.email
            
            # Determine correct status
            stripe_status = sub.status
            should_be_premium = stripe_status == "active"
            subscription_status = "active" if stripe_status == "active" else (
                "past_due" if stripe_status == "past_due" else "canceled"
            )
            
            # Get current Clerk user
            async with httpx.AsyncClient() as client:
                clerk_response = await client.get(
                    f"{CLERK_API_BASE}/users/{clerk_user_id}",
                    headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"}
                )
                
                if clerk_response.status_code != 200:
                    errors.append(f"Clerk user not found: {clerk_user_id} ({customer_email})")
                    continue
                
                clerk_user = clerk_response.json()
                current_metadata = clerk_user.get("public_metadata", {})
                current_is_premium = current_metadata.get("isPremium") == True
                
                # Check if update needed
                if current_is_premium != should_be_premium:
                    # Update user metadata
                    update_response = await client.patch(
                        f"{CLERK_API_BASE}/users/{clerk_user_id}/metadata",
                        headers={
                            "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                            "Content-Type": "application/json"
                        },
                        json={
                            "public_metadata": {
                                **current_metadata,
                                "subscriptionStatus": subscription_status,
                                "isPremium": should_be_premium,
                                "updatedAt": datetime.utcnow().isoformat(),
                                "syncedAt": datetime.utcnow().isoformat()
                            }
                        }
                    )
                    
                    if update_response.status_code == 200:
                        updates_made.append({
                            "email": customer_email,
                            "user_id": clerk_user_id,
                            "stripe_status": stripe_status,
                            "updated_to_premium": should_be_premium
                        })
                        logger.info(f"Updated {customer_email} to premium: {should_be_premium}")
                    else:
                        errors.append(f"Failed to update {customer_email}: {update_response.status_code}")
                        
        except Exception as e:
            errors.append(f"Error processing subscription {sub.id}: {str(e)}")
            logger.error(f"Sync error: {e}")
    
    return {
        "success": True,
        "total_subscriptions": len(subscriptions),
        "updates_made": len(updates_made),
        "updated_users": updates_made,
        "errors": errors,
        "timestamp": datetime.utcnow().isoformat()
    }

# Add this endpoint to your user_api.py
@router.post("/admin/sync-subscriptions")
async def sync_subscriptions_endpoint(authorization: str = Header(None)):
    """Systematic fix for all subscription statuses (Admin only)"""
    # Verify admin access (you can use your existing admin verification)
    user_id = await verify_clerk_token(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Check if user is admin (you might have this logic already)
    admin_emails = ["derickdavidjones@gmail.com"]  # Add your admin email
    clerk_user = await get_clerk_user(user_id)
    if not clerk_user or not any(email.get("email_address") == admin_email for admin_email in admin_emails for email in clerk_user.get("email_addresses", [])):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    try:
        result = await sync_all_subscriptions()
        return result
    except Exception as e:
        logger.error(f"Sync endpoint error: {e}")
        raise HTTPException(status_code=500, detail=f"Sync failed: {str(e)}")

if __name__ == "__main__":
    # For standalone execution
    asyncio.run(sync_all_subscriptions())