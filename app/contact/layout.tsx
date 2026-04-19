import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Contact | Hours & Location',
  description:
    '聯絡 TaiwanWay — 26 South St, Middletown, NY 10940。電話 845-381-1002。營業時間：週一二五六 11AM-7PM。Contact us for dine-in, takeout & catering.',
  keywords: [
    'TaiwanWay address',
    'TaiwanWay phone',
    'Middletown NY restaurant hours',
    '26 South St Middletown',
    'Taiwanese restaurant phone number',
    'takeout Middletown NY',
    'dine-in Taiwanese Middletown',
    '845-381-1002',
    '台灣味 地址',
    '台灣味 電話',
  ],
  alternates: { canonical: '/contact' },
  openGraph: {
    title: 'Contact TaiwanWay | Hours & Location',
    description: '26 South St, Middletown, NY 10940. Call 845-381-1002. Open Mon/Tue/Fri/Sat 11AM-7PM.',
    url: '/contact',
    images: ['/images/og-storefront.jpg'],
  },
}

export default function ContactLayout({ children }: { children: React.ReactNode }) {
  return children
}
