'use client'

import { useEffect } from 'react'
import { usePathname } from 'next/navigation'
import { initAllAnalytics, trackPageView, trackOrderClick, trackPhoneClick, trackMenuView, ANALYTICS_CONFIG } from '@/lib/analytics'
import { getCookieConsent } from '@/lib/cookies'

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  // 初始化分析追蹤
  useEffect(() => {
    // 檢查是否已有同意
    const consent = getCookieConsent()
    if (consent) {
      initAllAnalytics()
    }

    // 監聽同意狀態變化
    const handleConsentUpdate = () => {
      initAllAnalytics()
    }

    window.addEventListener('cookieConsentUpdated', handleConsentUpdate)

    return () => {
      window.removeEventListener('cookieConsentUpdated', handleConsentUpdate)
    }
  }, [])

  // 追蹤頁面瀏覽
  useEffect(() => {
    // 使用 window.location.search 代替 useSearchParams 以避免 SSR 問題
    const search = typeof window !== 'undefined' ? window.location.search : ''
    const url = pathname + search
    trackPageView(url)
  }, [pathname])

  // 追蹤菜單頁瀏覽（含從 Google 搜尋直接進來的訪客）
  useEffect(() => {
    if (pathname === '/menu') trackMenuView()
  }, [pathname])

  // 委派監聽外送與電話點擊：一次接好全站所有按鈕（含未來新增的）
  useEffect(() => {
    const handleClick = (e: MouseEvent) => {
      const anchor = (e.target as HTMLElement | null)?.closest('a')
      if (!anchor) return
      const href = anchor.getAttribute('href') || ''
      if (href.includes('ubereats.com')) trackOrderClick('ubereats')
      else if (href.includes('doordash.com')) trackOrderClick('doordash')
      else if (href.startsWith('tel:')) trackPhoneClick()
    }
    document.addEventListener('click', handleClick)
    return () => document.removeEventListener('click', handleClick)
  }, [])

  return <>{children}</>
}

// Google Analytics Script 組件（用於 Server Component）
export function GoogleAnalyticsScript() {
  if (!ANALYTICS_CONFIG.GA_MEASUREMENT_ID) return null

  return (
    <>
      <script
        async
        src={`https://www.googletagmanager.com/gtag/js?id=${ANALYTICS_CONFIG.GA_MEASUREMENT_ID}`}
      />
      <script
        id="google-analytics"
        dangerouslySetInnerHTML={{
          __html: `
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('consent', 'default', {
              'analytics_storage': 'granted',
              'ad_storage': 'denied',
              'ad_user_data': 'denied',
              'ad_personalization': 'denied'
            });
            gtag('config', '${ANALYTICS_CONFIG.GA_MEASUREMENT_ID}', {
              page_path: window.location.pathname,
              anonymize_ip: true
            });
          `,
        }}
      />
    </>
  )
}

// Facebook Pixel NoScript（用於不支持 JS 的瀏覽器）
export function FacebookPixelNoScript() {
  if (!ANALYTICS_CONFIG.FB_PIXEL_ID) return null

  return (
    <noscript>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img
        height="1"
        width="1"
        style={{ display: 'none' }}
        src={`https://www.facebook.com/tr?id=${ANALYTICS_CONFIG.FB_PIXEL_ID}&ev=PageView&noscript=1`}
        alt=""
      />
    </noscript>
  )
}

// GTM NoScript
export function GTMNoScript() {
  if (!ANALYTICS_CONFIG.GTM_ID) return null

  return (
    <noscript>
      <iframe
        src={`https://www.googletagmanager.com/ns.html?id=${ANALYTICS_CONFIG.GTM_ID}`}
        height="0"
        width="0"
        style={{ display: 'none', visibility: 'hidden' }}
      />
    </noscript>
  )
}
