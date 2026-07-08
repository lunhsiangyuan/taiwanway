'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import Link from 'next/link'
import Image from 'next/image'
import { BookOpen } from 'lucide-react'

export function Hero() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  const tagline = 'A Cozy Taste of Taiwan'

  const headline1 = lang === 'zh' ? '台灣的味道，' : lang === 'es' ? 'Un sabor de Taiwán,' : 'A Taste of Taiwan,'
  const headline2 = lang === 'zh' ? '為你而做。' : lang === 'es' ? 'hecho para ti.' : 'Made for You.'

  const description = lang === 'zh'
    ? '滷肉飯、牛肉麵、珍珠奶茶，還有更多家鄉味，從我們的家鄉，端上你的桌。'
    : lang === 'es'
      ? 'Arroz con cerdo, fideos con res, té de burbujas y más — de nuestra tierra a tu mesa.'
      : 'Braised Pork Rice, Beef Noodle Soup, Bubble Tea, and more cozy favorites — from our hometown to your table.'

  const viewMenu = lang === 'zh' ? '看菜單' : lang === 'es' ? 'Ver menú' : 'View Menu'

  // SEO/GEO：畫面顯示品牌標語，但真 h1 用關鍵字完整的在地描述（螢幕閱讀器/搜尋引擎讀）
  const srHeading = lang === 'zh'
    ? 'TaiwanWay 台灣味 — 紐約 Middletown 家鄉味台式咖啡館｜牛肉麵、滷肉飯、珍珠奶茶、鳳梨酥'
    : lang === 'es'
      ? 'TaiwanWay — Café taiwanés casero en Middletown, NY | Sopa de fideos con res, arroz con cerdo estofado, bubble tea'
      : 'TaiwanWay — Home-Style Taiwanese Café in Middletown, NY | Beef Noodle Soup, Braised Pork Rice, Bubble Tea & Pineapple Cake'

  return (
    <section className="relative w-full bg-cream">
      <div className="relative h-[440px] w-full overflow-hidden sm:h-[500px] md:h-[560px]">
        <Image
          src="/images/store/hero-food.png"
          alt={lang === 'zh'
            ? 'TaiwanWay 招牌 — 滷肉飯、珍珠奶茶、牛肉麵擺在木桌上'
            : 'TaiwanWay signatures — braised pork rice, bubble tea and beef noodle soup on a wood table'}
          fill
          priority
          className="object-cover object-right"
          sizes="100vw"
          quality={85}
        />
        {/* 左側米色柔化，確保文字清楚（手機也可讀） */}
        <div className="absolute inset-0 bg-gradient-to-r from-cream from-5% via-cream/85 via-40% to-transparent to-70%" />
        <div className="absolute inset-0 bg-gradient-to-t from-cream/60 to-transparent md:hidden" />

        <div className="relative z-10 mx-auto flex h-full max-w-screen-xl items-center px-6 md:px-12">
          <div className="max-w-lg text-left">
            <h1 className="sr-only">{srHeading}</h1>
            <p className="mb-2 font-heading text-base italic text-primary/80 md:text-lg">{tagline}</p>
            <div className="font-heading text-4xl font-bold leading-[1.08] sm:text-5xl md:text-6xl">
              <span className="text-[#5b3a2e]">{headline1}</span>
              <br />
              <span className="text-primary">{headline2}</span>
            </div>
            <p className="mt-5 max-w-md font-body text-base leading-relaxed text-foreground/75 md:text-lg">
              {description}
            </p>
            <div className="mt-7">
              <Link
                href="/menu"
                className="inline-flex items-center gap-2 rounded-full bg-primary px-8 py-3.5 font-heading text-lg font-bold text-primary-foreground shadow-lg shadow-primary/25 transition-all duration-300 hover:scale-105 hover:bg-accent"
              >
                <BookOpen className="h-5 w-5" />
                {viewMenu}
              </Link>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
