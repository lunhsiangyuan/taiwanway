import Image from "next/image"

export function ContactHero() {
  return (
    <section className="relative h-[40vh] min-h-[320px] w-full bg-[#F5E6D3]">
      <div className="absolute inset-0 w-full h-full flex items-center justify-center">
        <Image
          src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_0329-4xKjbDPxXgMadO2d2D81rsDbqYYh6q.jpeg"
          alt="Taiwanway Logo"
          fill
          className="object-contain"
        />
      </div>
    </section>
  )
}

