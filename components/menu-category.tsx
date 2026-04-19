import Image from "next/image"

interface MenuItem {
  name: string
  price: number
  image: string
}

interface MenuCategoryProps {
  id: string
  title: string
  items: MenuItem[]
}

export function MenuCategory({ id, title, items }: MenuCategoryProps) {
  return (
    <section id={id} className="mb-12 scroll-mt-20">
      <h2 className="text-3xl font-bold mb-6 px-4">{title}</h2>
      <div className="px-4 md:px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {items.map((item) => (
            <div key={item.name} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="relative h-64 w-full">
                <Image
                  src={item.image || "/placeholder.svg"}
                  alt={item.name}
                  fill
                  className="object-cover object-center"
                  sizes="(min-width: 1024px) 25vw, (min-width: 768px) 50vw, 100vw"
                />
              </div>
              <div className="p-4">
                <h3 className="font-semibold text-lg mb-2">{item.name}</h3>
                <p className="text-primary">${item.price.toFixed(2)}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </section>
  )
}

