'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import { Soup, CupSoda, Heart, Coffee, type LucideIcon } from 'lucide-react'

type Item = { icon: LucideIcon; title: Record<string, string>; sub: Record<string, string> }

const items: Item[] = [
  {
    icon: Soup,
    title: { zh: '台灣經典美味', en: 'Taiwanese Classics', es: 'Clásicos de Taiwán' },
    sub: { zh: '經典料理，原汁原味', en: 'Time-honored, made the real way', es: 'Auténtico, como debe ser' },
  },
  {
    icon: CupSoda,
    title: { zh: '嚴選食材', en: 'Quality Ingredients', es: 'Ingredientes selectos' },
    sub: { zh: '用心挑選，安心享用', en: 'Carefully chosen, enjoyed with ease', es: 'Elegidos con cuidado' },
  },
  {
    icon: Heart,
    title: { zh: '家鄉的溫度', en: 'A Taste of Home', es: 'El sabor de casa' },
    sub: { zh: '一碗料理，一份思念', en: 'Every bowl, a little piece of home', es: 'Cada plato, un recuerdo' },
  },
  {
    icon: Coffee,
    title: { zh: '舒適放鬆空間', en: 'A Cozy Space', es: 'Un espacio acogedor' },
    sub: { zh: '在這裡，慢下來吧', en: 'Slow down and stay a while', es: 'Tómate tu tiempo' },
  },
]

export function ValueStrip() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  return (
    <section className="bg-cream">
      <div className="mx-auto max-w-screen-xl px-6 py-10 md:px-12 md:py-12">
        <div className="grid grid-cols-2 gap-x-6 gap-y-8 md:grid-cols-4">
          {items.map((item) => {
            const Icon = item.icon
            return (
              <div key={item.title.en} className="flex items-center gap-3 md:gap-4">
                <Icon className="h-9 w-9 shrink-0 text-primary md:h-10 md:w-10" strokeWidth={1.5} aria-hidden="true" />
                <div>
                  <p className="font-heading text-base font-bold text-foreground md:text-lg">{item.title[lang]}</p>
                  <p className="font-body text-xs text-muted-foreground md:text-sm">{item.sub[lang]}</p>
                </div>
              </div>
            )
          })}
        </div>
      </div>
    </section>
  )
}
