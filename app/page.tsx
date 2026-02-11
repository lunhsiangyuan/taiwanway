import { Hero } from "@/components/hero"
import { StorySection } from "@/components/story-section"
import { MenuShowcase } from "@/components/menu-showcase"
import { ContactSection } from "@/components/contact-section"

export default function Home() {
  return (
    <main>
      <Hero />
      <StorySection />
      <MenuShowcase />
      <ContactSection />
    </main>
  )
}
