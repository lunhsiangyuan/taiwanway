'use client'

import Link from 'next/link'
import { Instagram, MapPin, Phone, Mail } from 'lucide-react'
import { useLanguage } from '@/lib/i18n/language-context'

const navLinks = [
  { key: 'nav.home', href: '/' },
  { key: 'nav.menu', href: '/menu' },
  { key: 'nav.about', href: '/about' },
  { key: 'nav.contact', href: '/contact' },
] as const

const hours = [
  { day: 'Mon', dayZh: '週一', dayEs: 'Lun', hours: '11AM - 7PM' },
  { day: 'Tue', dayZh: '週二', dayEs: 'Mar', hours: '11AM - 7PM' },
  { day: 'Wed', dayZh: '週三', dayEs: 'Mié', hours: null },
  { day: 'Thu', dayZh: '週四', dayEs: 'Jue', hours: null },
  { day: 'Fri', dayZh: '週五', dayEs: 'Vie', hours: '11AM - 7PM' },
  { day: 'Sat', dayZh: '週六', dayEs: 'Sáb', hours: '11AM - 7PM' },
  { day: 'Sun', dayZh: '週日', dayEs: 'Dom', hours: null },
] as const

const closedLabels: Record<string, string> = {
  zh: '公休',
  en: 'Closed',
  es: 'Cerrado',
}

export function Footer() {
  const { t, language } = useLanguage()

  const getDayName = (item: typeof hours[number]) => {
    if (language === 'zh') return item.dayZh
    if (language === 'es') return item.dayEs
    return item.day
  }

  const columnTitles = {
    quickLinks: { zh: '快速連結', en: 'Quick Links', es: 'Enlaces' },
    hours: { zh: '營業時間', en: 'Hours', es: 'Horario' },
    contact: { zh: '聯絡資訊', en: 'Contact', es: 'Contacto' },
  }

  const getTitle = (section: keyof typeof columnTitles) =>
    columnTitles[section][language] || columnTitles[section].en

  return (
    <footer className="bg-[#1A0F0A] pt-16 pb-8 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-10">
          {/* Column 1 - Brand */}
          <div>
            <Link href="/" className="font-heading text-2xl text-white hover:text-white/80 transition-colors">
              TaiwanWay
            </Link>
            <p className="text-white/60 font-body mt-1 text-lg">
              {language === 'zh' ? '臺灣味' : language === 'es' ? 'Sabor de Taiwán' : 'Taste of Taiwan'}
            </p>
            <p className="text-white/50 font-body text-sm mt-3 leading-relaxed">
              {language === 'zh'
                ? '在紐約體驗道地的台灣美食'
                : language === 'es'
                  ? 'Auténtica cocina taiwanesa en Nueva York'
                  : 'Authentic Taiwanese cuisine in New York'}
            </p>
            {/* Social Icons */}
            <div className="flex items-center gap-4 mt-5">
              <a
                href="https://www.instagram.com/taiwanway10940/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-white/40 hover:text-white transition-colors"
                aria-label="Instagram"
              >
                <Instagram className="w-5 h-5" />
              </a>
              <a
                href="https://www.facebook.com/taiwanway10940/"
                target="_blank"
                rel="noopener noreferrer"
                className="text-white/40 hover:text-white transition-colors"
                aria-label="Facebook"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" />
                </svg>
              </a>
            </div>
          </div>

          {/* Column 2 - Quick Links */}
          <div>
            <h3 className="text-white font-body font-semibold uppercase tracking-wider text-xs mb-4">
              {getTitle('quickLinks')}
            </h3>
            <ul className="space-y-3">
              {navLinks.map((item) => (
                <li key={item.key}>
                  <Link
                    href={item.href}
                    className="text-white/50 hover:text-white font-body text-sm transition-colors"
                  >
                    {t(item.key)}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          {/* Column 3 - Hours */}
          <div>
            <h3 className="text-white font-body font-semibold uppercase tracking-wider text-xs mb-4">
              {getTitle('hours')}
            </h3>
            <div className="space-y-2">
              {hours.map((item) => (
                <div key={item.day} className="flex justify-between gap-4">
                  <span className={`font-body text-sm ${item.hours ? 'text-white/50' : 'text-white/30'}`}>
                    {getDayName(item)}
                  </span>
                  <span className={`font-body text-sm ${item.hours ? 'text-white/50' : 'text-white/30'}`}>
                    {item.hours || closedLabels[language] || 'Closed'}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Column 4 - Contact */}
          <div>
            <h3 className="text-white font-body font-semibold uppercase tracking-wider text-xs mb-4">
              {getTitle('contact')}
            </h3>
            <div className="space-y-3">
              <div className="flex items-start gap-2">
                <MapPin className="w-4 h-4 text-white/40 mt-0.5 flex-shrink-0" />
                <p className="text-white/50 font-body text-sm leading-relaxed">
                  26 South St,<br />Middletown, NY 10940
                </p>
              </div>
              <div className="flex items-center gap-2">
                <Phone className="w-4 h-4 text-white/40 flex-shrink-0" />
                <a
                  href="tel:845-381-1002"
                  className="text-white/50 hover:text-white font-body text-sm transition-colors"
                >
                  845-381-1002
                </a>
              </div>
              <div className="flex items-center gap-2">
                <Mail className="w-4 h-4 text-white/40 flex-shrink-0" />
                <a
                  href="mailto:usamyheish@gmail.com"
                  className="text-white/50 hover:text-white font-body text-sm transition-colors"
                >
                  usamyheish@gmail.com
                </a>
              </div>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-white/10 mt-12 pt-8">
          <p className="text-white/30 text-sm text-center font-body">
            &copy; 2026 TaiwanWay. {t('footer.allRights')}.
          </p>
        </div>
      </div>
    </footer>
  )
}
