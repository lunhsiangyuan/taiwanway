'use client'

import { useEffect, useState, useRef } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'
import Image from 'next/image'
import Link from 'next/link'

type Product = {
  id: string
  slug: string
  image_url: string
  price: number | null
  brand: string | null
  name_zh: string
  name_en: string
  name_es: string
  description_zh: string
  description_en: string
  description_es: string
}

export function SnackShop() {
  const { language } = useLanguage()
  const [products, setProducts] = useState<Product[]>([])
  const [isVisible, setIsVisible] = useState(false)
  const sectionRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) setIsVisible(true) },
      { threshold: 0.1 }
    )
    if (sectionRef.current) observer.observe(sectionRef.current)
    return () => observer.disconnect()
  }, [])

  useEffect(() => {
    fetch('/api/products')
      .then((r) => r.json())
      .then((data) => setProducts(Array.isArray(data) ? data : []))
      .catch(() => {})
  }, [])

  const title = { zh: '台灣零食專賣', en: 'Taiwanese Snacks', es: 'Snacks Taiwaneses' }[language]
  const subtitle = {
    zh: '精選台灣好物，掃碼了解更多',
    en: 'Curated goods from Taiwan — scan QR codes in store to learn more',
    es: 'Productos selectos de Taiwán — escanea el código QR en la tienda',
  }[language]
  const viewAll = { zh: '查看全部', en: 'View All', es: 'Ver Todos' }[language]

  if (products.length === 0) return null

  return (
    <section ref={sectionRef} className="relative bg-[#FAF7F2] py-24 overflow-hidden">
      <div className="absolute -top-32 -left-32 h-[400px] w-[400px] rounded-full bg-[hsl(44,80%,40%)]/[0.05] blur-3xl" />

      <div className="relative mx-auto max-w-6xl px-4">
        <div className={`mb-16 text-center transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          <h2 className="font-heading text-4xl font-bold text-[#2D1810] md:text-5xl">
            {title}
          </h2>
          <div className="mx-auto mt-4 h-0.5 w-20 bg-[hsl(44,80%,40%)]" />
          <p className="mx-auto mt-4 max-w-xl font-body text-lg text-[hsl(17,20%,40%)]">
            {subtitle}
          </p>
        </div>

        <div className={`grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6 transition-all duration-700 delay-200 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
          {products.slice(0, 8).map((p) => {
            const name = p[`name_${language}`] || p.name_en
            const desc = p[`description_${language}`] || p.description_en
            return (
              <Link
                key={p.id}
                href={`/product/${p.slug}`}
                className="group bg-white rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1"
              >
                <div className="relative aspect-square bg-[#FAF7F2]">
                  <Image
                    src={p.image_url}
                    alt={name}
                    fill
                    className="object-contain p-3 group-hover:scale-105 transition-transform duration-300"
                    sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, 25vw"
                  />
                </div>
                <div className="p-4">
                  {p.brand && (
                    <p className="text-[10px] text-[hsl(17,45%,57%)] uppercase tracking-wider font-medium">{p.brand}</p>
                  )}
                  <h3 className="font-heading font-semibold text-sm text-[#2D1810] leading-tight mt-1 group-hover:text-[hsl(17,45%,57%)] transition-colors">
                    {name}
                  </h3>
                  <p className="text-xs text-[hsl(17,20%,40%)] mt-1.5 line-clamp-2">{desc}</p>
                  {p.price && (
                    <p className="font-heading font-bold text-[hsl(17,45%,57%)] text-sm mt-2">
                      ${Number(p.price).toFixed(2)}
                    </p>
                  )}
                </div>
              </Link>
            )
          })}
        </div>

        {products.length > 0 && (
          <div className={`mt-12 text-center transition-all duration-700 delay-400 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'}`}>
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
  )
}
