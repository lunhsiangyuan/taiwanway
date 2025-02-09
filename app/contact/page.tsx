'use client'

import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { ContactHero } from "@/components/contact-hero"
import { Contact } from "@/components/contact"
import { useLanguage } from "@/lib/i18n/language-context"
import { useEffect } from "react"

export default function ContactPage() {
  const { language } = useLanguage()

  useEffect(() => {
    // 強制重新渲染當語言改變時
    document.documentElement.lang = language
  }, [language])

  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="flex-1">
        <ContactHero />
        <Contact />
      </div>
      <Footer />
    </main>
  )
}

