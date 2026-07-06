'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import Image from 'next/image'

export function StorySection() {
  const { language } = useLanguage()

  const quote = language === 'zh'
    ? '「門推開，就像回到台灣的家。」'
    : language === 'es'
      ? '"Abre la puerta — sabe a casa, en taiwanés."'
      : '"Open the door — it tastes like home, in Taiwanese."'

  const altInterior = language === 'zh'
    ? '台式咖啡廳座位區 — 吊燈、壁爐、台灣商品架（Middletown, NY）'
    : language === 'es'
      ? 'Área de asientos del café taiwanés con candelabro y chimenea en Middletown, NY'
      : 'Taiwanese café seating area with chandelier, fireplace and Taiwan shelves in Middletown, NY'

  const altStore = language === 'zh'
    ? 'TaiwanWay 店門口 — 26 South St, Middletown NY 的紅磚歷史建築'
    : language === 'es'
      ? 'Fachada de TaiwanWay — edificio histórico de ladrillo rojo en 26 South St, Middletown NY'
      : 'TaiwanWay storefront — historic red-brick building at 26 South St, Middletown NY'

  return (
    <section className="bg-[#FAF7F2] py-16 md:py-20">
      <div className="mx-auto max-w-5xl px-6 md:px-4">
        {/* 引言（置中） */}
        <blockquote className="mx-auto max-w-2xl text-center">
          <p className="font-heading text-2xl italic leading-relaxed text-[#2D1810] md:text-3xl">
            {quote}
          </p>
        </blockquote>

        {/* 兩張店照並排 */}
        <div className="mt-10 grid gap-5 sm:grid-cols-2 md:mt-12 md:gap-6">
          <div className="relative aspect-[4/3] overflow-hidden rounded-2xl shadow-lg ring-1 ring-black/5">
            <Image
              src="/images/cafe-interior-seating.jpg"
              alt={altInterior}
              fill
              className="object-cover"
              sizes="(max-width: 640px) 100vw, 50vw"
            />
          </div>
          <div className="relative aspect-[4/3] overflow-hidden rounded-2xl shadow-lg ring-1 ring-black/5">
            <Image
              src="/images/storefront.jpg"
              alt={altStore}
              fill
              className="object-cover"
              sizes="(max-width: 640px) 100vw, 50vw"
            />
          </div>
        </div>
      </div>
    </section>
  )
}
