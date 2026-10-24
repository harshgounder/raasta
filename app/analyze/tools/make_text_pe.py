"""One-time: compute YOLOE text embeddings for the prompt list and cache them, so the 600 MB
MobileCLIP text encoder never loads at request time. Run from app/analyze:
  .venv/bin/python tools/make_text_pe.py
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from raasta import config  # noqa: E402

os.chdir(config.WEIGHTS)  # ultralytics looks for mobileclip_blt.ts in the cwd
import torch  # noqa: E402
from ultralytics import YOLOE  # noqa: E402

t = time.time()
m = YOLOE(config.A_WEIGHTS)
pe = m.get_text_pe(config.PROMPT_LIST)
torch.save({"names": config.PROMPT_LIST, "pe": pe.cpu()}, config.A_TEXT_PE)
print("saved", config.A_TEXT_PE, tuple(pe.shape), f"{time.time() - t:.1f}s")
