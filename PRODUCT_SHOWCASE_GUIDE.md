# TaiwanWay 產品展示系統使用指南

## 概述

全新的產品展示系統模仿春水堂官網設計風格，提供專業、優雅的產品呈現方式。

## ✨ 主要特色

### 1. 春水堂風格設計
- **大圖置頂**：使用 WebP 優化圖片，快速載入
- **多語言支援**：中文、英文、西班牙文
- **分類標籤**：熱飲、冷飲、辣、甜點等
- **詳細描述**：50-80 字故事性文字，突顯食材、烹飪方式、口感
- **過敏原資訊**：清楚標示潛在過敏原
- **備註說明**：「圖片僅供參考」等專業提示

### 2. 圖片優化系統
- **三種尺寸**：
  - Hero (2880px): 主視覺圖
  - Product (800px): 產品頁面
  - Thumbnail (400px): 縮圖
- **WebP 格式**：比 JPG/PNG 減少 60-80% 檔案大小
- **備份原檔**：原始 JPG 保存在 `public/images/originals/`

### 3. 彈性展示模式
- **Grid 視圖**：4 欄網格（響應式）
- **List 視圖**：橫向卡片，更詳細的資訊
- **平滑捲動**：點擊分類自動捲動到該區域
- **Sticky 導航**：分類按鈕固定在頂部

## 📁 檔案結構

```
taiwanway/
├── lib/
│   └── menu-data.ts              # 產品數據（14 個產品）
├── components/
│   ├── product-card.tsx          # 產品卡片組件
│   └── products-showcase.tsx     # 產品展示頁面
├── scripts/
│   └── process-product-images.ts # 圖片處理腳本
└── public/
    └── images/
        ├── products/             # 優化的 WebP 圖片（42 個）
        └── originals/            # 原始 JPG 備份（14 個）
```

## 🎨 產品數據結構

```typescript
interface Product {
  id: string;                     // 唯一識別碼
  category: string;               // 分類（main-dishes, bubble-tea 等）
  image: {
    hero: string;                 // 2880px WebP
    product: string;              // 800px WebP
    thumbnail: string;            // 400px WebP
  };
  name: {
    zh: string;                   // 中文名稱
    en: string;                   // 英文名稱
    es?: string;                  // 西班牙文名稱
  };
  tags: string[];                 // 標籤（熱飲、冷飲、辣等）
  description: {
    zh: string;                   // 中文描述
    en: string;                   // 英文描述
    es?: string;                  // 西班牙文描述
  };
  price?: number;                 // 價格（USD）
  allergens?: string[];           // 過敏原列表
}
```

## 🚀 使用方式

### 瀏覽產品
1. 訪問 `http://localhost:3000/menu`
2. 使用頂部分類按鈕快速導航
3. 切換 Grid/List 視圖模式
4. 滾動瀏覽所有產品

### 添加新產品
1. 將產品照片放入 `~/Dropbox/Ubereats 照片拷貝/`
2. 更新 `scripts/process-product-images.ts` 的 `IMAGE_MAPPING`
3. 執行圖片處理：
   ```bash
   bun run scripts/process-product-images.ts
   ```
4. 編輯 `lib/menu-data.ts`，添加產品資料：
   ```typescript
   {
     id: 'product-name',
     category: CATEGORIES.BUBBLE_TEA,
     image: {
       hero: '/images/products/product-name-hero.webp',
       product: '/images/products/product-name-product.webp',
       thumbnail: '/images/products/product-name-thumbnail.webp',
     },
     name: { zh: '產品名稱', en: 'Product Name' },
     tags: ['冷飲'],
     description: {
       zh: '詳細描述...',
       en: 'Detailed description...',
     },
     price: 5.95,
     allergens: ['乳製品'],
   }
   ```

### 修改現有產品
直接編輯 `lib/menu-data.ts` 中的對應產品物件即可。

## 🎯 目前產品列表

### 主餐 (2 項)
- 牛肉麵 ($12.95)
- 滷肉飯 ($9.95)

### 珍珠奶茶系列 (4 項)
- 黑糖珍珠鮮奶 ($6.45)
- 招牌珍珠奶茶（熱）($5.95)
- 茉香綠茶珍珠 ($5.95)
- 蜜香烏龍珍珠 ($6.45)

### 奶茶系列 (2 項)
- 台式奶茶 ($4.95)
- 茉香綠奶茶 ($5.45)

### 綠茶系列 (1 項)
- 蜂蜜茉香綠茶 ($5.95)

### 檸檬飲品 (1 項)
- 冬瓜檸檬 ($5.45)

### 甜點 (3 項)
- 芒果椰香奶酪 ($5.95)
- 芋頭奶酪 ($5.95)
- 茶點糕 ($4.95)

## 📊 圖片處理腳本

`scripts/process-product-images.ts` 提供自動化圖片優化：

### 功能
- ✅ 從 Dropbox 複製照片
- ✅ 轉換為 WebP 格式
- ✅ 生成三種尺寸
- ✅ 備份原始檔案
- ✅ 詳細處理報告

### 執行方式
```bash
cd ~/Projects/taiwanway
bun run scripts/process-product-images.ts
```

### 範例輸出
```
════════════════════════════════════════════════════════════
TaiwanWay 產品照片處理
來源: /Users/lunhsiangyuan/Dropbox/Ubereats 照片拷貝
輸出: /Users/lunhsiangyuan/Projects/taiwanway/public/images/products
════════════════════════════════════════════════════════════

  處理: beef-noodle-soup
    ✓ 備份: beef-noodle-soup.jpg
    原始尺寸: 2880×2304
    ✓ hero: 2880px → 0.62MB
    ✓ product: 800px → 0.07MB
    ✓ thumbnail: 400px → 0.02MB

════════════════════════════════════════════════════════════
結果: 14 成功, 0 跳過
════════════════════════════════════════════════════════════
```

## 🎨 設計參考

### 春水堂特色元素
1. **大圖優先**：視覺吸引力
2. **多語言呈現**：國際化體驗
3. **分類清晰**：易於導航
4. **描述豐富**：故事性文字
5. **專業備註**：品質保證

### 色彩方案
- **主色調**：Amber 600 (#D97706) - 溫暖、親切
- **背景色**：Gray 50 - 淺灰底色
- **卡片底色**：White - 純白卡片
- **文字色**：Gray 900/700 - 高對比度

## 🔧 技術細節

### 響應式設計
- **手機版**：1 欄
- **平板版**：2 欄
- **桌面版**：3-4 欄
- **大螢幕**：4 欄

### 效能優化
- **WebP 格式**：現代瀏覽器支援
- **圖片懶載入**：Next.js Image 自動處理
- **尺寸適配**：根據視窗寬度載入適當尺寸
- **快取策略**：瀏覽器快取 + CDN

### 無障礙性
- **Alt 文字**：所有圖片都有描述
- **語意化 HTML**：正確使用標籤
- **鍵盤導航**：完整支援
- **對比度**：符合 WCAG AA 標準

## 📝 維護建議

### 圖片管理
- 定期清理未使用的圖片
- 保持 Dropbox 資料夾整潔
- 使用一致的命名規範

### 內容更新
- 季節性更新產品描述
- 定期檢查價格
- 保持多語言翻譯同步

### 效能監控
- 使用 Lighthouse 檢測效能
- 監控圖片載入時間
- 優化 LCP (Largest Contentful Paint)

## 🚀 未來計劃

- [ ] 產品詳情頁（點擊產品查看完整資訊）
- [ ] 搜尋功能（按名稱、標籤搜尋）
- [ ] 篩選功能（過濾過敏原、價格範圍）
- [ ] 收藏功能（儲存喜愛的產品）
- [ ] 購物車整合
- [ ] 評價系統
- [ ] 相關產品推薦

## 🎉 完成！

您的 TaiwanWay 網站現在擁有專業的產品展示系統，模仿春水堂的設計風格，提供優質的用戶體驗！

訪問 http://localhost:3000/menu 查看效果。
