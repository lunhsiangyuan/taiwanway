This is a [Next.js](https://nextjs.org) project bootstrapped with [`create-next-app`](https://nextjs.org/docs/app/api-reference/cli/create-next-app).

## Getting Started

First, run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/app/building-your-application/optimizing/fonts) to automatically optimize and load [Geist](https://vercel.com/font), a new font family for Vercel.

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.

## 專案特色 Features

### 核心架構
- 使用 Next.js App Router
- 整合 shadcn/ui 組件庫 (New York style)
- Tailwind CSS 樣式系統搭配自定義主題
- 多語言支援 (中英雙語介面)

### 主要功能
- 響應式導航列與行動選單
- 菜單錨點滾動定位
- 雙模式菜單顯示 (Grid/List)
- Google 地圖整合
- Vercel Blob 圖片托管

## 技術棧 Tech Stack
- **Framework**: Next.js 14
- **Styling**: Tailwind CSS + CSS Variables
- **UI Library**: shadcn/ui + Radix UI
- **Icons**: Lucide React
- **Deployment**: Vercel
- **Image Hosting**: Vercel Blob Storage

## 組件結構
components/
├── header.tsx # 導航列與行動選單
├── hero.tsx # 首頁大圖區塊
├── menu-section.tsx # 菜單區塊 (雙模式核心邏輯)
├── contact-map.tsx # Google 地圖嵌入
├── ui/ # shadcn/ui 客製化組件
└── ... # 其他業務組件

## 部署指南 Deployment
1. Vercel 環境變數設定：

```bash
NEXT_PUBLIC_IMAGE_DOMAIN=hebbkx1anhila5yf.public.blob.vercel-storage.com
```
2. 圖片託管需搭配 Vercel Blob Storage
3. 使用 Next.js 靜態生成：
```bash
npm run build && vercel --prod
```

## 樣式規範
- 主色調：`hsl(10 65% 45%)` (紅色系)
- 字體：Geist (透過 `next/font` 自動優化)
- 動畫：`tailwindcss-animate` 插件
