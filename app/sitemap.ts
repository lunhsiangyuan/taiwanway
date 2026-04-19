import type { MetadataRoute } from 'next'

const BASE_URL = 'https://taiwanwayny.com'

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const staticRoutes: MetadataRoute.Sitemap = [
    {
      url: BASE_URL,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 1.0,
      alternates: {
        languages: {
          en: BASE_URL,
          'zh-TW': BASE_URL,
          es: BASE_URL,
        },
      },
    },
    {
      url: `${BASE_URL}/menu`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.9,
    },
    {
      url: `${BASE_URL}/products`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.85,
    },
    {
      url: `${BASE_URL}/catering`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/faq`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${BASE_URL}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    {
      url: `${BASE_URL}/contact`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
  ]

  // Product detail pages — fetch published slugs from API
  const productRoutes: MetadataRoute.Sitemap = []
  try {
    const res = await fetch(`${BASE_URL}/api/products`, {
      next: { revalidate: 3600 },
    })
    if (res.ok) {
      const products = (await res.json()) as Array<{ slug?: string; updated_at?: string }>
      for (const p of products) {
        if (!p.slug) continue
        productRoutes.push({
          url: `${BASE_URL}/product/${p.slug}`,
          lastModified: p.updated_at ? new Date(p.updated_at) : new Date(),
          changeFrequency: 'monthly',
          priority: 0.6,
        })
      }
    }
  } catch {
    // Silent fail — sitemap stays static if API unavailable at build time
  }

  return [...staticRoutes, ...productRoutes]
}
