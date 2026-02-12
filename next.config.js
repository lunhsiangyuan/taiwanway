/** @type {import('next').NextConfig} */
const nextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: 'https',
        hostname: 'hebbkx1anhila5yf.public.blob.vercel-storage.com',
      },
      {
        protocol: 'https',
        hostname: '06jfzz4maekxll04.public.blob.vercel-storage.com',
      },
      {
        protocol: 'https',
        hostname: 'www.ganjingworld.com',
      },
    ],
  },
  async headers() {
    return [
      {
        source: '/(.*)',
        headers: [
          {
            key: 'X-Frame-Options',
            value: 'DENY',
          },
          {
            key: 'X-Content-Type-Options',
            value: 'nosniff',
          },
          {
            key: 'Referrer-Policy',
            value: 'strict-origin-when-cross-origin',
          },
          {
            key: 'Permissions-Policy',
            value: 'camera=(), microphone=(), geolocation=(self)',
          },
          {
            key: 'Content-Security-Policy',
            value: [
              "default-src 'self'",
              "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://www.googletagmanager.com https://www.google-analytics.com https://connect.facebook.net https://static.hotjar.com https://*.hotjar.com",
              "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
              "img-src 'self' data: blob: https://*.public.blob.vercel-storage.com https://www.ganjingworld.com https://www.facebook.com https://www.google-analytics.com",
              "font-src 'self' https://fonts.gstatic.com",
              "frame-src https://www.google.com https://www.googletagmanager.com",
              "connect-src 'self' https://www.google-analytics.com https://*.analytics.google.com https://*.hotjar.com https://www.facebook.com https://*.hotjar.io wss://*.hotjar.com",
            ].join('; '),
          },
        ],
      },
    ];
  },
};

module.exports = nextConfig;
