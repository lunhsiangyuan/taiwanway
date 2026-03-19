'use client'

import { useState, useCallback, useEffect, useRef } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'
import Image from 'next/image'
import { ChevronLeft, ChevronRight } from 'lucide-react'

/* ── 資料型別 ── */
type MenuItemData = {
  nameZh: string
  nameEn: string
  nameEs: string
  descZh?: string
  descEn?: string
  descEs?: string
  options?: string
  price?: string
}

type MenuCategory = {
  id: string
  titleZh: string
  titleEn: string
  titleEs: string
  subtitleZh?: string
  subtitleEn?: string
  subtitleEs?: string
  image: string
  items: MenuItemData[]
}

/* ── 菜單資料 ── */
const menuCategories: MenuCategory[] = [
  {
    id: 'signature',
    titleZh: '招牌推薦',
    titleEn: 'Signature',
    titleEs: 'Especialidades',
    subtitleZh: '經典必點',
    subtitleEn: 'Must-Try Classics',
    subtitleEs: 'Clásicos Imperdibles',
    image: '/images/hero-bg.png',
    items: [
      { nameZh: '招牌珍珠奶茶', nameEn: 'Signature Bubble Tea', nameEs: 'Té de Burbujas Especial', descZh: 'Q彈珍珠配濃郁奶香，經典臺灣味', descEn: 'Chewy tapioca pearls with rich milk tea, classic Taiwan flavor', descEs: 'Perlas de tapioca con té de leche', price: '5.95' },
      { nameZh: '紅燒牛肉麵', nameEn: 'Braised Beef Noodle Soup', nameEs: 'Sopa de Fideos con Res', descZh: '香濃湯頭，嫩滑牛肉，手工麵條', descEn: 'Rich broth with tender beef and handmade noodles', descEs: 'Caldo con res y fideos hechos a mano', price: '12.99' },
      { nameZh: '古早味滷肉飯', nameEn: 'Braised Pork Rice', nameEs: 'Arroz con Cerdo', descZh: '慢火燉煮，古早味入味白飯', descEn: 'Slow-braised pork over steamed rice', descEs: 'Cerdo estofado sobre arroz', price: '8.99' },
    ],
  },
  {
    id: 'taiwanese-black-tea',
    titleZh: '台灣紅茶',
    titleEn: 'Taiwanese Black Tea',
    titleEs: 'Té Negro Taiwanés',
    subtitleZh: '在地茶香',
    subtitleEn: 'Local Tea Aroma',
    subtitleEs: 'Aroma del Té Local',
    image: '/images/honey-black-tea.png',
    items: [
      { nameZh: '台灣蜜香紅茶', nameEn: 'Taiwan Honey Black Tea', nameEs: 'Té Negro con Miel', options: '熱 / 冷', price: '5.95' },
      { nameZh: '招牌珍珠奶茶', nameEn: 'Signature Bubble Tea', nameEs: 'Té de Burbujas', options: '熱 / 冷', price: '5.95' },
      { nameZh: '蜜香奶茶', nameEn: 'Honey Milk Tea', nameEs: 'Té de Leche con Miel', options: '熱 / 冷', price: '4.95' },
    ],
  },
  {
    id: 'caffeine-free',
    titleZh: '無咖啡因',
    titleEn: 'Caffeine Free',
    titleEs: 'Sin Cafeína',
    subtitleZh: '溫潤無負擔',
    subtitleEn: 'Gentle & Light',
    subtitleEs: 'Suave y Ligero',
    image: '/images/brown-sugar-milk.png',
    items: [
      { nameZh: '黑糖珍珠鮮奶', nameEn: 'Brown Sugar Pearl Fresh Milk', nameEs: 'Leche con Perlas de Azúcar Morena', options: '熱 / 冷', price: '6.45' },
    ],
  },
  {
    id: 'jasmine',
    titleZh: '茉莉綠茶',
    titleEn: 'Jasmine Green Tea',
    titleEs: 'Té Verde Jazmín',
    subtitleZh: '花香清新',
    subtitleEn: 'Floral Freshness',
    subtitleEs: 'Frescura Floral',
    image: '/images/jasmine-tea.png',
    items: [
      { nameZh: '茉莉蜂蜜綠茶', nameEn: 'Jasmine Honey Green Tea', nameEs: 'Té Verde Jazmín con Miel', options: '冷飲', price: '5.25' },
      { nameZh: '茉莉珍珠奶綠', nameEn: 'Jasmine Pearl Milk Green Tea', nameEs: 'Té Verde Jazmín con Perlas', options: '熱 / 冷', price: '6.25' },
    ],
  },
  {
    id: 'oolong',
    titleZh: '台灣烏龍茶',
    titleEn: 'Taiwan Oolong',
    titleEs: 'Oolong Taiwanés',
    subtitleZh: '半發酵茶韻',
    subtitleEn: 'Semi-Fermented Elegance',
    subtitleEs: 'Elegancia Semi-Fermentada',
    image: '/images/oolong-tea.png',
    items: [
      { nameZh: '蜂蜜烏龍珍珠奶茶', nameEn: 'Honey Oolong Bubble Tea', nameEs: 'Oolong con Miel y Perlas', options: '熱 / 冷', price: '6.25' },
      { nameZh: '蜂蜜烏龍奶茶', nameEn: 'Honey Oolong Milk Tea', nameEs: 'Oolong con Miel y Leche', options: '熱 / 冷', price: '5.25' },
    ],
  },
  {
    id: 'matcha',
    titleZh: '京都抹茶',
    titleEn: 'Kyoto Matcha',
    titleEs: 'Matcha de Kioto',
    subtitleZh: '茶道之美',
    subtitleEn: 'Beauty of Tea Ceremony',
    subtitleEs: 'Belleza de la Ceremonia',
    image: '/images/matcha-latte.png',
    items: [
      { nameZh: '抹茶拿鐵', nameEn: 'Matcha Latte', nameEs: 'Latte de Matcha', options: '熱 / 冷', price: '5.65' },
      { nameZh: '珍珠抹茶拿鐵', nameEn: 'Pearl Matcha Latte', nameEs: 'Latte de Matcha con Perlas', options: '熱 / 冷', price: '6.85' },
    ],
  },
  {
    id: 'pot-brewed',
    titleZh: '現沖高山茶',
    titleEn: 'Pot-Brewed Tea',
    titleEs: 'Té de Tetera',
    subtitleZh: '壺泡原味',
    subtitleEn: 'Authentic Pot-Brewed',
    subtitleEs: 'Auténtico de Tetera',
    image: '/images/pot-brewed-tea.png',
    items: [
      { nameZh: '冬片', nameEn: 'Winter Harvest', nameEs: 'Cosecha de Invierno', options: '熱飲', price: '5' },
      { nameZh: '春茶', nameEn: 'Spring Tea', nameEs: 'Té de Primavera', options: '熱飲', price: '5' },
      { nameZh: '金萱', nameEn: 'Jin Xuan', nameEs: 'Jin Xuan', options: '熱飲', price: '5' },
      { nameZh: '鐵觀音', nameEn: 'Tieguanyin', nameEs: 'Tieguanyin', options: '熱飲', price: '6' },
      { nameZh: '阿里山紅茶', nameEn: 'Alishan Black Tea', nameEs: 'Té Negro Alishan', options: '熱飲', price: '5' },
    ],
  },
  {
    id: 'main-dishes',
    titleZh: '主餐',
    titleEn: 'Main Dishes',
    titleEs: 'Platos Principales',
    subtitleZh: '道地臺灣味',
    subtitleEn: 'Authentic Taiwanese Flavor',
    subtitleEs: 'Sabor Auténtico',
    image: '/images/beef-noodle.png',
    items: [
      { nameZh: '紅燒牛肉麵', nameEn: 'Braised Beef Noodle Soup', nameEs: 'Sopa de Fideos con Res', descZh: '香濃湯頭，嫩滑牛肉，手工麵條', descEn: 'Rich broth, tender beef, handmade noodles', descEs: 'Caldo, res tierna, fideos artesanales', price: '12.99' },
      { nameZh: '古早味滷肉飯', nameEn: 'Braised Pork Rice', nameEs: 'Arroz con Cerdo', descZh: '入味滷肉，搭配香Q白飯', descEn: 'Savory braised pork over steamed rice', descEs: 'Cerdo estofado sobre arroz', price: '8.99' },
      { nameZh: '嘉義雞肉飯', nameEn: 'Chiayi Chicken Rice', nameEs: 'Arroz con Pollo de Chiayi', descZh: '火雞肉絲，搭配油蔥與醬汁', descEn: 'Shredded turkey with fried shallots and sauce', descEs: 'Pavo desmenuzado con chalotes fritos y salsa', price: '9.99' },
    ],
  },
  {
    id: 'desserts',
    titleZh: '甜點',
    titleEn: 'Desserts',
    titleEs: 'Postres',
    subtitleZh: '甜蜜收尾',
    subtitleEn: 'Sweet Endings',
    subtitleEs: 'Finales Dulces',
    image: '/images/pineapple-cake.png',
    items: [
      { nameZh: '台灣鳳梨酥', nameEn: 'Taiwan Pineapple Cake', nameEs: 'Pastel de Piña', descZh: '酥脆外皮包裹鳳梨內餡，每日現作', descEn: 'Buttery pastry with pineapple filling, freshly made daily', descEs: 'Pastel de mantequilla con piña, hecho diariamente', price: '2.85' },
    ],
  },
]

/* ── 元件本體 ── */
export function MenuCarousel() {
  const { language } = useLanguage()
  const [currentPage, setCurrentPage] = useState(0)
  const [direction, setDirection] = useState(0) // -1 left, 1 right
  const [isAnimating, setIsAnimating] = useState(false)
  const touchStartX = useRef(0)
  const containerRef = useRef<HTMLDivElement>(null)

  const totalPages = menuCategories.length

  const goToPage = useCallback((page: number, dir?: number) => {
    if (isAnimating || page === currentPage) return
    setDirection(dir ?? (page > currentPage ? 1 : -1))
    setIsAnimating(true)
    setTimeout(() => {
      setCurrentPage(page)
      setTimeout(() => setIsAnimating(false), 50)
    }, 300)
  }, [currentPage, isAnimating])

  const goNext = useCallback(() => {
    if (currentPage < totalPages - 1) goToPage(currentPage + 1, 1)
  }, [currentPage, totalPages, goToPage])

  const goPrev = useCallback(() => {
    if (currentPage > 0) goToPage(currentPage - 1, -1)
  }, [currentPage, goToPage])

  // 鍵盤導航
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight') goNext()
      if (e.key === 'ArrowLeft') goPrev()
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [goNext, goPrev])

  // 觸控滑動
  const handleTouchStart = (e: React.TouchEvent) => {
    touchStartX.current = e.touches[0].clientX
  }
  const handleTouchEnd = (e: React.TouchEvent) => {
    const diff = touchStartX.current - e.changedTouches[0].clientX
    if (Math.abs(diff) > 60) {
      if (diff > 0) goNext()
      else goPrev()
    }
  }

  const cat = menuCategories[currentPage]

  const getTitle = (c: MenuCategory) =>
    language === 'zh' ? c.titleZh : language === 'es' ? c.titleEs : c.titleEn
  const getSubtitle = (c: MenuCategory) =>
    language === 'zh' ? c.subtitleZh : language === 'es' ? c.subtitleEs : c.subtitleEn
  const getName = (item: MenuItemData) =>
    language === 'zh' ? item.nameZh : language === 'es' ? item.nameEs : item.nameEn
  const getDesc = (item: MenuItemData) =>
    language === 'zh' ? item.descZh : language === 'es' ? item.descEs : item.descEn

  const pageLabel = language === 'zh'
    ? `第 ${currentPage + 1} 頁，共 ${totalPages} 頁`
    : `${currentPage + 1} / ${totalPages}`

  return (
    <div
      ref={containerRef}
      className="relative min-h-screen bg-[#2D1810] overflow-hidden pt-20"
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
    >
      {/* 頂部分類標籤列（固定在 Header 下方） */}
      <div className="sticky top-20 z-20 bg-[#1A0F0A]/95 backdrop-blur-md border-b border-white/[0.06]">
        <div className="max-w-7xl mx-auto px-4 py-3 overflow-x-auto scrollbar-hide">
          <div className="flex gap-2 min-w-max" role="tablist" aria-label="Menu categories">
            {menuCategories.map((c, i) => (
              <button
                key={c.id}
                role="tab"
                aria-selected={i === currentPage}
                onClick={() => goToPage(i)}
                className={`px-4 py-2 rounded-full font-body text-sm whitespace-nowrap transition-all duration-300 cursor-pointer focus-visible:ring-2 focus-visible:ring-[hsl(44,80%,40%)] focus-visible:ring-offset-2 focus-visible:ring-offset-[#1A0F0A] ${
                  i === currentPage
                    ? 'bg-[hsl(44,80%,40%)] text-white'
                    : 'text-white/50 hover:text-white hover:bg-white/[0.06]'
                }`}
              >
                {getTitle(c)}
              </button>
            ))}
          </div>
        </div>
      </div>

      {/* 主要內容區域 */}
      <div
        className={`transition-all duration-300 ease-out ${
          isAnimating
            ? direction > 0
              ? 'opacity-0 translate-x-12'
              : 'opacity-0 -translate-x-12'
            : 'opacity-100 translate-x-0'
        }`}
      >
        <div className="max-w-7xl mx-auto px-4 pt-20 pb-12 lg:pt-28 lg:pb-20">
          <div className="grid lg:grid-cols-2 gap-12 lg:gap-20 items-start">
            {/* 左側 - 大圖 */}
            <div className="relative">
              <div className="relative aspect-[4/3] rounded-2xl overflow-hidden shadow-2xl">
                <Image
                  src={cat.image}
                  alt={getTitle(cat)}
                  fill
                  className="object-cover"
                  sizes="(max-width: 1024px) 90vw, 45vw"
                  priority={currentPage === 0}
                />
                {/* 圖片上的漸層 */}
                <div className="absolute inset-0 bg-gradient-to-t from-black/40 via-transparent to-transparent" />
                {/* 示意圖標籤 */}
                <div className="absolute top-3 right-3 bg-black/70 backdrop-blur-sm text-white text-xs font-medium px-3 py-1.5 rounded-full border border-white/20">
                  示意圖
                </div>
              </div>
              {/* 裝飾圓點 */}
              <div className="absolute -top-3 -right-3 h-16 w-16 rounded-full bg-[hsl(44,80%,40%)]/10" />
              <div className="absolute -bottom-2 -left-2 h-10 w-10 rounded-full bg-[hsl(17,45%,57%)]/10" />
            </div>

            {/* 右側 - 品項列表 */}
            <div className="flex flex-col">
              {/* 分類標題 */}
              <div className="mb-10">
                <p className="font-body text-sm font-medium uppercase tracking-[0.2em] text-[hsl(44,80%,40%)] mb-2">
                  {getSubtitle(cat)}
                </p>
                <h2 className="font-heading text-4xl md:text-5xl font-bold text-white">
                  {getTitle(cat)}
                </h2>
                <div className="mt-4 h-0.5 w-16 bg-[hsl(44,80%,40%)]" />
              </div>

              {/* 品項列表 */}
              <div className="space-y-0">
                {cat.items.map((item, idx) => (
                  <div key={idx}>
                    {idx === 0 && <div className="h-px bg-white/[0.06]" />}
                    <div className="py-5 group">
                      <div className="flex items-baseline justify-between gap-4">
                        <h3 className="font-heading text-xl text-white group-hover:text-[hsl(44,80%,60%)] transition-colors">
                          {getName(item)}
                        </h3>
                        <div className="flex items-baseline gap-3 flex-shrink-0">
                          {item.options && (
                            <span className="font-body text-xs text-[hsl(44,80%,40%)]/70 whitespace-nowrap">
                              {item.options}
                            </span>
                          )}
                          {item.price && (
                            <span className="font-heading text-lg text-[hsl(44,80%,50%)] whitespace-nowrap">
                              ${item.price}
                            </span>
                          )}
                        </div>
                      </div>
                      {/* 副名稱 */}
                      <p className="font-body text-sm text-white/60 mt-0.5">
                        {language === 'zh' ? item.nameEn : item.nameZh}
                      </p>
                      {/* 描述 */}
                      {getDesc(item) && (
                        <p className="font-body text-sm text-white/65 mt-1.5 leading-relaxed">
                          {getDesc(item)}
                        </p>
                      )}
                    </div>
                    <div className="h-px bg-white/[0.06]" />
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* 底部導航列 */}
      <div className="absolute bottom-0 left-0 right-0 z-20 bg-gradient-to-t from-[#1A0F0A] via-[#1A0F0A]/80 to-transparent pt-16 pb-8">
        <div className="max-w-7xl mx-auto px-4 flex items-center justify-between">
          {/* 上一頁按鈕 */}
          <button
            onClick={goPrev}
            disabled={currentPage === 0}
            className="flex items-center gap-2 text-white/50 hover:text-white disabled:opacity-20 disabled:cursor-not-allowed transition-all cursor-pointer"
          >
            <ChevronLeft className="w-5 h-5" />
            <span className="font-body text-sm hidden sm:inline">
              {currentPage > 0 ? getTitle(menuCategories[currentPage - 1]) : ''}
            </span>
          </button>

          {/* 頁碼指示器 */}
          <div className="flex items-center gap-3">
            <div className="flex gap-1.5">
              {menuCategories.map((_, i) => (
                <button
                  key={i}
                  onClick={() => goToPage(i)}
                  className={`rounded-full transition-all duration-300 cursor-pointer ${
                    i === currentPage
                      ? 'w-8 h-2 bg-[hsl(44,80%,40%)]'
                      : 'w-2 h-2 bg-white/20 hover:bg-white/40'
                  }`}
                  aria-label={`Go to page ${i + 1}`}
                />
              ))}
            </div>
            <span className="font-body text-xs text-white/60 ml-2">{pageLabel}</span>
          </div>

          {/* 下一頁按鈕 */}
          <button
            onClick={goNext}
            disabled={currentPage === totalPages - 1}
            className="flex items-center gap-2 text-white/50 hover:text-white disabled:opacity-20 disabled:cursor-not-allowed transition-all cursor-pointer"
          >
            <span className="font-body text-sm hidden sm:inline">
              {currentPage < totalPages - 1 ? getTitle(menuCategories[currentPage + 1]) : ''}
            </span>
            <ChevronRight className="w-5 h-5" />
          </button>
        </div>
      </div>
    </div>
  )
}
