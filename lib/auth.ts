import { NextRequest, NextResponse } from 'next/server';
import { timingSafeEqual, createHash } from 'crypto';

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD || '';

function hashString(s: string): Buffer {
  return createHash('sha256').update(s).digest();
}

/** 安全比較密碼（防 timing attack） */
export function verifyPassword(input: string): boolean {
  if (!ADMIN_PASSWORD || !input) return false;
  const a = hashString(input);
  const b = hashString(ADMIN_PASSWORD);
  return timingSafeEqual(a, b);
}

/** 從 request header 驗證 admin 身份 */
export function isAdmin(request: NextRequest): boolean {
  const pw = request.headers.get('x-admin-password') || '';
  return verifyPassword(pw);
}

/** 回傳 401 response */
export function unauthorizedResponse(): NextResponse {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
}
