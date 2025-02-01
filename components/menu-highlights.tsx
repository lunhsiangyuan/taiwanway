"use client"

import { useState, useEffect } from "react"
import Image from "next/image"
import { Card, CardContent } from "@/components/ui/card"

const highlights = [
  {
    name: "牛肉麵 Beef Noodle Soup",
    description: "香濃湯頭，嫩滑牛肉，手工麵條",
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-c1Jpe5PyzOQfbFnAYZNfgGtCHw6yZ5.png",
  },
  {
    name: "滷肉飯 Braised Pork Rice",
    description: "入味滷肉，搭配香Q白飯",
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-iZMQRdfWbj3r2TCguRsanZuXD9O8Dt.png",
  },
  {
    name: "鳳梨酥 Pineapple Cake",
    description: "酥脆外皮，內餡飽滿鳳梨",
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-c1Jpe5PyzOQfbFnAYZNfgGtCHw6yZ5.png",
  },
  {
    name: "珍珠奶茶 Bubble Tea",
    description: "香醇奶茶，搭配Q彈珍珠",
    image: "https://hebbkx1anhila5yf.public.blob.vercel-storage.com/image-iZMQRdfWbj3r2TCguRsanZuXD9O8Dt.png",
  },
]

export function MenuHighlights() {
  const [isMobile, setIsMobile] = useState(false)

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768) // 設置移動設備的斷點
    }

    handleResize() // 初始化
    window.addEventListener("resize", handleResize)

    return () => {
      window.removeEventListener("resize", handleResize)
    }
  }, [])

  return (
    <section className="py-20 bg-secondary/50">
      <div className="container">
        <h2 className="text-3xl font-bold text-center mb-12">我們的招牌 Our Specialties</h2>
        <div className="grid md:grid-cols-2 gap-6">
          <div className="space-y-6">
            {highlights.slice(0, 2).map((item) => (
              <Card key={item.name} className="border-primary/20 hover:border-primary/40 transition-colors">
                <CardContent className="p-4">
                  <div className="flex items-center">
                    <div className={`relative ${isMobile ? "w-24 h-24" : "w-32 h-32"} mr-4`}>
                      <Image
                        src={item.image || "/placeholder.svg"}
                        alt={item.name}
                        fill
                        className="object-cover rounded-md"
                      />
                    </div>
                    <div>
                      <h3 className="font-semibold mb-2">{item.name}</h3>
                      <p className="text-sm text-muted-foreground">{item.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
          <div className="space-y-6">
            {highlights.slice(2, 4).map((item) => (
              <Card key={item.name} className="border-primary/20 hover:border-primary/40 transition-colors">
                <CardContent className="p-4">
                  <div className="flex items-center">
                    <div className={`relative ${isMobile ? "w-24 h-24" : "w-32 h-32"} mr-4`}>
                      <Image
                        src={item.image || "/placeholder.svg"}
                        alt={item.name}
                        fill
                        className="object-cover rounded-md"
                      />
                    </div>
                    <div>
                      <h3 className="font-semibold mb-2">{item.name}</h3>
                      <p className="text-sm text-muted-foreground">{item.description}</p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      </div>
    </section>
  )
}

