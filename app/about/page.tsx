'use client'

import { useLanguage } from "@/lib/i18n/language-context"
import Image from "next/image"

export default function AboutPage() {
  const { t } = useLanguage()

  return (
    <main id="main-content">
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
            <div className="text-center mb-8">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">{t('about.title')}</h1>
              <p className="text-xl text-muted-foreground">
                {t('hero.description')}
              </p>
            </div>

            <div className="prose prose-lg">
              <p className="text-lg leading-relaxed">{t('about.story1')}</p>
              <p className="text-lg leading-relaxed">{t('about.story2')}</p>
              <p className="text-lg leading-relaxed">{t('about.story3')}</p>
              <p className="text-lg leading-relaxed font-medium text-primary">{t('about.closing')}</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  )
}
