# convert_images.py（プロジェクトルートに置いて実行）
from PIL import Image
import os

targets = [
    r"shop0c\static\cosmos-hero.webp",
]

for path in targets:
    img = Image.open(path)
    out = os.path.splitext(path)[0] + ".webp"
    img.save(out, "webp", quality=60, method=6)
    before = os.path.getsize(path) / 1024
    after = os.path.getsize(out) / 1024
    print(f"{path}")
    print(f"  変換前: {before:.0f} KB → 変換後: {after:.0f} KB ({100*after/before:.0f}%)")