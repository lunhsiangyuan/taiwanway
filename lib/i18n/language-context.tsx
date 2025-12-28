'use client'

import React, { createContext, useContext, useState, useCallback, useEffect } from 'react'
import { Language, translations } from './translations'

type LanguageContextType = {
  language: Language
  setLanguage: (lang: Language) => void
  t: <T = string>(key: string) => T
}

const LanguageContext = createContext<LanguageContextType | undefined>(undefined)

const LANGUAGE_STORAGE_KEY = 'taiwanway-language'

function getInitialLanguage(): Language {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem(LANGUAGE_STORAGE_KEY)
    if (stored === 'zh' || stored === 'en' || stored === 'es') {
      return stored
    }
  }
  return 'zh'
}

export function LanguageProvider({ children }: { children: React.ReactNode }) {
  const [language, setLanguageState] = useState<Language>('zh')
  const [isHydrated, setIsHydrated] = useState(false)

  useEffect(() => {
    setLanguageState(getInitialLanguage())
    setIsHydrated(true)
  }, [])

  const setLanguage = useCallback((lang: Language) => {
    setLanguageState(lang)
    if (typeof window !== 'undefined') {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, lang)
      document.documentElement.lang = lang
    }
  }, [])

  useEffect(() => {
    if (isHydrated) {
      document.documentElement.lang = language
    }
  }, [language, isHydrated])

  const t = useCallback(<T = string>(key: string): T => {
    const keys = key.split('.')
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    let value: any = translations[language]

    for (const k of keys) {
      if (value === undefined) return key as T
      value = value[k]
    }

    return (value || key) as T
  }, [language])

  return (
    <LanguageContext.Provider value={{ language, setLanguage, t }}>
      {children}
    </LanguageContext.Provider>
  )
}

export function useLanguage() {
  const context = useContext(LanguageContext)
  if (context === undefined) {
    throw new Error('useLanguage must be used within a LanguageProvider')
  }
  return context
} 