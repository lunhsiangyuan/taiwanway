'use client'

import { Clock, MapPin, Phone, Mail, Instagram, Navigation } from 'lucide-react'
import { useLanguage } from '@/lib/i18n/language-context'
import { OrderButton } from './order-button'

const MAPS = 'https://www.google.com/maps/search/?api=1&query=TaiwanWay+26+South+St+Middletown+NY+10940'

export function Contact() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  const t = {
    heading: { zh: '歡迎光臨', en: 'Visit Us', es: 'Visítanos' }[lang],
    intro: {
      zh: '想吃碗熱騰騰的牛肉麵、喝杯手搖，或帶包台灣零食回家——歡迎來店坐坐，也可以叫外送或直接來電。',
      en: 'Come in for a warm bowl of beef noodle soup, a hand-shaken tea, or a bag of Taiwanese snacks — dine in, order delivery, or give us a call.',
      es: 'Ven por un tazón de fideos, un té artesanal o snacks de Taiwán — en tienda, a domicilio o llámanos.',
    }[lang],
    hours: { zh: '營業時間', en: 'Hours', es: 'Horario' }[lang],
    hoursVal: { zh: '週一 · 二 · 五 · 六　11:00am – 7:00pm', en: 'Mon · Tue · Fri · Sat　11:00am – 7:00pm', es: 'Lun · Mar · Vie · Sáb　11:00am – 7:00pm' }[lang],
    closed: { zh: '週三 · 四 · 日 公休', en: 'Closed Wed · Thu · Sun', es: 'Cerrado Mié · Jue · Dom' }[lang],
    address: { zh: '地址', en: 'Address', es: 'Dirección' }[lang],
    phone: { zh: '電話', en: 'Phone', es: 'Teléfono' }[lang],
    email: { zh: '電子郵件', en: 'Email', es: 'Correo' }[lang],
    directions: { zh: '導航到店', en: 'Get Directions', es: 'Cómo llegar' }[lang],
    call: { zh: '來電洽詢', en: 'Call Us', es: 'Llámanos' }[lang],
    findUs: { zh: '來找我們', en: 'Find Us', es: 'Encuéntranos' }[lang],
  }

  return (
    <section className="bg-cream py-16 md:py-20">
      <div className="mx-auto max-w-6xl px-6 md:px-8">
        <div className="mb-12 text-center">
          <h2 className="font-heading text-3xl font-bold text-primary md:text-4xl">{t.heading}</h2>
          <span className="mx-auto mt-3 block h-1 w-16 rounded-full bg-primary/70" />
          <p className="mx-auto mt-4 max-w-xl font-body text-base text-muted-foreground md:text-lg">{t.intro}</p>
        </div>

        <div className="grid items-start gap-8 lg:grid-cols-2 lg:gap-12">
          {/* 左：資訊 */}
          <div className="space-y-6">
            <InfoRow icon={MapPin} label={t.address}>
              <a href={MAPS} target="_blank" rel="noopener noreferrer" className="hover:text-primary">26 South St, Middletown, NY 10940</a>
            </InfoRow>
            <InfoRow icon={Clock} label={t.hours}>
              <p>{t.hoursVal}</p>
              <p className="text-sm text-muted-foreground">{t.closed}</p>
            </InfoRow>
            <InfoRow icon={Phone} label={t.phone}>
              <a href="tel:+18453811002" className="hover:text-primary">(845) 381-1002</a>
            </InfoRow>
            <InfoRow icon={Mail} label={t.email}>
              <a href="mailto:taiwanway10940@gmail.com" className="hover:text-primary">taiwanway10940@gmail.com</a>
            </InfoRow>

            {/* CTA 按鈕 */}
            <div className="flex flex-wrap items-center gap-3 pt-2">
              <OrderButton align="start" className="px-5 py-2.5 text-sm" />
              <a href="tel:+18453811002" className="inline-flex items-center gap-2 rounded-full border-2 border-primary px-5 py-2.5 font-body text-sm font-semibold text-primary transition hover:bg-primary hover:text-primary-foreground">
                <Phone className="h-4 w-4" />{t.call}
              </a>
            </div>

            {/* 社群 */}
            <div className="flex items-center gap-4 pt-1">
              <a href="https://www.instagram.com/taiwanway10940/" target="_blank" rel="noopener noreferrer" aria-label="Instagram" className="text-foreground/60 transition hover:text-primary">
                <Instagram className="h-5 w-5" />
              </a>
              <a href="https://www.facebook.com/taiwanway10940/" target="_blank" rel="noopener noreferrer" aria-label="Facebook" className="text-foreground/60 transition hover:text-primary">
                <svg className="h-5 w-5" viewBox="0 0 24 24" fill="currentColor"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z" /></svg>
              </a>
            </div>
          </div>

          {/* 右：地圖 */}
          <div>
            <div className="overflow-hidden rounded-2xl shadow-md ring-1 ring-black/5">
              <iframe
                src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2991.0!2d-74.4206521!3d41.4437301!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x89c33262597cb655%3A0x968db5356171d2eb!2s26%20South%20St%2C%20Middletown%2C%20NY%2010940!5e0!3m2!1sen!2sus!4v1706810757943!5m2!1sen!2sus"
                title={t.findUs}
                className="aspect-[4/3] w-full border-0"
                allowFullScreen
                loading="lazy"
                referrerPolicy="no-referrer-when-downgrade"
              />
            </div>
            <a href={MAPS} target="_blank" rel="noopener noreferrer" className="mt-4 inline-flex items-center gap-2 font-body text-sm font-semibold text-primary hover:underline">
              <Navigation className="h-4 w-4" />{t.directions}
            </a>
          </div>
        </div>
      </div>
    </section>
  )
}

function InfoRow({ icon: Icon, label, children }: { icon: typeof MapPin; label: string; children: React.ReactNode }) {
  return (
    <div className="flex items-start gap-4">
      <div className="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-primary/[0.08]">
        <Icon className="h-5 w-5 text-primary" />
      </div>
      <div className="pt-1">
        <h3 className="font-heading text-base font-bold text-foreground">{label}</h3>
        <div className="mt-0.5 font-body text-foreground/80">{children}</div>
      </div>
    </div>
  )
}
