'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import { ShoppingBag, Truck, Clock, MapPin } from 'lucide-react'

export function OrderBanner() {
  const { language } = useLanguage()

  const title = language === 'zh'
    ? '線上訂餐'
    : language === 'es'
      ? 'Ordena en Linea'
      : 'Order Online'

  const pickupLabel = language === 'zh' ? '來店自取' : language === 'es' ? 'Recoger' : 'Pickup'
  const deliveryLabel = language === 'zh' ? '外送 Uber Eats' : 'Delivery (Uber Eats)'

  const hours = language === 'zh'
    ? '週一二五六 11AM–7PM'
    : 'Mon/Tue/Fri/Sat 11AM–7PM'

  return (
    <div className="bg-[hsl(17,45%,47%)] text-white">
      <div className="mx-auto max-w-6xl px-4 py-4 flex flex-col sm:flex-row items-center justify-between gap-3">
        <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-1 text-sm">
          <span className="font-semibold">{title}</span>
          <span className="flex items-center gap-1 text-white/80">
            <Clock className="h-3.5 w-3.5" /> {hours}
          </span>
          <span className="flex items-center gap-1 text-white/80">
            <MapPin className="h-3.5 w-3.5" /> 26 South St, Middletown
          </span>
        </div>
        <div className="flex items-center gap-2">
          <a
            href="https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-1.5 rounded-full bg-[#06C167] px-4 py-2 text-sm font-bold text-white transition-all hover:bg-[#05a557] active:scale-95 whitespace-nowrap"
          >
            <Truck className="h-3.5 w-3.5" />
            {deliveryLabel}
          </a>
          <a
            href="https://order.taiwanwayny.com/order"
            className="inline-flex items-center gap-1.5 rounded-full bg-white px-4 py-2 text-sm font-bold text-[hsl(17,45%,40%)] transition-all hover:bg-white/90 active:scale-95 whitespace-nowrap"
          >
            <ShoppingBag className="h-3.5 w-3.5" />
            {pickupLabel}
          </a>
        </div>
      </div>
    </div>
  )
}
