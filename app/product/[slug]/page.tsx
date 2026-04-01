import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import { getSupabaseClient } from '@/lib/supabase';
import type { Product } from '@/types/product';
import { isValidSlug } from '@/types/product';
import ProductDetail from './product-detail';

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
    return { title: 'Product Not Found | Taiwanway' };
  }

  return {
    title: `${product.name_en} | Taiwanway`,
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

  return <ProductDetail product={product} />;
}
