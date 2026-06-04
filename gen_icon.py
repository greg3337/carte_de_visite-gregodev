from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os

W, H = 180, 180
RADIUS = 36
BG     = (8, 8, 16)
CYAN   = (0, 210, 255)
VIOLET = (123, 47, 247)

# ── Background with rounded corners ──────────────────────────
img  = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)
draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=RADIUS, fill=(*BG, 255))

# ── Diagonal gradient (135°, cyan → violet) ──────────────────
xx, yy = np.meshgrid(np.linspace(0, 1, W), np.linspace(0, 1, H))
t  = (xx + yy) / 2
r  = (CYAN[0] + (VIOLET[0] - CYAN[0]) * t).astype(np.uint8)
g  = (CYAN[1] + (VIOLET[1] - CYAN[1]) * t).astype(np.uint8)
b  = (CYAN[2] + (VIOLET[2] - CYAN[2]) * t).astype(np.uint8)
a  = np.full((H, W), 255, dtype=np.uint8)
gradient = Image.fromarray(np.stack([r, g, b, a], axis=-1), "RGBA")

# ── Text mask ─────────────────────────────────────────────────
candidates = [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/verdanab.ttf",
]
font = None
for path in candidates:
    if os.path.exists(path):
        try:
            font = ImageFont.truetype(path, 90)
            break
        except Exception:
            pass
if font is None:
    font = ImageFont.load_default()

text      = "< >"
mask_img  = Image.new("L", (W, H), 0)
mask_draw = ImageDraw.Draw(mask_img)
bbox      = mask_draw.textbbox((0, 0), text, font=font)
tx        = (W - (bbox[2] - bbox[0])) // 2 - bbox[0]
ty        = (H - (bbox[3] - bbox[1])) // 2 - bbox[1]
mask_draw.text((tx, ty), text, fill=255, font=font)

# ── Composite gradient through text mask ─────────────────────
gradient_text = Image.composite(gradient, Image.new("RGBA", (W, H), (0, 0, 0, 0)), mask_img)
result        = Image.alpha_composite(img, gradient_text)

result.save("apple-touch-icon.png")
print("apple-touch-icon.png generated (180×180)")
