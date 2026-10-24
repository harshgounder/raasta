# LUNAR-TIE moves applied to SC-02 (claude, read 2026-10-24 ~16:20 from ~/sih-2026/GRAND-ARCHITECTURE.md L40-179 + method/IDEATION-LUNAR-TIE.md)

## The three principles LUNAR-TIE converged on (GRAND-ARCHITECTURE L92-117), mapped

| LUNAR-TIE principle | quote | SC-02 use |
|---|---|---|
| P1 continuous parametric geometry beats fixed grids | "landmarks as continuous primitives, ties as real-valued coordinates with covariance" (L101-102) | every barrier is a 3D point WITH a covariance ellipse (GPS error 5-15 m, heading error, depth error). Map-matching becomes a probability over footpath segments, drawn on the map as an "uncertainty cloud". The street itself can be a Gaussian splat (3D) |
| P2 physics first, learned second | "SPICE + photometric division before matching" (L106-107) | compute the sun position from photo time + GPS, predict where shadows must fall, check the photo's heading and timestamp against it; physics-based re-weathering (night, rain, fog) to stress-test the detectors; kerb height from metric depth, compared with IRC/MoHUA limits |
| P3 calibrated uncertainty is the product | "conformal ACCEPT/ABSTAIN/REJECT + tier stamps" (L112-113) | every barrier and every footpath segment carries ACCEPT / ABSTAIN ("needs a human look") / REJECT, plus a tier stamp: observed today / observed earlier / inferred from a cue / unknown |

## The honesty rule for reconstruction (GRAND-ARCHITECTURE L57-64, L170-171)
"continuity does not recover missing information": a Gaussian or generative reconstruction of a blurry or missing area chooses one plausible answer, it does not measure it. So SC-02 uses the 4-layer product contract (L170-171):
1. raw evidence (the photo, untouched)
2. geometry + covariance (where the barrier is and how sure)
3. residual (what the model could not explain)
4. preview with a prior flag (reconstructed or generated views are always labelled "reconstructed", never shown as observed)

## The zoo router (L83-85): condition-indexed dispatch
"fingerprint -> bin ledger -> dispatch policy -> drift dashboard". For "any time, any weather, anywhere in India": fingerprint each photo (night / rain / fog / glare / blur / motion / indoor-outdoor / region), send it to the detector + preprocessing that scored best for that condition bin, and show a drift dashboard of which conditions fail. A new condition with no score gets a loud ABSTAIN, not a guess (solar IDEA 5 says the same).

## Other moves (IDEATION-LUNAR-TIE.md section 3)
- M5 two independent routes, agreement = confidence: open-vocab detector vs VLM; and two photos of the same spot from different times or angles.
- M6 make your own ground truth: generate night / monsoon / fog versions of labelled campus photos (same kerb, different sky) and measure detector drift on them.
- M10 abstain on stage, M11 self-check without labels (two photos of the same kerb must give the same height), M17 one picture (naive map route vs our route).
