#!/usr/bin/env python3
"""Render the front page for news-image-20261123.

"The World Today - 23 November 2026": one 1024x1024 JPEG summing up the
day's world news, drawn with Pillow and DejaVu fonts. No network, no AI
image generation - every element is drawn from the story list below.
"""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

CREAM = (245, 241, 232)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (163, 30, 34)
NAVY = (13, 27, 62)
GOLD = (201, 162, 39)
GREY = (105, 105, 105)
INK = (35, 35, 35)
SKYLINE = (4, 8, 20)

SERIF_BOLD = "DejaVuSerif-Bold.ttf"
SERIF = "DejaVuSerif.ttf"
SANS_BOLD = "DejaVuSans-Bold.ttf"

FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/local/share/fonts",
]


def load_font(name, size):
    for folder in FONT_DIRS:
        path = os.path.join(folder, name)
        if os.path.exists(path):
            return ImageFont.truetype(path, size)
    return ImageFont.load_default(size)


def wrap(draw, text, font, max_width):
    words = text.split()
    lines = []
    current = ""
    for word in words:
        trial = (current + " " + word).strip()
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def fit_text(draw, text, font_name, start_size, max_width, max_lines, min_size=12):
    size = start_size
    while size > min_size:
        font = load_font(font_name, size)
        lines = wrap(draw, text, font, max_width)
        if len(lines) <= max_lines:
            return font, lines
        size -= 1
    font = load_font(font_name, min_size)
    return font, wrap(draw, text, font, max_width)


def draw_lines(draw, lines, x, y, font, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


PANELS = [
    ("NATO • POLAND", "NATO sends jets to Poland",
     "Early-warning aircraft head to Poland after Russian missiles landed; "
     "Warsaw summons Moscow's envoy."),
    ("EUROPE", "EU unveils 22nd Russia sanctions",
     "Brussels targets Russian banks, crypto, the shadow fleet and sport "
     "in its latest package."),
    ("WASHINGTON", "US sanctions Iran shadow banks",
     "Treasury blacklists more than two dozen Iranian entities tied to "
     "shadow banking networks."),
    ("TRADE • ASIA", "US blacklists AI firm Megaspeed",
     "Commerce bars the Nvidia partner over alleged AI-chip diversion "
     "to China."),
    ("LONDON • HEALTH", "NHS launches AI cancer trial",
     "The world's largest AI breast screening trial starts; 700,000 women, "
     "30 sites, £10m."),
    ("COLOMBIA", "Drones hit police base in Cúcuta",
     "Explosive drones injure three civilians, including an infant, and "
     "damage 60 homes."),
]


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)

    # Outer border.
    draw.rectangle([8, 8, W - 9, H - 9], outline=BLACK, width=3)

    # Masthead.
    masthead = load_font(SERIF_BOLD, 76)
    draw.text((W // 2, 26), "THE WORLD TODAY", font=masthead, fill=BLACK, anchor="mt")

    # Date line with rules above and below.
    draw.line([(28, 116), (W - 28, 116)], fill=BLACK, width=2)
    date_font = load_font(SERIF_BOLD, 34)
    draw.text((W // 2, 126), "MONDAY, 23 NOVEMBER 2026", font=date_font, fill=RED, anchor="mt")
    draw.line([(28, 170), (W - 28, 170)], fill=BLACK, width=2)

    # Hero band.
    draw.rectangle([20, 182, 1004, 500], fill=NAVY)
    kicker = load_font(SANS_BOLD, 20)
    draw.text((44, 198), "TECH • SILICON VALLEY • LEAD STORY", font=kicker, fill=GOLD)
    headline = load_font(SERIF_BOLD, 62)
    draw.text((44, 226), "HUANG IS BACK", font=headline, fill=WHITE)
    draw.text((44, 292), "AT NVIDIA", font=headline, fill=WHITE)
    body_font = load_font(SERIF, 23)
    hero_body = ("Nvidia's board unanimously reinstates Jensen Huang as chief "
                 "executive, 11 days after he resigned. Shares jump about 30%.")
    hero_lines = wrap(draw, hero_body, body_font, 940)
    draw_lines(draw, hero_lines, 44, 362, body_font, WHITE, 30)

    # Decorative strip: skyline silhouette, glowing orb, gold horizon line.
    buildings = [
        (20, 56, 34), (84, 30, 52), (122, 52, 26), (182, 36, 44),
        (226, 60, 30), (294, 34, 56), (336, 48, 36), (392, 30, 48),
        (430, 56, 28), (494, 40, 50), (542, 32, 38), (582, 54, 30),
        (644, 36, 52), (688, 48, 34), (744, 30, 46), (782, 56, 28),
        (846, 40, 50), (894, 34, 40), (936, 68, 30),
    ]
    for x, w, h in buildings:
        draw.rectangle([x, 500 - h, x + w, 500], fill=SKYLINE)
    strip = Image.new("RGBA", (984, 72), (0, 0, 0, 0))
    sd = ImageDraw.Draw(strip)
    cx, cy = 810, 40
    for radius, alpha in [(58, 25), (46, 45), (34, 80), (24, 130)]:
        sd.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                   fill=(255, 214, 120, alpha))
    sd.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(255, 232, 170, 230))
    img.paste(strip, (20, 428), strip)
    draw = ImageDraw.Draw(img)
    draw.line([(28, 494), (996, 494)], fill=GOLD, width=2)

    # Six panels in two rows of three.
    card_w, card_h = 320, 184
    xs = [20, 352, 684]
    ys = [512, 708]
    for row, y0 in enumerate(ys):
        for col, x0 in enumerate(xs):
            kicker_text, headline_text, body_text = PANELS[row * 3 + col]
            draw.rectangle([x0, y0, x0 + card_w, y0 + card_h],
                           fill=WHITE, outline=BLACK, width=1)
            kfont = load_font(SANS_BOLD, 16)
            draw.text((x0 + 14, y0 + 12), kicker_text, font=kfont, fill=RED)
            hfont, hlines = fit_text(draw, headline_text, SERIF_BOLD, 26, 292, 2)
            draw_lines(draw, hlines, x0 + 14, y0 + 36, hfont, BLACK, 30)
            bfont, blines = fit_text(draw, body_text, SERIF, 17, 292, 3)
            draw_lines(draw, blines, x0 + 14, y0 + 102, bfont, INK, 21)

    # Ticker strip.
    draw.rectangle([20, 902, 1004, 962], fill=BLACK)
    label_font = load_font(SANS_BOLD, 18)
    label = "ALSO TODAY"
    draw.text((36, 922), label, font=label_font, fill=GOLD)
    label_w = draw.textlength(label, font=label_font)
    ticker_text = ("Russia rules out new Black Sea grain deal • Zelensky warns of new "
                   "Russian strikes • Riemann proof clears machine checks • "
                   "Tajikistan quits ICC • Trump limits Congress data demands")
    text_x = 36 + label_w + 16
    tfont, tlines = fit_text(draw, ticker_text, SERIF, 15, 1004 - 16 - text_x, 2)
    draw_lines(draw, tlines, text_x, 916, tfont, WHITE, 20)

    # Footer.
    footer_font = load_font(SERIF, 15)
    draw.text((W // 2, 974), "All stories reported Monday 23 November 2026 • The World Today",
              font=footer_font, fill=GREY, anchor="mt")

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img.save(out_path, "JPEG", quality=92)
    print("wrote %s %d bytes" % (out_path, os.path.getsize(out_path)))


if __name__ == "__main__":
    main()
