'use client'

import { useState } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'
import { ProductCard } from './product-card'
import { PRODUCTS, CATEGORIES, getProductsByCategory } from '@/lib/menu-data'

/**
 * 分類中文名稱
 */
const CATEGORY_NAMES = {
  [CATEGORIES.MAIN_DISHES]: {
    zh: '主餐',
    en: 'Main Dishes',
    es: 'Platos Principales',
  },
  [CATEGORIES.BUBBLE_TEA]: {
    zh: '珍珠奶茶系列',
    en: 'Bubble Tea Series',
    es: 'Serie de Té de Burbujas',
  },
  [CATEGORIES.MILK_TEA]: {
    zh: '奶茶系列',
    en: 'Milk Tea Series',
    es: 'Serie de Té con Leche',
  },
  [CATEGORIES.GREEN_TEA]: {
    zh: '綠茶系列',
    en: 'Green Tea Series',
    es: 'Serie de Té Verde',
  },
  [CATEGORIES.LEMONADE]: {
    zh: '檸檬飲品',
    en: 'Lemonade',
    es: 'Limonada',
  },
  [CATEGORIES.DESSERTS]: {
    zh: '甜點',
    en: 'Desserts',
    es: 'Postres',
  },
}

type ViewMode = 'grid' | 'list'

/**
 * 產品展示組件 - 春水堂風格
 *
 * 功能：
 * - 分類導航（側邊欄或頂部）
 * - Grid/List 視圖切換
 * - 響應式設計
 * - 平滑捲動到分類
 */
export function ProductsShowcase() {
  const { language } = useLanguage()
  const [viewMode, setViewMode] = useState<ViewMode>('grid')
  const [activeCategory, setActiveCategory] = useState<string>(CATEGORIES.MAIN_DISHES)

  // 取得分類名稱
  const getCategoryName = (category: string) => {
    const names = CATEGORY_NAMES[category as keyof typeof CATEGORY_NAMES]
    return names?.[language as keyof typeof names] || names?.zh || category
  }

  // 平滑捲動到分類
  const scrollToCategory = (category: string) => {
    setActiveCategory(category)
    const element = document.getElementById(category)
    if (element) {
      element.scrollIntoView({ behavior: 'smooth', block: 'start' })
    }
  }

  return (
    <div className="bg-gray-50 min-h-screen">
      {/* 頂部工具列 */}
      <div className="bg-white border-b sticky top-0 z-10 shadow-sm">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            {/* 分類導航（桌面版） */}
            <nav className="hidden md:flex space-x-6 overflow-x-auto" role="tablist" aria-label="Menu categories">
              {Object.values(CATEGORIES).map((category) => {
                const products = getProductsByCategory(category)
                if (products.length === 0) return null

                return (
                  <button
                    key={category}
                    role="tab"
                    aria-selected={activeCategory === category}
                    onClick={() => scrollToCategory(category)}
                    className={`whitespace-nowrap px-4 py-2 rounded-full font-medium transition-all ${
                      activeCategory === category
                        ? 'bg-amber-600 text-white'
                        : 'text-gray-600 hover:bg-gray-100'
                    }`}
                  >
                    {getCategoryName(category)}
                  </button>
                )
              })}
            </nav>

            {/* 視圖切換 */}
            <div className="flex items-center space-x-2 bg-gray-100 rounded-lg p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  viewMode === 'grid'
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
                </svg>
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                  viewMode === 'list'
                    ? 'bg-white text-gray-900 shadow-sm'
                    : 'text-gray-600 hover:text-gray-900'
                }`}
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                </svg>
              </button>
            </div>
          </div>

          {/* 分類導航（手機版） */}
          <div className="md:hidden mt-4 overflow-x-auto">
            <div className="flex space-x-3 pb-2" role="tablist" aria-label="Menu categories">
              {Object.values(CATEGORIES).map((category) => {
                const products = getProductsByCategory(category)
                if (products.length === 0) return null

                return (
                  <button
                    key={category}
                    role="tab"
                    aria-selected={activeCategory === category}
                    onClick={() => scrollToCategory(category)}
                    className={`whitespace-nowrap px-4 py-2 rounded-full text-sm font-medium transition-all ${
                      activeCategory === category
                        ? 'bg-amber-600 text-white'
                        : 'bg-gray-100 text-gray-600'
                    }`}
                  >
                    {getCategoryName(category)}
                  </button>
                )
              })}
            </div>
          </div>
        </div>
      </div>

      {/* 產品列表 */}
      <div className="container mx-auto px-4 py-8">
        {Object.values(CATEGORIES).map((category) => {
          const products = getProductsByCategory(category)
          if (products.length === 0) return null

          return (
            <section
              key={category}
              id={category}
              className="mb-16 scroll-mt-32"
            >
              {/* 分類標題 */}
              <div className="mb-8">
                <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-2">
                  {getCategoryName(category)}
                </h2>
                <div className="w-20 h-1 bg-amber-600 rounded-full"></div>
              </div>

              {/* 產品網格/列表 */}
              {viewMode === 'grid' ? (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
                  {products.map((product) => (
                    <ProductCard key={product.id} product={product} variant="grid" />
                  ))}
                </div>
              ) : (
                <div className="space-y-6">
                  {products.map((product) => (
                    <ProductCard key={product.id} product={product} variant="list" />
                  ))}
                </div>
              )}
            </section>
          )
        })}
      </div>
    </div>
  )
}
