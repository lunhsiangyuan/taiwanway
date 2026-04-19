import { Metadata } from 'next';
import { getSupabaseClient } from '@/lib/supabase';
import type { Product } from '@/types/product';
import ProductsGrid from './products-grid';

export const metadata: Metadata = {
  title: 'Taiwanese Products | Tea, Snacks & Specialty Goods',
  description: 'Curated Taiwanese goods — premium tea, handmade pineapple cakes, traditional snacks and specialty items imported from Taiwan. Shop at TaiwanWay in Middletown, NY.',
  keywords: [
    'Taiwanese snacks NY',
    'Taiwan tea online',
    'handmade pineapple cake',
    'authentic Taiwanese products',
    'Taiwanese specialty goods',
    'imported Taiwan snacks',
    'TaiwanWay shop',
    '台灣零食 紐約',
    '台灣茶葉 美國',
  ],
  alternates: { canonical: '/products' },
  openGraph: {
    title: 'Taiwanese Products | TaiwanWay Shop',
    description: 'Shop premium Taiwanese tea, handmade pineapple cakes, and specialty goods imported from Taiwan.',
    url: '/products',
    images: ['/images/og-storefront.jpg'],
  },
};

export const revalidate = 3600;

async function getProducts(): Promise<Product[]> {
  if (!process.env.NEXT_PUBLIC_SUPABASE_URL || !process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY) {
    return [];
  }
  try {
    const supabase = getSupabaseClient(false);
    const { data } = await supabase
      .from('products')
      .select('*')
      .eq('is_active', true)
      .order('created_at', { ascending: true });
    return data || [];
  } catch {
    return [];
  }
}

export default async function ProductsPage() {
  const products = await getProducts();

  return (
    <div className="min-h-screen bg-amber-50 pt-20">
      <ProductsGrid products={products} />
    </div>
  );
}
