"""Build a public GitHub profile snapshot for @3zz2004. No personal token needed locally;
GitHub Actions supplies a short-lived, repository-scoped GITHUB_TOKEN.
"""
from datetime import datetime, timezone
from pathlib import Path
import os
import json
import urllib.request
from PIL import Image, ImageDraw, ImageFont

USERNAME = "3zz2004"
OUT = Path(__file__).resolve().parents[1] / "assets" / "live-stats.png"
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def get_profile():
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "3zz2004-profile-readme",
    }
    token = os.getenv("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    req = urllib.request.Request("https://api.github.com/users/" + USERNAME, headers=headers)
    with urllib.request.urlopen(req, timeout=20) as response:
        data = json.load(response)
    if not isinstance(data.get("followers"), int) or not isinstance(data.get("public_repos"), int):
        raise ValueError("GitHub API did not provide expected public profile metrics")
    return data


def draw_card(draw, x, title, number, accent):
    y=107
    draw.rounded_rectangle((x,y,x+353,y+92),radius=14,fill=(18,36,24),outline=(55,88,57),width=2)
    draw.text((x+18,y+14),title,font=font(BOLD,15),fill=(145,173,150))
    draw.text((x+18,y+39),str(number),font=font(BOLD,35 if len(str(number))<12 else 23),fill=accent)


def render(profile):
    W,H=1200,238
    img=Image.new("RGB",(W,H),(10,17,14))
    draw=ImageDraw.Draw(img)
    draw.rounded_rectangle((18,18,W-18,H-18),radius=16,outline=(43,69,49),width=2)
    draw.text((52,35),"04 / GITHUB SNAPSHOT",font=font(BOLD,24),fill=(242,248,239))
    draw.text((53,73),"PUBLIC DATA   /   REFRESHED BY GITHUB ACTIONS",font=font(FONT,14),fill=(157,203,158))
    now=datetime.now(timezone.utc).strftime("%d %b %Y · %H:%M UTC").upper()
    draw_card(draw,53,"FOLLOWERS",f"{profile['followers']:,}",(165,215,160))
    draw_card(draw,423,"PUBLIC REPOS",f"{profile['public_repos']:,}",(242,248,239))
    draw_card(draw,793,"LAST SYNC",now,(165,215,160))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    img.save(OUT,optimize=True)

if __name__ == "__main__":
    render(get_profile())
    print("Updated", OUT)
