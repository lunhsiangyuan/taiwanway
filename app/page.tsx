import { Header } from "@/components/header"
import { Hero } from "@/components/hero"
import { MenuHighlights } from "@/components/menu-highlights"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <Hero />
      <MenuHighlights />
      <Footer />
    </main>
  )
}
