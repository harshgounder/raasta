"""Step 1 intake: EXIF time / GPS / heading, and a condition fingerprint ("condition bin")."""
from __future__ import annotations

import datetime as dt
import hashlib

import cv2
import numpy as np
from PIL import Image, ImageOps

IST = dt.timezone(dt.timedelta(hours=5, minutes=30))


def _ratio(v) -> float:
    try:
        return float(v)
    except TypeError:
        n, d = v
        return float(n) / float(d) if d else 0.0


def _dms(vals) -> float:
    d, m, s = (_ratio(x) for x in vals)
    return d + m / 60.0 + s / 3600.0


def read_exif(img: Image.Image) -> dict:
    out: dict = {"has_exif": False}
    try:
        ex = img.getexif()
    except Exception:  # noqa: BLE001
        return out
    if not ex:
        return out
    out["has_exif"] = True
    try:
        sub = ex.get_ifd(0x8769)
    except Exception:  # noqa: BLE001
        sub = {}
    t = sub.get(36867) or ex.get(306)
    if t:
        try:
            ts = dt.datetime.strptime(str(t).strip("\x00 "), "%Y:%m:%d %H:%M:%S")
            off = sub.get(36881)
            if off and len(str(off)) >= 6:
                sign = -1 if str(off)[0] == "-" else 1
                hh, mm = str(off)[1:].split(":")[:2]
                tz = dt.timezone(sign * dt.timedelta(hours=int(hh), minutes=int(mm)))
                out["time_tz_source"] = "exif OffsetTimeOriginal"
            else:
                tz = IST
                out["time_tz_source"] = "assumed IST (EXIF has no offset)"
            out["captured_at"] = ts.replace(tzinfo=tz).isoformat()
        except ValueError:
            pass
    f35 = sub.get(41989)
    if f35:
        out["focal_35mm"] = _ratio(f35)
    out["make_model"] = " ".join(str(ex.get(k, "")).strip("\x00 ") for k in (271, 272)).strip() or None
    try:
        gps = ex.get_ifd(0x8825)
    except Exception:  # noqa: BLE001
        gps = {}
    if gps and 2 in gps and 4 in gps:
        try:
            lat = _dms(gps[2]) * (-1 if str(gps.get(1, "N")).upper().startswith("S") else 1)
            lon = _dms(gps[4]) * (-1 if str(gps.get(3, "E")).upper().startswith("W") else 1)
            if abs(lat) > 0.01 or abs(lon) > 0.01:
                out["lat"], out["lon"] = round(lat, 7), round(lon, 7)
        except Exception:  # noqa: BLE001
            pass
        if 17 in gps:
            out["heading"] = round(_ratio(gps[17]), 1)
            out["heading_ref"] = "true" if str(gps.get(16, "T")).upper().startswith("T") else "magnetic"
        if 31 in gps:
            out["gps_error_m"] = round(_ratio(gps[31]), 1)
    return out


def load_image(data: bytes) -> tuple[Image.Image, dict, str]:
    import io
    sha = hashlib.sha256(data).hexdigest()
    img = Image.open(io.BytesIO(data))
    exif = read_exif(img)
    img = ImageOps.exif_transpose(img).convert("RGB")
    return img, exif, sha


def condition(img: Image.Image, captured_at: dt.datetime | None, sun_elev: float | None) -> dict:
    a = np.asarray(img)
    small = cv2.resize(a, (min(640, a.shape[1]), int(a.shape[0] * min(640, a.shape[1]) / a.shape[1])))
    gray = cv2.cvtColor(small, cv2.COLOR_RGB2GRAY)
    mean = float(gray.mean())
    lap = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    contrast = float(gray.std())
    # dark channel prior (He et al. 2009): haze/fog lifts the per-patch min over RGB
    dark = cv2.erode(small.min(axis=2), np.ones((15, 15), np.uint8))
    dark_mean = float(dark.mean())
    hsv = cv2.cvtColor(small, cv2.COLOR_RGB2HSV)
    sat = float(hsv[..., 1].mean())
    sky = float(gray[: max(1, int(0.12 * gray.shape[0]))].mean())
    hot = float((gray > 245).mean())

    if sun_elev is not None:
        light = "day" if sun_elev > 6 else ("dusk" if sun_elev > -6 else "night")
        light_src = f"sun elevation {sun_elev:.1f} deg from time+GPS"
        if light == "day" and mean < 45:
            light, light_src = "night_or_indoor", light_src + "; image very dark, flagged"
    else:
        light = "day" if mean > 85 else ("dusk" if mean > 50 else "night")
        light_src = f"brightness (mean gray {mean:.0f}/255) + sky check (top 12 % mean {sky:.0f}), no time+GPS"
        if light != "night" and sky < 60 and hot > 0.002:
            light = "night_lit"
            light_src += "; dark sky with bright point lights: lit night scene"
        if captured_at is not None:
            h = captured_at.hour
            if 7 <= h <= 17 and light == "night":
                light_src += f"; EXIF hour {h} says day, image dark: flagged"
            if (h >= 20 or h <= 4) and light == "day":
                light = "night_lit"
                light_src += f"; EXIF hour {h} says night, image bright (street light or flash)"
    blur = "blurry" if lap < 60 else ("soft" if lap < 150 else "sharp")
    haze = "hazy" if (dark_mean > 95 and contrast < 50) else "clear"
    bin_ = f"{light}/{blur}/{haze}"
    return {
        "bin": bin_, "light": light, "light_source": light_src, "blur": blur, "haze": haze,
        "rain": "not checked",
        "metrics": {"mean_gray": round(mean, 1), "laplacian_var": round(lap, 1),
                    "contrast_std": round(contrast, 1), "dark_channel_mean": round(dark_mean, 1),
                    "mean_saturation": round(sat, 1),
                    "sky_top12_mean": round(sky, 1), "hot_pixel_frac": round(hot, 4)},
        "rules": "light: sun elev >6 day, -6..6 dusk, else night (or gray mean >85 day, >50 dusk); "
                 "blur: Laplacian var <60 blurry, <150 soft; haze: dark-channel mean >95 and contrast <50",
    }
