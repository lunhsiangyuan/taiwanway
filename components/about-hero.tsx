import Image from "next/image"

export function AboutHero() {
  return (
    <section className="relative h-[40vh] min-h-[320px] w-full bg-[#F5E6D3] px-4 md:px-6">
      <div className="absolute inset-0 w-full h-full rounded-lg">
        <Image
          src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_0329-4xKjbDPxXgMadO2d2D81rsDbqYYh6q.jpeg"
          alt="Taiwanway Logo"
          fill
          className="object-cover rounded-lg sm:object-center object-[15%_center]"
        />
      </div>
    </section>
  )
}

