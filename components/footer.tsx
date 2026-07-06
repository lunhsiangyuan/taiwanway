'use client'

import Image from 'next/image'
import { Instagram, MapPin, Phone, Clock } from 'lucide-react'
import { useLanguage } from '@/lib/i18n/language-context'

export function Footer() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  const cafeName = lang === 'zh' ? 'TaiwanWay 臺灣味' : 'Taiwan Way Cafe'
  const hoursLabel =
    lang === 'zh' ? '週一 · 二 · 五 · 六　11:00am – 7:00pm'
      : 'Mon · Tue · Fri · Sat　11:00am – 7:00pm'
  const closedNote =
    lang === 'zh' ? '週三 · 四 · 日 公休'
      : lang === 'es' ? 'Cerrado Mié · Jue · Dom'
        : 'Closed Wed · Thu · Sun'

  const note = lang === 'zh'
    ? ['謝謝你來到這裡，', '希望我們的味道，', '能成為你生活的一部分。']
    : lang === 'es'
      ? ['Gracias por venir.', 'Ojalá nuestro sabor', 'sea parte de tu día.']
      : ['Thank you for stopping by.', 'We hope our flavors become', 'a small part of your everyday.']

  return (
    <footer className="border-t border-black/5 bg-[#f0e7d6] text-foreground">
      <div className="mx-auto max-w-screen-xl px-6 py-12 md:px-12 md:py-14">
        <div className="grid grid-cols-1 gap-10 md:grid-cols-[auto_1fr_auto] md:items-center md:gap-12">
          {/* 左：磚紅 logo（淺底上清楚可見） */}
          <div className="flex justify-center md:justify-start">
            <Image
              src="/brand/logo-mascot-trim.png"
              alt="TaiwanWay 臺灣味"
              width={1673}
              height={1208}
              className="h-28 w-auto md:h-32"
            />
          </div>

          {/* 中：店家資訊 */}
          <div className="text-center md:text-left">
            <h3 className="font-heading text-2xl font-bold text-primary">{cafeName}</h3>
            <div className="mt-4 space-y-2.5 font-body text-sm text-foreground/80">
              <a
                href="https://www.google.com/maps/search/?api=1&query=TaiwanWay+26+South+St+Middletown+NY+10940"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center justify-center gap-2 transition-colors hover:text-primary md:justify-start"
              >
                <MapPin className="h-4 w-4 shrink-0 text-primary" />
                26 South St, Middletown, NY 10940
              </a>
              <a
                href="tel:+18453811002"
                className="flex items-center justify-center gap-2 transition-colors hover:text-primary md:justify-start"
              >
                <Phone className="h-4 w-4 shrink-0 text-primary" />
                (845) 381-1002
              </a>
              <p className="flex items-center justify-center gap-2 md:justify-start">
                <Clock className="h-4 w-4 shrink-0 text-primary" />
                {hoursLabel}
              </p>
              <p className="pl-6 text-xs text-foreground/50">{closedNote}</p>
            </div>
            <div className="mt-5 flex items-center justify-center gap-4 md:justify-start">
              <a
                href="https://www.instagram.com/taiwanway10940/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-foreground/60 transition-colors hover:text-primary"
                aria-label="Instagram"
              >
                <Instagram className="h-5 w-5" />
              </a>
              <a
                href="https://www.facebook.com/taiwanway10940/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-foreground/60 transition-colors hover:text-primary"
                aria-label="Facebook"
              >
                <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                </svg>
              </a>
            </div>
          </div>

          {/* 右：手寫暖心話 */}
          <div className="text-center md:text-right">
            <p className="font-heading text-xl italic leading-relaxed text-primary/90 md:text-2xl">
              {note.map((line, i) => (
                <span key={i} className="block">{line}</span>
              ))}
            </p>
            <span className="mt-2 inline-block text-primary/50">♡</span>
          </div>
        </div>

        <div className="mt-10 border-t border-black/10 pt-6 text-center">
          <p className="font-body text-xs text-foreground/50">
            &copy; 2026 TaiwanWay · Middletown, NY
          </p>
        </div>
      </div>
    </footer>
  )
}
