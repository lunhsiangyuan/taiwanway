import Image from "next/image"

export function Desserts() {
  const desserts = [
    {
      name: "鳳梨酥 Pineapple Cake",
      description: "酥脆外皮，內餡飽滿的台灣名產",
      price: "3.99",
      image: "/placeholder.svg",
    },
    {
      name: "蛋糕捲 Cake Roll",
      description: "輕盈蓬鬆的美味蛋糕",
      price: "5.99",
      image: "/placeholder.svg",
    }
  ]

  return (
    <section id="desserts" className="mb-12 scroll-mt-20">
      <h2 className="text-3xl font-bold mb-6 px-4">Desserts 自製甜點</h2>
      <div className="px-4 md:px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {desserts.map((dessert, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="relative h-40 w-full">
                <Image
                  src={dessert.image || "/placeholder.svg"}
                  alt={dessert.name}
                  fill
                  className="object-cover object-center"
                />
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2">{dessert.name}</h3>
                <p className="text-sm text-gray-600 mb-2">{dessert.description}</p>
                <p className="text-primary font-bold">${dessert.price}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}
