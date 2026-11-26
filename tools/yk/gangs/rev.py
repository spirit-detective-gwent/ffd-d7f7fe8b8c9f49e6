import sys
from PIL import Image
BG=(92,92,108,255)
def cell(s,r,c,k=1):
  a=Image.open(f'baked/{s}_walk.webp').convert('RGBA').crop((c*208,r*272,(c+1)*208,(r+1)*272)); return a.resize((208*k,272*k),Image.NEAREST) if k!=1 else a
def fig(s,k=2):
  a=Image.open(f'baked/{s}_fig.webp').convert('RGBA'); return a.resize((a.width*k,a.height*k),Image.LANCZOS)
specs=sys.argv[1].split(','); out=sys.argv[2]
rows=[]
for s in specs:
  ims=[cell(s,0,2,2),cell(s,1,2),cell(s,2,4),cell(s,3,2),fig(s,3)]
  W=Image.new('RGBA',(sum(i.width for i in ims)+10*len(ims),544),BG); x=0
  for i in ims: W.alpha_composite(i,(x,544-i.height)); x+=i.width+10
  rows.append(W)
T=Image.new('RGBA',(max(r.width for r in rows),544*len(rows)),BG)
for n,r in enumerate(rows): T.alpha_composite(r,(0,n*544))
T.convert('RGB').save(out)
