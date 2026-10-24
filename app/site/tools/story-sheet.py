# contact sheet of shots/v2/<tag>/y-*.jpg, labelled with scroll y. usage: python3 -I tools/story-sheet.py shots/v2/desk [cols] [from] [to]
import sys, glob, os
from PIL import Image, ImageDraw
d = sys.argv[1]; cols = int(sys.argv[2]) if len(sys.argv) > 2 else 5
lo = int(sys.argv[3]) if len(sys.argv) > 3 else 0; hi = int(sys.argv[4]) if len(sys.argv) > 4 else 10**9
fs = [f for f in sorted(glob.glob(os.path.join(d, 'y-*.jpg'))) if lo <= int(os.path.basename(f)[2:8]) <= hi]
im0 = Image.open(fs[0]); tw = 360; th = int(im0.height * tw / im0.width)
rows = (len(fs) + cols - 1) // cols
sheet = Image.new('RGB', (cols * tw, rows * (th + 18)), (255, 255, 255))
dr = ImageDraw.Draw(sheet)
for i, f in enumerate(fs):
    im = Image.open(f).convert('RGB').resize((tw, th))
    x, y = (i % cols) * tw, (i // cols) * (th + 18)
    sheet.paste(im, (x, y + 18)); dr.text((x + 4, y + 3), os.path.basename(f)[2:8], fill=(200, 0, 0))
name = os.path.join(d, f'sheet-{lo}-{min(hi, 999999)}.jpg')
sheet.save(name, quality=80); print(name, len(fs))
