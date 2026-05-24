'use client'

import { useEffect, useState } from 'react'
import { useLanguage } from '@/lib/i18n/language-context'

const CLOSURE_END = new Date('2026-08-14T00:00:00')

export function AnnouncementMarquee() {
  const { t } = useLanguage()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    setMounted(true)
  }, [])

  if (!mounted) return null
  if (new Date() >= CLOSURE_END) return null

  const text = t('announcement.closure')

  return (
    <div
      role="status"
      aria-live="polite"
      className="overflow-hidden bg-amber-500 text-amber-950 h-10 flex items-center"
    >
      <div className="marquee-track whitespace-nowrap font-medium text-sm sm:text-base">
        <span className="px-8">{text}</span>
        <span className="px-8" aria-hidden="true">{text}</span>
      </div>
    </div>
  )
}
