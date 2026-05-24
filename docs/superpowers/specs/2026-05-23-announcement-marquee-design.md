# 首頁店休公告跑馬燈 — 設計 Spec

**日期**：2026-05-23
**目標**：在 TaiwanWay 官網首頁加一條跑馬燈，公告 2026-06-01 至 2026-08-13 暫停營業。
**自動下架日**：2026-08-13 後不再顯示。

## 背景

店家將於 2026-06-01 至 2026-08-13 暫停營業，需要讓首頁訪客在進站第一眼就看到。要求醒目但不過度干擾。

## 範圍

**做：**
- 新增 `AnnouncementMarquee` 元件，放在首頁 `<Hero />` 之上
- 三語文案（zh / en / es）
- CSS-only 橫向跑馬燈動畫
- 過了 2026-08-13 自動隱藏

**不做（YAGNI）：**
- 不做關閉按鈕、不寫 cookie 記憶
- 不放到其他頁面（菜單、聯絡、關於）
- 不使用第三方 marquee 套件
- 不做後台可編輯（直接寫死在翻譯檔）

## 架構

### 新檔案

`components/announcement-marquee.tsx`
- `'use client'` 元件（需用 i18n context）
- 內部邏輯：
  1. 從 `useLanguage()` 取 `t('announcement.closure')`
  2. 比對當天日期，若 `new Date() > 2026-08-14T00:00:00` 則 `return null`
  3. 渲染琥珀色橫條 + 跑馬燈內容
- 無障礙：`role="status"` + `aria-live="polite"`
- 動畫：`prefers-reduced-motion: reduce` 時改靜態顯示（不滾動）

### 修改檔案

1. `lib/i18n/translations.ts`
   - 新增 key：`announcement.closure`
   - zh：「📢 公告｜本店將於 6/1 至 8/13 暫停營業，8/14 起恢復正常營業時間。感謝您的支持！」
   - en：「📢 Notice: We will be closed from June 1 to August 13. We'll reopen on August 14. Thank you for your support!」
   - es：「📢 Aviso: Estaremos cerrados del 1 de junio al 13 de agosto. Reabriremos el 14 de agosto. ¡Gracias por su apoyo!」

2. `app/page.tsx`
   - import `AnnouncementMarquee`
   - 插在 `<main>` 內最頂、`<Hero />` 之上

3. `app/globals.css`（或元件內 `<style jsx>`）
   - 加 `@keyframes marquee-scroll`：`transform: translateX(0) → translateX(-50%)`（因為渲染兩份文字並列，滾動半個 track 就接續無縫）
   - 一輪時長：20 秒，linear，無限循環
   - hover 時 `animation-play-state: paused`

## 視覺規格

- 高度：40px（`h-10`）
- 背景：`bg-amber-500`
- 文字：`text-amber-950 font-medium`
- 內容渲染兩份（並列），讓滾動無縫接續
- 整頁寬，不 sticky（會跟著首頁向上捲走）

## 元件草圖

```tsx
'use client'

import { useLanguage } from '@/lib/i18n/language-context'

const CLOSURE_END = new Date('2026-08-14T00:00:00')

export function AnnouncementMarquee() {
  const { t } = useLanguage()
  if (new Date() >= CLOSURE_END) return null

  const text = t('announcement.closure')

  return (
    <div
      role="status"
      aria-live="polite"
      className="overflow-hidden bg-amber-500 text-amber-950 h-10 flex items-center"
    >
      <div className="marquee-track whitespace-nowrap font-medium">
        <span className="px-8">{text}</span>
        <span className="px-8" aria-hidden="true">{text}</span>
      </div>
    </div>
  )
}
```

CSS：
```css
.marquee-track {
  display: inline-flex;
  animation: marquee-scroll 20s linear infinite;
}
.marquee-track:hover {
  animation-play-state: paused;
}
@keyframes marquee-scroll {
  from { transform: translateX(0); }
  to { transform: translateX(-50%); }
}
@media (prefers-reduced-motion: reduce) {
  .marquee-track {
    animation: none;
    justify-content: center;
    width: 100%;
  }
}
```

## 測試計畫

1. `npm run dev` 啟動，確認首頁頂部出現黃色跑馬燈
2. 切換語言（zh/en/es），確認文字三語都正確
3. hover 時動畫暫停
4. 在 macOS 系統偏好設定關閉動畫（或 DevTools 模擬 reduced-motion），確認改為靜態置中
5. DevTools console 暫時把 `CLOSURE_END` 改為過去日期，驗證自動隱藏邏輯
6. 響應式：手機寬度（375px）下文字仍可讀、不破版

## 驗收標準

- [ ] 首頁載入第一眼看到黃色公告橫條
- [ ] 三語切換顯示對應文字
- [ ] 過了 2026-08-13 自動不顯示
- [ ] 其他頁面（/menu, /about, /contact）不顯示
- [ ] Lighthouse 無障礙分數不下降
