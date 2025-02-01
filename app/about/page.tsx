import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { About } from "@/components/about"
import { AboutHero } from "@/components/about-hero"

export default function AboutPage() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <AboutHero />
      <About />
      <Footer />
    </main>
  )
}

