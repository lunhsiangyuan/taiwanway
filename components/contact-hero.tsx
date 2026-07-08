'use client'

import Image from 'next/image'
import { useLanguage } from '@/lib/i18n/language-context'

export function ContactHero() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  const title = lang === 'zh' ? '與我們聯繫' : lang === 'es' ? 'Contáctanos' : 'Get in Touch'
  const sub = lang === 'zh' ? '來坐坐，喝杯茶' : lang === 'es' ? 'Ven a visitarnos' : 'Come say hello'

  return (
    <section className="relative h-[42vh] min-h-[320px] w-full overflow-hidden">
      <Image
        src="/images/store/exterior.jpg"
        alt="TaiwanWay 店門口 — 26 South St, Middletown, NY"
        fill
        priority
        className="object-cover"
        sizes="100vw"
      />
      <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-black/25 to-black/10" />
      <div className="relative z-10 flex h-full flex-col items-center justify-end px-4 pb-10 text-center">
        <p className="mb-1 font-heading text-sm uppercase tracking-[0.28em] text-white/85">Middletown, NY</p>
        <h1 className="font-heading text-4xl font-bold text-white drop-shadow-md md:text-5xl">{title}</h1>
        <p className="mt-2 font-heading text-lg italic text-white/90">{sub}</p>
      </div>
    </section>
  )
}
