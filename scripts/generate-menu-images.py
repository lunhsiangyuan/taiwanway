#!/usr/bin/env python3
"""
生成菜單頁面額外需要的飲品分類圖片
"""
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

API_KEY = "AIzaSyDHwneH3Z99JHfyY76ufDVQSrO-6eZP0OA"
client = genai.Client(api_key=API_KEY)

OUTPUT_DIR = Path(__file__).parent.parent / "public" / "images"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# 額外需要生成的圖片
IMAGE_PROMPTS = [
    {
        "name": "iced-black-tea",
        "prompt": (
            "A tall glass of Taiwanese iced black tea with ice cubes, deep amber color, "
            "condensation on the glass. Traditional Taiwanese tea house setting. "
            "Dark moody background with warm side lighting. Professional food photography. "
            "Minimalist composition. High quality."
        ),
    },
    {
        "name": "honey-black-tea",
        "prompt": (
            "Taiwanese honey-scented black tea in an elegant glass cup, golden-amber color, "
            "with a drizzle of honey visible. Warm honey tones. Dark wooden surface, "
            "soft bokeh background. Professional food photography, shallow depth of field. "
            "Warm cozy atmosphere. High quality."
        ),
    },
    {
        "name": "jasmine-tea",
        "prompt": (
            "A clear glass teacup filled with light green jasmine green tea, with dried jasmine "
            "flowers floating on top. Small jasmine blossoms scattered nearby on a light bamboo mat. "
            "Soft natural lighting from the side. Zen-like minimalist setting. "
            "Professional food photography, peaceful atmosphere. High quality."
        ),
    },
    {
        "name": "matcha-latte",
        "prompt": (
            "A beautiful matcha latte in a ceramic cup with latte art on top, vibrant green color. "
            "Small bamboo whisk (chasen) visible in background. Dark moody setting with warm accent light. "
            "Professional food photography, shallow depth of field. Japanese-Taiwanese aesthetic. "
            "Minimalist, elegant. High quality."
        ),
    },
    {
        "name": "pot-brewed-tea",
        "prompt": (
            "A traditional Chinese gaiwan tea set with high mountain oolong tea. Small clay teapot "
            "with multiple tiny cups arranged elegantly. Dried tea leaves in a small bamboo scoop. "
            "Zen-like minimalist setting on wooden tea tray. Steam wisps. Warm natural lighting. "
            "Professional food photography. High quality."
        ),
    },
    {
        "name": "wonton-noodle",
        "prompt": (
            "A bowl of Taiwanese wonton noodle soup with plump hand-wrapped wontons, thin egg noodles, "
            "clear golden broth, bok choy, and scallions. Steam rising. Dark ceramic bowl on dark wood. "
            "Warm side lighting. Professional food photography, shot from above. High quality."
        ),
    },
    {
        "name": "chicken-rice",
        "prompt": (
            "A plate of Taiwanese chicken rice — sliced tender poached chicken thigh over steamed rice, "
            "drizzled with soy-based sauce and sesame oil. Garnished with cucumber slices. "
            "Small bowl of chicken broth on the side. Dark wood surface. "
            "Professional food photography, warm tones. High quality."
        ),
    },
    {
        "name": "brown-sugar-milk",
        "prompt": (
            "Taiwanese brown sugar pearl fresh milk in a clear glass, showing beautiful tiger stripe "
            "pattern of brown sugar swirling through white milk. Dark tapioca pearls at bottom. "
            "Dark moody background. Professional food photography, dramatic lighting. High quality."
        ),
    },
]


def generate_image(prompt_data: dict) -> bool:
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
                aspect_ratio="1:1",
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
        print(f"  [錯誤] {name}: {e}")
        return False


def main():
    print("=" * 60)
    print("TaiwanWay 菜單頁面額外圖片生成")
    print("=" * 60)

    success = 0
    failed = 0

    for i, prompt_data in enumerate(IMAGE_PROMPTS, 1):
        print(f"\n[{i}/{len(IMAGE_PROMPTS)}] {prompt_data['name']}")
        if generate_image(prompt_data):
            success += 1
        else:
            failed += 1
        if i < len(IMAGE_PROMPTS):
            time.sleep(3)

    print(f"\n結果: {success} 成功, {failed} 失敗")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
