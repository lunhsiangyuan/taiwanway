/**
 * 卡片顯示用的「短名稱」對照表（不動資料庫；詳情頁仍用完整名稱）
 * 只列需要縮短的商品；沒列到的沿用資料庫原名。
 * 要調整某商品卡片上的顯示名，改這裡即可。
 */

import type { Product } from '@/types/product';
import { getProductName } from '@/types/product';

type Lang = 'zh' | 'en' | 'es';

export const SHORT_NAMES: Record<string, Record<Lang, string>> = {
  // 茶
  'hanyi-red-oolong-bop': { zh: '紅烏龍 BOP', en: 'Red Oolong BOP', es: 'Oolong Rojo BOP' },
  'qing-xin-oolong-tea': { zh: '青心烏龍', en: 'Qing Xin Oolong', es: 'Oolong Qing Xin' },
  'four-seasons-oolong-white-ginger-lily': { zh: '四季春烏龍', en: 'Four Seasons Oolong', es: 'Oolong Four Seasons' },
  'alishan-black-tea-floral-fruity': { zh: '阿里山紅茶', en: 'Alishan Black Tea', es: 'Té Negro Alishan' },
  'chen-fa-mucha-tieguanyin-gift-box': { zh: '木柵鐵觀音禮盒', en: 'Mucha Tieguanyin Gift Box', es: 'Tieguanyin Mucha (Regalo)' },
  'chen-fa-oolong-tea-gift-box-10bags': { zh: '烏龍茶包禮盒', en: 'Oolong Tea Gift Box', es: 'Oolong en Bolsitas (Regalo)' },
  'taiwan-osmanthus-oolong-tea-10bags': { zh: '桂花烏龍', en: 'Osmanthus Oolong', es: 'Oolong de Osmanto' },
  'taiwan-jasmine-green-tea-10bags': { zh: '茉莉綠茶', en: 'Jasmine Green Tea', es: 'Té Verde de Jazmín' },
  'taiwan-gardenia-pouchong-tea-10bags': { zh: '梔子花包種茶', en: 'Gardenia Pouchong Tea', es: 'Pouchong de Gardenia' },
  // 果乾蜜餞
  'fullten-seedless-dried-mandarin': { zh: '無籽甜蜜柑', en: 'Seedless Dried Mandarin', es: 'Mandarina Seca Sin Semilla' },
  'plums-honey-dried-plum-seedless': { zh: '蜂蜜無籽梅肉', en: 'Honey Dried Plum', es: 'Ciruela con Miel' },
  'plums-guanmiao-pineapple-plum': { zh: '關廟鳳梨梅', en: 'Guanmiao Pineapple Plum', es: 'Ciruela con Piña de Guanmiao' },
  'herbal-hard-candy-asian-pear': { zh: '草本蜂梨糖', en: 'Asian Pear Herbal Candy', es: 'Caramelo de Pera' },
  'liang-ji-plum-cake-assorted': { zh: '綜合梅餅', en: 'Assorted Plum Cake', es: 'Pastel de Ciruela Surtido' },
  'tomita-plum-heart-candy': { zh: '梅心糖', en: 'Plum Heart Candy', es: 'Caramelo de Ciruela' },
  'huixiang-red-date-chips': { zh: '紅棗脆片', en: 'Crispy Red Date Chips', es: 'Chips de Dátil Rojo' },
  // 零食
  'te-yu-fish-crackers-original': { zh: '魚酥（原味）', en: 'Fish Crackers (Original)', es: 'Galletas de Pescado' },
  'freshly-baked-pineapple-cake-gift-box': { zh: '現烤鳳梨酥禮盒', en: 'Pineapple Cake Gift Box', es: 'Pastel de Piña (Regalo)' },
};

/** 卡片顯示用短名稱（沒對照到就回完整名稱） */
export function getShortName(p: Product, lang: string): string {
  const l: Lang = (['zh', 'en', 'es'] as const).includes(lang as Lang) ? (lang as Lang) : 'en';
  return SHORT_NAMES[p.slug]?.[l] || getProductName(p, lang as Lang);
}
