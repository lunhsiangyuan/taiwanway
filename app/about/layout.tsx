import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'About Us | Our Story',
  description:
    'TaiwanWay 的故事 — 從臺灣到紐約 Middletown，將正宗臺灣味帶到 Hudson Valley。Our story of bringing authentic Taiwanese cuisine to Middletown, NY.',
  alternates: { canonical: '/about' },
  openGraph: {
    title: 'About TaiwanWay | Our Story',
    description: 'From Taiwan to Middletown, NY — our journey of bringing authentic Taiwanese cuisine to Hudson Valley.',
    url: '/about',
  },
}

export default function AboutLayout({ children }: { children: React.ReactNode }) {
  return children
}
