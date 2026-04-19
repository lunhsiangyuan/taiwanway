import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Catering & Group Orders',
  description:
    'TaiwanWay 企業團餐與團購服務。適合公司聚餐、活動派對、節慶團購。Catering for corporate events, parties & group orders in Middletown, NY.',
  keywords: [
    'Taiwanese catering Middletown NY',
    'corporate catering Orange County NY',
    'Asian catering Hudson Valley',
    'group orders Taiwanese food',
    'party catering Middletown',
    'office lunch catering NY',
    'event catering TaiwanWay',
    '台灣料理 外燴',
    '公司團餐 紐約',
  ],
  alternates: { canonical: '/catering' },
  openGraph: {
    title: 'Catering & Group Orders | TaiwanWay',
    description: 'Corporate catering, party packages & holiday group orders. Authentic Taiwanese cuisine for your next event in Middletown, NY.',
    url: '/catering',
    images: ['/images/og-storefront.jpg'],
  },
}

export default function CateringLayout({ children }: { children: React.ReactNode }) {
  return children
}
