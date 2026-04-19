-- 新品上架功能 — 每月限量 New Arrival 區塊
-- 在 Supabase Dashboard → SQL Editor 執行

-- 新增 2 個欄位
ALTER TABLE products
  ADD COLUMN IF NOT EXISTS is_new_arrival BOOLEAN DEFAULT false,
  ADD COLUMN IF NOT EXISTS featured_until DATE;

-- 索引加速查詢（snack-shop 會頻繁查詢 is_new_arrival = true 的商品）
CREATE INDEX IF NOT EXISTS idx_products_new_arrival
  ON products (is_new_arrival, featured_until)
  WHERE is_new_arrival = true;

COMMENT ON COLUMN products.is_new_arrival IS '是否在首頁 New Arrival 區塊顯示（管理員手動勾選）';
COMMENT ON COLUMN products.featured_until IS '自動下架日期；超過此日期即使 is_new_arrival=true 也不顯示';
