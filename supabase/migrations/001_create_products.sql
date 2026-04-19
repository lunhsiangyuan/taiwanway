-- 產品介紹 QR Code 系統 — Supabase Migration
-- 在 Supabase Dashboard → SQL Editor 執行

CREATE TABLE IF NOT EXISTS products (
  id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  slug TEXT UNIQUE NOT NULL,
  image_url TEXT NOT NULL,
  price DECIMAL(10,2),
  brand TEXT,
  
  -- 三語文案
  name_zh TEXT NOT NULL,
  name_en TEXT NOT NULL,
  name_es TEXT NOT NULL,
  description_zh TEXT NOT NULL,
  description_en TEXT NOT NULL,
  description_es TEXT NOT NULL,
  
  -- 額外資訊
  how_to_use_zh TEXT,
  how_to_use_en TEXT,
  how_to_use_es TEXT,
  origin TEXT,
  
  -- QR Code
  qr_code_url TEXT,
  
  -- 狀態
  is_active BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);

-- RLS: 允許匿名讀取 active 產品
ALTER TABLE products ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Public can view active products" ON products
  FOR SELECT USING (is_active = true);

-- Service role 可以做所有操作（後台用）
CREATE POLICY "Service role full access" ON products
  FOR ALL USING (auth.role() = 'service_role');

-- 自動更新 updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER products_updated_at
  BEFORE UPDATE ON products
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at();
