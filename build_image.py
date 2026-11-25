#!/usr/bin/env python3
"""Render the 25 November 2026 front page for make.fun news-image-20261125.

High-density newspaper front page following the Round 3 top-ranked
pattern: 39 stories across 6 regions, a world map, a KPI numbers bar, a
UTC timeline, a red-box DATE CHECK, 3 illustrated lead headlines plus
small illustrations, a region distribution bar, and Reuters/AP source
labels. 1024x1024, deterministic, no network, no randomness.
"""
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
BACKGROUND = (251, 247, 238)
FOREGROUND = (20, 20, 20)
ACCENT = (176, 30, 40)
DEEP = (22, 35, 63)
MUTED = (90, 88, 82)
BODY_INK = (52, 50, 46)
WHITE = (255, 255, 255)
MAP_FILL = (178, 198, 214)
MAP_LINE = (70, 95, 120)
KPI_BG = (240, 235, 224)

SERIF_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"

GUTTER = 46
CONTENT_W = PAGE_W - 2 * GUTTER
COL_W = (CONTENT_W - 28) // 3
COL_X = [GUTTER, GUTTER + COL_W + 14, GUTTER + 2 * (COL_W + 14)]

LEADS = [
    {
        "kicker": "SPACE  ·  CHINA",
        "headline": "FIRST FOREIGNER ABOARD TIANGONG",
        "deck": ("Shenzhou-24 lifts off at 08:18 with Tang Hongbo, Wu Yi "
                 "and Pakistan's Muhammad Zeeshan Ali — first foreigner "
                 "on Tiangong."),
        "icon": "rocket",
        "tint": (214, 230, 242),
        "source": "Reuters / Xinhua",
    },
    {
        "kicker": "CYBER  ·  USA",
        "headline": "CIA AND ODNI HACKED",
        "deck": ("Intruders breach the unclassified open-source network "
                 "used by the CIA and ODNI; no classified data hit. The "
                 "FBI crime database was probed too."),
        "icon": "shield",
        "tint": (244, 220, 218),
        "source": "NYT / CNN",
    },
    {
        "kicker": "MIDDLE EAST  ·  SAUDI ARABIA",
        "headline": "HOUTHIS HIT RIYADH'S TALLEST TOWER",
        "deck": ("Second strike on the capital's financial-district "
                 "landmark in under a week; 11 wounded as the kingdom's "
                 "air defences face a new test."),
        "icon": "tower",
        "tint": (250, 232, 205),
        "source": "SCMP / Reuters",
    },
]

KPIS = [
    ("08:18", "SHENZHOU-24 LIFTOFF"),
    ("11", "WOUNDED IN RIYADH"),
    ("5.6", "NEPAL QUAKE MAGNITUDE"),
    ("7,000", "LANDMINE VICTIMS, 2025"),
    ("5 / HR", "WOMEN KILLED BY FAMILY"),
]

REGIONS = [
    ("ASIA", "9", [
        ("NEPAL QUAKE M5.6, NO CASUALTIES", "quake"),
        ("CHINA COBALT FIRMS RACE CONGO BAN", None),
        ("N. KOREA THREATENS SWISS OFFICE", None),
        ("SEOUL SUBWAY DEAL, STRIKE OFF", None),
        ("XIAMEN AIR ORDERS 50 BOEING 737-8s", None),
        ("PAKISTAN EYES $1.21BN PAYOUT", None),
        ("US SOLDIER ADMITS SELLING SECRETS", None),
        ("SOLOMON IS. BARS FOREIGN BASES", None),
    ]),
    ("MIDDLE EAST", "6", [
        ("SAUDI JETS STRIKE HODEIDAH PORT", "flame"),
        ("HAMAS SECURITY CHIEF KILLED", None),
        ("IRAN MEDICINE SHORTAGE BITES", None),
        ("IRAQ TO SEIZE KURDISH OILFIELDS", None),
        ("BRITAIN SANCTIONS HOUTHIS", None),
    ]),
    ("EUROPE", "8", [
        ("COP31 COLLAPSES — FIRST SINCE 2009", "globe"),
        ("ZELENSKIY: WE HIT RUSSIAN SHIP", "ship"),
        ("UKRAINE STRIKES BEYOND EUROPE", None),
        ("SARKOZY CORRUPTION TRIAL ORDERED", None),
        ("2 HELD OVER PRINCE WILLIAM BREAK-IN", None),
        ("PELICOT SLAMS PUBLISHER", None),
        ("DENMARK UPHOLDS 'GHETTO' EVICTIONS", None),
        ("NORWAY BARS RUSSIAN SKATERS", None),
    ]),
    ("AMERICAS", "8", [
        ("FBI CRIME DATABASE ALSO BREACHED", "shield"),
        ("TRUMP GIVES GIULIANI TOP HONOUR", "medal"),
        ("FORT HOOD GUNMAN SEEKS STAY", None),
        ("O'HARE RADAR DELAYS FLIGHTS", None),
        ("TRUMP SPARES TURKEYS FOR THANKSGIVING", None),
        ("COLOMBIA SUPERMARKET HOSTAGES", None),
        ("CAR BOMB INJURES 23 IN COLOMBIA", None),
    ]),
    ("AFRICA", "4", [
        ("DR CONGO REBELS PULL BACK", "flame"),
        ("SENEGAL GETS AFCON TITLE BACK", None),
        ("NIGERIAN EMIR SUSPENDED", None),
        ("CAMEROON REBEL LEADER IN COURT", None),
    ]),
    ("GLOBAL", "4", [
        ("UN: 5 WOMEN KILLED EVERY HOUR", "globe"),
        ("UN CHIEF URGES AI SAFETY TALKS", None),
        ("WHO: END US FUEL BLOCKADE ON CUBA", None),
        ("REAL MADRID THRASH PSV 5-1", "ball"),
    ]),
]

DIST = [("ASIA", 9), ("MIDDLE EAST", 6), ("EUROPE", 8),
        ("AMERICAS", 8), ("AFRICA", 4), ("GLOBAL", 4)]
DIST_COLORS = [(176, 30, 40), (214, 110, 30), (22, 35, 63),
               (40, 110, 70), (120, 70, 140), (90, 88, 82)]

MAP_W, MAP_H = CONTENT_W, 92
CONTINENTS = [
    [(40, 18), (120, 7), (200, 13), (230, 27), (210, 50), (170, 63),
     (140, 85), (90, 90), (50, 63), (30, 36)],
    [(250, 4), (280, 2), (295, 11), (270, 18), (250, 11)],
    [(210, 67), (250, 62), (280, 71), (270, 93), (240, 98),
     (215, 84)],
    [(430, 13), (470, 7), (500, 16), (490, 31), (460, 36),
     (440, 27)],
    [(440, 40), (490, 36), (520, 49), (510, 76), (480, 93),
     (450, 80), (435, 58)],
    [(510, 9), (650, 4), (780, 13), (850, 27), (820, 54), (750, 67),
     (680, 62), (600, 54), (540, 36), (510, 22)],
    [(760, 80), (820, 76), (850, 84), (820, 95), (770, 93),
     (750, 87)],
]
MARKERS = [
    (720, 34, "JIUQUAN"), (575, 62, "RIYADH"), (150, 38, "LANGLEY"),
    (680, 47, "NEPAL"), (532, 42, "GAZA"), (490, 23, "KYIV"),
]


def load(path, size):
    return ImageFont.truetype(path, size)


def fit_lines(draw, text, font, width):
    done, current = [], ""
    for word in text.split(" "):
        candidate = (current + " " + word).strip()
        if draw.textlength(candidate, font=font) <= width:
            current = candidate
        else:
            if current:
                done.append(current)
            current = word
    if current:
        done.append(current)
    return done


def put_centred(draw, cx, y, text, font, fill=FOREGROUND):
    wide = draw.textlength(text, font=font)
    draw.text((cx - wide / 2, y), text, font=font, fill=fill)
    return y + font.size


def hrule(draw, y, x0=GUTTER, x1=PAGE_W - GUTTER, weight=1, fill=FOREGROUND):
    draw.rectangle([x0, y, x1, y + weight - 1], fill=fill)
    return y + weight


def icon_rocket(draw, x, y, s, ink=DEEP):
    draw.polygon([(x + s * .5, y), (x + s * .72, y + s * .35),
                  (x + s * .28, y + s * .35)], fill=ink)
    draw.rectangle([x + s * .32, y + s * .32, x + s * .68, y + s * .72],
                   fill=ink)
    draw.polygon([(x + s * .32, y + s * .72), (x + s * .12, y + s * .88),
                  (x + s * .32, y + s * .82)], fill=ink)
    draw.polygon([(x + s * .68, y + s * .72), (x + s * .88, y + s * .88),
                  (x + s * .68, y + s * .82)], fill=ink)
    draw.polygon([(x + s * .42, y + s * .72), (x + s * .58, y + s * .72),
                  (x + s * .5, y + s)], fill=ACCENT)
    draw.ellipse([x + s * .42, y + s * .42, x + s * .58, y + s * .58],
                 fill=WHITE)


def icon_shield(draw, x, y, s, ink=ACCENT):
    draw.polygon([(x + s * .5, y), (x + s * .95, y + s * .18),
                  (x + s * .95, y + s * .55), (x + s * .5, y + s),
                  (x + s * .05, y + s * .55), (x + s * .05, y + s * .18)],
                 outline=ink, width=max(2, s // 12))
    draw.ellipse([x + s * .4, y + s * .32, x + s * .6, y + s * .52],
                 fill=ink)
    draw.rectangle([x + s * .46, y + s * .5, x + s * .54, y + s * .72],
                   fill=ink)


def icon_tower(draw, x, y, s, ink=FOREGROUND):
    draw.rectangle([x + s * .38, y + s * .2, x + s * .62, y + s], fill=ink)
    draw.polygon([(x + s * .5, y), (x + s * .62, y + s * .2),
                  (x + s * .38, y + s * .2)], fill=ink)
    for yy in (0.35, 0.5, 0.65, 0.8):
        draw.line([x + s * .38, y + s * yy, x + s * .62, y + s * yy],
                  fill=WHITE, width=1)
    draw.line([x + s * .7, y + s * .1, x + s * .85, y], fill=ACCENT, width=2)
    draw.line([x + s * .72, y + s * .22, x + s * .9, y + s * .18],
              fill=ACCENT, width=2)


def icon_quake(draw, x, y, s, ink=FOREGROUND):
    pts = [(x, y + s * .2), (x + s * .25, y + s * .45),
           (x + s * .45, y + s * .25), (x + s * .65, y + s * .6),
           (x + s * .85, y + s * .4), (x + s, y + s * .7)]
    draw.line(pts, fill=ink, width=max(2, s // 10), joint="curve")
    draw.line([(x + s * .1, y + s * .8), (x + s * .4, y + s * .95),
               (x + s * .7, y + s * .8)], fill=ACCENT, width=max(2, s // 10))


def icon_globe(draw, x, y, s, ink=DEEP):
    draw.ellipse([x, y, x + s, y + s], outline=ink, width=max(2, s // 12))
    draw.ellipse([x + s * .3, y, x + s * .7, y + s], outline=ink, width=1)
    draw.line([x, y + s * .5, x + s, y + s * .5], fill=ink, width=1)
    draw.arc([x, y + s * .18, x + s, y + s * .82], 200, 340, fill=ink, width=1)
    draw.arc([x, y + s * .18, x + s, y + s * .82], 20, 160, fill=ink, width=1)


def icon_ship(draw, x, y, s, ink=DEEP):
    draw.polygon([(x, y + s * .55), (x + s, y + s * .55),
                  (x + s * .85, y + s * .85), (x + s * .15, y + s * .85)],
                 fill=ink)
    draw.rectangle([x + s * .45, y + s * .1, x + s * .55, y + s * .55],
                   fill=ink)
    draw.line([x + s * .05, y + s * .95, x + s * .95, y + s * .95],
              fill=MAP_LINE, width=2)


def icon_medal(draw, x, y, s, ink=ACCENT):
    draw.polygon([(x + s * .3, y), (x + s * .7, y),
                  (x + s * .58, y + s * .35), (x + s * .42, y + s * .35)],
                 fill=ink)
    draw.ellipse([x + s * .2, y + s * .35, x + s * .8, y + s * .95],
                 outline=ink, width=max(2, s // 12))
    draw.text((x + s * .38, y + s * .5), "1", font=load(SANS_BOLD, s // 3),
              fill=ink)


def icon_flame(draw, x, y, s, ink=(214, 110, 30)):
    draw.polygon([(x + s * .5, y), (x + s * .85, y + s * .45),
                  (x + s * .95, y + s * .7), (x + s * .7, y + s),
                  (x + s * .3, y + s), (x + s * .05, y + s * .7),
                  (x + s * .15, y + s * .45)], fill=ink)
    draw.polygon([(x + s * .5, y + s * .45), (x + s * .68, y + s * .68),
                  (x + s * .5, y + s * .85), (x + s * .32, y + s * .68)],
                 fill=(250, 232, 205))


def icon_ball(draw, x, y, s, ink=FOREGROUND):
    draw.ellipse([x, y, x + s, y + s], outline=ink, width=max(2, s // 12))
    draw.polygon([(x + s * .5, y + s * .3), (x + s * .68, y + s * .45),
                  (x + s * .6, y + s * .68), (x + s * .4, y + s * .68),
                  (x + s * .32, y + s * .45)], fill=ink)


ICONS = {"rocket": icon_rocket, "shield": icon_shield, "tower": icon_tower,
         "quake": icon_quake, "globe": icon_globe, "ship": icon_ship,
         "medal": icon_medal, "flame": icon_flame, "ball": icon_ball}


def draw_globe(draw, cx, cy, radius):
    draw.ellipse([cx - radius, cy - radius, cx + radius, cy + radius],
                 outline=FOREGROUND, width=3)
    draw.ellipse([cx - 10, cy - radius, cx + 10, cy + radius],
                 outline=FOREGROUND, width=2)
    draw.line([cx - radius, cy, cx + radius, cy], fill=FOREGROUND, width=2)
    draw.arc([cx - radius, cy - 14, cx + radius, cy + 14], 200, 340,
             fill=FOREGROUND, width=2)
    draw.arc([cx - radius, cy - 14, cx + radius, cy + 14], 20, 160,
             fill=FOREGROUND, width=2)


def draw_masthead(draw):
    cx = PAGE_W // 2
    draw_globe(draw, 66, 62, 17)
    draw.rectangle([812, 36, 992, 76], fill=ACCENT)
    draw.text((822, 42), "DATE CHECK", font=load(SANS_BOLD, 15), fill=WHITE)
    draw.text((822, 60), "25 NOV 2026 · UTC", font=load(SANS_BOLD, 12),
              fill=WHITE)
    put_centred(draw, cx, 40, "THE WORLD IN ONE IMAGE",
                load(SERIF_BOLD, 34))
    put_centred(draw, cx, 86, "T U E S D A Y ,  2 5  N O V E M B E R  2 0 2 6",
                load(SANS_BOLD, 16), fill=ACCENT)
    y = hrule(draw, 110, weight=3)
    y = hrule(draw, y + 4, weight=1)
    return y + 8


def draw_kpi(draw, y):
    h = 34
    draw.rectangle([GUTTER, y, PAGE_W - GUTTER, y + h], fill=KPI_BG)
    cell_w = CONTENT_W // len(KPIS)
    for i, (num, label) in enumerate(KPIS):
        x = GUTTER + i * cell_w
        if i:
            draw.line([x, y + 5, x, y + h - 5], fill=MUTED, width=1)
        draw.text((x + 8, y + 3), num, font=load(SANS_BOLD, 17),
                  fill=ACCENT)
        draw.text((x + 8, y + 20), label, font=load(SANS_BOLD, 9),
                  fill=BODY_INK)
    return y + h + 8


def draw_leads(draw, y):
    box_h = 84
    for idx, lead in enumerate(LEADS):
        x = COL_X[idx]
        draw.rectangle([x, y, x + COL_W, y + box_h], fill=lead["tint"],
                       outline=FOREGROUND, width=1)
        ICONS[lead["icon"]](draw, x + COL_W // 2 - 30, y + 12, 60)
        draw.text((x + 8, y + box_h - 18), lead["source"],
                  font=load(SANS_BOLD, 10), fill=MUTED)
        yy = y + box_h + 8
        draw.text((x, yy), lead["kicker"], font=load(SANS_BOLD, 14),
                  fill=ACCENT)
        yy += 22
        head_font = load(SERIF_BOLD, 25)
        for line in fit_lines(draw, lead["headline"], head_font, COL_W)[:2]:
            draw.text((x, yy), line, font=head_font, fill=FOREGROUND)
            yy += 30
        yy += 2
        deck_font = load(SANS, 13)
        for line in fit_lines(draw, lead["deck"], deck_font, COL_W)[:3]:
            draw.text((x, yy), line, font=deck_font, fill=BODY_INK)
            yy += 17
    return y + box_h + 8 + 22 + 60 + 2 + 51 + 6


def draw_map(draw, y):
    label_font = load(SANS_BOLD, 13)
    draw.text((GUTTER, y), "THE WORLD TODAY", font=label_font, fill=DEEP)
    right = "6 REGIONS · 39 STORIES"
    draw.text((PAGE_W - GUTTER - draw.textlength(right, font=label_font), y),
              right, font=label_font, fill=ACCENT)
    my = y + 18
    draw.rectangle([GUTTER, my, GUTTER + MAP_W, my + MAP_H],
                   fill=(232, 240, 246), outline=FOREGROUND, width=1)
    for poly in CONTINENTS:
        pts = [(GUTTER + px, my + py) for px, py in poly]
        draw.polygon(pts, fill=MAP_FILL, outline=MAP_LINE)
    for mx, myy, label in MARKERS:
        cx, cy = GUTTER + mx, my + myy
        draw.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=ACCENT,
                     outline=WHITE, width=1)
        draw.text((cx + 6, cy - 6), label, font=load(SANS_BOLD, 9),
                  fill=ACCENT)
    return my + MAP_H + 6


def draw_timeline(draw, y):
    label_font = load(SANS_BOLD, 13)
    draw.text((GUTTER, y), "UTC TIMELINE — TUESDAY 25 NOVEMBER",
              font=label_font, fill=DEEP)
    line_y = y + 34
    x0, x1 = GUTTER, PAGE_W - GUTTER
    draw.line([x0, line_y, x1, line_y], fill=FOREGROUND, width=2)
    for h in (0, 4, 8, 12, 16, 20):
        tx = x0 + (x1 - x0) * h / 24
        draw.line([tx, line_y - 4, tx, line_y + 4], fill=FOREGROUND, width=2)
        draw.text((tx - 10, line_y + 8), f"{h:02d}:00", font=load(SANS, 10),
                  fill=MUTED)
    # events: (hour, label, above_line?)
    for h, label, above in [(0.3, "00:18 SHENZHOU-24 LIFTOFF", True),
                            (1.53, "01:32 NEPAL QUAKE", False),
                            (6.0, "06:00 RIYADH TOWER HIT", True)]:
        tx = x0 + (x1 - x0) * h / 24
        draw.ellipse([tx - 4, line_y - 4, tx + 4, line_y + 4], fill=ACCENT)
        if above:
            draw.text((tx - 4, line_y - 18), label,
                      font=load(SANS_BOLD, 10), fill=ACCENT)
        else:
            draw.text((tx - 4, line_y + 22), label,
                      font=load(SANS_BOLD, 10), fill=ACCENT)
    return line_y + 32


def draw_regions(draw, y, row_regions, row_h):
    for idx, (name, count, stories) in enumerate(row_regions):
        x = COL_X[idx]
        draw.rectangle([x, y, x + COL_W, y + 20], fill=DEEP)
        draw.text((x + 6, y + 3), name, font=load(SANS_BOLD, 13),
                  fill=WHITE)
        cnt = f"{count} STORIES"
        draw.text((x + COL_W - 6 - draw.textlength(cnt,
                   font=load(SANS_BOLD, 10)), y + 5), cnt,
                  font=load(SANS_BOLD, 10), fill=WHITE)
        yy = y + 28
        for headline, icon in stories:
            tx = x
            if icon:
                ICONS[icon](draw, x, yy + 1, 14)
                tx = x + 20
            font = load(SANS, 13)
            line = headline
            while draw.textlength(line, font=font) > COL_W - (tx - x):
                line = line.rsplit(" ", 1)[0]
            draw.text((tx, yy), line, font=font, fill=BODY_INK)
            yy += 17
    return y + row_h


def draw_distribution(draw, y):
    label_font = load(SANS_BOLD, 12)
    draw.text((GUTTER, y), "STORIES BY REGION", font=label_font, fill=DEEP)
    y += 18
    total = sum(n for _, n in DIST)
    bx, bw, bh = GUTTER, CONTENT_W, 16
    xx = bx
    for (name, n), color in zip(DIST, DIST_COLORS):
        w = bw * n // total
        draw.rectangle([xx, y, xx + w - 1, y + bh], fill=color)
        xx += w
    draw.rectangle([bx, y, bx + bw, y + bh], outline=FOREGROUND, width=1)
    y += bh + 5
    lx = GUTTER
    for (name, n), color in zip(DIST, DIST_COLORS):
        draw.rectangle([lx, y, lx + 10, y + 10], fill=color)
        txt = f"{name} {n}"
        draw.text((lx + 13, y - 1), txt, font=load(SANS_BOLD, 10),
                  fill=BODY_INK)
        lx += 13 + draw.textlength(txt, font=load(SANS_BOLD, 10)) + 14
    return y + 12


def render():
    page = Image.new("RGB", (PAGE_W, PAGE_H), BACKGROUND)
    draw = ImageDraw.Draw(page)
    draw.rectangle([12, 12, PAGE_W - 13, PAGE_H - 13], outline=FOREGROUND,
                   width=2)
    draw.rectangle([20, 20, PAGE_W - 21, PAGE_H - 21], outline=FOREGROUND,
                   width=1)
    y = draw_masthead(draw)
    y = draw_kpi(draw, y)
    y = draw_leads(draw, y)
    y = draw_map(draw, y)
    y = draw_timeline(draw, y)
    y = draw_regions(draw, y, REGIONS[:3], 168)
    y = draw_regions(draw, y + 4, REGIONS[3:], 148)
    y = draw_distribution(draw, y + 4)
    hrule(draw, y + 6)
    put_centred(draw, PAGE_W // 2, y + 10,
                "Sources: Reuters · AP · Xinhua · NYT · CNN · SCMP · Kathmandu Post",
                load(SANS, 13), fill=MUTED)
    put_centred(draw, PAGE_W // 2, y + 26,
                "Compiled from the day's reporting  ·  25 November 2026",
                load(SANS, 13), fill=MUTED)
    return page


def main():
    image = render()
    image.save("entry.png", "PNG", optimize=True)
    print("saved entry.png", image.size)


if __name__ == "__main__":
    main()
