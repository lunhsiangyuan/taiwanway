'use client';

import { useEffect, useState } from 'react';
import { useLanguage } from '@/lib/i18n/language-context';
import Image from 'next/image';
import Link from 'next/link';

type Product = {
  id: string;
  slug: string;
  image_url: string;
  price: number | null;
  brand: string | null;
  name_zh: string;
  name_en: string;
  name_es: string;
  description_zh: string;
  description_en: string;
  description_es: string;
};

export default function ProductsPage() {
  const { language } = useLanguage();
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('/api/products')
      .then((r) => r.json())
      .then((data) => setProducts(Array.isArray(data) ? data : []))
      .catch(() => {})
      .finally(() => setLoading(false));
  }, []);

  const title = { zh: '我們的產品', en: 'Our Products', es: 'Nuestros Productos' }[language];
  const subtitle = {
    zh: '精選台灣好物，掃碼了解更多',
    en: 'Curated Taiwanese goods — scan to learn more',
    es: 'Productos taiwaneses seleccionados',
  }[language];

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-amber-50">
        <div className="animate-pulse text-amber-800">Loading...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-amber-50">
      <header className="bg-amber-900 text-white py-6 px-4 text-center">
        <Link href="/" className="text-lg font-bold tracking-wide">
          台灣味 Taiwanway
        </Link>
        <h1 className="text-2xl font-bold mt-2">{title}</h1>
        <p className="text-amber-200 text-sm mt-1">{subtitle}</p>
      </header>

      <div className="max-w-5xl mx-auto px-4 py-8">
        {products.length === 0 ? (
          <p className="text-center text-amber-700 py-12">
            {language === 'zh' ? '即將上架，敬請期待！' : 'Coming soon!'}
          </p>
        ) : (
          <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-4">
            {products.map((p) => {
              const name = p[`name_${language}`] || p.name_en;
              const desc = p[`description_${language}`] || p.description_en;
              return (
                <Link
                  key={p.id}
                  href={`/product/${p.slug}`}
                  className="bg-white rounded-xl overflow-hidden shadow-sm hover:shadow-md transition-shadow"
                >
                  <div className="relative aspect-square bg-gray-50">
                    <Image
                      src={p.image_url}
                      alt={name}
                      fill
                      className="object-contain p-2"
                      sizes="(max-width: 640px) 50vw, (max-width: 768px) 33vw, 25vw"
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

      <footer className="text-center py-6 text-xs text-amber-500">
        <Link href="/" className="hover:underline">
          ← {language === 'zh' ? '回到台灣味' : 'Back to Taiwanway'}
        </Link>
      </footer>
    </div>
  );
}
