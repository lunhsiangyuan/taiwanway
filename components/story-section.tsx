'use client'

import { useEffect, useState, useRef } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'
import Image from 'next/image'

export function StorySection() {
  const { language } = useLanguage()
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setIsVisible(true)
      },
      { threshold: 0.2 }
    )
    if (sectionRef.current) observer.observe(sectionRef.current)
    return () => observer.disconnect()
  }, [])

  const quote = language === 'zh'
    ? '「門推開，就像回到台灣的家。」'
    : language === 'es'
      ? '"Abre la puerta — sabe a casa, en taiwanés."'
      : '"Open the door — it tastes like home, in Taiwanese."'

  return (
    <section ref={sectionRef} className="relative bg-[#FAF7F2] py-24 overflow-hidden">
      {/* 背景裝飾 */}
      <div className="absolute -top-40 -right-40 h-[500px] w-[500px] rounded-full bg-[hsl(17,45%,57%)]/[0.04] blur-3xl" />
      <div className="absolute -bottom-20 -left-20 h-[300px] w-[300px] rounded-full bg-[hsl(44,80%,40%)]/[0.06] blur-2xl" />

      <div className="relative mx-auto max-w-6xl px-4">
        {/* 兩欄佈局：引言 + 雙圖拼貼 */}
        <div className="grid gap-16 lg:grid-cols-2 items-center">
          {/* 左欄 - 引言 */}
          <div className={`flex flex-col justify-center transition-all duration-700 delay-200 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8'}`}>
            {/* 引用 */}
            <blockquote className="border-l-4 border-[hsl(44,80%,40%)] pl-6">
              <p className="font-heading text-xl italic text-[#2D1810]">
                {quote}
              </p>
            </blockquote>
          </div>

          {/* 右欄 - 圖片拼貼 */}
          <div className={`relative min-h-[500px] transition-all duration-700 delay-400 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8'}`}>
            {/* 主圖 - 咖啡廳座位區 */}
            <div className="absolute top-0 right-0 w-[75%] aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl">
              <Image
                src="/images/cafe-interior-seating.jpg"
                alt={language === 'zh' ? '台式咖啡廳座位區 — 吊燈、壁爐、台灣商品架（Middletown, NY）' : language === 'es' ? 'Area de asientos del cafe taiwanes con candelabro y chimenea en Middletown, NY' : 'Taiwanese café seating area with chandelier, fireplace and Taiwan shelves in Middletown, NY'}
                fill
                className="object-cover"
                sizes="(max-width: 1024px) 70vw, 35vw"
              />
            </div>

            {/* 次圖 - 店門口紅磚建築 */}
            <div className="absolute bottom-0 left-0 w-[60%] aspect-square rounded-2xl overflow-hidden shadow-xl ring-4 ring-[#FAF7F2]">
              <Image
                src="/images/storefront.jpg"
                alt={language === 'zh' ? 'TaiwanWay 店門口 — 26 South St, Middletown NY 的紅磚歷史建築' : language === 'es' ? 'Fachada de TaiwanWay — edificio historico de ladrillo rojo en 26 South St, Middletown NY' : 'TaiwanWay storefront — historic red-brick building at 26 South St, Middletown NY'}
                fill
                className="object-cover"
                sizes="(max-width: 1024px) 55vw, 28vw"
              />
            </div>

            {/* 裝飾元素 */}
            <div className="absolute -top-4 -right-4 h-24 w-24 rounded-full bg-[hsl(44,80%,40%)]/10" />
            <div className="absolute bottom-16 right-[15%] h-3 w-3 rounded-full bg-[hsl(44,80%,40%)]/40" />
            <div className="absolute top-[40%] left-[25%] h-4 w-4 rounded-full bg-[hsl(17,45%,57%)]/20" />
          </div>
        </div>
      </div>
    </section>
  )
}
