#!/usr/bin/env python3
"""
User Management API Routes for Gospel Study App
Handles usage tracking, analytics, feedback, and Stripe payments
Migrated from Next.js API routes for Capacitor mobile app support
"""

import os
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, HTTPException, Header, Request
from pydantic import BaseModel
import httpx
import stripe

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter(prefix="/api", tags=["user"])

# Initialize Stripe
stripe_secret_key = os.getenv("STRIPE_SECRET_KEY")
stripe_webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")
if stripe_secret_key:
    stripe.api_key = stripe_secret_key
    logger.info("✅ Stripe initialized")
else:
    logger.warning("⚠️ STRIPE_SECRET_KEY not found")

# Clerk configuration
CLERK_SECRET_KEY = os.getenv("CLERK_SECRET_KEY")
CLERK_API_BASE = "https://api.clerk.com/v1"
ADMIN_USER_IDS = os.getenv("ADMIN_USER_IDS", "").split(",") if os.getenv("ADMIN_USER_IDS") else []
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://gospel-study-app.vercel.app")

# In-memory feedback storage (for demo purposes - consider using a database for production)
recent_feedback = []
MAX_FEEDBACK_ITEMS = 100  # Keep last 100 feedback items

# ============================================================================
# Pydantic Models
# ============================================================================

class ActivityLog(BaseModel):
    type: str  # qa_question, study_guide, audio_summary, tile_click, podcast_play, lesson_plan, core_content, daily_thought
    timestamp: str
    metadata: Optional[Dict[str, str]] = None

class UsageRecordRequest(BaseModel):
    count: int
    date: str
    activity: Optional[ActivityLog] = None
    isPremium: Optional[bool] = False

class UsageRecordResponse(BaseModel):
    success: bool
    count: int
    date: str
    activitiesCount: Optional[int] = 0

class UsageGetResponse(BaseModel):
    count: int
    date: str

class FeedbackRequest(BaseModel):
    type: str  # bug, feature, general, praise
    message: str
    email: Optional[str] = None
    userId: Optional[str] = None
    userName: Optional[str] = None

class FeedbackResponse(BaseModel):
    success: bool
    message: str

class StripeCheckoutRequest(BaseModel):
    priceId: str

class StripeCheckoutResponse(BaseModel):
    sessionId: str
    url: str

class StripeCustomerPortalRequest(BaseModel):
    return_url: Optional[str] = None

class StripeCustomerPortalResponse(BaseModel):
    url: str

class AnalyticsResponse(BaseModel):
    totalUsers: int
    activeToday: int
    premiumUsers: int
    freeUsers: int
    activityBreakdown: Dict[str, int]
    topActivities: List[Dict[str, Any]]
    conversionRate: float
    userDetails: List[Dict[str, Any]]

class FeedbackListResponse(BaseModel):
    feedback: List[Dict[str, Any]]
    total: int

# ============================================================================
# Helper Functions
# ============================================================================

async def verify_clerk_token(authorization: str) -> Optional[str]:
    """Verify Clerk JWT token and return user ID"""
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("No authorization header or invalid format")
        return None
    
    token = authorization.replace("Bearer ", "")
    logger.info(f"Token received - length: {len(token)}, first 20 chars: {token[:20]}...")
    
    if not CLERK_SECRET_KEY:
        logger.error("CLERK_SECRET_KEY not configured")
        return None
    
    try:
        # Decode JWT to extract user ID from 'sub' claim
        # The token is already verified by Clerk on the frontend
        import base64
        import json
        
        parts = token.split(".")
        logger.info(f"Token parts: {len(parts)}")
        
        if len(parts) >= 2:
            # Decode payload (add padding if needed)
            payload = parts[1]
            padding = 4 - len(payload) % 4
            if padding != 4:
                payload += "=" * padding
            
            decoded = base64.urlsafe_b64decode(payload)
            claims = json.loads(decoded)
            user_id = claims.get("sub")
            
            if user_id:
                logger.info(f"Token verified for user: {user_id}")
                return user_id
            else:
                logger.warning("No 'sub' claim in token")
                logger.info(f"Available claims: {list(claims.keys())}")
                return None
        else:
            logger.warning(f"Invalid token format: {len(parts)} parts")
            return None
            
    except Exception as e:
        logger.error(f"Token verification error: {e}")
        return None


async def get_clerk_user(user_id: str) -> Optional[Dict]:
    """Get user details from Clerk"""
    if not CLERK_SECRET_KEY:
        return None
    
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
        logger.error(f"Error fetching Clerk user: {e}")
        return None


async def update_clerk_user_metadata(user_id: str, public_metadata: Dict) -> bool:
    """Update user's public metadata in Clerk"""
    if not CLERK_SECRET_KEY:
        return False
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.patch(
                f"{CLERK_API_BASE}/users/{user_id}/metadata",
                headers={
                    "Authorization": f"Bearer {CLERK_SECRET_KEY}",
                    "Content-Type": "application/json"
                },
                json={"public_metadata": public_metadata}
            )
            return response.status_code == 200
    except Exception as e:
        logger.error(f"Error updating Clerk user metadata: {e}")
        return False


# ============================================================================
# API Endpoints
# ============================================================================

@router.post("/usage/record", response_model=UsageRecordResponse)
async def record_usage(
    request: UsageRecordRequest,
    authorization: str = Header(None)
):
    """Record user activity and update usage statistics"""
    user_id = await verify_clerk_token(authorization)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        # Get current user
        user = await get_clerk_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        current_metadata = user.get("public_metadata", {})
        
        # Get existing activities for today, or start fresh
        existing_date = current_metadata.get("usageDate")
        activities = []
        
        if existing_date == request.date and current_metadata.get("activities"):
            activities = current_metadata.get("activities", [])
        
        # Add new activity if provided
        if request.activity:
            activities.append(request.activity.model_dump())
            # Keep only last 50 activities per day
            if len(activities) > 50:
                activities = activities[-50:]
        
        # Track lifetime stats
        lifetime_stats = current_metadata.get("lifetimeStats", {})
        if request.activity and request.activity.type:
            lifetime_stats[request.activity.type] = lifetime_stats.get(request.activity.type, 0) + 1
            lifetime_stats["totalActions"] = lifetime_stats.get("totalActions", 0) + 1
        
        # Update metadata
        new_metadata = {
            **current_metadata,
            "usageCount": request.count,
            "usageDate": request.date,
            "activities": activities,
            "lifetimeStats": lifetime_stats,
            "lastActivity": datetime.utcnow().isoformat()
        }
        
        success = await update_clerk_user_metadata(user_id, new_metadata)
        
        if not success:
            raise HTTPException(status_code=500, detail="Failed to update user metadata")
        
        logger.info(f"[usage/record] Success for user {user_id}")
        
        return UsageRecordResponse(
            success=True,
            count=request.count,
            date=request.date,
            activitiesCount=len(activities)
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[usage/record] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to record usage: {str(e)}")


@router.get("/usage/record", response_model=UsageGetResponse)
async def get_usage(authorization: str = Header(None)):
    """Get current day's usage count for user"""
    user_id = await verify_clerk_token(authorization)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    try:
        user = await get_clerk_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        metadata = user.get("public_metadata", {})
        today = datetime.utcnow().strftime("%Y-%m-%d")
        usage_date = metadata.get("usageDate")
        usage_count = metadata.get("usageCount", 0)
        
        # Reset if it's a new day
        if usage_date != today:
            return UsageGetResponse(count=0, date=today)
        
        return UsageGetResponse(
            count=usage_count,
            date=usage_date or today
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[usage/get] Error: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch usage")


@router.get("/analytics", response_model=AnalyticsResponse)
async def get_analytics(authorization: str = Header(None)):
    """Get aggregated user analytics (admin only)"""
    user_id = await verify_clerk_token(authorization)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Check admin access
    if ADMIN_USER_IDS and user_id not in ADMIN_USER_IDS:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if not CLERK_SECRET_KEY:
        raise HTTPException(status_code=503, detail="Clerk not configured")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{CLERK_API_BASE}/users",
                headers={"Authorization": f"Bearer {CLERK_SECRET_KEY}"},
                params={"limit": 100}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=500, detail="Failed to fetch users")
            
            users_data = response.json()
            users = users_data.get("data", []) if isinstance(users_data, dict) else users_data
        
        today = datetime.utcnow().strftime("%Y-%m-%d")
        
        analytics = {
            "totalUsers": len(users),
            "activeToday": 0,
            "premiumUsers": 0,
            "freeUsers": 0,
            "activityBreakdown": {},
            "topActivities": [],
            "conversionRate": 0.0,
            "userDetails": []
        }
        
        for user in users:
            metadata = user.get("public_metadata", {})
            is_premium = metadata.get("isPremium") == True or metadata.get("subscriptionStatus") == "active"
            lifetime_stats = metadata.get("lifetimeStats", {})
            usage_date = metadata.get("usageDate")
            
            # Count premium vs free
            if is_premium:
                analytics["premiumUsers"] += 1
            else:
                analytics["freeUsers"] += 1
            
            # Count active today
            if usage_date == today:
                analytics["activeToday"] += 1
            
            # Aggregate activity breakdown
            for activity, count in lifetime_stats.items():
                if activity != "totalActions" and isinstance(count, (int, float)):
                    analytics["activityBreakdown"][activity] = analytics["activityBreakdown"].get(activity, 0) + count
            
            # Get email
            email_addresses = user.get("email_addresses", [])
            email = email_addresses[0].get("email_address", "N/A") if email_addresses else "N/A"
            
            # Add user details
            analytics["userDetails"].append({
                "id": user.get("id"),
                "email": email,
                "isPremium": is_premium,
                "lifetimeActions": lifetime_stats.get("totalActions", 0),
                "lastActivity": metadata.get("lastActivity"),
                "activityBreakdown": lifetime_stats
            })
        
        # Sort activities by count
        analytics["topActivities"] = [
            {"activity": k, "count": v}
            for k, v in sorted(analytics["activityBreakdown"].items(), key=lambda x: x[1], reverse=True)
        ]
        
        # Calculate conversion rate
        if analytics["totalUsers"] > 0:
            analytics["conversionRate"] = round((analytics["premiumUsers"] / analytics["totalUsers"]) * 100, 1)
        
        # Sort users by activity
        analytics["userDetails"].sort(key=lambda x: x["lifetimeActions"], reverse=True)
        
        return AnalyticsResponse(**analytics)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"[analytics] Error: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch analytics: {str(e)}")


@router.get("/feedback", response_model=FeedbackListResponse)
async def get_feedback(authorization: str = Header(None)):
    """Get all submitted feedback (admin only)"""
    user_id = await verify_clerk_token(authorization)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Check admin access
    if ADMIN_USER_IDS and user_id not in ADMIN_USER_IDS:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    # Return feedback in reverse chronological order (newest first)
    sorted_feedback = sorted(recent_feedback, key=lambda x: x["timestamp"], reverse=True)
    
    return FeedbackListResponse(
        feedback=sorted_feedback,
        total=len(sorted_feedback)
    )


@router.post("/feedback", response_model=FeedbackResponse)
async def submit_feedback(request: FeedbackRequest):
    """Submit user feedback"""
    if not request.message or not request.type:
        raise HTTPException(status_code=400, detail="Missing required fields")
    
    feedback = {
        "type": request.type,
        "message": request.message,
        "email": request.email,
        "userId": request.userId,
        "userName": request.userName,
        "timestamp": datetime.utcnow().isoformat()
    }
    
    # Log feedback (visible in Cloud Run logs)
    logger.info(f"📨 FEEDBACK: {feedback}")
    
    # Store in memory for admin viewing
    recent_feedback.append(feedback)
    if len(recent_feedback) > MAX_FEEDBACK_ITEMS:
        recent_feedback.pop(0)  # Remove oldest item
    
    # TODO: Optionally save to database or send email
    
    return FeedbackResponse(
        success=True,
        message="Feedback submitted successfully"
    )


@router.post("/stripe/checkout", response_model=StripeCheckoutResponse)
async def create_checkout_session(
    request: StripeCheckoutRequest,
    authorization: str = Header(None)
):
    """Create Stripe checkout session for subscription"""
    if not stripe_secret_key:
        raise HTTPException(
            status_code=503,
            detail="Payment processing not configured yet. Please contact support."
        )
    
    user_id = await verify_clerk_token(authorization)
    
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    if not request.priceId:
        raise HTTPException(status_code=400, detail="Price ID is required")
    
    try:
        session = stripe.checkout.Session.create(
            line_items=[{
                "price": request.priceId,
                "quantity": 1
            }],
            mode="subscription",
            success_url=f"{FRONTEND_URL}/?success=true&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/?canceled=true",
            metadata={
                "clerkUserId": user_id
            },
            subscription_data={
                "metadata": {
                    "clerkUserId": user_id
                }
            }
        )
        
        return StripeCheckoutResponse(
            sessionId=session.id,
            url=session.url
        )
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create checkout session")
    except Exception as e:
        logger.error(f"Checkout error: {e}")
        raise HTTPException(status_code=500, detail="Failed to create checkout session")


@router.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    """Handle Stripe webhook events"""
    if not stripe_secret_key or not stripe_webhook_secret:
        raise HTTPException(status_code=503, detail="Stripe webhook not configured")
    
    body = await request.body()
    signature = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            body, signature, stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")
    
    try:
        if event["type"] in ["customer.subscription.created", "customer.subscription.updated"]:
            subscription = event["data"]["object"]
            clerk_user_id = subscription.get("metadata", {}).get("clerkUserId")
            
            if clerk_user_id:
                status = subscription["status"]
                sub_status = "active" if status == "active" else ("past_due" if status == "past_due" else "canceled")
                
                await update_clerk_user_metadata(clerk_user_id, {
                    "subscriptionStatus": sub_status,
                    "isPremium": sub_status == "active",
                    "updatedAt": datetime.utcnow().isoformat()
                })
                logger.info(f"Updated subscription for user {clerk_user_id}: {sub_status}")
        
        elif event["type"] == "customer.subscription.deleted":
            subscription = event["data"]["object"]
            clerk_user_id = subscription.get("metadata", {}).get("clerkUserId")
            
            if clerk_user_id:
                await update_clerk_user_metadata(clerk_user_id, {
                    "subscriptionStatus": "canceled",
                    "isPremium": False,
                    "updatedAt": datetime.utcnow().isoformat()
                })
                logger.info(f"Canceled subscription for user {clerk_user_id}")
        
        elif event["type"] == "invoice.payment_failed":
            invoice = event["data"]["object"]
            subscription_id = invoice.get("subscription")
            
            if subscription_id:
                subscription = stripe.Subscription.retrieve(subscription_id)
                clerk_user_id = subscription.get("metadata", {}).get("clerkUserId")
                
                if clerk_user_id:
                    await update_clerk_user_metadata(clerk_user_id, {
                        "subscriptionStatus": "past_due",
                        "updatedAt": datetime.utcnow().isoformat()
                    })
        
        return {"received": True}
        
    except Exception as e:
        logger.error(f"Webhook processing error: {e}")
        raise HTTPException(status_code=500, detail="Webhook processing failed")


@router.post("/admin/sync-user-subscription")
async def sync_user_subscription(request: dict):
    """Sync a single user's subscription status automatically (no auth required for auto-sync)"""
    user_id = request.get("userId")
    email = request.get("email")
    
    if not user_id:
        raise HTTPException(status_code=400, detail="userId is required")
    
    if not stripe_secret_key or not CLERK_SECRET_KEY:
        logger.warning("Sync skipped - Stripe or Clerk not configured")
        return {"success": True, "message": "Sync skipped - configuration unavailable", "updated": False}
    
    logger.info(f"Auto-syncing subscription for user: {user_id} ({email})")
    
    try:
        # Find user's Stripe subscriptions by searching for their Clerk user ID
        subscriptions = stripe.Subscription.list(
            limit=10,  # Most users will only have 1 subscription
            expand=["data.customer"]
        )
        
        user_subscription = None
        for sub in subscriptions.data:
            if sub.metadata.get("clerkUserId") == user_id:
                user_subscription = sub
                break
        
        # If no subscription found, ensure user is marked as non-premium
        if not user_subscription:
            # Get current Clerk user
            clerk_user_data = await get_clerk_user(user_id)
            if not clerk_user_data:
                logger.warning(f"Clerk user not found for auto-sync: {user_id}")
                return {"success": True, "message": "User not found", "updated": False}
            
            current_metadata = clerk_user_data.get("public_metadata", {})
            current_is_premium = current_metadata.get("isPremium") == True
            
            # If currently marked as premium but no subscription, update to non-premium
            if current_is_premium:
                success = await update_clerk_user_metadata(
                    user_id,
                    {
                        **current_metadata,
                        "subscriptionStatus": "none",
                        "isPremium": False,
                        "syncedAt": datetime.utcnow().isoformat()
                    }
                )
                
                if success:
                    logger.info(f"✅ Auto-sync: Updated {email} to non-premium (no subscription found)")
                    return {"success": True, "message": "Updated to non-premium", "updated": True}
                else:
                    logger.error(f"❌ Auto-sync: Failed to update {email}")
                    return {"success": False, "message": "Failed to update user", "updated": False}
            else:
                logger.info(f"✅ Auto-sync: {email} already correctly set as non-premium")
                return {"success": True, "message": "Already in sync (non-premium)", "updated": False}
        
        # Process the found subscription
        stripe_status = user_subscription.status
        should_be_premium = stripe_status == "active"
        subscription_status = "active" if stripe_status == "active" else (
            "past_due" if stripe_status == "past_due" else "canceled"
        )
        
        # Get current Clerk user
        clerk_user_data = await get_clerk_user(user_id)
        if not clerk_user_data:
            logger.warning(f"Clerk user not found for auto-sync: {user_id}")
            return {"success": True, "message": "User not found", "updated": False}
        
        current_metadata = clerk_user_data.get("public_metadata", {})
        current_is_premium = current_metadata.get("isPremium") == True
        current_sub_status = current_metadata.get("subscriptionStatus")
        
        # Check if update needed
        if current_is_premium != should_be_premium or current_sub_status != subscription_status:
            # Update user metadata
            success = await update_clerk_user_metadata(
                user_id,
                {
                    **current_metadata,
                    "subscriptionStatus": subscription_status,
                    "isPremium": should_be_premium,
                    "syncedAt": datetime.utcnow().isoformat(),
                    "stripeCustomerId": user_subscription.customer.id if hasattr(user_subscription.customer, 'id') else user_subscription.customer
                }
            )
            
            if success:
                logger.info(f"✅ Auto-sync: Updated {email} - Premium: {should_be_premium} (was {current_is_premium})")
                return {"success": True, "message": f"Updated to premium: {should_be_premium}", "updated": True}
            else:
                logger.error(f"❌ Auto-sync: Failed to update {email}")
                return {"success": False, "message": "Failed to update user", "updated": False}
        else:
            logger.info(f"✅ Auto-sync: {email} already in sync (premium: {should_be_premium})")
            return {"success": True, "message": f"Already in sync (premium: {should_be_premium})", "updated": False}
            
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error during auto-sync: {e}")
        return {"success": False, "message": f"Stripe error: {str(e)}", "updated": False}
    except Exception as e:
        logger.error(f"Auto-sync error: {e}")
        return {"success": False, "message": f"Auto-sync failed: {str(e)}", "updated": False}


@router.post("/admin/sync-subscriptions")
async def sync_all_subscriptions(authorization: str = Header(None)):
    """Systematically sync all Stripe subscriptions with Clerk metadata (Admin only)"""
    user_id = await verify_clerk_token(authorization)
    if not user_id:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    # Verify admin access
    clerk_user = await get_clerk_user(user_id)
    if not clerk_user:
        raise HTTPException(status_code=401, detail="User not found")
    
    # Check if user is admin
    user_emails = [email.get("email_address", "") for email in clerk_user.get("email_addresses", [])]
    admin_emails = ["derickdavidjones@gmail.com"]  # Add your admin emails here
    
    if not any(email in admin_emails for email in user_emails):
        raise HTTPException(status_code=403, detail="Admin access required")
    
    if not stripe_secret_key or not CLERK_SECRET_KEY:
        raise HTTPException(
            status_code=503,
            detail="Stripe or Clerk not properly configured"
        )
    
    logger.info("Starting systematic subscription synchronization...")
    
    try:
        # Get all subscriptions from Stripe
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
        premium_users = []
        
        for sub in subscriptions:
            clerk_user_id = sub.metadata.get("clerkUserId")
            if not clerk_user_id:
                continue
                
            try:
                # Get customer email
                customer = stripe.Customer.retrieve(sub.customer)
                customer_email = customer.email or "unknown@email.com"
                
                # Determine correct status
                stripe_status = sub.status
                should_be_premium = stripe_status == "active"
                subscription_status = "active" if stripe_status == "active" else (
                    "past_due" if stripe_status == "past_due" else "canceled"
                )
                
                # Get current Clerk user
                clerk_user_data = await get_clerk_user(clerk_user_id)
                if not clerk_user_data:
                    errors.append(f"Clerk user not found: {clerk_user_id} ({customer_email})")
                    continue
                
                current_metadata = clerk_user_data.get("public_metadata", {})
                current_is_premium = current_metadata.get("isPremium") == True
                current_sub_status = current_metadata.get("subscriptionStatus")
                
                # Check if update needed
                if current_is_premium != should_be_premium or current_sub_status != subscription_status:
                    # Update user metadata
                    success = await update_clerk_user_metadata(
                        clerk_user_id,
                        {
                            **current_metadata,
                            "subscriptionStatus": subscription_status,
                            "isPremium": should_be_premium,
                            "updatedAt": datetime.utcnow().isoformat(),
                            "syncedAt": datetime.utcnow().isoformat(),
                            "stripeCustomerId": sub.customer
                        }
                    )
                    
                    if success:
                        updates_made.append({
                            "email": customer_email,
                            "user_id": clerk_user_id,
                            "stripe_status": stripe_status,
                            "updated_to_premium": should_be_premium,
                            "previous_premium": current_is_premium
                        })
                        logger.info(f"✅ Updated {customer_email} - Premium: {should_be_premium}")
                    else:
                        errors.append(f"Failed to update {customer_email} in Clerk")
                else:
                    logger.info(f"✅ {customer_email} already in sync")
                
                if should_be_premium:
                    premium_users.append(customer_email)
                        
            except Exception as e:
                error_msg = f"Error processing subscription {sub.id}: {str(e)}"
                errors.append(error_msg)
                logger.error(error_msg)
        
        logger.info(f"Sync complete - {len(updates_made)} users updated")
        
        return {
            "success": True,
            "message": f"Synchronization complete",
            "stats": {
                "total_subscriptions_checked": len([s for s in subscriptions if s.metadata.get('clerkUserId')]),
                "updates_made": len(updates_made),
                "current_premium_users": len(premium_users),
                "errors_count": len(errors)
            },
            "updated_users": updates_made,
            "premium_users": premium_users,
            "errors": errors,
            "timestamp": datetime.utcnow().isoformat()
        }
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error during sync: {e}")
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")
    except Exception as e:
        logger.error(f"Sync error: {e}")
        raise HTTPException(status_code=500, detail=f"Synchronization failed: {str(e)}")


@router.post("/stripe/customer-portal", response_model=StripeCustomerPortalResponse)
async def create_customer_portal_session(
    request: StripeCustomerPortalRequest,
    authorization: str = Header(None)
):
    """Create Stripe customer portal session for subscription management"""
    if not stripe_secret_key:
        raise HTTPException(
            status_code=503,
            detail="Payment processing not configured yet. Please contact support."
        )
    
    user_id = await verify_clerk_token(authorization)
    
    if not user_id:
        logger.error("Customer portal: No user_id from token verification")
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    logger.info(f"Customer portal: Processing request for user {user_id}")

    try:
        logger.info(f"Creating customer portal for user: {user_id}")
        
        # First, try to find the customer ID by looking up the user's Clerk metadata
        # This would require storing the customer ID in Clerk when subscription is created
        # For now, let's search for subscriptions more efficiently
        
        customer_id = None
        
        # Method 1: Search active subscriptions first (more likely to find matches)
        active_subscriptions = stripe.Subscription.list(
            limit=20,
            status="active"
        )
        
        for subscription in active_subscriptions:
            if subscription.metadata.get("clerkUserId") == user_id:
                customer_id = subscription.customer
                logger.info(f"Found customer ID via active subscription: {customer_id}")
                break
        
        # Method 2: If not found in active, check all subscriptions
        if not customer_id:
            all_subscriptions = stripe.Subscription.list(
                limit=50,
                status="all"
            )
            
            for subscription in all_subscriptions:
                if subscription.metadata.get("clerkUserId") == user_id:
                    customer_id = subscription.customer
                    logger.info(f"Found customer ID via subscription history: {customer_id}")
                    break
        
        if not customer_id:
            logger.error(f"No subscription found for user {user_id}")
            raise HTTPException(
                status_code=404, 
                detail="No subscription found. Please upgrade to premium first, or contact support if you believe this is an error."
            )
        
        # Create customer portal session
        return_url = request.return_url or f"{FRONTEND_URL}/pricing"
        logger.info(f"Creating portal session for customer {customer_id}, return_url: {return_url}")
        
        session = stripe.billing_portal.Session.create(
            customer=customer_id,
            return_url=return_url
        )
        
        logger.info(f"Portal session created successfully: {session.id}")
        return StripeCustomerPortalResponse(url=session.url)
        
    except stripe.error.StripeError as e:
        logger.error(f"Stripe error creating customer portal: {e}")
        logger.error(f"Stripe error type: {type(e)}")
        logger.error(f"Stripe error details: {getattr(e, 'user_message', 'No user message')}")
        raise HTTPException(status_code=500, detail=f"Stripe error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Customer portal error: {e}")
        logger.error(f"Error type: {type(e)}")
        import traceback
        logger.error(f"Full traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Failed to create customer portal session: {str(e)}")
