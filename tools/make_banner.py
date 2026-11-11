#!/usr/bin/env python3
"""生成 GitHub 主页横幅（无需联网，纯 PIL）。

用法：python3 tools/make_banner.py
输出：assets/banner.png（1280x400）
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1280, 400
S = 2  # 2x 超采样，缩回去更干净

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "banner.png"

FONT_LATIN = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_LATIN_LIGHT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
FONT_CJK = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"
FONT_CJK_LIGHT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"

BG_TOP = (7, 14, 28)
BG_BOTTOM = (10, 38, 58)
CYAN = (120, 214, 255)
DIM = (143, 186, 214)


def lerp(a, b, t):
    return tuple(round(x + (y - x) * t) for x, y in zip(a, b))


def gradient(w, h, top, bottom):
    img = Image.new("RGB", (1, h))
    px = img.load()
    for y in range(h):
        px[0, y] = lerp(top, bottom, y / max(1, h - 1))
    return img.resize((w, h), Image.BILINEAR)


def main():
    w, h = W * S, H * S
    img = gradient(w, h, BG_TOP, BG_BOTTOM).convert("RGBA")

    # 左上角青色柔光
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow)
    gd.ellipse((-500, -700, 1100, 500), fill=(64, 196, 255, 46))
    gd.ellipse((1500, -600, 2600, 500), fill=(0, 110, 160, 60))
    glow = glow.filter(ImageFilter.GaussianBlur(220))
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img, "RGBA")

    # 细点阵
    step = 46
    for x in range(0, w, step):
        for y in range(0, h, step):
            draw.ellipse((x, y, x + 4, y + 4), fill=(255, 255, 255, 12))

    # 右侧虚线圆环
    cx, cy, r = int(w * 0.815), int(h * 0.50), int(h * 0.40)
    for i in range(72):
        import math

        a0 = math.radians(i * 5)
        a1 = math.radians(i * 5 + 2.4)
        draw.arc(
            (cx - r, cy - r, cx + r, cy + r),
            start=math.degrees(a0),
            end=math.degrees(a1),
            fill=(120, 214, 255, 70),
            width=3 * S,
        )
    r2 = int(r * 0.72)
    for i in range(48):
        import math

        a0 = math.radians(i * 7.5 + 40)
        a1 = math.radians(i * 7.5 + 43)
        draw.arc(
            (cx - r2, cy - r2, cx + r2, cy + r2),
            start=math.degrees(a0),
            end=math.degrees(a1),
            fill=(255, 255, 255, 40),
            width=2 * S,
        )

    # 左侧文字
    x = 112 * S
    label_font = ImageFont.truetype(FONT_LATIN_LIGHT, 19 * S)
    draw.text((x, 96 * S), "G I T H U B   P R O F I L E", font=label_font, fill=(120, 214, 255, 220))

    name_font = ImageFont.truetype(FONT_LATIN, 108 * S)
    draw.text((x - 4 * S, 122 * S), "xiaoyu", font=name_font, fill=(245, 250, 255))

    cjk_font = ImageFont.truetype(FONT_CJK_LIGHT, 44 * S, index=2)
    draw.text((x + 4 * S, 262 * S), "小鱼", font=cjk_font, fill=(190, 226, 245))
    tag_font = ImageFont.truetype(FONT_LATIN_LIGHT, 25 * S)
    draw.text((x + 130 * S, 276 * S), "tools  ·  automation  ·  fetch  ·  search", font=tag_font, fill=DIM)

    # 强调线
    draw.rounded_rectangle((x, 340 * S, x + 380 * S, 344 * S), radius=2 * S, fill=(120, 214, 255, 180))
    draw.rounded_rectangle((x, 340 * S, x + 120 * S, 344 * S), radius=2 * S, fill=(120, 214, 255, 255))

    out = img.resize((W, H), Image.LANCZOS).convert("RGB")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    out.save(OUT, optimize=True)
    print(f"wrote {OUT} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
