"use client"

import Link from "next/link"
import { MapPin, Menu } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"

export function Header() {
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between">
        <Link href="/" className="font-bold text-2xl text-primary">
          Taiwan Way
        </Link>

        <nav className="hidden md:flex gap-6">
          <Link href="/" className="font-medium hover:text-primary transition-colors">
            首頁 Home
          </Link>
          <Link href="/menu" className="font-medium hover:text-primary transition-colors">
            菜單 Menu
          </Link>
          <Link href="/about" className="font-medium hover:text-primary transition-colors">
            關於 About
          </Link>
          <Link href="/contact" className="font-medium hover:text-primary transition-colors">
            聯絡 Contact
          </Link>
        </nav>

        <div className="flex items-center gap-4">
          <Button variant="outline" className="hidden md:flex hover:bg-primary/10">
            <MapPin className="mr-2 h-4 w-4" />
            Get Directions
          </Button>
          <Button className="bg-primary hover:bg-primary/90">Order Online</Button>

          <Sheet>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="md:hidden">
                <Menu className="h-6 w-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right">
              <nav className="flex flex-col gap-4">
                <Link href="/" className="font-medium hover:text-primary transition-colors">
                  首頁 Home
                </Link>
                <Link href="/menu" className="font-medium hover:text-primary transition-colors">
                  菜單 Menu
                </Link>
                <Link href="/about" className="font-medium hover:text-primary transition-colors">
                  關於 About
                </Link>
                <Link href="/contact" className="font-medium hover:text-primary transition-colors">
                  聯絡 Contact
                </Link>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}

