# SPDX-License-Identifier: MIT
"""Build entry.png: 'THE DAY IN WORLD NEWS' for Thursday 19 November 2026.

Deterministic one-page editorial infographic, 1024x1024 PNG.
Every story, number and source below comes only from the verified
news list supplied for this entry. Run: python3 build_image.py
Writes entry.png beside this file. Two runs produce identical bytes.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 24

IVORY = (247, 242, 230)
CARD = (253, 251, 245)
INK = (26, 26, 24)
GREY = (96, 92, 82)
NAVY = (13, 33, 55)
NAVY2 = (24, 58, 94)
GOLD = (198, 150, 44)
RED = (178, 34, 52)
TEAL = (23, 107, 110)
BLUE = (45, 90, 140)
LINE = (203, 193, 168)
WHITE = (255, 255, 255)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if draw.textlength(trial, font=fnt) <= maxw:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, xy, text, fnt, fill, maxw, leading=1.18, max_lines=None):
    x, y = xy
    lines = wrap(draw, text, fnt, maxw)
    if max_lines:
        lines = lines[:max_lines]
    lh = int(fnt.size * leading)
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


def fit_headline(draw, text, maxw, start=16, minimum=11):
    size = start
    while size > minimum:
        fnt = font(SERIF_B, size)
        if len(wrap(draw, text, fnt, maxw)) <= 3:
            return fnt
        size -= 1
    return font(SERIF_B, minimum)


def badge(draw, cx, cy, r, num, fill=RED):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill)
    fnt = font(SANS_B, int(r * 1.15))
    t = str(num)
    tw = draw.textlength(t, font=fnt)
    draw.text((cx - tw / 2, cy - fnt.size / 2 - 1), t, font=fnt, fill=WHITE)


def gradient(draw, box, top, bottom, steps=28):
    x0, y0, x1, y1 = box
    h = y1 - y0
    for i in range(steps):
        c = tuple(int(top[k] + (bottom[k] - top[k]) * i / (steps - 1)) for k in range(3))
        yy0 = y0 + h * i // steps
        yy1 = y0 + h * (i + 1) // steps
        draw.rectangle([x0, yy0, x1, yy1], fill=c)


def silhouette_person(draw, cx, base, scale, suit):
    r = int(9 * scale)
    draw.ellipse([cx - r, base - int(34 * scale), cx + r, base - int(34 * scale) + 2 * r], fill=suit)
    draw.pieslice([cx - int(15 * scale), base - int(20 * scale), cx + int(15 * scale),
                   base + int(14 * scale)], 180, 360, fill=suit)


def scene_summit(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (18, 62, 96), (64, 128, 150))
    for bx, bh in [(6, 34), (44, 48), (86, 30), (210, 42), (252, 32), (150, 24)]:
        draw.rectangle([x0 + bx, y1 - 34 - bh, x0 + bx + 26, y1 - 34], fill=(16, 44, 70))
        for wy in range(y1 - 34 - bh + 6, y1 - 40, 10):
            draw.rectangle([x0 + bx + 5, wy, x0 + bx + 9, wy + 4], fill=(250, 205, 92))
            draw.rectangle([x0 + bx + 15, wy, x0 + bx + 19, wy + 4], fill=(250, 205, 92))
    draw.ellipse([x0 + 30, y1 - 36, x1 - 30, y1 - 4], fill=(10, 30, 50))
    silhouette_person(draw, x0 + 92, y1 - 12, 1.0, (178, 34, 52))
    silhouette_person(draw, x0 + 160, y1 - 10, 1.15, (240, 238, 230))
    silhouette_person(draw, x0 + 228, y1 - 12, 1.0, (36, 84, 140))


def scene_bridge(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (112, 142, 168), (196, 208, 214))
    draw.rectangle([x0, y1 - 26, x1, y1], fill=(52, 96, 138))
    for i in range(9):
        draw.line([x0 + 8 + i * 38, y1 - 6, x0 + 26 + i * 38, y1 - 6], fill=(90, 140, 180), width=2)
    deck = y0 + 44
    draw.rectangle([x0, deck, x0 + 128, deck + 7], fill=(40, 44, 50))
    draw.rectangle([x0 + 176, deck, x1, deck + 7], fill=(40, 44, 50))
    draw.arc([x0 + 96, deck - 30, x0 + 208, deck + 26], 180, 360, fill=(40, 44, 50), width=4)
    draw.line([x0 + 140, deck + 7, x0 + 152, deck + 24], fill=(40, 44, 50), width=3)
    draw.line([x0 + 176, deck + 7, x0 + 168, deck + 22], fill=(40, 44, 50), width=3)
    for px, py in [(150, 18), (162, 10), (176, 16), (188, 8)]:
        draw.ellipse([x0 + px, y0 + py, x0 + px + 22, y0 + py + 13], fill=(120, 118, 112))
    draw.polygon([(x0 + 146, deck + 8), (x0 + 160, deck + 8), (x0 + 154, deck + 20)], fill=RED)


def scene_gta(draw, box):
    x0, y0, x1, y1 = box
    gradient(draw, box, (250, 128, 92), (146, 52, 118))
    draw.ellipse([x1 - 78, y0 + 8, x1 - 34, y0 + 52], fill=(255, 214, 120))
    for bx, bh in [(4, 26), (36, 38), (70, 22), (216, 30), (252, 40), (282, 24)]:
        draw.rectangle([x0 + bx, y1 - 30 - bh, x0 + bx + 24, y1 - 30], fill=(52, 22, 62))
    for px in (26, 292):
        draw.line([x0 + px, y1 - 8, x0 + px, y1 - 44], fill=(30, 16, 36), width=4)
        for ang in (-38, -14, 12, 36):
            import math
            ex = x0 + px + int(20 * math.sin(math.radians(ang)))
            ey = y1 - 44 - int(13 * math.cos(math.radians(ang)))
            draw.line([x0 + px, y1 - 44, ex, ey], fill=(30, 90, 60), width=4)
    fnt = font(SERIF_B, 44)
    t = "VI"
    tw = draw.textlength(t, font=fnt)
    draw.text(((x0 + x1) / 2 - tw / 2, y0 + 22), t, font=fnt, fill=(255, 226, 130))
    draw.rectangle([x0 + 118, y1 - 22, x0 + 202, y1 - 12], fill=(18, 14, 24))
    draw.ellipse([x0 + 128, y1 - 16, x0 + 140, y1 - 4], fill=(200, 200, 200))
    draw.ellipse([x0 + 178, y1 - 16, x0 + 190, y1 - 4], fill=(200, 200, 200))


SCENES = {1: scene_summit, 2: scene_bridge, 3: scene_gta}

FEATURES = [
    dict(num=1, cat="ASIA · SUMMIT", src="BusinessWorld · AFP · AP", color=TEAL,
         head="Trump, Xi and Putin sit down together in Shenzhen — a first",
         body="Leaders of the world's three largest nuclear powers met three-way for the "
              "first time on Thursday, on the sidelines of the APEC summit in Shenzhen. "
              "Trump pressed for nuclear arms control; Ukraine was not on the agenda."),
    dict(num=2, cat="EUROPE · CONFLICT", src="Reuters", color=RED,
         head="Crimea Bridge attacked for the third time in a week",
         body="Traffic on the 19-kilometre bridge was halted again on Thursday after a "
              "new attack. Earlier strikes this week destroyed the central roadway "
              "section and dropped the main arch into the sea."),
    dict(num=3, cat="CULTURE · TECHNOLOGY", src="Associated Press", color=(146, 52, 118),
         head="After a 13-year wait, Grand Theft Auto VI is finally here",
         body="Worldwide release on Thursday for PlayStation 5 and Xbox Series X|S, "
              "priced at $79.99. A return to Vice City with Lucia and Jason; GTA V has "
              "sold more than 230 million copies."),
]

GRID = [
    dict(num=4, cat="MIDDLE EAST · CONFLICT", src="Sky News · AFP", color=RED, icon="tank",
         head="Israeli tanks cross Gaza's ceasefire line",
         body="First ground operation across the Yellow Line since October's ceasefire: "
              "tanks entered central Gaza as displaced families fled tents near Nuseirat. "
              "Israel said it was dismantling tunnels; Hamas called it a ceasefire breach."),
    dict(num=5, cat="ASIA · WEATHER", src="India Meteorological Department · The Hindu",
         color=BLUE, icon="storm",
         head="Cyclone Akvan closes in on India's east coast",
         body="Severe storm to make landfall around Friday noon between Narsapur and "
              "Puri, winds 90-100 km/h gusting to 110. Odisha readied 204,070 people "
              "for possible evacuation across eight districts."),
    dict(num=6, cat="UNITED STATES · POLITICS", src="AP · Reuters", color=NAVY2, icon="dome",
         head="Jeffries nominated for Speaker, a historic first",
         body="House Democrats voted 251-11 to nominate Hakeem Jeffries, on course to "
              "become the first Black Speaker of the House. The full vote is on "
              "3 January, when the new Congress convenes."),
    dict(num=7, cat="EUROPE · ECONOMY", src="Reuters · European Commission", color=GOLD,
         icon="euro",
         head="EU proposes a €45 billion loan for Ukraine",
         body="The Brussels loan for 2027 covers two-thirds of Kyiv's €70 billion "
              "funding gap - €25 billion military, €20 billion budget - repayable "
              "only after Russia pays reparations."),
    dict(num=8, cat="MARKETS", src="Reuters · Investopedia", color=(120, 84, 10), icon="chart",
         head="Gold slumps to a 14-month low",
         body="Gold fell 3% to $3,735 an ounce, its lowest since September 2025, as "
              "rate-rise bets lifted the dollar to a 19-month high. The Dow fell 560 "
              "points and the S&P 500 fell for a fifth straight session."),
    dict(num=9, cat="WORLD · SOCIETY", src="Pew Research Center · AP", color=TEAL, icon="globe",
         head="Islam to become the world's largest religion by 2035",
         body="Pew projects 2.57 billion Muslims vs 2.52 billion Christians in 2035, "
              "driven by births: 3.1 children per Muslim woman vs 2.5 per Christian "
              "woman in 2020-25."),
]

STATS = [("€45bn", "EU loan proposed\nfor Ukraine, 2027"),
         ("251-11", "House Democrats'\nJeffries nomination vote"),
         ("$3,735", "Gold per ounce,\na 14-month low"),
         ("204,070", "People readied for\nCyclone Akvan evacuation")]

ALSO = [("i", "NASA was expected to confirm on Thursday that Voyager 1's signal "
              "now takes a full 24 hours to reach Earth."),
        ("ii", "Ebola cases in DR Congo passed 11,000, with 5,400 deaths (UN)."),
        ("iii", "GTA VI topped The Game Awards with eight nominations before a "
                "single review was published."),
        ("iv", "The dollar rose to its strongest in 19 months on bets on a "
               "December Fed rate rise.")]

SOURCES = ("Reuters · Associated Press · AFP · Sky News · BBC · BusinessWorld · "
           "European Commission · India Meteorological Department · The Hindu · "
           "CNN · Investopedia · Pew Research Center")


def draw_icon(draw, kind, cx, cy):
    if kind == "tank":
        draw.rectangle([cx - 13, cy - 2, cx + 11, cy + 5], fill=INK)
        draw.rectangle([cx - 4, cy - 8, cx + 6, cy - 2], fill=INK)
        draw.line([cx + 6, cy - 6, cx + 16, cy - 6], fill=INK, width=3)
        draw.ellipse([cx - 14, cy + 4, cx + 13, cy + 11], outline=INK, width=2)
    elif kind == "storm":
        import math
        for a0 in (0, 120, 240):
            draw.arc([cx - 11, cy - 11, cx + 11, cy + 11], a0, a0 + 100, fill=BLUE, width=3)
        draw.ellipse([cx - 3, cy - 3, cx + 3, cy + 3], fill=BLUE)
    elif kind == "dome":
        draw.arc([cx - 11, cy - 16, cx + 11, cy + 2], 180, 360, fill=NAVY2, width=3)
        draw.line([cx - 13, cy + 4, cx + 13, cy + 4], fill=NAVY2, width=3)
        for dx in (-8, 0, 8):
            draw.line([cx + dx, cy + 4, cx + dx, cy + 11], fill=NAVY2, width=2)
    elif kind == "euro":
        import math
        for i in range(8):
            import math as m
            px = cx + int(11 * m.cos(m.radians(i * 45)))
            py = cy + int(11 * m.sin(m.radians(i * 45)))
            draw.ellipse([px - 2, py - 2, px + 2, py + 2], fill=GOLD)
        fnt = font(SANS_B, 15)
        draw.text((cx - 5, cy - 9), "€", font=fnt, fill=(120, 84, 10))
    elif kind == "chart":
        for i, bh in enumerate((12, 9, 6, 3)):
            draw.rectangle([cx - 13 + i * 7, cy + 11 - bh, cx - 8 + i * 7, cy + 11], fill=GOLD)
        draw.line([cx - 13, cy - 9, cx + 12, cy + 4], fill=RED, width=3)
        draw.polygon([(cx + 12, cy + 4), (cx + 5, cy + 3), (cx + 10, cy - 2)], fill=RED)
    elif kind == "globe":
        draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11], outline=TEAL, width=2)
        draw.line([cx - 11, cy, cx + 11, cy], fill=TEAL, width=1)
        draw.ellipse([cx - 5, cy - 11, cx + 5, cy + 11], outline=TEAL, width=1)


def draw_map(draw, box):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=(214, 226, 232))
    for gx in range(x0 + 30, x1, 30):
        draw.line([gx, y0, gx, y1], fill=(196, 212, 220))
    for gy in range(y0 + 20, y1, 20):
        draw.line([x0, gy, x1, gy], fill=(196, 212, 220))
    land = (148, 168, 150)
    # Simplified continent shapes (schematic editorial map).
    draw.polygon([(x0 + 18, y0 + 22), (x0 + 92, y0 + 12), (x0 + 118, y0 + 30),
                  (x0 + 96, y0 + 56), (x0 + 66, y0 + 62), (x0 + 40, y0 + 48)], fill=land)  # N America
    draw.polygon([(x0 + 88, y0 + 64), (x0 + 112, y0 + 66), (x0 + 104, y0 + 96),
                  (x0 + 88, y0 + 100)], fill=land)  # S America
    draw.polygon([(x0 + 208, y0 + 16), (x0 + 252, y0 + 12), (x0 + 258, y0 + 30),
                  (x0 + 228, y0 + 34), (x0 + 210, y0 + 28)], fill=land)  # Europe
    draw.polygon([(x0 + 224, y0 + 40), (x0 + 258, y0 + 38), (x0 + 262, y0 + 74),
                  (x0 + 240, y0 + 96), (x0 + 222, y0 + 66)], fill=land)  # Africa
    draw.polygon([(x0 + 262, y0 + 14), (x0 + 420, y0 + 10), (x0 + 448, y0 + 34),
                  (x0 + 392, y0 + 58), (x0 + 320, y0 + 60), (x0 + 268, y0 + 36)], fill=land)  # Asia
    draw.polygon([(x0 + 392, y0 + 76), (x0 + 428, y0 + 74), (x0 + 434, y0 + 92),
                  (x0 + 398, y0 + 96)], fill=land)  # Australia
    markers = {1: (0.83, 0.40), 2: (0.60, 0.22), 3: (0.265, 0.40), 4: (0.585, 0.37),
               5: (0.735, 0.47), 6: (0.255, 0.27), 7: (0.505, 0.155), 8: (0.465, 0.25),
               9: (0.405, 0.42)}
    mw, mh = x1 - x0, y1 - y0
    for num, (fx, fy) in markers.items():
        badge(draw, x0 + int(fx * mw), y0 + int(fy * mh), 9, num, fill=RED if num != 9 else NAVY2)


def build():
    img = Image.new("RGB", (W, H), IVORY)
    draw = ImageDraw.Draw(img)
    # Deterministic paper speckle.
    for i in range(900):
        px = (i * 613) % W
        py = (i * 389) % H
        if (px + py) % 7 == 0:
            draw.point((px, py), fill=(238, 231, 214))

    # Masthead.
    draw.rectangle([0, 0, W, 84], fill=NAVY)
    draw.rectangle([0, 84, W, 88], fill=GOLD)
    fnt = font(SERIF_B, 41)
    title = "THE DAY IN WORLD NEWS"
    tw = draw.textlength(title, font=fnt)
    draw.text(((W - tw) / 2, 12), title, font=fnt, fill=WHITE)
    sub = font(SANS, 11)
    s = "A ONE-PAGE BRIEFING OF THE WORLD'S DAY  ·  PREMIUM EDITORIAL EDITION"
    tw = draw.textlength(s, font=sub)
    draw.text(((W - tw) / 2, 62), s, font=sub, fill=(198, 208, 220))

    # Header row.
    draw.rectangle([MARGIN, 100, MARGIN + 74, 152], fill=NAVY)
    fnt = font(SERIF_B, 30)
    draw.text((MARGIN + 14, 102), "19", font=fnt, fill=WHITE)
    draw.text((MARGIN + 13, 134), "NOV 2026", font=font(SANS_B, 10), fill=(250, 205, 92))
    draw.text((112, 100), "Thursday 19 November 2026", font=font(SERIF_B, 25), fill=INK)
    draw.text((112, 132), "Everything on this page happened, or was first reported, on Thursday 19 November 2026.",
              font=font(SANS_I, 11), fill=GREY)
    draw.rectangle([760, 100, 1000, 152], outline=NAVY, width=2)
    draw.text((776, 110), "9 STORIES · 3 CONTINENTS ·", font=font(SANS_B, 13), fill=NAVY)
    draw.text((776, 130), "ONE PAGE", font=font(SANS_B, 13), fill=RED)
    draw.line([MARGIN, 160, 1000, 160], fill=INK, width=2)
    draw.line([MARGIN, 164, 1000, 164], fill=INK, width=1)

    # Feature panels.
    fy, fh, fw, gap = 172, 258, 320, 8
    for i, st in enumerate(FEATURES):
        x = MARGIN + i * (fw + gap)
        draw.rectangle([x, fy, x + fw, fy + fh], fill=CARD, outline=LINE, width=1)
        SCENES[st["num"]](draw, (x + 6, fy + 6, x + fw - 6, fy + 98))
        badge(draw, x + 18, fy + 116, 11, st["num"])
        draw.text((x + 36, fy + 108), st["cat"], font=font(SANS_B, 10), fill=st["color"])
        srcw = draw.textlength(st["src"], font=font(SANS, 8))
        draw.text((x + fw - 10 - srcw, fy + 109), st["src"], font=font(SANS, 8), fill=GREY)
        hf = fit_headline(draw, st["head"], fw - 20, start=16)
        y = text_block(draw, (x + 10, fy + 128), st["head"], hf, INK, fw - 20, leading=1.12, max_lines=3)
        draw.line([x + 10, y + 2, x + fw - 10, y + 2], fill=LINE, width=1)
        text_block(draw, (x + 10, y + 8), st["body"], font(SANS, 10), (52, 50, 46), fw - 20, leading=1.22)

    # Main grid: six cards, 3 x 2.
    gy, gh, gw = 442, 136, 320
    for idx, st in enumerate(GRID):
        col, row = idx % 3, idx // 3
        x = MARGIN + col * (gw + gap)
        y = gy + row * (gh + gap)
        draw.rectangle([x, y, x + gw, y + gh], fill=CARD, outline=LINE, width=1)
        draw.rectangle([x, y, x + gw, y + 4], fill=st["color"])
        badge(draw, x + 16, y + 22, 10, st["num"], fill=NAVY)
        draw.text((x + 32, y + 13), st["cat"], font=font(SANS_B, 8), fill=st["color"])
        src = st["src"]
        if draw.textlength(src, font=font(SANS, 7)) > 200:
            src = src.replace("India Meteorological Department", "IMD")
        draw.text((x + 32, y + 25), src, font=font(SANS, 7), fill=GREY)
        draw_icon(draw, st["icon"], x + gw - 22, y + 20)
        hf = fit_headline(draw, st["head"], gw - 20, start=13)
        yy = text_block(draw, (x + 10, y + 40), st["head"], hf, INK, gw - 20, leading=1.1, max_lines=2)
        text_block(draw, (x + 10, max(yy + 2, y + 68)), st["body"], font(SANS, 9), (52, 50, 46),
                   gw - 20, leading=1.18, max_lines=4)

    # Bottom section.
    by = 730
    draw.line([MARGIN, by - 6, 1000, by - 6], fill=INK, width=1)
    draw.text((MARGIN, by), "WHERE IT HAPPENED", font=font(SERIF_B, 13), fill=NAVY)
    draw_map(draw, (MARGIN, by + 24, MARGIN + 492, by + 138))
    # Stats: four boxes under the map.
    sy = by + 146
    for i, (num, label) in enumerate(STATS):
        x = MARGIN + i * 126
        wbox = 120 if i < 3 else 118
        draw.rectangle([x, sy, x + wbox, sy + 52], fill=NAVY if i == 0 else CARD,
                       outline=LINE, width=1)
        nf = font(SERIF_B, 17)
        draw.text((x + 8, sy + 4), num, font=nf, fill=(250, 205, 92) if i == 0 else NAVY)
        for j, ln in enumerate(label.split("\n")):
            draw.text((x + 8, sy + 27 + j * 10), ln, font=font(SANS, 7),
                      fill=(220, 226, 232) if i == 0 else GREY)
    # Right: ALSO ON.
    ax = 540
    draw.text((ax, by), "ALSO ON THURSDAY 19 NOVEMBER", font=font(SERIF_B, 13), fill=NAVY)
    for idx, (roman, txt) in enumerate(ALSO):
        col, row = idx % 2, idx // 2
        x = ax + col * 234
        y = by + 24 + row * 88
        draw.rectangle([x, y, x + 226, y + 82], fill=CARD, outline=LINE, width=1)
        draw.ellipse([x + 8, y + 8, x + 30, y + 30], fill=GOLD)
        rf = font(SERIF_B, 11)
        rtw = draw.textlength(roman, font=rf)
        draw.text((x + 19 - rtw / 2, y + 13), roman, font=rf, fill=NAVY)
        text_block(draw, (x + 38, y + 9), txt, font(SANS, 9), (52, 50, 46), 180, leading=1.2, max_lines=5)
    draw.text((ax, by + 192), "Numbers on this page are as reported by the sources named on each story.",
              font=font(SANS_I, 8), fill=GREY)

    # Footer.
    fy2 = 950
    draw.line([MARGIN, fy2, 1000, fy2], fill=INK, width=2)
    draw.text((MARGIN, fy2 + 8),
              "DATE CHECK — Every story on this page happened, or was first reported, on Thursday 19 November 2026.",
              font=font(SANS_B, 9), fill=INK)
    draw.text((MARGIN, fy2 + 24), "Sources: " + SOURCES, font=font(SANS, 8), fill=GREY)
    draw.text((MARGIN, fy2 + 40),
              "THE DAY IN WORLD NEWS · Thursday 19 November 2026 · Stories 1-9 as numbered on the map · End of page",
              font=font(SANS, 8), fill=GREY)
    return img


if __name__ == "__main__":
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    build().save(out, format="PNG", optimize=True)
    print(out)
