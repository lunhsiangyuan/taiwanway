import { NextRequest, NextResponse } from 'next/server';
import QRCode from 'qrcode';
import { isValidSlug } from '@/types/product';
import { getSupabaseClient } from '@/lib/supabase';

const SITE_DOMAIN = 'https://taiwanwayny.com';

export async function GET(request: NextRequest) {
  const slug = request.nextUrl.searchParams.get('slug');
  if (!slug) {
    return NextResponse.json({ error: 'slug is required' }, { status: 400 });
  }

  if (!isValidSlug(slug)) {
    return NextResponse.json({ error: 'Invalid slug format' }, { status: 400 });
  }

  // 驗證產品存在
  const supabase = getSupabaseClient(false);
  const { data: product } = await supabase
    .from('products')
    .select('slug')
    .eq('slug', slug)
    .eq('is_active', true)
    .single();

  if (!product) {
    return NextResponse.json({ error: 'Product not found' }, { status: 404 });
  }

  try {
    const url = `${SITE_DOMAIN}/product/${slug}`;
    const qrBuffer = await QRCode.toBuffer(url, {
      type: 'png',
      width: 400,
      margin: 2,
      color: { dark: '#000000', light: '#FFFFFF' },
      errorCorrectionLevel: 'M',
    });

    return new NextResponse(qrBuffer, {
      headers: {
        'Content-Type': 'image/png',
        'Content-Disposition': `inline; filename="qr-${slug}.png"`,
        'Cache-Control': 'public, max-age=86400',
      },
    });
  } catch (err) {
    console.error('Error generating QR code:', err);
    return NextResponse.json(
      { error: err instanceof Error ? err.message : 'QR generation failed' },
      { status: 500 }
    );
  }
}
