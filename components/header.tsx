"use client"

import { useState } from "react"
import Link from "next/link"
import { MapPin, Menu, ChevronDown } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { usePathname } from "next/navigation"

const menuItems = [
  { name: "Full Menu 完整菜單", href: "/menu" },
  { name: "Snacks 小點心", href: "/menu#snacks" },
  { name: "Main Dishes 主餐", href: "/menu#main-dishes" },
  { name: "Drinks 飲品", href: "/menu#drinks" },
  { name: "Desserts 甜點", href: "/menu#desserts" },
]

export function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()

  const handleMenuClick = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    if (!href.includes("#")) return

    if (pathname === "/menu") {
      e.preventDefault()
      const id = href.split("#")[1]
      const element = document.getElementById(id)
      if (element) {
        element.scrollIntoView({ behavior: "smooth" })
      }
    }
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center">
        <Link href="/" className="font-bold text-2xl text-primary mr-6">
          Taiwanway
        </Link>

        <nav className="hidden md:flex gap-6 flex-1">
          <Link href="/" className="font-medium hover:text-primary transition-colors">
            HOME 首頁
          </Link>
          <DropdownMenu>
            <DropdownMenuTrigger className="flex items-center font-medium hover:text-primary transition-colors">
              MENUS 菜單 <ChevronDown className="ml-1 h-4 w-4" />
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              {menuItems.map((item) => (
                <DropdownMenuItem key={item.name}>
                  <Link href={item.href} onClick={(e) => handleMenuClick(e, item.href)}>
                    {item.name}
                  </Link>
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
          <Link href="/about" className="font-medium hover:text-primary transition-colors">
            ABOUT 關於
          </Link>
          <Link href="/contact" className="font-medium hover:text-primary transition-colors">
            CONTACT 聯絡
          </Link>
        </nav>

        <div className="flex items-center gap-4 ml-auto">
          <Button variant="outline" className="hidden md:flex" asChild>
            <Link
              href="https://www.google.com/maps/search/?api=1&query=Taiwanway+26+South+St+Middletown+NY"
              target="_blank"
              rel="noopener noreferrer"
            >
              <MapPin className="mr-2 h-4 w-4" />
              Get Directions
            </Link>
          </Button>
          <Button>Order For Pickup</Button>

          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button variant="outline" size="icon" className="md:hidden">
                <Menu className="h-6 w-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right">
              <nav className="flex flex-col gap-4">
                <Link
                  href="/"
                  className="font-medium hover:text-primary transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  HOME 首頁
                </Link>
                {menuItems.map((item) => (
                  <Link
                    key={item.name}
                    href={item.href}
                    className="font-medium hover:text-primary transition-colors pl-4"
                    onClick={(e) => {
                      handleMenuClick(e, item.href)
                      setIsOpen(false)
                    }}
                  >
                    {item.name}
                  </Link>
                ))}
                <Link
                  href="/about"
                  className="font-medium hover:text-primary transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  ABOUT 關於
                </Link>
                <Link
                  href="/contact"
                  className="font-medium hover:text-primary transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  CONTACT 聯絡
                </Link>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}

