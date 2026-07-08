'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import { faqs } from './faqs'
import Link from 'next/link'
import { ChevronDown, MessageCircleQuestion } from 'lucide-react'
import { useState } from 'react'

export function FaqClient() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'
  const [openIndex, setOpenIndex] = useState<number | null>(0)

  const eyebrow = lang === 'zh' ? '有問必答' : lang === 'es' ? 'Ayuda' : 'Help Center'
  const title =
    lang === 'zh' ? '常見問題' : lang === 'es' ? 'Preguntas Frecuentes' : 'Frequently Asked Questions'
  const subtitle =
    lang === 'zh'
      ? '關於 TaiwanWay 臺灣味的常見問題 — 營業時間、菜單、外送、訂位'
      : lang === 'es'
        ? 'Preguntas comunes sobre TaiwanWay — horarios, menú, entrega y reservas'
        : 'Common questions about TaiwanWay — hours, menu, delivery, and reservations'
  const contactLine =
    lang === 'zh' ? '沒找到你的問題？' : lang === 'es' ? '¿No encontró su pregunta?' : "Didn't find your question?"
  const contactSub =
    lang === 'zh'
      ? '直接聯絡我們，我們很樂意為你解答。'
      : lang === 'es'
        ? 'Contáctenos directamente, con gusto le ayudamos.'
        : "Reach out to us directly — we're happy to help."
  const contactCta = lang === 'zh' ? '聯絡我們' : lang === 'es' ? 'Contáctenos' : 'Contact Us'
  const home = lang === 'zh' ? '首頁' : lang === 'es' ? 'Inicio' : 'Home'

  return (
    <main className="min-h-screen bg-cream pb-20 pt-28">
      <div className="mx-auto max-w-3xl px-6">
        {/* 麵包屑 */}
        <nav aria-label="Breadcrumb" className="mb-8 font-body text-sm text-muted-foreground">
          <ol className="flex items-center gap-2">
            <li>
              <Link href="/" className="transition-colors hover:text-primary">
                {home}
              </Link>
            </li>
            <li aria-hidden>·</li>
            <li aria-current="page" className="font-medium text-foreground">
              FAQ
            </li>
          </ol>
        </nav>

        {/* 標題區 */}
        <header className="mb-12 text-center">
          <p className="mb-3 font-heading text-sm uppercase tracking-[0.28em] text-primary/70">{eyebrow}</p>
          <h1 className="font-heading text-4xl font-bold text-[#5b3a2e] md:text-5xl">{title}</h1>
          <span className="mx-auto mt-4 block h-1 w-16 rounded-full bg-primary/70" />
          <p className="mx-auto mt-5 max-w-xl font-body text-base leading-relaxed text-muted-foreground md:text-lg">
            {subtitle}
          </p>
        </header>

        {/* 手風琴 */}
        <div className="space-y-4">
          {faqs.map((faq, i) => {
            const q = lang === 'zh' ? faq.q_zh : lang === 'es' ? faq.q_es : faq.q_en
            const a = lang === 'zh' ? faq.a_zh : lang === 'es' ? faq.a_es : faq.a_en
            const isOpen = openIndex === i

            return (
              <details
                key={i}
                open={isOpen}
                onToggle={(e) => {
                  if ((e.target as HTMLDetailsElement).open) setOpenIndex(i)
                  else if (openIndex === i) setOpenIndex(null)
                }}
                className={`group overflow-hidden rounded-2xl bg-white shadow-sm ring-1 transition-shadow duration-300 hover:shadow-md ${
                  isOpen ? 'ring-primary/30' : 'ring-black/5'
                }`}
              >
                <summary className="flex cursor-pointer list-none items-center justify-between gap-4 px-6 py-5">
                  <h2 className="font-heading text-lg font-semibold leading-snug text-foreground md:text-xl">
                    {q}
                  </h2>
                  <span
                    className={`flex h-8 w-8 flex-shrink-0 items-center justify-center rounded-full transition-colors ${
                      isOpen ? 'bg-primary text-primary-foreground' : 'bg-primary/[0.08] text-primary'
                    }`}
                  >
                    <ChevronDown
                      className={`h-5 w-5 transition-transform duration-300 ${isOpen ? 'rotate-180' : ''}`}
                      aria-hidden
                    />
                  </span>
                </summary>
                <div className="px-6 pb-6 pt-0">
                  <p className="border-t border-black/5 pt-4 font-body text-base leading-relaxed text-foreground/75">
                    {a}
                  </p>
                </div>
              </details>
            )
          })}
        </div>

        {/* 底部聯絡 CTA */}
        <div className="mt-14 flex flex-col items-center rounded-2xl bg-primary/[0.06] px-6 py-10 text-center ring-1 ring-primary/10">
          <MessageCircleQuestion className="mb-3 h-8 w-8 text-primary" aria-hidden />
          <p className="font-heading text-xl font-bold text-foreground">{contactLine}</p>
          <p className="mt-1.5 max-w-sm font-body text-sm text-muted-foreground">{contactSub}</p>
          <Link
            href="/contact"
            className="mt-5 inline-flex items-center gap-2 rounded-full bg-primary px-6 py-2.5 font-body text-sm font-semibold text-primary-foreground transition hover:bg-accent"
          >
            {contactCta}
          </Link>
        </div>
      </div>
    </main>
  )
}
