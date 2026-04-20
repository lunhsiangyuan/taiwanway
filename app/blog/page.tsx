import type { Metadata } from 'next'
import { BLOG_POSTS } from './posts'
import { BlogIndexClient } from './blog-index-client'

export const metadata: Metadata = {
  title: 'Blog — Taiwanese Food Stories from Middletown, NY',
  description:
    'Stories about Taiwanese tea, food, and craft behind TaiwanWay in Middletown, NY. Why native pineapple, why winter melon, how our bubble tea differs from the rest.',
  alternates: { canonical: 'https://taiwanwayny.com/blog' },
  openGraph: {
    title: 'TaiwanWay Blog — Taiwanese Food Stories',
    description:
      'The why behind our menu — pineapple cake, bubble tea, beef noodle soup, and more.',
    url: 'https://taiwanwayny.com/blog',
  },
}

export default function BlogIndexPage() {
  const blogListJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Blog',
    '@id': 'https://taiwanwayny.com/blog#blog',
    name: 'TaiwanWay Blog',
    description:
      'Stories behind TaiwanWay\u2019s menu — Taiwanese tea, food, and craft, from Middletown, NY.',
    url: 'https://taiwanwayny.com/blog',
    publisher: { '@id': 'https://taiwanwayny.com/#organization' },
    blogPost: BLOG_POSTS.map((p) => ({
      '@type': 'BlogPosting',
      headline: p.title.en,
      datePublished: p.date,
      url: `https://taiwanwayny.com/blog/${p.slug}`,
      image: `https://taiwanwayny.com${p.coverImage}`,
    })),
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(blogListJsonLd) }}
      />
      <BlogIndexClient />
    </>
  )
}
