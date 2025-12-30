'use client'

import { useLanguage } from "@/lib/i18n/language-context"

type DrinkItem = {
  name: string
  price: string
  options: string
}

type DrinkCategory = {
  title: string
  items: Record<string, DrinkItem>
}

export function DrinksList() {
  const { t } = useLanguage()

  const categories = [
    'oldFashioned',
    'taiwaneseBlackTea',
    'caffeineFree',
    'jasmineGreenTea',
    'oolong',
    'matcha',
    'potBrewed'
  ] as const

  return (
    <section id="drinks" className="py-20">
      <div className="container px-4 md:px-6">
        <div className="max-w-4xl mx-auto">
          <h2 className="text-3xl font-bold mb-4">{t('menu.sections.drinks.title')}</h2>
          <p className="text-lg text-muted-foreground mb-8">{t('menu.sections.drinks.description')}</p>
          <div className="space-y-12">
            {categories.map((categoryKey) => {
              const category = t(`menu.drinksList.categories.${categoryKey}`) as unknown as DrinkCategory
              return (
                <div key={categoryKey} className="space-y-6">
                  <div className="space-y-1">
                    <h3 className="text-2xl text-primary font-medium">
                      {category.title}
                    </h3>
                    <div className="h-0.5 bg-primary w-full"></div>
                  </div>
                  <div className="space-y-4">
                    {Object.entries(category.items).map(([itemKey, item]) => (
                      <div key={itemKey} className="flex justify-between items-start gap-4">
                        <div className="space-y-1">
                          <div className="text-xl font-medium">{item.name}</div>
                        </div>
                        <div className="text-right flex flex-col items-end">
                          {/* Price hidden by request */}
                          {/* <div className="text-xl">${item.price}</div> */}
                          <div className="text-primary">{item.options}</div>
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

