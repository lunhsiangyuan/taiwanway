import type { Metadata } from 'next'
import { Hero } from "@/components/hero"

export const metadata: Metadata = {
  title: 'TaiwanWay | Authentic Taiwanese Cuisine in Middletown, NY',
  description:
    'TaiwanWay 臺灣味 — 紐約 Middletown 正宗臺灣料理。招牌牛肉麵、滷肉飯、珍珠奶茶、鳳梨酥。Visit us at 26 South St, Middletown, NY 10940.',
  alternates: { canonical: '/' },
  openGraph: {
    title: 'TaiwanWay | Authentic Taiwanese Cuisine in Middletown, NY',
    description: 'Authentic Taiwanese beef noodles, braised pork rice, bubble tea & pineapple cakes. 26 South St, Middletown, NY 10940.',
    url: '/',
  },
}
import { StorySection } from "@/components/story-section"
import { MenuShowcase } from "@/components/menu-showcase"
import { Testimonials } from "@/components/testimonials"
import { ContactSection } from "@/components/contact-section"

export default function Home() {
  return (
    <main id="main-content">
      <Hero />
      <StorySection />
      <MenuShowcase />
      <Testimonials />
      <ContactSection />
    </main>
  )
}
