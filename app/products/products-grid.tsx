'use client';

import { useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useLanguage } from '@/lib/i18n/language-context';
import type { Product } from '@/types/product';
import { getProductName } from '@/types/product';
import { MapPin, Phone, Clock, ArrowRight } from 'lucide-react';

type CatId = 'tea' | 'fruit' | 'snack';
type FilterId = 'all' | CatId | 'gift';
type Lang = 'zh' | 'en' | 'es';

/* 有精緻直式海報的商品（slug → 海報路徑） */
const POSTERS: Record<string, string> = {
  'honey-aroma-oolong-tea': '/images/products/honey-aroma-oolong-tea.png',
  'dong-pian-oolong-tea': '/images/products/dong-pian-oolong-tea.png',
  'taiwan-roasted-black-bean-tea-15bags': '/images/products/taiwan-roasted-black-bean-tea-15bags.png',
  'fullten-dried-guava': '/images/products/fullten-dried-guava.png',
  'taiwan-osmanthus-plum': '/images/products/taiwan-osmanthus-plum.png',
  'taiwan-perilla-plum': '/images/products/taiwan-perilla-plum.png',
  'jin-he-tai-dried-roselle': '/images/products/jin-he-tai-dried-roselle.png',
  'liao-hsin-lan-dried-tofu-shacha': '/images/products/liao-hsin-lan-dried-tofu-shacha.png',
  'sun-moon-lake-stewed-mushrooms': '/images/products/sun-moon-lake-stewed-mushrooms.png',
};

const CATS: { id: CatId; kicker: string; title: Record<Lang, string> }[] = [
  { id: 'tea', kicker: 'High-Mountain Tea', title: { zh: '台灣高山茶', en: 'Taiwan High-Mountain Tea', es: 'Té de Alta Montaña' } },
  { id: 'fruit', kicker: 'Dried Fruit & Preserves', title: { zh: '台灣果乾蜜餞', en: 'Dried Fruit & Preserves', es: 'Frutas Secas y Confitadas' } },
  { id: 'snack', kicker: 'Snacks & Crackers', title: { zh: '零食餅乾', en: 'Snacks & Crackers', es: 'Snacks y Galletas' } },
];

const FILTERS: { id: FilterId; label: Record<Lang, string> }[] = [
  { id: 'all', label: { zh: '全部', en: 'All', es: 'Todos' } },
  { id: 'tea', label: { zh: '茶葉', en: 'Tea', es: 'Té' } },
  { id: 'fruit', label: { zh: '果乾蜜餞', en: 'Dried Fruit', es: 'Fruta Seca' } },
  { id: 'snack', label: { zh: '零食', en: 'Snacks', es: 'Snacks' } },
  { id: 'gift', label: { zh: '禮盒', en: 'Gift Boxes', es: 'Regalos' } },
];

/* 分類卡的子分組（每個大類拆成幾張大卡） */
const SUBGROUPS: { id: string; cat: CatId; label: Record<Lang, string> }[] = [
  { id: 'oolong', cat: 'tea', label: { zh: '烏龍茶', en: 'Oolong Tea', es: 'Té Oolong' } },
  { id: 'otherTea', cat: 'tea', label: { zh: '紅茶・綠茶・其他', en: 'Black · Green & More', es: 'Negro · Verde y Más' } },
  { id: 'plum', cat: 'fruit', label: { zh: '蜜餞・梅子・糖果', en: 'Preserved Plums & Candy', es: 'Ciruelas y Dulces' } },
  { id: 'driedFruit', cat: 'fruit', label: { zh: '果乾脆片', en: 'Dried Fruit & Chips', es: 'Fruta Seca' } },
  { id: 'snack', cat: 'snack', label: { zh: '鹹食零嘴', en: 'Savory Snacks', es: 'Snacks Salados' } },
];

function categorize(p: Product): CatId {
  const n = p.name_zh || '';
  if (/梅|果乾|芭樂乾|甜蜜柑|脆片|梨糖|洛神/.test(n)) return 'fruit';
  if (/豆干|豆乾|魚酥|香菇|鳳梨酥/.test(n)) return 'snack';
  if (/茶|烏龍|黑糖磚|黑豆/.test(n)) return 'tea';
  return 'snack';
}

function isGift(p: Product): boolean {
  return /禮盒|gift box/i.test(`${p.name_zh || ''} ${p.name_en || ''}`);
}

function subGroupOf(p: Product, cat: CatId): string {
  const n = `${p.name_zh || ''} ${p.name_en || ''}`;
  if (cat === 'tea') return /烏龍|Oolong|鐵觀音|Tieguanyin/.test(n) ? 'oolong' : 'otherTea';
  if (cat === 'fruit') return /乾|脆片|Dried|Chips|柑|Mandarin/.test(n) ? 'driedFruit' : 'plum';
  return 'snack';
}

/* ── 海報卡 ── */
function PosterCard({ p, language, detail, inStore }: { p: Product; language: string; detail: string; inStore: string }) {
  return (
    <Link
      href={`/product/${p.slug}`}
      className="group flex flex-col overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-black/5 transition-shadow duration-300 hover:shadow-md"
    >
      <div className="relative aspect-[2/3] overflow-hidden bg-[#faf7f2]">
        <Image
          src={POSTERS[p.slug]}
          alt={getProductName(p, language)}
          fill
          className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
          sizes="(max-width:768px) 50vw, 33vw"
        />
      </div>
      <div className="flex items-center justify-between gap-2 px-4 py-3">
        <span className="font-body text-sm font-bold text-primary">
          {p.price != null ? `$${Number(p.price).toFixed(2)}` : inStore}
        </span>
        <span className="inline-flex items-center gap-1 font-body text-xs font-semibold text-primary/70 transition-colors group-hover:text-primary">
          {detail}
          <ArrowRight className="h-3.5 w-3.5" />
        </span>
      </div>
    </Link>
  );
}

/* ── 分類列表大卡（品項列在卡內，可點進詳情） ── */
function ListCard({ title, items, lang, language }: { title: string; items: Product[]; lang: Lang; language: string }) {
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-black/5">
      <div className="mb-3 border-b border-primary/15 pb-3">
        <h3 className="font-heading text-lg font-bold text-primary">{title}</h3>
      </div>
      <ul>
        {items.map((p) => (
          <li key={p.id}>
            <Link
              href={`/product/${p.slug}`}
              className="group -mx-2 flex items-baseline justify-between gap-3 rounded-lg px-2 py-2 transition-colors hover:bg-primary/[0.05]"
            >
              <span className="min-w-0 font-body text-sm font-medium leading-snug text-foreground group-hover:text-primary">
                {getProductName(p, language)}
              </span>
              {p.price != null && (
                <span className="shrink-0 font-body text-sm font-bold text-primary">${Number(p.price).toFixed(2)}</span>
              )}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

/* ── 單一分類區塊：海報卡 + 分類列表大卡 ── */
function CategoryBlock({
  catId,
  items,
  showHeader,
  lang,
  language,
  detail,
  inStore,
}: {
  catId: CatId;
  items: Product[];
  showHeader: boolean;
  lang: Lang;
  language: string;
  detail: string;
  inStore: string;
}) {
  if (!items.length) return null;
  const posters = items.filter((p) => POSTERS[p.slug]);
  const lists = items.filter((p) => !POSTERS[p.slug]);
  const cat = CATS.find((c) => c.id === catId)!;
  const groups = SUBGROUPS.filter((sg) => sg.cat === catId)
    .map((sg) => ({ sg, list: lists.filter((p) => subGroupOf(p, catId) === sg.id) }))
    .filter((g) => g.list.length);

  return (
    <section className="mb-16">
      {showHeader && (
        <div className="mb-8 text-center">
          <p className="mb-2 font-heading text-xs uppercase tracking-[0.28em] text-primary/60">{cat.kicker}</p>
          <h2 className="font-heading text-3xl font-bold text-foreground md:text-4xl">{cat.title[lang]}</h2>
          <span className="mx-auto mt-3 block h-1 w-14 rounded-full bg-primary/70" />
        </div>
      )}
      {posters.length > 0 && (
        <div className="mb-6 grid grid-cols-2 gap-5 md:grid-cols-3 md:gap-6">
          {posters.map((p) => (
            <PosterCard key={p.id} p={p} language={language} detail={detail} inStore={inStore} />
          ))}
        </div>
      )}
      {groups.length > 0 && (
        <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
          {groups.map(({ sg, list }) => (
            <ListCard key={sg.id} title={sg.label[lang]} items={list} lang={lang} language={language} />
          ))}
        </div>
      )}
    </section>
  );
}

export default function ProductsGrid({ products }: { products: Product[] }) {
  const { language } = useLanguage();
  const lang: Lang = (['zh', 'en', 'es'] as const).includes(language as Lang) ? (language as Lang) : 'en';
  const [filter, setFilter] = useState<FilterId>('all');

  const inStore = lang === 'zh' ? '店內販售' : lang === 'es' ? 'En tienda' : 'In-store';
  const detail = lang === 'zh' ? '看詳情' : lang === 'es' ? 'Ver más' : 'Details';
  const title = lang === 'zh' ? '台灣零食' : lang === 'es' ? 'Snacks Taiwaneses' : 'Taiwanese Snacks';
  const intro =
    lang === 'zh'
      ? '嚴選台灣好茶、果乾蜜餞與傳統零嘴——歡迎到店選購，把家鄉味帶回家。'
      : lang === 'es'
        ? 'Tés selectos, frutas confitadas y snacks tradicionales de Taiwán — disponibles en tienda.'
        : 'Curated Taiwanese teas, dried fruits and traditional snacks — come pick some up in store.';

  const grouped: Record<CatId, Product[]> = { tea: [], fruit: [], snack: [] };
  products.forEach((p) => grouped[categorize(p)].push(p));

  const emptyLabel = lang === 'zh' ? '此分類目前沒有商品' : lang === 'es' ? 'No hay productos en esta categoría' : 'No products in this category';

  // 依篩選決定要呈現的分類區塊
  let blocks: { catId: CatId; items: Product[] }[] = [];
  if (filter === 'all') {
    blocks = CATS.map((c) => ({ catId: c.id, items: grouped[c.id] }));
  } else if (filter === 'gift') {
    blocks = CATS.map((c) => ({ catId: c.id, items: grouped[c.id].filter(isGift) })).filter((b) => b.items.length);
  } else {
    blocks = [{ catId: filter, items: grouped[filter] }];
  }
  const nothing = blocks.every((b) => b.items.length === 0);

  return (
    <div className="bg-cream">
      {/* 頁首 banner */}
      <div className="mx-auto max-w-5xl px-6 pt-6 pb-4 md:px-8">
        <h1 className="sr-only">{title} — Tea · Snacks · Gifts | TaiwanWay 台灣茶點伴手禮</h1>
        <div className="overflow-hidden rounded-2xl shadow-sm ring-1 ring-black/5">
          <Image
            src="/images/products/gift-wall-banner-wide.png"
            alt="TaiwanWay — Taiwan Tea & Snack 台灣茶伴手禮"
            width={1774}
            height={887}
            priority
            className="h-auto w-full"
            sizes="(max-width:1024px) 100vw, 1024px"
          />
        </div>
        <p className="mx-auto mt-6 max-w-xl text-center font-body text-base text-muted-foreground md:text-lg">{intro}</p>
      </div>

      {/* 分類篩選列（黏頂） */}
      <nav className="sticky top-20 z-30 border-y border-black/5 bg-cream/95 backdrop-blur-md">
        <div className="scrollbar-hide mx-auto max-w-6xl overflow-x-auto px-4 py-3">
          <div className="flex min-w-max justify-center gap-2">
            {FILTERS.map((f) => (
              <button
                key={f.id}
                onClick={() => setFilter(f.id)}
                className={`whitespace-nowrap rounded-full px-5 py-2 font-body text-sm font-semibold transition-colors duration-200 ${
                  filter === f.id ? 'bg-primary text-primary-foreground' : 'text-foreground/60 hover:bg-primary/10 hover:text-primary'
                }`}
              >
                {f.label[lang]}
              </button>
            ))}
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-6xl px-6 py-8 md:px-8">
        {nothing ? (
          <p className="py-16 text-center font-body text-muted-foreground">{emptyLabel}</p>
        ) : (
          blocks.map((b) => (
            <CategoryBlock
              key={b.catId}
              catId={b.catId}
              items={b.items}
              showHeader={filter === 'all' || filter === 'gift'}
              lang={lang}
              language={language}
              detail={detail}
              inStore={inStore}
            />
          ))
        )}

        {/* 到店資訊 */}
        <section className="border-t border-black/5 pt-10 text-center">
          <h2 className="font-heading text-2xl font-bold text-primary">{lang === 'zh' ? '歡迎到店選購' : 'Come Visit Us'}</h2>
          <div className="mx-auto mt-4 flex max-w-xl flex-col items-center gap-2 font-body text-sm text-foreground/80">
            <a
              href="https://www.google.com/maps/search/?api=1&query=TaiwanWay+26+South+St+Middletown+NY+10940"
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-2 hover:text-primary"
            >
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
