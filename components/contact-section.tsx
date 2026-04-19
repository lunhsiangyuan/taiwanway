'use client'

import { useRef, useEffect, useState } from 'react'
import { MapPin, Phone, Mail, Clock, ExternalLink } from 'lucide-react'
import { useLanguage } from '@/lib/i18n/language-context'

const businessHours = [
  { day: 'Monday', dayZh: '週一', dayEs: 'Lunes', hours: '11AM - 7PM' },
  { day: 'Tuesday', dayZh: '週二', dayEs: 'Martes', hours: '11AM - 7PM' },
  { day: 'Wednesday', dayZh: '週三', dayEs: 'Miércoles', hours: 'Closed', closed: true },
  { day: 'Thursday', dayZh: '週四', dayEs: 'Jueves', hours: 'Closed', closed: true },
  { day: 'Friday', dayZh: '週五', dayEs: 'Viernes', hours: '11AM - 7PM' },
  { day: 'Saturday', dayZh: '週六', dayEs: 'Sábado', hours: '11AM - 7PM' },
  { day: 'Sunday', dayZh: '週日', dayEs: 'Domingo', hours: 'Closed', closed: true },
] as const

const closedLabels: Record<string, string> = {
  zh: '公休',
  en: 'Closed',
  es: 'Cerrado',
}

export function ContactSection() {
  const { t, language } = useLanguage()
  const sectionRef = useRef<HTMLElement>(null)
  const [isVisible, setIsVisible] = useState(false)

  useEffect(() => {
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting) {
          setIsVisible(true)
          observer.disconnect()
        }
      },
      { threshold: 0.1 }
    )

    if (sectionRef.current) {
      observer.observe(sectionRef.current)
    }

    return () => observer.disconnect()
  }, [])

  const getDayName = (item: typeof businessHours[number]) => {
    if (language === 'zh') return item.dayZh
    if (language === 'es') return item.dayEs
    return item.day
  }

  const getHoursLabel = (item: typeof businessHours[number]) => {
    if ('closed' in item && item.closed) return closedLabels[language] || 'Closed'
    return item.hours
  }

  const sectionTitle: Record<string, string> = {
    zh: '來店用餐',
    en: 'Visit Us',
    es: 'Visítenos',
  }

  return (
    <section
      ref={sectionRef}
      id="contact"
      className="bg-[#FAF7F2] py-24 px-4"
    >
      <div className="max-w-6xl mx-auto">
        {/* Section Header */}
        <div
          className={`text-center mb-16 transition-all duration-700 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <h2 className="font-heading text-4xl md:text-5xl text-[#2D1810] mb-4">
            {sectionTitle[language] || sectionTitle.en}
          </h2>
          <div className="w-20 h-0.5 bg-gold mx-auto" />
        </div>

        {/* Two Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
          {/* Left Column - Map */}
          <div
            className={`transition-all duration-700 delay-200 ${
              isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 -translate-x-8'
            }`}
          >
            <div className="aspect-video overflow-hidden rounded-2xl shadow-lg">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2991.0!2d-74.4206521!3d41.4437301!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c33262597cb655%3A0x968db5356171d2eb!2s26%20South%20St%2C%20Middletown%2C%20NY%2010940!5e0!3m2!1sen!2sus!4v1706810757943!5m2!1sen!2sus"
                width="100%"
                height="100%"
                style={{ border: 0 }}
                allowFullScreen
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
                title="TaiwanWay Café Location — Middletown, NY"
              />
            </div>
          </div>

          {/* Right Column - Contact Info */}
          <div
            className={`space-y-6 transition-all duration-700 delay-400 ${
              isVisible ? 'opacity-100 translate-x-0' : 'opacity-0 translate-x-8'
            }`}
          >
            {/* Address */}
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-terracotta/10 flex items-center justify-center flex-shrink-0">
                <MapPin className="w-5 h-5 text-terracotta" />
              </div>
              <div>
                <p className="font-body font-semibold text-[#2D1810]">
                  {t('contact.address')}
                </p>
                <p className="font-body text-[#2D1810]/70">
                  26 South St, Middletown, NY 10940
                </p>
              </div>
            </div>

            {/* Phone */}
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-terracotta/10 flex items-center justify-center flex-shrink-0">
                <Phone className="w-5 h-5 text-terracotta" />
              </div>
              <div>
                <p className="font-body font-semibold text-[#2D1810]">
                  {t('contact.phone')}
                </p>
                <a
                  href="tel:845-381-1002"
                  className="font-body text-[#2D1810]/70 hover:text-terracotta transition-colors"
                >
                  845-381-1002
                </a>
              </div>
            </div>

            {/* Email */}
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-terracotta/10 flex items-center justify-center flex-shrink-0">
                <Mail className="w-5 h-5 text-terracotta" />
              </div>
              <div>
                <p className="font-body font-semibold text-[#2D1810]">
                  {t('contact.email')}
                </p>
                <a
                  href="mailto:usamyheish@gmail.com"
                  className="font-body text-[#2D1810]/70 hover:text-terracotta transition-colors"
                >
                  usamyheish@gmail.com
                </a>
              </div>
            </div>

            {/* Business Hours */}
            <div className="flex items-start gap-4">
              <div className="w-10 h-10 rounded-full bg-terracotta/10 flex items-center justify-center flex-shrink-0 mt-0.5">
                <Clock className="w-5 h-5 text-terracotta" />
              </div>
              <div>
                <p className="font-body font-semibold text-[#2D1810] mb-2">
                  {t('contact.businessHours')}
                </p>
                <div className="space-y-1">
                  {businessHours.map((item) => (
                    <div
                      key={item.day}
                      className="flex justify-between gap-8 font-body text-sm"
                    >
                      <span className={'closed' in item ? 'text-[#2D1810]/40' : 'text-[#2D1810]/70'}>
                        {getDayName(item)}
                      </span>
                      <span className={'closed' in item ? 'text-[#2D1810]/40' : 'text-[#2D1810]/70'}>
                        {getHoursLabel(item)}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* CTA Buttons */}
            <div className="flex flex-wrap gap-4 pt-4">
              <a
                href="https://www.google.com/maps/dir/?api=1&destination=26+South+St+Middletown+NY+10940"
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 bg-gold text-white font-body font-semibold px-6 py-3 rounded-full hover:bg-gold/90 transition-colors"
              >
                <ExternalLink className="w-4 h-4" />
                Get Directions
              </a>
              <a
                href="tel:845-381-1002"
                className="inline-flex items-center gap-2 border-2 border-terracotta text-terracotta font-body font-semibold px-6 py-3 rounded-full hover:bg-terracotta hover:text-white transition-colors"
              >
                <Phone className="w-4 h-4" />
                Call Us
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
