import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getSupabaseClient } from '@/lib/supabase';
import type { Product } from '@/types/product';
import { isValidSlug } from '@/types/product';
import { POSTERS } from '@/app/products/posters';
import ProductDetail from './product-detail';

const SITE = 'https://taiwanwayny.com';

/** 商品結構化資料（schema.org/Product）— 助 Google 複合式結果與 AI 引擎（GEO） */
function productJsonLd(product: Product) {
  const poster = POSTERS[product.slug];
  const jsonLd: Record<string, unknown> = {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: product.name_en,
    alternateName: product.name_zh,
    image: [poster ? `${SITE}${poster}` : product.image_url],
    description: product.description_en,
    url: `${SITE}/product/${product.slug}`,
  };
  if (product.brand) jsonLd.brand = { '@type': 'Brand', name: product.brand };
  if (product.price != null) {
    jsonLd.offers = {
      '@type': 'Offer',
      priceCurrency: 'USD',
      price: Number(product.price).toFixed(2),
      availability: 'https://schema.org/InStoreOnly',
      itemCondition: 'https://schema.org/NewCondition',
      seller: { '@type': 'CafeOrCoffeeShop', name: 'TaiwanWay 臺灣味', '@id': `${SITE}/#business` },
      areaServed: { '@type': 'City', name: 'Middletown, NY' },
    };
  }
  return jsonLd;
}

async function getProduct(slug: string): Promise<Product | null> {
  if (!isValidSlug(slug)) return null;
  try {
    const supabase = getSupabaseClient(false);
    const { data } = await supabase
      .from('products')
      .select('*')
      .eq('slug', slug)
      .eq('is_active', true)
      .single();
    return data;
  } catch {
    return null;
  }
}

export async function generateStaticParams() {
  // Graceful: return empty when env vars not available (build time)
  // Pages will be generated on-demand via ISR
  if (!process.env.NEXT_PUBLIC_SUPABASE_URL || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
    return [];
  }
  try {
    const supabase = getSupabaseClient(false);
    const { data } = await supabase
      .from('products')
      .select('slug')
      .eq('is_active', true);
    return (data || []).map((p) => ({ slug: p.slug }));
  } catch {
    return [];
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>;
}): Promise<Metadata> {
  const { slug } = await params;
  const product = await getProduct(slug);
  if (!product) {
    return { title: 'Product Not Found' };
  }

  return {
    title: `${product.name_en}`,
    description: product.description_en,
    openGraph: {
      title: `${product.name_zh} ${product.name_en}`,
      description: product.description_en,
      images: [{ url: product.image_url, width: 800, height: 800, alt: product.name_en }],
      type: 'website',
      siteName: 'Taiwanway 台灣味',
    },
    twitter: {
      card: 'summary_large_image',
      title: `${product.name_zh} ${product.name_en}`,
      description: product.description_en,
      images: [product.image_url],
    },
  };
}

export const revalidate = 3600;

export default async function ProductPage({
  params,
}: {
  params: Promise<{ slug: string }>;
}) {
  const { slug } = await params;
  const product = await getProduct(slug);

  if (!product) {
    notFound();
  }

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(productJsonLd(product)) }}
      />
      <ProductDetail product={product} />
    </>
  );
}
