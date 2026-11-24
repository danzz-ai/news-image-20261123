#!/usr/bin/env python3
"""Draw the news-image-20261123 front page: 'The World Today — 23 November 2026'.

A newspaper front page rendered with PIL so every headline and the date are
crisp and legible. Output: entry.png (a JPEG, 1024x1024, under 1 MiB).
All stories were reported on Monday 23 November 2026.
"""
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

PAPER = (247, 243, 233)
INK = (17, 17, 17)
RED = (179, 32, 44)
GREY = (90, 86, 78)
PANEL = (255, 253, 246)
HERO_BG = (10, 26, 48)
HERO_BG2 = (16, 48, 84)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_center(draw, cx, y, text, fnt, fill):
    draw.text((cx - draw.textlength(text, font=fnt) / 2, y), text, font=fnt, fill=fill)


def hero_art(base):
    """Night sky over a chip skyline: glowing circuit nodes, gold horizon."""
    art = Image.new("RGB", (968, 100), HERO_BG2)
    d = ImageDraw.Draw(art)
    # sky gradient bands
    for i in range(100):
        t = i / 99
        d.line([(0, i), (968, i)],
               fill=(int(16 + 10 * t), int(48 + 18 * t), int(84 + 20 * t)))
    rng = random.Random(23112026)
    # circuit nodes scattered in the sky
    for _ in range(46):
        x, y = rng.randint(0, 967), rng.randint(0, 45)
        r = rng.choice([1, 1, 2])
        d.ellipse([x - r, y - r, x + r, y + r], fill=(190, 214, 235))
    # a few thin circuit traces
    for _ in range(8):
        x, y = rng.randint(0, 900), rng.randint(0, 40)
        d.line([(x, y), (x + rng.randint(20, 60), y)], fill=(120, 160, 200), width=1)
    # pale glow, right third — centred higher so it sits in the sky,
    # clear of the dark band at the bottom of the art panel
    glow = Image.new("RGB", (968, 100), (0, 0, 0))
    gd = ImageDraw.Draw(glow)
    for r, col in ((58, (120, 190, 255)), (38, (170, 215, 255)), (22, (220, 238, 255))):
        gd.ellipse([790 - r, 44 - r, 790 + r, 44 + r], fill=col)
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    art = Image.blend(art, Image.composite(glow, Image.new("RGB", (968, 100), (0, 0, 0)),
                                            glow.convert("L").point(lambda v: v)), 0.85)
    d = ImageDraw.Draw(art)
    # thin gold horizon line above the skyline
    d.line([(0, 73), (968, 73)], fill=(255, 214, 130), width=2)
    # dark skyline along the bottom
    d.rectangle([0, 74, 968, 100], fill=(6, 18, 34))
    for x, w, h in ((0, 90, 22), (110, 60, 32), (200, 130, 18), (360, 70, 28),
                    (470, 110, 20), (620, 80, 34), (730, 120, 22), (880, 88, 30)):
        d.rectangle([x, 100 - h, x + w, 100], fill=(3, 10, 20))
    return art


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([6, 6, W - 7, H - 7], outline=INK, width=3)

    # ---- masthead ----
    draw_center(d, W // 2, 12, "THE WORLD TODAY", font(SERIF_B, 72), INK)
    d.line([(28, 108), (996, 108)], fill=INK, width=3)
    d.line([(28, 114), (996, 114)], fill=INK, width=1)
    draw_center(d, W // 2, 124, "MONDAY, 23 NOVEMBER 2026",
                font(SANS_B, 30), RED)
    d.line([(28, 164), (996, 164)], fill=INK, width=2)

    # ---- hero ----
    hx0, hy0, hx1, hy1 = 28, 174, 996, 490
    d.rectangle([hx0, hy0, hx1, hy1], fill=HERO_BG)
    d.text((hx0 + 20, hy0 + 12), "TECH  •  SILICON VALLEY  •  LEAD STORY",
           font=font(SANS_B, 19), fill=(255, 214, 130))
    d.text((hx0 + 20, hy0 + 42), "HUANG IS BACK",
           font=font(SERIF_B, 54), fill=(255, 255, 255))
    d.text((hx0 + 20, hy0 + 100), "AT NVIDIA",
           font=font(SERIF_B, 54), fill=(255, 255, 255))
    deck = ("Nvidia's board unanimously reinstates Jensen Huang as chief "
            "executive, 11 days after he resigned. Shares jump about 30%.")
    y = hy0 + 164
    for line in wrap(d, deck, font(SANS, 21), hx1 - hx0 - 40):
        d.text((hx0 + 20, y), line, font=font(SANS, 21), fill=(215, 228, 238))
        y += 27
    img.paste(hero_art(img), (hx0, hy1 - 100))

    # ---- panels ----
    def panel(x0, y0, x1, y1, kicker, headline, deck_text, head_size=24):
        d.rectangle([x0, y0, x1, y1], fill=PANEL, outline=(150, 146, 136), width=1)
        d.text((x0 + 14, y0 + 10), kicker, font=font(SANS_B, 16), fill=RED)
        y = y0 + 34
        for line in wrap(d, headline, font(SERIF_B, head_size), x1 - x0 - 28):
            d.text((x0 + 14, y), line, font=font(SERIF_B, head_size), fill=INK)
            y += head_size + 6
        y += 4
        for line in wrap(d, deck_text, font(SANS, 16), x1 - x0 - 28):
            d.text((x0 + 14, y), line, font=font(SANS, 16), fill=(52, 50, 46))
            y += 20

    d.line([(28, 504), (996, 504)], fill=INK, width=2)
    panel(28, 516, 340, 698, "NATO  •  POLAND",
          "NATO sends jets to Poland",
          "Early-warning aircraft head to Poland after Russian missiles "
          "landed; Warsaw summons Moscow's envoy.")
    panel(356, 516, 668, 698, "EUROPE",
          "EU unveils 22nd Russia sanctions",
          "Brussels targets Russian banks, crypto, the shadow fleet and "
          "sport in its latest package.")
    panel(684, 516, 996, 698, "WASHINGTON",
          "US sanctions Iran shadow banks",
          "Treasury blacklists more than two dozen Iranian entities tied "
          "to shadow banking networks.")
    d.line([(28, 710), (996, 710)], fill=INK, width=2)
    panel(28, 722, 340, 904, "TRADE  •  ASIA",
          "US blacklists AI firm Megaspeed",
          "Commerce bars the Nvidia partner over alleged AI-chip diversion "
          "to China.")
    panel(356, 722, 668, 904, "LONDON  •  HEALTH",
          "NHS launches AI cancer trial",
          "The world's largest AI breast screening trial starts; 700,000 "
          "women, 30 sites, £10m.")
    panel(684, 722, 996, 904, "COLOMBIA",
          "Drones hit police base in Cúcuta",
          "Explosive drones injure three civilians, including an infant, "
          "and damage 60 homes.")

    # ---- ticker ----
    tick1 = ("Russia rules out new Black Sea grain deal  •  Zelensky warns "
             "of new Russian strikes")
    tick2 = ("Riemann proof clears machine checks  •  Tajikistan quits ICC  •  "
             "Trump limits Congress data demands")
    d.rectangle([28, 916, 996, 980], fill=INK)
    d.text((44, 924), "ALSO TODAY", font=font(SANS_B, 17), fill=(255, 214, 130))
    d.text((188, 924), tick1, font=font(SANS, 16), fill=(255, 255, 255))
    d.text((44, 950), tick2, font=font(SANS, 16), fill=(255, 255, 255))

    draw_center(d, W // 2, 988, "All stories reported Monday 23 November 2026  •  The World Today",
                font(SANS, 14), GREY)

    img.save(OUT, format="JPEG", quality=88, optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
