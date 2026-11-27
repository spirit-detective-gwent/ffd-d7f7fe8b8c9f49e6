#!/bin/bash
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; T=/workspace/alleycat/tools; S=/workspace/alleycat/shots
TIP=$(git -C $W rev-parse --short HEAD)
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while pgrep -f "final522.sh" >/dev/null; do sleep 15; done
note "final522 finished; starting final523"
cd $T
for sp in "aoi left h_aoi_side after_aoi_side" "aoi up h_aoi_front after_aoi_front" "aoi down h_aoi_back after_aoi_back"; do set -- $sp; wl
  timeout 250 $P td.py 8801 $W $1 $2 $3 > /tmp/td_$3.log 2>&1; rc=$?
  python3 mkvid.py $3 $S/$4 > /tmp/mk_$3.log 2>&1; note "t523 regen $4.mp4/_strip.png (td rc=$rc, $(grep -o 'world:opn:td:\(v:[a-z]*\|sweep\|kneel\|spin\)' /tmp/td_$3.log | sort -u | tr '\n' ' '), $(tail -1 /tmp/mk_$3.log))"
done
r(){ tag=$1; ch=$2; who=$3; trig=$4; shift 4; wl; env "$@" timeout 300 $P bo.py $tag $ch $who $trig > /tmp/bo_${tag}_${ch}_${who}.log 2>&1; rc=$?
  note "battle-open $tag ch$ch $who ($trig $*) rc=$rc: $(grep -o 'SWIRL_SEEN.*' /tmp/bo_${tag}_${ch}_${who}.log); $(grep '^AT' /tmp/bo_${tag}_${ch}_${who}.log | sed -E 's/^AT ([0-9]+) .*"pose":([a-z]+).*"standOp":"?([0-9.]*)"?.*/\1ms pose=\2 stand=\3/' | tr '\n' ' ')"; }
r br 1 ryo tap
r br 1 aoi tap
r br 2 aoi api ROOM=c2_club FFD_INDEX=$W/index.html
L=/workspace/alleycat/tests/logs_523; mkdir -p $L; cd $W; export FFD=$W FFD_INDEX=$W/index.html
t(){ n=$1; shift; wl; timeout 1500 "$@" > $L/$n.log 2>&1; note "test $n rc=$? $(grep -v '^\s*$' $L/$n.log | tail -1 | cut -c1-160)"; }
t s2 $P tools/s2/s2_test.py index.html
t ngp $P tools/ngp/ngp_test.py $W/index.html
t verify_wired bash -c "cd /workspace/v6560-review/portraits && $P verify_wired.py $W"
t amb_check $P /workspace/ambsafe/p2/amb_check.py $W 54730
t ch_smoke $P tools/yk/ch_smoke.py $W 54711
note "FINAL523 DONE"
