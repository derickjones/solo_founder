import { NextRequest, NextResponse } from 'next/server';
import { auth } from '@clerk/nextjs/server';

export async function POST(request: NextRequest) {
  try {
    // Get user session from Clerk
    const { getToken } = await auth();
    const token = await getToken();
    
    if (!token) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    // Forward the request to our backend
    const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'https://gospel-app-backend-273320302933.us-central1.run.app';
    
    console.log('[customer-portal] Making request to backend:', `${API_BASE_URL}/api/stripe/customer-portal`);
    console.log('[customer-portal] Using token:', token ? 'present' : 'missing');
    
    const body = await request.json();
    
    const response = await fetch(`${API_BASE_URL}/api/stripe/customer-portal`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        return_url: body.return_url || `${request.nextUrl.origin}/pricing`,
      }),
    });

    const data = await response.json();
    
    if (!response.ok) {
      console.error('[customer-portal] Backend error:', data);
      return NextResponse.json(data, { status: response.status });
    }

    return NextResponse.json(data);
  } catch (error) {
    console.error('[customer-portal] Error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}