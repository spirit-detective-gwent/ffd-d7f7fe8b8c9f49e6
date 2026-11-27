#!/bin/bash
P=/workspace/pwenv/bin/python3; cd /workspace/alleycat/tools; N=/workspace/alleycat/NOTES.md
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
r(){ tag=$1; ch=$2; who=$3; trig=$4; shift 4; wl; env "$@" timeout 300 $P bo.py $tag $ch $who $trig > /tmp/bo_${tag}_${ch}_${who}.log 2>&1
  echo "- bo $tag ch$ch $who ($trig): swirl $(grep -o 'SWIRL_SEEN.*' /tmp/bo_${tag}_${ch}_${who}.log); $(grep '^AT' /tmp/bo_${tag}_${ch}_${who}.log | sed -E 's/.*"pose":([a-z]+).*"tip":([a-z]+).*"standOp":"?([0-9.]*)"?.*/pose=\1 tip=\2 standOp=\3/' | tr '\n' ' ')" >> $N; }
r br 1 aoi tap
r br 2 ryo api FFD_INDEX=/workspace/alleycat/wt/index.html
r br 2 aoi api FFD_INDEX=/workspace/alleycat/wt/index.html
r live 1 ryo api PORT=8802 ROOT=/workspace/release/wt
r live 1 aoi api PORT=8802 ROOT=/workspace/release/wt
r live 2 ryo api FFD_INDEX=/workspace/release/wt/index.html
echo BOALL >> /tmp/bo_all.done
