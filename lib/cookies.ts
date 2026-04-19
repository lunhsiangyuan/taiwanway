'use client'

// Cookie 工具函數庫

export type CookieOptions = {
  expires?: Date | number // Date 或天數
  path?: string
  domain?: string
  secure?: boolean
  sameSite?: 'strict' | 'lax' | 'none'
}

// Cookie 同意類型
export type CookieConsent = {
  necessary: boolean      // 必要 Cookie（始終開啟）
  analytics: boolean      // 分析追蹤 Cookie
  marketing: boolean      // 行銷追蹤 Cookie
  preferences: boolean    // 偏好設定 Cookie
  timestamp: number       // 同意時間戳
}

export const CONSENT_COOKIE_NAME = 'taiwanway-cookie-consent'
export const LANGUAGE_COOKIE_NAME = 'taiwanway-language'

// 設置 Cookie
export function setCookie(
  name: string,
  value: string,
  options: CookieOptions = {}
): void {
  if (typeof document === 'undefined') return

  let cookieString = `${encodeURIComponent(name)}=${encodeURIComponent(value)}`

  if (options.expires) {
    let expiresDate: Date
    if (typeof options.expires === 'number') {
      expiresDate = new Date()
      expiresDate.setDate(expiresDate.getDate() + options.expires)
    } else {
      expiresDate = options.expires
    }
    cookieString += `; expires=${expiresDate.toUTCString()}`
  }

  cookieString += `; path=${options.path || '/'}`

  if (options.domain) {
    cookieString += `; domain=${options.domain}`
  }

  if (options.secure) {
    cookieString += '; secure'
  }

  cookieString += `; samesite=${options.sameSite || 'lax'}`

  document.cookie = cookieString
}

// 獲取 Cookie
export function getCookie(name: string): string | null {
  if (typeof document === 'undefined') return null

  const cookies = document.cookie.split(';')
  for (const cookie of cookies) {
    const [cookieName, cookieValue] = cookie.trim().split('=')
    if (cookieName === encodeURIComponent(name)) {
      return decodeURIComponent(cookieValue)
    }
  }
  return null
}

// 刪除 Cookie
export function deleteCookie(name: string, path: string = '/'): void {
  if (typeof document === 'undefined') return

  document.cookie = `${encodeURIComponent(name)}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=${path}`
}

// 獲取 Cookie 同意狀態
export function getCookieConsent(): CookieConsent | null {
  const consent = getCookie(CONSENT_COOKIE_NAME)
  if (!consent) return null

  try {
    return JSON.parse(consent) as CookieConsent
  } catch {
    return null
  }
}

// 設置 Cookie 同意
export function setCookieConsent(consent: Omit<CookieConsent, 'timestamp' | 'necessary'>): void {
  const fullConsent: CookieConsent = {
    ...consent,
    necessary: true, // 必要 Cookie 始終開啟
    timestamp: Date.now()
  }

  setCookie(CONSENT_COOKIE_NAME, JSON.stringify(fullConsent), {
    expires: 365, // 1 年
    secure: true,
    sameSite: 'lax'
  })
}

// 檢查是否已同意特定類型的 Cookie
export function hasConsent(type: keyof Omit<CookieConsent, 'timestamp'>): boolean {
  const consent = getCookieConsent()
  if (!consent) return type === 'necessary' // 必要 Cookie 預設允許
  return consent[type] ?? false
}

// 撤銷所有同意
export function revokeConsent(): void {
  deleteCookie(CONSENT_COOKIE_NAME)
}

// 接受所有 Cookie
export function acceptAllCookies(): void {
  setCookieConsent({
    analytics: true,
    marketing: true,
    preferences: true
  })
}

// 只接受必要 Cookie
export function acceptNecessaryOnly(): void {
  setCookieConsent({
    analytics: false,
    marketing: false,
    preferences: false
  })
}
