'use client';

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
  how_to_use_zh: string | null;
  how_to_use_en: string | null;
  how_to_use_es: string | null;
  origin: string | null;
};

const langLabel = { zh: '中文', en: 'EN', es: 'ES' } as const;

export default function ProductDetail({ product }: { product: Product }) {
  const { language, setLanguage } = useLanguage();

  const name = product[`name_${language}`] || product.name_en;
  const description = product[`description_${language}`] || product.description_en;
  const howToUse = product[`how_to_use_${language}`] || product.how_to_use_en;

  return (
    <div className="min-h-screen bg-amber-50">
      {/* Header */}
      <header className="bg-amber-900 text-white py-3 px-4 flex items-center justify-between">
        <Link href="/" className="text-lg font-bold tracking-wide">
          台灣味 Taiwanway
        </Link>
        <div className="flex gap-1">
          {(['zh', 'en', 'es'] as const).map((lang) => (
            <button
              key={lang}
              onClick={() => setLanguage(lang)}
              className={`px-2 py-1 rounded text-sm font-medium transition-colors ${
                language === lang
                  ? 'bg-white text-amber-900'
                  : 'bg-amber-800 text-amber-100 hover:bg-amber-700'
              }`}
            >
              {langLabel[lang]}
            </button>
          ))}
        </div>
      </header>

      {/* Product Image */}
      <div className="relative w-full aspect-square max-w-lg mx-auto bg-white">
        <Image
          src={product.image_url}
          alt={name}
          fill
          className="object-contain p-4"
          sizes="(max-width: 768px) 100vw, 512px"
          priority
        />
      </div>

      {/* Product Info */}
      <div className="max-w-lg mx-auto px-4 py-6 space-y-4">
        {product.brand && (
          <p className="text-sm text-amber-700 font-medium uppercase tracking-wider">
            {product.brand}
          </p>
        )}

        <div className="flex items-start justify-between gap-4">
          <h1 className="text-2xl font-bold text-amber-950 leading-tight">
            {name}
          </h1>
          {product.price && (
            <span className="text-2xl font-bold text-amber-800 whitespace-nowrap">
              ${Number(product.price).toFixed(2)}
            </span>
          )}
        </div>

        {product.origin && (
          <p className="text-sm text-amber-600">📍 {product.origin}</p>
        )}

        <div className="bg-white rounded-xl p-4 shadow-sm border border-amber-100">
          <p className="text-amber-900 leading-relaxed whitespace-pre-line">
            {description}
          </p>
        </div>

        {howToUse && (
          <div className="bg-amber-100 rounded-xl p-4">
            <h2 className="font-semibold text-amber-900 mb-2">
              {language === 'zh' ? '🍵 食用方式' : language === 'es' ? '🍵 Modo de uso' : '🍵 How to Use'}
            </h2>
            <p className="text-amber-800 leading-relaxed whitespace-pre-line">
              {howToUse}
            </p>
          </div>
        )}

        <div className="text-center pt-4 pb-8">
          <Link
            href="/products"
            className="inline-block bg-amber-800 text-white px-6 py-3 rounded-full font-medium hover:bg-amber-900 transition-colors"
          >
            {language === 'zh' ? '探索更多台灣味' : language === 'es' ? 'Explorar más' : 'Explore Taiwanway'}
          </Link>
          <p className="mt-3 text-xs text-amber-500">
            26 South St, Middletown, NY 10940
          </p>
        </div>
      </div>
    </div>
  );
}
