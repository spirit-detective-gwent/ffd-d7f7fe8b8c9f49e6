#!/bin/bash
# alleycat regression lane on /workspace/alleycat/wt. serial, waits while load>=6. logs in logs/
P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; L=/workspace/alleycat/tests/logs; mkdir -p $L; : > $L/summary.log
export FFD=$W FFD_INDEX=$W/index.html BOND_PORT=8987
cd $W
run() { n=$1; shift; while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 30; done
  echo "== $n start $(date +%T)" >> $L/summary.log
  timeout 1500 "$@" > $L/$n.log 2>&1; rc=$?
  echo "$n rc=$rc $(tail -1 $L/$n.log | cut -c1-200)" >> $L/summary.log; }
run verify_wired bash -c "cd /workspace/v6560-review/portraits && $P verify_wired.py $W"
run s2 $P tools/s2/s2_test.py index.html
run ngp $P tools/ngp/ngp_test.py $W/index.html
run bond $P tools/bond/bond_test.py
run ch_smoke $P tools/yk/ch_smoke.py $W 54711
run no_old_art $P tools/yk/test_no_old_art.py $W 54721 q
run amb_check $P /workspace/ambsafe/p2/amb_check.py $W 54730
run ground env PORT=54757 $P tools/ground/test_ground.py $W/index.html
echo LANEDONE >> $L/summary.log
