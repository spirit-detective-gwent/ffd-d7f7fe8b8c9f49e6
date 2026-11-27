#!/bin/bash
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt
TIP=$(git -C $W rev-parse --short HEAD)
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while pgrep -f "final527.sh|bo527.sh" >/dev/null; do sleep 15; done
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
cd /workspace/alleycat/perf
for o in battle world; do wl; note "perf527 $o start load=$(cut -d' ' -f1 /proc/loadavg)"
  timeout 3000 $P perf_check.py c1a3b8c $TIP --throttle 4 --repo /workspace/ffd --only $o --runs 3 > perf_527_$o.log 2>&1
  note "perf_check c1a3b8c vs $TIP x4 --only $o --runs 3 (interleaved): $(grep -c '^- PASS' perf_527_$o.log) PASS / $(grep -c '^- FAIL' perf_527_$o.log) FAIL; $(grep -E '^\| x4 battle (fps|cpu_busy_pct)' perf_527_$o.log | tr '\n' ' '); fails: $(grep '^- FAIL' perf_527_$o.log | tr '\n' ' ' | cut -c1-500); load=$(cut -d' ' -f1 /proc/loadavg)"
done
note "PERF527 DONE"
