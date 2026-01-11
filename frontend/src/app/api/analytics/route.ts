import { NextRequest, NextResponse } from 'next/server';
import { auth, clerkClient } from '@clerk/nextjs/server';

// Simple admin check - you can customize this
const ADMIN_USER_IDS = process.env.ADMIN_USER_IDS?.split(',') || [];

export async function GET(request: NextRequest) {
  try {
    const { userId } = await auth();
    
    // Check if user is admin (optional - remove if you want any signed-in user to see)
    if (!userId || (!ADMIN_USER_IDS.includes(userId) && ADMIN_USER_IDS.length > 0)) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const client = await clerkClient();
    
    // Get all users (paginate if you have many users)
    const users = await client.users.getUserList({ limit: 100 });
    
    // Aggregate analytics
    const analytics = {
      totalUsers: users.totalCount,
      activeToday: 0,
      premiumUsers: 0,
      freeUsers: 0,
      activityBreakdown: {} as Record<string, number>,
      dailyActiveUsers: [] as Array<{ date: string; count: number }>,
      topActivities: [] as Array<{ activity: string; count: number }>,
      conversionRate: 0,
      userDetails: [] as Array<{
        id: string;
        email: string;
        isPremium: boolean;
        lifetimeActions: number;
        lastActivity: string | null;
        activityBreakdown: Record<string, number>;
      }>,
    };

    const today = new Date().toISOString().split('T')[0];

    for (const user of users.data) {
      const metadata = user.publicMetadata || {};
      const isPremium = metadata.isPremium === true || metadata.subscriptionStatus === 'active';
      const lifetimeStats = (metadata.lifetimeStats || {}) as Record<string, number>;
      const usageDate = metadata.usageDate as string | undefined;

      // Count premium vs free
      if (isPremium) {
        analytics.premiumUsers++;
      } else {
        analytics.freeUsers++;
      }

      // Count active today
      if (usageDate === today) {
        analytics.activeToday++;
      }

      // Aggregate activity breakdown
      for (const [activity, count] of Object.entries(lifetimeStats)) {
        if (activity !== 'totalActions') {
          analytics.activityBreakdown[activity] = (analytics.activityBreakdown[activity] || 0) + (count as number);
        }
      }

      // Add user details
      analytics.userDetails.push({
        id: user.id,
        email: user.emailAddresses[0]?.emailAddress || 'N/A',
        isPremium,
        lifetimeActions: (lifetimeStats.totalActions as number) || 0,
        lastActivity: (metadata.lastActivity as string) || null,
        activityBreakdown: lifetimeStats,
      });
    }

    // Sort activities by count
    analytics.topActivities = Object.entries(analytics.activityBreakdown)
      .map(([activity, count]) => ({ activity, count }))
      .sort((a, b) => b.count - a.count);

    // Calculate conversion rate
    if (analytics.totalUsers > 0) {
      analytics.conversionRate = Math.round((analytics.premiumUsers / analytics.totalUsers) * 100);
    }

    // Sort users by activity
    analytics.userDetails.sort((a, b) => b.lifetimeActions - a.lifetimeActions);

    return NextResponse.json(analytics);
  } catch (error) {
    console.error('Error fetching analytics:', error);
    return NextResponse.json(
      { error: 'Failed to fetch analytics' },
      { status: 500 }
    );
  }
}
