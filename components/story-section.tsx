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
    ? '在紐約 Middletown 的心臟地帶，TaiwanWay 臺灣味誕生於一個簡單的信念——讓每一位客人都能品嚐到最道地的臺灣家鄉味。我們的創辦人帶著對臺灣美食的熱情，遠渡重洋，只為將那份記憶中的味道帶到這片土地。'
    : language === 'es'
      ? 'En el corazon de Middletown, Nueva York, TaiwanWay nacio de una simple creencia: que cada comensal merece probar los sabores mas autenticos de Taiwan.'
      : 'In the heart of Middletown, New York, TaiwanWay was born from a simple belief — that every diner deserves to taste the most authentic flavors of Taiwan. Our founders brought their passion for Taiwanese cuisine across the ocean, driven by the desire to share the tastes of home.'

  const paragraph2 = language === 'zh'
    ? '我們堅持使用新鮮食材，遵循傳統烹飪手法，從手工現揉的麵條到慢火燉煮的滷肉，每一道料理都承載著數代人的智慧與堅持。'
    : language === 'es'
      ? 'Insistimos en usar ingredientes frescos y seguir tecnicas de cocina tradicionales. Desde fideos hechos a mano hasta cerdo estofado a fuego lento, cada plato lleva la sabiduria de generaciones.'
      : 'We insist on using fresh ingredients and following traditional cooking techniques. From handmade noodles to slow-braised pork, every dish carries the wisdom of generations.'

  const paragraph3 = language === 'zh'
    ? '臺灣味不僅是一間餐廳，更是一座連接臺灣與紐約的美食橋樑。無論你是思鄉的遊子，還是初次嘗試臺灣料理的朋友，這裡永遠有一個位置為你留著。'
    : language === 'es'
      ? 'TaiwanWay no es solo un restaurante, es un puente culinario entre Taiwan y Nueva York.'
      : 'TaiwanWay is not just a restaurant — it is a culinary bridge between Taiwan and New York. Whether you are missing home or trying Taiwanese cuisine for the first time, there is always a seat reserved for you.'

  const quote = language === 'zh'
    ? '「將最道地的臺灣味，帶到 Middletown 的每一張餐桌上。」'
    : language === 'es'
      ? '"Llevando los sabores mas autenticos de Taiwan a cada mesa en Middletown."'
      : '"Bringing authentic Taiwan flavors to Middletown, NY since day one."'

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
            {/* 主圖 - 餐廳內部 */}
            <div className="absolute top-0 right-0 w-[75%] aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl">
              <Image
                src="/images/story-restaurant.png"
                alt={language === 'zh' ? '溫馨的餐廳內部' : 'Warm restaurant interior'}
                fill
                className="object-cover"
                sizes="(max-width: 1024px) 70vw, 35vw"
              />
            </div>

            {/* 次圖 - 手工製麵 */}
            <div className="absolute bottom-0 left-0 w-[60%] aspect-square rounded-2xl overflow-hidden shadow-xl ring-4 ring-[#FAF7F2]">
              <Image
                src="/images/story-cooking.png"
                alt={language === 'zh' ? '手工製麵' : 'Handmade noodles'}
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
