"""Render a real GitHub profile stats image for @3zz2004."""
from datetime import datetime, timezone
from pathlib import Path
import json
import os
import urllib.request

from PIL import Image, ImageDraw, ImageFont

USER = "3zz2004"
OUTPUT = Path(__file__).resolve().parents[1] / "live-stats.png"
REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(size, bold=False):
    return ImageFont.truetype(BOLD if bold else REGULAR, size)


def github_profile():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "3zz2004-readme-stats",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(f"https://api.github.com/users/{USER}", headers=headers)
    with urllib.request.urlopen(request, timeout=25) as response:
        data = json.load(response)
    for field in ("followers", "public_repos"):
        if not isinstance(data.get(field), int):
            raise ValueError(f"Missing GitHub public profile metric: {field}")
    return data


def card(draw, x, label, value, secondary=""):
    y = 102
    draw.rounded_rectangle((x, y, x + 350, y + 100), radius=12,
                           fill=(17, 34, 24), outline=(53, 83, 61), width=2)
    draw.text((x + 18, y + 13), label, font=font(16, True), fill=(151, 190, 158))
    draw.text((x + 18, y + 42), str(value), font=font(31, True), fill=(222, 244, 219))
    if secondary:
        draw.text((x + 205, y + 69), secondary, font=font(13), fill=(152, 191, 160))


def render(data):
    img = Image.new("RGB", (1200, 234), (10, 17, 14))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((14, 14, 1186, 220), radius=16,
                        outline=(49, 79, 55), width=2)
    d.text((48, 30), "LIVE / GITHUB SNAPSHOT", font=font(25, True), fill=(239, 250, 236))
    d.text((48, 68), "PUBLIC DATA  /  UPDATED AUTOMATICALLY", font=font(14),
           fill=(149, 184, 155))
    now = datetime.now(timezone.utc)
    card(d, 48, "FOLLOWERS", f"{data['followers']:,}")
    card(d, 425, "PUBLIC REPOS", f"{data['public_repos']:,}")
    card(d, 802, "LAST SYNC", now.strftime("%d %b %Y").upper(),
         now.strftime("%H:%M UTC"))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUTPUT, optimize=True)


if __name__ == "__main__":
    render(github_profile())
    print(f"Refreshed {OUTPUT}")
