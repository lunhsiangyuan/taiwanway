export type Language = 'zh' | 'en' | 'es';

export const translations = {
  zh: {
    nav: {
      home: '首頁',
      menu: '菜單',
      about: '關於',
      contact: '聯絡',
      getDirections: '前往地圖',
      orderPickup: '線上訂餐',
    },
    hero: {
      welcome: '歡迎來到',
      brandName: '台灣味',
      description: '在紐約體驗道地的台灣美食。從我們的招牌牛肉麵到珍珠奶茶， 每一道菜都為您帶來台灣的溫暖與美味。',
      viewMenu: '查看菜單',
      orderOnline: '線上訂餐',
    },
    menu: {
      mainDishes: '主餐',
      drinks: '飲品',
      items: {
        beefNoodle: {
          name: '牛肉麵',
          description: '香濃湯頭，嫩滑牛肉，手工麵條',
        },
        braisedPork: {
          name: '滷肉飯',
          description: '入味滷肉，搭配香Q白飯',
        },
        dessert: {
          name: '自製甜點',
          description: '每日新鮮手作甜點',
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
          oldFashioned: {
            title: "懷舊古早味",
            items: {
              blackTea: {
                name: "冰紅茶",
                price: "2.99",
                options: "(冷飲)"
              },
              milkTea: {
                name: "鮮奶茶",
                price: "4.35",
                options: "(冷飲)"
              }
            }
          },
          taiwaneseBlackTea: {
            title: "台灣紅茶",
            items: {
              honeyBlackTea: {
                name: "台灣蜜香紅茶",
                price: "5.95",
                options: "(熱/冷)"
              },
              bubbleTea: {
                name: "招牌珍珠奶茶",
                price: "5.95",
                options: "(熱/冷)"
              },
              milkTea: {
                name: "蜜香奶茶",
                price: "4.95",
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
                price: "5.25",
                options: "(冷飲)"
              },
              jasmineBubble: {
                name: "茉莉珍珠奶綠",
                price: "6.25",
                options: "(熱/冷)"
              }
            }
          },
          oolong: {
            title: "台灣烏龍茶",
            items: {
              honeyOolongBubble: {
                name: "蜂蜜烏龍珍珠奶茶",
                price: "6.25",
                options: "(熱/冷)"
              },
              honeyOolongMilk: {
                name: "蜂蜜烏龍奶茶",
                price: "5.25",
                options: "(熱/冷)"
              }
            }
          },
          matcha: {
            title: "京都一保堂抹茶",
            items: {
              matchaLatte: {
                name: "抹茶拿鐵",
                price: "5.65",
                options: "(熱/冷)"
              },
              bubbleMatchaLatte: {
                name: "珍珠抹茶拿鐵",
                price: "6.85",
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
          riceDishes: {
            title: "飯類",
            items: {
              braisedPork: {
                name: "滷肉飯",
                description: "入味滷肉，搭配香Q白飯",
                price: "8.99"
              },
              chickenRice: {
                name: "雞肉飯",
                description: "嫩煎雞腿肉，搭配特製醬汁",
                price: "9.99"
              }
            }
          },
          noodleSoups: {
            title: "麵類",
            items: {
              beefNoodle: {
                name: "牛肉麵",
                description: "香濃湯頭，嫩滑牛肉，手工麵條",
                price: "12.99"
              },
              wontonNoodle: {
                name: "餛飩麵",
                description: "手工餛飩，清甜湯頭",
                price: "10.99"
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
      story1: '歡迎來到 TaiwanWay，這裡是紐約地道台灣美食的家園。我們的故事始於一位母親，她陪伴小孩來到Middletown念書，愛上了這裡，為了照顧小孩並解鄉愁，開了這家店。',
      story2: '在 TaiwanWay，每道菜都承載著我們對台灣的思念與對食材的敬重。我們每日精選Adams的新鮮食材，搭配來自台灣的獨特香料與茶葉，堅持純天然、不過度加工。從濃郁的牛肉麵到Q彈的珍珠奶茶，我們用心烹調每一道料理，只為帶給您最道地的台灣滋味。',
      story3: '我們不僅僅是一家餐廳，更是一個文化交流的平台。在這裡，您可以品嚐到家鄉的味道，感受台灣的熱情好客，體驗獨特的飲食文化。',
      closing: '來 TaiwanWay，讓我們一起分享美食，傳遞溫暖，品味台灣！',
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
      about: 'ABOUT',
      contact: 'CONTACT',
      getDirections: 'Get Directions',
      orderPickup: 'Order For Pickup',
    },
    hero: {
      welcome: 'Welcome to',
      brandName: 'Taiwanway',
      description: 'Experience authentic Taiwanese cuisine in New York. From our signature beef noodle soup to bubble tea, each dish brings you the warmth and flavor of Taiwan.',
      viewMenu: 'View Menu',
      orderOnline: 'Order Online',
    },
    menu: {
      mainDishes: 'Main Dishes',
      drinks: 'Drinks',
      items: {
        beefNoodle: {
          name: 'Beef Noodle Soup',
          description: 'Rich broth, tender beef, handmade noodles',
        },
        braisedPork: {
          name: 'Braised Pork Rice',
          description: 'Savory braised pork over steamed rice',
        },
        dessert: {
          name: 'Homemade Dessert',
          description: 'Fresh daily handmade desserts',
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
          oldFashioned: {
            title: "Taiwanese Old-Fashioned Tea",
            items: {
              blackTea: {
                name: "Classic Black Tea",
                price: "2.99",
                options: "(Cold)"
              },
              milkTea: {
                name: "Classic Milk Tea (Whole Milk)",
                price: "4.35",
                options: "(Cold)"
              }
            }
          },
          taiwaneseBlackTea: {
            title: "Taiwanese Black Tea",
            items: {
              honeyBlackTea: {
                name: "Nature Honey-flavored Black Tea",
                price: "5.95",
                options: "(Hot/Cold)"
              },
              bubbleTea: {
                name: "Taiwanese Bubble Tea",
                price: "5.95",
                options: "(Hot/Cold)"
              },
              milkTea: {
                name: "Taiwanese Milk Tea",
                price: "4.95",
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
                price: "5.25",
                options: "(Cold)"
              },
              jasmineBubble: {
                name: "Jasmine Green Bubble Tea",
                price: "6.25",
                options: "(Hot/Cold)"
              }
            }
          },
          oolong: {
            title: "Taiwanese Oolong Tea",
            items: {
              honeyOolongBubble: {
                name: "Honey Oolong Bubble Tea",
                price: "6.25",
                options: "(Hot/Cold)"
              },
              honeyOolongMilk: {
                name: "Honey Oolong Milk Tea",
                price: "5.25",
                options: "(Hot/Cold)"
              }
            }
          },
          matcha: {
            title: "Ippodo Japanese Matcha",
            items: {
              matchaLatte: {
                name: "Matcha Latte",
                price: "5.65",
                options: "(Hot/Cold)"
              },
              bubbleMatchaLatte: {
                name: "Bubble Matcha Latte",
                price: "6.85",
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
          riceDishes: {
            title: "Rice Dishes",
            items: {
              braisedPork: {
                name: "Braised Pork Rice",
                description: "Savory braised pork over steamed rice",
                price: "8.99"
              },
              chickenRice: {
                name: "Chicken Rice",
                description: "Pan-seared chicken thigh with special sauce",
                price: "9.99"
              }
            }
          },
          noodleSoups: {
            title: "Noodle Soups",
            items: {
              beefNoodle: {
                name: "Beef Noodle Soup",
                description: "Rich broth, tender beef, handmade noodles",
                price: "12.99"
              },
              wontonNoodle: {
                name: "Wonton Noodle Soup",
                description: "Handmade wontons in clear broth",
                price: "10.99"
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
      story1: 'Welcome to TaiwanWay, a home for authentic Taiwanese cuisine in New York. Our story begins with a mother who accompanied her child to Middletown for school, fell in love with the place, and opened this restaurant to care for her child and ease her homesickness.',
      story2: 'At TaiwanWay, each dish is a reflection of our longing for Taiwan and respect for ingredients. We carefully select fresh ingredients from Adams daily, paired with unique spices and teas from Taiwan, insisting on natural, minimally processed foods. From our rich beef noodle soup to the chewy bubble tea, we put our heart into every dish to bring you the most authentic taste of Taiwan.',
      story3: 'We are more than just a restaurant; we are a platform for cultural exchange. Here, you can taste the flavors of home, experience Taiwan\'s warm hospitality, and immerse yourself in a unique culinary culture.',
      closing: 'Come to TaiwanWay, let\'s share great food, spread warmth, and savor Taiwan together!',
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
      about: 'SOBRE',
      contact: 'CONTACTO',
      getDirections: 'Cómo Llegar',
      orderPickup: 'Ordenar para Recoger',
    },
    hero: {
      welcome: 'Bienvenido a',
      brandName: 'Taiwanway',
      description: 'Experimenta la auténtica cocina taiwanesa en Nueva York. Desde nuestra sopa de fideos con res hasta el té de burbujas, cada plato te trae el calor y el sabor de Taiwán.',
      viewMenu: 'Ver Menú',
      orderOnline: 'Ordenar en Línea',
    },
    menu: {
      mainDishes: 'Platos Principales',
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
          oldFashioned: {
            title: "Té Tradicional Taiwanés",
            items: {
              blackTea: {
                name: "Té Negro Clásico",
                price: "2.99",
                options: "(Frío)"
              },
              milkTea: {
                name: "Té con Leche Clásico (Leche Entera)",
                price: "4.35",
                options: "(Frío)"
              }
            }
          },
          taiwaneseBlackTea: {
            title: "Té Negro Taiwanés",
            items: {
              honeyBlackTea: {
                name: "Té Negro con Miel Natural",
                price: "5.95",
                options: "(Caliente/Frío)"
              },
              bubbleTea: {
                name: "Té de Burbujas Taiwanés",
                price: "5.95",
                options: "(Caliente/Frío)"
              },
              milkTea: {
                name: "Té con Leche Taiwanés",
                price: "4.95",
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
                price: "5.25",
                options: "(Frío)"
              },
              jasmineBubble: {
                name: "Té Verde al Jazmín con Burbujas",
                price: "6.25",
                options: "(Caliente/Frío)"
              }
            }
          },
          oolong: {
            title: "Té Oolong Taiwanés",
            items: {
              honeyOolongBubble: {
                name: "Té Oolong con Miel y Burbujas",
                price: "6.25",
                options: "(Caliente/Frío)"
              },
              honeyOolongMilk: {
                name: "Té Oolong con Miel y Leche",
                price: "5.25",
                options: "(Caliente/Frío)"
              }
            }
          },
          matcha: {
            title: "Matcha Japonés Ippodo",
            items: {
              matchaLatte: {
                name: "Matcha Latte",
                price: "5.65",
                options: "(Caliente/Frío)"
              },
              bubbleMatchaLatte: {
                name: "Matcha Latte con Burbujas",
                price: "6.85",
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
          riceDishes: {
            title: "Platos de Arroz",
            items: {
              braisedPork: {
                name: "Arroz con Cerdo Guisado",
                description: "Cerdo guisado sabroso sobre arroz al vapor",
                price: "8.99"
              },
              chickenRice: {
                name: "Arroz con Pollo",
                description: "Muslo de pollo salteado con salsa especial",
                price: "9.99"
              }
            }
          },
          noodleSoups: {
            title: "Sopas de Fideos",
            items: {
              beefNoodle: {
                name: "Sopa de Fideos con Res",
                description: "Caldo rico, res tierna, fideos hechos a mano",
                price: "12.99"
              },
              wontonNoodle: {
                name: "Sopa de Fideos con Wonton",
                description: "Wontons hechos a mano en caldo claro",
                price: "10.99"
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
      story1: 'Bienvenido a TaiwanWay, un hogar para la auténtica cocina taiwanesa en Nueva York. Nuestra historia comienza con una madre que acompañó a su hijo a Middletown para estudiar, se enamoró del lugar y abrió este restaurante para cuidar de su hijo y aliviar su nostalgia.',
      story2: 'En TaiwanWay, cada plato es un reflejo de nuestra añoranza por Taiwán y respeto por los ingredientes. Seleccionamos cuidadosamente ingredientes frescos de Adams diariamente, combinados con especias y tés únicos de Taiwán, insistiendo en alimentos naturales y mínimamente procesados. Desde nuestra rica sopa de fideos con res hasta el té de burbujas masticable, ponemos nuestro corazón en cada plato para traerte el sabor más auténtico de Taiwán.',
      story3: 'Somos más que un restaurante; somos una plataforma para el intercambio cultural. Aquí puedes probar los sabores de casa, experimentar la cálida hospitalidad de Taiwán y sumergirte en una cultura culinaria única.',
      closing: '¡Ven a TaiwanWay, compartamos buena comida, difundamos calidez y saboreemos Taiwán juntos!',
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