#!/usr/bin/env python3
"""data/contributions.json -> contrib-heatmap.svg

Klasik 53 hafta x 7 gün takvimini, köşegen boyunca sırayla beliren
yuvarlak kutular olarak çizer. Animasyon SVG'nin içinde CSS keyframe
olarak yaşar; yüklenince bir kez oynar ve donar (döngü yok).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "contrib-heatmap.svg"

# none -> en parlak (seviye 5 neon üst uç)
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 15          # kutu + boşluk
BOX = 11
RADIUS = 2.5
TITLE_H = 30       # pencere çubuğu
MONTH_H = 16       # ay etiketleri
PAD_L = 34
PAD_R = 18
PAD_B = 52         # açıklama + istatistik alt bilgisi
BG = "#0d1117"
FG = "#7d8590"
FG_BRIGHT = "#c9d1d9"
FONT = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

WEEKDAYS = {1: "Pzt", 3: "Çar", 5: "Cum"}  # Pazar=0 tabanlı satır index'i
MONTHS_TR = ["Oca", "Şub", "Mar", "Nis", "May", "Haz",
             "Tem", "Ağu", "Eyl", "Eki", "Kas", "Ara"]


def tr_int(n: int) -> str:
    return f"{n:,}".replace(",", ".")


def eff_level(day: dict, max_count: int) -> int:
    """En yoğun günlere neon üst ucu (seviye 5) ver."""
    lvl = int(day["level"])
    if max_count and day["count"] >= max_count * 0.6:
        return 5
    return min(lvl, 4)


def build() -> str:
    data = json.loads(DATA.read_text(encoding="utf-8"))
    days = data["days"]
    weeks = data["weeks"]
    max_count = data.get("max_count", 0)
    stats = data.get("stats", {})

    grid_w = weeks * CELL
    grid_h = 7 * CELL
    grid_x = PAD_L
    grid_y = TITLE_H + MONTH_H
    width = PAD_L + grid_w + PAD_R
    height = grid_y + grid_h + PAD_B

    parts: list[str] = []
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" '
        f'aria-label="{data["username"]} GitHub katkı takvimi">'
    )

    # --- stil + animasyon ---
    parts.append(
        "<style>"
        "@keyframes cellIn{from{opacity:0;transform:translateY(-6px) scale(.4);}"
        "to{opacity:1;transform:none;}}"
        "@keyframes fadeIn{from{opacity:0;}to{opacity:1;}}"
        ".cell{opacity:0;transform-box:fill-box;transform-origin:center;"
        "animation:cellIn .5s cubic-bezier(.2,.8,.2,1) forwards;}"
        ".meta{opacity:0;animation:fadeIn .6s ease forwards;}"
        ".mono{font-family:" + FONT + ";}"
        "@media(prefers-reduced-motion:reduce){"
        ".cell,.meta{animation:none;opacity:1;transform:none;}}"
        "</style>"
    )

    # arka plan kartı
    parts.append(
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="10" fill="{BG}"/>'
        f'<rect x=".5" y=".5" width="{width-1}" height="{height-1}" rx="10" '
        f'fill="none" stroke="#21262d" stroke-width="1"/>'
    )

    # neon parıltı filtresi
    parts.append(
        '<defs><filter id="glow" x="-50%" y="-50%" width="200%" height="200%">'
        '<feGaussianBlur stdDeviation="1.4" result="b"/>'
        '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>'
        '</filter></defs>'
    )

    # pencere çubuğu
    for i, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        parts.append(f'<circle cx="{18 + i*16}" cy="16" r="5" fill="{color}"/>')
    parts.append(
        f'<text x="{width/2}" y="20" text-anchor="middle" class="mono" '
        f'font-size="12" fill="{FG}">emir@github ~/contributions --live</text>'
    )

    # ay etiketleri (bir sütundaki ilk günün ayına göre)
    col_month: dict[int, int] = {}
    for d in days:
        c = d["col"]
        m = int(d["date"][5:7])
        col_month.setdefault(c, m)
    last_m = None
    month_row = []
    for c in range(weeks):
        m = col_month.get(c)
        if m and m != last_m:
            x = grid_x + c * CELL
            month_row.append(
                f'<text x="{x}" y="{TITLE_H + 11}" class="mono meta" font-size="10" '
                f'fill="{FG}" style="animation-delay:.2s">{MONTHS_TR[m-1]}</text>'
            )
            last_m = m
    parts.extend(month_row)

    # haftanın günü etiketleri
    for row, label in WEEKDAYS.items():
        y = grid_y + row * CELL + BOX - 1
        parts.append(
            f'<text x="{grid_x - 8}" y="{y}" text-anchor="end" class="mono meta" '
            f'font-size="9" fill="{FG}" style="animation-delay:.2s">{label}</text>'
        )

    # hücreler
    for d in days:
        lvl = eff_level(d, max_count)
        x = grid_x + d["col"] * CELL
        y = grid_y + d["row"] * CELL
        delay = round((d["col"] + d["row"]) * 0.018, 3)
        extra = ' filter="url(#glow)"' if lvl == 5 else ""
        parts.append(
            f'<rect class="cell" x="{x}" y="{y}" width="{BOX}" height="{BOX}" '
            f'rx="{RADIUS}" fill="{PALETTE[lvl]}"{extra} '
            f'style="animation-delay:{delay}s"><title>{d["date"]}: '
            f'{d["count"]} katkı</title></rect>'
        )

    # açıklama (Az -> Çok)
    legend_y = grid_y + grid_h + 20
    legend_x = width - PAD_R - (6 * (BOX + 3)) - 60
    parts.append(
        f'<text x="{legend_x - 6}" y="{legend_y + BOX - 2}" text-anchor="end" '
        f'class="mono meta" font-size="10" fill="{FG}" '
        f'style="animation-delay:1.2s">Az</text>'
    )
    for i, color in enumerate(PALETTE):
        lx = legend_x + i * (BOX + 3)
        parts.append(
            f'<rect class="meta" x="{lx}" y="{legend_y}" width="{BOX}" height="{BOX}" '
            f'rx="{RADIUS}" fill="{color}" style="animation-delay:1.2s"/>'
        )
    parts.append(
        f'<text x="{legend_x + 6*(BOX+3) + 4}" y="{legend_y + BOX - 2}" '
        f'class="mono meta" font-size="10" fill="{FG}" '
        f'style="animation-delay:1.2s">Çok</text>'
    )

    # istatistik alt bilgisi
    total = data.get("total", 0)
    cur = stats.get("current_streak", 0)
    longest = stats.get("longest_streak", 0)
    footer = (
        f"{tr_int(total)} katkı · son 1 yıl    "
        f"güncel seri {cur} gün · en uzun {longest} gün"
    )
    parts.append(
        f'<text x="{PAD_L}" y="{legend_y + BOX - 2}" class="mono meta" '
        f'font-size="11" fill="{FG_BRIGHT}" style="animation-delay:1.3s">{footer}</text>'
    )

    parts.append("</svg>")
    return "".join(parts)


def main() -> int:
    OUT.write_text(build(), encoding="utf-8")
    print(f"OK -> {OUT} ({OUT.stat().st_size:,} bayt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
