'use client'

import { useState, useEffect } from 'react'
import { ChevronDown } from 'lucide-react'
import { useLanguage } from '@/lib/i18n/language-context'
import {
  getCookieConsent,
  setCookieConsent,
  acceptAllCookies,
  acceptNecessaryOnly
} from '@/lib/cookies'

const translations = {
  zh: {
    description: '按一下「全部接受」，代表您允許我們置放 Cookie 來提升您在本網站上的使用體驗、協助我們分析網站效能和使用狀況，以及讓我們投放相關聯的行銷內容。您可以在下方管理 Cookie 設定。',
    acceptAll: '全部接受',
    manage: '管理 Cookies',
    settingsTitle: '隱私權偏好設定',
    confirm: '確認選擇',
    necessary: '必要的 Cookie',
    necessaryDesc: '網站運行離不開這些 Cookie 且您不能在系統中將其關閉。通常僅根據您所做出的操作來設置這些 Cookie，如設置隱私偏好、登錄或填充表格。',
    analytics: '分析 Cookie',
    analyticsDesc: '幫助我們了解訪客如何使用網站，以便改善用戶體驗。',
    marketing: '行銷 Cookie',
    marketingDesc: '用於追蹤訪客以顯示相關廣告和行銷活動。',
    preferences: '偏好 Cookie',
    preferencesDesc: '記住您的偏好設定，如語言選擇。',
    alwaysOn: '一律啟用',
    privacyPolicy: '查看隱私權政策',
    title: 'Cookie 設定',
  },
  en: {
    description: 'By clicking "Accept All", you agree to the storing of cookies on your device to enhance site navigation, analyze site usage, and assist in our marketing efforts. You can manage your cookie settings below.',
    acceptAll: 'Accept All',
    manage: 'Manage Cookies',
    settingsTitle: 'Privacy Preference Center',
    confirm: 'Confirm Selection',
    necessary: 'Necessary Cookies',
    necessaryDesc: 'These cookies are essential for the website to function properly. They are usually set in response to actions made by you, such as setting privacy preferences, logging in, or filling in forms.',
    analytics: 'Analytics Cookies',
    analyticsDesc: 'Help us understand how visitors use the website to improve user experience.',
    marketing: 'Marketing Cookies',
    marketingDesc: 'Used to track visitors to display relevant ads and marketing campaigns.',
    preferences: 'Preference Cookies',
    preferencesDesc: 'Remember your preferences such as language selection.',
    alwaysOn: 'Always On',
    privacyPolicy: 'View Privacy Policy',
    title: 'Cookie Settings',
  },
  es: {
    description: 'Al hacer clic en "Aceptar todo", usted acepta el almacenamiento de cookies en su dispositivo para mejorar la navegación del sitio, analizar el uso del sitio y ayudar en nuestros esfuerzos de marketing.',
    acceptAll: 'Aceptar Todo',
    manage: 'Gestionar Cookies',
    settingsTitle: 'Centro de Preferencias de Privacidad',
    confirm: 'Confirmar Selección',
    necessary: 'Cookies Necesarias',
    necessaryDesc: 'Estas cookies son esenciales para el funcionamiento del sitio web. No se pueden desactivar en nuestros sistemas.',
    analytics: 'Cookies de Análisis',
    analyticsDesc: 'Nos ayudan a entender cómo los visitantes usan el sitio web para mejorar la experiencia.',
    marketing: 'Cookies de Marketing',
    marketingDesc: 'Se utilizan para rastrear visitantes y mostrar anuncios y campañas relevantes.',
    preferences: 'Cookies de Preferencias',
    preferencesDesc: 'Recuerdan sus preferencias como la selección de idioma.',
    alwaysOn: 'Siempre Activo',
    privacyPolicy: 'Ver Política de Privacidad',
    title: 'Configuración de Cookies',
  }
}

/* 自訂 toggle 開關 */
function Toggle({ checked, onChange, disabled }: { checked: boolean; onChange?: (v: boolean) => void; disabled?: boolean }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      disabled={disabled}
      onClick={() => onChange?.(!checked)}
      className={`relative inline-flex h-6 w-11 shrink-0 items-center rounded-full transition-colors duration-200 ${
        disabled ? 'cursor-default' : 'cursor-pointer'
      } ${checked ? 'bg-[hsl(44,80%,40%)]' : 'bg-white/20'}`}
    >
      <span
        className={`pointer-events-none inline-block h-4 w-4 rounded-full bg-white shadow-sm transition-transform duration-200 ${
          checked ? 'translate-x-6' : 'translate-x-1'
        }`}
      />
    </button>
  )
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
      const timer = setTimeout(() => setIsVisible(true), 1000)
      return () => clearTimeout(timer)
    }
  }, [])

  const handleAcceptAll = () => {
    acceptAllCookies()
    setIsVisible(false)
    window.dispatchEvent(new CustomEvent('cookieConsentUpdated', {
      detail: { analytics: true, marketing: true, preferences: true }
    }))
  }

  const handleConfirm = () => {
    setCookieConsent(preferences)
    setIsVisible(false)
    window.dispatchEvent(new CustomEvent('cookieConsentUpdated', {
      detail: preferences
    }))
  }

  if (!isVisible) return null

  return (
    <div
      className={`fixed bottom-0 left-0 right-0 z-50 transition-transform duration-500 ${
        isVisible ? 'translate-y-0' : 'translate-y-full'
      }`}
    >
      {/* 展開的設定面板 */}
      {showDetails && (
        <div className="bg-[#1A0F0A] border-t border-white/[0.08]">
          <div className="mx-auto max-w-3xl px-6 py-6">
            <h3 className="font-heading text-lg text-white mb-1">{t.settingsTitle}</h3>
            <p className="font-body text-sm text-white/60 mb-5">{t.description}</p>

            <div className="space-y-4">
              {/* 必要 Cookie */}
              <div className="flex items-center justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2">
                    <span className="font-body text-sm font-medium text-white">{t.necessary}</span>
                    <span className="font-body text-[11px] text-[hsl(44,80%,40%)] bg-[hsl(44,80%,40%)]/10 px-2 py-0.5 rounded-full">{t.alwaysOn}</span>
                  </div>
                  <p className="font-body text-xs text-white/60 mt-0.5 leading-relaxed">{t.necessaryDesc}</p>
                </div>
                <Toggle checked={true} disabled />
              </div>

              <div className="h-px bg-white/[0.06]" />

              {/* 分析 Cookie */}
              <div className="flex items-center justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <span className="font-body text-sm font-medium text-white">{t.analytics}</span>
                  <p className="font-body text-xs text-white/60 mt-0.5">{t.analyticsDesc}</p>
                </div>
                <Toggle checked={preferences.analytics} onChange={(v) => setPreferences(p => ({ ...p, analytics: v }))} />
              </div>

              <div className="h-px bg-white/[0.06]" />

              {/* 行銷 Cookie */}
              <div className="flex items-center justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <span className="font-body text-sm font-medium text-white">{t.marketing}</span>
                  <p className="font-body text-xs text-white/60 mt-0.5">{t.marketingDesc}</p>
                </div>
                <Toggle checked={preferences.marketing} onChange={(v) => setPreferences(p => ({ ...p, marketing: v }))} />
              </div>

              <div className="h-px bg-white/[0.06]" />

              {/* 偏好 Cookie */}
              <div className="flex items-center justify-between gap-4">
                <div className="flex-1 min-w-0">
                  <span className="font-body text-sm font-medium text-white">{t.preferences}</span>
                  <p className="font-body text-xs text-white/60 mt-0.5">{t.preferencesDesc}</p>
                </div>
                <Toggle checked={preferences.preferences} onChange={(v) => setPreferences(p => ({ ...p, preferences: v }))} />
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 底部主橫幅 */}
      <div className="bg-[#2D1810] border-t border-white/[0.08] shadow-[0_-4px_20px_rgba(0,0,0,0.3)]">
        <div className="mx-auto max-w-3xl px-6 py-4">
          {!showDetails && (
            <p className="font-body text-sm text-white/50 leading-relaxed mb-4">
              {t.description}
            </p>
          )}
          <div className="flex items-center gap-3 flex-wrap">
            <button
              onClick={() => setShowDetails(!showDetails)}
              className="font-body text-sm text-[hsl(44,80%,40%)] hover:text-[hsl(44,80%,60%)] transition-colors cursor-pointer flex items-center gap-1"
            >
              {t.manage}
              <ChevronDown className={`h-3.5 w-3.5 transition-transform duration-200 ${showDetails ? 'rotate-180' : ''}`} />
            </button>
            <div className="flex-1" />
            {showDetails && (
              <button
                onClick={handleConfirm}
                className="font-body text-sm px-5 py-2 rounded-full border border-white/20 text-white hover:bg-white/[0.06] transition-colors cursor-pointer"
              >
                {t.confirm}
              </button>
            )}
            <button
              onClick={handleAcceptAll}
              className="font-body text-sm font-medium px-5 py-2 rounded-full bg-[hsl(44,80%,40%)] text-white hover:bg-[hsl(44,80%,50%)] transition-colors cursor-pointer"
            >
              {t.acceptAll}
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

/* 用於頁腳的 Cookie 設定按鈕 */
export function CookieSettingsButton() {
  const { language } = useLanguage()
  const t = translations[language]

  const handleOpenSettings = () => {
    window.dispatchEvent(new CustomEvent('openCookieSettings'))
  }

  return (
    <button
      onClick={handleOpenSettings}
      className="font-body text-sm text-white/60 hover:text-[hsl(44,80%,40%)] transition-colors cursor-pointer"
    >
      {t.title}
    </button>
  )
}
