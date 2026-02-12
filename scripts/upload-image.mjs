import { put } from '@vercel/blob';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const BLOB_TOKEN = process.env.BLOB_READ_WRITE_TOKEN;
if (!BLOB_TOKEN) {
  console.error('錯誤: 請設定環境變數 BLOB_READ_WRITE_TOKEN');
  process.exit(1);
}

async function uploadImage() {
  try {
    const imagePath = join(dirname(__dirname), 'public', '鳳梨酥.jpeg');
    const imageBuffer = readFileSync(imagePath);

    const blob = await put('pineapple-cake.jpg', imageBuffer, {
      access: 'public',
      addRandomSuffix: true,
      token: BLOB_TOKEN
    });

    console.log('Image uploaded successfully!');
    console.log('URL:', blob.url);
  } catch (error) {
    console.error('Error uploading image:', error);
  }
}

uploadImage(); 