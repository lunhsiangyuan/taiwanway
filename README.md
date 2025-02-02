# TaiwanWay 網站專案

這是一個使用 Next.js 14+ 開發的現代化餐廳網站。

## 專案架構

### 核心技術
- Framework: Next.js 14+ (App Router)
- 樣式: Tailwind CSS + CSS Variables
- UI 元件: shadcn/ui (New York style)
- 圖示: Lucide React
- 部署: Vercel
- 圖片儲存: Vercel Blob Storage

### 目錄結構
```
components/
├── header.tsx          # 導航列與行動選單
├── hero.tsx           # 首頁大圖區塊
├── menu-section.tsx    # 菜單區塊
├── contact-map.tsx    # Google Maps 整合
├── ui/               # shadcn/ui 客製化元件
└── [其他業務元件]
```

## 快速開始

### 環境要求
- Node.js 18.x 或更高版本
- npm 或 yarn 或 pnpm

### 安裝步驟
1. 複製專案
```bash
git clone [your-repo-url]
cd taiwanway
```

2. 安裝依賴
```bash
npm install
# 或
yarn install
# 或
pnpm install
```

3. 設定環境變數
```bash
# .env.local
NEXT_PUBLIC_IMAGE_DOMAIN=hebbkx1anhila5yf.public.blob.vercel-storage.com
```

4. 啟動開發伺服器
```bash
npm run dev
# 或
yarn dev
# 或
pnpm dev
```

5. 開啟瀏覽器訪問 http://localhost:3000

## 部署指南

### Vercel 部署
1. 安裝 Vercel CLI
```bash
npm install -g vercel
```

2. 部署到生產環境
```bash
npm run build
vercel deploy --prod
```

### 常見問題排除

#### 建置錯誤處理
如果遇到 TypeScript 或 ESLint 錯誤，可以在 `next.config.js` 中暫時關閉檢查：
```javascript
const nextConfig = {
  eslint: {
    ignoreDuringBuilds: true,
  },
  typescript: {
    ignoreBuildErrors: true,
  }
};
```

#### 圖片載入問題
確保在 `next.config.js` 中正確配置 `images.remotePatterns`：
```javascript
images: {
  remotePatterns: [
    {
      protocol: 'https',
      hostname: 'hebbkx1anhila5yf.public.blob.vercel-storage.com',
    },
    {
      protocol: 'https',
      hostname: 'www.ganjingworld.com',
    },
  ],
}
```

#### 樣式相關問題
1. 確保 Tailwind CSS 配置正確
2. 檢查 shadcn/ui 主題設定
3. 確認 CSS Variables 是否正確載入

## 主要功能
- 響應式導航列
- 雙語系支援（中/英）
- 菜單展示（Grid/List 模式）
- Google Maps 整合
- 圖片最佳化

## 開發注意事項
1. 使用 `next/image` 替代原生 `<img>` 標籤
2. 確保所有頁面都支援響應式設計
3. 遵循 TypeScript 型別定義
4. 使用 CSS Variables 進行主題設定

## 維護指南
- 定期更新依賴套件
- 檢查 Vercel 部署日誌
- 監控圖片儲存空間使用量
- 定期備份資料

## 授權
[授權說明]

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
- 地圖尺寸：
  - 桌面版：高度至少 500px (使用 min-h-[500px])
  - 行動版：保持原有響應式設計

## 地圖組件設定
為了讓桌面版的地圖顯示更大，建議在 contact-map.tsx 中加入以下樣式：
```tsx
<div className="w-full min-h-[500px] md:min-h-[600px]">
  {/* Google Map iframe */}
</div>
```

## Learn More

To learn more about Next.js, take a look at the following resources:

- [Next.js Documentation](https://nextjs.org/docs) - learn about Next.js features and API.
- [Learn Next.js](https://nextjs.org/learn) - an interactive Next.js tutorial.

You can check out [the Next.js GitHub repository](https://github.com/vercel/next.js) - your feedback and contributions are welcome!

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/app/building-your-application/deploying) for more details.
