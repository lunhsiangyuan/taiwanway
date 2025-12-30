"use client"

import { useState } from "react"
import Link from "next/link"
import { MapPin, Menu, ChevronDown, Globe } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Sheet, SheetContent, SheetTrigger } from "@/components/ui/sheet"
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from "@/components/ui/dropdown-menu"
import { usePathname, useRouter } from "next/navigation"
import Image from "next/image"
import { cn } from "@/lib/utils"
import { useLanguage } from "@/lib/i18n/language-context"

const menuItems = [
  { key: 'mainDishes', href: '/menu#main-dishes' },
  { key: 'desserts', href: '/menu#desserts' },
  { key: 'drinks', href: '/menu#drinks' },
] as const

const languages = [
  { code: 'zh', label: '中文', name: '中文' },
  { code: 'en', label: 'English', name: 'English' },
  { code: 'es', label: 'Español', name: 'Español' },
] as const

export function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const pathname = usePathname()
  const [menuOpen, setMenuOpen] = useState(false)
  const { language, setLanguage, t } = useLanguage()
  const router = useRouter()

  const handleMenuClick = (e: React.MouseEvent<HTMLAnchorElement>, href: string) => {
    e.preventDefault()

    const id = href.split("#")[1]
    if (!id) return

    if (pathname !== "/menu") {
      router.push(`/menu#${id}`)
      return
    }

    const element = document.getElementById(id)
    if (element) {
      element.scrollIntoView({ behavior: "smooth" })
    }
  }

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="w-full px-4 md:px-6 lg:px-8 max-w-screen-2xl mx-auto flex h-16 items-center">
        <Link href="/" className="font-bold text-2xl text-primary mr-2 flex items-center gap-2">
          Taiwanway
          <div className="hidden md:flex h-12 w-auto aspect-[2/1] relative">
            <Image
              src="https://hebbkx1anhila5yf.public.blob.vercel-storage.com/LOGO-A(%E5%8E%BB%E8%83%8C)-01-md2UWlZPf63lgtuEOcu8FhyaJJySOU.png"
              alt="Taiwanway Logo"
              fill
              className="object-contain"
              priority
            />
          </div>
        </Link>

        <nav className="hidden md:flex gap-6 flex-1">
          <Link href="/" className="font-medium hover:text-primary transition-colors">
            {t('nav.home')}
          </Link>
          <DropdownMenu>
            <DropdownMenuTrigger className="font-medium hover:text-primary transition-colors flex items-center">
              <Link href="/menu">{t('nav.menu')}</Link> <ChevronDown className="ml-1 h-4 w-4" />
            </DropdownMenuTrigger>
            <DropdownMenuContent>
              {menuItems.map((item) => (
                <DropdownMenuItem key={item.key} asChild>
                  <Link href={item.href} onClick={(e) => handleMenuClick(e, item.href)} className="w-full">
                    {t(`menu.${item.key}`)}
                  </Link>
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>
          <Link href="/about" className="font-medium hover:text-primary transition-colors">
            {t('nav.about')}
          </Link>
          <Link href="/contact" className="font-medium hover:text-primary transition-colors">
            {t('nav.contact')}
          </Link>
        </nav>

        <div className="flex items-center gap-4 ml-auto">
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button variant="ghost" size="icon" className="flex items-center gap-2 min-w-[40px] sm:min-w-[100px] justify-center">
                <Globe className="h-5 w-5" />
                <span className="hidden sm:inline-block text-sm font-medium">
                  {languages.find(l => l.code === language)?.name || '中文'}
                </span>
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {languages.map((lang) => (
                <DropdownMenuItem
                  key={lang.code}
                  className={cn(
                    "font-medium cursor-pointer",
                    language === lang.code && "text-primary"
                  )}
                  onClick={() => setLanguage(lang.code)}
                >
                  {lang.label}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          <Button variant="outline" className="hidden md:flex" asChild>
            <Link
              href="https://www.google.com/maps/search/?api=1&query=Taiwanway+26+South+St+Middletown+NY"
              target="_blank"
              rel="noopener noreferrer"
            >
              <MapPin className="mr-2 h-4 w-4" />
              {t('nav.getDirections')}
            </Link>
          </Button>
          <Button className="hidden md:flex" asChild>
            <Link href="tel:8453811002">
              {t('nav.orderPickup')}
            </Link>
          </Button>

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
                  {t('nav.home')}
                </Link>
                <div className="flex flex-col gap-2">
                  <button
                    onClick={() => setMenuOpen(!menuOpen)}
                    className="font-medium hover:text-primary transition-colors flex items-center justify-between"
                  >
                    {t('nav.menu')}
                    <ChevronDown className={cn("h-4 w-4 transition-transform", menuOpen ? "rotate-180" : "")} />
                  </button>
                  {menuOpen && (
                    <div className="flex flex-col gap-2 pl-4">
                      {menuItems.map((item) => (
                        <Link
                          key={item.key}
                          href={item.href}
                          className="font-medium hover:text-primary transition-colors"
                          onClick={(e) => {
                            handleMenuClick(e, item.href)
                            setIsOpen(false)
                          }}
                        >
                          {t(`menu.${item.key}`)}
                        </Link>
                      ))}
                    </div>
                  )}
                </div>
                <Link
                  href="/about"
                  className="font-medium hover:text-primary transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {t('nav.about')}
                </Link>
                <Link
                  href="/contact"
                  className="font-medium hover:text-primary transition-colors"
                  onClick={() => setIsOpen(false)}
                >
                  {t('nav.contact')}
                </Link>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}

