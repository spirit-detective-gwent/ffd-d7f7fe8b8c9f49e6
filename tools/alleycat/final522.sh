#!/bin/bash
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; T=/workspace/alleycat/tools
TIP=$(git -C $W rev-parse --short HEAD)
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while pgrep -f "regen522.sh|td.py 8801" >/dev/null; do sleep 10; done
cd $T
r(){ tag=$1; ch=$2; who=$3; trig=$4; shift 4; wl; env "$@" timeout 300 $P bo.py $tag $ch $who $trig > /tmp/bo_${tag}_${ch}_${who}.log 2>&1
  note "battle-open $tag ch$ch $who ($trig $*): $(grep -o 'SWIRL_SEEN.*' /tmp/bo_${tag}_${ch}_${who}.log); $(grep '^AT' /tmp/bo_${tag}_${ch}_${who}.log | sed -E 's/^AT ([0-9]+) .*"pose":([a-z]+).*"standOp":"?([0-9.]*)"?.*/\1ms pose=\2 stand=\3/' | tr '\n' ' ')"; }
r br 1 ryo tap
r br 1 aoi tap
r br 2 ryo api ROOM=c2_club FFD_INDEX=$W/index.html
r br 2 aoi api ROOM=c2_club FFD_INDEX=$W/index.html
r live 2 ryo api ROOM=c2_club FFD_INDEX=/workspace/release/wt/index.html
r live 2 aoi api ROOM=c2_club FFD_INDEX=/workspace/release/wt/index.html
L=/workspace/alleycat/tests/logs_522; mkdir -p $L; cd $W; export FFD=$W FFD_INDEX=$W/index.html
t(){ n=$1; shift; wl; timeout 1500 "$@" > $L/$n.log 2>&1; note "test $n rc=$? $(grep -v '^\s*$' $L/$n.log | tail -1 | cut -c1-160)"; }
t s2 $P tools/s2/s2_test.py index.html
t ngp $P tools/ngp/ngp_test.py $W/index.html
t verify_wired bash -c "cd /workspace/v6560-review/portraits && $P verify_wired.py $W"
t amb_check $P /workspace/ambsafe/p2/amb_check.py $W 54730
t ch_smoke $P tools/yk/ch_smoke.py $W 54711
wl; cd /workspace/alleycat/perf; timeout 3600 $P perf_check.py c1a3b8c $TIP --throttle 4 --repo /workspace/ffd --only world,battle --runs 2 > perf_522.log 2>&1
note "perf_check c1a3b8c vs $TIP x4 (world,battle; interleaved 2 runs): $(grep -c '^- PASS' perf_522.log) PASS / $(grep -c '^- FAIL' perf_522.log) FAIL; fails: $(grep '^- FAIL' perf_522.log | tr '\n' ' ' | cut -c1-600)"
note "FINAL522 DONE"
