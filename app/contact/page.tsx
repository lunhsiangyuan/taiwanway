import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { ContactHero } from "@/components/contact-hero"
import { ContactInfo } from "@/components/contact-info"
import { ContactMap } from "@/components/contact-map"

export default function ContactPage() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <ContactHero />
      <ContactInfo />
      <ContactMap />
      <Footer />
    </main>
  )
}

