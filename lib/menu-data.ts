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
  // 雙尺寸定價（主餐常見：小碗 / 大碗）。若同時存在，顯示時優先使用 priceRange
  priceRange?: {
    regular: number;
    large: number;
  };
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
 * 產品目錄
 */
export const PRODUCTS: Product[] = [

  // ============ 主餐 ============
  {
    id: 'braised-beef-noodle-soup',
    category: CATEGORIES.MAIN_DISHES,
    image: {
      hero: '/images/beef-noodle-soup-v3.jpg',
      product: '/images/beef-noodle-soup-v3.jpg',
      thumbnail: '/images/beef-noodle-soup-v3.jpg',
    },
    name: {
      zh: '紅燒牛肉麵',
      en: 'Braised Beef Noodle Soup',
      es: 'Sopa de Fideos con Ternera Estofada',
    },
    tags: ['主餐', '湯麵'],
    description: {
      zh: '台灣經典紅燒牛肉麵——精選牛腩以香料與醬油慢燉一整天，湯頭濃郁鮮甜。搭配 Q 彈手工麵條與當季青菜，一碗上桌，就是最道地的台灣午後。',
      en: 'The Taiwanese classic — beef brisket slow-simmered all day in a rich spiced soy broth, served over hand-pulled chewy noodles with seasonal greens. Every bowl captures a Taiwan afternoon.',
      es: 'El clásico taiwanés — pecho de res cocinado a fuego lento todo el día en caldo especiado de salsa de soja, servido sobre fideos artesanales con verduras de temporada. Un bol que captura una tarde en Taiwán.',
    },
    priceRange: { regular: 13.99, large: 15.99 },
    allergens: ['麩質', '大豆'],
  },
  {
    id: 'sesame-beef-noodles',
    category: CATEGORIES.MAIN_DISHES,
    image: {
      hero: '/images/sesame-beef-noodles-v3.jpg',
      product: '/images/sesame-beef-noodles-v3.jpg',
      thumbnail: '/images/sesame-beef-noodles-v3.jpg',
    },
    name: {
      zh: '麻醬牛肉乾麵',
      en: 'Sesame Beef Noodles',
      es: 'Fideos con Ternera y Pasta de Sésamo',
    },
    tags: ['主餐', '乾麵'],
    description: {
      zh: '手工 Q 彈麵條淋上濃香芝麻醬，搭配滷製入味的牛腱肉片與當季青菜。攪拌均勻的瞬間，整碗的芝麻香氣瞬間釋放。',
      en: 'Hand-pulled chewy noodles tossed in rich sesame paste, topped with tender braised beef shank and seasonal greens. Mix to release a bowlful of toasted-sesame aroma.',
      es: 'Fideos artesanales al dente con pasta de sésamo, cubiertos con jarrete de ternera estofado y verduras de temporada. Mezcla para liberar el aroma del sésamo tostado.',
    },
    priceRange: { regular: 13.99, large: 15.99 },
    allergens: ['麩質', '芝麻', '大豆'],
  },
  {
    id: 'braised-pork-rice',
    category: CATEGORIES.MAIN_DISHES,
    image: {
      hero: '/images/braised-pork-rice-v5.jpg',
      product: '/images/braised-pork-rice-v5.jpg',
      thumbnail: '/images/braised-pork-rice-v5.jpg',
    },
    name: {
      zh: '古早味滷肉飯',
      en: 'Braised Pork Rice',
      es: 'Arroz con Cerdo Estofado',
    },
    tags: ['主餐', '飯類'],
    description: {
      zh: '阿嬤的古早味——豬五花切小丁，以醬油、糖與五香慢燉至融化入味，淋在熱騰騰的香 Q 白飯上。一口，就是台灣街邊最經典的家常滋味。',
      en: 'Grandma\u2019s traditional braise — minced pork belly slow-cooked in soy, sugar, and five-spice until melt-in-your-mouth tender, ladled over steaming rice. The classic taste of Taiwan street food.',
      es: 'La receta tradicional de la abuela — panceta de cerdo picada cocinada a fuego lento con soja, azúcar y cinco especias, servida sobre arroz humeante. El sabor clásico de la comida callejera taiwanesa.',
    },
    priceRange: { regular: 10.99, large: 12.99 },
    allergens: ['大豆'],
  },
  {
    id: 'chiayi-chicken-rice',
    category: CATEGORIES.MAIN_DISHES,
    image: {
      hero: '/images/chiayi-chicken-rice-v3.jpg',
      product: '/images/chiayi-chicken-rice-v3.jpg',
      thumbnail: '/images/chiayi-chicken-rice-v3.jpg',
    },
    name: {
      zh: '嘉義雞肉飯',
      en: 'Chiayi Chicken Rice',
      es: 'Arroz con Pollo al Estilo Chiayi',
    },
    tags: ['主餐', '飯類'],
    description: {
      zh: '來自台灣嘉義的經典——火雞肉手撕成絲，淋上金黃紅蔥頭酥與特製醬汁，鋪在粒粒分明的白飯上。簡單三層味道，卻是很多台灣人心中的白月光。',
      en: 'A classic from Chiayi, Taiwan — hand-shredded turkey over fluffy steamed rice, finished with golden fried shallots and a signature sauce. Three simple layers every Taiwanese dreams of.',
      es: 'Un clásico de Chiayi, Taiwán — pavo desmenuzado a mano sobre arroz al vapor, terminado con chalotas doradas fritas y salsa de la casa. Tres capas simples con las que sueña todo taiwanés.',
    },
    priceRange: { regular: 10.99, large: 12.99 },
    allergens: ['大豆'],
  },
  {
    id: 'sakura-shrimp-sticky-rice',
    category: CATEGORIES.MAIN_DISHES,
    image: {
      hero: '/images/sakura-shrimp-rice-v2.jpg',
      product: '/images/sakura-shrimp-rice-v2.jpg',
      thumbnail: '/images/sakura-shrimp-rice-v2.jpg',
    },
    name: {
      zh: '櫻花蝦米糕',
      en: 'Sakura Shrimp Sticky Rice',
      es: 'Arroz Glutinoso con Gambas Sakura',
    },
    tags: ['主餐', '糯米'],
    description: {
      zh: '台灣糯米蒸煮至粒粒晶瑩，拌入香氣撲鼻的櫻花蝦、乾香菇與炒過的紅蔥頭。鹹香入味，每一口都是海潮與山林的交融。',
      en: 'Taiwanese sticky rice steamed to a glossy finish, tossed with fragrant sakura shrimp, dried shiitake, and golden fried shallots. Savory and complex — a harmony of sea and forest.',
      es: 'Arroz glutinoso taiwanés cocido al vapor, mezclado con gambas sakura fragantes, shiitake seco y chalotas doradas. Sabroso y complejo — una armonía de mar y bosque.',
    },
    price: 12.99,
    allergens: ['甲殼類', '大豆'],
  },

  // ============ 珍珠奶茶系列 ============
  {
    id: 'brown-sugar-bubble-milk',
    category: CATEGORIES.BUBBLE_TEA,
    image: {
      hero: '/images/products/brown-sugar-v3.jpg',
      product: '/images/products/brown-sugar-v3.jpg',
      thumbnail: '/images/products/brown-sugar-v3.jpg',
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
    price: 6.45,
    allergens: ['乳製品'],
  },
  {
    id: 'bubble-tea',
    category: CATEGORIES.BUBBLE_TEA,
    image: {
      hero: '/images/products/bubble-tea-iced-v3.jpg',
      product: '/images/products/bubble-tea-iced-v3.jpg',
      thumbnail: '/images/products/bubble-tea-iced-v3.jpg',
    },
    name: {
      zh: '台灣珍珠奶茶',
      en: 'Taiwanese Bubble Tea',
      es: 'Té de Burbujas Taiwanés',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '台灣珍珠奶茶的經典原味，嚴選蜜香紅茶與鮮奶完美比例調配，搭配每日手工熬煮的 Q 彈珍珠。冷熱皆宜，冰飲清爽透亮、熱飲溫暖身心。茶香與奶香滑順融合，每一口都是最純粹的台灣味。',
      en: 'The classic original Taiwanese bubble tea — premium honey-scented black tea perfectly blended with fresh milk and daily-handcrafted chewy tapioca pearls. Available hot or iced: crisp and refreshing on ice, warm and soothing when hot. Every sip is the purest taste of Taiwan.',
      es: 'El clásico té de burbujas taiwanés — té negro con miel premium perfectamente mezclado con leche fresca y perlas artesanales diarias. Disponible frío o caliente, cada sorbo es el sabor más puro de Taiwán.',
    },
    price: 6.45,
    allergens: ['乳製品'],
  },
  {
    id: 'jasmine-green-bubble-tea',
    category: CATEGORIES.BUBBLE_TEA,
    image: {
      hero: '/images/products/jasmine-bubble-v3.jpg',
      product: '/images/products/jasmine-bubble-v3.jpg',
      thumbnail: '/images/products/jasmine-bubble-v3.jpg',
    },
    name: {
      zh: '茉莉珍珠綠奶茶',
      en: 'Jasmine Green Bubble Tea',
      es: 'Té Verde de Jazmín con Perlas',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '嚴選高山茉莉綠茶，花香清雅，茶韻悠長。搭配Q彈珍珠，清爽不膩，帶來優雅的品茗體驗。茉莉花的芬芳與綠茶的甘甜交織，珍珠的嚼勁增添層次感，是喜愛清新口感的最佳選擇。',
      en: 'Premium high-mountain jasmine green tea with elegant floral aroma and lingering tea notes. Paired with chewy tapioca pearls for a refreshing, non-greasy experience. The jasmine fragrance intertwines with green tea sweetness while pearls add delightful texture.',
      es: 'Té verde de jazmín premium de alta montaña con elegante aroma floral y notas de té persistentes. Combinado con perlas de tapioca masticables para una experiencia refrescante y sin grasa.',
    },
    price: 6.25,
    allergens: [],
  },
  {
    id: 'honey-oolong-bubble-tea',
    category: CATEGORIES.BUBBLE_TEA,
    image: {
      hero: '/images/products/honey-oolong-bubble-v3.jpg',
      product: '/images/products/honey-oolong-bubble-v3.jpg',
      thumbnail: '/images/products/honey-oolong-bubble-v3.jpg',
    },
    name: {
      zh: '蜜香烏龍珍珠奶茶',
      en: 'Honey Oolong Bubble Tea',
      es: 'Té Oolong de Miel con Perlas',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '台灣高山烏龍茶，經小綠葉蟬咬食後散發獨特蜜香。茶湯金黃透亮，蜜香馥郁，回甘綿長。搭配手工珍珠，層次豐富，是烏龍茶愛好者的極致享受。每一口都能感受到台灣茶藝的精髓。',
      en: 'Taiwan high-mountain oolong tea with unique honey fragrance from leafhopper bites. Golden amber tea with rich honey aroma and lingering sweet aftertaste. Paired with handcrafted pearls for complex layers, the ultimate treat for oolong tea lovers.',
      es: 'Té oolong de alta montaña de Taiwán con fragancia única de miel de picaduras de saltahojas. Té ámbar dorado con rico aroma a miel y regusto dulce persistente. Combinado con perlas artesanales.',
    },
    price: 6.25,
    allergens: [],
  },

  // ============ 奶茶系列 ============
  {
    id: 'taiwanese-milk-tea',
    category: CATEGORIES.MILK_TEA,
    image: {
      hero: '/images/products/taiwanese-milk-tea-v3.jpg',
      product: '/images/products/taiwanese-milk-tea-v3.jpg',
      thumbnail: '/images/products/taiwanese-milk-tea-v3.jpg',
    },
    name: {
      zh: '台灣蜜香奶茶',
      en: 'Taiwanese Milk Tea',
      es: 'Té con Leche Taiwanés',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '經典台式奶茶，選用錫蘭紅茶與香濃鮮奶，比例恰到好處。茶香與奶香完美平衡，不過甜不過膩，滑順爽口。這是最純粹的台灣味道，也是每個台灣人的童年回憶。',
      en: 'Classic Taiwanese milk tea with Ceylon black tea and rich fresh milk in perfect proportion. Tea aroma and milk fragrance beautifully balanced-not too sweet, not too rich, smooth and refreshing. The purest taste of Taiwan and a childhood memory for every Taiwanese.',
      es: 'Té con leche taiwanés clásico con té negro de Ceilán y leche fresca rica en proporción perfecta. Aroma a té y fragancia a leche bellamente equilibrados, no demasiado dulce, ni demasiado rico, suave y refrescante.',
    },
    price: 4.95,
    allergens: ['乳製品'],
  },
  {
    id: 'jasmine-green-milk-tea',
    category: CATEGORIES.MILK_TEA,
    image: {
      hero: '/images/products/jasmine-green-milk-tea-v3.jpg',
      product: '/images/products/jasmine-green-milk-tea-v3.jpg',
      thumbnail: '/images/products/jasmine-green-milk-tea-v3.jpg',
    },
    name: {
      zh: '茉莉綠奶茶',
      en: 'Jasmine Green Milk Tea',
      es: 'Té Verde de Jazmín con Leche',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '清新的茉莉綠茶遇上香醇鮮奶，碰撞出優雅的滋味。茉莉花香淡雅不膩，綠茶的甘甜與鮮奶的柔滑相輔相成。口感清爽，適合喜歡清新風味的您，每一口都是花香與茶香的交響樂章。',
      en: 'Refreshing jasmine green tea meets creamy fresh milk in an elegant flavor collision. Subtle jasmine fragrance complements the sweet green tea and smooth milk. Light and refreshing, perfect for those who prefer delicate flavors-a symphony of floral and tea notes.',
      es: 'El refrescante té verde de jazmín se encuentra con leche fresca cremosa en una elegante colisión de sabores. La sutil fragancia de jazmín complementa el té verde dulce y la leche suave.',
    },
    price: 5.25,
    allergens: ['乳製品'],
  },

  // ============ 綠茶系列 ============
  {
    id: 'honey-jasmine-green-tea',
    category: CATEGORIES.GREEN_TEA,
    image: {
      hero: '/images/products/honey-jasmine-v3.jpg',
      product: '/images/products/honey-jasmine-v3.jpg',
      thumbnail: '/images/products/honey-jasmine-v3.jpg',
    },
    name: {
      zh: '蜂蜜綠茶',
      en: 'Honey Jasmine Green Tea',
      es: 'Té Verde de Jazmín con Miel',
    },
    tags: ['冷飲', '熱飲'],
    description: {
      zh: '高山茉莉綠茶加入天然蜂蜜，甘甜清香。茉莉花的優雅與蜂蜜的醇厚完美結合，茶湯金黃透亮，入口清爽回甘。不添加人工糖分，保留茶葉原始風味，是追求健康與美味的最佳選擇。',
      en: "High-mountain jasmine green tea enhanced with natural honey for sweet freshness. Elegant jasmine meets rich honey in perfect harmony, creating golden amber tea that's refreshing with a sweet aftertaste. No artificial sweeteners-pure tea flavor for health-conscious tea lovers.",
      es: 'Té verde de jazmín de alta montaña realzado con miel natural para una frescura dulce. El elegante jazmín se encuentra con la rica miel en perfecta armonía, creando té ámbar dorado que es refrescante.',
    },
    price: 5.25,
    allergens: [],
  },

  // ============ 檸檬飲品 ============
  {
    id: 'winter-melon-lemonade',
    category: CATEGORIES.LEMONADE,
    image: {
      hero: '/images/products/winter-melon-lemonade-v3.jpg',
      product: '/images/products/winter-melon-lemonade-v3.jpg',
      thumbnail: '/images/products/winter-melon-lemonade-v3.jpg',
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
    price: 5.25,
    allergens: [],
  },

  // ============ 甜點 ============
  {
    id: 'mango-coconut-pannacotta',
    category: CATEGORIES.DESSERTS,
    image: {
      hero: '/images/products/mango-coconut-pannacotta-v3.jpg',
      product: '/images/products/mango-coconut-pannacotta-v3.jpg',
      thumbnail: '/images/products/mango-coconut-pannacotta-v3.jpg',
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
    price: 4.50,
    allergens: ['乳製品'],
  },
  {
    id: 'pineapple-cake',
    category: CATEGORIES.DESSERTS,
    image: {
      hero: '/images/products/pineapple-cake-v3.jpg',
      product: '/images/products/pineapple-cake-v3.jpg',
      thumbnail: '/images/products/pineapple-cake-v3.jpg',
    },
    name: {
      zh: '台灣鳳梨酥',
      en: 'Taiwan Pineapple Cake',
      es: 'Pastel de Piña Taiwanés',
    },
    tags: ['甜點', '手工烘焙'],
    description: {
      zh: '傳統台式糕點，每日新鮮手作。酥鬆奶香外皮包裹香甜土鳳梨內餡，入口層次豐富，甜而不膩。淡淡的奶油與鳳梨的清香相互輝映，搭配茶飲享用最對味。是下午茶的絕佳伴侶，也是伴手禮的首選。',
      en: 'Traditional Taiwanese pastry handcrafted fresh daily. Buttery shortcrust pastry encases sweet Taiwan pineapple filling—layered, balanced, not overly sweet. The delicate butter notes complement the bright pineapple fragrance, pairing beautifully with tea. An ideal afternoon companion or gift.',
      es: 'Pastelería tradicional taiwanesa elaborada a mano fresca diariamente. Masa mantecosa que envuelve un delicado relleno de piña taiwanesa, capas equilibradas, no demasiado dulce. Perfecto con té — un regalo ideal.',
    },
    price: 3.25,
    allergens: ['麩質', '乳製品'],
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
