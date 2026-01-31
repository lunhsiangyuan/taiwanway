# Findings & Decisions

## Requirements
### 團購功能需求 (已確認)
- **核心功能**: 客人填表單訂購 → 同步到 Google Sheets → 店家管理訂單
- **分支**: feature/group-buy-google-sync
- **商品類型**:
  - 常態商品 (每天): 主餐、飲料
  - 不定期商品: 禮盒、台灣直進物品
- **運作方式**:
  - 常態商品: 持續接單，每天結算
  - 特殊商品: 限時團購，有截止時間
- **取貨方式**: 到店自取
- **付款方式**:
  - 第一階段: 到店付款
  - 未來: 加入線上預付 (Square Online)
- **表單欄位**: 姓名、電話、Email、取貨時間、備註

### 其他待辦
- CLAUDE.md 待辦: Analytics 環境變數設定
- 改善報告建議: 產品照片、線上訂餐、CTA 按鈕等

## 現有功能 (已完成)
- 多語言支援 (中/英/西)
- GDPR Cookie 同意系統
- 多平台分析追蹤 (GA4, FB Pixel, Hotjar, GTM)
- 菜單頁面 (主餐、飲料、甜點)
- 響應式設計
- Square POS 整合基礎

## 改善建議報告摘要 (2025-12-29)
1. **首頁優化**: Hero 區域增加醒目的 CTA 按鈕
2. **菜單頁面**: 為每道菜品添加高質量照片
3. **線上訂餐**: 整合外送平台或建立訂餐系統
4. **多語言**: 語言切換功能更顯眼 (已實作)
5. **關於頁面**: 加入團隊照片、店面環境照
6. **社群整合**: Instagram 動態牆、Google/Yelp 評價
7. **SEO 優化**: 結構化資料 (已實作 JSON-LD)
8. **其他**: 最新消息區塊、會員計畫、預約功能

## Technical Decisions
| Decision | Rationale |
|----------|-----------|
| Next.js 15 App Router | 現有技術棧 |
| Tailwind CSS | 現有樣式方案 |
| shadcn/ui | 現有 UI 元件庫 |

## Issues Encountered
| Issue | Resolution |
|-------|------------|
| (尚無) | - |

## Resources
- 專案位置: ~/Projects/taiwanway
- 部署平台: Vercel
- 圖片存儲: Vercel Blob Storage
- POS 系統: Square API

## Visual/Browser Findings
<!-- 待更新 -->
-

---
*Update this file after every 2 view/browser/search operations*
