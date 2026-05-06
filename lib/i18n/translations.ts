export type Language = 'zh' | 'en' | 'es';

export const translations = {
  zh: {
    nav: {
      home: '首頁',
      menu: '菜單',
      products: '商品',
      about: '關於',
      contact: '聯絡',
      faq: '常見問題',
      getDirections: '前往地圖',
      orderOnline: '線上訂餐',
      orderPickup: '線上訂餐',
      delivery: '外送 (Uber Eats)',
      pickup: '來店自取',
    },
    hero: {
      welcome: '歡迎來到',
      brandName: '臺灣味',
      description: '位於紐約 Middletown 的家鄉味台式咖啡館 — 牛肉麵、滷肉飯、珍珠奶茶，以及來自家鄉的溫暖風味。',
      viewMenu: '查看菜單',
      orderOnline: '線上訂餐',
    },
    menu: {
      mainDishes: '主餐',
      desserts: '自製甜點',
      drinks: '飲品',
      items: {
        beefNoodle: {
          name: '牛肉麵',
          description: '香濃湯頭，嫩滑牛肉，Q彈麵條',
        },
        braisedPork: {
          name: '滷肉飯',
          description: '入味滷肉，搭配香Q白飯',
        },
        dessert: {
          name: '自製甜點',
          description: '每日新鮮手作甜點',
        },
        pineappleCake: {
          name: '台灣鳳梨酥',
          description: '每日現作',
        },
        bubbleTea: {
          name: '珍珠奶茶',
          description: '香醇奶茶，搭配Q彈珍珠',
        },
      },
      sections: {
        mainDishes: {
          title: '主餐',
          description: '精選台灣傳統美食',
        },
        drinks: {
          title: '飲品',
          description: '道地台式飲料',
        },
      },
      drinksList: {
        categories: {
          taiwaneseBlackTea: {
            title: "台灣紅茶",
            items: {
              bubbleTea: {
                name: "招牌珍珠奶茶",
                price: "6.45",
                options: "(熱/冷)"
              },
              milkTea: {
                name: "蜜香奶茶",
                price: "5.65",
                options: "(熱/冷)"
              }
            }
          },
          caffeineFree: {
            title: "無咖啡因",
            items: {
              brownSugarMilk: {
                name: "黑糖珍珠鮮奶",
                price: "6.45",
                options: "(熱/冷)"
              }
            }
          },
          jasmineGreenTea: {
            title: "茉莉綠茶",
            items: {
              honeyJasmine: {
                name: "茉莉蜂蜜綠茶",
                price: "4.85",
                options: "(冷飲)"
              },
              jasmineBubble: {
                name: "茉莉珍珠奶綠",
                price: "6.45",
                options: "(熱/冷)"
              }
            }
          },
          oolong: {
            title: "台灣烏龍茶",
            items: {
              honeyOolongBubble: {
                name: "蜂蜜烏龍珍珠奶茶",
                price: "6.65",
                options: "(熱/冷)"
              },
              honeyOolongMilk: {
                name: "蜂蜜烏龍奶茶",
                price: "5.85",
                options: "(熱/冷)"
              }
            }
          },
          matcha: {
            title: "京都一保堂抹茶",
            items: {
              matchaLatte: {
                name: "抹茶拿鐵",
                price: "5.95",
                options: "(熱/冷)"
              }
            }
          },
          potBrewed: {
            title: "現沖高山茶",
            items: {
              winterOolong: {
                name: "冬片",
                price: "5",
                options: "(熱飲)"
              },
              springOolong: {
                name: "春茶",
                price: "5",
                options: "(熱飲)"
              },
              no12Oolong: {
                name: "金萱",
                price: "5",
                options: "(熱飲)"
              },
              ironGoddess: {
                name: "鐵觀音",
                price: "6",
                options: "(熱飲)"
              },
              alishan: {
                name: "阿里山紅茶",
                price: "5",
                options: "(熱飲)"
              }
            }
          }
        }
      },
      mainDishesList: {
        categories: {
          desserts: {
            title: "自製甜點",
            items: {
              pineappleCake: {
                name: "台灣鳳梨酥",
                description: "每日現作",
                price: "3.25"
              }
            }
          },
          riceDishes: {
            title: "飯類",
            items: {
              braisedPork: {
                name: "滷肉飯",
                description: "入味滷肉，搭配香Q白飯",
                price: "10.99 / 12.99"
              },
              chickenRice: {
                name: "雞肉飯",
                description: "嫩煎雞腿肉，搭配特製醬汁",
                price: "10.99 / 12.99"
              }
            }
          },
          noodleSoups: {
            title: "麵類",
            items: {
              beefNoodle: {
                name: "牛肉麵",
                description: "香濃湯頭，嫩滑牛肉，Q彈麵條",
                price: "13.99 / 15.99"
              }
            }
          }
        }
      }
    },
    footer: {
      quickLinks: '快速連結',
      hours: '營業時間',
      contact: '聯絡我們',
      followUs: '關注我們',
      schedule: '週一、二、五、六',
      allRights: '版權所有',
    },
    about: {
      title: '關於我們',
      story1: 'TaiwanWay 把家鄉味帶到紐約 Middletown 10940 — 一家位於 Hudson Valley 的家鄉味台式咖啡館。從慢燉牛肉麵、經典滷肉飯，到手作珍珠奶茶與每日現烤鳳梨酥，每一道菜都承襲真正的台灣街頭飲食傳統，端上桌的是溫暖與鄰里的問候。',
      story2: '我們的故事始於一位母親 — 她陪伴孩子來到 Middletown 念書，愛上了這個小鎮，為了照顧家人也安撫鄉愁，開了這家店。我們每日精選 Adams 的新鮮食材，搭配來自台灣的香料與茶葉，堅持純天然、不過度加工。從香濃湯頭到 Q 彈珍珠，每一道都用心料理。',
      story3: '我們不只是一家咖啡館，更是 Hudson Valley 裡的一小片台灣 — 在這裡，您可以嚐到家鄉的味道、感受台灣的熱情好客、沉浸在獨特的飲食文化裡。',
      closing: '來 TaiwanWay — 一起分享美食，傳遞溫暖，品味台灣！',
    },
    contact: {
      title: '與我們聯繫',
      getInTouch: '聯絡我們',
      findUs: '來找我們',
      address: '地址',
      phone: '電話',
      email: '電子郵件',
      businessHours: '營業時間',
      schedule: '週一、二、五、六',
      time: '11:00 AM - 7:00 PM',
      closed: '週三、四、日公休',
      description: '歡迎蒞臨品嚐我們的美食，或透過電話、電子郵件與我們聯繫。我們期待為您服務！',
    },
  },
  en: {
    nav: {
      home: 'HOME',
      menu: 'MENUS',
      products: 'PRODUCTS',
      about: 'ABOUT',
      contact: 'CONTACT',
      faq: 'FAQ',
      getDirections: 'Get Directions',
      orderOnline: 'Order Online',
      orderPickup: 'Order For Pickup',
      delivery: 'Delivery (Uber Eats)',
      pickup: 'Pickup (Order Online)',
    },
    hero: {
      welcome: 'Welcome to',
      brandName: 'Taiwanway',
      description: 'A Taiwanese café in Middletown, NY — beef noodle soup, braised pork rice, bubble tea, and comforting flavors from home.',
      viewMenu: 'View Menu',
      orderOnline: 'Order Online',
    },
    menu: {
      mainDishes: 'Main Dishes',
      desserts: 'Homemade Desserts',
      drinks: 'Drinks',
      items: {
        beefNoodle: {
          name: 'Beef Noodle Soup',
          description: 'Rich broth, tender beef, springy noodles',
        },
        braisedPork: {
          name: 'Braised Pork Rice',
          description: 'Savory braised pork over steamed rice',
        },
        dessert: {
          name: 'Homemade Dessert',
          description: 'Fresh daily handmade desserts',
        },
        pineappleCake: {
          name: 'Taiwan Pineapple Cake',
          description: 'Freshly made daily',
        },
        bubbleTea: {
          name: 'Bubble Tea',
          description: 'Rich milk tea with chewy pearls',
        },
      },
      sections: {
        mainDishes: {
          title: 'Main Dishes',
          description: 'Selected Traditional Taiwanese Cuisine',
        },
        drinks: {
          title: 'Drinks',
          description: 'Authentic Taiwanese Beverages',
        },
      },
      drinksList: {
        categories: {
          taiwaneseBlackTea: {
            title: "Taiwanese Black Tea",
            items: {
              bubbleTea: {
                name: "Taiwanese Bubble Tea",
                price: "6.45",
                options: "(Hot/Cold)"
              },
              milkTea: {
                name: "Taiwanese Milk Tea",
                price: "5.65",
                options: "(Hot/Cold)"
              }
            }
          },
          caffeineFree: {
            title: "Caffeine-Free",
            items: {
              brownSugarMilk: {
                name: "Brown Sugar Bubble Milk",
                price: "6.45",
                options: "(Hot/Cold)"
              }
            }
          },
          jasmineGreenTea: {
            title: "Jasmine Green Tea",
            items: {
              honeyJasmine: {
                name: "Honey Jasmine Green Tea",
                price: "4.85",
                options: "(Cold)"
              },
              jasmineBubble: {
                name: "Jasmine Green Bubble Tea",
                price: "6.45",
                options: "(Hot/Cold)"
              }
            }
          },
          oolong: {
            title: "Taiwanese Oolong Tea",
            items: {
              honeyOolongBubble: {
                name: "Honey Oolong Bubble Tea",
                price: "6.65",
                options: "(Hot/Cold)"
              },
              honeyOolongMilk: {
                name: "Honey Oolong Milk Tea",
                price: "5.85",
                options: "(Hot/Cold)"
              }
            }
          },
          matcha: {
            title: "Ippodo Japanese Matcha",
            items: {
              matchaLatte: {
                name: "Matcha Latte",
                price: "5.95",
                options: "(Hot/Cold)"
              }
            }
          },
          potBrewed: {
            title: "Pot-Brewed Tea (Sugar-Free)",
            items: {
              winterOolong: {
                name: "Winter Leaves (Oolong)",
                price: "5",
                options: "(Hot)"
              },
              springOolong: {
                name: "Spring Leaves (Oolong)",
                price: "5",
                options: "(Hot)"
              },
              no12Oolong: {
                name: "No.12 (Oolong)",
                price: "5",
                options: "(Hot)"
              },
              ironGoddess: {
                name: "Iron Goddess (Oolong)",
                price: "6",
                options: "(Hot)"
              },
              alishan: {
                name: "A-Li Shan Black Tea",
                price: "5",
                options: "(Hot)"
              }
            }
          }
        }
      },
      mainDishesList: {
        categories: {
          desserts: {
            title: "Homemade Dessert",
            items: {
              pineappleCake: {
                name: "Taiwan Pineapple Cake",
                description: "Freshly made daily",
                price: "3.25"
              }
            }
          },
          riceDishes: {
            title: "Rice Dishes",
            items: {
              braisedPork: {
                name: "Braised Pork Rice",
                description: "Savory braised pork over steamed rice",
                price: "10.99 / 12.99"
              },
              chickenRice: {
                name: "Chicken Rice",
                description: "Pan-seared chicken thigh with special sauce",
                price: "10.99 / 12.99"
              }
            }
          },
          noodleSoups: {
            title: "Noodle Soups",
            items: {
              beefNoodle: {
                name: "Beef Noodle Soup",
                description: "Rich broth, tender beef, springy noodles",
                price: "13.99 / 15.99"
              }
            }
          }
        }
      }
    },
    footer: {
      quickLinks: 'Quick Links',
      hours: 'Hours',
      contact: 'Contact',
      followUs: 'Follow Us',
      schedule: 'Mon, Tue, Fri, Sat',
      allRights: 'All rights reserved',
    },
    about: {
      title: 'About Us',
      story1: 'TaiwanWay brings the flavors of Taiwan to Middletown, NY 10940 — a home-style Taiwanese café in the Hudson Valley. From slow-braised beef noodle soup and classic braised pork rice to handcrafted bubble tea and freshly baked pineapple cakes, every dish is rooted in real Taiwanese street-food traditions, served with warmth and a welcoming neighborhood feel.',
      story2: 'Our story begins with a mother who accompanied her child to Middletown for school, fell in love with the small town, and opened this café to care for her family and ease her homesickness. We carefully select fresh ingredients from Adams daily, paired with unique spices and teas brought from Taiwan, insisting on natural, minimally processed foods. From rich broth to chewy pearls, every dish is made by hand.',
      story3: 'We are more than just a café — we are a small piece of Taiwan in the Hudson Valley, where you can taste the flavors of home, experience Taiwan\'s warm hospitality, and immerse yourself in a unique culinary culture.',
      closing: 'Come to TaiwanWay — let\'s share great food, spread warmth, and savor Taiwan together!',
    },
    contact: {
      title: 'Contact Us',
      getInTouch: 'Get in Touch',
      findUs: 'Find Us',
      address: 'Address',
      phone: 'Phone',
      email: 'Email',
      businessHours: 'Business Hours',
      schedule: 'Monday, Tuesday, Friday, Saturday',
      time: '11:00 AM - 7:00 PM',
      closed: 'Closed on Wednesday, Thursday, and Sunday',
      description: 'Welcome to visit and taste our food, or contact us by phone or email. We look forward to serving you!',
    },
  },
  es: {
    nav: {
      home: 'INICIO',
      menu: 'MENÚ',
      products: 'PRODUCTOS',
      about: 'SOBRE',
      contact: 'CONTACTO',
      faq: 'FAQ',
      getDirections: 'Cómo Llegar',
      orderOnline: 'Ordenar en Línea',
      orderPickup: 'Ordenar para Recoger',
      delivery: 'Delivery (Uber Eats)',
      pickup: 'Recoger en Tienda',
    },
    hero: {
      welcome: 'Bienvenido a',
      brandName: 'Taiwanway',
      description: 'Un café taiwanés en Middletown, NY — sopa de fideos con res, arroz con cerdo guisado, té de burbujas y sabores reconfortantes de casa.',
      viewMenu: 'Ver Menú',
      orderOnline: 'Ordenar en Línea',
    },
    menu: {
      mainDishes: 'Platos Principales',
      desserts: 'Postres Caseros',
      drinks: 'Bebidas',
      items: {
        beefNoodle: {
          name: 'Sopa de Fideos con Res',
          description: 'Caldo rico, res tierna, fideos hechos a mano',
        },
        braisedPork: {
          name: 'Arroz con Cerdo Guisado',
          description: 'Cerdo guisado sabroso sobre arroz al vapor',
        },
        dessert: {
          name: 'Postres Caseros',
          description: 'Postres frescos hechos a mano diariamente',
        },
        pineappleCake: {
          name: 'Pastel de Piña Taiwanesa',
          description: 'Fresco hecho diariamente',
        },
        bubbleTea: {
          name: 'Té de Burbujas',
          description: 'Té con leche rico con perlas masticables',
        },
      },
      sections: {
        mainDishes: {
          title: 'Platos Principales',
          description: 'Selección de Cocina Tradicional Taiwanesa',
        },
        drinks: {
          title: 'Bebidas',
          description: 'Bebidas Auténticas Taiwanesas',
        },
      },
      drinksList: {
        categories: {
          taiwaneseBlackTea: {
            title: "Té Negro Taiwanés",
            items: {
              bubbleTea: {
                name: "Té de Burbujas Taiwanés",
                price: "6.45",
                options: "(Caliente/Frío)"
              },
              milkTea: {
                name: "Té con Leche Taiwanés",
                price: "5.65",
                options: "(Caliente/Frío)"
              }
            }
          },
          caffeineFree: {
            title: "Sin Cafeína",
            items: {
              brownSugarMilk: {
                name: "Leche con Burbujas y Azúcar Moreno",
                price: "6.45",
                options: "(Caliente/Frío)"
              }
            }
          },
          jasmineGreenTea: {
            title: "Té Verde al Jazmín",
            items: {
              honeyJasmine: {
                name: "Té Verde al Jazmín con Miel",
                price: "4.85",
                options: "(Frío)"
              },
              jasmineBubble: {
                name: "Té Verde al Jazmín con Burbujas",
                price: "6.45",
                options: "(Caliente/Frío)"
              }
            }
          },
          oolong: {
            title: "Té Oolong Taiwanés",
            items: {
              honeyOolongBubble: {
                name: "Té Oolong con Miel y Burbujas",
                price: "6.65",
                options: "(Caliente/Frío)"
              },
              honeyOolongMilk: {
                name: "Té Oolong con Miel y Leche",
                price: "5.85",
                options: "(Caliente/Frío)"
              }
            }
          },
          matcha: {
            title: "Matcha Japonés Ippodo",
            items: {
              matchaLatte: {
                name: "Matcha Latte",
                price: "5.95",
                options: "(Caliente/Frío)"
              }
            }
          },
          potBrewed: {
            title: "Té Preparado en Tetera (Sin Azúcar)",
            items: {
              winterOolong: {
                name: "Hojas de Invierno (Oolong)",
                price: "5",
                options: "(Caliente)"
              },
              springOolong: {
                name: "Hojas de Primavera (Oolong)",
                price: "5",
                options: "(Caliente)"
              },
              no12Oolong: {
                name: "No.12 (Oolong)",
                price: "5",
                options: "(Caliente)"
              },
              ironGoddess: {
                name: "Diosa de Hierro (Oolong)",
                price: "6",
                options: "(Caliente)"
              },
              alishan: {
                name: "Té Negro A-Li Shan",
                price: "5",
                options: "(Caliente)"
              }
            }
          }
        }
      },
      mainDishesList: {
        categories: {
          desserts: {
            title: "Postres Caseros",
            items: {
              pineappleCake: {
                name: "Pastel de Piña Taiwanesa",
                description: "Fresco hecho diariamente",
                price: "3.25"
              }
            }
          },
          riceDishes: {
            title: "Platos de Arroz",
            items: {
              braisedPork: {
                name: "Arroz con Cerdo Guisado",
                description: "Cerdo guisado sabroso sobre arroz al vapor",
                price: "10.99 / 12.99"
              },
              chickenRice: {
                name: "Arroz con Pollo",
                description: "Muslo de pollo salteado con salsa especial",
                price: "10.99 / 12.99"
              }
            }
          },
          noodleSoups: {
            title: "Sopas de Fideos",
            items: {
              beefNoodle: {
                name: "Sopa de Fideos con Res",
                description: "Caldo rico, res tierna, fideos hechos a mano",
                price: "13.99 / 15.99"
              }
            }
          }
        }
      }
    },
    footer: {
      quickLinks: 'Enlaces Rápidos',
      hours: 'Horario',
      contact: 'Contacto',
      followUs: 'Síguenos',
      schedule: 'Lun, Mar, Vie, Sáb',
      allRights: 'Todos los derechos reservados',
    },
    about: {
      title: 'Sobre Nosotros',
      story1: 'TaiwanWay trae los sabores de Taiwán a Middletown, NY 10940 — un café taiwanés casero en el valle del Hudson. Desde sopa de fideos con res a fuego lento y arroz con cerdo guisado clásico, hasta té de burbujas artesanal y pasteles de piña recién horneados, cada plato está enraizado en auténticas tradiciones de comida callejera taiwanesa, servido con calidez y un acogedor ambiente de barrio.',
      story2: 'Nuestra historia comienza con una madre que acompañó a su hijo a Middletown para estudiar, se enamoró del pueblo y abrió este café para cuidar de su familia y aliviar su nostalgia. Seleccionamos cuidadosamente ingredientes frescos de Adams diariamente, combinados con especias y tés traídos de Taiwán, insistiendo en alimentos naturales y mínimamente procesados. Desde el caldo intenso hasta las perlas masticables, cada plato está hecho a mano.',
      story3: 'Somos más que un café — somos un pequeño pedazo de Taiwán en el valle del Hudson, donde puedes probar los sabores de casa, experimentar la cálida hospitalidad de Taiwán y sumergirte en una cultura culinaria única.',
      closing: '¡Ven a TaiwanWay — compartamos buena comida, difundamos calidez y saboreemos Taiwán juntos!',
    },
    contact: {
      title: 'Contáctenos',
      getInTouch: 'Ponte en Contacto',
      findUs: 'Encuéntranos',
      address: 'Dirección',
      phone: 'Teléfono',
      email: 'Correo Electrónico',
      businessHours: 'Horario de Atención',
      schedule: 'Lunes, Martes, Viernes, Sábado',
      time: '11:00 AM - 7:00 PM',
      closed: 'Cerrado los Miércoles, Jueves y Domingos',
      description: '¡Bienvenido a visitar y probar nuestra comida, o contáctenos por teléfono o correo electrónico. ¡Esperamos poder servirle!',
    },
  },
} as const; 