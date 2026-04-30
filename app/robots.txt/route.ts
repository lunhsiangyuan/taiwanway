/**
 * Custom robots.txt route handler.
 *
 * Replaces the Next.js metadata `robots.ts` so we can emit non-standard
 * directives like Content-Signal (https://contentsignals.org/) which the
 * structured MetadataRoute.Robots API cannot represent.
 */

export const dynamic = 'force-static'
export const revalidate = 86400 // 24 h

export function GET() {
  const lines = [
    '# robots.txt for taiwanwayny.com',
    '# TaiwanWay 臺灣味 — home-style Taiwanese café in Middletown, NY 10940',
    '',
    'User-agent: *',
    'Allow: /',
    'Disallow: /api/',
    'Disallow: /_next/',
    'Disallow: /admin/',
    '',
    '# Content Signals — declared AI/search usage preferences',
    '# https://contentsignals.org/  |  draft-romm-aipref-contentsignals',
    'Content-Signal: search=yes, ai-train=yes, ai-input=yes',
    '',
    '# Sitemaps & AI-friendly summary',
    'Sitemap: https://taiwanwayny.com/sitemap.xml',
    '',
  ]
  return new Response(lines.join('\n'), {
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=3600, s-maxage=86400',
    },
  })
}
