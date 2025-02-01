import Image from "next/image"

export function AboutHero() {
  return (
    <section className="relative h-[50vh] min-h-[300px] w-full">
      <div className="absolute inset-0 w-full h-full">
        <Image
          src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9053.JPG-4ohewz2SiN4NhrcIua5RHH3DvjCKYW.jpeg"
          alt="TaiwanWay storefront with beautiful pink dogwood blossoms"
          fill
          className="object-cover"
          priority
        />
      </div>
      <div className="absolute inset-0 bg-black/30" />
    </section>
  )
}

