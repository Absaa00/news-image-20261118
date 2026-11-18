# SPDX-License-Identifier: MIT
"""news-image-20261118: sum up Wednesday 18 November 2026's world news in one image.

A deterministic program (no network, no randomness, no clock) that draws a
six-panel newspaper front page -- 1024x1024 PNG -- from six real news stories
reported on 17-18 November 2026 (AP, Reuters, DW, BBC, IMD):

1. Trump lands in Manila for Quad talks ahead of a China visit.
2. Ukraine strikes the Crimean bridge for a second day; Russia hits Kyiv bridges.
3. Iran fires drones at a US radar facility in Bahrain -- third strike in days,
   intercepted, no damage or injuries.
4. Canada and China extend trade deals as Xi meets Carney ahead of APEC.
5. Britain sanctions firms tied to Israeli settlements.
6. Cyclone Akvan strengthens in the Bay of Bengal; landfall forecast 20 Nov
   with gusts to 145 km/h.

Usage: python3 main.py [output-path]   (default: /output/entry.png)
"""

import math
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (24, 24, 22)
RULE = (24, 24, 22)
MUTED = (90, 86, 76)
ACCENT = (178, 34, 34)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SERIF_B = os.path.join(FONT_DIR, "DejaVuSerif-Bold.ttf")
SERIF = os.path.join(FONT_DIR, "DejaVuSerif.ttf")
SANS = os.path.join(FONT_DIR, "DejaVuSans.ttf")
SANS_B = os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_centered(draw, cx, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text((cx - w / 2, y), text, font=fnt, fill=fill)
    return y + fnt.size + 2


# ---------------------------------------------------------------- scenes
def scene_manila(d, x, y, w, h):
    # Sunset sky, skyline, two flag poles.
    d.rectangle([x, y, x + w, y + h], fill=(233, 164, 90))
    d.ellipse([x + w - 78, y + 12, x + w - 18, y + 72], fill=(245, 222, 120))
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(70, 90, 110))
    for bx, bw, bh in [(8, 44, 40), (60, 34, 58), (102, 52, 34), (162, 38, 64),
                       (208, 46, 44), (262, 40, 56), (310, 44, 36)]:
        d.rectangle([x + bx, y + h - 26 - bh, x + bx + bw, y + h - 26],
                    fill=(52, 58, 74))
        for wy in range(y + h - 26 - bh + 8, y + h - 30, 16):
            d.rectangle([x + bx + 6, wy, x + bx + bw - 6, wy + 6],
                        fill=(245, 222, 120))
    d.line([x + 20, y + 8, x + 20, y + 52], fill=INK, width=3)
    d.polygon([(x + 20, y + 8), (x + 52, y + 16), (x + 20, y + 24)],
              fill=(178, 34, 34))
    d.line([x + w - 20, y + 8, x + w - 20, y + 52], fill=INK, width=3)
    d.polygon([(x + w - 20, y + 8), (x + w - 52, y + 16), (x + w - 20, y + 24)],
              fill=(36, 74, 160))


def scene_bridge(d, x, y, w, h):
    # Bridge deck over water, blast burst at mid-span.
    d.rectangle([x, y, x + w, y + h], fill=(168, 196, 222))
    d.rectangle([x, y + h - 34, x + w, y + h], fill=(46, 90, 130))
    for i in range(5):
        wx = x + 24 + i * 78
        d.arc([wx, y + h - 52, wx + 56, y + h - 10], 180, 360, fill=(255, 255, 255), width=3)
    d.rectangle([x, y + 62, x + w, y + 74], fill=(70, 70, 78))
    for px in (60, 190, 320):
        d.rectangle([x + px, y + 74, x + px + 12, y + h - 34], fill=(70, 70, 78))
    cx, cy = x + w // 2, y + 46
    for r, col in [(46, (255, 140, 40)), (34, (255, 190, 60)), (22, (255, 240, 140))]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col)
    for k in range(8):
        ang = k * 3.14159 / 4
        d.line([cx, cy, cx + int(58 * math.cos(ang)),
                cy + int(34 * math.sin(ang))],
               fill=(255, 140, 40), width=4)


def scene_radar(d, x, y, w, h):
    # Radar dish sweeping, drones overhead.
    d.rectangle([x, y, x + w, y + h], fill=(28, 42, 66))
    for i in range(4):
        d.ellipse([x + w // 2 - 78 + i * 12, y + h - 78 + i * 12,
                   x + w // 2 + 78 - i * 12, y + h - 78 + i * 12 + 6],
                  outline=(90, 200, 120), width=2)
    d.pieslice([x + w // 2 - 56, y + 8, x + w // 2 + 56, y + 120], 200, 340,
               fill=(120, 220, 150))
    d.line([x + w // 2, y + 64, x + w // 2, y + h - 22], fill=(200, 200, 200), width=4)
    d.line([x + w // 2 - 34, y + h - 22, x + w // 2 + 34, y + h - 22],
           fill=(200, 200, 200), width=4)
    for dx, dy in [(52, 26), (150, 14), (250, 34), (330, 20)]:
        d.ellipse([x + dx - 5, y + dy - 5, x + dx + 5, y + dy + 5], fill=(255, 90, 60))
        d.line([x + dx - 16, y + dy, x + dx + 16, y + dy], fill=(255, 90, 60), width=2)
        d.line([x + dx, y + dy - 8, x + dx, y + dy + 8], fill=(255, 90, 60), width=2)


def scene_trade(d, x, y, w, h):
    # Two flags side by side, arrows of exchange between them.
    d.rectangle([x, y, x + w, y + h], fill=(238, 238, 230))
    # Canada flag
    fx, fy, fw, fh = x + 18, y + 22, 150, 84
    d.rectangle([fx, fy, fx + 34, fy + fh], fill=(200, 30, 30))
    d.rectangle([fx + fw - 34, fy, fx + fw, fy + fh], fill=(200, 30, 30))
    d.rectangle([fx + 34, fy, fx + fw - 34, fy + fh], fill=(255, 255, 255))
    cx, cy = fx + fw // 2, fy + fh // 2
    d.polygon([(cx, cy - 26), (cx + 8, cy - 8), (cx + 20, cy - 12), (cx + 14, cy + 2),
               (cx + 24, cy + 8), (cx + 8, cy + 10), (cx + 10, cy + 26),
               (cx, cy + 16), (cx - 10, cy + 26), (cx - 8, cy + 10),
               (cx - 24, cy + 8), (cx - 14, cy + 2), (cx - 20, cy - 12),
               (cx - 8, cy - 8)], fill=(200, 30, 30))
    # China flag
    gx, gy = x + w - 168, y + 22
    d.rectangle([gx, gy, gx + 150, gy + 84], fill=(222, 40, 30))
    d.polygon([(gx + 22, gy + 12), (gx + 26, gy + 22), (gx + 36, gy + 22),
               (gx + 28, gy + 29), (gx + 31, gy + 39), (gx + 22, gy + 33),
               (gx + 13, gy + 39), (gx + 16, gy + 29), (gx + 8, gy + 22),
               (gx + 18, gy + 22)], fill=(255, 220, 60))
    for sx, sy in [(gx + 52, gy + 14), (gx + 62, gy + 26), (gx + 62, gy + 40),
                   (gx + 50, gy + 48)]:
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 220, 60))
    # exchange arrows
    d.line([x + 190, y + 52, x + w - 190, y + 52], fill=INK, width=3)
    d.polygon([(x + w - 190, y + 52), (x + w - 204, y + 44), (x + w - 204, y + 60)],
              fill=INK)
    d.line([x + w - 190, y + 84, x + 190, y + 84], fill=INK, width=3)
    d.polygon([(x + 190, y + 84), (x + 204, y + 76), (x + 204, y + 92)], fill=INK)


def scene_london(d, x, y, w, h):
    # Westminster silhouette and a gavel of sanctions.
    d.rectangle([x, y, x + w, y + h], fill=(196, 214, 228))
    d.rectangle([x + 40, y + h - 10, x + w - 40, y + h], fill=(90, 100, 110))
    d.rectangle([x + 52, y + 34, x + 92, y + h - 10], fill=(52, 58, 74))
    d.polygon([(x + 52, y + 34), (x + 72, y + 10), (x + 92, y + 34)], fill=(52, 58, 74))
    d.ellipse([x + 58, y + 42, x + 86, y + 70], fill=(245, 240, 220))
    d.line([x + 72, y + 42, x + 72, y + 70], fill=INK, width=2)
    d.line([x + 72, y + 56, x + 82, y + 48], fill=INK, width=2)
    for bx in (120, 180, 240, 300):
        d.rectangle([x + bx, y + 64, x + bx + 44, y + h - 10], fill=(70, 76, 92))
        for wy in range(y + 70, y + h - 16, 14):
            d.rectangle([x + bx + 6, wy, x + bx + 38, wy + 6], fill=(245, 222, 120))
    d.line([x + 300, y + 22, x + 326, y + 48], fill=(120, 40, 30), width=8)
    d.rectangle([x + 292, y + 14, x + 336, y + 30], fill=(120, 40, 30))
    d.rectangle([x + 318, y + 48, x + 348, y + 54], fill=(120, 40, 30))


def scene_cyclone(d, x, y, w, h):
    # Spiral storm over a rough sea.
    d.rectangle([x, y, x + w, y + h], fill=(140, 180, 205))
    cx, cy = x + w // 2, y + h // 2
    for r in range(12, 58, 9):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20 + r * 3, 300 + r * 3,
              fill=(255, 255, 255), width=6)
    d.ellipse([cx - 12, cy - 12, cx + 12, cy + 12], fill=(245, 245, 245))
    for wy in range(y + h - 26, y + h - 2, 8):
        for sx in range(0, w, 44):
            d.arc([x + sx, wy, x + sx + 34, wy + 12], 200, 340,
                  fill=(255, 255, 255), width=3)


SCENES = [scene_manila, scene_bridge, scene_radar, scene_trade, scene_london,
          scene_cyclone]

STORIES = [
    ("ASIA", "Trump lands in Manila for Quad talks",
     "The US president opens his Asia tour in the Philippines ahead of the Quad "
     "leaders' meeting and a planned visit to China."),
    ("WAR IN UKRAINE", "Ukraine hits Crimea bridge for a second day",
     "Kyiv strikes the strategic span again as Russian attacks hit bridges and "
     "cut power and water in the capital."),
    ("GULF TENSIONS", "Iran drones target US radar in Bahrain",
     "Tehran's third strike in days on US targets in the Gulf is intercepted; "
     "no damage or injuries are reported."),
    ("TRADE", "Canada and China extend trade deals",
     "Xi meets Carney ahead of the APEC summit as Ottawa and Beijing widen "
     "trade cooperation."),
    ("MIDDLE EAST", "Britain sanctions settlement firms",
     "London blacklists firms tied to Israeli settlements in a push to protect "
     "the two-state solution."),
    ("WEATHER", "Cyclone Akvan bears down on India",
     "The severe storm in the Bay of Bengal is forecast to strike Andhra "
     "Pradesh on 20 November, gusts to 145 km/h."),
]


def draw_panel(d, x, y, w, h, idx):
    kicker, headline, caption = STORIES[idx]
    d.rectangle([x, y, x + w, y + h], outline=INK, width=2)
    img_h = 118
    SCENES[idx](d, x + 2, y + 2, w - 4, img_h)
    d.line([x, y + img_h + 2, x + w, y + img_h + 2], fill=INK, width=2)
    tx = x + 12
    ty = y + img_h + 10
    d.text((tx, ty), kicker, font=font(SANS_B, 14), fill=ACCENT)
    ty += 20
    for line in wrap(d, headline, font(SERIF_B, 23), w - 24):
        d.text((tx, ty), line, font=font(SERIF_B, 23), fill=INK)
        ty += 28
    ty += 2
    for line in wrap(d, caption, font(SANS, 15), w - 24):
        d.text((tx, ty), line, font=font(SANS, 15), fill=(52, 50, 46))
        ty += 19


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Masthead
    d.rectangle([0, 0, W, 118], fill=(24, 24, 22))
    draw_centered(d, W // 2, 14, "THE WORLD IN ONE PAGE", font(SERIF_B, 52), (247, 243, 232))
    draw_centered(d, W // 2, 78, "WEDNESDAY 18 NOVEMBER 2026  •  SIX STORIES THAT SHAPED THE DAY",
                  font(SANS, 17), (200, 194, 178))
    d.line([24, 130, W - 24, 130], fill=RULE, width=3)

    # 2 x 3 grid (142 .. 984), footer below
    margin, gap = 24, 16
    pw = (W - 2 * margin - gap) // 2
    ph = (984 - 142 - 2 * gap) // 3
    for i in range(6):
        col, row = i % 2, i // 2
        draw_panel(d, margin + col * (pw + gap), 142 + row * (ph + gap),
                   pw, ph, i)

    # Footer
    d.line([24, 994, W - 24, 994], fill=RULE, width=2)
    d.text((24, 1000), "Sources: AP, Reuters, DW, BBC, IMD  •  Drawn programmatically, no photos",
           font=font(SANS, 13), fill=MUTED)

    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    img.save(out, format="PNG")


if __name__ == "__main__":
    main()
