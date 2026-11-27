#!/bin/bash
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; TIP=54f2764
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while pgrep -f "v528.sh" >/dev/null; do sleep 15; done
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
cd /workspace/alleycat/perf; cp results_world.json results_world_527full.json; wl; note "perf spots rerun start load=$(cut -d' ' -f1 /proc/loadavg)"
PERF_SPOTS=ch1_grounds,ch2_lantern_alley,ch2_town_centre,ch2_genji_gym timeout 3600 $P perf_check_spots.py c1a3b8c $TIP --throttle 4 --repo /workspace/ffd --only world --runs 3 --walk 5 > perf_528_spots.log 2>&1
note "perf spots rerun (x4 interleaved 3 runs, ch1_grounds/lantern/town/gym): $(grep -E '^\| x4 .*(fps|cpu_busy)' perf_528_spots.log | tr '\n' ' ') fails: $(grep '^- FAIL' perf_528_spots.log | tr '\n' ' ' | cut -c1-400) load=$(cut -d' ' -f1 /proc/loadavg)"
note "PERFSPOTS DONE"
