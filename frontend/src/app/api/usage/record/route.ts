import { NextRequest, NextResponse } from 'next/server';
import { auth, clerkClient } from '@clerk/nextjs/server';

// Activity types for analytics
type ActivityType = 
  | 'qa_question'
  | 'study_guide'
  | 'audio_summary'
  | 'tile_click'
  | 'podcast_play'
  | 'lesson_plan'
  | 'core_content'
  | 'daily_thought';

interface ActivityLog {
  type: ActivityType;
  timestamp: string;
  metadata?: Record<string, string>;
}

export async function POST(request: NextRequest) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { count, date, activity, isPremium } = await request.json();

    if (typeof count !== 'number' || typeof date !== 'string') {
      return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
    }

    // Get current user metadata
    const client = await clerkClient();
    const user = await client.users.getUser(userId);
    
    // Get existing activities for today, or start fresh
    const existingDate = user.publicMetadata?.usageDate as string | undefined;
    let activities: ActivityLog[] = [];
    
    if (existingDate === date && user.publicMetadata?.activities) {
      activities = user.publicMetadata.activities as ActivityLog[];
    }
    
    // Add new activity if provided
    if (activity) {
      activities.push(activity as ActivityLog);
    }

    // Also track lifetime stats (doesn't reset daily)
    const lifetimeStats = (user.publicMetadata?.lifetimeStats || {}) as Record<string, number>;
    if (activity?.type) {
      lifetimeStats[activity.type] = (lifetimeStats[activity.type] || 0) + 1;
      lifetimeStats.totalActions = (lifetimeStats.totalActions || 0) + 1;
    }

    // Update user's public metadata with usage info
    await client.users.updateUserMetadata(userId, {
      publicMetadata: {
        ...user.publicMetadata,
        usageCount: count,
        usageDate: date,
        activities,
        lifetimeStats,
        lastActivity: new Date().toISOString(),
      },
    });

    return NextResponse.json({ success: true, count, date, activitiesCount: activities.length });
  } catch (error) {
    console.error('Error recording usage:', error);
    return NextResponse.json(
      { error: 'Failed to record usage' },
      { status: 500 }
    );
  }
}

// GET endpoint to fetch current usage (optional, for syncing)
export async function GET() {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const client = await clerkClient();
    const user = await client.users.getUser(userId);
    
    const today = new Date().toISOString().split('T')[0];
    const usageDate = user.publicMetadata?.usageDate as string | undefined;
    const usageCount = user.publicMetadata?.usageCount as number | undefined;
    
    // Reset if it's a new day
    if (usageDate !== today) {
      return NextResponse.json({ count: 0, date: today });
    }

    return NextResponse.json({ 
      count: usageCount || 0, 
      date: usageDate || today 
    });
  } catch (error) {
    console.error('Error fetching usage:', error);
    return NextResponse.json(
      { error: 'Failed to fetch usage' },
      { status: 500 }
    );
  }
}
