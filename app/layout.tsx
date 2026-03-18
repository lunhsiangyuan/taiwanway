import type { Metadata } from "next"
import { Playfair_Display_SC, Karla } from "next/font/google"
import "./globals.css"
import { LanguageProvider } from "@/lib/i18n/language-context"
import { CookieConsentBanner } from "@/components/cookie-consent"
import { AnalyticsProvider, GoogleAnalyticsScript, FacebookPixelNoScript, GTMNoScript } from "@/components/analytics-provider"

import { JsonLd } from "@/components/json-ld"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"
import { FloatingOrderCTA } from "@/components/floating-order-cta"

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
    'TaiwanWay 臺灣味 — 紐約 Middletown 正宗臺灣料理。招牌牛肉麵、滷肉飯、珍珠奶茶、鳳梨酥。Authentic Taiwanese beef noodles, braised pork rice, bubble tea in Middletown, NY.',
  openGraph: {
    siteName: 'TaiwanWay',
    locale: 'zh_TW',
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
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

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="zh-TW">
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
            <FloatingOrderCTA />
          </AnalyticsProvider>
          <CookieConsentBanner />
        </LanguageProvider>
      </body>
    </html>
  )
}
