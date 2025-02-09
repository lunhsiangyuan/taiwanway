'use client'

import Image from "next/image"
import { useLanguage } from "@/lib/i18n/language-context"

export function PineappleCakeSection() {
  const { t } = useLanguage()
  return (
    <section id="pineapple-cake" className="py-20 bg-secondary/30">
      <h2 className="text-3xl font-bold mb-6 px-4">手工點心</h2>
      <div className="container px-0 lg:px-4">
        <div className="flex flex-col items-center lg:flex-row">
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="relative h-48 w-full">
              <Image
                src="/鳳梨酥.jpeg"
                alt="台灣鳳梨酥 (手工現作)"
                fill
                className="object-cover object-center w-full h-full"
              />
            </div>
            <div className="p-4">
              <h3 className="font-semibold text-lg mb-2">台灣鳳梨酥 (手工現作)</h3>
              <p className="text-sm text-gray-600 mb-2">酥脆外皮,內餡飽滿的台灣名產</p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
