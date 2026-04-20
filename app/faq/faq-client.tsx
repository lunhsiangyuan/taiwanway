'use client'

import { useLanguage } from '@/lib/i18n/language-context'
import { faqs } from './faqs'
import Link from 'next/link'
import { ChevronDown } from 'lucide-react'
import { useState } from 'react'

export function FaqClient() {
  const { language } = useLanguage()
  const [openIndex, setOpenIndex] = useState<number | null>(0)

  const title =
    language === 'zh'
      ? '常見問題'
      : language === 'es'
        ? 'Preguntas Frecuentes'
        : 'Frequently Asked Questions'

  const subtitle =
    language === 'zh'
      ? '關於 TaiwanWay 臺灣味的常見問題 — 營業時間、菜單、外送、外燴'
      : language === 'es'
        ? 'Preguntas comunes sobre TaiwanWay — horarios, menú, entrega y catering'
        : 'Common questions about TaiwanWay — hours, menu, delivery, and catering'

  const contactLine =
    language === 'zh'
      ? '沒找到你的問題？'
      : language === 'es'
        ? '¿No encontró su pregunta?'
        : "Didn't find your question?"

  const contactCta =
    language === 'zh' ? '聯絡我們' : language === 'es' ? 'Contáctenos' : 'Contact us'

  return (
    <main className="min-h-screen bg-cream pt-24 pb-16">
      <div className="mx-auto max-w-3xl px-4">
        <nav aria-label="Breadcrumb" className="mb-6 text-sm text-muted-foreground">
          <ol className="flex items-center gap-2">
            <li>
              <Link href="/" className="hover:text-terracotta">
                {language === 'zh' ? '首頁' : language === 'es' ? 'Inicio' : 'Home'}
              </Link>
            </li>
            <li aria-hidden>/</li>
            <li aria-current="page" className="text-foreground font-medium">
              FAQ
            </li>
          </ol>
        </nav>

        <h1 className="font-body text-3xl sm:text-4xl font-bold text-foreground mb-3 tracking-tight">
          {title}
        </h1>
        <p className="font-body text-base text-muted-foreground mb-10">{subtitle}</p>

        <div className="space-y-3">
          {faqs.map((faq, i) => {
            const q =
              language === 'zh' ? faq.q_zh : language === 'es' ? faq.q_es : faq.q_en
            const a =
              language === 'zh' ? faq.a_zh : language === 'es' ? faq.a_es : faq.a_en
            const isOpen = openIndex === i

            return (
              <details
                key={i}
                open={isOpen}
                onToggle={(e) => {
                  if ((e.target as HTMLDetailsElement).open) setOpenIndex(i)
                  else if (openIndex === i) setOpenIndex(null)
                }}
                className="group rounded-lg border border-border bg-white shadow-sm overflow-hidden"
              >
                <summary className="flex items-center justify-between gap-4 cursor-pointer list-none px-5 py-4 hover:bg-sand/20 transition">
                  <h2 className="font-body text-base sm:text-lg font-semibold text-foreground leading-snug">
                    {q}
                  </h2>
                  <ChevronDown
                    className={`h-5 w-5 flex-shrink-0 text-terracotta transition-transform ${
                      isOpen ? 'rotate-180' : ''
                    }`}
                    aria-hidden
                  />
                </summary>
                <div className="font-body px-5 pb-5 pt-0 text-[0.95rem] text-foreground/80 leading-relaxed">
                  {a}
                </div>
              </details>
            )
          })}
        </div>

        <div className="mt-12 rounded-xl bg-sand/30 px-6 py-5 text-center">
          <p className="text-foreground mb-2">{contactLine}</p>
          <Link
            href="/contact"
            className="inline-flex items-center gap-2 rounded-full bg-terracotta px-5 py-2 text-sm font-bold text-cream hover:bg-terracotta/90 transition"
          >
            {contactCta}
          </Link>
        </div>
      </div>
    </main>
  )
}
