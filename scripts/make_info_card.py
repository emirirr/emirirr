#!/usr/bin/env python3
"""neofetch tarzı bilgi kartını SVG olarak üretir -> info-card.svg

Solda küçük bir terminal logosu, sağda başlık + anahtar/değer satırları.
Her satır kısa bir gecikmeyle belirir; kart, portrenin/ısı haritasının
yanında "yazılıyormuş" gibi görünür. STATIC=1 ile donmuş kare üretilir.
"""
from __future__ import annotations

import os
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "info-card.svg"
STATIC = os.environ.get("STATIC") == "1"

BG = "#0d1117"
BORDER = "#21262d"
KEY = "#39d353"        # neofetch anahtar rengi (yeşil)
ACCENT = "#58a6ff"     # başlık vurgusu
FG = "#c9d1d9"
DIM = "#7d8590"
FONT = "'SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"

TITLE = "emir@github"
ROWS = [
    ("Ad", "Emir Tiryaki"),
    ("Rol", "Full-Stack Developer"),
    ("Konum", "İstanbul · Remote / Hibrit"),
    ("Odak", "Web + Mobil · uçtan uca ürün"),
    ("Stack", "TypeScript · React / Next · Node · Python"),
    ("Veri", "PostgreSQL · MongoDB · Redis · Prisma"),
    ("Bulut", "Docker · AWS · CI/CD · Linux"),
    ("Mobil", "Swift / SwiftUI · React Native / Expo"),
    ("Markalar", "Tiryaki Yazılım · Odak Software · Kodlasa"),
    ("Deneyim", "5+ yıl · 50+ proje · 25+ teknoloji"),
    ("Web", "emirtiryaki.com"),
    ("İletişim", "info@emirtiryaki.com"),
]
PALETTE = ["#39d353", "#58a6ff", "#ff5f56", "#ffbd2e",
           "#bc8cff", "#39c5cf", "#c9d1d9", "#7d8590"]

TITLE_H = 30
PAD_T = TITLE_H + 26
ROW_H = 22
LOGO_X = 26
LOGO_W = 132
COL_X = LOGO_X + LOGO_W + 28   # anahtar sütunu başlangıcı
KEY_W = 92                     # anahtar/değer arası boşluk
WIDTH = 660


def anim(delay: float) -> str:
    """Animasyonlu eleman için class+style döndürür (mono dahil)."""
    if STATIC:
        return 'class="mono" style="opacity:1"'
    return f'class="mono row" style="animation-delay:{delay}s"'


def build() -> str:
    # dikey yerleşimi önce hesapla ki yükseklik içeriği tam kapsasın
    ty = PAD_T + 4               # başlık satırı taban çizgisi
    start_y = ty + 42            # ilk anahtar/değer satırı
    pal_y = start_y + len(ROWS) * ROW_H - 6   # renk paleti satırı
    logo_bottom = PAD_T + 6 + 118
    height = max(pal_y + 15, logo_bottom) + 20
    p: list[str] = []
    p.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-label="{TITLE} neofetch kartı">'
    )

    style = (
        "<style>"
        ".mono{font-family:" + FONT + ";}"
    )
    if not STATIC:
        style += (
            "@keyframes rowIn{from{opacity:0;transform:translateX(8px);}"
            "to{opacity:1;transform:none;}}"
            ".row{opacity:0;animation:rowIn .45s ease forwards;}"
            "@keyframes blink{50%{opacity:0;}}"
            ".cursor{animation:blink 1.05s step-end infinite;}"
            "@media(prefers-reduced-motion:reduce){.row{animation:none;opacity:1;transform:none;}"
            ".cursor{animation:none;}}"
        )
    style += "</style>"
    p.append(style)

    # kart
    p.append(
        f'<rect x="0" y="0" width="{WIDTH}" height="{height}" rx="10" fill="{BG}"/>'
        f'<rect x=".5" y=".5" width="{WIDTH-1}" height="{height-1}" rx="10" '
        f'fill="none" stroke="{BORDER}"/>'
    )

    # pencere çubuğu
    for i, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        p.append(f'<circle cx="{18 + i*16}" cy="16" r="5" fill="{color}"/>')
    p.append(
        f'<text x="{WIDTH/2}" y="20" text-anchor="middle" class="mono" '
        f'font-size="12" fill="{DIM}">{TITLE}:~$ neofetch</text>'
    )
    p.append(f'<line x1="0" y1="{TITLE_H}" x2="{WIDTH}" y2="{TITLE_H}" stroke="{BORDER}"/>')

    # --- sol terminal logosu ---
    lx, ly, lw, lh = LOGO_X, PAD_T + 6, LOGO_W, 118
    p.append(
        f'<rect x="{lx}" y="{ly}" width="{lw}" height="{lh}" rx="8" '
        f'fill="#010409" stroke="{KEY}" stroke-width="1.5"/>'
    )
    for i, color in enumerate(("#ff5f56", "#ffbd2e", "#27c93f")):
        p.append(f'<circle cx="{lx + 14 + i*13}" cy="{ly + 15}" r="4" fill="{color}"/>')
    p.append(f'<line x1="{lx}" y1="{ly+28}" x2="{lx+lw}" y2="{ly+28}" stroke="{KEY}" stroke-opacity=".4"/>')
    p.append(
        f'<text x="{lx + 14}" y="{ly + 58}" class="mono" font-size="16" fill="{KEY}">'
        f'&gt; dev<tspan class="cursor" fill="{FG}">_</tspan></text>'
    )
    p.append(
        f'<text x="{lx + 14}" y="{ly + 84}" class="mono" font-size="11" fill="{DIM}">'
        f'~/istanbul</text>'
    )
    p.append(
        f'<text x="{lx + 14}" y="{ly + 104}" class="mono" font-size="11" fill="{ACCENT}">'
        f'building...</text>'
    )

    # başlık satırı: emir@github
    user, host = TITLE.split("@")
    ty = PAD_T + 4
    p.append(
        f'<text x="{COL_X}" y="{ty}" font-size="14" {anim(0.0)}>'
        f'<tspan fill="{KEY}" font-weight="bold">{user}</tspan>'
        f'<tspan fill="{DIM}">@</tspan>'
        f'<tspan fill="{ACCENT}" font-weight="bold">{host}</tspan></text>'
    )
    p.append(
        f'<text x="{COL_X}" y="{ty + 16}" font-size="12" fill="{DIM}" '
        f'{anim(0.05)}>{"-" * 26}</text>'
    )

    # anahtar/değer satırları
    start_y = ty + 42
    for i, (key, val) in enumerate(ROWS):
        y = start_y + i * ROW_H
        delay = round(0.12 + i * 0.06, 3)
        p.append(
            f'<text x="{COL_X}" y="{y}" font-size="12.5" {anim(delay)}>'
            f'<tspan fill="{KEY}" font-weight="bold">{escape(key)}</tspan>'
            f'<tspan fill="{DIM}"> ~ </tspan>'
            f'<tspan x="{COL_X + KEY_W}" fill="{FG}">{escape(val)}</tspan></text>'
        )

    # neofetch renk paleti kareleri
    pal_y = start_y + len(ROWS) * ROW_H - 6
    for i, color in enumerate(PALETTE):
        p.append(
            f'<rect x="{COL_X + i*20}" y="{pal_y}" width="15" height="15" rx="3" '
            f'fill="{color}" {anim(round(0.12 + len(ROWS)*0.06 + i*0.04, 3))}/>'
        )

    p.append("</svg>")
    return "".join(p)


def main() -> int:
    OUT.write_text(build(), encoding="utf-8")
    tag = " (STATIC)" if STATIC else ""
    print(f"OK{tag} -> {OUT} ({OUT.stat().st_size:,} bayt)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
