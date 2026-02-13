#!/usr/bin/env bun
/**
 * 處理 Dropbox 產品照片：複製、優化、轉換為 WebP
 *
 * 功能：
 * 1. 從 Dropbox 複製高品質產品照片
 * 2. 轉換為 WebP 格式（減少 60-80% 檔案大小）
 * 3. 生成多種尺寸：
 *    - hero: 2880px（主視覺）
 *    - product: 800px（產品頁）
 *    - thumbnail: 400px（縮圖）
 * 4. 保留原始 JPG 備份
 */

import sharp from 'sharp';
import { copyFileSync, existsSync, mkdirSync, readdirSync } from 'fs';
import { join } from 'path';

// 設定路徑
const DROPBOX_DIR = `${process.env.HOME}/Dropbox/Ubereats 照片拷貝`;
const PROJECT_DIR = join(import.meta.dir, '..');
const OUTPUT_DIR = join(PROJECT_DIR, 'public', 'images', 'products');
const BACKUP_DIR = join(PROJECT_DIR, 'public', 'images', 'originals');

// 圖片尺寸配置
const SIZES = {
  hero: { width: 2880, quality: 90 },      // 主視覺圖（Hero）
  product: { width: 800, quality: 85 },    // 產品頁
  thumbnail: { width: 400, quality: 80 },  // 縮圖
};

// 產品照片映射（Dropbox 檔名 → 網站檔名）
const IMAGE_MAPPING: Record<string, string> = {
  'Taiwanway_BeefNoodleSoup_2880x2304.jpg': 'beef-noodle-soup',
  'Taiwanway_BraisedPorkRice_2880x2304.jpg': 'braised-pork-rice',
  'Taiwanway_BrownSugarBubbleMilk_2880x2304.jpg': 'brown-sugar-bubble-milk',
  'Taiwanway_BubbleTeaHot_2880x2304.jpg': 'bubble-tea-hot',
  'Taiwanway_Hero_2880x2304.jpg': 'hero',
  'Taiwanway_HoneyJasmineGreenTea_2880x2304.jpg': 'honey-jasmine-green-tea',
  'Taiwanway_HoneyOolongBubbleTea_2880x2304.jpg': 'honey-oolong-bubble-tea',
  'Taiwanway_JasmineGreenBubbleTea_2880x2304.jpg': 'jasmine-green-bubble-tea',
  'Taiwanway_JasmineGreenMilkTea_2880x2304.jpg': 'jasmine-green-milk-tea',
  'Taiwanway_MangoCocounutPannacotta_2880x2304.jpg': 'mango-coconut-pannacotta',
  'Taiwanway_TaiwaneseMilkTea_2880x2304.jpg': 'taiwanese-milk-tea',
  'Taiwanway_TaroPannacotta_2880x2304.jpg': 'taro-pannacotta',
  'Taiwanway_TeaCake_2880x2304.jpg': 'tea-cake',
  'Taiwanway_WinterMelonLemonade_2880x2304.jpg': 'winter-melon-lemonade',
};

/**
 * 處理單張圖片：轉換為 WebP 並生成多種尺寸
 */
async function processImage(
  sourcePath: string,
  outputName: string
): Promise<void> {
  console.log(`\n  處理: ${outputName}`);

  // 1. 備份原始檔案
  const backupPath = join(BACKUP_DIR, `${outputName}.jpg`);
  if (!existsSync(backupPath)) {
    copyFileSync(sourcePath, backupPath);
    console.log(`    ✓ 備份: ${outputName}.jpg`);
  }

  // 2. 讀取原始圖片
  const image = sharp(sourcePath);
  const metadata = await image.metadata();
  console.log(`    原始尺寸: ${metadata.width}×${metadata.height}`);

  // 3. 生成不同尺寸的 WebP 圖片
  for (const [sizeName, config] of Object.entries(SIZES)) {
    const outputPath = join(OUTPUT_DIR, `${outputName}-${sizeName}.webp`);

    await image
      .resize(config.width, null, {
        fit: 'inside',
        withoutEnlargement: true,
      })
      .webp({ quality: config.quality })
      .toFile(outputPath);

    const stats = await Bun.file(outputPath).size;
    const sizeMB = (stats / 1024 / 1024).toFixed(2);
    console.log(`    ✓ ${sizeName}: ${config.width}px → ${sizeMB}MB`);
  }
}

/**
 * 主程式
 */
async function main() {
  console.log('═'.repeat(60));
  console.log('TaiwanWay 產品照片處理');
  console.log(`來源: ${DROPBOX_DIR}`);
  console.log(`輸出: ${OUTPUT_DIR}`);
  console.log('═'.repeat(60));

  // 檢查來源目錄
  if (!existsSync(DROPBOX_DIR)) {
    console.error(`\n❌ 找不到 Dropbox 資料夾: ${DROPBOX_DIR}`);
    process.exit(1);
  }

  // 創建輸出目錄
  mkdirSync(OUTPUT_DIR, { recursive: true });
  mkdirSync(BACKUP_DIR, { recursive: true });

  // 處理所有圖片
  let processed = 0;
  let skipped = 0;

  for (const [sourceFile, outputName] of Object.entries(IMAGE_MAPPING)) {
    const sourcePath = join(DROPBOX_DIR, sourceFile);

    if (!existsSync(sourcePath)) {
      console.log(`\n  ⚠️  跳過（找不到檔案）: ${sourceFile}`);
      skipped++;
      continue;
    }

    try {
      await processImage(sourcePath, outputName);
      processed++;
    } catch (error) {
      console.error(`\n  ❌ 處理失敗: ${sourceFile}`, error);
      skipped++;
    }
  }

  // 摘要報告
  console.log('\n' + '═'.repeat(60));
  console.log(`結果: ${processed} 成功, ${skipped} 跳過`);
  console.log('═'.repeat(60));

  // 列出生成的檔案
  console.log('\n生成的檔案：');
  const files = readdirSync(OUTPUT_DIR).filter(f => f.endsWith('.webp'));
  console.log(`  總共 ${files.length} 個 WebP 檔案`);

  process.exit(skipped > 0 ? 1 : 0);
}

// 執行
main().catch(console.error);
