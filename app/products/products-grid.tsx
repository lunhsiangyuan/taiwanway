'use client';

import Image from 'next/image';
import Link from 'next/link';
import { useLanguage } from '@/lib/i18n/language-context';
import type { Product } from '@/types/product';
import { getProductName } from '@/types/product';
import { MapPin, Phone, Clock } from 'lucide-react';

type CatId = 'tea' | 'fruit' | 'snack';

const CATS: { id: CatId; title: Record<string, string>; banner: string }[] = [
  { id: 'tea', title: { zh: '台灣高山茶', en: 'Taiwan High-Mountain Tea', es: 'Té de Alta Montaña' }, banner: '/images/menu-cards/snack-tea.png' },
  { id: 'fruit', title: { zh: '台灣果乾蜜餞', en: 'Dried Fruit & Preserves', es: 'Frutas Secas y Confitadas' }, banner: '/images/menu-cards/snack-plum.png' },
  { id: 'snack', title: { zh: '零食餅乾', en: 'Snacks & Crackers', es: 'Snacks y Galletas' }, banner: '/images/menu-cards/snack-savory.png' },
];

function categorize(p: Product): CatId {
  const n = p.name_zh || '';
  if (/梅|果乾|芭樂乾|甜蜜柑|脆片|梨糖|洛神/.test(n)) return 'fruit';
  if (/豆干|魚酥|香菇燒|鳳梨酥/.test(n)) return 'snack';
  if (/茶|烏龍|黑糖磚|黑豆茶/.test(n)) return 'tea';
  return 'snack';
}

export default function ProductsGrid({ products }: { products: Product[] }) {
  const { language } = useLanguage();
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en';

  const inStore = lang === 'zh' ? '店內販售' : lang === 'es' ? 'En tienda' : 'In-store';
  const title = lang === 'zh' ? '台灣零食' : lang === 'es' ? 'Snacks Taiwaneses' : 'Taiwanese Snacks';
  const intro = lang === 'zh'
    ? '嚴選台灣好茶、果乾蜜餞與傳統零嘴——歡迎到店選購，把家鄉味帶回家。'
    : lang === 'es'
      ? 'Tés selectos, frutas confitadas y snacks tradicionales de Taiwán — disponibles en tienda.'
      : 'Curated Taiwanese teas, dried fruits and traditional snacks — come pick some up in store.';

  const grouped: Record<CatId, Product[]> = { tea: [], fruit: [], snack: [] };
  products.forEach((p) => grouped[categorize(p)].push(p));

  return (
    <div className="bg-cream">
      <div className="mx-auto max-w-6xl px-6 pt-8 pb-6 text-center md:px-8">
        <p className="mb-2 font-heading text-sm uppercase tracking-[0.28em] text-primary/70">Snacks · Gifts · Tea</p>
        <h1 className="font-heading text-5xl font-bold text-[#5b3a2e] md:text-6xl">{title}</h1>
        <p className="mx-auto mt-4 max-w-xl font-body text-base text-muted-foreground md:text-lg">{intro}</p>
      </div>

      <div className="mx-auto max-w-6xl px-6 py-8 md:px-8">
        {CATS.map((cat) => {
          const items = grouped[cat.id];
          if (!items.length) return null;
          return (
            <section key={cat.id} className="mb-14">
              <div className="mb-8 overflow-hidden rounded-2xl shadow-md ring-1 ring-black/5">
                <Image src={cat.banner} alt={cat.title[lang]} width={1536} height={1024} className="h-auto w-full" sizes="(max-width:1152px) 100vw, 1152px" />
              </div>

              <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 md:gap-6">
                {items.map((p) => (
                  <Link key={p.id} href={`/product/${p.slug}`} className="group flex flex-col overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-black/5 transition-shadow duration-300 hover:shadow-md">
                    <div className="relative aspect-square bg-[#faf7f2]">
                      {p.image_url ? (
                        <Image src={p.image_url} alt={getProductName(p, language)} fill className="object-contain p-3 transition-transform duration-300 group-hover:scale-105" sizes="(max-width:640px) 45vw, 22vw" />
                      ) : null}
                    </div>
                    <div className="flex flex-1 flex-col p-4">
                      {p.brand && <p className="font-body text-[11px] uppercase tracking-wide text-primary/60">{p.brand}</p>}
                      <h3 className="mt-0.5 font-body text-sm font-semibold leading-snug text-foreground group-hover:text-primary">{getProductName(p, language)}</h3>
                      <div className="mt-auto flex items-center justify-between gap-2 pt-3">
                        <span className="rounded-full bg-primary/[0.08] px-2 py-0.5 font-body text-[11px] font-medium text-primary/80">{inStore}</span>
                        {p.price != null && <span className="font-body text-base font-bold text-primary">${Number(p.price).toFixed(2)}</span>}
                      </div>
                    </div>
                  </Link>
                ))}
              </div>
            </section>
          );
        })}

        <section className="border-t border-black/5 pt-10 text-center">
          <h2 className="font-heading text-2xl font-bold text-primary">{lang === 'zh' ? '歡迎到店選購' : 'Come Visit Us'}</h2>
          <div className="mx-auto mt-4 flex max-w-xl flex-col items-center gap-2 font-body text-sm text-foreground/80">
            <a href="https://www.google.com/maps/search/?api=1&query=TaiwanWay+26+South+St+Middletown+NY+10940" target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 hover:text-primary">
              <MapPin className="h-4 w-4 text-primary" />26 South St, Middletown, NY 10940
            </a>
            <a href="tel:+18453811002" className="flex items-center gap-2 hover:text-primary">
              <Phone className="h-4 w-4 text-primary" />(845) 381-1002
            </a>
            <p className="flex items-center gap-2">
              <Clock className="h-4 w-4 text-primary" />{lang === 'zh' ? '週一・二・五・六 11AM–7PM' : 'Mon · Tue · Fri · Sat 11AM–7PM'}
            </p>
          </div>
        </section>
      </div>
    </div>
  );
}
