import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us | Our Story',
  description:
    'TaiwanWay 的故事 — 從臺灣到紐約 Middletown，將正宗臺灣味帶到 Hudson Valley。Our story of bringing authentic Taiwanese cuisine to Middletown, NY.',
  keywords: [
    'TaiwanWay story',
    'Taiwanese restaurant history',
    'authentic Taiwanese Middletown',
    'family-owned Taiwanese restaurant',
    'Taiwan to New York',
    'Hudson Valley Taiwanese chef',
    '台灣味 故事',
    '台灣餐廳 紐約',
  ],
  alternates: { canonical: '/about' },
  openGraph: {
    title: 'About TaiwanWay | Our Story',
    description: 'From Taiwan to Middletown, NY — our journey of bringing authentic Taiwanese cuisine to Hudson Valley.',
    url: '/about',
    images: ['/images/og-storefront.jpg'],
  },
}

export default function AboutLayout({ children }: { children: React.ReactNode }) {
  return children
}
