"""Photo links for the Jaipur photo areas (hroute/photos.py, cli._photo_extras). Offline, synthetic files."""
import json
import os

from PIL import Image

from hroute import cli, photos


def _rec(tmp_path, w=2000, h=1500, annotated=True):
    repo = tmp_path / "repo"
    run = repo / "app" / "analyze" / "out" / "run1"
    (run / "receipts").mkdir(parents=True)
    (run / "receipts" / "mly_X_1.json").write_text("{}")
    if annotated:
        (run / "annotated").mkdir()
        Image.new("RGB", (w, h), (200, 30, 40)).save(run / "annotated" / "mly_X_1.jpg")
    rec = {"id": "img-abc-d00", "type": "pole_obstruction", "lat": 26.9, "lon": 75.8, "status": "ACCEPT",
           "photo": "site-data/jaipur/evidence/mly_X_1.jpg", "receipt_ref": "app/analyze/out/run1/receipts/mly_X_1.json",
           "receipt_id": "rx-abc", "author": "someone", "licence": "CC BY-SA 4.0",
           "source_url": "https://www.mapillary.com/app/?pKey=1", "box": [100, 300, 300, 900], "image_wh": [w, h],
           "observed_at": "2026-07-29T11:10:49+00:00"}
    return repo, rec


def test_link_copies_annotated_image_capped_and_keeps_placement(tmp_path):
    repo, rec = _rec(tmp_path)
    pub = tmp_path / "public"
    pl = {"record_id": rec["id"], "status": "ABSTAIN", "segment_id": None, "p": 0.2, "record": dict(rec)}
    before = {k: pl[k] for k in ("status", "segment_id", "p")}
    written = photos.link_placements([pl], "jaipur-photos", public_root=str(pub), repo=str(repo))
    # placement decision is untouched
    assert {k: pl[k] for k in ("status", "segment_id", "p")} == before
    out = pub / "evidence" / "jaipur-photos" / "mly_X_1.jpg"
    assert out.exists()
    with Image.open(out) as im:
        assert max(im.size) == 1280 and im.size == (1280, 960)
    assert written["mly_X_1"]["url"] == "/evidence/jaipur-photos/mly_X_1.jpg"
    assert written["mly_X_1"]["kind"] == "annotated"
    ev = pl["evidence_photo"]
    assert ev["url"] == "/evidence/jaipur-photos/mly_X_1.jpg" and ev["annotated"] is True
    assert ev["credit"] == "someone; CC BY-SA 4.0; https://www.mapillary.com/app/?pKey=1"
    assert ev["receipt_ref"].endswith("mly_X_1.json")
    # site receipt shape: photo {url, crop, credit, license}; old string path kept
    assert pl["record"]["photo"]["url"] == ev["url"]
    assert pl["record"]["photo_path"] == "site-data/jaipur/evidence/mly_X_1.jpg"
    # box [100,300,300,900] in 2000x1500, padded 15 % of box size each side, as fractions
    assert pl["record"]["photo"]["crop"] == [0.035, 0.14, 0.13, 0.52]


def test_small_image_is_not_upscaled_and_missing_image_gives_no_url(tmp_path):
    repo, rec = _rec(tmp_path, w=640, h=480)
    pub = tmp_path / "public"
    pl = {"status": "ACCEPT", "record": dict(rec)}
    photos.link_placements([pl], "s", public_root=str(pub), repo=str(repo))
    with Image.open(pub / "evidence" / "s" / "mly_X_1.jpg") as im:
        assert im.size == (640, 480)
    repo2, rec2 = _rec(tmp_path / "b", annotated=False)
    pl2 = {"status": "ABSTAIN", "record": dict(rec2)}
    w2 = photos.link_placements([pl2], "s", public_root=str(tmp_path / "pub2"), repo=str(repo2))
    assert w2["mly_X_1"] is None and pl2["evidence_photo"]["url"] is None
    assert pl2["record"]["photo"] == rec2["photo"]  # untouched when no image exists


def test_reason_counts_are_computed_from_placements():
    pls = [{"status": "ACCEPT"},
           {"status": "ABSTAIN", "reason": "no footpath segment within 30 m", "record": {}},
           {"status": "ABSTAIN", "reason": "detector abstained; placement kept as candidates only", "record": {}},
           {"status": "ABSTAIN", "reason": "best segment p=0.20 < 0.7", "record": {"heading": None}},
           {"status": "ABSTAIN", "reason": "best segment p=0.47 < 0.7", "record": {"heading": 194.3}},
           {"status": "REJECT", "reason": "ValueError: unknown barrier type 'x'"}]
    c = photos.reason_counts(pls)
    assert sum(c.values()) == len(pls)
    assert c["placed (p >= accept_p)"] == 1
    assert c["ABSTAIN: detector ACCEPT, p < accept_p, no camera heading"] == 1
    assert c["ABSTAIN: detector ACCEPT, p < accept_p, heading present"] == 1
    assert c["REJECT: ValueError"] == 1


def test_photo_areas_are_configured_and_walled_city_untouched():
    for key in ("jaipur-photos", "jaipur-photos-south"):
        a = cli.AREAS[key]
        assert a["records_from"] == "jaipur" and a["photo_evidence"] == "jaipur-photos"
        assert a["what_if"] is False and len(a["scenarios"]) >= 1
        s, w, n, e = a["bbox"]
        for sc in a["scenarios"]:
            for pt in (sc["start"], sc["end"]):
                assert s <= pt["lat"] <= n and w <= pt["lon"] <= e
    j = cli.AREAS["jaipur"]
    assert j["bbox"] == (26.913, 75.815, 26.928, 75.833)
    assert "photo_evidence" not in j and "records_from" not in j
    assert [sc["id"] for sc in j["scenarios"]] == ["hawa-johari", "palace-hawa", "palace-quarter"]
    # a non-photo area gets no extra keys in barriers.json
    assert cli._photo_extras(j, [], "x") == {}


def test_photo_extras_never_lowers_the_threshold(tmp_path, monkeypatch):
    seen = {}
    monkeypatch.setattr(photos, "link_placements", lambda pls, slug: seen.setdefault("slug", slug) and {})
    ex = cli._photo_extras(cli.AREAS["jaipur-photos"], [{"status": "ABSTAIN", "reason": "best segment p=0.2 < 0.7",
                                                        "record": {"heading": 10}}],
                           os.path.join(cli.SITE_DATA, "jaipur", "barriers.input.json"))
    assert seen["slug"] == "jaipur-photos"
    assert ex["accept_p"] == 0.7
    assert ex["records_file"] == os.path.join("site-data", "jaipur", "barriers.input.json")
    json.dumps(ex)
