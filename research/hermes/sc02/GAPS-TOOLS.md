# GAPS-TOOLS: same spot over time, and reconstruction from bad or few photos

hermes, 2026-10-25 01:50 IST, research only. Two features the user asked for and we have not built. For each,
the top three candidates ranked by how fast they could land tonight, with licence, weights, GPU need for a
4 GB GTX 1650, and a one-hour integration plan. Licences and push dates were read from the GitHub API tonight
with `gh api repos/<owner>/<repo>`, so the SPDX strings below are GitHub's record, not a memory.

Two constraints that shape everything: 4 GB of VRAM, and no training tonight. Anything that needs a fine-tune
is out; anything that ships usable weights is in.

---

# A. SAME SPOT OVER TIME

Goal: given two photos of the same place taken years apart, say whether it is the same spot, and show what
changed. We already hold 16 Mapillary pairs in `data/online/mapillary-pairs`, which is enough to prove a
pipeline before promising a feature.

## A1. MegaLoc, place recognition, the fastest path to "same spot"

- Repo: https://github.com/gmberton/MegaLoc (MIT), last push 2026-08-06, which is inside the Aug to Oct 2026
  window the brief asked for.
- What it does: a single global descriptor per image, built on DINOv2 backbones, trained across multiple
  place-recognition datasets. It replaces the old retrieval stack with one cosine similarity, which is why it
  is an hour and not a day.
- Weights: published on Hugging Face and linked from the repo; downloadable, no gate.
- GPU: DINOv2 ViT-L in fp16 is about 1.2 GB, comfortably inside 4 GB at 518 px. On CPU it still runs on 16
  pairs, just slower.
- One-hour plan: clone, install, download the descriptor weights, extract descriptors for both halves of the
  16 pairs, print cosine similarity per pair and sort. Success = the true pairs rank above shuffled
  cross-pairs, which is a measurable claim we can print on the method page.
- What goes wrong: two photos of the same street from opposite directions can score lower than two different
  streets that share a shopfront. That is why A2 exists.

## A2. SuperPoint plus LightGlue, local verification, the honest second opinion

- Repo: https://github.com/cvg/LightGlue (Apache-2.0), last push 2026-02-18; SuperPoint weights ship with it.
- What it does: matches a few hundred keypoints between the two frames and returns an inlier count after RANSAC,
  which is a much stronger "same spot" signal than a global descriptor when the scene changed.
- Weights: bundled with the package, no separate download.
- GPU: works at 4 GB at 640 px; also fine on CPU for 16 pairs.
- One-hour plan: run LightGlue on the same 16 pairs, record inlier counts, then build a two-vote rule with A1:
  accept as same spot only when the global similarity is high and the inlier count clears a floor. Print both
  numbers in the receipt, because two engines agreeing is our standing rule.
- What goes wrong: repeated architecture, like a colonnade, produces confident wrong matches. The inlier rate
  alone will not catch it, so the pair needs a third check, which is A3.

## A3. ChangeFormer, pixel-level change, only for the demo card

- Repo: https://github.com/wgcban/ChangeFormer (MIT), last push 2024-01-31, so it is older than the window but
  it is the workhorse for a visible change mask.
- What it does: a transformer change detector trained on before/after pairs (LEVIR-CD and similar), producing
  a mask of what changed between the two images once they are aligned.
- Weights: the repo links pretrained checkpoints; they are trained on buildings and land, so a footpath change
  will be imperfect.
- GPU: small model, fits in 4 GB at 256 or 512 crops.
- One-hour plan: only after A1 and A2 pass, align the pair by homography from the LightGlue inliers, run
  ChangeFormer on the aligned crops, and use the mask as a highlight layer, never as a claim.
- What goes wrong: the training domain is aerial and building change, not street furniture, so it will fire on
  shadows and cars. It is a visual, not evidence, and the copy should say so.

Not chosen tonight: DINOv2 itself as a descriptor (Apache-2.0, pushed 2026-10-06) works but MegaLoc is the same
idea already tuned for retrieval, and AnyLoc (BSD-3-Clause, 2024-03-13) is a solid fallback if MegaLoc weights
fail to download, since it uses the same DINOv2 features with VLAD aggregation.

---

# B. BLURRY OR MISSING IMAGE, AND A ROUTE FROM A FEW PHOTOS

Two different problems that the user asked for in one breath: make a bad photo usable, and build a path from
whatever photos a person has, including indoors.

## B1. Real-ESRGAN, restore and upscale, the safest first move

- Repo: https://github.com/xinntao/Real-ESRGAN (BSD-3-Clause), last push 2024-08-06, 37k stars, the most
  battle-tested option in the list.
- What it does: blind super-resolution that also cleans compression and mild blur, on real-world degraded
  images rather than synthetic ones.
- Weights: released binaries and model files, x2 and x4, no gate.
- GPU: fits comfortably in 4 GB at 512 px tiles; the repo ships tiling for exactly this case.
- One-hour plan: run it on the five blurriest images in our C6 set, then re-run the detector on the restored
  versions and compare ACCEPT counts. That gives us a measured before/after rather than a claim, and the
  acceptance test is the detector, not the eye.
- What goes wrong: super-resolution invents texture, so a sharpened image can increase false detections. If the
  ACCEPT count rises without a matching rise in correct labels, the tool is hurting us and we say so.

## B2. Restormer, deblur specifically, the second engine

- Repo: https://github.com/swz30/Restormer (MIT), last push 2025-10-23.
- What it does: transformer restoration for motion blur, defocus and rain; the pretrained deblurring models are
  the part we would use.
- Weights: linked from the repo (Google Drive and similar), no gate.
- GPU: the base model runs at 4 GB on 256 px crops; full-resolution is out on this card.
- One-hour plan: use Restormer on the same five images, compare against B1, and keep whichever raises correct
  ACCEPTs on the labelled set. Two engines, one acceptance test, which is the same discipline as everywhere
  else in this project.
- What goes wrong: deblurring a night frame amplifies sensor noise into fake edges. If the image is night and
  blurry, the honest answer stays ABSTAIN and the copy offers the "take one more photo" prompt instead.

Not chosen: NAFNet (NOASSERTION, 2024-07-03) is a strong deblurrer but its licence is not a clean SPDX identity,
which matters if we ever publish the pipeline.

## B3. DUSt3R or MASt3R, geometry from a few photos, with a licence caveat

- Repos: https://github.com/naver/dust3r (last push 2025-09-24) and https://github.com/naver/mast3r (last push
  2025-06-30). Both are NOASSERTION on GitHub, and in practice they ship under a non-commercial research
  licence. That is a real constraint for a pitch that might imply a product.
- What they do: feed-forward dense stereo and pointmap regression from two or a few unposed images, no camera
  intrinsics needed, which is exactly the "user's own hallway photos" case.
- Weights: released checkpoints linked from the repos; the 512 model is the one to try.
- GPU: 512 model is about 4 to 6 GB. On a 4 GB card expect to run at reduced resolution, or on CPU very slowly.
  This is the one candidate that may simply not fit tonight.
- One-hour plan: run DUSt3R on three of our own photos of one corridor or hallway, at reduced resolution, and
  measure whether the reconstructed point cloud has a walkable floor plane. If it does, the indoor route idea
  becomes demonstrable; if it does not, we tell the user it needs a bigger card rather than pretending.
- What goes wrong: non-commercial licence, VRAM, and the fact that a point cloud is not yet a path: turning
  geometry into a traversable route with kerb and width semantics is product work, not a model call.

Not chosen: VGGT (https://github.com/facebookresearch/vggt, NOASSERTION, pushed 2026-05-19, 14.5k stars) is the
strongest feed-forward reconstruction in the window, and it is the wrong tool for tonight because it wants
substantially more VRAM than 4 GB.

---

# The ranking, in one table

| rank | feature | tool | licence | weights | fits 4 GB | tonight's realistic outcome |
|---|---|---|---|---|---|---|
| A1 | same spot | MegaLoc | MIT | yes, HF | yes | a similarity number per pair on our 16 pairs |
| A2 | same spot, verified | LightGlue + SuperPoint | Apache-2.0 | bundled | yes | inlier counts, a two-vote rule |
| A3 | change mask | ChangeFormer | MIT | yes, repo links | yes | a visual highlight, not evidence |
| B1 | restore | Real-ESRGAN | BSD-3-Clause | yes | yes | ACCEPT-count before and after on 5 images |
| B2 | deblur | Restormer | MIT | yes | yes, at 256 crops | a second opinion on the same 5 images |
| B3 | geometry from few photos | DUSt3R or MASt3R | non-commercial | yes | marginal | one corridor cloud, or an honest no |

## The sentence for the deck, if a judge asks about these

"Same-spot matching is a retrieval problem and we can demo it on 16 real pairs tonight; reconstruction from a
few photos is a research model that does not fit our card, and we would rather say that than show a point
cloud that looks like a path and is not one."
