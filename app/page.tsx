import { Header } from "@/components/header"
import { Hero } from "@/components/hero"
import { MenuHighlights } from "@/components/menu-highlights"
import { Contact } from "@/components/contact"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <Hero />
      <MenuHighlights />
      <Contact />
      <Footer />
    </main>
  )
}

