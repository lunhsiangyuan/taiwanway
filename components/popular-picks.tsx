'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import Link from 'next/link'
import Image from 'next/image'

type Card = { img: string; alt: Record<string, string> }

const cards: Card[] = [
  { img: '/images/menu-cards/beef-noodle-sq.png', alt: { zh: '牛肉麵', en: 'Beef Noodle Soup', es: 'Sopa de fideos con res' } },
  { img: '/images/menu-cards/pork-rice-sq.png', alt: { zh: '滷肉飯', en: 'Braised Pork Rice', es: 'Arroz con cerdo' } },
  { img: '/images/menu-cards/bubble-tea-sq.png', alt: { zh: '黑糖珍珠鮮奶', en: 'Brown Sugar Bubble Milk', es: 'Té de burbujas' } },
  { img: '/images/menu-cards/dessert-sq.png', alt: { zh: '甜點推薦', en: 'Dessert Favorites', es: 'Postres' } },
]

export function PopularPicks() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  const heading = lang === 'zh' ? '人氣推薦' : lang === 'es' ? 'Los favoritos' : 'Popular Picks'
  const viewMenu = lang === 'zh' ? '查看完整菜單' : lang === 'es' ? 'Ver menú completo' : 'View Full Menu'

  return (
    <section className="relative bg-cream">
      <div className="mx-auto max-w-screen-xl px-6 pb-14 md:px-12 md:pb-20">
        <div className="mb-8 flex flex-col items-center">
          <h2 className="font-heading text-3xl font-bold text-primary md:text-4xl">{heading}</h2>
          <span className="mt-2 h-1 w-16 rounded-full bg-primary/70" />
        </div>

        <div className="grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6">
          {cards.map((c) => (
            <Link
              key={c.img}
              href="/menu"
              className="group block overflow-hidden rounded-2xl shadow-sm ring-1 ring-black/5 transition-shadow duration-300 hover:shadow-lg"
            >
              <div className="relative aspect-square w-full">
                <Image
                  src={c.img}
                  alt={c.alt[lang]}
                  fill
                  className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
                  sizes="(max-width: 768px) 45vw, 22vw"
                  quality={85}
                />
              </div>
            </Link>
          ))}
        </div>

        <div className="mt-10 flex justify-center">
          <Link
            href="/menu"
            className="inline-flex items-center rounded-full border-2 border-primary px-8 py-3 font-body font-semibold text-primary transition-colors duration-300 hover:bg-primary hover:text-primary-foreground"
          >
            {viewMenu}
          </Link>
        </div>
      </div>
    </section>
  )
}
