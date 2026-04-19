import type { Metadata } from 'next'
import { FaqClient } from './faq-client'
import { faqs } from './faqs'
import { BreadcrumbJsonLd } from '@/components/json-ld'

export const metadata: Metadata = {
  title: 'FAQ — Frequently Asked Questions',
  description:
    'Common questions about TaiwanWay 臺灣味 — hours, location, menu, delivery, catering, and more. Authentic Taiwanese restaurant in Middletown, NY.',
  alternates: {
    canonical: 'https://taiwanwayny.com/faq',
  },
  openGraph: {
    title: 'TaiwanWay FAQ — Hours, Menu, Delivery, Catering',
    description:
      'Answers to common questions about TaiwanWay — the Taiwanese restaurant at 26 South St, Middletown, NY.',
    url: 'https://taiwanwayny.com/faq',
  },
}

export default function FaqPage() {
  const faqPageJsonLd = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    '@id': 'https://taiwanwayny.com/faq#faqpage',
    mainEntity: faqs.map((f) => ({
      '@type': 'Question',
      name: f.q_en,
      acceptedAnswer: {
        '@type': 'Answer',
        text: f.a_en,
      },
    })),
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqPageJsonLd) }}
      />
      <BreadcrumbJsonLd
        items={[
          { name: 'Home', url: 'https://taiwanwayny.com' },
          { name: 'FAQ', url: 'https://taiwanwayny.com/faq' },
        ]}
      />
      <FaqClient />
    </>
  )
}
