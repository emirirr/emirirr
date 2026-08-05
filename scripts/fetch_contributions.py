#!/usr/bin/env python3
"""GitHub katkı takvimini token'sız çeker.

GitHub, profil sayfasının kullandığı katkı takvimini herkese açık HTML olarak
https://github.com/users/<username>/contributions adresinde servis eder.
GraphQL API'ye veya kişisel erişim token'ına gerek yoktur.

Çıktı: data/contributions.json — ham günler + türetilmiş istatistikler.
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup

USERNAME = os.environ.get("GH_USERNAME", "emirirr")
URL = f"https://github.com/users/{USERNAME}/contributions"
OUT = Path(__file__).resolve().parent.parent / "data" / "contributions.json"

_COUNT_RE = re.compile(r"^([\d,]+)\s+contribution")


def _count_from_tooltip(text: str) -> int:
    """'3 contributions on August 10th.' -> 3 ; 'No contributions ...' -> 0."""
    if not text:
        return 0
    m = _COUNT_RE.match(text.strip())
    if not m:
        return 0
    return int(m.group(1).replace(",", ""))


def fetch_html() -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; profile-art/1.0)",
        "Accept": "text/html",
        "X-Requested-With": "XMLHttpRequest",
    }
    resp = requests.get(URL, headers=headers, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")

    # id -> tooltip metnindeki katkı sayısı
    counts: dict[str, int] = {}
    for tip in soup.find_all("tool-tip"):
        target = tip.get("for")
        if target:
            counts[target] = _count_from_tooltip(tip.get_text())

    days: list[dict] = []
    for td in soup.select("td.ContributionCalendar-day"):
        d = td.get("data-date")
        if not d:
            continue
        cell_id = td.get("id", "")
        # id: contribution-day-component-<row>-<col> (row=haftanın günü 0=Pazar, col=hafta)
        parts = cell_id.rsplit("-", 2)
        try:
            row, col = int(parts[-2]), int(parts[-1])
        except (ValueError, IndexError):
            row = (datetime.strptime(d, "%Y-%m-%d").isoweekday()) % 7
            col = len(days)  # yalnızca güvenlik ağı; normalde buraya düşmez
        days.append(
            {
                "date": d,
                "level": int(td.get("data-level", 0)),
                "count": counts.get(cell_id, 0),
                "row": row,
                "col": col,
            }
        )

    days.sort(key=lambda x: x["date"])
    return days


def compute_stats(days: list[dict]) -> dict:
    total = sum(d["count"] for d in days)
    max_count = max((d["count"] for d in days), default=0)
    best = max(days, key=lambda x: x["count"], default=None)

    # En uzun seri
    longest = run = 0
    for d in days:
        run = run + 1 if d["count"] > 0 else 0
        longest = max(longest, run)

    # Mevcut seri: bugünden geriye; bugün 0 ise (gün henüz sürüyor) atla
    current = 0
    seq = days[:]
    if seq and seq[-1]["count"] == 0:
        seq = seq[:-1]
    for d in reversed(seq):
        if d["count"] > 0:
            current += 1
        else:
            break

    # Aylık toplamlar (son 12 ay etiketi)
    monthly: dict[str, int] = {}
    for d in days:
        key = d["date"][:7]  # YYYY-MM
        monthly[key] = monthly.get(key, 0) + d["count"]

    return {
        "total": total,
        "max_count": max_count,
        "best_day": {"date": best["date"], "count": best["count"]} if best else None,
        "current_streak": current,
        "longest_streak": longest,
        "monthly": monthly,
    }


def main() -> int:
    html = fetch_html()
    days = parse(html)
    if not days:
        print("HATA: hiç katkı hücresi bulunamadı (HTML yapısı değişmiş olabilir).", file=sys.stderr)
        return 1

    stats = compute_stats(days)
    weeks = max((d["col"] for d in days), default=0) + 1

    payload = {
        "username": USERNAME,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "range": {"from": days[0]["date"], "to": days[-1]["date"]},
        "weeks": weeks,
        "total": stats["total"],
        "max_count": stats["max_count"],
        "stats": stats,
        "days": days,
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(
        f"OK: {len(days)} gün · {stats['total']:,} katkı · "
        f"seri {stats['current_streak']} (en uzun {stats['longest_streak']}) -> {OUT}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
