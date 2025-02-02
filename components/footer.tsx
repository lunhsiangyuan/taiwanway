'use client'

import Link from "next/link"
import { Instagram, Mail, Phone } from "lucide-react"
import Image from "next/image"
import { useLanguage } from "@/lib/i18n/language-context"

export function Footer() {
  const { t } = useLanguage()

  return (
    <footer className="bg-secondary/30 border-t">
      <div className="w-full px-4 md:px-6 lg:px-8 max-w-screen-2xl mx-auto py-8 pb-16 md:py-12">
        <div className="grid grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <h3 className="font-semibold mb-4">{t('footer.quickLinks')}</h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-muted-foreground hover:text-primary">
                  {t('nav.home')}
                </Link>
              </li>
              <li>
                <Link href="/menu" className="text-muted-foreground hover:text-primary">
                  {t('nav.menu')}
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-muted-foreground hover:text-primary">
                  {t('nav.about')}
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-muted-foreground hover:text-primary">
                  {t('nav.contact')}
                </Link>
              </li>
            </ul>
          </div>
          <div>
            <h3 className="font-semibold mb-4">{t('footer.hours')}</h3>
            <p className="text-muted-foreground">{t('footer.schedule')}</p>
            <p className="text-muted-foreground">11:00 AM - 7:00 PM</p>
          </div>
          <div>
            <h3 className="font-semibold mb-4">{t('footer.contact')}</h3>
            <p className="text-muted-foreground">26 South St, Middletown NY</p>
            <p className="text-muted-foreground">845-381-1002</p>
            <p className="text-muted-foreground">usamyheish@gmail.com</p>
          </div>
          <div className="pb-6 md:pb-0">
            <h3 className="font-semibold mb-4">{t('footer.followUs')}</h3>
            <div className="flex flex-wrap gap-4">
              <a 
                href="https://www.instagram.com/taiwanway10940/" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary"
              >
                <Instagram className="h-6 w-6" />
              </a>
              <a 
                href="https://www.ganjingworld.com/zh-TW/channel/1gn0bh6v5723YVk4DTBsG6uEk1sq0c" 
                target="_blank" 
                rel="noopener noreferrer"
                className="text-muted-foreground hover:text-primary flex items-center"
              >
                <Image 
                  src="https://www.ganjingworld.com/icons/favicon-32x32.png" 
                  alt="GanJing World" 
                  width={24} 
                  height={24} 
                  className="opacity-75 hover:opacity-100 transition-opacity"
                />
              </a>
              <a href="mailto:usamyheish@gmail.com" className="text-muted-foreground hover:text-primary">
                <Mail className="h-6 w-6" />
              </a>
              <a href="tel:845-381-1002" className="text-muted-foreground hover:text-primary">
                <Phone className="h-6 w-6" />
              </a>
            </div>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t text-center text-muted-foreground">
          <p>&copy; 2025 Taiwanway. {t('footer.allRights')}.</p>
        </div>
      </div>
    </footer>
  )
}

