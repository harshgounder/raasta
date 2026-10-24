"""Parallel ranged download of a Hugging Face repo snapshot into a local folder (the HF client
stalled on this network on 2026-10-24; single connections run ~230 KB/s).
  python3 tools/pfetch.py REPO_ID OUT_DIR [--parts 12] [--skip-pattern .bin,.h5,.msgpack,.onnx]
"""
import argparse
import concurrent.futures as cf
import json
import os
import subprocess
import urllib.request

ap = argparse.ArgumentParser()
ap.add_argument("repo")
ap.add_argument("out")
ap.add_argument("--parts", type=int, default=12)
ap.add_argument("--skip", default=".bin,.h5,.msgpack,.onnx,.ot,.tflite,.pb")
a = ap.parse_args()
os.makedirs(a.out, exist_ok=True)
info = json.load(urllib.request.urlopen(f"https://huggingface.co/api/models/{a.repo}/tree/main", timeout=30))
skip = tuple(a.skip.split(","))
files = [(f["path"], f.get("size", 0)) for f in info if f["type"] == "file" and not f["path"].endswith(skip)]
base = f"https://huggingface.co/{a.repo}/resolve/main/"


def get_range(url, path, lo, hi):
    for _ in range(6):
        r = subprocess.run(["curl", "-sL", "--retry", "3", "-r", f"{lo}-{hi}", "-o", path, url])
        if r.returncode == 0 and os.path.exists(path) and os.path.getsize(path) == hi - lo + 1:
            return True
    return False


for path, size in files:
    dst = os.path.join(a.out, path)
    os.makedirs(os.path.dirname(dst) or a.out, exist_ok=True)
    if os.path.exists(dst) and os.path.getsize(dst) == size:
        continue
    url = base + path
    if size < 8_000_000:
        subprocess.run(["curl", "-sL", "--retry", "3", "-o", dst, url], check=True)
        print("got", path, size, flush=True)
        continue
    n = a.parts
    step = size // n + 1
    parts = [(i, i * step, min(size - 1, (i + 1) * step - 1)) for i in range(n) if i * step < size]
    with cf.ThreadPoolExecutor(len(parts)) as ex:
        futs = [ex.submit(get_range, url, f"{dst}.part{i}", lo, hi) for i, lo, hi in parts]
        ok = all(f.result() for f in futs)
    if not ok:
        raise SystemExit(f"failed {path}")
    with open(dst, "wb") as out:
        for i, _, _ in parts:
            with open(f"{dst}.part{i}", "rb") as fh:
                out.write(fh.read())
            os.remove(f"{dst}.part{i}")
    print("got", path, size, os.path.getsize(dst), flush=True)
print("DONE", a.repo)
