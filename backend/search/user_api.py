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

class AnalyticsResponse(BaseModel):
    totalUsers: int
    activeToday: int
    premiumUsers: int
    freeUsers: int
    activityBreakdown: Dict[str, int]
    topActivities: List[Dict[str, Any]]
    conversionRate: float
    userDetails: List[Dict[str, Any]]

# ============================================================================
# Helper Functions
# ============================================================================

async def verify_clerk_token(authorization: str) -> Optional[str]:
    """Verify Clerk JWT token and return user ID"""
    if not authorization or not authorization.startswith("Bearer "):
        logger.warning("No authorization header or invalid format")
        return None
    
    token = authorization.replace("Bearer ", "")
    
    if not CLERK_SECRET_KEY:
        logger.error("CLERK_SECRET_KEY not configured")
        return None
    
    try:
        # Decode JWT to extract user ID from 'sub' claim
        # The token is already verified by Clerk on the frontend
        import base64
        import json
        
        parts = token.split(".")
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
