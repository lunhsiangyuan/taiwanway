import { NextRequest, NextResponse } from 'next/server';
import { verifyPassword } from '@/lib/auth';

export async function POST(request: NextRequest) {
  const pw = request.headers.get('x-admin-password') || '';
  if (verifyPassword(pw)) {
    return NextResponse.json({ ok: true });
  }
  return NextResponse.json({ error: 'Invalid password' }, { status: 401 });
}
