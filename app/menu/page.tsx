import { Header } from "@/components/header"
import { MenuCategory } from "@/components/menu-category"
import { Footer } from "@/components/footer"

const menuCategories = [
  {
    id: "snacks",
    title: "Snacks 小點心",
    items: [
      { name: "鹽酥雞 Taiwanese Popcorn Chicken", price: 6.99, image: "/placeholder.svg" },
      { name: "蔥油餅 Scallion Pancake", price: 4.99, image: "/placeholder.svg" },
      { name: "滷味拼盤 Braised Delights Platter", price: 8.99, image: "/placeholder.svg" },
      { name: "炸豆腐 Fried Tofu", price: 5.99, image: "/placeholder.svg" },
    ],
  },
  {
    id: "main-dishes",
    title: "Main Dishes 主餐",
    items: [
      {
        name: "滷肉飯 Braised Pork Rice",
        price: 8.99,
        image:
          "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2466.JPG-RIKgCt96QrGfXKlfWAgI8BjZN2thK1.jpeg",
      },
      {
        name: "牛肉麵 Beef Noodle Soup",
        price: 12.99,
        image:
          "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2467.JPG-12cMHEqSdXbYmVHMe0F7GS10Fauj7H.jpeg",
      },
    ],
  },
  {
    id: "drinks",
    title: "Drinks 飲品",
    items: [
      {
        name: "黑糖珍珠鮮奶 Brown Sugar Bubble Fresh Milk",
        price: 6.99,
        image:
          "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9008.JPG-R6OLOktSElMsNmsXUSUNhbn64fU4Zf.jpeg",
      },
      {
        name: "一保堂抹茶珍珠鮮奶 Ippodo Matcha Bubble Fresh Milk",
        price: 6.99,
        image:
          "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9012.JPG-3IAQXxAdSc0KSu7y9VNQs7anLbC1dB.jpeg",
      },
      {
        name: "珍珠奶茶 Bubble Tea",
        price: 5.99,
        image:
          "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9009.JPG-8Ke0jB3xYx1Ws4ynQLZCXnhyQcsYEl.jpeg",
      },
      { name: "冬瓜檸檬 Winter Melon Lemonade", price: 4.99, image: "/placeholder.svg" },
    ],
  },
  {
    id: "desserts",
    title: "Desserts 甜點",
    items: [{ name: "鳳梨酥 Pineapple Cake", price: 2.99, image: "/placeholder.svg" }],
  },
]

export default function MenuPage() {
  return (
    <main className="min-h-screen flex flex-col">
      <Header />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-4xl font-bold mb-8">Full Menu 完整菜單</h1>
        {menuCategories.map((category) => (
          <MenuCategory key={category.id} id={category.id} title={category.title} items={category.items} />
        ))}
      </div>
      <Footer />
    </main>
  )
}

