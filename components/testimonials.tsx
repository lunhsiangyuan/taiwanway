'use client'

import { useRef, useEffect, useState, useCallback } from 'react'
import { Star } from 'lucide-react'
import { useLanguage } from '@/lib/i18n/language-context'

interface Review {
  name: string
  rating: number
  text: string
  source: 'Yelp'
}

const reviews: Review[] = [
  {
    name: 'Heather S.',
    rating: 5,
    text: "I am in-love with this place. I felt instantly calm with the lovely atmosphere and beautiful tea. My husband had the slow roasted beef noodles which was amazing!!!!!!! I can't wait to go back.",
    source: 'Yelp',
  },
  {
    name: 'Didit P.',
    rating: 5,
    text: 'This place is delightful! They served delicious braised pork rice and beef noodle soup. The bubble tea has a very delicate flavor and not at all overly sweet!',
    source: 'Yelp',
  },
  {
    name: 'Kimberly W.',
    rating: 5,
    text: "Delightful modern tea house in the heart of Middletown! Upon entering, you're greeted by a small cafe with a bright atmosphere. I had a seasonal choice, the Apple Jade Dew green tea. My friend had the Taiwanese bubble tea. Both are excellent!",
    source: 'Yelp',
  },
  {
    name: 'Russell D.',
    rating: 5,
    text: 'Great bubble tea as well as desserts! Braised pork bowl was delicious!! Service is friendly',
    source: 'Yelp',
  },
]

const sectionTitles: Record<string, string> = {
  zh: '顧客好評',
  en: 'What Our Customers Say',
  es: 'Lo Que Dicen Nuestros Clientes',
}

const readMoreLabels: Record<string, string> = {
  zh: '閱讀更多',
  en: 'Read more',
  es: 'Leer más',
}

const TRUNCATE_LENGTH = 120
const AUTO_SCROLL_INTERVAL = 4000
const CARD_WIDTH = 340
const CARD_GAP = 24

function StarRating({ rating }: { rating: number }) {
  return (
    <div className="flex gap-0.5">
      {Array.from({ length: 5 }, (_, i) => (
        <Star
          key={i}
          className={`w-4 h-4 ${
            i < rating
              ? 'fill-[hsl(44,80%,40%)] text-[hsl(44,80%,40%)]'
              : 'fill-none text-[#2D1810]/20'
          }`}
        />
      ))}
    </div>
  )
}

function ReviewCard({
  review,
  language,
}: {
  review: Review
  language: string
}) {
  const [expanded, setExpanded] = useState(false)
  const shouldTruncate = review.text.length > TRUNCATE_LENGTH

  return (
    <div
      className="flex-shrink-0 w-[300px] sm:w-[340px] min-h-[220px] bg-white rounded-2xl p-6 shadow-md
                 border border-[#2D1810]/5 flex flex-col justify-between
                 hover:shadow-lg transition-shadow duration-300"
    >
      {/* 星級評分與來源 */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <StarRating rating={review.rating} />
          <span className="text-xs font-body font-semibold px-2 py-0.5 rounded-full bg-[#d32323]/10 text-[#d32323]">
            {review.source}
          </span>
        </div>

        {/* 評論內容 */}
        <p className="font-body text-sm leading-relaxed text-[#2D1810]/80">
          &ldquo;
          {expanded || !shouldTruncate
            ? review.text
            : `${review.text.slice(0, TRUNCATE_LENGTH).trimEnd()}...`}
          &rdquo;
          {shouldTruncate && !expanded && (
            <button
              onClick={() => setExpanded(true)}
              className="ml-1 text-[hsl(17,45%,47%)] font-semibold hover:underline text-sm"
            >
              {readMoreLabels[language] || readMoreLabels.en}
            </button>
          )}
        </p>
      </div>

      {/* 評論者名稱 */}
      <p className="mt-4 font-body font-semibold text-sm text-[#2D1810]">
        {review.name}
      </p>
    </div>
  )
}

export function Testimonials() {
  const { language } = useLanguage()
  const sectionRef = useRef<HTMLElement>(null)
  const scrollRef = useRef<HTMLDivElement>(null)
  const [isVisible, setIsVisible] = useState(false)
  const [isPaused, setIsPaused] = useState(false)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  // Intersection Observer 淡入動畫
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

  // 自動捲動
  const scrollNext = useCallback(() => {
    const container = scrollRef.current
    if (!container) return

    const step = CARD_WIDTH + CARD_GAP
    const maxScroll = container.scrollWidth - container.clientWidth

    if (container.scrollLeft >= maxScroll - 10) {
      // 回到開頭（平滑）
      container.scrollTo({ left: 0, behavior: 'smooth' })
    } else {
      container.scrollBy({ left: step, behavior: 'smooth' })
    }
  }, [])

  useEffect(() => {
    if (isPaused || !isVisible) {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
      return
    }

    intervalRef.current = setInterval(scrollNext, AUTO_SCROLL_INTERVAL)

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
        intervalRef.current = null
      }
    }
  }, [isPaused, isVisible, scrollNext])

  return (
    <section
      ref={sectionRef}
      className="relative bg-[#2D1810] py-24 overflow-hidden"
    >
      {/* 背景裝飾 */}
      <div className="absolute -top-32 -left-32 h-[400px] w-[400px] rounded-full bg-[hsl(44,80%,40%)]/[0.04] blur-3xl" />
      <div className="absolute -bottom-24 -right-24 h-[300px] w-[300px] rounded-full bg-[hsl(17,45%,57%)]/[0.05] blur-3xl" />

      <div className="relative mx-auto max-w-6xl px-4">
        {/* 區塊標題 */}
        <div
          className={`text-center mb-14 transition-all duration-700 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <h2 className="font-heading text-4xl md:text-5xl text-[#FAF7F2] mb-4">
            {sectionTitles[language] || sectionTitles.en}
          </h2>
          <div className="mx-auto h-0.5 w-20 bg-[hsl(44,80%,40%)] mb-6" />

          {/* 整體評分摘要 */}
          <div className="flex items-center justify-center gap-6 font-body text-[#FAF7F2]/80">
            <div className="flex items-center gap-2">
              <Star className="w-5 h-5 fill-[hsl(44,80%,40%)] text-[hsl(44,80%,40%)]" />
              <span className="text-lg font-semibold text-[#FAF7F2]">
                Google 4.9★
              </span>
              <span className="text-sm">(69 reviews)</span>
            </div>
            <span className="text-[#FAF7F2]/30">|</span>
            <div className="flex items-center gap-2">
              <Star className="w-5 h-5 fill-[hsl(44,80%,40%)] text-[hsl(44,80%,40%)]" />
              <span className="text-lg font-semibold text-[#FAF7F2]">
                Yelp 4.8★
              </span>
              <span className="text-sm">(8 reviews)</span>
            </div>
          </div>
        </div>

        {/* 評論卡片輪播 */}
        <div
          className={`transition-all duration-700 delay-300 ${
            isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-8'
          }`}
        >
          <div
            ref={scrollRef}
            onMouseEnter={() => setIsPaused(true)}
            onMouseLeave={() => setIsPaused(false)}
            onTouchStart={() => setIsPaused(true)}
            onTouchEnd={() => setIsPaused(false)}
            className="flex gap-6 overflow-x-auto pb-4 scrollbar-hide snap-x snap-mandatory"
            style={{
              scrollbarWidth: 'none',
              msOverflowStyle: 'none',
              WebkitOverflowScrolling: 'touch',
            }}
          >
            {reviews.map((review) => (
              <div key={review.name} className="snap-start">
                <ReviewCard review={review} language={language} />
              </div>
            ))}
          </div>
        </div>

        {/* Yelp 連結 */}
        <div
          className={`text-center mt-10 transition-all duration-700 delay-500 ${
            isVisible ? 'opacity-100' : 'opacity-0'
          }`}
        >
          <a
            href="https://www.google.com/maps/place//@41.4437301,-74.4206521,17z/data=!4m8!3m7!1s0x89c33262597cb655:0x968db5356171d2eb!8m2!3d41.4437301!4d-74.4206521!9m1!1b1"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 font-body text-sm text-[#FAF7F2]/60 hover:text-[hsl(44,80%,40%)] transition-colors"
          >
            View all reviews on Google →
          </a>
        </div>
      </div>
    </section>
  )
}
