'use client';

import Image from 'next/image';
import Link from 'next/link';
import { useLanguage } from '@/lib/i18n/language-context';
import type { Product } from '@/types/product';
import { getProductName, getProductDescription } from '@/types/product';

export default function ProductsGrid({ products }: { products: Product[] }) {
  const { language } = useLanguage();

  const title = { zh: '我們的產品', en: 'Our Products', es: 'Nuestros Productos' }[language];
  const subtitle = {
    zh: '精選台灣好物，掃碼了解更多',
    en: 'Curated Taiwanese goods — scan to learn more',
    es: 'Productos taiwaneses seleccionados',
  }[language];

  return (
    <>
      <div className="bg-amber-900 text-white py-8 px-4 text-center">
        <h1 className="text-2xl font-bold">{title}</h1>
        <p className="text-amber-200 text-sm mt-1">{subtitle}</p>
      </div>

      <div className="max-w-5xl mx-auto px-4 py-8">
        {products.length === 0 ? (
          <p className="text-center text-amber-700 py-12">
            {language === 'zh' ? '即將上架，敬請期待！' : 'Coming soon!'}
          </p>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {products.map((p) => {
              const name = getProductName(p, language);
              const desc = getProductDescription(p, language);
              return (
                <Link
                  key={p.id}
                  href={`/product/${p.slug}`}
                  className="relative bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
                >
                  {p.is_new_arrival && (!p.featured_until || p.featured_until >= new Date().toISOString().slice(0, 10)) && (
                    <div className="absolute top-2 right-2 z-10 bg-amber-500 text-white text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full shadow">
                      NEW
                    </div>
                  )}
                  <div className="relative aspect-square bg-gray-50">
                    <Image
                      src={p.image_url}
                      alt={name}
                      fill
                      className="object-contain p-2"
                      sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, 25vw"
                      loading="lazy"
                    />
                  </div>
                  <div className="p-3">
                    {p.brand && (
                      <p className="text-[10px] text-amber-600 uppercase tracking-wider">{p.brand}</p>
                    )}
                    <h3 className="font-semibold text-sm text-amber-950 leading-tight mt-0.5">{name}</h3>
                    <p className="text-xs text-gray-500 mt-1 line-clamp-2">{desc}</p>
                    {p.price && (
                      <p className="font-bold text-amber-800 text-sm mt-2">${Number(p.price).toFixed(2)}</p>
                    )}
                  </div>
                </Link>
              );
            })}
          </div>
        )}
      </div>

      <div className="text-center py-6 text-xs text-amber-500">
        <Link href="/" className="hover:underline">
          ← {language === 'zh' ? '回到台灣味' : 'Back to Taiwanway'}
        </Link>
      </div>
    </>
  );
}
