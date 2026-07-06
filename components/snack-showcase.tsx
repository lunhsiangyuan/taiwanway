'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import Link from 'next/link'
import Image from 'next/image'

type Banner = { img: string; alt: Record<string, string> }

const banners: Banner[] = [
  { img: '/images/menu-cards/snack-tea.png', alt: { zh: '台灣高山茶', en: 'Premium Taiwanese Tea', es: 'Té de alta montaña de Taiwán' } },
  { img: '/images/menu-cards/snack-tea-gifts.png', alt: { zh: '台灣茶禮', en: 'Tea Gifts', es: 'Regalos de té' } },
  { img: '/images/menu-cards/snack-plum.png', alt: { zh: '台灣梅子蜜餞', en: 'Taiwanese Plum Snacks', es: 'Ciruelas dulces de Taiwán' } },
  { img: '/images/menu-cards/snack-savory.png', alt: { zh: '台灣鹹香小點', en: 'Savory Taiwanese Snacks', es: 'Snacks salados de Taiwán' } },
]

export function SnackShowcase() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  const title = lang === 'zh' ? '台灣零食專賣' : lang === 'es' ? 'Snacks Taiwaneses' : 'Taiwanese Snacks'
  const subtitle =
    lang === 'zh' ? '從高山茶到鹹甜零嘴，把台灣的味道帶回家'
      : lang === 'es' ? 'Del té de montaña a los bocados dulces y salados — llévate un sabor de Taiwán'
        : 'From mountain tea to sweet & savory bites — take a taste of Taiwan home'
  const viewAll = lang === 'zh' ? '查看全部' : lang === 'es' ? 'Ver todos' : 'View All'

  return (
    <section className="bg-[#faf7f2]">
      <div className="mx-auto max-w-screen-xl px-6 py-16 md:px-12 md:py-20">
        <div className="mb-10 flex flex-col items-center text-center">
          <h2 className="font-heading text-3xl font-bold text-primary md:text-4xl">{title}</h2>
          <span className="mt-2 h-1 w-16 rounded-full bg-primary/70" />
          <p className="mt-4 max-w-xl font-body text-base text-muted-foreground md:text-lg">{subtitle}</p>
        </div>

        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 md:gap-6">
          {banners.map((b) => (
            <Link
              key={b.img}
              href="/products"
              className="group block overflow-hidden rounded-2xl shadow-sm ring-1 ring-black/5 transition-shadow duration-300 hover:shadow-lg"
            >
              <div className="relative aspect-[3/2] w-full">
                <Image
                  src={b.img}
                  alt={b.alt[lang]}
                  fill
                  className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
                  sizes="(max-width: 640px) 100vw, 50vw"
                  quality={85}
                />
              </div>
            </Link>
          ))}
        </div>

        <div className="mt-10 flex justify-center">
          <Link
            href="/products"
            className="inline-flex items-center rounded-full border-2 border-primary px-8 py-3 font-body font-semibold text-primary transition-colors duration-300 hover:bg-primary hover:text-primary-foreground"
          >
            {viewAll}
          </Link>
        </div>
      </div>
    </section>
  )
}
