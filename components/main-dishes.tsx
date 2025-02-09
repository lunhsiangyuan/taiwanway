'use client'

import { useLanguage } from "@/lib/i18n/language-context"
import Image from "next/image"

type MenuItem = {
  name: string;
  description: string;
  price: string;
}

const menuImages = {
  pineappleCake: "https://06jfzz4maekxll04.public.blob.vercel-storage.com/pineapple-cake-QtQVUryed5EphoMtw2te8NyLjQFrSq.jpg",
  beefNoodle: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2467.JPG-12cMHEqSdXbYmVHMe0F7GS10Fauj7H.jpeg",
  braisedPork: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2466.JPG-RIKgCt96QrGfXKlfWAgI8BjZN2thK1.jpeg",
}

export function MainDishes() {
  const { t } = useLanguage()

  const desserts = t('menu.mainDishesList.categories.desserts.items') as unknown as Record<string, MenuItem>
  const mainDishItems = {
    braisedPork: t('menu.mainDishesList.categories.riceDishes.items.braisedPork') as unknown as MenuItem,
    beefNoodle: t('menu.mainDishesList.categories.noodleSoups.items.beefNoodle') as unknown as MenuItem,
  }

  return (
    <div>      
      {/* Main Dishes Section */}
      <div id="main-dishes" className="mb-16 scroll-mt-20">
        <h3 className="text-2xl font-semibold mb-8">{t('menu.sections.mainDishes.title')}</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {Object.entries(mainDishItems).map(([key, item]) => (
            <div key={key} className="flex flex-col md:flex-row gap-6 items-start">
              <div className="relative w-full md:w-48 h-48 rounded-lg overflow-hidden">
                <Image
                  src={menuImages[key as keyof typeof menuImages]}
                  alt={item.name}
                  fill
                  className="object-cover"
                />
              </div>
              <div className="flex-1 flex flex-col justify-between h-48">
                <div>
                  <h4 className="text-xl font-semibold">{item.name}</h4>
                  <p className="text-muted-foreground">{item.description}</p>
                </div>
                <p className="text-lg font-medium">${item.price}</p>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Desserts Section */}
      <div id="desserts" className="mb-16 scroll-mt-20">
        <h3 className="text-2xl font-semibold mb-8">{t('menu.mainDishesList.categories.desserts.title')}</h3>
        <div className="grid gap-8">
          {Object.entries(desserts).map(([key, item]) => (
            <div key={key} className="flex flex-col md:flex-row gap-6 items-start">
              <div className="relative w-full md:w-48 h-48 rounded-lg overflow-hidden">
                <Image
                  src={menuImages[key as keyof typeof menuImages]}
                  alt={item.name}
                  fill
                  className="object-cover"
                />
              </div>
              <div className="flex-1 flex flex-col justify-between h-48">
                <div>
                  <h4 className="text-xl font-semibold">{item.name}</h4>
                  <p className="text-muted-foreground">{item.description}</p>
                </div>
                <p className="text-lg font-medium">${item.price}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

