from PIL import Image, ImageDraw, ImageFont
import os

SIZE = 256
COLOR = "#5645d4"
DARK = "#0a1530"
WHITE = "#ffffff"

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

margin = 20
draw.rounded_rectangle(
    [margin, margin, SIZE - margin, SIZE - margin],
    radius=40, fill=COLOR
)

inner = 56
draw.rounded_rectangle(
    [inner, inner, SIZE - inner, SIZE - inner],
    radius=28, fill=DARK
)

try:
    font = ImageFont.truetype("segoeui.ttf", 110)
except Exception:
    font = ImageFont.load_default()

bbox = draw.textbbox((0, 0), "M", font=font)
tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
tx = (SIZE - tw) // 2 - bbox[0]
ty = (SIZE - th) // 2 - bbox[1] - 4
draw.text((tx, ty), "M", fill=WHITE, font=font)

try:
    font_small = ImageFont.truetype("segoeui.ttf", 28)
except Exception:
    font_small = ImageFont.load_default()

bbox2 = draw.textbbox((0, 0), "CONV", font=font_small)
sw, sh = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]
sx = (SIZE - sw) // 2 - bbox2[0]
sy = ty + th + 6
draw.text((sx, sy), "CONV", fill=COLOR, font=font_small)

path = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(path, exist_ok=True)
icon_path = os.path.join(path, "icon.ico")

img_sizes = []
for s in [256, 128, 64, 48, 32, 16]:
    resized = img.resize((s, s), Image.LANCZOS)
    img_sizes.append(resized)

img_sizes[0].save(
    icon_path,
    format="ICO",
    sizes=[(s, s) for s in [256, 128, 64, 48, 32, 16]],
    append_images=img_sizes[1:]
)

png_path = os.path.join(path, "icon.png")
img.save(png_path, "PNG")
print(f"Icon saved: {icon_path}")
print(f"PNG saved: {png_path}")
