'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { Menu, Globe, ChevronDown } from 'lucide-react'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/i18n/language-context'
import { cn } from '@/lib/utils'

const navItems = [
  { key: 'nav.home', href: '/' },
  { key: 'nav.menu', href: '/menu' },
  { key: 'nav.products', href: '/products' },
  { key: 'nav.faq', href: '/faq' },
  { key: 'nav.about', href: '/about' },
  { key: 'nav.contact', href: '/contact' },
] as const

const languages = [
  { code: 'zh', label: '中文' },
  { code: 'en', label: 'English' },
  { code: 'es', label: 'Espanol' },
] as const

const UBER_URL = 'https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A'
const DOORDASH_URL = 'https://www.doordash.com/store/taiwan-way-middletown-42843267/'

export function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const [orderOpen, setOrderOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const { language, setLanguage, t } = useLanguage()

  const orderLabel = language === 'zh' ? '線上訂餐' : language === 'es' ? 'Pedir en línea' : 'Order Online'

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50)
    }
    handleScroll()
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  // 新版 Hero 改為明亮米底，header 一律採淺色底＋深色文字，確保可讀
  const useDarkText = true

  return (
    <header
      className={cn(
        'sticky top-0 z-50 transition-all duration-300 bg-cream/95 backdrop-blur-md',
        scrolled ? 'shadow-sm' : 'shadow-none'
      )}
    >
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[60] focus:bg-gold focus:text-white focus:px-4 focus:py-2 focus:rounded-md focus:font-body"
      >
        Skip to main content
      </a>
      <div className="w-full px-4 md:px-6 lg:px-8 max-w-screen-2xl mx-auto flex h-20 items-center justify-between">
        {/* Logo — 橫式文字 logo（LOGO-B） */}
        <Link href="/" className="flex items-center shrink-0" aria-label="TaiwanWay home">
          <Image
            src="/brand/logo-horizontal-trim.png"
            alt="TaiwanWay"
            width={2246}
            height={506}
            priority
            className="h-10 w-auto md:h-12"
          />
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8">
          {navItems.map((item) => (
            <Link
              key={item.key}
              href={item.href}
              className={cn(
                'font-body font-medium text-sm uppercase tracking-wider transition-colors duration-300 hover:text-gold focus-visible:outline-2 focus-visible:outline-[hsl(44,80%,40%)]',
                useDarkText ? 'text-foreground' : 'text-white'
              )}
            >
              {t(item.key)}
            </Link>
          ))}
        </nav>

        {/* Desktop Right Actions */}
        <div className="hidden md:flex items-center gap-4">
          {/* Language Switcher */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="sm"
                className={cn(
                  'flex items-center gap-1.5 transition-colors duration-300',
                  useDarkText
                    ? 'text-foreground hover:text-gold'
                    : 'text-white hover:text-gold'
                )}
              >
                <Globe className="h-4 w-4" />
                <span className="text-sm font-medium">
                  {languages.find(l => l.code === language)?.label || '中文'}
                </span>
                <ChevronDown className="h-3 w-3" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {languages.map((lang) => (
                <DropdownMenuItem
                  key={lang.code}
                  className={cn(
                    'cursor-pointer font-body',
                    language === lang.code && 'text-primary font-semibold'
                  )}
                  onClick={() => setLanguage(lang.code)}
                >
                  {lang.label}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          {/* Order CTA — 線上訂餐（合併 Uber Eats + DoorDash） */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button className="bg-primary text-primary-foreground hover:bg-accent font-body font-semibold rounded-full px-5 flex items-center gap-1.5">
                🛵 {orderLabel}
                <ChevronDown className="h-3.5 w-3.5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="min-w-[11rem]">
              <DropdownMenuItem asChild className="cursor-pointer font-body font-medium">
                <a href={UBER_URL} target="_blank" rel="noopener noreferrer">
                  <span className="mr-2 text-[#06C167]">●</span> Uber Eats
                </a>
              </DropdownMenuItem>
              <DropdownMenuItem asChild className="cursor-pointer font-body font-medium">
                <a href={DOORDASH_URL} target="_blank" rel="noopener noreferrer">
                  <span className="mr-2 text-[#FF3008]">●</span> DoorDash
                </a>
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </div>

        {/* Mobile Hamburger */}
        <div className="md:hidden flex items-center gap-2">
          {/* Mobile Language Switcher */}
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                aria-label="Switch language"
                className={cn(
                  'transition-colors duration-300',
                  useDarkText ? 'text-foreground' : 'text-white'
                )}
              >
                <Globe className="h-5 w-5" />
              </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              {languages.map((lang) => (
                <DropdownMenuItem
                  key={lang.code}
                  className={cn(
                    'cursor-pointer font-body',
                    language === lang.code && 'text-primary font-semibold'
                  )}
                  onClick={() => setLanguage(lang.code)}
                >
                  {lang.label}
                </DropdownMenuItem>
              ))}
            </DropdownMenuContent>
          </DropdownMenu>

          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button
                variant="ghost"
                size="icon"
                aria-label="Open navigation menu"
                className={cn(
                  'transition-colors duration-300',
                  useDarkText ? 'text-foreground' : 'text-white'
                )}
              >
                <Menu className="h-6 w-6" />
              </Button>
            </SheetTrigger>
            <SheetContent side="right" className="bg-cream w-72">
              <nav className="flex flex-col gap-6 mt-8">
                {navItems.map((item) => (
                  <Link
                    key={item.key}
                    href={item.href}
                    className="font-body font-medium text-lg text-foreground hover:text-gold transition-colors"
                    onClick={() => setIsOpen(false)}
                  >
                    {t(item.key)}
                  </Link>
                ))}
                <div className="mt-4">
                  <Button
                    onClick={() => setOrderOpen(!orderOpen)}
                    className="w-full bg-primary text-primary-foreground hover:bg-accent font-body font-semibold rounded-full flex items-center justify-center gap-1.5"
                  >
                    🛵 {orderLabel}
                    <ChevronDown className={cn('h-4 w-4 transition-transform', orderOpen && 'rotate-180')} />
                  </Button>
                  {orderOpen && (
                    <div className="mt-3 flex flex-col gap-2">
                      <a
                        href={UBER_URL}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={() => setIsOpen(false)}
                        className="flex items-center gap-2 rounded-full border border-primary/30 px-4 py-2.5 font-body text-sm font-medium text-foreground hover:bg-primary/[0.06]"
                      >
                        <span className="text-[#06C167]">●</span> Uber Eats
                      </a>
                      <a
                        href={DOORDASH_URL}
                        target="_blank"
                        rel="noopener noreferrer"
                        onClick={() => setIsOpen(false)}
                        className="flex items-center gap-2 rounded-full border border-primary/30 px-4 py-2.5 font-body text-sm font-medium text-foreground hover:bg-primary/[0.06]"
                      >
                        <span className="text-[#FF3008]">●</span> DoorDash
                      </a>
                    </div>
                  )}
                </div>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}
