import Image from "next/image"

const highlights = [
  {
    name: "牛肉麵 Beef Noodle Soup",
    description: "香濃湯頭，嫩滑牛肉，手工麵條",
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2467.JPG-12cMHEqSdXbYmVHMe0F7GS10Fauj7H.jpeg",
  },
  {
    name: "滷肉飯 Braised Pork Rice",
    description: "入味滷肉，搭配香Q白飯",
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_2466.JPG-RIKgCt96QrGfXKlfWAgI8BjZN2thK1.jpeg",
  },
  {
    name: "自製甜點 Homemade Dessert",
    description: "每日新鮮手作甜點",
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_1167.JPG-2RGQnkcNjgJUfESKiEk8uNRWm7dqdR.jpeg",
  },
  {
    name: "珍珠奶茶 Bubble Tea",
    description: "香醇奶茶，搭配Q彈珍珠",
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9009.JPG-8Ke0jB3xYx1Ws4ynQLZCXnhyQcsYEl.jpeg",
  },
]

export function MenuHighlights() {
  return (
    <div>
      {highlights.map((item, index) => (
        <section key={item.name} className={`py-20 ${index % 2 === 0 ? "bg-secondary/30" : "bg-background"}`}>
          <div className="container px-0 lg:px-4">
            <div className={`flex flex-col ${index % 2 === 0 ? "lg:flex-row" : "lg:flex-row-reverse"} items-center`}>
              <div className="lg:w-2/3 relative h-[400px] lg:h-[600px] w-full">
                <Image
                  src={item.image || "/placeholder.svg"}
                  alt={item.name}
                  fill
                  className="object-cover"
                  priority={index === 0}
                />
              </div>
              <div className="lg:w-1/3 p-8 lg:p-12 space-y-4">
                <h2 className="text-3xl font-bold">{item.name}</h2>
                <p className="text-lg text-muted-foreground">{item.description}</p>
              </div>
            </div>
          </div>
        </section>
      ))}
    </div>
  )
}

