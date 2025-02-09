import { put } from '@vercel/blob';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const BLOB_TOKEN = "vercel_blob_rw_06jFzz4mAEKXLl04_de0hBFr91YN1CaU2X29S4jyrA3CKvF";

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