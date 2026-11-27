#!/bin/bash
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; T=/workspace/alleycat/tools; S=/workspace/alleycat/shots
TIP=$(git -C $W rev-parse --short HEAD)
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while pgrep -f "bo.py" >/dev/null; do sleep 5; done
cd $T
for sp in "ryo left h_ryo_side after_ryo_side" "aoi left h_aoi_side after_aoi_side" "ryo up h_ryo_front after_ryo_front" "aoi up h_aoi_front after_aoi_front" "ryo down h_ryo_back after_ryo_back" "aoi down h_aoi_back after_aoi_back"; do set -- $sp; wl
  timeout 250 $P td.py 8801 $W $1 $2 $3 > /tmp/td_$3.log 2>&1; rc=$?
  python3 mkvid.py $3 $S/$4 > /tmp/mk_$3.log 2>&1; note "t518 regen $4.mp4/_strip.png (td rc=$rc, $(grep -o 'world:opn:td:v:[a-z]*' /tmp/td_$3.log | head -1), $(tail -1 /tmp/mk_$3.log))"
done
note "REGEN518 DONE"
