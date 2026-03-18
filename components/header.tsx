'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Menu, Globe, ChevronDown } from 'lucide-react'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/i18n/language-context'
import { cn } from '@/lib/utils'

const navItems = [
  { key: 'nav.home', href: '/' },
  { key: 'nav.menu', href: '/menu' },
  { key: 'nav.about', href: '/about' },
  { key: 'nav.contact', href: '/contact' },
] as const

const languages = [
  { code: 'zh', label: '中文' },
  { code: 'en', label: 'English' },
  { code: 'es', label: 'Espanol' },
] as const

export function Header() {
  const [isOpen, setIsOpen] = useState(false)
  const [scrolled, setScrolled] = useState(false)
  const { language, setLanguage, t } = useLanguage()

  useEffect(() => {
    const handleScroll = () => {
      setScrolled(window.scrollY > 50)
    }
    handleScroll()
    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  return (
    <header
      className={cn(
        'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
        scrolled
          ? 'bg-cream/95 backdrop-blur-md shadow-sm'
          : 'bg-transparent'
      )}
    >
      <a
        href="#main-content"
        className="sr-only focus:not-sr-only focus:absolute focus:top-2 focus:left-2 focus:z-[60] focus:bg-gold focus:text-white focus:px-4 focus:py-2 focus:rounded-md focus:font-body"
      >
        Skip to main content
      </a>
      <div className="w-full px-4 md:px-6 lg:px-8 max-w-screen-2xl mx-auto flex h-20 items-center justify-between">
        {/* Logo */}
        <Link
          href="/"
          className={cn(
            'font-heading text-2xl font-bold tracking-wide transition-colors duration-300',
            scrolled ? 'text-foreground' : 'text-white'
          )}
        >
          TaiwanWay
        </Link>

        {/* Desktop Nav */}
        <nav className="hidden md:flex items-center gap-8">
          {navItems.map((item) => (
            <Link
              key={item.key}
              href={item.href}
              className={cn(
                'font-body font-medium text-sm uppercase tracking-wider transition-colors duration-300 hover:text-gold',
                scrolled ? 'text-foreground' : 'text-white'
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
                  scrolled
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

          {/* Order Online CTA */}
          <Button
            asChild
            className="bg-gold text-white hover:bg-gold/90 font-body font-semibold rounded-full px-6"
          >
            <Link href="https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjMzMiVFOCU5QiU4QiVFNiU4RCVCMiUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUp0Ukk4U3pHVWJqUVJnaTI1VUlGeTJsUSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyMy40Nzg1NzMyOTk5OTk5OTclMkMlMjJsb25naXR1ZGUlMjIlM0ExMjAuNDUyOTQwNCU3RA%3D%3D" target="_blank" rel="noopener noreferrer">
              Order Online
            </Link>
          </Button>
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
                  scrolled ? 'text-foreground' : 'text-white'
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
                  scrolled ? 'text-foreground' : 'text-white'
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
                <Button
                  asChild
                  className="bg-gold text-white hover:bg-gold/90 font-body font-semibold rounded-full mt-4"
                >
                  <Link href="https://www.ubereats.com/store/taiwanway-middletown/sELndOIGX42P7drGC5jC1A?diningMode=DELIVERY&pl=JTdCJTIyYWRkcmVzcyUyMiUzQSUyMjMzMiVFOCU5QiU4QiVFNiU4RCVCMiUyMiUyQyUyMnJlZmVyZW5jZSUyMiUzQSUyMkNoSUp0Ukk4U3pHVWJqUVJnaTI1VUlGeTJsUSUyMiUyQyUyMnJlZmVyZW5jZVR5cGUlMjIlM0ElMjJnb29nbGVfcGxhY2VzJTIyJTJDJTIybGF0aXR1ZGUlMjIlM0EyMy40Nzg1NzMyOTk5OTk5OTclMkMlMjJsb25naXR1ZGUlMjIlM0ExMjAuNDUyOTQwNCU3RA%3D%3D" target="_blank" rel="noopener noreferrer" onClick={() => setIsOpen(false)}>
                    Order Online
                  </Link>
                </Button>
              </nav>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </header>
  )
}
