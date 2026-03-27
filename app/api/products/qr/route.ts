import { NextRequest, NextResponse } from 'next/server';
import QRCode from 'qrcode';

const SITE_DOMAIN = 'https://taiwanway.nyc';

export async function GET(request: NextRequest) {
  const slug = request.nextUrl.searchParams.get('slug');
  if (!slug) {
    return NextResponse.json({ error: 'slug is required' }, { status: 400 });
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
