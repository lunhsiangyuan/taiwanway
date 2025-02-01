export function MainDishes() {
  const mainDishes = [
    {
      name: "滷肉飯 Braised Pork Rice",
      description: "入味滷肉，搭配香Q白飯",
      price: "8.99",
      image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2466.JPG-RIKgCt96QrGfXKlfWAgI8BjZN2thK1.jpeg",
    },
    {
      name: "牛肉麵 Beef Noodle Soup",
      description: "香濃湯頭，嫩滑牛肉，手工麵條",
      price: "12.99",
      image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2467.JPG-12cMHEqSdXbYmVHMe0F7GS10Fauj7H.jpeg",
    },
    // 可以根据需要添加更多主菜
  ]

  return (
    <section id="main-dishes" className="mb-12 scroll-mt-20">
      <h2 className="text-3xl font-bold mb-6 px-4">Main Dishes 主餐</h2>
      <div className="px-4 md:px-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {mainDishes.map((dish, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="relative h-48 w-full">
                <img
                  src={dish.image || "/placeholder.svg"}
                  alt={dish.name}
                  className="object-cover object-center w-full h-full"
                />
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2">{dish.name}</h3>
                <p className="text-sm text-gray-600 mb-2">{dish.description}</p>
                <p className="text-primary font-bold">${dish.price}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

