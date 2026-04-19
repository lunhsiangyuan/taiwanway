import { NextRequest, NextResponse } from 'next/server';
import { getSupabaseClient } from '@/lib/supabase';
import { isAdmin, unauthorizedResponse } from '@/lib/auth';

// POST /api/products/activate — batch activate staged products
export async function POST(request: NextRequest) {
  if (!isAdmin(request)) return unauthorizedResponse();
  const supabase = getSupabaseClient(true);

  const body = await request.json().catch(() => ({}));
  const ids: string[] | undefined = body.ids;

  let query = supabase
    .from('products')
    .update({ is_active: true })
    .eq('is_active', false);

  // If specific IDs provided, only activate those
  if (ids?.length) {
    query = query.in('id', ids);
  }

  const { data, error, count } = await query.select();
  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json({ activated: data?.length ?? 0, products: data });
}
