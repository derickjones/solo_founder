import { NextRequest, NextResponse } from 'next/server';
import { auth, clerkClient } from '@clerk/nextjs/server';

export async function POST(request: NextRequest) {
  try {
    const { userId } = await auth();
    
    if (!userId) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const { count, date } = await request.json();

    if (typeof count !== 'number' || typeof date !== 'string') {
      return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
    }

    // Update user's public metadata with usage info
    const client = await clerkClient();
    await client.users.updateUserMetadata(userId, {
      publicMetadata: {
        usageCount: count,
        usageDate: date,
      },
    });

    return NextResponse.json({ success: true, count, date });
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
