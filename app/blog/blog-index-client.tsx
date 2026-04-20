'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useLanguage } from '@/lib/i18n/language-context'
import { BLOG_POSTS } from './posts'

export function BlogIndexClient() {
  const { language } = useLanguage()

  const heading =
    language === 'zh' ? '台灣味筆記' : language === 'es' ? 'Diario TaiwanWay' : 'TaiwanWay Journal'
  const subheading =
    language === 'zh'
      ? '每一道菜、每一杯茶背後的故事'
      : language === 'es'
        ? 'Historias detrás de cada plato y cada taza'
        : 'Stories behind every dish and every cup'
  const readLabel =
    language === 'zh' ? '閱讀全文 →' : language === 'es' ? 'Leer más →' : 'Read more →'
  const minutesLabel = (n: number) =>
    language === 'zh' ? `${n} 分鐘閱讀` : language === 'es' ? `${n} min de lectura` : `${n} min read`

  return (
    <main className="min-h-screen bg-cream pt-28 pb-20">
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
              Blog
            </li>
          </ol>
        </nav>

        <header className="mb-10">
          <h1 className="font-body text-3xl md:text-4xl font-bold text-foreground mb-3 tracking-tight">
            {heading}
          </h1>
          <p className="font-body text-base md:text-lg text-muted-foreground leading-relaxed">
            {subheading}
          </p>
        </header>

        <div className="space-y-8">
          {BLOG_POSTS.map((post) => (
            <Link
              key={post.slug}
              href={`/blog/${post.slug}`}
              className="group block overflow-hidden rounded-2xl border border-border bg-white shadow-sm transition hover:shadow-md"
            >
              <div className="relative aspect-[16/9] w-full bg-sand/30">
                <Image
                  src={post.coverImage}
                  alt={post.title[language] || post.title.en}
                  fill
                  className="object-cover"
                  sizes="(min-width: 768px) 640px, 100vw"
                />
              </div>
              <div className="p-6">
                <div className="mb-2 flex items-center gap-3 text-xs text-muted-foreground">
                  <time dateTime={post.date}>{post.date}</time>
                  <span aria-hidden>·</span>
                  <span>{minutesLabel(post.readingMinutes)}</span>
                </div>
                <h2 className="font-body text-xl md:text-2xl font-semibold text-foreground mb-3 group-hover:text-terracotta transition">
                  {post.title[language] || post.title.en}
                </h2>
                <p className="font-body text-sm md:text-base text-foreground/80 leading-relaxed mb-4">
                  {post.excerpt[language] || post.excerpt.en}
                </p>
                <span className="font-body text-sm font-semibold text-terracotta group-hover:underline">
                  {readLabel}
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </main>
  )
}
