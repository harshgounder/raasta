# C6 review queue: 20 images a human must confirm first

The labels in `c6-v1.jsonl` are team labels made with AI assistance (Claude looked at each image). They need one human pass. These 20 come first because each one moves a score or settles a rule. About 15 minutes total.

How to review: open `data/online/<file>`. Check the line for that file in `c6-v1.jsonl`. Then change `status` (and boxes if needed) and bump `label_version` to `c6-v1-human` on lines you touched. Rerun `python3 -I eval/eval_c6.py`.

| # | file | current label | the question for the human |
|---|---|---|---|
| 1 | commons/cm_130_Ghaffar_Manzil_Colony_Jamia_Nagar_Okhla_New_Delhi_Delhi_1100.jpg | kerb ramp = present (zebra end), footpath = broken | Night. Is there really no ramp where the zebra meets the kerb? This is 1 of only 4 kerb-ramp positives |
| 2 | mapillary/mly_Chandigarh_280931197086749.jpg | kerb ramp = present, footpath = broken | Raised junction corner with no ramp, crumbling edge. Confirm |
| 3 | mapillary-pairs/mlypair_Jaipur_724686079525921.jpg | kerb ramp = present | The call is on a median island at the zebra end, not a footpath. Should it count? |
| 4 | youtube/yt_fZLx7heZHtc_maxres1.jpg | kerb ramp = present | Footpath starts with a raised painted kerb and no ramp. Is that a crossing point? |
| 5 | mapillary-pairs/mlypair_Panaji_1763999497392607.jpg | steps = present, pole = present (scaffolding) | Are temple entrance steps "in the walking path"? Does temporary scaffolding count as a pole? |
| 6 | mapillary/mly_Jaipur_2530467737465123.jpg | steps = present (small, far) | The step flight at the far end is small. Confirm it is steps on the path |
| 7 | mapillary/mly_MUJ-Dehmi-Kalan_1231369965628851.jpg | steps = present (two short red flights) | Very small in frame. Confirm |
| 8 | mapillary/mly_Chandigarh_511414063225158.jpg | parked = present, pole = present, footpath = broken | Dusk, motion blur. Are the bikes on the raised footpath? |
| 9 | youtube-cc/yt_AHJpk-HDmL0_maxres1.jpg | parked = unsure (rule) | RULE: a street with no footpath, scooters parked on its edge. Is that "parked vehicle blocking footpath"? The answer applies to 5 more lines (cm_019, mly_Shimla_481137163091641, mlypair_Mumbai_856307225274630, yt_SzDvWkilL_g_maxres1, and this one) plus about 10 fork lines already unsure for the same reason |
| 10 | mapillary-pairs/mlypair_Mumbai_856307225274630.jpg | parked = unsure (rule), footpath = missing | Same rule as #9, second example |
| 11 | commons/cm_065_Footpath_Bowbazar_Street_Kolkata_2013_03_03_5221_JPG.jpg | parked = present (rickshaw far ahead) | The rickshaw or cart is small. Parked on the footpath or moving? |
| 12 | mapillary/mly_Kolkata_906852491733079.jpg | pole = unsure (downgraded at merge) | Pedestrian lane: are the signboards on posts standing in the lane (present) or fixed to the wall (absent)? |
| 13 | youtube/yt_JpAxfAtxTz8_maxres3.jpg | pole = present (banner stands in arcade) | Do movable banner stands count as pole obstruction? |
| 14 | commons/cm_200_Gultekdi_Road_2_jpg.jpg | pole = present (advert board), footpath = missing | Is the advert board standing on the footpath? |
| 15 | commons/cm_058_Water_puddles_in_road_by_raindrops_jpg.jpg | footpath = broken (standing water) | Does a puddle covering the path count as broken? (Definition question) |
| 16 | commons/cm_067_Modern_Sidewalk_Art_14657855027_jpg.jpg | footpath = broken (repair in progress) | Does a footpath under re-paving count as broken? (Definition question) |
| 17 | commons/cm_184_Kali_Bari_Temple_Shimla_1_jpg.jpg | footpath = unsure | Shimla road with no footpath in a pedestrian-heavy core. Is it missing? |
| 18 | commons/cm_217_Korattur_shop_jpg.jpg | all 5 unsure | Night and wet. A human may be able to read more than "unsure" |
| 19 | commons/cm_156_Pune_Laxmi_Road_Shopping_Main_jpg.jpg | kerb, footpath, parked = unsure | Blurred night market. Are the rows of bikes on the footpath? |
| 20 | mapillary-pairs/mlypair_Mumbai_1714602086341628.jpg | kerb, footpath, pole, parked = unsure | Footpath hidden by scooters and vendors. Can a human tell? |

How this list was made: I ranked the 100 lines by difficulty, unsure count and rare-class positives with a small script, then hand-picked items that change a score (rare positives), settle a rule (#9, #13, #15, #16) or could recover an image that is currently excluded (#18 to #20). Other hard items not in the 20: mly_Kolkata_1660571772298215 (night, through a windscreen), yt_QQ2oXrC1dQA_maxres2 (night), cm_034 (close crop of a vendor), cm_222 (dense crowd), mly_Puri_792529403863840 (three borderline calls).
