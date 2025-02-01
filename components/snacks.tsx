export function Snacks() {
  const snacks = [
    {
      name: "鹽酥雞 Taiwanese Popcorn Chicken",
      description: "香脆可口的台式炸雞",
      price: "6.99",
      image: "/placeholder.svg",
    },
    {
      name: "蔥油餅 Scallion Pancake",
      description: "外酥內軟的傳統小吃",
      price: "4.99",
      image: "/placeholder.svg",
    },
    {
      name: "滷味拼盤 Braised Delights Platter",
      description: "多種滷味的美味組合",
      price: "8.99",
      image: "/placeholder.svg",
    },
    {
      name: "炸豆腐 Fried Tofu",
      description: "外酥內嫩的黃金豆腐",
      price: "5.99",
      image: "/placeholder.svg",
    },
    // 可以根据需要添加更多小吃
  ]

  return (
    <section id="snacks" className="mb-12 scroll-mt-20">
      <h2 className="text-3xl font-bold mb-6 px-4">Snacks 小點心</h2>
      <div className="px-4 md:px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {snacks.map((snack, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="relative h-40 w-full">
                <img
                  src={snack.image || "/placeholder.svg"}
                  alt={snack.name}
                  className="object-cover object-center w-full h-full"
                />
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2">{snack.name}</h3>
                <p className="text-sm text-gray-600 mb-2">{snack.description}</p>
                <p className="text-primary font-bold">${snack.price}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

