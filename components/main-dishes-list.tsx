'use client'

import Image from "next/image"
import { useLanguage } from "@/lib/i18n/language-context"

type MenuItem = {
  name: string
  description: string
  price: string
}

type MenuCategory = {
  title: string
  items: Record<string, MenuItem>
}

export function MainDishesList() {
  const { t } = useLanguage()

  const categories = [
    'riceDishes',
    'noodleSoups'
  ] as const

  return (
    <section id="main-dishes" className="py-20">
      <div className="container">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">{t('menu.sections.mainDishes.title')}</h2>
          <p className="text-lg text-muted-foreground mb-8">{t('menu.sections.mainDishes.description')}</p>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            {categories.map((categoryKey) => {
              const category = t(`menu.mainDishesList.categories.${categoryKey}`) as unknown as MenuCategory
              return (
                <div key={categoryKey} className="space-y-6">
                  <div className="space-y-1">
                    <h3 className="text-2xl text-primary font-medium">
                      {category.title}
                    </h3>
                    <div className="h-0.5 bg-primary w-full"></div>
                  </div>
                  <div className="space-y-6">
                    {Object.entries(category.items).map(([itemKey, item]) => (
                      <div key={itemKey} className="relative group">
                        <div className="aspect-[4/3] overflow-hidden rounded-lg bg-gray-100 relative">
                          <Image
                            src={`/images/dishes/${itemKey}.jpg`}
                            alt={item.name}
                            fill
                            className="object-cover group-hover:scale-105 transition-transform duration-300"
                          />
                        </div>
                        <div className="mt-4">
                          <h4 className="text-xl font-medium">{item.name}</h4>
                          <p className="text-muted-foreground mt-1">{item.description}</p>
                          {/* Price hidden by request */}
                          {/* <p className="text-primary font-medium mt-2">${item.price}</p> */}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </section>
  )
} 