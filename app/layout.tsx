import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { Suspense } from "react"
import "./globals.css"
import { LanguageProvider } from "@/lib/i18n/language-context"
import { CookieConsentBanner } from "@/components/cookie-consent"
import { AnalyticsProvider, GoogleAnalyticsScript, FacebookPixelNoScript, GTMNoScript } from "@/components/analytics-provider"

const inter = Inter({ subsets: ["latin"] })

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
      <body className={inter.className}>
        <FacebookPixelNoScript />
        <GTMNoScript />
        <LanguageProvider>
          <Suspense fallback={null}>
            <AnalyticsProvider>
              {children}
            </AnalyticsProvider>
          </Suspense>
          <CookieConsentBanner />
        </LanguageProvider>
      </body>
    </html>
  )
}

