from PIL import Image, ImageOps
from pathlib import Path

src_dir = Path("media/item_images")
out_dir = Path("media/item_images_light")
out_dir.mkdir(exist_ok=True)

for path in src_dir.iterdir():
    if path.suffix.lower() not in [".png", ".jpg", ".jpeg", ".webp"]:
        continue

    img = Image.open(path)
    img = ImageOps.exif_transpose(img)

    if img.mode in ("RGBA", "LA"):
        background = Image.new("RGB", img.size, (255, 255, 255))
        background.paste(img, mask=img.getchannel("A"))
        img = background
    else:
        img = img.convert("RGB")

    img.thumbnail((600, 600))

    save_path = out_dir / (path.stem + ".webp")
    img.save(save_path, "WEBP", quality=75, method=6)

    print(path.name, "->", save_path.name)