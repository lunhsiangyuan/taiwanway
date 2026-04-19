export type Product = {
  id: string;
  slug: string;
  image_url: string;
  price: number | null;
  brand: string | null;
  name_zh: string;
  name_en: string;
  name_es: string;
  description_zh: string;
  description_en: string;
  description_es: string;
  how_to_use_zh: string | null;
  how_to_use_en: string | null;
  how_to_use_es: string | null;
  origin: string | null;
  qr_code_url?: string | null;
  is_active?: boolean;
  is_new_arrival?: boolean;
  featured_until?: string | null;
  created_at?: string;
};

export type Language = 'zh' | 'en' | 'es';

/** 取得對應語系的產品名稱 */
export function getProductName(product: Product, lang: Language): string {
  return product[`name_${lang}`] || product.name_en;
}

/** 取得對應語系的產品描述 */
export function getProductDescription(product: Product, lang: Language): string {
  return product[`description_${lang}`] || product.description_en;
}

/** 取得對應語系的使用方式 */
export function getProductHowToUse(product: Product, lang: Language): string | null {
  return product[`how_to_use_${lang}`] || product.how_to_use_en;
}

/** Slug 格式驗證 */
export const SLUG_REGEX = /^[a-z0-9][a-z0-9-]*$/;

export function isValidSlug(slug: string): boolean {
  return SLUG_REGEX.test(slug) && slug.length <= 200;
}
