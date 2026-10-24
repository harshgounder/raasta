"""Lazy model holders. Each model loads on first use, fp16 on the GPU when CUDA is up, CPU otherwise.
Free RAM on this box is ~2 GB, so models load one at a time and `unload_all()` frees them.
Set ANALYZE_LOW_MEM=1 to unload each model right after use (slower, lowest peak memory)."""
from __future__ import annotations

import gc
import os
import threading
import time

import numpy as np
import torch

from . import config

LOCK = threading.RLock()
LOW_MEM = os.environ.get("ANALYZE_LOW_MEM", "0") == "1"
_models: dict = {}
LOAD_SECONDS: dict = {}


def device() -> str:
    if os.environ.get("ANALYZE_CPU") == "1":
        return "cpu"
    return "cuda" if torch.cuda.is_available() else "cpu"


def _dtype():
    return torch.float16 if device() == "cuda" else torch.float32


def unload(name: str):
    with LOCK:
        if _models.pop(name, None) is not None:
            gc.collect()
            if torch.cuda.is_available():
                torch.cuda.empty_cache()


def unload_all():
    for k in list(_models):
        unload(k)


def versions() -> dict:
    import transformers
    import ultralytics
    return {
        "detector_A": "YOLOE-11s-seg (ultralytics %s), text prompts via cached MobileCLIP-BLT embeddings" % ultralytics.__version__,
        "detector_B": f"{config.B_MODEL} (transformers {transformers.__version__})",
        "depth": f"{config.DEPTH_MODEL} (metric, outdoor vkitti fine-tune, max 80 m)",
        "footpath_context": f"{config.SEG_MODEL} (SegFormer-B0, segments.ai sidewalk set, Belgium)",
        "torch": torch.__version__, "device": device(),
        "gpu": torch.cuda.get_device_name(0) if device() == "cuda" else None,
    }


# ---------------- detector A: YOLOE ----------------
def yoloe():
    with LOCK:
        if "A" not in _models:
            t = time.time()
            from ultralytics import YOLOE
            m = YOLOE(config.A_WEIGHTS)
            d = torch.load(config.A_TEXT_PE, map_location="cpu")
            if list(d["names"]) != config.PROMPT_LIST:
                raise RuntimeError("cached YOLOE text embeddings do not match PROMPT_LIST; rerun tools/make_text_pe.py")
            m.set_classes(d["names"], d["pe"])
            _models["A"] = m
            LOAD_SECONDS["A"] = round(time.time() - t, 2)
        return _models["A"]


def run_a(img) -> list[dict]:
    with LOCK:
        m = yoloe()
        dev = 0 if device() == "cuda" else "cpu"
        res = m.predict(img, conf=config.A_CONF, iou=0.5, imgsz=640, device=dev, half=(dev == 0),
                        verbose=False, max_det=config.MAX_DETS_PER_MODEL)
        out = []
        for r in res:
            for b in r.boxes:
                i = int(b.cls)
                out.append({"prompt": config.PROMPT_LIST[i], "family": config.PROMPTS[config.PROMPT_LIST[i]],
                            "box": [round(float(v), 1) for v in b.xyxy[0].tolist()], "score": round(float(b.conf), 3)})
        if LOW_MEM:
            unload("A")
        return out


# ---------------- detector B: OWLv2 ----------------
def owl():
    with LOCK:
        if "B" not in _models:
            t = time.time()
            from transformers import Owlv2ForObjectDetection, Owlv2Processor
            src = config.resolve(config.B_MODEL)
            proc = Owlv2Processor.from_pretrained(src)
            model = Owlv2ForObjectDetection.from_pretrained(src, dtype=_dtype()).to(device()).eval()
            q = proc(text=[config.PROMPT_LIST], return_tensors="pt")
            _models["B"] = (proc, model, q)
            LOAD_SECONDS["B"] = round(time.time() - t, 2)
        return _models["B"]


@torch.inference_mode()
def run_b(img) -> list[dict]:
    with LOCK:
        proc, model, _ = owl()
        w, h = img.size
        S = max(w, h)
        inputs = proc(text=[config.PROMPT_LIST], images=img, return_tensors="pt")
        inputs = {k: (v.to(device(), _dtype()) if v.dtype.is_floating_point else v.to(device())) for k, v in inputs.items()}
        out = model(**inputs)
        logits = out.logits[0].float().sigmoid()          # (N boxes, Q queries)
        boxes = out.pred_boxes[0].float()                  # cx, cy, w, h normalised to the padded square
        score, q = logits.max(dim=1)
        keep = score >= config.B_CONF
        score, q, boxes = score[keep], q[keep], boxes[keep]
        cx, cy, bw, bh = boxes.unbind(-1)
        xyxy = torch.stack([(cx - bw / 2) * S, (cy - bh / 2) * S, (cx + bw / 2) * S, (cy + bh / 2) * S], -1)
        xyxy[:, 0::2] = xyxy[:, 0::2].clamp(0, w)
        xyxy[:, 1::2] = xyxy[:, 1::2].clamp(0, h)
        dets = []
        if len(score):
            from torchvision.ops import batched_nms
            fam_ids = torch.tensor([sorted(set(config.PROMPTS.values())).index(config.PROMPTS[config.PROMPT_LIST[int(i)]])
                                    for i in q], device=score.device)
            idx = batched_nms(xyxy, score, fam_ids, 0.5)[: config.MAX_DETS_PER_MODEL]
            for j in idx.tolist():
                p = config.PROMPT_LIST[int(q[j])]
                bx = xyxy[j].tolist()
                if (bx[2] - bx[0]) < 4 or (bx[3] - bx[1]) < 4:
                    continue
                dets.append({"prompt": p, "family": config.PROMPTS[p], "box": [round(v, 1) for v in bx],
                             "score": round(float(score[j]), 3)})
        if LOW_MEM:
            unload("B")
        return dets


# ---------------- metric depth ----------------
def depth_model():
    with LOCK:
        if "D" not in _models:
            t = time.time()
            from transformers import AutoImageProcessor, AutoModelForDepthEstimation
            src = config.resolve(config.DEPTH_MODEL)
            proc = AutoImageProcessor.from_pretrained(src)
            model = AutoModelForDepthEstimation.from_pretrained(src, dtype=_dtype()).to(device()).eval()
            _models["D"] = (proc, model)
            LOAD_SECONDS["D"] = round(time.time() - t, 2)
        return _models["D"]


@torch.inference_mode()
def run_depth(img) -> np.ndarray:
    """HxW metric depth in metres (model's own focal assumption, see receipt notes)."""
    with LOCK:
        proc, model = depth_model()
        inputs = proc(images=img, return_tensors="pt")
        inputs = {k: v.to(device(), _dtype()) for k, v in inputs.items()}
        pred = model(**inputs).predicted_depth.float()
        pred = torch.nn.functional.interpolate(pred.unsqueeze(1), size=(img.size[1], img.size[0]),
                                               mode="bicubic", align_corners=False)[0, 0]
        d = pred.clamp(min=0.05).cpu().numpy()
        if LOW_MEM:
            unload("D")
        return d


# ---------------- footpath context: SegFormer-B0 sidewalk segmentation ----------------
def seg_model():
    with LOCK:
        if "S" not in _models:
            t = time.time()
            from transformers import AutoImageProcessor, SegformerForSemanticSegmentation
            src = config.resolve(config.SEG_MODEL)
            proc = AutoImageProcessor.from_pretrained(src)
            model = SegformerForSemanticSegmentation.from_pretrained(src, dtype=_dtype()).to(device()).eval()
            _models["S"] = (proc, model)
            LOAD_SECONDS["S"] = round(time.time() - t, 2)
        return _models["S"]


@torch.inference_mode()
def run_seg(img) -> np.ndarray:
    """Label map at 1/4 image size (labels = config.SEG_LABELS)."""
    with LOCK:
        proc, model = seg_model()
        inputs = proc(images=img, return_tensors="pt")
        inputs = {k: v.to(device(), _dtype()) for k, v in inputs.items()}
        logits = model(**inputs).logits.float()
        h, w = max(1, img.size[1] // 4), max(1, img.size[0] // 4)
        lab = torch.nn.functional.interpolate(logits, size=(h, w), mode="bilinear", align_corners=False).argmax(1)[0]
        out = lab.to(torch.uint8).cpu().numpy()
        if LOW_MEM:
            unload("S")
        return out
