'use client'

import { useEffect, useState, useRef } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'
import Link from 'next/link'
import { Truck, ShoppingBag } from 'lucide-react'
import Image from 'next/image'

type MenuItem = {
  nameZh: string
  nameEn: string
  nameEs: string
  descZh: string
  descEn: string
  descEs: string
  price: string
  image: string
  category: 'drink' | 'main' | 'dessert'
}

const menuItems: MenuItem[] = [
  {
    nameZh: '珍珠奶茶',
    nameEn: 'Bubble Tea',
    nameEs: 'Te de Burbujas',
    descZh: '台灣空運蜜香紅茶，每日手煮 Q 彈珍珠',
    descEn: 'Honey-scented black tea air-shipped from Taiwan, hand-cooked tapioca pearls daily',
    descEs: 'Te negro miel de Taiwan, perlas cocidas a mano cada dia',
    price: '$6.45',
    image: '/images/bubble-tea.png',
    category: 'drink',
  },
  {
    nameZh: '阿里山高山烏龍',
    nameEn: 'Alishan High-Mountain Oolong',
    nameEs: 'Oolong de Alta Montana Alishan',
    descZh: '海拔千米以上茶園，壺泡現沏，茶香回甘',
    descEn: 'Grown above 1,000m in Taiwan\'s Alishan mountains, pot-brewed fresh to order',
    descEs: 'Cultivado sobre 1,000m en las montanas de Alishan, preparado al momento',
    price: '$5.00',
    image: '/images/oolong-tea.png',
    category: 'drink',
  },
  {
    nameZh: '牛肉麵',
    nameEn: 'Beef Noodle Soup',
    nameEs: 'Sopa de Fideos con Res',
    descZh: '紅燒牛肉湯底慢燉一整天，配手工麵條',
    descEn: 'Slow-simmered all day — rich braised beef broth with handmade noodles',
    descEs: 'Caldo de res estofada cocido todo el dia, con fideos hechos a mano',
    price: 'M $13.99 / L $15.99',
    image: '/images/beef-noodle.png',
    category: 'main',
  },
  {
    nameZh: '滷肉飯',
    nameEn: 'Braised Pork Rice',
    nameEs: 'Arroz con Cerdo Estofado',
    descZh: '慢火燉煮滷肉澆淋白飯，台灣人的 comfort food',
    descEn: 'Savory braised pork over steamed rice — Taiwan\'s ultimate comfort food',
    descEs: 'Cerdo estofado sobre arroz al vapor — el comfort food de Taiwan',
    price: 'M $10.99 / L $12.99',
    image: '/images/braised-pork-v3.jpg',
    category: 'main',
  },
  {
    nameZh: '鳳梨酥',
    nameEn: 'Pineapple Cake',
    nameEs: 'Pastel de Pina',
    descZh: '手工現作，酥脆外皮包裹土鳳梨內餡',
    descEn: 'Handmade in-house — buttery pastry with Taiwan pineapple filling',
    descEs: 'Hecho a mano — masa mantecosa con relleno de pina de Taiwan',
    price: '$3.25',
    image: '/images/pineapple-cake.png',
    category: 'dessert',
  },
]

export function MenuShowcase() {
  const { language } = useLanguage()
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setIsVisible(true)
      },
      { threshold: 0.1 }
    )
    if (sectionRef.current) observer.observe(sectionRef.current)
    return () => observer.disconnect()
  }, [])

  const title = language === 'zh' ? '經典推薦' : language === 'es' ? 'Nuestro Menu' : 'Our Menu'
  const subtitle = language === 'zh'
    ? '招牌飲品 · 家常料理'
    : language === 'es'
      ? 'Bebidas Artesanales · Comida Casera'
      : 'Handcrafted Drinks · Comfort Food'
  const viewFullMenu = language === 'zh' ? '查看完整菜單' : language === 'es' ? 'Ver Menu Completo' : 'View Full Menu'
  const pickupLabel = language === 'zh' ? '來店自取' : language === 'es' ? 'Recoger' : 'Pickup'
  const deliveryLabel = language === 'zh' ? '外送 Uber Eats' : 'Delivery'

  const getName = (item: MenuItem) => language === 'zh' ? item.nameZh : language === 'es' ? item.nameEs : item.nameEn
  const getSubName = (item: MenuItem) => language === 'zh' ? item.nameEn : item.nameZh
  const getDesc = (item: MenuItem) => language === 'zh' ? item.descZh : language === 'es' ? item.descEs : item.descEn

  return (
    <section ref={sectionRef} className="relative bg-[#2D1810] py-24 overflow-hidden">
      {/* 背景裝飾 */}
      <div className="absolute top-0 left-0 w-full h-px bg-gradient-to-r from-transparent via-[hsl(44,80%,40%)]/20 to-transparent" />
      <div className="absolute -top-32 -right-32 h-64 w-64 rounded-full bg-[hsl(17,45%,57%)]/[0.06] blur-3xl" />
      <div className="absolute -bottom-20 -left-20 h-48 w-48 rounded-full bg-[hsl(44,80%,40%)]/[0.04] blur-2xl" />

      <div className="relative mx-auto max-w-6xl px-4">
        {/* 區塊標題 */}
        <div className={`mb-20 text-center transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <p className="mb-3 font-body text-sm font-medium uppercase tracking-[0.2em] text-[hsl(44,80%,40%)]">
            {subtitle}
          </p>
          <h2 className="font-heading text-4xl font-bold text-white md:text-5xl">
            {title}
          </h2>
          <div className="mx-auto mt-4 h-0.5 w-20 bg-[hsl(44,80%,40%)]" />
        </div>

        {/* 菜品列表 */}
        <div className="space-y-0">
          {menuItems.map((item, index) => (
            <div
              key={item.nameEn}
              className={`group relative transition-all duration-500 ${
                isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-6'
              }`}
              style={{ transitionDelay: isVisible ? `${150 + index * 80}ms` : '0ms' }}
            >
              {/* 分隔線 */}
              {index === 0 && <div className="h-px bg-white/[0.08]" />}

              <div className="flex items-center gap-5 py-6 px-2 transition-all duration-300 hover:bg-white/[0.03] rounded-lg cursor-default">
                {/* 食物照片 */}
                <div className="hidden sm:block relative h-16 w-16 flex-shrink-0 rounded-full overflow-hidden ring-2 ring-white/10 transition-transform duration-300 group-hover:scale-110 group-hover:ring-[hsl(44,80%,40%)]/30">
                  <Image
                    src={item.image}
                    alt={getName(item)}
                    fill
                    className="object-cover"
                    sizes="64px"
                  />
                </div>

                {/* 名稱和描述 */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-baseline gap-3 flex-wrap">
                    <h3 className="font-heading text-xl text-white group-hover:text-[hsl(44,80%,60%)] transition-colors duration-300">
                      {getName(item)}
                    </h3>
                    <span className="font-body text-sm text-white/30">
                      {getSubName(item)}
                    </span>
                  </div>
                  <p className="mt-1 font-body text-sm text-white/40 leading-relaxed">
                    {getDesc(item)}
                  </p>
                </div>

                {/* 價格 */}
                <div className="hidden sm:flex items-center flex-shrink-0 gap-4">
                  <div className="w-8 lg:w-16 border-b border-dotted border-white/10" />
                  <span className="font-heading text-lg text-[hsl(44,80%,60%)] whitespace-nowrap">
                    {item.price}
                  </span>
                </div>
              </div>

              {/* 分隔線 */}
              <div className="h-px bg-white/[0.08]" />
            </div>
          ))}
        </div>

        {/* CTA 按鈕 */}
        <div className={`mt-16 flex flex-col sm:flex-row items-center justify-center gap-4 transition-all duration-700 delay-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <a
            href="https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center justify-center gap-2 rounded-full bg-[#06C167] px-8 py-3.5 font-body text-sm font-semibold text-white transition-all duration-300 hover:bg-[#05a557] hover:scale-105 cursor-pointer"
          >
            <Truck className="h-4 w-4" /> {deliveryLabel}
          </a>
          <a
            href="https://order.taiwanwayny.com/order"
            className="inline-flex items-center justify-center gap-2 rounded-full bg-[hsl(44,80%,40%)] px-8 py-3.5 font-body text-sm font-semibold text-white transition-all duration-300 hover:bg-[hsl(44,80%,35%)] hover:scale-105 cursor-pointer"
          >
            <ShoppingBag className="h-4 w-4" /> {pickupLabel}
          </a>
          <Link
            href="/menu"
            className="inline-flex items-center justify-center rounded-full border-2 border-[hsl(44,80%,40%)] px-8 py-3.5 font-body text-sm font-semibold text-[hsl(44,80%,40%)] transition-all duration-300 hover:bg-[hsl(44,80%,40%)] hover:text-white cursor-pointer"
          >
            {viewFullMenu}
          </Link>
        </div>
      </div>
    </section>
  )
}
