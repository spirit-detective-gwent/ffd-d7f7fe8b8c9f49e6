#!/bin/bash
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; T=/workspace/alleycat/tools
TIP=$(git -C $W rev-parse --short HEAD)
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while pgrep -f "bo527.sh$|bo527.sh " >/dev/null; do sleep 15; done
cd $T
r(){ tag=$1; ch=$2; who=$3; trig=$4; shift 4; wl; env "$@" timeout 300 $P bo.py $tag $ch $who $trig > /tmp/bo_${tag}_${ch}_${who}.log 2>&1; rc=$?
  note "battle-open(t527 v2) $tag ch$ch $who ($trig $*) rc=$rc: $(grep -o 'SWIRL_SEEN.*' /tmp/bo_${tag}_${ch}_${who}.log); $(grep '^AT' /tmp/bo_${tag}_${ch}_${who}.log | sed -E 's/^AT ([0-9]+) .*"pose":([a-z]+).*"standOp":"?([0-9.]*)"?.*/\1ms pose=\2 stand=\3/' | tr '\n' ' ') $(grep -o 'T527.*' /tmp/bo_${tag}_${ch}_${who}.log)"; }
r br 1 ryo tap
note "BO527 ryo-rerun DONE"
