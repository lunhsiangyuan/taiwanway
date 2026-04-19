'use client'

import { getCookieConsent, hasConsent } from './cookies'

// ==========================================
// 分析追蹤配置
// ==========================================

// 在這裡填入您的追蹤 ID
export const ANALYTICS_CONFIG = {
  // Google Analytics 4
  GA_MEASUREMENT_ID: process.env.NEXT_PUBLIC_GA_MEASUREMENT_ID || '',

  // Facebook Pixel
  FB_PIXEL_ID: process.env.NEXT_PUBLIC_FB_PIXEL_ID || '',

  // Hotjar
  HOTJAR_ID: process.env.NEXT_PUBLIC_HOTJAR_ID || '',
  HOTJAR_VERSION: 6,

  // Google Tag Manager (可選)
  GTM_ID: process.env.NEXT_PUBLIC_GTM_ID || '',
}

// ==========================================
// Google Analytics 4
// ==========================================

declare global {
  interface Window {
    gtag: (...args: unknown[]) => void
    dataLayer: unknown[]
    fbq: (...args: unknown[]) => void
    _fbq: unknown
    hj: (...args: unknown[]) => void
    _hjSettings: { hjid: number; hjsv: number }
  }
}

export function initGoogleAnalytics(): void {
  if (!ANALYTICS_CONFIG.GA_MEASUREMENT_ID || typeof window === 'undefined') return
  if (!hasConsent('analytics')) return

  // 載入 gtag.js
  const script = document.createElement('script')
  script.async = true
  script.src = `https://www.googletagmanager.com/gtag/js?id=${ANALYTICS_CONFIG.GA_MEASUREMENT_ID}`
  document.head.appendChild(script)

  // 初始化 dataLayer
  window.dataLayer = window.dataLayer || []
  window.gtag = function gtag(...args: unknown[]) {
    window.dataLayer.push(args)
  }
  window.gtag('js', new Date())
  window.gtag('config', ANALYTICS_CONFIG.GA_MEASUREMENT_ID, {
    page_path: window.location.pathname,
    anonymize_ip: true, // GDPR 合規
  })

  console.log('[Analytics] Google Analytics initialized')
}

// GA4 事件追蹤
export function trackEvent(
  eventName: string,
  eventParams?: Record<string, unknown>
): void {
  if (!hasConsent('analytics') || typeof window === 'undefined' || !window.gtag) return

  window.gtag('event', eventName, eventParams)
}

// 頁面瀏覽追蹤
export function trackPageView(path: string): void {
  if (!hasConsent('analytics') || typeof window === 'undefined' || !window.gtag) return

  window.gtag('config', ANALYTICS_CONFIG.GA_MEASUREMENT_ID, {
    page_path: path,
  })
}

// ==========================================
// Facebook Pixel
// ==========================================

export function initFacebookPixel(): void {
  if (!ANALYTICS_CONFIG.FB_PIXEL_ID || typeof window === 'undefined') return
  if (!hasConsent('marketing')) return

  // Facebook Pixel 初始化代碼
  const fbq = function(...args: unknown[]) {
    if ((fbq as unknown as { callMethod?: (...args: unknown[]) => void }).callMethod) {
      (fbq as unknown as { callMethod: (...args: unknown[]) => void }).callMethod(...args)
    } else {
      (fbq as unknown as { queue: unknown[] }).queue.push(args)
    }
  }

  if (!window._fbq) window._fbq = fbq
  window.fbq = fbq
  ;(fbq as unknown as { push: typeof fbq }).push = fbq
  ;(fbq as unknown as { loaded: boolean }).loaded = true
  ;(fbq as unknown as { version: string }).version = '2.0'
  ;(fbq as unknown as { queue: unknown[] }).queue = []

  // 載入 Facebook Pixel 腳本
  const script = document.createElement('script')
  script.async = true
  script.src = 'https://connect.facebook.net/en_US/fbevents.js'
  document.head.appendChild(script)

  window.fbq('init', ANALYTICS_CONFIG.FB_PIXEL_ID)
  window.fbq('track', 'PageView')

  console.log('[Analytics] Facebook Pixel initialized')
}

// FB Pixel 事件追蹤
export function trackFBEvent(
  eventName: string,
  eventParams?: Record<string, unknown>
): void {
  if (!hasConsent('marketing') || typeof window === 'undefined' || !window.fbq) return

  window.fbq('track', eventName, eventParams)
}

// FB 自訂事件
export function trackFBCustomEvent(
  eventName: string,
  eventParams?: Record<string, unknown>
): void {
  if (!hasConsent('marketing') || typeof window === 'undefined' || !window.fbq) return

  window.fbq('trackCustom', eventName, eventParams)
}

// ==========================================
// Hotjar
// ==========================================

export function initHotjar(): void {
  if (!ANALYTICS_CONFIG.HOTJAR_ID || typeof window === 'undefined') return
  if (!hasConsent('analytics')) return

  window.hj = window.hj || function(...args: unknown[]) {
    (window.hj as unknown as { q: unknown[] }).q = (window.hj as unknown as { q: unknown[] }).q || []
    ;(window.hj as unknown as { q: unknown[] }).q.push(args)
  }
  window._hjSettings = {
    hjid: Number(ANALYTICS_CONFIG.HOTJAR_ID),
    hjsv: ANALYTICS_CONFIG.HOTJAR_VERSION
  }

  const script = document.createElement('script')
  script.async = true
  script.src = `https://static.hotjar.com/c/hotjar-${ANALYTICS_CONFIG.HOTJAR_ID}.js?sv=${ANALYTICS_CONFIG.HOTJAR_VERSION}`
  document.head.appendChild(script)

  console.log('[Analytics] Hotjar initialized')
}

// Hotjar 事件
export function trackHotjarEvent(eventName: string): void {
  if (!hasConsent('analytics') || typeof window === 'undefined' || !window.hj) return

  window.hj('event', eventName)
}

// Hotjar 用戶識別
export function identifyHotjarUser(userId: string, attributes?: Record<string, unknown>): void {
  if (!hasConsent('analytics') || typeof window === 'undefined' || !window.hj) return

  window.hj('identify', userId, attributes)
}

// ==========================================
// Google Tag Manager (可選)
// ==========================================

export function initGTM(): void {
  if (!ANALYTICS_CONFIG.GTM_ID || typeof window === 'undefined') return

  window.dataLayer = window.dataLayer || []
  window.dataLayer.push({
    'gtm.start': new Date().getTime(),
    event: 'gtm.js'
  })

  const script = document.createElement('script')
  script.async = true
  script.src = `https://www.googletagmanager.com/gtm.js?id=${ANALYTICS_CONFIG.GTM_ID}`
  document.head.appendChild(script)

  console.log('[Analytics] Google Tag Manager initialized')
}

// GTM 數據層推送
export function pushToDataLayer(data: Record<string, unknown>): void {
  if (typeof window === 'undefined') return

  window.dataLayer = window.dataLayer || []
  window.dataLayer.push(data)
}

// ==========================================
// 統一初始化函數
// ==========================================

export function initAllAnalytics(): void {
  const consent = getCookieConsent()

  if (!consent) {
    console.log('[Analytics] No consent given, skipping initialization')
    return
  }

  if (consent.analytics) {
    initGoogleAnalytics()
    initHotjar()
  }

  if (consent.marketing) {
    initFacebookPixel()
  }

  // GTM 可以在有任何同意時初始化（在 GTM 內部控制追蹤器）
  if (consent.analytics || consent.marketing) {
    initGTM()
  }
}

// ==========================================
// 預設電商事件
// ==========================================

// 查看商品
export function trackViewItem(item: {
  id: string
  name: string
  category?: string
  price?: number
}): void {
  trackEvent('view_item', {
    items: [item]
  })
  trackFBEvent('ViewContent', {
    content_ids: [item.id],
    content_name: item.name,
    content_type: 'product',
    value: item.price,
    currency: 'USD'
  })
}

// 加入購物車
export function trackAddToCart(item: {
  id: string
  name: string
  price: number
  quantity: number
}): void {
  trackEvent('add_to_cart', {
    items: [item],
    value: item.price * item.quantity,
    currency: 'USD'
  })
  trackFBEvent('AddToCart', {
    content_ids: [item.id],
    content_name: item.name,
    content_type: 'product',
    value: item.price * item.quantity,
    currency: 'USD'
  })
}

// 開始結帳
export function trackBeginCheckout(value: number, items: unknown[]): void {
  trackEvent('begin_checkout', {
    items,
    value,
    currency: 'USD'
  })
  trackFBEvent('InitiateCheckout', {
    value,
    currency: 'USD',
    num_items: items.length
  })
}

// 完成購買
export function trackPurchase(transactionId: string, value: number, items: unknown[]): void {
  trackEvent('purchase', {
    transaction_id: transactionId,
    items,
    value,
    currency: 'USD'
  })
  trackFBEvent('Purchase', {
    value,
    currency: 'USD',
    content_ids: items.map((i: unknown) => (i as { id: string }).id),
    content_type: 'product'
  })
}

// 聯繫表單提交
export function trackContact(method?: string): void {
  trackEvent('contact', { method })
  trackFBEvent('Contact')
  trackHotjarEvent('contact_form_submitted')
}

// 電話點擊
export function trackPhoneClick(): void {
  trackEvent('click_phone')
  trackFBCustomEvent('ClickPhone')
}

// 地圖點擊
export function trackMapClick(): void {
  trackEvent('click_map')
  trackFBCustomEvent('ClickMap')
}

// 菜單查看
export function trackMenuView(category?: string): void {
  trackEvent('view_menu', { category })
  trackFBEvent('ViewContent', {
    content_type: 'menu',
    content_category: category
  })
}
