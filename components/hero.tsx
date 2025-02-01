import Image from "next/image"
import { Button } from "@/components/ui/button"

export function Hero() {
  return (
    <div>
      {/* Image Section */}
      <section className="relative h-[50vh] md:h-[70vh] w-full overflow-hidden">
        <Image
          src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/IMG_9053.JPG-4ohewz2SiN4NhrcIua5RHH3DvjCKYW.jpeg"
          alt="TaiwanWay storefront with beautiful pink dogwood blossoms"
          fill
          className="object-cover object-center"
          priority
        />
      </section>

      {/* Content Section */}
      <section className="py-16 bg-secondary/30">
        <div className="container mx-auto px-4">
          <div className="max-w-3xl mx-auto text-center">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
              歡迎來到
              <span className="text-primary"> 台灣味</span>
            </h1>
            <p className="text-xl text-muted-foreground mb-8">
              在紐約體驗道地的台灣美食。從我們的招牌牛肉麵到珍珠奶茶， 每一道菜都為您帶來台灣的溫暖與美味。
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Button size="lg" className="bg-primary hover:bg-primary/90 text-white px-8">
                查看菜單 View Menu
              </Button>
              <Button size="lg" variant="outline">
                線上訂餐 Order Online
              </Button>
            </div>
          </div>
        </div>
      </section>
    </div>
  )
}

