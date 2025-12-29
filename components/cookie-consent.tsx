'use client'

import { useState, useEffect } from 'react'
import { X, Settings, Cookie } from 'lucide-react'
import { Button } from '@/components/ui/button'
import { useLanguage } from '@/lib/i18n/language-context'
import {
  getCookieConsent,
  setCookieConsent,
  acceptAllCookies,
  acceptNecessaryOnly
} from '@/lib/cookies'

const translations = {
  zh: {
    title: 'Cookie 設定',
    description: '我們使用 Cookie 來改善您的瀏覽體驗、分析網站流量，並提供個人化內容。您可以選擇接受所有 Cookie，或自訂您的偏好設定。',
    acceptAll: '接受全部',
    acceptNecessary: '僅必要',
    customize: '自訂設定',
    save: '儲存設定',
    necessary: '必要 Cookie',
    necessaryDesc: '這些 Cookie 是網站正常運作所必需的，無法關閉。',
    analytics: '分析 Cookie',
    analyticsDesc: '幫助我們了解訪客如何使用網站，以便改善用戶體驗。',
    marketing: '行銷 Cookie',
    marketingDesc: '用於追蹤訪客以顯示相關廣告和行銷活動。',
    preferences: '偏好 Cookie',
    preferencesDesc: '記住您的偏好設定，如語言選擇。',
    privacyPolicy: '隱私政策',
    alwaysOn: '始終開啟'
  },
  en: {
    title: 'Cookie Settings',
    description: 'We use cookies to improve your browsing experience, analyze site traffic, and provide personalized content. You can accept all cookies or customize your preferences.',
    acceptAll: 'Accept All',
    acceptNecessary: 'Necessary Only',
    customize: 'Customize',
    save: 'Save Settings',
    necessary: 'Necessary Cookies',
    necessaryDesc: 'These cookies are essential for the website to function properly and cannot be disabled.',
    analytics: 'Analytics Cookies',
    analyticsDesc: 'Help us understand how visitors use the website to improve user experience.',
    marketing: 'Marketing Cookies',
    marketingDesc: 'Used to track visitors to display relevant ads and marketing campaigns.',
    preferences: 'Preference Cookies',
    preferencesDesc: 'Remember your preferences such as language selection.',
    privacyPolicy: 'Privacy Policy',
    alwaysOn: 'Always On'
  },
  es: {
    title: 'Configuración de Cookies',
    description: 'Utilizamos cookies para mejorar su experiencia de navegación, analizar el tráfico del sitio y proporcionar contenido personalizado. Puede aceptar todas las cookies o personalizar sus preferencias.',
    acceptAll: 'Aceptar Todo',
    acceptNecessary: 'Solo Necesarias',
    customize: 'Personalizar',
    save: 'Guardar Configuración',
    necessary: 'Cookies Necesarias',
    necessaryDesc: 'Estas cookies son esenciales para el funcionamiento del sitio web y no se pueden desactivar.',
    analytics: 'Cookies de Análisis',
    analyticsDesc: 'Nos ayudan a entender cómo los visitantes usan el sitio web para mejorar la experiencia.',
    marketing: 'Cookies de Marketing',
    marketingDesc: 'Se utilizan para rastrear visitantes y mostrar anuncios y campañas relevantes.',
    preferences: 'Cookies de Preferencias',
    preferencesDesc: 'Recuerdan sus preferencias como la selección de idioma.',
    privacyPolicy: 'Política de Privacidad',
    alwaysOn: 'Siempre Activo'
  }
}

export function CookieConsentBanner() {
  const { language } = useLanguage()
  const t = translations[language]

  const [isVisible, setIsVisible] = useState(false)
  const [showDetails, setShowDetails] = useState(false)
  const [preferences, setPreferences] = useState({
    analytics: false,
    marketing: false,
    preferences: true
  })

  useEffect(() => {
    const consent = getCookieConsent()
    if (!consent) {
      // 延遲顯示，避免影響首次載入體驗
      const timer = setTimeout(() => setIsVisible(true), 1000)
      return () => clearTimeout(timer)
    }
  }, [])

  const handleAcceptAll = () => {
    acceptAllCookies()
    setIsVisible(false)
    // 觸發自訂事件通知分析追蹤器
    window.dispatchEvent(new CustomEvent('cookieConsentUpdated', {
      detail: { analytics: true, marketing: true, preferences: true }
    }))
  }

  const handleAcceptNecessary = () => {
    acceptNecessaryOnly()
    setIsVisible(false)
    window.dispatchEvent(new CustomEvent('cookieConsentUpdated', {
      detail: { analytics: false, marketing: false, preferences: false }
    }))
  }

  const handleSavePreferences = () => {
    setCookieConsent(preferences)
    setIsVisible(false)
    window.dispatchEvent(new CustomEvent('cookieConsentUpdated', {
      detail: preferences
    }))
  }

  if (!isVisible) return null

  return (
    <div className="fixed inset-0 z-50 flex items-end justify-center p-4 sm:items-center">
      {/* 背景遮罩 */}
      <div
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={() => setShowDetails(false)}
      />

      {/* Cookie 橫幅 */}
      <div className="relative w-full max-w-lg rounded-2xl bg-white p-6 shadow-2xl sm:max-w-xl">
        {/* 關閉按鈕 */}
        <button
          onClick={handleAcceptNecessary}
          className="absolute right-4 top-4 text-gray-400 hover:text-gray-600 transition-colors"
          aria-label="Close"
        >
          <X className="h-5 w-5" />
        </button>

        {/* 標題 */}
        <div className="flex items-center gap-3 mb-4">
          <div className="flex h-10 w-10 items-center justify-center rounded-full bg-primary/10">
            <Cookie className="h-5 w-5 text-primary" />
          </div>
          <h2 className="text-xl font-semibold text-gray-900">{t.title}</h2>
        </div>

        {/* 描述 */}
        <p className="text-sm text-gray-600 mb-6 leading-relaxed">
          {t.description}
        </p>

        {/* 詳細設定 */}
        {showDetails && (
          <div className="mb-6 space-y-4 border-t border-b py-4">
            {/* 必要 Cookie */}
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-2">
                  <span className="font-medium text-gray-900">{t.necessary}</span>
                  <span className="text-xs bg-gray-100 text-gray-600 px-2 py-0.5 rounded">
                    {t.alwaysOn}
                  </span>
                </div>
                <p className="text-xs text-gray-500 mt-1">{t.necessaryDesc}</p>
              </div>
              <input
                type="checkbox"
                checked={true}
                disabled
                className="h-5 w-5 rounded border-gray-300 text-primary"
              />
            </div>

            {/* 分析 Cookie */}
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <span className="font-medium text-gray-900">{t.analytics}</span>
                <p className="text-xs text-gray-500 mt-1">{t.analyticsDesc}</p>
              </div>
              <input
                type="checkbox"
                checked={preferences.analytics}
                onChange={(e) => setPreferences(prev => ({ ...prev, analytics: e.target.checked }))}
                className="h-5 w-5 rounded border-gray-300 text-primary cursor-pointer"
              />
            </div>

            {/* 行銷 Cookie */}
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <span className="font-medium text-gray-900">{t.marketing}</span>
                <p className="text-xs text-gray-500 mt-1">{t.marketingDesc}</p>
              </div>
              <input
                type="checkbox"
                checked={preferences.marketing}
                onChange={(e) => setPreferences(prev => ({ ...prev, marketing: e.target.checked }))}
                className="h-5 w-5 rounded border-gray-300 text-primary cursor-pointer"
              />
            </div>

            {/* 偏好 Cookie */}
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <span className="font-medium text-gray-900">{t.preferences}</span>
                <p className="text-xs text-gray-500 mt-1">{t.preferencesDesc}</p>
              </div>
              <input
                type="checkbox"
                checked={preferences.preferences}
                onChange={(e) => setPreferences(prev => ({ ...prev, preferences: e.target.checked }))}
                className="h-5 w-5 rounded border-gray-300 text-primary cursor-pointer"
              />
            </div>
          </div>
        )}

        {/* 按鈕組 */}
        <div className="flex flex-col sm:flex-row gap-3">
          {showDetails ? (
            <Button
              onClick={handleSavePreferences}
              className="flex-1 bg-primary hover:bg-primary/90"
            >
              {t.save}
            </Button>
          ) : (
            <>
              <Button
                onClick={handleAcceptAll}
                className="flex-1 bg-primary hover:bg-primary/90"
              >
                {t.acceptAll}
              </Button>
              <Button
                onClick={handleAcceptNecessary}
                variant="outline"
                className="flex-1"
              >
                {t.acceptNecessary}
              </Button>
              <Button
                onClick={() => setShowDetails(true)}
                variant="ghost"
                className="flex-1 gap-2"
              >
                <Settings className="h-4 w-4" />
                {t.customize}
              </Button>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

// 用於頁腳的 Cookie 設定按鈕
export function CookieSettingsButton() {
  const { language } = useLanguage()
  const t = translations[language]

  const handleOpenSettings = () => {
    // 清除同意以重新顯示橫幅
    window.dispatchEvent(new CustomEvent('openCookieSettings'))
  }

  return (
    <button
      onClick={handleOpenSettings}
      className="text-sm text-gray-500 hover:text-primary transition-colors flex items-center gap-1"
    >
      <Cookie className="h-3.5 w-3.5" />
      {t.title}
    </button>
  )
}
