export type BlogPost = {
  slug: string
  date: string // YYYY-MM-DD
  coverImage: string
  readingMinutes: number
  title: { zh: string; en: string; es: string }
  excerpt: { zh: string; en: string; es: string }
  tags: string[]
}

export const BLOG_POSTS: BlogPost[] = [
  {
    slug: 'why-our-pineapple-cake-uses-winter-melon',
    date: '2026-04-19',
    coverImage: '/images/pineapple-cake.png',
    readingMinutes: 5,
    tags: ['pineapple cake', 'Taiwanese', 'bakery', '鳳梨酥'],
    title: {
      zh: '為什麼我們的鳳梨酥用台灣空運土鳳梨 + 冬瓜餡',
      en: 'Why Our Pineapple Cake Uses Real Taiwanese Pineapple + Winter Melon',
      es: 'Por Qué Nuestro Pastel de Piña Usa Piña Taiwanesa + Melón de Invierno',
    },
    excerpt: {
      zh: '市售多數鳳梨酥用濃縮鳳梨醬、糖漿、香精，跟台灣現做的根本是兩種東西。我們堅持從台灣空運土鳳梨 + 古法冬瓜餡——為什麼這樣做，一顆 $3.25 值不值得？',
      en: 'Most US "pineapple cakes" are made with pineapple concentrate, corn syrup, and artificial flavor. We air-freight native Taiwanese pineapple and use a traditional winter melon base. Here\u2019s why — and what $3.25 actually buys you.',
      es: 'La mayoría de "pineapple cakes" en EE.UU. se hacen con concentrado de piña, jarabe de maíz y aromatizantes. Nosotros traemos piña nativa taiwanesa por aire y usamos relleno tradicional de melón de invierno. He aquí por qué.',
    },
  },
]

export function getPostBySlug(slug: string): BlogPost | undefined {
  return BLOG_POSTS.find((p) => p.slug === slug)
}
