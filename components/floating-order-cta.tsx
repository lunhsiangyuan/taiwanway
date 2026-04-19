'use client'

import { useState, useEffect } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'
import { ShoppingBag, Truck } from 'lucide-react'

export function FloatingOrderCTA() {
  const { language } = useLanguage()
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setVisible(window.scrollY > window.innerHeight * 0.6)
    }
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const pickupLabel = language === 'zh' ? '來店自取' : language === 'es' ? 'Recoger' : 'Pickup'
  const deliveryLabel = language === 'zh' ? '外送' : 'Delivery'

  return (
    <div
      className={`fixed bottom-0 left-0 right-0 z-40 md:hidden transition-transform duration-300 ${
        visible ? 'translate-y-0' : 'translate-y-full'
      }`}
    >
      <div className="bg-[hsl(17,40%,12%)]/95 backdrop-blur-md px-4 py-3 shadow-[0_-4px_12px_rgba(0,0,0,0.15)]">
        <div className="flex gap-2">
          <a
            href="https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center justify-center gap-1.5 flex-1 rounded-full bg-[#06C167] py-3 font-body text-sm font-bold text-white transition-all active:scale-95"
          >
            <Truck className="h-4 w-4" />
            {deliveryLabel}
          </a>
          <a
            href="https://order.taiwanwayny.com/order"
            className="flex items-center justify-center gap-1.5 flex-1 rounded-full bg-white py-3 font-body text-sm font-bold text-[hsl(17,45%,40%)] transition-all active:scale-95"
          >
            <ShoppingBag className="h-4 w-4" />
            {pickupLabel}
          </a>
        </div>
      </div>
    </div>
  )
}
