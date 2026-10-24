#!/usr/bin/env bash
# re-record the 3 site recordings (archive the old ones first). run from app/analyze with the server up on :8010
set -e
O=../site/public/content/scan-examples
A=archive/scan-examples-$(date +%Y%m%d-%H%M)
mkdir -p "$A"; cp $O/*.json "$A"/ 2>/dev/null || true
.venv/bin/python tools/record_scan.py ../../data/online/commons/cm_033_Cart_on_footpath_in_India_jpg.jpg $O/street-cart-on-footpath.json --label "Cart on footpath in India (Wikimedia Commons)" --source-url "https://commons.wikimedia.org/wiki/File:Cart_on_footpath_in_India.jpg" --licence "CC BY 4.0, Vendor on Robolow Universe" | tail -1
.venv/bin/python tools/record_scan.py test-in/scan/hallway_lagos_hospital_cc0.jpg $O/hallway-hospital.json --label "Hospital hallway in Lagos (Wikimedia Commons)" --source-url "https://commons.wikimedia.org/wiki/File:Hospital_hallway_in_Lagos.jpg" --licence "CC0" | tail -1
.venv/bin/python tools/record_scan.py test-in/scan/night_bailey_road_patna_cc0.jpg $O/night-road-patna.json --label "Bailey Road, Patna at night (Wikimedia Commons)" --source-url "https://commons.wikimedia.org/wiki/File:Bailey_Road,_Patna_at_night.jpg" --licence "CC0" | tail -1
