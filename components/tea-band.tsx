'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import Image from 'next/image'

export function TeaBand() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  const tagline = lang === 'zh' ? '慢下來，喝杯茶。' : lang === 'es' ? 'Baja el ritmo. Toma un té.' : 'Slow down. Stay for tea.'

  return (
    <section className="relative w-full">
      <div className="relative h-[280px] w-full overflow-hidden sm:h-[360px] md:h-[460px]">
        <Image
          src="/images/store/tea-pour.png"
          alt={lang === 'zh' ? '手沖台灣高山茶 — 溫暖的茶席時光' : 'Pouring Taiwanese mountain tea — a warm tea moment'}
          fill
          className="object-cover object-center"
          sizes="100vw"
          quality={85}
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />
        <div className="absolute inset-x-0 bottom-0 flex justify-center pb-8 md:pb-12">
          <p className="font-heading text-2xl italic text-white drop-shadow-md md:text-3xl">{tagline}</p>
        </div>
      </div>
    </section>
  )
}
