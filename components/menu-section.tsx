import Image from "next/image"

interface MenuItem {
  name: string
  nameCh?: string
  price: number | string
  image?: string
  options?: string
}

interface MenuSectionProps {
  id: string
  title: string
  titleCh?: string
  items: MenuItem[]
  layout: "grid" | "list"
}

export function MenuSection({ id, title, titleCh, items, layout }: MenuSectionProps) {
  return (
    <section id={id} className="mb-12 scroll-mt-20">
      <h2 className="text-3xl font-bold mb-6 px-4">
        {title} {titleCh && <span className="text-primary">{titleCh}</span>}
      </h2>
      <div className="px-4 md:px-6">
        {layout === "grid" ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {items.map((item) => (
              <div key={item.name} className="bg-white rounded-lg shadow-md overflow-hidden">
                {item.image && (
                  <div className="relative h-64 w-full">
                    <Image
                      src={item.image || "/placeholder.svg"}
                      alt={item.name}
                      fill
                      className="object-cover object-center"
                      sizes="(min-width: 1024px) 25vw, (min-width: 768px) 50vw, 100vw"
                    />
                  </div>
                )}
                <div className="p-4">
                  <h3 className="font-semibold text-lg mb-2">{item.name}</h3>
                  {item.nameCh && <p className="text-md mb-2">{item.nameCh}</p>}
                  <p className="text-primary">${typeof item.price === "number" ? item.price.toFixed(2) : item.price}</p>
                  {item.options && <p className="text-sm text-muted-foreground">{item.options}</p>}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-6">
            {items.map((item) => (
              <div key={item.name} className="flex justify-between items-start gap-4">
                <div className="space-y-1">
                  <div className="text-xl font-medium">{item.name}</div>
                  {item.nameCh && <div className="text-lg">{item.nameCh}</div>}
                </div>
                <div className="text-right flex flex-col items-end">
                  <div className="text-xl">${item.price}</div>
                  {item.options && <div className="text-primary">{item.options}</div>}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </section>
  )
}

