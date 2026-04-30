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

  const title = language === 'zh' ? '我們的故事' : language === 'es' ? 'Nuestra Historia' : 'Our Story'

  const paragraph1 = language === 'zh'
    ? 'Middletown 10940 的家鄉味台式咖啡館。從一碗慢燉牛肉麵、一杯手作珍珠奶茶開始——把家鄉的味道，帶到 Hudson Valley 的這個小角落。'
    : language === 'es'
      ? "Un café taiwanés casero en Middletown 10940. Desde un tazón de fideos con res a fuego lento y un té de burbujas artesanal — llevando los sabores de casa a este pequeño rincón del valle del Hudson."
      : "A home-style Taiwanese café in Middletown 10940. From a bowl of slow-braised beef noodle soup to a hand-shaken bubble tea — bringing the comforting flavors of home to this quiet corner of the Hudson Valley."

  const paragraph2 = language === 'zh'
    ? '我們用做茶的規格做每一杯珍奶。台灣空運蜜香紅茶、阿里山高山茶、京都一保堂抹茶——搭配每日手煮的 Q 彈珍珠。再加上慢燉一整天的牛肉麵、經典滷肉飯，與每日現烤的鳳梨酥——每一道都用手做。'
    : language === 'es'
      ? "Tratamos cada té de burbujas con el rigor de una casa de té. Té negro miel enviado desde Taiwán, oolong de alta montaña de Alishan, matcha de Ippodo en Kioto — con perlas cocinadas a mano cada día. Además, sopa de fideos con res a fuego lento, arroz con cerdo guisado clásico y pasteles de piña recién horneados — cada plato hecho a mano."
      : "We treat every bubble tea with the rigor of a tea house. Honey-scented black tea air-shipped from Taiwan, Alishan high-mountain oolong, Kyoto Ippodo matcha — paired with tapioca pearls hand-cooked daily. Plus slow-braised beef noodle soup, classic braised pork rice, and freshly baked pineapple cakes — every dish made by hand."

  const paragraph3 = language === 'zh'
    ? '點一杯招牌珍奶配一碗滷肉飯當午餐、帶筆電待一個下午、或和朋友分享一壺阿里山烏龍。不只是一間咖啡廳——是你在 Middletown 像家一樣的小角落。'
    : language === 'es'
      ? "Pide nuestro té de burbujas artesanal con un tazón de arroz con cerdo guisado para el almuerzo, trae tu laptop para trabajar una tarde, o comparte una tetera de oolong de Alishan con amigos. Más que un café — somos tu rincón en Middletown, donde Taiwán sabe a casa."
      : "Order our signature bubble tea with a bowl of braised pork rice for lunch, bring your laptop for an afternoon of work, or share a pot of Alishan oolong with friends. More than a café — we're your corner of Middletown, where Taiwan tastes like home."

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
        {/* 區塊標題 */}
        <div className={`mb-20 text-center transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <h2 className="font-heading text-4xl font-bold text-[#2D1810] md:text-5xl">
            {title}
          </h2>
          <div className="mx-auto mt-4 h-0.5 w-20 bg-[hsl(44,80%,40%)]" />
        </div>

        {/* 兩欄佈局 */}
        <div className="grid gap-16 lg:grid-cols-2 items-center">
          {/* 左欄 - 故事文字 */}
          <div className={`flex flex-col justify-center space-y-6 transition-all duration-700 delay-200 ${isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8'}`}>
            <p className="font-body text-lg leading-relaxed text-[hsl(17,20%,40%)]">
              {paragraph1}
            </p>
            <p className="font-body text-lg leading-relaxed text-[hsl(17,20%,40%)]">
              {paragraph2}
            </p>
            <p className="font-body text-lg leading-relaxed text-[hsl(17,20%,40%)]">
              {paragraph3}
            </p>

            {/* 引用 */}
            <blockquote className="mt-4 border-l-4 border-[hsl(44,80%,40%)] pl-6">
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
