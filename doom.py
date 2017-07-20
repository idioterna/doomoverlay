from PIL import Image
import math

sn = [Image.open('doom/STYSNUM%s.png' % x).convert("RGBA") for x in range(10)] # small yellow numbers
bn = [Image.open('doom/STTNUM%s.png' % x).convert("RGBA") for x in range(10)] # big numbers
bm = Image.open('doom/STTMINUS.png').convert("RGBA") # big minus
bp = Image.open('doom/STTPRCNT.png').convert("RGBA") # big percent
bd = Image.open('doom/STTDOT.png').convert("RGBA") # big decimal dot
ba = Image.open('doom/STBAR.png').convert("RGBA") # bar
bh = Image.open('doom/STFKILL1.png').convert("RGBA") # going hard
be = Image.open('doom/STFST11.png').convert("RGBA") # going easy

def sround(x, digits=2):
    return round(x, digits-1-int(math.floor(math.log10(abs(x)))))


def big(char):
    if char in '0123456789':
        return bn[int(char)]
    elif char == '-':
        return bm
    elif char == '.':
        return bd
    elif char == '%':
        return bp

def bignum(number, places=0):
    if places > 0:
        fmt = '%%.%df' % places
        s = fmt % number
    else:
        s = '%d' % number
    cpos = 0
    for ch in s:
        cpos += big(ch).size[0] + 6
    i = Image.new('RGBA', (cpos, 96), (255, 255, 255, 0))
    cpos = 0
    for ch in s:
        l = big(ch)
        i.paste(l, (cpos, 0))
        cpos += l.size[0] + 6
    return i


def center(dst, src, x, y):
    dst.paste(src, (x-src.size[0]//2, y), src)

def decimal(dst, src, x, y, num):
    if ('%.1f' % num).endswith('1'):
        dst.paste(src, (x-src.size[0]-18, y), src)
    else:
        dst.paste(src, (x-src.size[0], y), src)

def generate(data):
    bar = ba.copy()

    # speed
    spd = data.get('speed', 0)
    speed = bignum(spd, 1)
    decimal(bar, speed, 620, 24, spd)

    # heart rate
    hr = data.get('heartrate', 0)
    hrd = bignum(hr)
    center(bar, hrd, 136, 24)
    if hr >= 150:
        center(bar, bh, 1005, 12)
    else:
        center(bar, be, 1005, 12)

    # distance
    ds = data.get('distance', 0) / 1000.0
    dst = bignum(ds, 1)
    center(bar, dst, 1284, 24)

    # cadence
    cd = data.get('cadence', 0)
    cad = bignum(cd, 0)
    center(bar, cad, 765, 24)

    # elev. gain
    eg = data.get('altgain', 0)
    elg = bignum(eg, 0)
    center(bar, elg, 1728, 24)

    return bar

