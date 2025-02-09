'use client'

import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { useLanguage } from "@/lib/i18n/language-context"
import { useEffect } from "react"
import Image from "next/image"

export default function AboutPage() {
  const { t, language } = useLanguage()
  
  useEffect(() => {
    // 強制重新渲染當語言改變時
    document.documentElement.lang = language
  }, [language])

  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="flex-1">
        {/* Hero Image Section */}
        <section className="relative h-[50vh] min-h-[400px] w-full">
          <Image
            src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_0329-4xKjbDPxXgMadO2d2D81rsDbqYYh6q.jpeg"
            alt="Taiwanway Store Front with Cherry Blossoms"
            fill
            className="object-cover"
            priority
          />
        </section>

        {/* Content Section */}
        <section className="py-12 bg-background">
          <div className="container mx-auto px-4">
            <div className="max-w-3xl mx-auto">
              {/* Title and Description */}
              <div className="text-center mb-8">
                <h1 className="text-4xl md:text-5xl font-bold mb-4">{t('about.title')}</h1>
                <p className="text-xl text-muted-foreground">
                  {t('hero.description')}
                </p>
              </div>

              {/* Story Content */}
              <div className="prose prose-lg">
                <p className="text-lg leading-relaxed">
                  {t('about.story1')}
                </p>
                <p className="text-lg leading-relaxed">
                  {t('about.story2')}
                </p>
                <p className="text-lg leading-relaxed">
                  {t('about.story3')}
                </p>
                <p className="text-lg leading-relaxed font-medium text-primary">
                  {t('about.closing')}
                </p>
              </div>
            </div>
          </div>
        </section>
      </div>
      <Footer />
    </main>
  )
}

