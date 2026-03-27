import { NextRequest, NextResponse } from 'next/server';
import { getSupabaseClient } from '@/lib/supabase';

const ADMIN_PASSWORD = process.env.ADMIN_PASSWORD;

function isAdmin(request: NextRequest): boolean {
  return request.headers.get('x-admin-password') === ADMIN_PASSWORD;
}

// Field allowlist — only these fields can be written
const ALLOWED_FIELDS = [
  'slug', 'image_url', 'price', 'brand',
  'name_zh', 'name_en', 'name_es',
  'description_zh', 'description_en', 'description_es',
  'how_to_use_zh', 'how_to_use_en', 'how_to_use_es',
  'origin', 'qr_code_url', 'is_active',
] as const;

function pickAllowed(body: Record<string, unknown>): Record<string, unknown> {
  const result: Record<string, unknown> = {};
  for (const key of ALLOWED_FIELDS) {
    if (key in body) result[key] = body[key];
  }
  return result;
}

// GET /api/products
export async function GET(request: NextRequest) {
  const admin = isAdmin(request);
  const supabase = getSupabaseClient(admin);
  const slug = request.nextUrl.searchParams.get('slug');

  let query = supabase.from('products').select('*');
  if (slug) {
    query = query.eq('slug', slug);
  } else if (!admin) {
    query = query.eq('is_active', true);
  }

  const { data, error } = await query;
  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json(data);
}

// POST /api/products
export async function POST(request: NextRequest) {
  if (!isAdmin(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const supabase = getSupabaseClient(true);
  const body = await request.json();
  const safe = pickAllowed(body);

  // Validate required fields
  if (!safe.slug || !safe.name_zh || !safe.name_en || !safe.name_es || !safe.image_url) {
    return NextResponse.json({ error: 'Missing required fields: slug, name_zh, name_en, name_es, image_url' }, { status: 400 });
  }

  const { data, error } = await supabase.from('products').insert([safe]).select().single();
  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json(data, { status: 201 });
}

// PATCH /api/products
export async function PATCH(request: NextRequest) {
  if (!isAdmin(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const supabase = getSupabaseClient(true);
  const body = await request.json();
  const { id } = body;

  if (!id) {
    return NextResponse.json({ error: 'id is required' }, { status: 400 });
  }

  const updates = pickAllowed(body);
  if (Object.keys(updates).length === 0) {
    return NextResponse.json({ error: 'No valid fields to update' }, { status: 400 });
  }

  const { data, error } = await supabase
    .from('products')
    .update(updates)
    .eq('id', id)
    .select()
    .single();

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json(data);
}

// DELETE /api/products (soft delete)
export async function DELETE(request: NextRequest) {
  if (!isAdmin(request)) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }
  const supabase = getSupabaseClient(true);
  const { id } = await request.json();

  if (!id) {
    return NextResponse.json({ error: 'id is required' }, { status: 400 });
  }

  const { error } = await supabase
    .from('products')
    .update({ is_active: false })
    .eq('id', id);

  if (error) {
    return NextResponse.json({ error: error.message }, { status: 500 });
  }
  return NextResponse.json({ message: 'Product deactivated' });
}
