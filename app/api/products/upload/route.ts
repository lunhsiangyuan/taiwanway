import { NextRequest, NextResponse } from 'next/server';
import { put } from '@vercel/blob';
import { isAdmin, unauthorizedResponse } from '@/lib/auth';

export async function POST(request: NextRequest) {
  if (!isAdmin(request)) return unauthorizedResponse();

  const formData = await request.formData();
  const file = formData.get('file') as File | null;

  if (!file) {
    return NextResponse.json({ error: 'No file provided' }, { status: 400 });
  }

  // Validate file type
  const validTypes = ['image/jpeg', 'image/png', 'image/webp'];
  if (!validTypes.includes(file.type)) {
    return NextResponse.json(
      { error: 'Invalid file type. Use JPEG, PNG, or WebP.' },
      { status: 400 }
    );
  }

  // Max 5MB
  if (file.size > 5 * 1024 * 1024) {
    return NextResponse.json({ error: 'File too large (max 5MB)' }, { status: 400 });
  }

  try {
    const timestamp = Date.now();
    const ext = file.name.split('.').pop() || 'jpg';
    const filename = `products/${timestamp}.${ext}`;

    // @vercel/blob v1 起 addRandomSuffix 預設改為 false，且同路徑重複上傳
    // 會直接丟錯（需 allowOverwrite）。這裡明確帶 true，維持升級前的行為，
    // 同時避免同一毫秒內兩筆上傳撞檔名而失敗。
    const blob = await put(filename, file, {
      access: 'public',
      contentType: file.type,
      addRandomSuffix: true,
    });

    return NextResponse.json({ url: blob.url });
  } catch (err) {
    console.error('Error uploading file:', err);
    return NextResponse.json(
      { error: err instanceof Error ? err.message : 'Upload failed' },
      { status: 500 }
    );
  }
}
