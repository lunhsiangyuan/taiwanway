'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import Link from 'next/link'
import { useLanguage } from '@/lib/i18n/language-context'
import { menuCategories, type MenuCategory, type MenuItemData } from './menu-carousel'
import { Soup, CupSoda, Coffee, CakeSlice, MapPin, Phone, Clock, Truck, type LucideIcon } from 'lucide-react'

type Lang = 'zh' | 'en' | 'es'

const UBER = 'https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A'
const DOORDASH = 'https://www.doordash.com/store/taiwan-way-middletown-42843267/'
const MAPS = 'https://www.google.com/maps/search/?api=1&query=TaiwanWay+26+South+St+Middletown+NY+10940'

/* 品項 → 照片檔名 */
const PHOTOS: Record<string, string> = {
  '紅燒牛肉麵': 'beef-noodle.jpg',
  '麻醬牛肉乾麵': 'dried-beef-noodles.png',
  '古早味滷肉飯': 'braised-pork-rice.jpg',
  '雞肉飯': 'chicken-rice.jpg',
  '櫻花蝦米糕': 'sticky-rice.png',
  '芋頭餅': 'taro-cake.png',
  '台灣鳳梨酥': 'pineapple-cake.jpg',
  '每日現做各式起司蛋糕': 'cheesecake.jpg',
}

/* 品項 → 手繪 SVG icon */
const ICON_SVG: Record<string, string> = {
  '紅燒牛肉麵': '/images/icons/icon-braised-beef-noodle-soup.svg',
  '麻醬牛肉乾麵': '/images/icons/icon-sesame-beef-dry-noodles.svg',
  '古早味滷肉飯': '/images/icons/icon-braised-pork-rice.svg',
  '雞肉飯': '/images/icons/icon-chicken-rice.svg',
  '櫻花蝦米糕': '/images/icons/icon-sakura-shrimp-sticky-rice.svg',
}

/* 標籤定義：hot=人氣、rec=主廚推薦、diet=成分/過敏原 */
type TagKind = 'hot' | 'rec' | 'diet'
const T: Record<string, { label: Record<Lang, string>; kind: TagKind }> = {
  hot: { label: { zh: '人氣', en: 'Popular', es: 'Popular' }, kind: 'hot' },
  rec: { label: { zh: '主廚推薦', en: "Chef's Pick", es: 'Recomendado' }, kind: 'rec' },
  beef: { label: { zh: '含牛肉', en: 'Beef', es: 'Res' }, kind: 'diet' },
  pork: { label: { zh: '含豬肉', en: 'Pork', es: 'Cerdo' }, kind: 'diet' },
  chicken: { label: { zh: '含雞肉', en: 'Chicken', es: 'Pollo' }, kind: 'diet' },
  seafood: { label: { zh: '含海鮮', en: 'Seafood', es: 'Marisco' }, kind: 'diet' },
  peanut: { label: { zh: '含花生', en: 'Peanuts', es: 'Cacahuete' }, kind: 'diet' },
  egg: { label: { zh: '含蛋', en: 'Egg', es: 'Huevo' }, kind: 'diet' },
  dairy: { label: { zh: '含奶', en: 'Dairy', es: 'Lácteos' }, kind: 'diet' },
  veg: { label: { zh: '素食', en: 'Veg', es: 'Veg' }, kind: 'diet' },
}
const TAGS: Record<string, string[]> = {
  '紅燒牛肉麵': ['hot', 'beef'],
  '麻醬牛肉乾麵': ['beef', 'peanut'],
  '古早味滷肉飯': ['hot', 'pork', 'egg'],
  '雞肉飯': ['chicken'],
  '櫻花蝦米糕': ['rec', 'seafood'],
  '芋頭餅': ['veg'],
  '涼拌花生芹菜': ['veg', 'peanut'],
  '台式泡菜': ['veg'],
  '台灣鳳梨酥': ['rec', 'dairy', 'egg'],
  '每日現做各式起司蛋糕': ['dairy', 'egg'],
  '戚風蛋糕': ['dairy', 'egg'],
}

/* 人氣推薦大卡（品牌卡） */
const POPULAR = [
  { img: '/images/menu-cards/beef-noodle-sq.png', alt: { zh: '牛肉麵', en: 'Beef Noodle Soup', es: 'Sopa de fideos' } },
  { img: '/images/menu-cards/pork-rice-sq-v2.png', alt: { zh: '滷肉飯', en: 'Braised Pork Rice', es: 'Arroz con cerdo' } },
  { img: '/images/menu-cards/bubble-tea-sq.png', alt: { zh: '黑糖珍珠鮮奶', en: 'Brown Sugar Bubble Milk', es: 'Té de burbujas' } },
  { img: '/images/menu-cards/dessert-sq.png', alt: { zh: '甜點', en: 'Desserts', es: 'Postres' } },
]

const NAV = [
  { id: 'popular', label: { zh: '人氣', en: 'Popular', es: 'Favoritos' } },
  { id: 'mains', label: { zh: '主餐', en: 'Mains', es: 'Platos' } },
  { id: 'desserts', label: { zh: '甜點', en: 'Desserts', es: 'Postres' } },
  { id: 'drinks', label: { zh: '飲品', en: 'Drinks', es: 'Bebidas' } },
  { id: 'combos', label: { zh: '套餐', en: 'Combos', es: 'Combos' } },
]

const DRINK_IDS = ['taiwanese-black-tea', 'jasmine', 'oolong', 'matcha', 'coffee', 'caffeine-free', 'pot-brewed', 'summer']

const comboItems = [
  { icon: CupSoda, name: { zh: '珍珠奶茶', en: 'Bubble Tea', es: 'Té de Burbujas' }, price: '$5.00' },
  { icon: Coffee, name: { zh: '熱茶', en: 'Hot Tea', es: 'Té Caliente' }, price: '$3.00' },
  { icon: CakeSlice, name: { zh: '起司蛋糕', en: 'Cheese Cake', es: 'Pastel de Queso' }, price: '$5.00' },
]

export function MenuFull() {
  const { language } = useLanguage()
  const lang: Lang = (['zh', 'en', 'es'].includes(language) ? language : 'en') as Lang
  const [active, setActive] = useState('popular')

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => entries.forEach((e) => { if (e.isIntersecting) setActive(e.target.id) }),
      { rootMargin: '-25% 0px -65% 0px' }
    )
    NAV.forEach((g) => { const el = document.getElementById(g.id); if (el) observer.observe(el) })
    return () => observer.disconnect()
  }, [])

  const catById = (id: string) => menuCategories.find((c) => c.id === id)
  const catTitle = (c: MenuCategory) => (lang === 'zh' ? c.titleZh : lang === 'es' ? c.titleEs : c.titleEn)
  const name = (i: MenuItemData) => (lang === 'zh' ? i.nameZh : lang === 'es' ? i.nameEs : i.nameEn)
  const subName = (i: MenuItemData) => (lang === 'zh' ? i.nameEn : i.nameZh)
  const desc = (i: MenuItemData) => (lang === 'zh' ? i.descZh : lang === 'es' ? i.descEs : i.descEn)
  const fmt = (p: string) => (p.startsWith('$') ? p : `$${p}`)

  const heading = lang === 'zh' ? '菜單' : lang === 'es' ? 'Menú' : 'Menu'
  const intro = lang === 'zh'
    ? '道地台式餐點、手搖茶飲、現煮咖啡與每日現做甜點——家鄉味，端上你的桌。'
    : lang === 'es'
      ? 'Platos taiwaneses, tés artesanales, café y postres del día — el sabor de casa.'
      : 'Taiwanese comfort food, hand-shaken teas, fresh coffee & daily desserts — the taste of home.'
  const orderLabel = lang === 'zh' ? '線上點餐' : lang === 'es' ? 'Pedir en línea' : 'Order Online'
  const callLabel = lang === 'zh' ? '來電洽詢' : lang === 'es' ? 'Llámanos' : 'Call Us'

  const mains = catById('main-dishes')
  const desserts = catById('desserts')

  return (
    <div className="bg-cream pb-24 md:pb-0">
      {/* 標題 + 介紹 + CTA */}
      <div className="mx-auto max-w-6xl px-6 pt-28 pb-8 text-center md:px-8">
        <p className="mb-2 font-heading text-sm uppercase tracking-[0.28em] text-primary/70">Snacks · Cafe · Bakery</p>
        <h1 className="font-heading text-5xl font-bold text-[#5b3a2e] md:text-6xl">{heading}</h1>
        <p className="mx-auto mt-4 max-w-xl font-body text-base text-muted-foreground md:text-lg">{intro}</p>
        <div className="mt-6 flex flex-wrap items-center justify-center gap-3">
          <a href={UBER} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 rounded-full bg-[#06C167] px-6 py-3 font-body font-semibold text-white transition hover:bg-[#05a557]">
            <Truck className="h-4 w-4" />Uber Eats
          </a>
          <a href={DOORDASH} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-2 rounded-full bg-[#FF3008] px-6 py-3 font-body font-semibold text-white transition hover:bg-[#d92806]">
            <Truck className="h-4 w-4" />DoorDash
          </a>
          <a href="tel:+18453811002" className="inline-flex items-center gap-2 rounded-full border-2 border-primary px-6 py-3 font-body font-semibold text-primary transition hover:bg-primary hover:text-primary-foreground">
            <Phone className="h-4 w-4" />{callLabel}
          </a>
        </div>
      </div>

      {/* 分類黏頂列 */}
      <nav className="sticky top-20 z-30 border-y border-black/5 bg-cream/95 backdrop-blur-md">
        <div className="scrollbar-hide mx-auto max-w-6xl overflow-x-auto px-4 py-3">
          <div className="flex min-w-max justify-center gap-2">
            {NAV.map((g) => (
              <a key={g.id} href={`#${g.id}`}
                className={`whitespace-nowrap rounded-full px-5 py-2 font-body text-sm font-semibold transition-colors duration-200 ${active === g.id ? 'bg-primary text-primary-foreground' : 'text-foreground/60 hover:bg-primary/10 hover:text-primary'}`}>
                {g.label[lang]}
              </a>
            ))}
          </div>
        </div>
      </nav>

      <div className="mx-auto max-w-6xl px-6 py-12 md:px-8">
        {/* 人氣推薦 */}
        <section id="popular" className="scroll-mt-36">
          <GroupHeader kicker="Signature · Most Loved" title={lang === 'zh' ? '人氣推薦' : lang === 'es' ? 'Los favoritos' : 'Popular Picks'} />
          <div className="grid grid-cols-2 gap-4 md:grid-cols-4 md:gap-6">
            {POPULAR.map((p) => (
              <div key={p.img} className="overflow-hidden rounded-2xl shadow-sm ring-1 ring-black/5">
                <div className="relative aspect-square">
                  <Image src={p.img} alt={p.alt[lang]} fill className="object-cover" sizes="(max-width:768px) 45vw, 22vw" quality={85} />
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* 主餐 */}
        {mains && (
          <CardSection id="mains" kicker="Rice Bowls & Noodles" title={lang === 'zh' ? '主餐' : 'Mains'}
            items={mains.items} lang={lang} name={name} subName={subName} desc={desc} fmt={fmt} icon={Soup}
            banner={{ src: '/images/menu-cards/mains-banner-wide.png', w: 1962, h: 802 }} textOnly />
        )}

        {/* 甜點 */}
        {desserts && (
          <CardSection id="desserts" kicker="Sweet Endings" title={lang === 'zh' ? '甜點' : 'Desserts'}
            items={desserts.items} lang={lang} name={name} subName={subName} desc={desc} fmt={fmt} icon={CakeSlice}
            banner={{ src: '/images/menu-cards/desserts-banner.png', w: 1536, h: 1024 }} textOnly />
        )}

        {/* 飲品（一大類一張卡） */}
        <section id="drinks" className="scroll-mt-36 pt-6">
          <GroupHeader kicker="Hand-Shaken Teas · Coffee" title={lang === 'zh' ? '飲品' : 'Drinks'} />
          <div className="grid items-start gap-5 md:grid-cols-2">
            {DRINK_IDS.map((id) => {
              const c = catById(id)
              if (!c) return null
              return <DrinkCard key={id} title={catTitle(c)} isCoffee={id === 'coffee'} items={c.items} name={name} subName={subName} fmt={fmt} />
            })}
          </div>
        </section>

        {/* 套餐 */}
        <section id="combos" className="scroll-mt-36 pt-6">
          <GroupHeader kicker="Better Together" title={lang === 'zh' ? '套餐' : 'Combos'} />
          <div className="mx-auto max-w-3xl rounded-2xl border-2 border-dashed border-primary/30 bg-[#f2e7d2] px-6 py-6">
            <p className="mb-4 text-center font-heading text-xl font-bold text-primary">
              {lang === 'zh' ? '超值套餐 · 加點享優惠' : 'Combo Deal · Add to Any Meal'}
            </p>
            <div className="flex flex-wrap items-center justify-center gap-x-10 gap-y-4">
              {comboItems.map((c) => {
                const Icon = c.icon
                return (
                  <div key={c.name.en} className="flex items-center gap-3">
                    <Icon className="h-8 w-8 text-primary" strokeWidth={1.5} aria-hidden="true" />
                    <div>
                      <p className="font-body font-semibold text-foreground">{c.name[lang]}</p>
                      <p className="font-body font-bold text-primary">{c.price}</p>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </section>

        {/* 注意事項 */}
        <section className="pt-14">
          <div className="mx-auto max-w-3xl rounded-2xl bg-white/70 p-6 ring-1 ring-black/5">
            <h3 className="mb-3 font-heading text-lg font-bold text-primary">
              {lang === 'zh' ? '注意事項' : lang === 'es' ? 'Aviso' : 'Good to Know'}
            </h3>
            <ul className="space-y-2 font-body text-sm text-foreground/75">
              <li>{lang === 'zh' ? '如有食物過敏，請於點餐時告知我們。' : lang === 'es' ? 'Si tienes alguna alergia, por favor avísanos al pedir.' : 'Please let us know of any food allergies when ordering.'}</li>
              <li>{lang === 'zh' ? '供應時段：週一・二・五・六 11:00am–7:00pm（週三・四・日 公休）。' : 'Serving hours: Mon · Tue · Fri · Sat 11:00am–7:00pm (closed Wed · Thu · Sun).'}</li>
              <li>{lang === 'zh' ? '菜單內容與價格可能隨季節調整，以店內為準。' : 'Menu items and prices may vary by season; in-store menu prevails.'}</li>
            </ul>
          </div>
        </section>

        {/* 店鋪資訊 */}
        <section className="pt-12">
          <GroupHeader kicker="Find Us" title={lang === 'zh' ? '店鋪資訊' : 'Visit Us'} />
          <div className="mx-auto grid max-w-3xl gap-3 font-body text-foreground/80">
            <a href={MAPS} target="_blank" rel="noopener noreferrer" className="flex items-center gap-3 hover:text-primary">
              <MapPin className="h-5 w-5 shrink-0 text-primary" />26 South St, Middletown, NY 10940
            </a>
            <a href="tel:+18453811002" className="flex items-center gap-3 hover:text-primary">
              <Phone className="h-5 w-5 shrink-0 text-primary" />(845) 381-1002
            </a>
            <p className="flex items-center gap-3">
              <Clock className="h-5 w-5 shrink-0 text-primary" />
              {lang === 'zh' ? '週一・二・五・六　11:00am – 7:00pm' : 'Mon · Tue · Fri · Sat　11:00am – 7:00pm'}
            </p>
          </div>
        </section>
      </div>

      {/* 固定底部點餐條（手機） */}
      <div className="fixed inset-x-0 bottom-0 z-40 border-t border-black/10 bg-cream/95 px-4 py-3 backdrop-blur-md md:hidden">
        <div className="flex items-center gap-2">
          <span className="shrink-0 font-heading text-sm font-bold text-primary">{orderLabel}</span>
          <a href={UBER} target="_blank" rel="noopener noreferrer" className="flex flex-1 items-center justify-center rounded-full bg-[#06C167] px-3 py-2.5 text-sm font-semibold text-white">Uber Eats</a>
          <a href={DOORDASH} target="_blank" rel="noopener noreferrer" className="flex flex-1 items-center justify-center rounded-full bg-[#FF3008] px-3 py-2.5 text-sm font-semibold text-white">DoorDash</a>
        </div>
      </div>
    </div>
  )
}

function CardSection({ id, kicker, title, items, lang, name, subName, desc, fmt, icon, banner, textOnly }: {
  id: string; kicker: string; title: string; items: MenuItemData[]; lang: Lang
  name: (i: MenuItemData) => string; subName: (i: MenuItemData) => string
  desc: (i: MenuItemData) => string | undefined; fmt: (p: string) => string; icon: LucideIcon
  banner?: { src: string; w: number; h: number }; textOnly?: boolean
}) {
  return (
    <section id={id} className="scroll-mt-36 pt-6">
      <GroupHeader kicker={kicker} title={title} />
      {banner && (
        <div className="mb-10 overflow-hidden rounded-2xl shadow-md ring-1 ring-black/5">
          <Image src={banner.src} alt={title} width={banner.w} height={banner.h} className="h-auto w-full" sizes="(max-width:1152px) 100vw, 1152px" />
        </div>
      )}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3 md:gap-6">
        {items.map((item, i) => (
          <DishCard key={i} photo={textOnly ? undefined : PHOTOS[item.nameZh]} icon={icon} dishIcon={ICON_SVG[item.nameZh]} name={name(item)} sub={subName(item)}
            desc={desc(item)} options={item.options} price={item.price ? fmt(item.price) : undefined}
            tags={(TAGS[item.nameZh] || []).map((k) => ({ label: T[k].label[lang], kind: T[k].kind }))} />
        ))}
      </div>
    </section>
  )
}

function tagClass(kind: TagKind) {
  if (kind === 'hot') return 'rounded-full bg-primary px-2 py-0.5 font-body text-[11px] font-semibold text-primary-foreground'
  if (kind === 'rec') return 'rounded-full bg-[hsl(44,80%,42%)] px-2 py-0.5 font-body text-[11px] font-semibold text-white'
  return 'rounded-full bg-primary/[0.08] px-2 py-0.5 font-body text-[11px] font-medium text-primary/80'
}

function DishCard({ photo, icon: Icon, dishIcon, name, sub, desc, options, price, tags }: {
  photo?: string; icon?: LucideIcon; dishIcon?: string; name: string; sub?: string; desc?: string; options?: string; price?: string
  tags?: { label: string; kind: TagKind }[]
}) {
  return (
    <div className="flex flex-col overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-black/5">
      {photo ? (
        <div className="relative aspect-[4/3]">
          <Image src={`/images/food/${photo}`} alt={name} fill className="object-cover" sizes="(max-width:640px) 100vw, 33vw" quality={80} />
        </div>
      ) : dishIcon ? (
        <div className="px-5 pt-5">
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={dishIcon} alt="" width={44} height={44} className="h-11 w-11" aria-hidden="true" />
        </div>
      ) : Icon ? (
        <div className="px-5 pt-5">
          <Icon className="h-7 w-7 text-primary/55" strokeWidth={1.5} aria-hidden="true" />
        </div>
      ) : null}
      <div className={`flex flex-1 flex-col ${photo ? 'p-4' : 'px-5 pb-5 pt-2'}`}>
        <h4 className="font-body text-lg font-bold text-foreground">{name}</h4>
        {sub && <p className="font-body text-sm text-muted-foreground">{sub}</p>}
        {desc && <p className="mt-1.5 font-body text-sm leading-relaxed text-foreground/70">{desc}</p>}
        <div className="mt-auto flex items-center justify-between gap-3 pt-3">
          {tags && tags.length > 0 ? (
            <div className="flex flex-wrap gap-1.5">
              {tags.map((t) => (
                <span key={t.label} className={tagClass(t.kind)}>{t.label}</span>
              ))}
            </div>
          ) : (
            <span />
          )}
          <div className="flex shrink-0 items-baseline gap-2">
            {options && <span className="font-body text-xs text-muted-foreground">{options}</span>}
            {price && <span className="whitespace-nowrap font-body text-lg font-bold text-primary">{price}</span>}
          </div>
        </div>
      </div>
    </div>
  )
}

function GroupHeader({ kicker, title }: { kicker: string; title: string }) {
  return (
    <div className="mb-8 mt-4 flex flex-col items-center text-center">
      <p className="font-body text-xs uppercase tracking-[0.24em] text-primary/60">{kicker}</p>
      <h2 className="mt-1 font-heading text-4xl font-bold text-[#5b3a2e] md:text-5xl">{title}</h2>
      <span className="mt-3 h-1 w-16 rounded-full bg-primary/70" />
    </div>
  )
}

function DrinkCard({ title, isCoffee, items, name, subName, fmt }: {
  title: string; isCoffee?: boolean; items: MenuItemData[]
  name: (i: MenuItemData) => string; subName: (i: MenuItemData) => string; fmt: (p: string) => string
}) {
  const Icon = isCoffee ? Coffee : CupSoda
  return (
    <div className="rounded-2xl bg-white p-5 shadow-sm ring-1 ring-black/5">
      <div className="mb-4 flex items-center gap-2.5 border-b border-primary/15 pb-3">
        <Icon className="h-5 w-5 shrink-0 text-primary" strokeWidth={1.5} aria-hidden="true" />
        <h3 className="font-heading text-lg font-bold text-primary">{title}</h3>
      </div>
      <ul className="space-y-3">
        {items.map((item, i) => (
          <li key={i} className="flex items-baseline justify-between gap-3">
            <div className="min-w-0">
              <p className="font-body text-sm font-semibold text-foreground">{name(item)}</p>
              <p className="font-body text-xs text-muted-foreground">{subName(item)}</p>
            </div>
            <div className="flex shrink-0 items-baseline gap-2">
              {item.options && <span className="whitespace-nowrap font-body text-[11px] text-muted-foreground">{item.options}</span>}
              {item.price && <span className="whitespace-nowrap font-body text-sm font-bold text-primary">{fmt(item.price)}</span>}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
