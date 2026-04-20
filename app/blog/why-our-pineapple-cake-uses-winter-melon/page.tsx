import type { Metadata } from 'next'
import { BreadcrumbJsonLd } from '@/components/json-ld'
import { getPostBySlug } from '../posts'
import { PineappleCakePostClient } from './post-client'

const SLUG = 'why-our-pineapple-cake-uses-winter-melon'
const post = getPostBySlug(SLUG)!

export const metadata: Metadata = {
  title: post.title.en,
  description: post.excerpt.en,
  keywords: [
    'Taiwanese pineapple cake',
    'authentic pineapple cake',
    'winter melon filling',
    '土鳳梨酥',
    '鳳梨酥內餡',
    'pineapple cake Middletown NY',
    'traditional pineapple cake',
    'native Taiwanese pineapple',
    'fèng lí sū',
  ],
  alternates: { canonical: `https://taiwanwayny.com/blog/${SLUG}` },
  openGraph: {
    type: 'article',
    title: post.title.en,
    description: post.excerpt.en,
    url: `https://taiwanwayny.com/blog/${SLUG}`,
    publishedTime: `${post.date}T12:00:00-04:00`,
    authors: ['TaiwanWay'],
    images: [
      {
        url: post.coverImage,
        alt: 'TaiwanWay hand-made Taiwanese pineapple cake (鳳梨酥) with native pineapple and winter melon filling',
      },
    ],
  },
}

export default function PineappleCakePost() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    '@id': `https://taiwanwayny.com/blog/${SLUG}#article`,
    headline: post.title.en,
    alternativeHeadline: post.title.zh,
    description: post.excerpt.en,
    datePublished: `${post.date}T12:00:00-04:00`,
    dateModified: `${post.date}T12:00:00-04:00`,
    inLanguage: ['en-US', 'zh-TW', 'es'],
    author: {
      '@type': 'Organization',
      name: 'TaiwanWay',
      url: 'https://taiwanwayny.com',
    },
    publisher: { '@id': 'https://taiwanwayny.com/#organization' },
    mainEntityOfPage: `https://taiwanwayny.com/blog/${SLUG}`,
    image: `https://taiwanwayny.com${post.coverImage}`,
    keywords: post.tags.join(', '),
    articleSection: 'Food & Craft',
    about: {
      '@type': 'Thing',
      name: 'Taiwanese Pineapple Cake (鳳梨酥)',
    },
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <BreadcrumbJsonLd
        items={[
          { name: 'Home', url: 'https://taiwanwayny.com' },
          { name: 'Blog', url: 'https://taiwanwayny.com/blog' },
          { name: post.title.en, url: `https://taiwanwayny.com/blog/${SLUG}` },
        ]}
      />
      <PineappleCakePostClient />
    </>
  )
}
