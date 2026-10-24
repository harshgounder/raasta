"""audio helpers: ffmpeg for decode/measure/encode, numpy for loops, fades, mixing."""
import json, os, re, subprocess, tempfile
import numpy as np

SR = 48000
TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tmp")
os.makedirs(TMP, exist_ok=True)


def decode(path, start=0.0, dur=None, af=None, ch=2):
    cmd = ["ffmpeg", "-v", "error", "-ss", str(start)]
    if dur:
        cmd += ["-t", str(dur)]
    cmd += ["-i", path]
    if af:
        cmd += ["-af", af]
    cmd += ["-ac", str(ch), "-ar", str(SR), "-f", "f32le", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, ch).copy()


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path], capture_output=True, text=True).stdout
    return float(out.strip() or 0)


def write_wav(arr, path):
    arr = np.ascontiguousarray(arr, dtype=np.float32)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", str(arr.shape[1]), "-i", "-", "-c:a", "pcm_f32le", path], input=arr.tobytes(), check=True)


def measure(arr, pad_to=1.2):
    """integrated LUFS + true peak dBTP (ffmpeg loudnorm analyser). short clips padded with silence (BS.1770 400 ms gating)."""
    n = int(pad_to * SR)
    if len(arr) < n:
        arr = np.vstack([arr, np.zeros((n - len(arr), arr.shape[1]), np.float32)])
    p = os.path.join(TMP, "m.wav")
    write_wav(arr, p)
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", p, "-af", "loudnorm=print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
    j = json.loads(err[err.rindex("{"):err.rindex("}") + 1])
    return float(j["input_i"]), float(j["input_tp"])


def limit(arr, ceiling_db):
    p, q = os.path.join(TMP, "l_in.wav"), os.path.join(TMP, "l_out.wav")
    write_wav(arr, p)
    lim = 10 ** (ceiling_db / 20)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-af", f"alimiter=limit={lim:.5f}:attack=2:release=60:level=disabled:latency=1", "-c:a", "pcm_f32le", q], check=True)
    return decode(q, ch=arr.shape[1])[: len(arr)]


def normalise(arr, target, ceiling=-1.5):
    """gain to target LUFS, keep true peak under ceiling (limiter if needed), 3 passes."""
    for _ in range(3):
        i, tp = measure(arr)
        arr = arr * np.float32(10 ** ((target - i) / 20))
        i2, tp2 = measure(arr)
        if tp2 > ceiling:
            arr = limit(arr, ceiling - 0.6)
        else:
            break
    i, tp = measure(arr)
    if tp > ceiling:  # safety: limiter could not catch it (very short clip), trade loudness for headroom
        arr = arr * np.float32(10 ** ((ceiling - 0.3 - tp) / 20))
        i, tp = measure(arr)
    return arr, i, tp


def fade(arr, fin=0.01, fout=0.05):
    a = arr.copy()
    ni, no = int(fin * SR), int(fout * SR)
    if ni:
        a[:ni] *= (np.sin(np.linspace(0, np.pi / 2, ni)) ** 2)[:, None]
    if no:
        a[-no:] *= (np.cos(np.linspace(0, np.pi / 2, no)) ** 2)[:, None]
    return a


def make_loop(seg, L, X):
    """seg must be >= L+X seconds. output length L, last sample flows into first (equal-power crossfade of tail into head)."""
    nL, nX = int(round(L * SR)), int(round(X * SR))
    seg = seg[: nL + nX]
    head = seg[:nX]
    tail = seg[nL:nL + nX]
    t = np.linspace(0, np.pi / 2, nX)[:, None]
    xf = tail * np.cos(t) + head * np.sin(t)
    return np.vstack([xf, seg[nX:nL]]).astype(np.float32)


def seam_db(arr):
    d = np.abs(np.diff(arr, axis=0)).max(axis=1)
    p99 = np.percentile(d, 99) + 1e-12
    j = np.abs(arr[0] - arr[-1]).max()
    return 20 * np.log10(j / p99 + 1e-12)


def encode(arr, out_dir, stem, loop=False):
    p = os.path.join(TMP, stem + ".wav")
    write_wav(arr, p)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-c:a", "libvorbis", "-q:a", "5", os.path.join(out_dir, stem + ".ogg")], check=True)
    if loop:  # AAC decoders may drop the last frame: pad with the loop's own head (wrap) so the buffer always covers loopEnd
        p = os.path.join(TMP, stem + "_wrap.wav")
        write_wav(np.vstack([arr, arr[:2048]]), p)
    else:  # ffmpeg's AAC path loses the first 1024 samples on decode: lead with 1024 samples of silence so the attack survives
        p = os.path.join(TMP, stem + "_lead.wav")
        write_wav(np.vstack([np.zeros((1024, arr.shape[1]), np.float32), arr]), p)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", os.path.join(out_dir, stem + ".m4a")], check=True)
    return p


def rms_env(arr, win=0.05):
    m = arr.mean(axis=1) if arr.ndim == 2 else arr
    n = int(win * SR)
    k = len(m) // n
    e = np.sqrt((m[: k * n].reshape(k, n) ** 2).mean(axis=1) + 1e-12)
    return 20 * np.log10(e)
