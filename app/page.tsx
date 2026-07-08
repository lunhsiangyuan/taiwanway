import type { Metadata } from 'next'
import { AnnouncementMarquee } from "@/components/announcement-marquee"
import { Hero } from "@/components/hero"

export const metadata: Metadata = {
  title: 'TaiwanWay | Beef Noodle Soup, Boba & Café · Middletown NY',
  description:
    'A Taiwanese café in Middletown, NY 10940 — beef noodle soup, braised pork rice, boba, and comforting flavors from home. Serving Orange County and the Hudson Valley.',
  keywords: [
    'Taiwanese restaurant near me',
    'Middletown NY Taiwanese food',
    'Middletown 10940 restaurants',
    'beef noodle soup Middletown NY',
    'boba Middletown NY',
    'beef noodle soup',
    'braised pork rice',
    'home-style Taiwanese cafe',
    'Orange County NY restaurant',
    'Hudson Valley Taiwanese',
    'boba near me',
    'pineapple cake Hudson Valley',
    '台灣味 紐約',
  ],
  alternates: { canonical: '/' },
  openGraph: {
    title: 'TaiwanWay | Beef Noodle Soup, Boba & Café · Middletown NY',
    description: 'A home-style Taiwanese café in Middletown, NY 10940. Slow-braised beef noodle soup, classic braised pork rice, handcrafted boba, and freshly baked pineapple cakes. Made with care, served with warmth.',
    url: '/',
    images: ['/images/og-cover.jpg'],
  },
}
import { ValueStrip } from "@/components/value-strip"
import { PopularPicks } from "@/components/popular-picks"
import { SnackShowcase } from "@/components/snack-showcase"
import { Testimonials } from "@/components/testimonials"
import { ContactSection } from "@/components/contact-section"
import { TeaBand } from "@/components/tea-band"

export default function Home() {
  return (
    <main id="main-content">
      <AnnouncementMarquee />
      <Hero />
      <ValueStrip />
      <PopularPicks />
      <SnackShowcase />
      <Testimonials />
      <ContactSection />
      <TeaBand />
    </main>
  )
}
