import { NextRequest, NextResponse } from 'next/server';

interface FeedbackData {
  type: 'bug' | 'feature' | 'general' | 'praise';
  message: string;
  email: string | null;
  userId: string | null;
  userName: string | null;
}

export async function POST(request: NextRequest) {
  try {
    const data: FeedbackData = await request.json();

    if (!data.message || !data.type) {
      return NextResponse.json(
        { error: 'Missing required fields' },
        { status: 400 }
      );
    }

    // Log feedback - visible in Vercel logs
    const feedback = {
      ...data,
      timestamp: new Date().toISOString(),
    };

    console.log('📨 FEEDBACK:', JSON.stringify(feedback));

    return NextResponse.json({ 
      success: true, 
      message: 'Feedback submitted successfully',
    });
  } catch (error) {
    console.error('Error processing feedback:', error);
    return NextResponse.json(
      { error: 'Failed to process feedback' },
      { status: 500 }
    );
  }
}
