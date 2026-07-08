'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useLanguage } from '@/lib/i18n/language-context'
import { BLOG_POSTS } from './posts'

export function BlogIndexClient() {
  const { language } = useLanguage()
  const lang = ['zh', 'en', 'es'].includes(language) ? language : 'en'

  const eyebrow = lang === 'zh' ? '台灣味筆記' : lang === 'es' ? 'Diario' : 'Journal'
  const heading =
    lang === 'zh' ? '台灣味筆記' : lang === 'es' ? 'Diario TaiwanWay' : 'TaiwanWay Journal'
  const subheading =
    lang === 'zh'
      ? '每一道菜、每一杯茶背後的故事'
      : lang === 'es'
        ? 'Historias detrás de cada plato y cada taza'
        : 'Stories behind every dish and every cup'
  const readLabel = lang === 'zh' ? '閱讀全文 →' : lang === 'es' ? 'Leer más →' : 'Read more →'
  const home = lang === 'zh' ? '首頁' : lang === 'es' ? 'Inicio' : 'Home'
  const minutesLabel = (n: number) =>
    lang === 'zh' ? `${n} 分鐘閱讀` : lang === 'es' ? `${n} min de lectura` : `${n} min read`

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
              Blog
            </li>
          </ol>
        </nav>

        {/* 標題區 */}
        <header className="mb-12 text-center">
          <p className="mb-3 font-heading text-sm uppercase tracking-[0.28em] text-primary/70">{eyebrow}</p>
          <h1 className="font-heading text-4xl font-bold text-[#5b3a2e] md:text-5xl">{heading}</h1>
          <span className="mx-auto mt-4 block h-1 w-16 rounded-full bg-primary/70" />
          <p className="mx-auto mt-5 max-w-xl font-body text-base leading-relaxed text-muted-foreground md:text-lg">
            {subheading}
          </p>
        </header>

        {/* 文章列表 */}
        <div className="space-y-8">
          {BLOG_POSTS.map((post) => (
            <Link
              key={post.slug}
              href={`/blog/${post.slug}`}
              className="group block overflow-hidden rounded-2xl bg-white shadow-sm ring-1 ring-black/5 transition-shadow duration-300 hover:shadow-md"
            >
              <div className="relative aspect-[16/9] w-full bg-[#faf7f2]">
                <Image
                  src={post.coverImage}
                  alt={post.title[lang] || post.title.en}
                  fill
                  className="object-cover transition-transform duration-500 group-hover:scale-[1.03]"
                  sizes="(min-width: 768px) 640px, 100vw"
                />
              </div>
              <div className="p-6 md:p-7">
                <div className="mb-2.5 flex items-center gap-3 font-body text-xs text-muted-foreground">
                  <time dateTime={post.date}>{post.date}</time>
                  <span aria-hidden>·</span>
                  <span>{minutesLabel(post.readingMinutes)}</span>
                </div>
                <h2 className="mb-3 font-heading text-2xl font-bold leading-snug text-foreground transition-colors group-hover:text-primary md:text-[1.6rem]">
                  {post.title[lang] || post.title.en}
                </h2>
                <p className="mb-4 font-body text-sm leading-relaxed text-foreground/75 md:text-base">
                  {post.excerpt[lang] || post.excerpt.en}
                </p>
                <span className="font-body text-sm font-semibold text-primary group-hover:underline">
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
