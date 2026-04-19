import type { Metadata } from "next"
import { Playfair_Display_SC, Karla } from "next/font/google"
import { cookies } from "next/headers"
import "./globals.css"
import { LanguageProvider } from "@/lib/i18n/language-context"
import { CookieConsentBanner } from "@/components/cookie-consent"
import { AnalyticsProvider, GoogleAnalyticsScript, FacebookPixelNoScript, GTMNoScript } from "@/components/analytics-provider"

import { JsonLd } from "@/components/json-ld"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"

const LANG_ATTR: Record<string, string> = {
  zh: 'zh-TW',
  en: 'en',
  es: 'es',
}

const playfairDisplaySC = Playfair_Display_SC({
  subsets: ['latin'],
  weight: ['400', '900'],
  variable: '--font-heading',
  display: 'swap',
})

const karla = Karla({
  subsets: ['latin'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-body',
  display: 'swap',
})

export const metadata: Metadata = {
  metadataBase: new URL('https://taiwanwayny.com'),
  title: {
    default: 'TaiwanWay | Authentic Taiwanese Cuisine in Middletown, NY',
    template: '%s | TaiwanWay',
  },
  description:
    'TaiwanWay 臺灣味 — 紐約 Middletown 正宗臺灣料理。招牌牛肉麵、滷肉飯、珍珠奶茶、鳳梨酥。Authentic Taiwanese beef noodles, braised pork rice, bubble tea in Middletown, NY. Serving Orange County & Hudson Valley.',
  keywords: [
    'Taiwanese restaurant Middletown NY',
    'Taiwanese food near me',
    'bubble tea Middletown NY',
    'authentic Taiwanese cuisine',
    'Hudson Valley Taiwanese restaurant',
    'Orange County NY Taiwanese food',
    'beef noodle soup Middletown',
    'braised pork rice',
    'pineapple cake NY',
    'boba tea Middletown',
    '台灣料理 紐約',
    '紐約 珍珠奶茶',
    'Middletown NY restaurant',
    'TaiwanWay 臺灣味',
  ],
  alternates: {
    canonical: 'https://taiwanwayny.com',
    languages: {
      'en-US': 'https://taiwanwayny.com',
      'zh-TW': 'https://taiwanwayny.com',
      'es': 'https://taiwanwayny.com',
      'x-default': 'https://taiwanwayny.com',
    },
  },
  openGraph: {
    siteName: 'TaiwanWay',
    locale: 'en_US',
    alternateLocale: ['zh_TW', 'es'],
    type: 'website',
    images: [
      {
        url: '/images/og-storefront.jpg',
        width: 1200,
        height: 630,
        alt: 'TaiwanWay 臺灣味 storefront at 26 South St, Middletown NY — Taiwanese café',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    images: ['/images/og-storefront.jpg'],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-image-preview': 'large',
    },
  },
}

export default async function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const cookieStore = await cookies()
  const langCookie = cookieStore.get('taiwanway-language')?.value
  const htmlLang = LANG_ATTR[langCookie ?? ''] ?? 'en'

  return (
    <html lang={htmlLang}>
      <head>
        <GoogleAnalyticsScript />
      </head>
      <body className={`${playfairDisplaySC.variable} ${karla.variable} font-body antialiased`}>
        <JsonLd />
        <FacebookPixelNoScript />
        <GTMNoScript />
        <LanguageProvider>
          <AnalyticsProvider>
            <Header />
            {children}
            <Footer />
          </AnalyticsProvider>
          <CookieConsentBanner />
        </LanguageProvider>
      </body>
    </html>
  )
}
