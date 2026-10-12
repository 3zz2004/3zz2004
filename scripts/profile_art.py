#!/usr/bin/env python3
"""EZZ / SYSTEM — self-hosted animated profile artwork.

No external README-image service. GitHub Actions regenerates SVGs using
GitHub public profile data and the public contribution calendar.
"""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone
from io import BytesIO
from pathlib import Path
from xml.sax.saxutils import escape
import json
import re
import urllib.request

from bs4 import BeautifulSoup
from PIL import Image, ImageEnhance, ImageOps

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "assets"
USER = "3zz2004"
BG = "#0c1510"
PANEL = "#112018"
FRAME = "#34513d"
WHITE = "#edf5eb"
GREEN = "#a1d6ab"
MUTED = "#789a84"
PALETTE = ["#1b2920", "#355440", "#537f5a", "#78ab7f", "#a5d4a9"]


def get(url: str) -> bytes:
    headers = {
        "User-Agent": "EzzProfileArtwork/1.0",
        "Accept": "application/vnd.github+json" if "api.github.com" in url else "text/html,image/*;q=0.9",
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=35) as result:
        return result.read()


def save(filename: str, svg: str) -> None:
    ART.mkdir(parents=True, exist_ok=True)
    (ART / filename).write_text(svg, encoding="utf-8")
    print("Rendered", filename, len(svg), "bytes")


def portrait(avatar_url: str) -> None:
    """ASCII rendition of the user's ACTUAL public GitHub avatar."""
    raw = get(avatar_url)
    img = Image.open(BytesIO(raw)).convert("RGB")
    img = ImageOps.fit(img, (76, 56), method=Image.Resampling.LANCZOS)
    img = ImageOps.grayscale(img)
    img = ImageOps.autocontrast(img, cutoff=2)
    img = ImageEnhance.Contrast(img).enhance(1.45)
    img = ImageEnhance.Brightness(img).enhance(1.13)

    # Retain an intentionally circular avatar silhouette rather than
    # treating the avatar's dark outer edges as facial features.
    ramp = " .:-=+*#%@"
    rows = []
    for y in range(56):
        chars = []
        for x in range(76):
            lum = img.getpixel((x, y)) / 255
            # Soften the outermost four character columns.
            radius = ((x - 37.5) / 39) ** 2 + ((y - 27.5) / 30) ** 2
            if radius > 1:
                chars.append(" ")
            else:
                level = max(0, min(len(ramp)-1, int((1-lum) * (len(ramp)-1))))
                chars.append(ramp[level])
        rows.append("".join(chars).rstrip())

    W, H = 450, 565
    top = 61
    dy = 8.45
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" stroke="{FRAME}" fill="none"/>',
        f'<rect x="1" y="1" width="{W-2}" height="40" rx="13" fill="#18251c"/>',
        f'<path d="M0 40H{W}" stroke="{FRAME}"/>',
        '<circle cx="19" cy="21" r="5" fill="#61886b"/>',
        '<circle cx="37" cy="21" r="5" fill="#477456"/>',
        '<circle cx="55" cy="21" r="5" fill="#31523a"/>',
        '<text x="225" y="26" font-family="monospace" font-size="12" text-anchor="middle" fill="#a8c3ad">ezz@github:~$ whoami --ascii</text>',
        '<defs>',
    ]
    for i in range(len(rows)):
        y = top + i * dy
        out.append(
            f'<clipPath id="row{i}"><rect x="19" y="{y:.2f}" width="0" height="9.5">'
            f'<animate attributeName="width" from="0" to="413" begin="{.14+i*.056:.3f}s" dur=".12s" fill="freeze"/>'
            '</rect></clipPath>'
        )
    out.append('</defs>')
    for i, row in enumerate(rows):
        out.append(
            f'<text xml:space="preserve" x="20" y="{top+i*dy+8:.2f}" '
            f'clip-path="url(#row{i})" textLength="410" lengthAdjust="spacing" '
            f'font-family="DejaVu Sans Mono,Consolas,monospace" font-size="9" fill="{GREEN}">'
            f'{escape(row)}</text>'
        )
    out += [
        '<path d="M18 538H432" stroke="#2c4b36"/>',
        '<text x="20" y="554" font-family="monospace" font-size="11" fill="#829e86">001 / IDENTITY LOADED</text>',
        '<rect x="198" y="545" width="7" height="11" fill="#a4daae">'
        '<animate attributeName="opacity" values="1;0;1" dur="1s" repeatCount="indefinite"/></rect>',
        '</svg>',
    ]
    save("ezz-portrait.svg", "".join(out))


def days_from_calendar() -> list[dict]:
    content = get(f"https://github.com/users/{USER}/contributions")
    soup = BeautifulSoup(content, "html.parser")
    cells = soup.select("td.ContributionCalendar-day[data-date]")
    if not cells:
        cells = soup.select("td[data-date][data-level], rect[data-date][data-level]")
    if len(cells) < 100:
        raise RuntimeError("GitHub public contribution calendar format changed; refusing to invent activity")
    tooltips = {
        tag.get("for"): tag.get_text(" ", strip=True)
        for tag in soup.find_all("tool-tip") if tag.get("for")
    }
    days = []
    for cell in cells:
        stamp = cell.get("data-date", "")
        try:
            date.fromisoformat(stamp)
        except ValueError:
            continue
        level = min(4, max(0, int(cell.get("data-level") or 0)))
        tip = tooltips.get(cell.get("id"), "")
        raw = cell.get("data-count")
        if raw is not None and str(raw).isdigit():
            count = int(raw)
        elif re.search(r"no contributions", tip, re.IGNORECASE):
            count = 0
        else:
            match = re.match(r"([\d,]+)\s+contributions?", tip, re.I)
            count = int(match.group(1).replace(",", "")) if match else None
        days.append({"date": stamp, "level": level, "count": count})
    if len(days) < 100:
        raise RuntimeError("Contribution dates unavailable")
    days.sort(key=lambda d: d["date"])
    return days


def heatmap(days: list[dict] | None, error: str = "") -> None:
    W, H = 1000, 274
    out = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">',
        '<style>@keyframes appear{from{opacity:0;transform:translateY(-6px)}to{opacity:1;transform:translateY(0)}}'
        '.cell{animation:appear .3s cubic-bezier(.2,.8,.2,1) both}'
        '@media(prefers-reduced-motion:reduce){.cell{animation:none!important}}</style>',
        f'<rect width="{W}" height="{H}" rx="14" fill="{BG}"/>',
        f'<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="none" stroke="{FRAME}"/>',
        '<rect x="1" y="1" width="998" height="41" rx="13" fill="#17251b"/>',
        '<path d="M0 41H1000" stroke="#34513d"/>',
        '<circle cx="21" cy="21" r="5" fill="#688d72"/>',
        '<circle cx="40" cy="21" r="5" fill="#4a7055"/>',
        '<circle cx="59" cy="21" r="5" fill="#315239"/>',
        '<text x="500" y="27" text-anchor="middle" font-family="monospace" font-size="14" fill="#b3c9ba">ezz@github:~$ ./activity --last-12-months</text>',
    ]
    if not days:
        out += [
            '<text x="500" y="137" text-anchor="middle" font-family="monospace" font-size="19" fill="#dbefdd">ACTIVITY SOURCE TEMPORARILY UNAVAILABLE</text>',
            '<text x="500" y="174" text-anchor="middle" font-family="monospace" font-size="13" fill="#819f88">No made-up contributions are displayed.</text>',
            '</svg>',
        ]
        save("ezz-heatmap.svg", "".join(out))
        print("Activity warning:", error)
        return

    # Calendar aligned Sunday to Saturday, last 53 columns.
    last_day = date.fromisoformat(days[-1]["date"])
    first_day = last_day - timedelta(days=370)
    first_sunday = first_day - timedelta(days=(first_day.weekday()+1)%7)
    lookups = {d["date"]: d for d in days}
    first_months = set()
    total = 0
    numeric_complete = True
    active = 0
    for c in range(53):
        for r in range(7):
            stamp = first_sunday + timedelta(days=7*c+r)
            if stamp > last_day:
                continue
            cell = lookups.get(stamp.isoformat())
            x, y = 76 + c*16.6, 94 + r*16.6
            if cell is None:
                color, level = "#151e18", -1
                numeric_complete = False
            else:
                level = cell["level"]
                color = PALETTE[level]
                if level:
                    active += 1
                if cell["count"] is None:
                    numeric_complete = False
                else:
                    total += cell["count"]
            if stamp.day <= 7 and (stamp.year,stamp.month) not in first_months:
                first_months.add((stamp.year,stamp.month))
                out.append(f'<text x="{x:.1f}" y="76" font-family="monospace" font-size="12" fill="#91a89a">{stamp.strftime("%b")}</text>')
            delay = .15 + c*.018 + r*.045
            out.append(
                f'<rect class="cell" x="{x:.1f}" y="{y:.1f}" width="12.6" height="12.6" '
                f'rx="2.5" fill="{color}" style="animation-delay:{delay:.3f}s"/>'
            )
    for r, label in [(1,"MON"),(3,"WED"),(5,"FRI")]:
        out.append(f'<text x="18" y="{104+r*16.6:.1f}" fill="#789a84" font-family="monospace" font-size="11">{label}</text>')
    out.append('<path d="M20 221H980" stroke="#2d4836"/>')
    summary = f"{total:,} CONTRIBUTIONS" if numeric_complete else f"{active} ACTIVE DAYS"
    out += [
        f'<text x="27" y="248" font-family="monospace" font-size="18" font-weight="700" fill="{WHITE}">{summary}</text>',
        f'<text x="525" y="246" font-family="monospace" font-size="12" fill="{MUTED}">LESS</text>',
    ]
    for i, col in enumerate(PALETTE):
        out.append(f'<rect x="{577+i*19}" y="234" width="14" height="14" rx="3" fill="{col}"/>')
    out += [
        f'<text x="682" y="246" font-family="monospace" font-size="12" fill="{MUTED}">MORE</text>',
        f'<text x="975" y="248" text-anchor="end" font-family="monospace" font-size="12" fill="{MUTED}">'
        f'PUBLIC CALENDAR · {escape(last_day.isoformat())}</text>',
        '</svg>',
    ]
    save("ezz-heatmap.svg", "".join(out))


def stats(profile: dict) -> None:
    now = datetime.now(timezone.utc)
    metric = [
        ("GITHUB FOLLOWERS", f"{int(profile['followers']):,}"),
        ("PUBLIC REPOSITORIES", f"{int(profile['public_repos']):,}"),
        ("LAST REFRESH (UTC)", now.strftime("%d %b %Y").upper()),
    ]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="156" viewBox="0 0 1000 156">',
        f'<rect width="1000" height="156" rx="14" fill="{BG}"/>',
        f'<rect x="1" y="1" width="998" height="154" rx="13" fill="none" stroke="{FRAME}"/>',
        f'<text x="28" y="29" font-family="monospace" fill="{MUTED}" font-size="13">PUBLIC DATA  /  VIA GITHUB API</text>',
    ]
    for i, (label, value) in enumerate(metric):
        x = 28 + i*330
        if i:
            out.append(f'<path d="M{x-13} 47V137" stroke="#2e4936"/>')
        out.append(f'<text x="{x}" y="69" font-family="monospace" font-size="13" fill="{MUTED}">{escape(label)}</text>')
        size = 30 if i == 2 else 43
        out.append(f'<text x="{x}" y="117" font-family="Arial, sans-serif" font-weight="800" font-size="{size}" fill="{GREEN}">{escape(value)}</text>')
        if i == 2:
            out.append(f'<text x="{x}" y="137" font-family="monospace" fill="{MUTED}" font-size="11">{now.strftime("%H:%M UTC")}</text>')
    out.append('</svg>')
    save("ezz-stats.svg", "".join(out))


def main() -> None:
    profile = json.loads(get(f"https://api.github.com/users/{USER}"))
    if not isinstance(profile.get("followers"), int) or not isinstance(profile.get("public_repos"), int):
        raise RuntimeError("GitHub public profile metrics unavailable")
    portrait(profile["avatar_url"])
    stats(profile)
    try:
        days = days_from_calendar()
        heatmap(days)
    except Exception as exc:
        heatmap(None, str(exc))


if __name__ == "__main__":
    main()
