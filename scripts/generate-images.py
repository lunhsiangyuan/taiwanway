#!/usr/bin/env python3
"""
使用 Gemini API 生成 TaiwanWay 網站所需圖片
"""
import os
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

# 設定 API
API_KEY = "AIzaSyDHwneH3Z99JHfyY76ufDVQSrO-6eZP0OA"
client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = Path(__file__).parent.parent / "public" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 定義需要生成的圖片
IMAGE_PROMPTS = [
    {
        "name": "hero-bg",
        "prompt": (
            "A stunning overhead shot of an authentic Taiwanese food spread on a dark wooden table. "
            "Include steaming beef noodle soup, bubble milk tea, braised pork rice, gua bao, "
            "and pineapple cakes arranged artistically. Warm ambient lighting with golden tones, "
            "soft bokeh background. Professional food photography, high-end restaurant quality, "
            "moody and inviting atmosphere. Cinematic color grading with warm terracotta and gold accents. "
            "Shot from 45-degree angle. 16:9 aspect ratio, ultra high quality."
        ),
    },
    {
        "name": "story-restaurant",
        "prompt": (
            "Interior of a cozy, modern Taiwanese restaurant with warm lighting. "
            "Wooden furniture, hanging pendant lights with warm golden glow, exposed brick wall elements. "
            "Traditional Taiwanese decorative elements subtly integrated — bamboo, calligraphy scrolls. "
            "Empty restaurant at golden hour, late afternoon light streaming through windows. "
            "Warm terracotta and cream color palette. Professional architectural photography. "
            "Inviting and authentic atmosphere. High quality, detailed."
        ),
    },
    {
        "name": "story-cooking",
        "prompt": (
            "Close-up of a Taiwanese chef's hands skillfully pulling handmade noodles in a kitchen. "
            "Flour dust floating in warm golden light. Steam rising from a large pot in the background. "
            "Authentic kitchen setting with professional equipment. Warm tones, dramatic lighting. "
            "Action shot capturing the motion of noodle making. Professional food photography, "
            "shallow depth of field. High quality."
        ),
    },
    {
        "name": "bubble-tea",
        "prompt": (
            "A single glass of authentic Taiwanese bubble milk tea with dark brown tapioca pearls "
            "visible at the bottom. The tea has a beautiful gradient from dark tea to creamy milk. "
            "Condensation droplets on the glass. Dark wooden surface background with soft bokeh. "
            "Single warm spotlight from the side creating dramatic shadows. "
            "Professional food photography, minimalist composition. Warm color palette. Ultra detailed."
        ),
    },
    {
        "name": "beef-noodle",
        "prompt": (
            "A steaming bowl of Taiwanese beef noodle soup (紅燒牛肉麵) in a ceramic bowl. "
            "Rich dark broth with visible chili oil sheen, thick hand-pulled noodles, "
            "tender braised beef chunks, bok choy, and scallions on top. "
            "Steam rising beautifully. Dark moody background with warm side lighting. "
            "Shot from slightly above. Professional food photography. Ultra appetizing, high quality."
        ),
    },
    {
        "name": "braised-pork",
        "prompt": (
            "A bowl of Taiwanese braised pork rice (滷肉飯) — white steamed rice topped with "
            "glossy, caramelized minced pork in rich brown sauce. Garnished with a halved soft-boiled egg "
            "and pickled mustard greens on the side. Small ceramic bowl on dark wood surface. "
            "Warm overhead lighting. Professional food photography, shallow depth of field. "
            "Rich warm tones, appetizing and traditional. High quality."
        ),
    },
    {
        "name": "pineapple-cake",
        "prompt": (
            "Taiwanese pineapple cakes (鳳梨酥) arranged on a minimalist ceramic plate. "
            "One cake cut in half showing the golden pineapple filling inside the buttery pastry. "
            "Soft natural lighting from window. Light cream/beige background. "
            "Elegant and delicate presentation. Professional food photography, "
            "soft shadows, pastel warm tones. Gift box slightly blurred in background. High quality."
        ),
    },
    {
        "name": "oolong-tea",
        "prompt": (
            "Traditional Taiwanese oolong tea being poured from a clay teapot into a small ceramic cup. "
            "Beautiful amber-colored tea liquid mid-pour. Tea leaves visible in a small dish nearby. "
            "Zen-like minimalist setting with bamboo mat. Soft warm natural lighting. "
            "Steam wisps rising from the cup. Professional food photography, "
            "shallow depth of field, tranquil atmosphere. High quality."
        ),
    },
    {
        "name": "gua-bao",
        "prompt": (
            "A Taiwanese gua bao (刈包) — fluffy white steamed bun filled with braised pork belly, "
            "pickled mustard greens, cilantro, and ground peanut powder. Held slightly open to show filling. "
            "Served on a small wooden board. Dark moody background with warm spotlight. "
            "Professional food photography, close-up shot with shallow depth of field. "
            "Warm terracotta and gold color accents. Ultra detailed, appetizing."
        ),
    },
]


def generate_with_imagen(prompt_data: dict) -> bool:
    """使用 Imagen 4.0 生成圖片"""
    name = prompt_data["name"]
    prompt = prompt_data["prompt"]
    output_path = OUTPUT_DIR / f"{name}.png"

    if output_path.exists():
        print(f"  [跳過] {name}.png 已存在")
        return True

    print(f"  [Imagen 4.0] {name}...")

    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="16:9" if name == "hero-bg" else "1:1",
            ),
        )

        if response.generated_images:
            image = response.generated_images[0]
            image.image.save(str(output_path))
            size = output_path.stat().st_size // 1024
            print(f"  [完成] {name}.png ({size}KB)")
            return True

        print(f"  [警告] {name} - 無圖片回傳")
        return False

    except Exception as e:
        print(f"  [Imagen 失敗] {name}: {e}")
        return generate_with_gemini_flash(prompt_data)


def generate_with_gemini_flash(prompt_data: dict) -> bool:
    """備用方案：使用 Gemini Flash Image Generation"""
    name = prompt_data["name"]
    prompt = prompt_data["prompt"]
    output_path = OUTPUT_DIR / f"{name}.png"

    print(f"  [備用 Gemini Flash] {name}...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            ),
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data is not None:
                image_data = part.inline_data.data
                with open(output_path, "wb") as f:
                    f.write(image_data)
                print(f"  [完成] {name}.png ({len(image_data) // 1024}KB)")
                return True

        print(f"  [警告] {name} - 回應中無圖片資料")
        return False

    except Exception as e:
        print(f"  [錯誤] {name}: {e}")
        return False


def main():
    print("=" * 60)
    print("TaiwanWay 網站圖片生成")
    print(f"輸出目錄: {OUTPUT_DIR}")
    print("=" * 60)

    success = 0
    failed = 0

    for i, prompt_data in enumerate(IMAGE_PROMPTS, 1):
        print(f"\n[{i}/{len(IMAGE_PROMPTS)}] {prompt_data['name']}")
        if generate_with_imagen(prompt_data):
            success += 1
        else:
            failed += 1

        # API 速率限制 - 每次生成間隔
        if i < len(IMAGE_PROMPTS):
            time.sleep(3)

    print("\n" + "=" * 60)
    print(f"結果: {success} 成功, {failed} 失敗")
    print("=" * 60)

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
