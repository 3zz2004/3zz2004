#!/usr/bin/env python3
"""Self-hosted premium README artwork generated from the real GitHub avatar."""
from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen
import json
import math
from PIL import Image, ImageDraw, ImageFont, ImageOps

ART = Path(__file__).resolve().parents[1] / "assets"
ART.mkdir(parents=True, exist_ok=True)
BGC = (13, 21, 17)
PANEL = (17, 30, 23)
LINE = (48, 72, 55)
WHITE = (243, 249, 242)
GREEN = (165, 217, 171)
MUTED = (143, 170, 151)
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(n, bold=False):
    return ImageFont.truetype(BOLD if bold else REG, n)


def base(w, h):
    im = Image.new("RGB", (w, h), BGC)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((2, 2, w-3, h-3), radius=18, outline=LINE, width=2)
    return im


def hero(t):
    im = base(1200, 290)
    d = ImageDraw.Draw(im)
    for x in range(28, 1200, 67):
        d.line((x, 8, x, 282), fill=(19, 30, 24), width=1)
    d.rectangle((27, 28, 34, 51), fill=GREEN)
    d.text((47, 29), "EZZ / THE BUILD SYSTEM", font=font(17, True), fill=MUTED)
    d.text((1048, 29), "v 02 / ONLINE", font=font(14), fill=GREEN)
    d.text((37, 72), "EZZ", font=font(105, True), fill=WHITE)
    d.text((282, 72), "MOHAMED", font=font(95, True), fill=GREEN)
    d.text((43, 198), "THINK LIKE A FOUNDER. BUILD LIKE AN ENGINEER.", font=font(26, True), fill=WHITE)
    d.text((44, 250), "SOFTWARE DEVELOPMENT  /  SAAS & PRODUCT  /  BUSINESS STRATEGY", font=font(14), fill=MUTED)
    d.line((44, 239, 1153, 239), fill=LINE, width=3)
    mx = int(44 + 1110*t)
    d.line((mx-42, 239, mx, 239), fill=GREEN, width=4)
    d.ellipse((mx-5, 234, mx+5, 244), fill=GREEN)
    return im


def identity(photo):
    W, H = 1200, 408
    im = base(W, H)
    d = ImageDraw.Draw(im)
    ph = ImageOps.fit(photo, (330, 358), method=Image.Resampling.LANCZOS, centering=(.5, .35))
    ph = ImageOps.colorize(ImageOps.grayscale(ph), black=(14, 24, 20), white=(185, 210, 192)).convert("RGB")
    mask = Image.new("L", (330, 358))
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 329, 357), radius=12, fill=255)
    im.paste(ph, (28, 24), mask)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((27, 23, 359, 383), radius=13, outline=(72, 105, 82), width=2)
    d.line((382, 27, 382, 380), fill=(49, 72, 56), width=2)
    d.text((420, 38), "PERSON / 001", font=font(18, True), fill=GREEN)
    d.text((417, 83), "THE PERSON", font=font(49, True), fill=WHITE)
    d.text((417, 145), "BEHIND THE BUILD.", font=font(48, True), fill=GREEN)
    d.line((420, 226, 1127, 226), fill=(64, 94, 70), width=2)
    d.text((420, 245), "Software Developer  /  Founder  /  SaaS Builder", font=font(20), fill=(227, 239, 228))
    d.text((420, 291), "I think about the business behind the code.", font=font(21), fill=WHITE)
    d.text((420, 324), "From the problem to the product to the growth.", font=font(19), fill=MUTED)
    d.text((420, 371), "SOFTWARE  /  PRODUCT  /  BUSINESS", font=font(15), fill=GREEN)
    return im


def disciplines(t):
    im = base(1200, 302)
    d = ImageDraw.Draw(im)
    d.text((36, 20), "THREE DISCIPLINES. ONE BUILDER.", font=font(31, True), fill=WHITE)
    d.text((39, 63), "I connect the strategy with the product and the technology that makes it possible.", font=font(16), fill=MUTED)
    cards = [
        ("01", "ENGINEERING", "Software development", "Architecture  /  AI"),
        ("02", "PRODUCT", "SaaS exploration", "Validate  /  Build"),
        ("03", "BUSINESS", "Business strategy", "Position  /  Grow"),
    ]
    for i, (num, title, detail, detail2) in enumerate(cards):
        x, y = 31+i*393, 104
        active = (i == int(t*3)%3)
        d.rounded_rectangle((x, y, x+368, y+167), radius=13, fill=PANEL,
                            outline=GREEN if active else LINE, width=3 if active else 2)
        d.text((x+22, y+20), num, font=font(17, True), fill=GREEN)
        d.text((x+22, y+56), title, font=font(32, True), fill=WHITE)
        d.text((x+22, y+113), detail, font=font(16), fill=(205, 222, 207))
        d.text((x+22, y+145), detail2, font=font(15), fill=MUTED)
    return im


def footer(t):
    im = base(1200, 157)
    d = ImageDraw.Draw(im)
    d.text((38, 24), "THE BEST IS YET TO BE BUILT.", font=font(43, True), fill=WHITE)
    d.text((41, 105), "EZZ MOHAMED   /   @3zz2004", font=font(15), fill=MUTED)
    x, y = 833, 91
    d.rounded_rectangle((x, y, x+328, y+48), radius=9, fill=(30, 53, 36), outline=GREEN, width=2)
    d.text((x+21, y+13), "EXPLORE MY REPOS", font=font(17, True), fill=GREEN)
    shift = 8+int(9*abs(math.sin(t*math.pi)))
    d.line((x+279, y+24, x+279+shift, y+24), fill=GREEN, width=3)
    d.line((x+279+shift-8, y+17, x+279+shift, y+24), fill=GREEN, width=3)
    d.line((x+279+shift-8, y+31, x+279+shift, y+24), fill=GREEN, width=3)
    return im


def gif(name, frames):
    frames = [frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=72) for frame in frames]
    frames[0].save(ART/name, save_all=True, append_images=frames[1:], loop=0,
                   duration=125, optimize=True, disposal=2)
    print(name, (ART/name).stat().st_size)


def main():
    req = Request("https://api.github.com/users/3zz2004",
                  headers={"User-Agent":"EzzREADME/1.0", "Accept":"application/vnd.github+json"})
    with urlopen(req, timeout=25) as f:
        profile = json.load(f)
    url = profile["avatar_url"]
    url += ("&" if "?" in url else "?") + "s=800"
    req = Request(url, headers={"User-Agent":"EzzREADME/1.0"})
    with urlopen(req, timeout=25) as f:
        photo = Image.open(BytesIO(f.read())).convert("RGB")
    identity(photo).save(ART/"ezz-identity.png", optimize=True)
    gif("ezz-hero-premium.gif", [hero(i/23) for i in range(24)])
    gif("ezz-disciplines-premium.gif", [disciplines(i/23) for i in range(24)])
    gif("ezz-footer.gif", [footer(i/15) for i in range(16)])
    print("Identity image refreshed from authentic GitHub avatar.")


if __name__ == "__main__":
    main()
