export function DrinksList() {
  const drinks = [
    {
      category: "Taiwanese Old-Fashioned Tea",
      categoryCh: "懷舊古早味",
      items: [
        {
          name: "Classic Black Tea",
          nameCh: "冰紅茶",
          price: "2.99",
          options: "(C)",
        },
        {
          name: "Classic Milk Tea (Whole Milk)",
          nameCh: "鮮奶茶",
          price: "4.35",
          options: "(C)",
        },
      ],
    },
    {
      category: "Taiwanese Black Tea",
      categoryCh: "台灣紅茶",
      items: [
        {
          name: "Nature Honey-flavored Black Tea",
          nameCh: "台灣蜜香紅茶",
          price: "5.95",
          options: "(H/C)",
        },
        {
          name: "Taiwanese Bubble Tea",
          nameCh: "招牌珍珠奶茶",
          price: "5.95",
          options: "(H/C)",
        },
        {
          name: "Taiwanese Milk Tea",
          nameCh: "蜜香奶茶",
          price: "4.95",
          options: "(H/C)",
        },
      ],
    },
    {
      category: "Caffeine-Free",
      categoryCh: "無咖啡因",
      items: [
        {
          name: "Brown Sugar Bubble Milk",
          nameCh: "黑糖珍珠鮮奶",
          price: "6.45",
          options: "(H/C)",
        },
      ],
    },
    {
      category: "Jasmine Green Tea",
      categoryCh: "茉莉綠茶",
      items: [
        {
          name: "Honey Jasmine Green Tea",
          nameCh: "茉莉蜂蜜綠茶",
          price: "5.25",
          options: "(C)",
        },
        {
          name: "Jasmine Green Bubble Tea",
          nameCh: "茉莉珍珠奶綠",
          price: "6.25",
          options: "(H/C)",
        },
      ],
    },
    {
      category: "Taiwanese Oolong Tea",
      categoryCh: "台灣烏龍茶",
      items: [
        {
          name: "Honey Oolong Bubble Tea",
          nameCh: "蜂蜜烏龍珍珠奶茶",
          price: "6.25",
          options: "(H/C)",
        },
        {
          name: "Honey Oolong Milk Tea",
          nameCh: "蜂蜜烏龍奶茶",
          price: "5.25",
          options: "(H/C)",
        },
      ],
    },
    {
      category: "Ippodo Japanese Matcha",
      categoryCh: "京都一保堂抹茶",
      items: [
        {
          name: "Matcha Latte",
          nameCh: "抹茶拿鐵",
          price: "5.65",
          options: "(H/C)",
        },
        {
          name: "Bubble Matcha Latte",
          nameCh: "珍珠抹茶拿鐵",
          price: "6.85",
          options: "(H/C)",
        },
      ],
    },
    {
      category: "Pot-Brewed Tea (Sugar-Free)",
      categoryCh: "現沖高山茶",
      items: [
        {
          name: "Winter Leaves (Oolong)",
          price: "5",
          nameCh: "冬片",
          options: "(H)",
        },
        {
          name: "Spring Leaves (Oolong)",
          nameCh: "春茶",
          price: "5",
          options: "(H)",
        },
        {
          name: "No.12 (Oolong)",
          nameCh: "金萱",
          price: "5",
          options: "(H)",
        },
        {
          name: "Iron Goddess (Oolong)",
          nameCh: "鐵觀音",
          price: "6",
          options: "(H)",
        },
        {
          name: "A-Li Shan Black Tea",
          nameCh: "阿里山紅茶",
          price: "5",
          options: "(H)",
        },
      ],
    },
  ]

  return (
    <section id="drinks" className="mb-12 scroll-mt-20">
      <h2 className="text-3xl font-bold mb-6 px-4">Drinks 飲品</h2>
      <div className="px-4 md:px-6">
        <div className="space-y-12">
          {drinks.map((category, index) => (
            <div key={index} className="space-y-6">
              <div className="space-y-1">
                <h3 className="text-2xl text-primary font-medium">
                  {category.category} {category.categoryCh}
                </h3>
                <div className="h-0.5 bg-primary w-full"></div>
              </div>
              <div className="space-y-4">
                {category.items.map((item, itemIndex) => (
                  <div key={itemIndex} className="flex justify-between items-start gap-4">
                    <div className="space-y-1">
                      <div className="text-xl font-medium">{item.name}</div>
                      {item.nameCh && <div className="text-lg">{item.nameCh}</div>}
                    </div>
                    <div className="text-right flex flex-col items-end">
                      <div className="text-xl">${item.price}</div>
                      <div className="text-primary">{item.options}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

