#!/bin/bash
# final chain at the tip: regen side/back clips, battle shots, tests, interleaved perf 3+3. Appends to NOTES.md.
N=/workspace/alleycat/NOTES.md; P=/workspace/pwenv/bin/python3; W=/workspace/alleycat/wt; T=/workspace/alleycat/tools; S=/workspace/alleycat/shots
TIP=$(git -C $W rev-parse --short HEAD)
wl(){ while [ "$(cut -d' ' -f1 /proc/loadavg | cut -d. -f1)" -ge 6 ]; do sleep 20; done; }
note(){ echo "- [$TIP] $*" >> $N; echo "$*"; }
while ! grep -q ALLTAP /tmp/c2tap2.log 2>/dev/null; do sleep 15; done
cd $T
for sp in "ryo left g_br_ryo_side after_ryo_side" "aoi left g_br_aoi_side after_aoi_side" "ryo down g_br_ryo_back after_ryo_back" "aoi down g_br_aoi_back after_aoi_back" "ryo up g_br_ryo_front after_ryo_front" "aoi up g_br_aoi_front after_aoi_front"; do set -- $sp; wl
  timeout 250 $P td.py 8801 $W $1 $2 $3 > /tmp/td_$3.log 2>&1; rc=$?
  python3 mkvid.py $3 $S/$4 > /tmp/mk_$3.log 2>&1; note "regen $4.mp4/_strip.png (td rc=$rc, $(grep -o 'world:opn:td:v:[a-z]*' /tmp/td_$3.log | head -1 || true), $(tail -1 /tmp/mk_$3.log))"
done
wl; timeout 600 $P bt.py 8801 $W bt > /tmp/bt_final.log 2>&1; rc=$?
for n in ch1lib ch1yard ch2udon ch2street; do cp $S/raw/bt_${n}_open.png $S/battle_open_downed_$n.png 2>/dev/null; done
python3 - <<'PY'
from PIL import Image
R='/workspace/alleycat/shots/raw/'; S='/workspace/alleycat/shots/'
for n in ('ch1lib','ch1yard','ch2udon','ch2street'):
  fs=['bt_%s_open'%n]+['bt_%s_rise%04d'%(n,m) for m in (120,260,450,1400)]
  ims=[Image.open(R+f+'.png').convert('RGB').resize((390,844)).crop((0,0,390,330)) for f in fs]
  M=Image.new('RGB',(390*5,330))
  for i,c in enumerate(ims): M.paste(c,(i*390,0))
  M.save(S+'battle_open_downed_%s_strip.png'%n)
PY
note "battle shots rc=$rc: $(grep -E '^ch.* (\{|after)' /tmp/bt_final.log | tr '\n' ' ' | cut -c1-900)"
L=/workspace/alleycat/tests/logs_final; mkdir -p $L; cd $W
t(){ n=$1; shift; wl; timeout 1500 "$@" > $L/$n.log 2>&1; note "test $n rc=$? $(grep -v '^\s*$' $L/$n.log | tail -1 | cut -c1-160)"; }
export FFD=$W FFD_INDEX=$W/index.html BOND_PORT=8987
t verify_wired bash -c "cd /workspace/v6560-review/portraits && $P verify_wired.py $W"
t s2 $P tools/s2/s2_test.py index.html
t ngp $P tools/ngp/ngp_test.py $W/index.html
t ch_smoke $P tools/yk/ch_smoke.py $W 54711
t amb_check $P /workspace/ambsafe/p2/amb_check.py $W 54730
t ground env PORT=54757 $P tools/ground/test_ground.py $W/index.html
D=/workspace/alleycat/perf/final; mkdir -p $D; cd $D
for i in 1 2 3; do for w in live br; do wl
  [ $w = live ] && I=/workspace/release/wt/index.html || I=$W/index.html
  for try in 1 2; do DPR=3 timeout 900 $P $T/perf_ac.py $I $w$i $D/$w$i.json > $D/$w$i.log 2>&1 && break; done
  note "perf $w$i $(grep '^RES' $D/$w$i.log | cut -c5-500)"
done; done
note "FINAL2 DONE"
