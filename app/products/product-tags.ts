/**
 * 商品標籤系統（不動資料庫，純程式設定）
 * TAG_LABELS：標籤 key → 三語文字
 * PRODUCT_TAGS：商品 slug → 標籤 key 陣列（每個商品 2–3 個）
 * 之後要調整某商品的標籤（例如加「熱賣」「推薦送禮」），改這裡即可。
 */

type Lang = 'zh' | 'en' | 'es';

export const TAG_LABELS: Record<string, Record<Lang, string>> = {
  // 茶種
  oolong: { zh: '烏龍', en: 'Oolong', es: 'Oolong' },
  greenTea: { zh: '綠茶', en: 'Green Tea', es: 'Té Verde' },
  blackTea: { zh: '紅茶', en: 'Black Tea', es: 'Té Negro' },
  pouchong: { zh: '包種茶', en: 'Pouchong', es: 'Pouchong' },
  tieguanyin: { zh: '鐵觀音', en: 'Tieguanyin', es: 'Tieguanyin' },
  redOolong: { zh: '紅烏龍', en: 'Red Oolong', es: 'Oolong Rojo' },
  blackBeanTea: { zh: '黑豆茶', en: 'Black Bean Tea', es: 'Té de Frijol Negro' },
  roselle: { zh: '洛神花', en: 'Roselle', es: 'Jamaica' },
  herbalTea: { zh: '花草茶', en: 'Herbal Tea', es: 'Té de Hierbas' },
  highMountain: { zh: '高山茶', en: 'High-Mountain', es: 'Alta Montaña' },
  // 風味・香氣
  floral: { zh: '花香', en: 'Floral', es: 'Floral' },
  honey: { zh: '蜜香', en: 'Honey Aroma', es: 'Aroma a Miel' },
  milky: { zh: '奶香', en: 'Milky', es: 'Lácteo' },
  roasted: { zh: '熟茶', en: 'Roasted', es: 'Tostado' },
  caffeineFree: { zh: '無咖啡因', en: 'Caffeine-Free', es: 'Sin Cafeína' },
  blackSugar: { zh: '黑糖', en: 'Brown Sugar', es: 'Azúcar Moreno' },
  // 規格・包裝
  bags10: { zh: '10入', en: '10 Bags', es: '10 Bolsas' },
  bags15: { zh: '15入', en: '15 Bags', es: '15 Bolsas' },
  giftBox: { zh: '禮盒', en: 'Gift Box', es: 'Caja de Regalo' },
  limited: { zh: '限量', en: 'Limited', es: 'Edición Limitada' },
  // 果乾蜜餞
  preservedPlum: { zh: '蜜餞', en: 'Preserved Plum', es: 'Ciruela Confitada' },
  driedFruit: { zh: '果乾', en: 'Dried Fruit', es: 'Fruta Seca' },
  seedless: { zh: '無籽', en: 'Seedless', es: 'Sin Semilla' },
  pineapple: { zh: '鳳梨', en: 'Pineapple', es: 'Piña' },
  redDate: { zh: '紅棗', en: 'Red Date', es: 'Dátil Rojo' },
  plumCake: { zh: '梅餅', en: 'Plum Cake', es: 'Pastel de Ciruela' },
  assorted: { zh: '綜合口味', en: 'Assorted', es: 'Surtido' },
  lozenge: { zh: '潤喉糖', en: 'Herbal Candy', es: 'Caramelo de Hierbas' },
  plumCandy: { zh: '梅心糖', en: 'Plum Candy', es: 'Caramelo de Ciruela' },
  // 零食
  driedTofu: { zh: '豆干', en: 'Dried Tofu', es: 'Tofu Seco' },
  shacha: { zh: '沙茶', en: 'Shacha', es: 'Shacha' },
  mushroom: { zh: '香菇', en: 'Mushroom', es: 'Champiñón' },
  fishCracker: { zh: '魚酥', en: 'Fish Cracker', es: 'Galleta de Pescado' },
  // 通用賣點
  readyToEat: { zh: '即食', en: 'Ready to Eat', es: 'Listo para Comer' },
  additiveFree: { zh: '無添加', en: 'Additive-Free', es: 'Sin Aditivos' },
  award: { zh: '得獎', en: 'Award-Winning', es: 'Premiado' },
  heritage: { zh: '百年老店', en: 'Heritage', es: 'Tradición Centenaria' },
  signature: { zh: '招牌', en: 'Signature', es: 'Especialidad' },
  bakedFresh: { zh: '現烤', en: 'Freshly Baked', es: 'Recién Horneado' },
};

export const PRODUCT_TAGS: Record<string, string[]> = {
  // 茶
  'tang-ding-brown-sugar-longan-red-date': ['blackSugar', 'redDate', 'caffeineFree'],
  'honey-aroma-oolong-tea': ['oolong', 'honey', 'floral'],
  'dong-pian-oolong-tea': ['oolong', 'limited', 'floral'],
  'taiwan-jasmine-green-tea-10bags': ['greenTea', 'floral', 'bags10'],
  'taiwan-gardenia-pouchong-tea-10bags': ['pouchong', 'floral', 'bags10'],
  'taiwan-osmanthus-oolong-tea-10bags': ['oolong', 'floral', 'bags10'],
  'chen-fa-oolong-tea-gift-box-10bags': ['oolong', 'giftBox', 'heritage'],
  'taiwan-roasted-black-bean-tea-15bags': ['blackBeanTea', 'caffeineFree', 'bags15'],
  'hanyi-red-oolong-bop': ['redOolong', 'honey', 'roasted'],
  'jin-xuan-oolong-tea': ['oolong', 'milky', 'floral'],
  'qing-xin-oolong-tea': ['oolong', 'highMountain', 'floral'],
  'four-seasons-oolong-white-ginger-lily': ['oolong', 'floral'],
  'alishan-black-tea-floral-fruity': ['blackTea', 'highMountain', 'floral'],
  'chen-fa-mucha-tieguanyin-gift-box': ['tieguanyin', 'roasted', 'giftBox'],
  // 果乾蜜餞
  'taiwan-perilla-plum': ['preservedPlum', 'readyToEat'],
  'taiwan-osmanthus-plum': ['preservedPlum', 'floral'],
  'fullten-dried-guava': ['driedFruit', 'additiveFree'],
  'fullten-seedless-dried-mandarin': ['driedFruit', 'seedless'],
  'plums-honey-dried-plum-seedless': ['preservedPlum', 'seedless'],
  'plums-guanmiao-pineapple-plum': ['preservedPlum', 'pineapple'],
  'jin-he-tai-dried-roselle': ['roselle', 'herbalTea'],
  'herbal-hard-candy-asian-pear': ['lozenge', 'additiveFree'],
  'liang-ji-plum-cake-assorted': ['plumCake', 'assorted'],
  'tomita-plum-heart-candy': ['plumCandy', 'additiveFree'],
  'huixiang-red-date-chips': ['redDate', 'additiveFree'],
  // 零食
  'liao-hsin-lan-dried-tofu-shacha': ['driedTofu', 'shacha', 'readyToEat'],
  'sun-moon-lake-stewed-mushrooms': ['mushroom', 'readyToEat'],
  'te-yu-fish-crackers-original': ['fishCracker', 'award'],
  'freshly-baked-pineapple-cake-gift-box': ['bakedFresh', 'giftBox', 'signature'],
};

/** 取某商品的標籤三語文字（找不到回空陣列） */
export function getProductTags(slug: string, lang: Lang): string[] {
  const keys = PRODUCT_TAGS[slug] || [];
  return keys.map((k) => TAG_LABELS[k]?.[lang] || TAG_LABELS[k]?.en || k);
}
