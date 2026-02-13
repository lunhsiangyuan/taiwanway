'use client'

import Image from 'next/image'
import { useLanguage } from '@/lib/i18n/language-context'
import type { Product } from '@/lib/menu-data'

interface ProductCardProps {
  product: Product
  variant?: 'grid' | 'list'
}

/**
 * 產品卡片組件 - 模仿春水堂風格
 *
 * 特色：
 * - 大圖置頂（使用優化的 WebP）
 * - 多語言名稱（中/英/西）
 * - 分類標籤
 * - 詳細描述（故事性文字）
 * - 價格顯示
 * - 過敏原資訊
 */
export function ProductCard({ product, variant = 'grid' }: ProductCardProps) {
  const { language, t } = useLanguage()

  const imageSrc = variant === 'grid' ? product.image.product : product.image.thumbnail
  const name = product.name[language as keyof typeof product.name] || product.name.zh
  const description = product.description[language as keyof typeof product.description] || product.description.zh

  if (variant === 'list') {
    return (
      <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
        <div className="flex flex-col md:flex-row">
          {/* 圖片區 */}
          <div className="relative w-full md:w-64 h-48 md:h-auto flex-shrink-0">
            <Image
              src={imageSrc}
              alt={name}
              fill
              className="object-cover"
              sizes="(min-width: 768px) 256px, 100vw"
            />
          </div>

          {/* 內容區 */}
          <div className="p-6 flex flex-col justify-between flex-1">
            {/* 標籤 */}
            {product.tags.length > 0 && (
              <div className="flex flex-wrap gap-2 mb-3">
                {product.tags.map((tag) => (
                  <span
                    key={tag}
                    className="px-3 py-1 text-xs font-medium bg-amber-100 text-amber-800 rounded-full"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            )}

            {/* 名稱 */}
            <div className="mb-3">
              <h3 className="text-2xl font-bold text-gray-900 mb-1">
                {product.name.zh}
              </h3>
              <p className="text-sm text-gray-500 italic">
                {product.name.en}
              </p>
            </div>

            {/* 描述 */}
            <p className="text-gray-700 text-sm leading-relaxed mb-4 flex-1">
              {description}
            </p>

            {/* 底部資訊 - 僅顯示過敏原 */}
            {product.allergens && product.allergens.length > 0 && (
              <div className="pt-4 border-t border-gray-200">
                <span className="text-xs text-gray-500">
                  過敏原：{product.allergens.join(', ')}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>
    )
  }

  // Grid 版本（預設）
  return (
    <div className="bg-white rounded-xl shadow-md overflow-hidden hover:shadow-xl transition-all duration-300 hover:-translate-y-1">
      {/* 圖片區 */}
      <div className="relative w-full h-64 overflow-hidden">
        <Image
          src={imageSrc}
          alt={name}
          fill
          className="object-cover transition-transform duration-300 hover:scale-105"
          sizes="(min-width: 1024px) 25vw, (min-width: 768px) 50vw, 100vw"
        />
      </div>

      {/* 內容區 */}
      <div className="p-6">
        {/* 標籤 */}
        {product.tags.length > 0 && (
          <div className="flex flex-wrap gap-2 mb-3">
            {product.tags.map((tag) => (
              <span
                key={tag}
                className="px-2 py-1 text-xs font-medium bg-amber-100 text-amber-800 rounded-full"
              >
                {tag}
              </span>
            ))}
          </div>
        )}

        {/* 名稱 */}
        <div className="mb-3">
          <h3 className="text-xl font-bold text-gray-900 mb-1">
            {product.name.zh}
          </h3>
          <p className="text-xs text-gray-500 italic">
            {product.name.en}
          </p>
        </div>

        {/* 描述（限制行數） */}
        <p className="text-gray-700 text-sm leading-relaxed mb-4 line-clamp-3">
          {description}
        </p>

        {/* 底部資訊 - 價格已移除 */}
        {product.allergens && product.allergens.length > 0 && (
          <div className="pt-4 border-t border-gray-200">
            <span className="text-xs text-gray-500">
              過敏原：{product.allergens.join(', ')}
            </span>
          </div>
        )}

        {/* 備註 */}
        <p className="text-xs text-gray-400 mt-3 italic">
          {language === 'zh'
            ? '圖片僅供參考，商品以實際現場供應為主。'
            : 'Images are for reference only. Actual products may vary.'}
        </p>
      </div>
    </div>
  )
}
