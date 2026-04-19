'use client'

import { useEffect, useState, useRef } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'
import Image from 'next/image'
import Link from 'next/link'
import type { Product } from '@/types/product'

/** 判斷商品是否為「目前有效」的 new arrival（勾選 + 未過截止日） */
function isActiveNewArrival(p: Product): boolean {
  if (!p.is_new_arrival) return false
  if (!p.featured_until) return true
  const today = new Date().toISOString().slice(0, 10)
  return p.featured_until >= today
}

function ProductCard({
  product,
  language,
  showNewBadge = false,
}: {
  product: Product
  language: 'zh' | 'en' | 'es'
  showNewBadge?: boolean
}) {
  const name = product[`name_${language}`] || product.name_en
  const desc = product[`description_${language}`] || product.description_en
  return (
    <Link
      href={`/product/${product.slug}`}
      className="group relative bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
    >
      {showNewBadge && (
        <div className="absolute top-3 right-3 z-10 bg-[hsl(44,80%,45%)] text-white text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full shadow-md">
          NEW
        </div>
      )}
      <div className="relative aspect-square bg-[#FAF7F2]">
        <Image
          src={product.image_url}
          alt={name}
          fill
          className="object-contain p-3 group-hover:scale-105 transition-transform duration-300"
          sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, 25vw"
        />
      </div>
      <div className="p-4">
        {product.brand && (
          <p className="text-[10px] text-[hsl(17,45%,57%)] uppercase tracking-wider font-medium">
            {product.brand}
          </p>
        )}
        <h3 className="font-heading font-semibold text-sm text-[#2D1810] leading-tight mt-1 group-hover:text-[hsl(17,45%,57%)] transition-colors">
          {name}
        </h3>
        <p className="text-xs text-[hsl(17,20%,40%)] mt-1.5 line-clamp-2">{desc}</p>
        {product.price && (
          <p className="font-heading font-bold text-[hsl(17,45%,57%)] text-sm mt-2">
            ${Number(product.price).toFixed(2)}
          </p>
        )}
      </div>
    </Link>
  )
}

export function SnackShop() {
  const { language } = useLanguage()
  const [products, setProducts] = useState<Product[]>([])
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    fetch('/api/products')
      .then((r) => r.json())
      .then((data) => setProducts(Array.isArray(data) ? data : []))
      .catch(() => {})
  }, [])

  useEffect(() => {
    if (products.length === 0) return
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) setIsVisible(true)
      },
      { threshold: 0.1 }
    )
    if (sectionRef.current) observer.observe(sectionRef.current)
    return () => observer.disconnect()
  }, [products.length])

  const title = { zh: '台灣零食專賣', en: 'Taiwanese Snacks', es: 'Snacks Taiwaneses' }[language]
  const subtitle = {
    zh: '精選台灣好物，掃碼了解更多',
    en: 'Curated goods from Taiwan — scan QR codes in store to learn more',
    es: 'Productos selectos de Taiwán — escanea el código QR en la tienda',
  }[language]
  const newArrivalTitle = {
    zh: '本月新品．限量供應',
    en: "This Month's New Arrivals · Limited",
    es: 'Novedades del Mes · Edición Limitada',
  }[language]
  const newArrivalSubtitle = {
    zh: '每月精選、當月限定，售完為止',
    en: 'Curated monthly · While supplies last',
    es: 'Selección mensual · Hasta agotar existencias',
  }[language]
  const viewAll = { zh: '查看全部', en: 'View All', es: 'Ver Todos' }[language]

  if (products.length === 0) return null

  const newArrivals = products.filter(isActiveNewArrival)
  const regularProducts = products.filter((p) => !isActiveNewArrival(p))

  return (
    <>
      {/* ============ New Arrival 區塊（金色背景） ============ */}
      {newArrivals.length > 0 && (
        <section className="relative bg-gradient-to-b from-[#FBF3DF] via-[#F7EACB] to-[#FBF3DF] py-20 overflow-hidden">
          {/* 裝飾光暈 */}
          <div className="absolute -top-24 left-1/2 -translate-x-1/2 h-[500px] w-[500px] rounded-full bg-[hsl(44,80%,55%)]/[0.15] blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 right-0 h-[300px] w-[300px] rounded-full bg-[hsl(44,80%,40%)]/[0.08] blur-3xl pointer-events-none" />

          <div className="relative mx-auto max-w-6xl px-4">
            {/* 區塊標題 */}
            <div className="mb-12 text-center">
              <div className="inline-flex items-center gap-2 mb-3">
                <span className="h-px w-12 bg-[hsl(44,60%,40%)]/40" />
                <span className="text-[11px] uppercase tracking-[0.3em] font-semibold text-[hsl(44,60%,35%)]">
                  New Arrival
                </span>
                <span className="h-px w-12 bg-[hsl(44,60%,40%)]/40" />
              </div>
              <h2 className="font-heading text-3xl font-bold text-[#2D1810] md:text-4xl">
                {newArrivalTitle}
              </h2>
              <p className="mx-auto mt-3 max-w-xl font-body text-base text-[hsl(17,20%,35%)]">
                {newArrivalSubtitle}
              </p>
            </div>

            {/* 商品 grid */}
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
              {newArrivals.slice(0, 8).map((p) => (
                <ProductCard key={p.id} product={p} language={language} showNewBadge />
              ))}
            </div>
          </div>
        </section>
      )}

      {/* ============ 一般商品區 ============ */}
      <section ref={sectionRef} className="relative bg-[#FAF7F2] py-24 overflow-hidden">
        <div className="absolute -top-32 -left-32 h-[400px] w-[400px] rounded-full bg-[hsl(44,80%,40%)]/[0.05] blur-3xl" />

        <div className="relative mx-auto max-w-6xl px-4">
          <div
            className={`mb-16 text-center transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}
          >
            <h2 className="font-heading text-4xl font-bold text-[#2D1810] md:text-5xl">
              {title}
            </h2>
            <div className="mx-auto mt-4 h-0.5 w-20 bg-[hsl(44,80%,40%)]" />
            <p className="mx-auto mt-4 max-w-xl font-body text-lg text-[hsl(17,20%,40%)]">
              {subtitle}
            </p>
          </div>

          <div
            className={`grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6 transition-all duration-700 delay-200 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}
          >
            {regularProducts.slice(0, 8).map((p) => (
              <ProductCard key={p.id} product={p} language={language} />
            ))}
          </div>

          {regularProducts.length > 0 && (
            <div
              className={`mt-12 text-center transition-all duration-700 delay-400 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}
            >
              <Link
                href="/products"
                className="inline-block rounded-full border-2 border-[#2D1810] px-8 py-3 font-heading text-sm font-semibold text-[#2D1810] transition-colors hover:bg-[#2D1810] hover:text-white"
              >
                {viewAll} →
              </Link>
            </div>
          )}
        </div>
      </section>
    </>
  )
}
