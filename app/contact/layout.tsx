import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Contact | Hours & Location',
  description:
    '聯絡 TaiwanWay — 26 South St, Middletown, NY 10940。電話 845-381-1002。營業時間：週一二五六 11AM-7PM。Contact us for dine-in, takeout & catering.',
  alternates: { canonical: '/contact' },
  openGraph: {
    title: 'Contact TaiwanWay | Hours & Location',
    description: '26 South St, Middletown, NY 10940. Call 845-381-1002. Open Mon/Tue/Fri/Sat 11AM-7PM.',
    url: '/contact',
  },
}

export default function ContactLayout({ children }: { children: React.ReactNode }) {
  return children
}
