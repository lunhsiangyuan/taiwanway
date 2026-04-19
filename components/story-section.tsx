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
    ? 'Middletown 的第一間台式咖啡廳，最自豪的一杯是我們的招牌手搖珍珠奶茶。巴黎咖啡館的悠閒遇上台灣茶館的溫度——從 Middletown 開始，把一杯台灣味，帶進 Hudson Valley。'
    : language === 'es'
      ? "El primer cafe taiwanes de Middletown — nuestro mayor orgullo es el te de burbujas artesanal. Donde las mananas parisinas se encuentran con las tardes de Taiwan — desde Middletown, llevando un sabor de Taiwan al Hudson Valley."
      : "Middletown's first Taiwanese café — and our proudest cup is our signature hand-shaken bubble tea. Where Parisian mornings meet Taiwan afternoons — starting in Middletown, bringing a taste of Taiwan to the Hudson Valley."

  const paragraph2 = language === 'zh'
    ? '我們用做茶的規格做每一杯珍奶。台灣空運蜜香紅茶、阿里山高山茶、京都一保堂抹茶——搭配每日手煮的 Q 彈珍珠。另有法式深烘焙拿鐵、慢燉一整天的牛肉麵和滷肉飯。'
    : language === 'es'
      ? "Tratamos cada te de burbujas con el rigor de una casa de te. Te negro miel enviado desde Taiwan, oolong de alta montana de Alishan, matcha de Ippodo en Kioto — con perlas cocinadas a mano cada dia. Ademas, lattes de tueste oscuro frances, fideos con carne a fuego lento y arroz con cerdo estofado."
      : "We treat every bubble tea with the rigor of a tea house. Honey-scented black tea air-shipped from Taiwan, Alishan high-mountain oolong, Kyoto Ippodo matcha — paired with tapioca pearls hand-cooked daily. Plus French dark-roast lattes, slow-simmered beef noodle soup, and braised pork rice."

  const paragraph3 = language === 'zh'
    ? '點一杯招牌珍奶配一碗滷肉飯當午餐、帶筆電待一個下午、或和朋友分享一壺阿里山烏龍。不只是一間咖啡廳——是你在 Middletown 的角落客廳。'
    : language === 'es'
      ? "Pide nuestro te de burbujas artesanal con un tazon de arroz con cerdo estofado para el almuerzo, trae tu laptop para trabajar una tarde, o comparte una tetera de oolong de Alishan con amigos. Mas que un cafe — somos tu rincon en Middletown."
      : "Order our signature bubble tea with a bowl of braised pork rice for lunch, bring your laptop for an afternoon of work, or share a pot of Alishan oolong with friends. More than a café — we're your corner retreat in Middletown."

  const quote = language === 'zh'
    ? '「門推開，就是台灣的午後。」'
    : language === 'es'
      ? '"Abre la puerta — una tarde en Taiwan."'
      : '"Open the door — it\'s a Taiwanese afternoon."'

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
