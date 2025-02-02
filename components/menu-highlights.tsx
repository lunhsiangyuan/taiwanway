'use client'

import * as React from "react"
import Image from "next/image"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/lib/i18n/language-context"

const highlights = [
  {
    key: 'beefNoodle',
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2467.JPG-12cMHEqSdXbYmVHMe0F7GS10Fauj7H.jpeg",
  },
  {
    key: 'braisedPork',
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2466.JPG-RIKgCt96QrGfXKlfWAgI8BjZN2thK1.jpeg",
  },
  {
    key: 'dessert',
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_1167.JPG-2RGQnkcNjgJUfESKiEk8uNRWm7dqdR.jpeg",
  },
  {
    key: 'bubbleTea',
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9009.JPG-8Ke0jB3xYx1Ws4ynQLZCXnhyQcsYEl.jpeg",
  },
] as const

export function MenuHighlights() {
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
  ]

  return (
    <div>
      {highlights.map((item, index) => (
        <section key={item.key} className={cn(
          "py-20",
          index % 2 === 0 ? "bg-secondary/30" : "bg-background"
        )}>
          <div className="container px-0 lg:px-4">
            <div className={cn(
              "flex flex-col items-center",
              index % 2 === 0 ? "lg:flex-row" : "lg:flex-row-reverse"
            )}>
              <div className="lg:w-2/3 relative h-[400px] lg:h-[600px] w-full">
                <Image
                  src={item.image}
                  alt={t(`menu.items.${item.key}.name`)}
                  fill
                  className="object-cover rounded-t-xl"
                  priority={index === 0}
                />
              </div>
              <div className="lg:w-1/3 p-8 lg:p-12 space-y-4">
                <h2 className="text-3xl font-bold">{t(`menu.items.${item.key}.name`)}</h2>
                <p className="text-lg text-muted-foreground">{t(`menu.items.${item.key}.description`)}</p>
              </div>
            </div>
          </div>
        </section>
      ))}
    </div>
  )
}

