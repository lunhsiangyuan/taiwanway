'use client'

import Image from "next/image"
import { Button } from "@/components/ui/button"
import Link from "next/link"
import { useLanguage } from "@/lib/i18n/language-context"

export function Hero() {
  const { t } = useLanguage()

  return (
    <div>
      {/* Image Section */}
      <section className="relative h-[50vh] sm:h-[70vh] w-full overflow-hidden px-4 md:px-6">
        <div className="absolute inset-0 w-full h-full rounded-lg">
          <Image
            src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9053.JPG-4ohewz2SiN4NhrcIua5RHH3DvjCKYW.jpeg"
            alt="TaiwanWay storefront with beautiful pink dogwood blossoms"
            fill
            className="object-cover rounded-lg sm:object-center object-[15%_center]"
            sizes="100vw"
            priority
          />
        </div>
        <div className="absolute inset-0 bg-black bg-opacity-30 rounded-lg"></div>
      </section>

      {/* Content Section */}
      <section className="py-16 bg-secondary/30">
        <div className="container mx-auto px-4 md:px-6">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
              {t('hero.welcome')}
              <span className="text-primary"> {t('hero.brandName')}</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8">
              {t('hero.description')}
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-white px-8" asChild>
                <Link href="/menu">
                  {t('hero.viewMenu')}
                </Link>
              </Button>
              <Button size="lg" variant="outline" className="border-primary text-primary hover:bg-primary hover:text-white" asChild>
                <Link href="tel:8453811002">
                  {t('hero.orderOnline')}
                </Link>
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

