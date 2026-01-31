import { Header } from "@/components/header"
import { Hero } from "@/components/hero"
import { MenuHighlights } from "@/components/menu-highlights"
import { Footer } from "@/components/footer"
import GroupBuy from "@/components/GroupBuy"

import { BusinessInfoSection } from "@/components/business-info-section"

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <Hero />
      <GroupBuy />
      <BusinessInfoSection />
      <MenuHighlights />
      <Footer />
    </main>
  )
}
