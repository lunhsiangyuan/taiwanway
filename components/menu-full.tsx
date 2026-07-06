'use client'

import { useEffect, useState } from 'react'
import Image from 'next/image'
import { useLanguage } from '@/lib/i18n/language-context'
import { menuCategories, type MenuCategory, type MenuItemData } from './menu-carousel'
import { CupSoda, Coffee, CakeSlice } from 'lucide-react'

type Lang = 'zh' | 'en' | 'es'

type FoodItem = {
  n: number
  img: string
  nameZh: string
  nameEn: string
  descZh: string
  descEn: string
  prices: [string, string][]
  tag?: 'POPULAR' | 'NEW'
}

type FoodGroup = { id: string; label: Record<Lang, string>; items: FoodItem[] }

const foodGroups: FoodGroup[] = [
  {
    id: 'rice-bowls',
    label: { zh: '飯食 & 湯麵', en: 'Rice Bowls & Soups', es: 'Arroces y Sopas' },
    items: [
      { n: 1, img: 'braised-pork-rice.jpg', nameZh: '台灣滷肉飯', nameEn: 'Braised Pork Rice', descZh: '慢燉滷肉、酸菜與滷蛋，淋在熱白飯上', descEn: 'Slow-braised pork belly over steamed rice with pickled mustard greens & soft-boiled egg', prices: [['M', '$10.99'], ['L', '$12.99']], tag: 'POPULAR' },
      { n: 2, img: 'chicken-rice.jpg', nameZh: '台灣雞肉飯', nameEn: 'Taiwanese Chicken Rice', descZh: '雞胸肉絲鋪飯，淋上油蔥與醬汁', descEn: 'Tender shredded chicken on rice, topped with savory jus & crispy shallots', prices: [['M', '$10.99'], ['L', '$12.99']] },
      { n: 3, img: 'beef-noodle.jpg', nameZh: '台灣牛肉麵', nameEn: 'Braised Beef Noodle Soup', descZh: '香濃湯頭、軟嫩牛肉、Q 彈麵條與青江菜', descEn: 'Rich braised broth with tender beef chunks, hand-pulled noodles & bok choy', prices: [['M', '$13.99'], ['L', '$15.99']], tag: 'POPULAR' },
    ],
  },
  {
    id: 'noodles-specials',
    label: { zh: '乾麵 & 特色', en: 'Noodles & Specials', es: 'Fideos y Especiales' },
    items: [
      { n: 4, img: 'dried-beef-noodles.png', nameZh: '麻醬牛肉乾麵', nameEn: 'Dried Beef Noodles', descZh: 'Q 彈麵條拌芝麻醬，配滷牛肉與青菜', descEn: 'Chewy noodles tossed in fragrant sesame sauce with braised beef & greens', prices: [['M', '$13.99'], ['L', '$15.99']] },
      { n: 5, img: 'sticky-rice.png', nameZh: '櫻花蝦米糕', nameEn: 'Taiwanese Sticky Rice', descZh: '糯米蒸煮，拌入櫻花蝦、香菇與油蔥', descEn: 'Savory glutinous rice steamed with sakura shrimp, mushrooms & crispy shallots', prices: [['One', '$12.99']], tag: 'NEW' },
    ],
  },
]

const comboItems = [
  { icon: CupSoda, name: { zh: '珍珠奶茶', en: 'Bubble Tea', es: 'Té de Burbujas' }, price: '$5.00' },
  { icon: Coffee, name: { zh: '熱茶', en: 'Hot Tea', es: 'Té Caliente' }, price: '$3.00' },
  { icon: CakeSlice, name: { zh: '起司蛋糕', en: 'Cheese Cake', es: 'Pastel de Queso' }, price: '$5.00' },
]

const DRINK_IDS = ['taiwanese-black-tea', 'jasmine', 'oolong', 'matcha', 'coffee', 'caffeine-free', 'pot-brewed', 'summer', 'winter']

const groupsNav = [
  { id: 'food', label: { zh: '餐點', en: 'Comfort Food', es: 'Comida' } },
  { id: 'drinks', label: { zh: '飲料', en: 'Drinks', es: 'Bebidas' } },
  { id: 'desserts', label: { zh: '甜點', en: 'Desserts', es: 'Postres' } },
]

export function MenuFull() {
  const { language } = useLanguage()
  const lang: Lang = (['zh', 'en', 'es'].includes(language) ? language : 'en') as Lang
  const [active, setActive] = useState('food')

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => entries.forEach((e) => { if (e.isIntersecting) setActive(e.target.id) }),
      { rootMargin: '-30% 0px -60% 0px' }
    )
    groupsNav.forEach((g) => { const el = document.getElementById(g.id); if (el) observer.observe(el) })
    return () => observer.disconnect()
  }, [])

  const catById = (id: string) => menuCategories.find((c) => c.id === id)
  const getCatTitle = (c: MenuCategory) => (lang === 'zh' ? c.titleZh : lang === 'es' ? c.titleEs : c.titleEn)
  const getName = (i: MenuItemData) => (lang === 'zh' ? i.nameZh : lang === 'es' ? i.nameEs : i.nameEn)
  const getSubName = (i: MenuItemData) => (lang === 'zh' ? i.nameEn : i.nameZh)
  const getDesc = (i: MenuItemData) => (lang === 'zh' ? i.descZh : lang === 'es' ? i.descEs : i.descEn)
  const fmt = (p: string) => (p.startsWith('$') ? p : `$${p}`)

  const heading = lang === 'zh' ? '菜單' : lang === 'es' ? 'Menú' : 'Menu'
  const subtitle = lang === 'zh'
    ? '道地台式餐點、手搖茶飲、現煮咖啡與每日甜點'
    : lang === 'es' ? 'Platos taiwaneses, tés artesanales, café y postres'
      : 'Taiwanese comfort food, hand-shaken teas, fresh coffee & daily desserts'

  const foodName = (it: FoodItem) => (lang === 'zh' ? it.nameZh : it.nameEn)
  const foodSub = (it: FoodItem) => (lang === 'zh' ? it.nameEn : it.nameZh)
  const foodDesc = (it: FoodItem) => (lang === 'zh' ? it.descZh : it.descEn)

  const sideCat = catById('appetizers')
  const dessertCat = catById('desserts')

  return (
    <div className="bg-cream">
      {/* 標題 */}
      <div className="mx-auto max-w-6xl px-6 pt-28 pb-8 text-center md:px-8">
        <p className="mb-2 font-heading text-sm uppercase tracking-[0.28em] text-primary/70">Snacks · Cafe · Bakery</p>
        <h1 className="font-heading text-5xl font-bold text-[#5b3a2e] md:text-6xl">{heading}</h1>
        <p className="mx-auto mt-4 max-w-xl font-body text-base text-muted-foreground md:text-lg">{subtitle}</p>
      </div>

      {/* 大分類黏頂列 */}
      <nav className="sticky top-20 z-30 border-y border-black/5 bg-cream/95 backdrop-blur-md">
        <div className="mx-auto flex max-w-6xl justify-center gap-2 px-4 py-3">
          {groupsNav.map((g) => (
            <a key={g.id} href={`#${g.id}`}
              className={`rounded-full px-6 py-2 font-heading text-sm font-semibold transition-colors duration-200 ${active === g.id ? 'bg-primary text-primary-foreground' : 'text-foreground/60 hover:bg-primary/10 hover:text-primary'}`}>
              {g.label[lang]}
            </a>
          ))}
        </div>
      </nav>

      <div className="mx-auto max-w-6xl px-6 py-12 md:px-8">
        {/* ===== 餐點 ===== */}
        <section id="food" className="scroll-mt-36">
          <GroupHeader kicker="Taiwanese Classics · Rice Bowls · Noodles" title={lang === 'zh' ? '餐點' : 'Comfort Food'} />

          {foodGroups.map((fg) => (
            <div key={fg.id} className="mb-12">
              <SubHeader title={fg.label[lang]} />
              <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
                {fg.items.map((it) => (
                  <div key={it.n} className="flex flex-col overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-black/5">
                    <div className="relative aspect-[4/3]">
                      <Image src={`/images/food/${it.img}`} alt={foodName(it)} fill className="object-cover" sizes="(max-width:640px) 100vw, 33vw" quality={80} />
                      <span className="absolute left-3 top-3 flex h-7 w-7 items-center justify-center rounded-full bg-primary font-heading text-sm font-bold text-primary-foreground shadow">{it.n}</span>
                      {it.tag && (
                        <span className={`absolute right-3 top-3 rounded-full px-2.5 py-1 font-body text-[10px] font-bold uppercase tracking-wider text-white shadow ${it.tag === 'NEW' ? 'bg-[hsl(44,80%,42%)]' : 'bg-primary'}`}>{it.tag}</span>
                      )}
                    </div>
                    <div className="flex flex-1 flex-col p-4">
                      <h4 className="font-body text-lg font-bold text-foreground">{foodName(it)}</h4>
                      <p className="font-body text-sm text-muted-foreground">{foodSub(it)}</p>
                      <p className="mt-1.5 flex-1 font-body text-sm leading-relaxed text-foreground/70">{foodDesc(it)}</p>
                      <div className="mt-3 flex flex-wrap gap-2">
                        {it.prices.map(([size, price]) => (
                          <span key={size} className="inline-flex items-baseline gap-1.5 rounded-lg bg-cream px-2.5 py-1">
                            <span className="font-body text-xs text-muted-foreground">{size}</span>
                            <span className="font-body text-sm font-bold text-primary">{price}</span>
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}

          {/* Combo Deal */}
          <div className="mx-auto mb-12 max-w-3xl rounded-2xl border-2 border-dashed border-primary/30 bg-[#f2e7d2] px-6 py-6">
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

          {/* 開胃小菜 */}
          {sideCat && (
            <div className="mb-4">
              <SubHeader title={getCatTitle(sideCat)} />
              <div className="grid gap-x-12 gap-y-5 md:grid-cols-2">
                {sideCat.items.map((item, i) => <ListRow key={i} name={getName(item)} sub={getSubName(item)} desc={getDesc(item)} options={item.options} price={item.price ? fmt(item.price) : undefined} />)}
              </div>
            </div>
          )}
        </section>

        {/* ===== 飲料 ===== */}
        <section id="drinks" className="scroll-mt-36 pt-6">
          <GroupHeader kicker="Hand-Shaken Teas · Coffee · Seasonal" title={lang === 'zh' ? '飲料' : 'Drinks'} />
          {DRINK_IDS.map((id) => {
            const c = catById(id)
            if (!c) return null
            return (
              <div key={id} className="mb-10">
                <SubHeader title={getCatTitle(c)} />
                <div className="grid gap-x-12 gap-y-4 md:grid-cols-2">
                  {c.items.map((item, i) => <ListRow key={i} name={getName(item)} sub={getSubName(item)} desc={getDesc(item)} options={item.options} price={item.price ? fmt(item.price) : undefined} />)}
                </div>
              </div>
            )
          })}
        </section>

        {/* ===== 甜點 ===== */}
        {dessertCat && (
          <section id="desserts" className="scroll-mt-36 pt-6">
            <GroupHeader kicker="Sweet Endings" title={lang === 'zh' ? '甜點' : 'Desserts'} />
            <div className="grid gap-x-12 gap-y-5 md:grid-cols-2">
              {dessertCat.items.map((item, i) => <ListRow key={i} name={getName(item)} sub={getSubName(item)} desc={getDesc(item)} options={item.options} price={item.price ? fmt(item.price) : undefined} />)}
            </div>
          </section>
        )}
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

function SubHeader({ title }: { title: string }) {
  return (
    <div className="mb-5 flex items-center gap-3">
      <h3 className="font-heading text-xl font-bold text-primary">{title}</h3>
      <span className="h-px flex-1 bg-primary/15" />
    </div>
  )
}

function ListRow({ name, sub, desc, options, price }: { name: string; sub?: string; desc?: string; options?: string; price?: string }) {
  return (
    <div className="border-b border-black/[0.06] pb-3">
      <div className="flex items-baseline gap-2.5">
        <h4 className="font-body text-base font-semibold text-foreground">{name}</h4>
        <span className="mb-1 h-0 flex-1 border-b border-dotted border-foreground/25" aria-hidden="true" />
        <div className="flex shrink-0 items-baseline gap-2">
          {options && <span className="whitespace-nowrap font-body text-xs text-muted-foreground">{options}</span>}
          {price && <span className="whitespace-nowrap font-body font-bold text-primary">{price}</span>}
        </div>
      </div>
      {sub && <p className="font-body text-xs text-muted-foreground">{sub}</p>}
      {desc && <p className="mt-1 font-body text-sm leading-relaxed text-foreground/70">{desc}</p>}
    </div>
  )
}
