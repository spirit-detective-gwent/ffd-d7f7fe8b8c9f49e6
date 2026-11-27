#!/bin/bash
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; T=/workspace/alleycat/tools
TIP=$(git -C $W rev-parse --short HEAD)
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while pgrep -f "perf527.sh" >/dev/null; do sleep 15; done
cd $T
r(){ tag=$1; ch=$2; who=$3; trig=$4; shift 4; wl; env "$@" timeout 300 $P bo.py $tag $ch $who $trig > /tmp/bo3_${tag}_${ch}_${who}.log 2>&1; rc=$?
  note "battle-open(v3 probe) $tag ch$ch $who ($trig $*) rc=$rc: $(grep '^AT' /tmp/bo3_${tag}_${ch}_${who}.log | sed -E 's/^AT ([0-9]+) .*"pose":([a-z]+).*"standOp":"?([0-9.]*)"?.*/\1ms pose=\2 stand=\3/' | tr '\n' ' ') $(grep -o 'T527.*' /tmp/bo3_${tag}_${ch}_${who}.log) PROBE $(grep -o 'PROBE.*' /tmp/bo3_${tag}_${ch}_${who}.log | cut -c7-400)"; }
r br 1 ryo tap
r br 1 aoi tap
r br 2 ryo api ROOM=c2_club FFD_INDEX=$W/index.html
r br 2 aoi api ROOM=c2_club FFD_INDEX=$W/index.html
r live 2 aoi api ROOM=c2_club FFD_INDEX=/workspace/release/wt/index.html
cd /workspace/alleycat/perf; wl; note "perf soak start load=$(cut -d' ' -f1 /proc/loadavg)"
timeout 3000 $P perf_check.py c1a3b8c $TIP --throttle 4 --repo /workspace/ffd --only soak > perf_528_soak.log 2>&1
note "perf_check c1a3b8c vs $TIP --only soak: $(grep -E '^- (PASS|FAIL)' perf_528_soak.log | tr '\n' ' ' | cut -c1-500) load=$(cut -d' ' -f1 /proc/loadavg)"
note "V528 DONE"
