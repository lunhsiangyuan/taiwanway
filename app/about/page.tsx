'use client'

import { useLanguage } from "@/lib/i18n/language-context"
import Image from "next/image"
import { StorySection } from "@/components/story-section"

export default function AboutPage() {
  const { t } = useLanguage()

  return (
    <main id="main-content">
      {/* Hero Image Section */}
      <section className="relative h-[50vh] min-h-[360px] w-full">
        <Image
          src="/images/store/about-hero.png"
          alt="TaiwanWay 店內空間 — 溫暖的午後茶席，Middletown, NY 的家鄉味台式咖啡館"
          fill
          className="object-cover"
          priority
          sizes="100vw"
        />
      </section>

      {/* Content Section */}
      <section className="py-16 md:py-20 bg-background">
        <div className="container mx-auto px-4">
          <div className="max-w-2xl mx-auto">
            <div className="text-center mb-10">
              <h1 className="font-heading text-3xl md:text-4xl font-bold text-foreground mb-6 tracking-tight">
                {t('about.title')}
              </h1>
              <p className="font-body text-base md:text-lg text-muted-foreground leading-relaxed">
                {t('hero.description')}
              </p>
            </div>

            <div className="space-y-5 font-body">
              <p className="text-base md:text-[1.0625rem] leading-relaxed text-foreground/85">{t('about.story1')}</p>
              <p className="text-base md:text-[1.0625rem] leading-relaxed text-foreground/85">{t('about.story2')}</p>
              <p className="text-base md:text-[1.0625rem] leading-relaxed text-foreground/85">{t('about.story3')}</p>
              <p className="text-base md:text-[1.0625rem] leading-relaxed font-semibold text-primary pt-2">{t('about.closing')}</p>
            </div>
          </div>
        </div>
      </section>

      {/* 我們的故事（由首頁移來） */}
      <StorySection />
    </main>
  )
}
