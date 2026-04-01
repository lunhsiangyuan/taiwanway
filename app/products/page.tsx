import { Metadata } from 'next';
import { getSupabaseClient } from '@/lib/supabase';
import type { Product } from '@/types/product';
import ProductsGrid from './products-grid';

export const metadata: Metadata = {
  title: 'Products',
  description: 'Curated Taiwanese goods — tea, snacks, and specialty items from Taiwan.',
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
