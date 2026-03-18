import type { Metadata } from 'next'
import { ProductsShowcase } from "@/components/products-showcase"

export const metadata: Metadata = {
  title: 'Menu | Bubble Tea, Beef Noodle Soup & More',
  description:
    'TaiwanWay 完整菜單 — 珍珠奶茶、牛肉麵、滷肉飯、鳳梨酥、烏龍茶。Full menu: bubble tea, beef noodle soup, braised pork rice & Taiwanese desserts.',
  alternates: { canonical: '/menu' },
  openGraph: {
    title: 'Menu | TaiwanWay - Taiwanese Restaurant Middletown NY',
    description: 'Browse our full menu — bubble tea, oolong tea, beef noodle soup, braised pork rice & handmade Taiwanese desserts.',
    url: '/menu',
  },
}
import { MenuCarousel } from "@/components/menu-carousel"

export default function MenuPage() {
  return (
    <main id="main-content">
      {/* 輪播展示 */}
      <MenuCarousel />

      {/* 產品展示 - 春水堂風格 */}
      <ProductsShowcase />
    </main>
  )
}
