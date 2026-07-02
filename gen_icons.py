"""
Gera os ícones do PWA (icons/icon-192.png, icon-512.png, icon-maskable-512.png,
apple-touch-icon.png) a partir das cores da identidade visual do ProtheusQuiz.

Uso:
    pip install pillow
    python3 gen_icons.py
"""
from PIL import Image, ImageDraw, ImageFont
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")
os.makedirs(OUT, exist_ok=True)

BG1 = (10, 14, 26)       # --bg (tema noite)
ACCENT = (0, 212, 255)   # --accent cyan
ACCENT2 = (124, 58, 237) # --accent2 violet


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def make_icon(size, path, maskable=False):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))

    grad = Image.new("RGB", (size, size))
    gdraw = ImageDraw.Draw(grad)
    for y in range(size):
        t = y / size
        gdraw.line([(0, y), (size, y)], fill=lerp(BG1, (17, 24, 39), t))

    mask = Image.new("L", (size, size), 0)
    mdraw = ImageDraw.Draw(mask)
    if maskable:
        mdraw.rectangle([0, 0, size, size], fill=255)
    else:
        mdraw.rounded_rectangle([0, 0, size - 1, size - 1], radius=int(size * 0.22), fill=255)
    img.paste(grad, (0, 0), mask)

    draw = ImageDraw.Draw(img)
    step = size // 8
    for gx in range(0, size, step):
        draw.line([(gx, 0), (gx, size)], fill=(0, 212, 255, 20), width=1)
    for gy in range(0, size, step):
        draw.line([(0, gy), (size, gy)], fill=(0, 212, 255, 20), width=1)

    safe = size * (0.6 if maskable else 0.78)
    off = (size - safe) / 2
    font_size = int(safe * 0.46)
    font = None
    for fp in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ]:
        if os.path.exists(fp):
            font = ImageFont.truetype(fp, font_size)
            break
    if font is None:
        font = ImageFont.load_default()

    text = "PQ"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (size - tw) / 2 - bbox[0]
    ty = (size - th) / 2 - bbox[1]

    text_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ImageDraw.Draw(text_layer).text((tx, ty), text, font=font, fill=(255, 255, 255, 255))
    text_mask = text_layer.split()[3]

    grad2 = Image.new("RGB", (size, size))
    g2draw = ImageDraw.Draw(grad2)
    for x in range(size):
        t = x / size
        g2draw.line([(x, 0), (x, size)], fill=lerp(ACCENT2, ACCENT, t))
    colored_text = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    colored_text.paste(grad2, (0, 0), text_mask)
    img = Image.alpha_composite(img, colored_text)

    draw = ImageDraw.Draw(img)
    bw = max(2, size // 40)
    bracket_len = safe * 0.18
    bx1 = off - size * 0.02
    by_top = size / 2 - safe * 0.30
    by_bot = size / 2 + safe * 0.30
    accent_col = (0, 212, 255, 230)
    draw.line([(bx1 + bracket_len, by_top), (bx1, size / 2), (bx1 + bracket_len, by_bot)],
              fill=accent_col, width=bw, joint="curve")
    bx2 = size - off + size * 0.02
    draw.line([(bx2 - bracket_len, by_top), (bx2, size / 2), (bx2 - bracket_len, by_bot)],
              fill=accent_col, width=bw, joint="curve")

    img.save(path)


if __name__ == "__main__":
    make_icon(192, f"{OUT}/icon-192.png")
    make_icon(512, f"{OUT}/icon-512.png")
    make_icon(512, f"{OUT}/icon-maskable-512.png", maskable=True)
    make_icon(180, f"{OUT}/apple-touch-icon.png")
    print("Ícones gerados em", OUT)
