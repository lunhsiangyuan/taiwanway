'use client'

import { useLanguage } from "@/lib/i18n/language-context"

export function About() {
  const { t } = useLanguage()

  return (
    <section className="py-20 bg-secondary/30" id="about">
      <div className="container px-4 md:px-6">
        <h2 className="text-3xl font-bold mb-8 text-center">{t('about.title')}</h2>
        <div className="max-w-4xl mx-auto space-y-6">
          <p className="text-lg text-muted-foreground">
            {t('about.story1')}
          </p>
          <p className="text-lg text-muted-foreground">
            {t('about.story2')}
          </p>
          <p className="text-lg text-muted-foreground">
            {t('about.story3')}
          </p>
          <p className="text-lg font-semibold">
            {t('about.closing')}
          </p>
        </div>
      </div>
    </section>
  )
}

