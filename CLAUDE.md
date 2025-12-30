# CLAUDE.md - AI Assistant Context for TaiwanWay

This file provides context for AI assistants working on the TaiwanWay restaurant website project.

## Project Overview

TaiwanWay is a modern restaurant website for a Taiwanese restaurant located in Middletown, NY. The site showcases their menu, provides business information, and supports multiple languages.

## Tech Stack

- **Framework**: Next.js 15.1.6 (App Router with Turbopack)
- **React**: 19.0.0
- **Styling**: Tailwind CSS 3.4.1 + CSS Variables
- **UI Components**: shadcn/ui (New York style) + Radix UI
- **Icons**: Lucide React
- **Language**: TypeScript (strict mode)
- **Deployment**: Vercel
- **Image Hosting**: Vercel Blob Storage

## Directory Structure

```
taiwanway/
├── app/                    # Next.js App Router pages
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Home page
│   ├── menu/page.tsx      # Menu page
│   ├── about/page.tsx     # About page
│   └── contact/page.tsx   # Contact page
├── components/            # React components
│   ├── header.tsx         # Navigation with language switcher
│   ├── footer.tsx         # Footer with contact info
│   ├── hero.tsx           # Hero section
│   ├── menu-*.tsx         # Menu-related components
│   ├── drinks-list.tsx    # Drinks menu (7 categories)
│   ├── contact-*.tsx      # Contact page components
│   ├── about-*.tsx        # About page components
│   ├── cookie-consent.tsx # GDPR cookie banner
│   ├── analytics-provider.tsx # Analytics integration
│   └── ui/                # shadcn/ui components
├── lib/                   # Utility libraries
│   ├── cookies.ts         # Cookie management system
│   ├── analytics.ts       # Multi-platform analytics
│   ├── utils.ts           # Utility functions (cn)
│   └── i18n/              # Internationalization
│       ├── language-context.tsx
│       └── translations.ts
└── public/                # Static assets
```

## Key Features

### 1. Multi-Language Support (i18n)
- **Languages**: Chinese (zh), English (en), Spanish (es)
- **Implementation**: React Context with cookie-based persistence
- **Usage**:
  ```typescript
  const { t, language, setLanguage } = useLanguage()
  <h1>{t('section.key')}</h1>
  ```
- **Translations file**: `lib/i18n/translations.ts` (750+ lines)

### 2. Cookie Consent System (GDPR)
- **Cookie types**: necessary, analytics, marketing, preferences
- **Utilities**: `lib/cookies.ts` provides setCookie, getCookie, deleteCookie, consent management
- **UI**: `components/cookie-consent.tsx` - Bilingual banner with customization options

### 3. Analytics Integration
- **Platforms**: Google Analytics 4, Facebook Pixel, Hotjar, Google Tag Manager
- **Consent-aware**: Only initializes after user consent
- **E-commerce tracking**: View item, add to cart, checkout, purchase events
- **Environment variables**:
  ```
  NEXT_PUBLIC_GA_MEASUREMENT_ID
  NEXT_PUBLIC_FB_PIXEL_ID
  NEXT_PUBLIC_HOTJAR_ID
  NEXT_PUBLIC_GTM_ID
  ```

### 4. Menu System
- Main dishes (Beef Noodle Soup, Braised Pork Rice, etc.)
- Drinks (7 categories, 20+ items including bubble tea)
- Desserts (Taiwan Pineapple Cake)
- Grid/List view modes

## Development Commands

```bash
npm run dev      # Start dev server with Turbopack
npm run build    # Production build
npm run start    # Start production server
npm run lint     # ESLint checking
```

## Important Patterns

### Component Translation Pattern
```typescript
'use client'
import { useLanguage } from '@/lib/i18n/language-context'

export function MyComponent() {
  const { t } = useLanguage()
  return <h1>{t('page.title')}</h1>
}
```

### Analytics Tracking Pattern
```typescript
import { trackEvent, hasConsent } from '@/lib/analytics'

// Always checks consent before tracking
trackMenuView('drinks')
trackContact('form_submit')
```

### Cookie Management Pattern
```typescript
import { setCookie, getCookie, hasConsent } from '@/lib/cookies'

// Check consent before setting non-essential cookies
if (hasConsent('analytics')) {
  setCookie('tracking_id', 'value', { expires: 365 })
}
```

## Configuration Files

### next.config.js
- Image remote patterns for Vercel Blob Storage
- Allowed domains: hebbkx1anhila5yf.public.blob.vercel-storage.com, 06jfzz4maekxll04.public.blob.vercel-storage.com, www.ganjingworld.com

### tailwind.config.ts
- Dark mode: class-based
- Custom colors via CSS variables
- Animation plugin enabled

## Business Information

- **Restaurant**: TaiwanWay
- **Address**: 26 South St, Middletown, NY
- **Phone**: 845-381-1002
- **Email**: usamyheish@gmail.com
- **Hours**: Mon/Tue/Fri/Sat 11AM-7PM

## Common Tasks

### Adding a new translation
1. Add keys to `lib/i18n/translations.ts` for all 3 languages (zh, en, es)
2. Use `t('your.key')` in components

### Adding a new menu item
1. Add to `lib/i18n/translations.ts` under `menu.mainDishes` or relevant section
2. Update the corresponding component (main-dishes.tsx, drinks-list.tsx, etc.)

### Adding a new page
1. Create folder in `app/` with `page.tsx`
2. Add navigation links to `components/header.tsx`
3. Add translations for page content

### Modifying analytics
1. Update `lib/analytics.ts` for new tracking functions
2. Ensure consent checks are in place
3. Add environment variables if needed

## Notes for AI Assistants

- All components are client-side ('use client') due to i18n context
- Always use `next/image` for images, never raw `<img>` tags
- Follow existing translation patterns when adding new text
- Check cookie consent before implementing any tracking
- The site is bilingual-first (Chinese primary, English secondary)
- Use Tailwind CSS classes, avoid inline styles
- Test responsive design (mobile-first approach)
