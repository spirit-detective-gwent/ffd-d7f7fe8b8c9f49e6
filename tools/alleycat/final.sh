#!/bin/bash
# final chain at 0c7299f: regen pre-0c7299f clips, tests, perf live4 (live1 failed on goto timeout). Appends results to NOTES.md.
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; T=/workspace/alleycat/tools; S=/workspace/alleycat/shots
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
note(){ echo "- $(date '+%H:%M UTC') $*" >> $N; echo "$*"; }
cd $T
for sp in "ryo left f3_br_ryo_side after_ryo_side" "aoi left f3_br_aoi_side after_aoi_side" "ryo down f3_br_ryo_back after_ryo_back" "aoi down f3_br_aoi_back after_aoi_back"; do set -- $sp; wl
  timeout 250 $P td.py 8801 $W $1 $2 $3 > /tmp/td_$3.log 2>&1; rc=$?
  python3 mkvid.py $3 $S/$4 > /tmp/mk_$3.log 2>&1; note "regen $4 (td rc=$rc, $(grep -o 'world:opn:td:v:[a-z]*\|world:amb2:dir:[a-z]*' /tmp/td_$3.log | head -1), mkvid $(tail -1 /tmp/mk_$3.log))"
done
L=/workspace/alleycat/tests/logs_final; mkdir -p $L; cd $W
t(){ n=$1; shift; wl; timeout 1500 "$@" > $L/$n.log 2>&1; note "test $n rc=$? $(grep -v '^\s*$' $L/$n.log | tail -1 | cut -c1-160)"; }
t verify_wired bash -c "cd /workspace/v6560-review/portraits && $P verify_wired.py $W"
t s2 $P tools/s2/s2_test.py index.html
t ngp $P tools/ngp/ngp_test.py $W/index.html
t ch_smoke $P tools/yk/ch_smoke.py $W 54711
wl; cd /workspace/alleycat/perf; DPR=3 timeout 900 $P $T/perf_ac.py /workspace/release/wt/index.html live4 live4.json > live4.log 2>&1; note "perf live4 rc=$? $(grep '^RES' live4.log | cut -c1-400)"
note "FINAL CHAIN DONE"
