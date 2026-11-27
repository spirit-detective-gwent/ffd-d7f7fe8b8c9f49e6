#!/bin/bash
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; T=/workspace/alleycat/tools; S=/workspace/alleycat/shots
TIP=$(git -C $W rev-parse --short HEAD)
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while pgrep -f "td.py 8801" >/dev/null; do sleep 5; done
cd $T
for sp in "aoi down g_br_aoi_back after_aoi_back" "ryo up g_br_ryo_front after_ryo_front" "aoi up g_br_aoi_front after_aoi_front"; do set -- $sp; wl
  timeout 250 $P td.py 8801 $W $1 $2 $3 > /tmp/td_$3.log 2>&1; rc=$?
  python3 mkvid.py $3 $S/$4 > /tmp/mk_$3.log 2>&1; note "regen $4.mp4/_strip.png (td rc=$rc, $(grep -o 'world:opn:td:v:[a-z]*' /tmp/td_$3.log | head -1), $(tail -1 /tmp/mk_$3.log))"
done
L=/workspace/alleycat/tests/logs_final; mkdir -p $L; cd $W
export FFD=$W FFD_INDEX=$W/index.html
t(){ n=$1; shift; wl; timeout 1500 "$@" > $L/$n.log 2>&1; note "test $n rc=$? $(grep -v '^\s*$' $L/$n.log | tail -1 | cut -c1-160)"; }
t s2 $P tools/s2/s2_test.py index.html
t ngp $P tools/ngp/ngp_test.py $W/index.html
t verify_wired bash -c "cd /workspace/v6560-review/portraits && $P verify_wired.py $W"
t amb_check $P /workspace/ambsafe/p2/amb_check.py $W 54730
t ch_smoke $P tools/yk/ch_smoke.py $W 54711
wl; cd /workspace/alleycat/perf; timeout 5400 $P perf_check.py c1a3b8c $TIP --throttle 4 --repo /workspace/ffd > perf_check.log 2>&1; rc=$?
note "perf_check c1a3b8c vs $TIP x4 rc=$rc $(grep -c '^- PASS' perf_check.log) PASS / $(grep -c '^- FAIL' perf_check.log) FAIL; $(grep '^OVERALL' perf_check.log); fails: $(grep '^- FAIL' perf_check.log | tr '\n' ' ' | cut -c1-700)"
note "FINAL3 DONE"
