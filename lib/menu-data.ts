/**
 * TaiwanWay 產品數據
 * 模仿春水堂風格：包含圖片、多語言名稱、分類、詳細描述
 */

export interface Product {
  id: string;
  category: string;
  image: {
    hero: string;      // 2880px WebP
    product: string;   // 800px WebP
    thumbnail: string; // 400px WebP
  };
  name: {
    zh: string;
    en: string;
    es?: string;
  };
  tags: string[];  // 例如：辣、冷飲、熱飲、素食
  description: {
    zh: string;
    en: string;
    es?: string;
  };
  price?: number;
  allergens?: string[];  // 過敏原
}

/**
 * 產品分類
 */
export const CATEGORIES = {
  MAIN_DISHES: 'main-dishes',      // 主餐
  BUBBLE_TEA: 'bubble-tea',        // 珍珠奶茶系列
  MILK_TEA: 'milk-tea',            // 奶茶系列
  GREEN_TEA: 'green-tea',          // 綠茶系列
  LEMONADE: 'lemonade',            // 檸檬飲品
  DESSERTS: 'desserts',            // 甜點
} as const;

/**
 * 產品目錄（僅包含飲料品項，主餐已在輪播中展示）
 */
export const PRODUCTS: Product[] = [

  // ============ 珍珠奶茶系列 ============
  {
    id: 'brown-sugar-bubble-milk',
    category: CATEGORIES.BUBBLE_TEA,
    image: {
      hero: '/images/products/brown-sugar-bubble-milk-hero.webp',
      product: '/images/products/brown-sugar-bubble-milk-product.webp',
      thumbnail: '/images/products/brown-sugar-bubble-milk-thumbnail.webp',
    },
    name: {
      zh: '黑糖珍珠鮮奶',
      en: 'Brown Sugar Bubble Milk',
      es: 'Leche con Perlas de Azúcar Morena',
    },
    tags: ['冷飲', '無咖啡因'],
    description: {
      zh: '香醇濃郁的黑糖漿在杯壁流淌，呈現迷人的虎紋圖樣。新鮮鮮奶搭配手工熬煮的黑糖珍珠，每一顆珍珠Q彈有勁，帶著焦糖香氣。黑糖的甘甜與鮮奶的醇厚完美融合，每一口都是幸福的滋味。',
      en: 'Rich brown sugar syrup cascades down the cup creating mesmerizing tiger stripes. Fresh milk paired with handcrafted brown sugar tapioca pearls-each pearl perfectly chewy with caramel notes. The sweetness of brown sugar and creaminess of milk create pure bliss in every sip.',
      es: 'El rico jarabe de azúcar morena cae por la taza creando rayas de tigre fascinantes. Leche fresca combinada con perlas de tapioca de azúcar morena hechas a mano, cada perla perfectamente masticable con notas de caramelo.',
    },
    allergens: ['乳製品'],
  },
  {
    id: 'bubble-tea-hot',
    category: CATEGORIES.BUBBLE_TEA,
    image: {
      hero: '/images/products/bubble-tea-hot-hero.webp',
      product: '/images/products/bubble-tea-hot-product.webp',
      thumbnail: '/images/products/bubble-tea-hot-thumbnail.webp',
    },
    name: {
      zh: '招牌珍珠奶茶（熱）',
      en: 'Signature Bubble Tea (Hot)',
      es: 'Té de Burbujas Signature (Caliente)',
    },
    tags: ['熱飲'],
    description: {
      zh: '台灣珍珠奶茶的經典原味，熱騰騰的奶茶搭配Q彈珍珠，溫暖身心。嚴選紅茶與鮮奶完美比例調配，香氣四溢，口感滑順。每一顆珍珠都是當日手工熬煮，保證最佳口感。冬日裡最溫暖的陪伴。',
      en: 'The classic original Taiwanese bubble tea served hot to warm your soul. Premium black tea perfectly blended with fresh milk, aromatic and smooth. Each tapioca pearl is handcrafted daily for optimal texture. The perfect warm companion for cold days.',
      es: 'El clásico té de burbujas taiwanés original servido caliente para calentar tu alma. Té negro premium perfectamente mezclado con leche fresca, aromático y suave. Cada perla de tapioca se elabora artesanalmente todos los días.',
    },
    allergens: ['乳製品'],
  },
  {
    id: 'jasmine-green-bubble-tea',
    category: CATEGORIES.BUBBLE_TEA,
    image: {
      hero: '/images/products/jasmine-green-bubble-tea-hero.webp',
      product: '/images/products/jasmine-green-bubble-tea-product.webp',
      thumbnail: '/images/products/jasmine-green-bubble-tea-thumbnail.webp',
    },
    name: {
      zh: '茉香綠茶珍珠',
      en: 'Jasmine Green Bubble Tea',
      es: 'Té Verde de Jazmín con Perlas',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '嚴選高山茉莉綠茶，花香清雅，茶韻悠長。搭配Q彈珍珠，清爽不膩，帶來優雅的品茗體驗。茉莉花的芬芳與綠茶的甘甜交織，珍珠的嚼勁增添層次感，是喜愛清新口感的最佳選擇。',
      en: 'Premium high-mountain jasmine green tea with elegant floral aroma and lingering tea notes. Paired with chewy tapioca pearls for a refreshing, non-greasy experience. The jasmine fragrance intertwines with green tea sweetness while pearls add delightful texture.',
      es: 'Té verde de jazmín premium de alta montaña con elegante aroma floral y notas de té persistentes. Combinado con perlas de tapioca masticables para una experiencia refrescante y sin grasa.',
    },
    allergens: [],
  },
  {
    id: 'honey-oolong-bubble-tea',
    category: CATEGORIES.BUBBLE_TEA,
    image: {
      hero: '/images/products/honey-oolong-bubble-tea-hero.webp',
      product: '/images/products/honey-oolong-bubble-tea-product.webp',
      thumbnail: '/images/products/honey-oolong-bubble-tea-thumbnail.webp',
    },
    name: {
      zh: '蜜香烏龍珍珠',
      en: 'Honey Oolong Bubble Tea',
      es: 'Té Oolong de Miel con Perlas',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '台灣高山烏龍茶，經小綠葉蟬咬食後散發獨特蜜香。茶湯金黃透亮，蜜香馥郁，回甘綿長。搭配手工珍珠，層次豐富，是烏龍茶愛好者的極致享受。每一口都能感受到台灣茶藝的精髓。',
      en: 'Taiwan high-mountain oolong tea with unique honey fragrance from leafhopper bites. Golden amber tea with rich honey aroma and lingering sweet aftertaste. Paired with handcrafted pearls for complex layers, the ultimate treat for oolong tea lovers.',
      es: 'Té oolong de alta montaña de Taiwán con fragancia única de miel de picaduras de saltahojas. Té ámbar dorado con rico aroma a miel y regusto dulce persistente. Combinado con perlas artesanales.',
    },
    allergens: [],
  },

  // ============ 奶茶系列 ============
  {
    id: 'taiwanese-milk-tea',
    category: CATEGORIES.MILK_TEA,
    image: {
      hero: '/images/products/taiwanese-milk-tea-hero.webp',
      product: '/images/products/taiwanese-milk-tea-product.webp',
      thumbnail: '/images/products/taiwanese-milk-tea-thumbnail.webp',
    },
    name: {
      zh: '台式奶茶',
      en: 'Taiwanese Milk Tea',
      es: 'Té con Leche Taiwanés',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '經典台式奶茶，選用錫蘭紅茶與香濃鮮奶，比例恰到好處。茶香與奶香完美平衡，不過甜不過膩，滑順爽口。這是最純粹的台灣味道，也是每個台灣人的童年回憶。',
      en: 'Classic Taiwanese milk tea with Ceylon black tea and rich fresh milk in perfect proportion. Tea aroma and milk fragrance beautifully balanced-not too sweet, not too rich, smooth and refreshing. The purest taste of Taiwan and a childhood memory for every Taiwanese.',
      es: 'Té con leche taiwanés clásico con té negro de Ceilán y leche fresca rica en proporción perfecta. Aroma a té y fragancia a leche bellamente equilibrados, no demasiado dulce, ni demasiado rico, suave y refrescante.',
    },
    allergens: ['乳製品'],
  },
  {
    id: 'jasmine-green-milk-tea',
    category: CATEGORIES.MILK_TEA,
    image: {
      hero: '/images/products/jasmine-green-milk-tea-hero.webp',
      product: '/images/products/jasmine-green-milk-tea-product.webp',
      thumbnail: '/images/products/jasmine-green-milk-tea-thumbnail.webp',
    },
    name: {
      zh: '茉香綠奶茶',
      en: 'Jasmine Green Milk Tea',
      es: 'Té Verde de Jazmín con Leche',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '清新的茉莉綠茶遇上香醇鮮奶，碰撞出優雅的滋味。茉莉花香淡雅不膩，綠茶的甘甜與鮮奶的柔滑相輔相成。口感清爽，適合喜歡清新風味的您，每一口都是花香與茶香的交響樂章。',
      en: 'Refreshing jasmine green tea meets creamy fresh milk in an elegant flavor collision. Subtle jasmine fragrance complements the sweet green tea and smooth milk. Light and refreshing, perfect for those who prefer delicate flavors-a symphony of floral and tea notes.',
      es: 'El refrescante té verde de jazmín se encuentra con leche fresca cremosa en una elegante colisión de sabores. La sutil fragancia de jazmín complementa el té verde dulce y la leche suave.',
    },
    allergens: ['乳製品'],
  },

  // ============ 綠茶系列 ============
  {
    id: 'honey-jasmine-green-tea',
    category: CATEGORIES.GREEN_TEA,
    image: {
      hero: '/images/products/honey-jasmine-green-tea-hero.webp',
      product: '/images/products/honey-jasmine-green-tea-product.webp',
      thumbnail: '/images/products/honey-jasmine-green-tea-thumbnail.webp',
    },
    name: {
      zh: '蜂蜜茉香綠茶',
      en: 'Honey Jasmine Green Tea',
      es: 'Té Verde de Jazmín con Miel',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '高山茉莉綠茶加入天然蜂蜜，甘甜清香。茉莉花的優雅與蜂蜜的醇厚完美結合，茶湯金黃透亮，入口清爽回甘。不添加人工糖分，保留茶葉原始風味，是追求健康與美味的最佳選擇。',
      en: "High-mountain jasmine green tea enhanced with natural honey for sweet freshness. Elegant jasmine meets rich honey in perfect harmony, creating golden amber tea that's refreshing with a sweet aftertaste. No artificial sweeteners-pure tea flavor for health-conscious tea lovers.",
      es: 'Té verde de jazmín de alta montaña realzado con miel natural para una frescura dulce. El elegante jazmín se encuentra con la rica miel en perfecta armonía, creando té ámbar dorado que es refrescante.',
    },
    allergens: [],
  },

  // ============ 檸檬飲品 ============
  {
    id: 'winter-melon-lemonade',
    category: CATEGORIES.LEMONADE,
    image: {
      hero: '/images/products/winter-melon-lemonade-hero.webp',
      product: '/images/products/winter-melon-lemonade-product.webp',
      thumbnail: '/images/products/winter-melon-lemonade-thumbnail.webp',
    },
    name: {
      zh: '冬瓜檸檬',
      en: 'Winter Melon Lemonade',
      es: 'Limonada de Melón de Invierno',
    },
    tags: ['冷飲', '無咖啡因'],
    description: {
      zh: '台灣古早味飲品，手工熬煮冬瓜糖加入新鮮檸檬汁。冬瓜的清甜與檸檬的酸爽完美平衡，清涼解渴，生津止渴。炎炎夏日的最佳良伴，每一口都是消暑的清涼享受。',
      en: 'Traditional Taiwanese beverage with handcrafted winter melon syrup and fresh lemon juice. The subtle sweetness of winter melon perfectly balances the tangy lemon, refreshing and thirst-quenching. The ultimate summer companion-every sip brings cooling satisfaction.',
      es: 'Bebida tradicional taiwanesa con jarabe de melón de invierno artesanal y jugo de limón fresco. La dulzura sutil del melón de invierno equilibra perfectamente el limón picante, refrescante y que quita la sed.',
    },
    allergens: [],
  },

  // ============ 甜點 ============
  {
    id: 'mango-coconut-pannacotta',
    category: CATEGORIES.DESSERTS,
    image: {
      hero: '/images/products/mango-coconut-pannacotta-hero.webp',
      product: '/images/products/mango-coconut-pannacotta-product.webp',
      thumbnail: '/images/products/mango-coconut-pannacotta-thumbnail.webp',
    },
    name: {
      zh: '芒果椰香奶酪',
      en: 'Mango Coconut Pannacotta',
      es: 'Pannacotta de Coco y Mango',
    },
    tags: ['甜點'],
    description: {
      zh: '義式奶酪融入熱帶風情，椰奶的清香與芒果的香甜交織。奶酪口感滑嫩細緻，搭配新鮮芒果丁，每一口都是南國的陽光滋味。清爽不膩，是飯後的完美句點。',
      en: 'Italian pannacotta meets tropical flavors-coconut milk fragrance intertwines with sweet mango. Silky smooth texture paired with fresh mango cubes delivers sunshine in every bite. Light and refreshing, the perfect ending to any meal.',
      es: 'La pannacotta italiana se encuentra con sabores tropicales: la fragancia de leche de coco se entrelaza con el mango dulce. Textura sedosa y suave combinada con cubos de mango fresco.',
    },
    allergens: ['乳製品'],
  },
  {
    id: 'taro-pannacotta',
    category: CATEGORIES.DESSERTS,
    image: {
      hero: '/images/products/taro-pannacotta-hero.webp',
      product: '/images/products/taro-pannacotta-product.webp',
      thumbnail: '/images/products/taro-pannacotta-thumbnail.webp',
    },
    name: {
      zh: '芋頭奶酪',
      en: 'Taro Pannacotta',
      es: 'Pannacotta de Taro',
    },
    tags: ['甜點'],
    description: {
      zh: '嚴選大甲芋頭，手工蒸製成泥，與義式奶酪完美結合。芋頭的綿密香甜與奶酪的滑嫩口感相得益彰，淡紫色澤優雅誘人。每一口都能品嚐到芋頭的天然香氣，是芋頭控的最愛。',
      en: 'Premium Dajia taro handcrafted into puree and perfectly blended with Italian pannacotta. The creamy sweetness of taro complements the silky texture-elegant lavender hue. Every spoonful delivers natural taro fragrance, a taro lover\'s dream dessert.',
      es: 'Taro premium de Dajia elaborado artesanalmente en puré y perfectamente mezclado con pannacotta italiana. La dulzura cremosa del taro complementa la textura sedosa: elegante tono lavanda.',
    },
    allergens: ['乳製品'],
  },
  {
    id: 'tea-cake',
    category: CATEGORIES.DESSERTS,
    image: {
      hero: '/images/products/tea-cake-hero.webp',
      product: '/images/products/tea-cake-product.webp',
      thumbnail: '/images/products/tea-cake-thumbnail.webp',
    },
    name: {
      zh: '茶點糕',
      en: 'Tea Cake',
      es: 'Pastel de Té',
    },
    tags: ['甜點', '手工烘焙'],
    description: {
      zh: '傳統台式糕點，每日新鮮手作。綠豆沙內餡細緻綿密，外皮酥鬆不黏牙。淡淡的茶香與綠豆的清甜相互輝映，搭配茶飲享用更添風味。是下午茶的絕佳伴侶，也是伴手禮的首選。',
      en: 'Traditional Taiwanese pastry handcrafted fresh daily. Delicate mung bean filling wrapped in flaky, non-sticky pastry. Subtle tea aroma complements the sweet mung bean-perfect with tea for afternoon enjoyment. An ideal gift or teatime companion.',
      es: 'Pastelería tradicional taiwanesa elaborada a mano fresca diariamente. Delicado relleno de frijol mungo envuelto en hojaldre no pegajoso. El sutil aroma a té complementa el dulce frijol mungo.',
    },
    allergens: ['麩質'],
  },
];

/**
 * 依分類取得產品
 */
export function getProductsByCategory(category: string): Product[] {
  return PRODUCTS.filter(p => p.category === category);
}

/**
 * 依 ID 取得產品
 */
export function getProductById(id: string): Product | undefined {
  return PRODUCTS.find(p => p.id === id);
}

/**
 * 取得所有分類
 */
export function getAllCategories(): string[] {
  return Object.values(CATEGORIES);
}
