import { ProductsShowcase } from "@/components/products-showcase"
import { MenuCarousel } from "@/components/menu-carousel"

export default function MenuPage() {
  return (
    <main>
      {/* 輪播展示 */}
      <MenuCarousel />

      {/* 產品展示 - 春水堂風格 */}
      <ProductsShowcase />
    </main>
  )
}
