#!/usr/bin/env python3
"""Animated, self-hosted README artwork from Ezz's supplied, unmodified photo."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps
import math

ART=Path(__file__).resolve().parents[1]/"assets"
ART.mkdir(parents=True,exist_ok=True)
PHOTO=ART/"ezz-source.webp"
BG=(12,19,16); WHITE=(239,246,237); GREEN=(167,219,174)
MUTED=(138,169,147); BORDER=(46,74,55)
FONT="/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
BOLD="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def f(n,b=False):
    return ImageFont.truetype(BOLD if b else FONT,n)

def base(w,h):
    a=Image.new("RGB",(w,h),BG)
    ImageDraw.Draw(a).rounded_rectangle((2,2,w-3,h-3),radius=18,outline=BORDER,width=2)
    return a

def hero(photo,t):
    im=base(1200,480)
    crop=ImageOps.fit(photo,(540,480),method=Image.Resampling.LANCZOS,centering=(.5,.43))
    # Only resize and blend the edge; no facial regeneration or alteration.
    alpha=Image.new("L",(540,480))
    ap=alpha.load()
    for y in range(480):
        for x in range(540):
            ap[x,y]=min(255,int(255*max(0,min(1,(x-6)/180))),max(90,int(255*max(0,min(1,(480-y)/105)))))
    im.paste(crop,(660,0),alpha)
    d=ImageDraw.Draw(im)
    d.line((55,70,1138,70),fill=(56,80,61),width=2)
    d.text((58,32),"EZZ / PORTFOLIO SYSTEM",font=f(17,True),fill=GREEN)
    d.text((959,34),"BUILD MODE / ACTIVE",font=f(14),fill=MUTED)
    d.line((57,107,57,367),fill=(81,126,92),width=3)
    d.text((77,101),"EZZ",font=f(118,True),fill=WHITE)
    d.text((72,222),"MOHAMED",font=f(78,True),fill=GREEN)
    d.text((75,345),"SOFTWARE DEVELOPER  /  FOUNDER",font=f(21,True),fill=WHITE)
    d.text((77,385),"PRODUCT. STRATEGY. ENGINEERING.",font=f(17),fill=MUTED)
    d.line((76,425,561,425),fill=(55,88,64),width=3)
    x1=76+int(485*t)
    d.line((max(76,x1-135),425,x1,425),fill=GREEN,width=4)
    d.ellipse((x1-4,421,x1+4,429),fill=GREEN)
    d.text((77,447),"I BUILD WHAT MAKES SENSE.",font=f(16,True),fill=WHITE)
    return im

def statement():
    im=base(1200,196);d=ImageDraw.Draw(im)
    d.rectangle((42,35,48,159),fill=GREEN)
    d.text((76,20),"THE THINKING BEHIND THE CODE",font=f(17,True),fill=MUTED)
    d.text((76,58),"I DON'T JUST BUILD SOFTWARE.",font=f(35,True),fill=WHITE)
    d.text((76,107),"I THINK ABOUT THE BUSINESS BEHIND IT.",font=f(29,True),fill=GREEN)
    d.text((76,163),"From the problem to the product to the growth.",font=f(16),fill=MUTED)
    return im

def disciplines(t):
    im=base(1200,305);d=ImageDraw.Draw(im)
    d.text((42,25),"ONE MINDSET. THREE DISCIPLINES.",font=f(33,True),fill=WHITE)
    d.text((43,73),"Connecting the strategy, the product and the technology.",font=f(17),fill=MUTED)
    items=[("01","ENGINEERING","Software & systems","Architecture / AI"),
           ("02","PRODUCT","SaaS & product thinking","Build / Iterate"),
           ("03","BUSINESS","Strategy & growth","Position / Scale")]
    for i,(num,title,line1,line2) in enumerate(items):
        x=35+i*394;y=119;active=int(t*3)%3==i
        d.rounded_rectangle((x,y,x+374,y+160),radius=12,fill=(18,33,24),
                            outline=GREEN if active else BORDER,width=3 if active else 2)
        d.text((x+17,y+13),num,font=f(18,True),fill=GREEN)
        d.text((x+18,y+44),title,font=f(28,True),fill=WHITE)
        d.text((x+18,y+103),line1,font=f(16),fill=(213,228,213))
        d.text((x+18,y+133),line2,font=f(15),fill=MUTED)
    return im

def process(t):
    im=base(1200,198);d=ImageDraw.Draw(im)
    d.text((43,18),"THE PRODUCT LOOP",font=f(27,True),fill=WHITE)
    d.text((44,57),"Not everything that can be built should be built.",font=f(17),fill=MUTED)
    stages=["DISCOVER","VALIDATE","DESIGN","BUILD","ITERATE"]
    active=int(t*5)%5
    for i,s in enumerate(stages):
        x=49+i*230;y=114
        d.ellipse((x,y,x+19,y+19),fill=GREEN if i==active else (61,94,70))
        d.text((x+31,y-2),s,font=f(17,True),fill=GREEN if i==active else WHITE)
        if i<4:d.line((x+159,y+10,x+211,y+10),fill=(91,129,98),width=2)
    d.line((49,159,1150,159),fill=BORDER,width=2)
    d.line((49,159,49+int(1101*t),159),fill=GREEN,width=4)
    return im

def footer(t):
    im=base(1200,190);d=ImageDraw.Draw(im)
    d.text((43,26),"THE BEST IS YET",font=f(45,True),fill=WHITE)
    d.text((43,84),"TO BE BUILT.",font=f(44,True),fill=GREEN)
    d.text((47,161),"EZZ MOHAMED   /   @3zz2004",font=f(17),fill=MUTED)
    x,y=804,67
    d.rounded_rectangle((x,y,x+347,y+65),radius=10,fill=(25,46,32),outline=GREEN,width=2)
    d.text((x+23,y+20),"VIEW MY WORK",font=f(23,True),fill=WHITE)
    ax=x+292+int(9*math.sin(t*math.pi)**2)
    d.line((ax-10,y+34,ax+13,y+34),fill=GREEN,width=4)
    d.line((ax+3,y+25,ax+13,y+34,ax+3,y+43),fill=GREEN,width=4)
    return im

def gif(name,frames,colors=170):
    indexed=[a.quantize(colors=colors,method=Image.Quantize.MEDIANCUT,
                        dither=Image.Dither.NONE) for a in frames]
    indexed[0].save(ART/name,save_all=True,append_images=indexed[1:],duration=160,
                    loop=0,disposal=2,optimize=True)
    print(name,(ART/name).stat().st_size)

def main():
    if not PHOTO.exists():
        raise RuntimeError("Missing user-supplied source photo; refusing avatar substitution")
    photo=Image.open(PHOTO).convert("RGB")
    # Render the photo-first cover as true RGB PNG to avoid GIF skin-tone banding.
    hero(photo, 0.57).save(ART/"ezz-identity.png", optimize=True)
    # Keep the photograph in full RGB: GIF's 256-color palette damages skin texture.
    # Animate the supporting sections, but preserve a crisp photo-first hero.
    hero(photo,0.57).save(ART/"ezz-hero-photo-v2.png", optimize=True)
    gif("ezz-disciplines-premium.gif",[disciplines(i/20) for i in range(21)],105)
    gif("ezz-process.gif",[process(i/24) for i in range(25)],110)
    gif("ezz-footer.gif",[footer(i/19) for i in range(20)],100)
    print("Rendered with Ezz's real uploaded photo")

if __name__=="__main__":main()
