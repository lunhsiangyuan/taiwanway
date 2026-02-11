import type { Metadata } from "next"
import { Playfair_Display_SC, Karla } from "next/font/google"
import "./globals.css"
import { LanguageProvider } from "@/lib/i18n/language-context"
import { CookieConsentBanner } from "@/components/cookie-consent"
import { AnalyticsProvider, GoogleAnalyticsScript, FacebookPixelNoScript, GTMNoScript } from "@/components/analytics-provider"

import { JsonLd } from "@/components/json-ld"
import { Header } from "@/components/header"
import { Footer } from "@/components/footer"

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
  title: "Taiwanway | Authentic Taiwanese Cuisine",
  description: "Authentic Taiwanese beef noodles, braised pork rice, pineapple cakes and bubble tea in New York",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
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
