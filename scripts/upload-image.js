import { put } from '@vercel/blob';
import { readFileSync } from 'fs';
import path from 'path';

async function uploadImage() {
  try {
    const imagePath = path.join(process.cwd(), 'public', '鳳梨酥.jpeg');
    const imageBuffer = readFileSync(imagePath);
    
    const blob = await put('pineapple-cake.jpg', imageBuffer, {
      access: 'public',
      addRandomSuffix: true,
    });

    console.log('Image uploaded successfully!');
    console.log('URL:', blob.url);
  } catch (error) {
    console.error('Error uploading image:', error);
  }
}

uploadImage(); 