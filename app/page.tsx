import type { Metadata } from 'next'
import { Hero } from "@/components/hero"

export const metadata: Metadata = {
  title: 'TaiwanWay | Taiwanese Street Bowls · Bubble Tea · Bakery in Middletown, NY',
  description:
    'A Taiwanese café in Middletown, NY 10940 — beef noodle soup, braised pork rice, bubble tea, and comforting flavors from home. Serving Orange County and the Hudson Valley.',
  keywords: [
    'Taiwanese restaurant near me',
    'Middletown NY Taiwanese food',
    'Middletown 10940 restaurants',
    'Taiwan Street Bowls',
    'bubble tea Middletown',
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
    title: 'TaiwanWay | Taiwanese Street Bowls · Bubble Tea · Bakery in Middletown, NY',
    description: 'A home-style Taiwanese café in Middletown, NY 10940. Slow-braised beef noodle soup, classic braised pork rice, handcrafted bubble tea, and freshly baked pineapple cakes. Made with care, served with warmth.',
    url: '/',
    images: ['/images/og-cover.jpg'],
  },
}
import { StorySection } from "@/components/story-section"
import { MenuShowcase } from "@/components/menu-showcase"
import { SnackShop } from "@/components/snack-shop"
import { Testimonials } from "@/components/testimonials"
import { ContactSection } from "@/components/contact-section"

export default function Home() {
  return (
    <main id="main-content">
      <Hero />
      <StorySection />
      <MenuShowcase />
      <SnackShop />
      <Testimonials />
      <ContactSection />
    </main>
  )
}
