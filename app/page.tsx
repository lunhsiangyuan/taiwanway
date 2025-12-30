import { Header } from "@/components/header"
import { Hero } from "@/components/hero"
import { MenuHighlights } from "@/components/menu-highlights"
import { Footer } from "@/components/footer"

import { BusinessInfoSection } from "@/components/business-info-section"

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <Hero />
      <BusinessInfoSection />
      <MenuHighlights />
      <Footer />
    </main>
  )
}
