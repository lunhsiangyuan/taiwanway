# TaiwanWay 首頁改版設計紀錄（可讀性 + 品牌一致）

日期：2026-07-05　分支：`redesign-homepage`

## 目標
讓新客一眼就懂「這是什麼店 + 該做什麼」，並解決兩個明確抱怨：
1. 字標（Playfair 全大寫）難看
2. 深色背景區塊文字看不清

## 定位（使用者確認）
位於紐約 Middletown 的**家鄉味台式咖啡館** — 牛肉麵、滷肉飯、珍珠奶茶，來自家鄉的溫暖風味。
品牌副標：SNACKS · CAFE · BAKERY。台灣零食伴手禮獨立成區、不與正餐混雜。

## 一句話方向
明亮白／米底 ＋ 磚紅 logo 品牌 ＋ 大張真實食物照片 ＋ 厚實好讀的字。
（保留餐廳食慾感與溫度，補上好讀與清楚動線；英文為主、中文並存。）

## 視覺系統（依 logo 定調）
- 主色：磚紅（取自 logo，約 `hsl(8 60% 45%)`）
- 背景：暖米白 / 白
- 標題字：Zilla Slab（厚實 slab，呼應 logo 的 TAIWAN WAY 字）
- 內文字：Noto Sans TC / Karla（清楚無襯線，字級加大、行距加寬、對比加強）
- 深色不可讀區塊 → 一律改亮底

## Logo 配置
- `LOGO-B`（橫式文字）→ 頁首 Header、頁尾 Footer
- `LOGO-A`（小女孩直式）→ 首頁 Hero 主視覺
- 小女孩臉 → favicon、手機選單、段落點綴
- 檔案：`public/brand/logo-horizontal.png`、`public/brand/logo-mascot.png`

## 首頁段落順序（Before → After）
1. Hero：食物大圖為主 + LOGO-A + 一句定位；**主按鈕＝看菜單**、次按鈕＝訂餐外送
2. 資訊條：營業時間 / 地址 / 電話（新客最想知道的，一眼可見）
3. 招牌雙主軸 / 招牌菜卡片：真實食物照片 + 菜名 + 一句話 + 價格
4. 台灣零食「帶回家」獨立區
5. 店的故事（濃縮 2–3 句；完整移 About）
6. 地圖 + 營業時間 + 聯絡收尾

## Hero 主按鈕決定
主按鈕＝**看菜單**（使用者選）；訂餐外送 Uber Eats / DoorDash 為次要。

## 真實素材
- 食物照片：`public/images/food/`（牛肉麵、滷肉飯、雞肉飯、珍珠抹茶拿鐵、黑糖珍奶、蜜香烏龍、鳳梨酥、抹茶巴斯克、茶蛋糕）
- 店家資訊：26 South St, Middletown, NY 10940｜(845) 381-1002｜Mon·Tue·Fri·Sat 11AM–7PM｜Uber Eats + DoorDash

## 做法
先做首頁最關鍵的「品牌色/字型 + 頁首 + Hero」，截圖給使用者確認方向，再往下做整頁其他段落，最後套用到其他頁面。線上站不動，全部在 `redesign-homepage` 分支。
