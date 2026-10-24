"""Annotated image: ACCEPT solid green-blue, ABSTAIN dashed amber, REJECT not drawn (count in the footer)."""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFont

COL = {"ACCEPT": (0, 158, 115), "ABSTAIN": (230, 159, 0)}


def _font(size):
    for p in ("/usr/share/fonts/TTF/DejaVuSans-Bold.ttf", "/usr/share/fonts/dejavu/DejaVuSans-Bold.ttf",
              "/usr/share/fonts/noto/NotoSans-Bold.ttf"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _dashed(dr, box, col, w):
    x1, y1, x2, y2 = box
    step = 12
    for x in range(int(x1), int(x2), step * 2):
        dr.line([(x, y1), (min(x + step, x2), y1)], fill=col, width=w)
        dr.line([(x, y2), (min(x + step, x2), y2)], fill=col, width=w)
    for y in range(int(y1), int(y2), step * 2):
        dr.line([(x1, y), (x1, min(y + step, y2))], fill=col, width=w)
        dr.line([(x2, y), (x2, min(y + step, y2))], fill=col, width=w)


def annotate(img: Image.Image, receipt: dict) -> Image.Image:
    im = img.copy()
    W, H = im.size
    dr = ImageDraw.Draw(im)
    w = max(2, int(min(W, H) / 300))
    f = _font(max(12, int(min(W, H) / 45)))
    hz = receipt["measure"]["horizon"]
    if hz.get("v_h") is not None:
        y = hz["v_h"]
        for x in range(0, W, 30):
            dr.line([(x, y), (x + 14, y)], fill=(120, 120, 255), width=1)
    for d in receipt["detections"]:
        st = d["status"]
        if st == "REJECT":
            continue
        col = COL[st]
        if st == "ACCEPT":
            dr.rectangle(d["box"], outline=col, width=w)
        else:
            _dashed(dr, d["box"], col, w)
        s = d["scores"]
        lab = f"{st[:3]} {d['class']} A{s['A'] if s['A'] is not None else '-'} B{s['B'] if s['B'] is not None else '-'}"
        if d.get("height_cm") is not None:
            lab += f" {d['height_cm']:.0f}+-{d['height_err_cm']:.0f}cm"
        elif d.get("height"):
            lab += " h:" + d["height"]["height_status"].lower()
        cv = (d.get("footpath_context") or {}).get("verdict")
        if cv in ("carriageway", "footpath", "mixed"):
            lab += {"carriageway": " [on road]", "footpath": " [on footpath]", "mixed": " [edge]"}[cv]
        x1, y1 = d["box"][0], d["box"][1]
        tb = dr.textbbox((x1, y1), lab, font=f)
        ty = y1 - (tb[3] - tb[1]) - 4 if y1 > (tb[3] - tb[1]) + 4 else y1 + 2
        dr.rectangle([x1, ty, x1 + (tb[2] - tb[0]) + 6, ty + (tb[3] - tb[1]) + 4], fill=col)
        dr.text((x1 + 3, ty), lab, fill=(0, 0, 0), font=f)
    c = receipt["counts"]
    foot = (f"{receipt['id']}  ACCEPT {c['ACCEPT']}  ABSTAIN {c['ABSTAIN']}  REJECT {c['REJECT']} (not drawn)  "
            f"{receipt['condition_bin']}  {receipt['tier']['tier']}  {receipt['timings']['total_s']:.1f}s")
    tb = dr.textbbox((0, 0), foot, font=f)
    dr.rectangle([0, H - (tb[3] - tb[1]) - 10, W, H], fill=(20, 20, 20))
    dr.text((6, H - (tb[3] - tb[1]) - 7), foot, fill=(240, 240, 240), font=f)
    return im
