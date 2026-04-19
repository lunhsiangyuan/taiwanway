import Image from "next/image"

export function Snacks() {
  const snacks: { name: string; description: string; price: string; image: string }[] = []

  return (
    <section id="snacks" className="mb-12 scroll-mt-20">
      <h2 className="text-3xl font-bold mb-6 px-4">Snacks 小點心</h2>
      <div className="px-4 md:px-6">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {snacks.map((snack, index) => (
            <div key={index} className="bg-white rounded-lg shadow-md overflow-hidden">
              <div className="relative h-40 w-full">
                <Image
                  src={snack.image || "/placeholder.svg"}
                  alt={snack.name}
                  fill
                  className="object-cover object-center"
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

