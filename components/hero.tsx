import Image from "next/image"
import { Button } from "@/components/ui/button"

export function Hero() {
  return (
    <div className="relative bg-secondary">
      <div className="container flex flex-col lg:flex-row items-center gap-8 py-20">
        <div className="flex-1 text-center lg:text-left">
          <h1 className="text-4xl font-bold tracking-tighter sm:text-5xl md:text-6xl">
            歡迎來到
            <span className="text-primary"> 台灣之味</span>
          </h1>
          <p className="mx-auto lg:mx-0 mt-4 max-w-[700px] text-lg text-muted-foreground">
            在紐約體驗道地的台灣美食。從我們的招牌牛肉麵到珍珠奶茶， 每一道菜都為您帶來台灣的溫暖與美味。
          </p>
          <div className="mt-8 flex flex-wrap gap-4 justify-center lg:justify-start">
            <Button size="lg" className="bg-primary hover:bg-primary/90">
              查看菜單 View Menu
            </Button>
            <Button size="lg" variant="outline" className="border-primary text-primary hover:bg-primary/10">
              線上訂餐 Order Online
            </Button>
          </div>
        </div>
        <div className="flex-1 relative aspect-square w-full max-w-[500px]">
          <Image
            src="/placeholder.svg"
            alt="Taiwanese Cuisine"
            fill
            className="object-cover rounded-lg shadow-lg"
            priority
          />
        </div>
      </div>
    </div>
  )
}

