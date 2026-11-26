#!/workspace/pwenv/bin/python3
"""Record a short EATG sweet-roll clip (bites + pull-apart) for the Phase 1 preview."""
import sys, os, shutil, subprocess, base64, json, wave, time, tempfile
from pathlib import Path
sys.path.insert(0, '/workspace/minigame-mock')
import capture
OUT = Path('/workspace/v6560-review/seal2/phase1')
tmp = '/tmp/s2-eat-clip'
# one clean Ryo win, including the pull beat, a short result hold
segs = [('sweetroll','ryo','win',11,'SWEET ROLL — mash, then tap to pull apart',0,2.4)]
capture.make('sweetroll_pull', segs, str(OUT/'eat_sweetroll_v2.mp4'), tmp)
# also dump a few stills from the frames if they remain; capture cleans tmp after
print('clip done')
