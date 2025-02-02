'use client'

import { useLanguage } from "@/lib/i18n/language-context"

export function MainDishes() {
  const { t } = useLanguage()

  const mainDishes = [
    {
      key: 'braisedPork',
      image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2466.JPG-RIKgCt96QrGfXKlfWAgI8BjZN2thK1.jpeg",
    },
    {
      key: 'beefNoodle',
      image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2467.JPG-12cMHEqSdXbYmVHMe0F7GS10Fauj7H.jpeg",
    },
    // 可以根据需要添加更多主菜
  ]

  return (
    <section id="main-dishes" className="mb-12 scroll-mt-20">
      <h2 className="text-3xl font-bold mb-6 px-4">{t('menu.mainDishes')}</h2>
      <div className="px-4 md:px-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {mainDishes.map((dish) => (
            <div key={dish.key} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="relative h-48 w-full">
                <img
                  src={dish.image}
                  alt={t(`menu.items.${dish.key}.name`)}
                  className="object-cover object-center w-full h-full"
                />
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2">{t(`menu.items.${dish.key}.name`)}</h3>
                <p className="text-sm text-gray-600 mb-2">{t(`menu.items.${dish.key}.description`)}</p>
                <p className="text-primary font-bold">${t(`menu.mainDishesList.categories.${dish.key === 'braisedPork' ? 'riceDishes' : 'noodleSoups'}.items.${dish.key}.price`)}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

