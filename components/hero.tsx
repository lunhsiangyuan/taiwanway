'use client'

import { useEffect, useState, useRef } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'
import Link from 'next/link'
import Image from 'next/image'
import { ChevronDown, Truck, ShoppingBag } from 'lucide-react'

export function Hero() {
  const { language } = useLanguage()
  const [scrollY, setScrollY] = useState(0)
  const heroRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches
    if (prefersReducedMotion) return

    const handleScroll = () => setScrollY(window.scrollY)
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const subtitle = language === 'zh'
    ? '招牌珍奶 · 台灣茶 · 家常料理'
    : language === 'es'
      ? 'Te de Burbujas · Te Taiwanes · Comida Casera'
      : 'Signature Bubble Tea · Taiwan Tea · Comfort Food'

  const description = language === 'zh'
    ? '巴黎咖啡館的悠閒，台灣茶館的溫度。招牌手搖珍珠奶茶、阿里山高山茶、慢燉牛肉麵。'
    : language === 'es'
      ? 'Mananas parisinas, tardes de Taiwan. Te de burbujas artesanal, te de alta montana de Alishan, fideos con carne a fuego lento.'
      : 'Parisian mornings meet Taiwan afternoons. Signature hand-shaken bubble tea, Alishan high-mountain tea, slow-simmered beef noodle soup.'

  const viewMenu = language === 'zh' ? '瀏覽菜單' : language === 'es' ? 'Ver Menu' : 'View Menu'
  const delivery = language === 'zh' ? '外送點餐' : language === 'es' ? 'Delivery' : 'Delivery'
  const ourStory = language === 'zh' ? '我們的故事' : language === 'es' ? 'Nuestra Historia' : 'Our Story'

  return (
    <section ref={heroRef} className="relative h-screen w-full overflow-hidden">
      {/* 背景圖片 */}
      <div
        className="absolute inset-0"
        style={{ transform: `translateY(${scrollY * 0.15}px)` }}
      >
        <Image
          src="/images/hero-bg-v2.jpg"
          alt="TaiwanWay 臺灣味 — Taiwanese café table with beef noodle soup, bubble tea, sea-salt caramel latte, Alishan oolong tea, braised pork rice and pineapple cakes in Middletown, NY"
          fill
          priority
          className="object-cover scale-110"
          sizes="100vw"
          quality={85}
        />
      </div>

      {/* 暗色漸層覆蓋層 */}
      <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/50 to-black/30" />
      <div className="absolute inset-0 bg-gradient-to-r from-black/30 via-transparent to-black/30" />

      {/* 主要內容 */}
      <div className="relative z-10 flex h-full flex-col items-center justify-center px-4 text-center">
        {/* 小標題 */}
        <p
          className="mb-4 font-body text-sm font-medium uppercase tracking-[0.3em] text-[hsl(44,80%,60%)] animate-fade-in-up"
          style={{ animationDelay: '0.2s', animationFillMode: 'both' }}
        >
          {subtitle}
        </p>

        {/* 主標題 */}
        <h1
          className="font-heading text-4xl font-black text-white sm:text-6xl md:text-7xl lg:text-8xl animate-fade-in-up drop-shadow-2xl"
          style={{ animationDelay: '0.4s', animationFillMode: 'both' }}
        >
          TaiwanWay
        </h1>

        {/* 中文副標題 */}
        <p
          className="mt-2 font-heading text-3xl text-white/80 md:text-4xl animate-fade-in-up"
          style={{ animationDelay: '0.6s', animationFillMode: 'both' }}
        >
          臺灣味
        </p>

        {/* 描述 */}
        <p
          className="mt-8 max-w-2xl font-body text-xl md:text-2xl leading-relaxed text-white/85 animate-fade-in-up"
          style={{ animationDelay: '0.8s', animationFillMode: 'both' }}
        >
          {description}
        </p>

        {/* CTA 按鈕 */}
        <div
          className="mt-8 w-full max-w-md animate-fade-in-up"
          style={{ animationDelay: '1s', animationFillMode: 'both' }}
        >
          {/* 訂餐 — 外送 */}
          <div className="flex justify-center">
            <a
              href="https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A"
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center justify-center gap-2 rounded-full bg-[hsl(44,80%,40%)] px-8 py-3 font-body text-sm font-semibold text-white transition-all duration-300 hover:bg-[hsl(44,80%,35%)] hover:scale-105 shadow-lg shadow-black/20"
            >
              <Truck className="h-4 w-4" />
              {delivery}
            </a>
          </div>
          {/* 瀏覽菜單 */}
          <div className="mt-3 flex justify-center">
            <Link
              href="/menu"
              className="inline-flex items-center justify-center rounded-full border-2 border-white/30 px-8 py-2.5 font-body text-xs font-medium text-white/80 backdrop-blur-sm transition-all duration-300 hover:border-white hover:bg-white/10"
            >
              {viewMenu}
            </Link>
          </div>
        </div>
      </div>

      {/* 滾動指示器 */}
      <div className="absolute bottom-8 left-1/2 z-10 -translate-x-1/2 flex flex-col items-center gap-2 text-white/50 animate-bounce">
        <span className="font-body text-xs uppercase tracking-widest">Scroll</span>
        <ChevronDown className="h-5 w-5" />
      </div>
    </section>
  )
}
