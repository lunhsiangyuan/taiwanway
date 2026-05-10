import type { Metadata } from 'next'
import { Hero } from "@/components/hero"

export const metadata: Metadata = {
  title: 'TaiwanWay | Taiwanese Café & Bubble Tea in Middletown, NY',
  description:
    'A Taiwanese café in Middletown, NY serving beef noodle soup, braised pork rice, Taiwanese bubble tea, desserts, and comforting flavors from home.',
  keywords: [
    'Taiwanese restaurant near me',
    'Middletown NY Taiwanese food',
    'bubble tea Middletown',
    'beef noodle soup',
    'braised pork rice',
    'authentic Taiwanese cuisine',
    'Orange County NY restaurant',
    'Hudson Valley Asian food',
    'boba near me',
    '台灣味 紐約',
  ],
  alternates: { canonical: '/' },
  openGraph: {
    title: 'TaiwanWay | Taiwanese Café & Bubble Tea in Middletown, NY',
    description: 'A Taiwanese café in Middletown, NY serving beef noodle soup, braised pork rice, Taiwanese bubble tea, desserts, and comforting flavors from home.',
    url: '/',
    images: ['/images/og-storefront.jpg'],
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
