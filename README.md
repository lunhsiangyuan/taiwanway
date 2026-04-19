# TaiwanWay

A modern, multilingual restaurant website built with Next.js 15 for TaiwanWay - a Taiwanese restaurant in Middletown, NY.

## Features

- **Multi-Language Support** - Chinese, English, and Spanish with cookie-based persistence
- **GDPR-Compliant Cookie Consent** - Granular control over cookie categories
- **Analytics Integration** - Google Analytics 4, Facebook Pixel, Hotjar, Google Tag Manager
- **Responsive Design** - Mobile-first approach with Tailwind CSS
- **Menu Display** - Grid/List view modes for dishes and drinks
- **Google Maps Integration** - Embedded location map

## Tech Stack

| Category | Technology |
|----------|------------|
| Framework | Next.js 15.1.6 (App Router) |
| UI | React 19, shadcn/ui, Radix UI |
| Styling | Tailwind CSS 3.4.1 |
| Icons | Lucide React |
| Language | TypeScript |
| Deployment | Vercel |
| Images | Vercel Blob Storage |

## Getting Started

### Prerequisites

- Node.js 18.x or higher
- npm, yarn, or pnpm

### Installation

```bash
# Clone the repository
git clone [your-repo-url]
cd taiwanway

# Install dependencies
npm install

# Start development server (with Turbopack)
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Environment Variables

Create a `.env.local` file:

```bash
# Image domain (required)
NEXT_PUBLIC_IMAGE_DOMAIN=hebbkx1anhila5yf.public.blob.vercel-storage.com

# Analytics (optional)
NEXT_PUBLIC_GA_MEASUREMENT_ID=your-ga4-id
NEXT_PUBLIC_FB_PIXEL_ID=your-facebook-pixel-id
NEXT_PUBLIC_HOTJAR_ID=your-hotjar-id
NEXT_PUBLIC_GTM_ID=your-gtm-id
```

## Project Structure

```
taiwanway/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout
│   ├── page.tsx           # Home page
│   ├── menu/              # Menu page
│   ├── about/             # About page
│   └── contact/           # Contact page
├── components/            # React components
│   ├── header.tsx         # Navigation
│   ├── footer.tsx         # Footer
│   ├── cookie-consent.tsx # Cookie banner
│   ├── analytics-provider.tsx
│   └── ui/                # shadcn/ui components
├── lib/                   # Utilities
│   ├── cookies.ts         # Cookie management
│   ├── analytics.ts       # Analytics tracking
│   └── i18n/              # Internationalization
└── public/                # Static assets
```

## Available Scripts

```bash
npm run dev      # Start dev server with Turbopack
npm run build    # Build for production
npm run start    # Start production server
npm run lint     # Run ESLint
```

## Deployment

### Vercel (Recommended)

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy to production
npm run build
vercel deploy --prod
```

### Image Configuration

Ensure `next.config.js` includes your image domains:

```javascript
images: {
  remotePatterns: [
    {
      protocol: 'https',
      hostname: 'hebbkx1anhila5yf.public.blob.vercel-storage.com',
    },
  ],
}
```

## Key Features Detail

### Internationalization (i18n)

The site supports 3 languages with automatic persistence:

```typescript
import { useLanguage } from '@/lib/i18n/language-context'

const { t, language, setLanguage } = useLanguage()
return <h1>{t('hero.title')}</h1>
```

### Cookie Consent

GDPR-compliant cookie management with 4 categories:
- **Necessary** - Always enabled
- **Analytics** - GA4, Hotjar tracking
- **Marketing** - Facebook Pixel
- **Preferences** - Language settings

### Analytics

Consent-aware tracking with support for:
- Page views and custom events
- E-commerce tracking (view item, add to cart, purchase)
- Session recording (Hotjar)

## Contact

- **Address**: 26 South St, Middletown, NY
- **Phone**: 845-381-1002
- **Email**: usamyheish@gmail.com
- **Hours**: Mon/Tue/Fri/Sat 11AM-7PM

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [shadcn/ui](https://ui.shadcn.com)

## License

[MIT License](LICENSE)
