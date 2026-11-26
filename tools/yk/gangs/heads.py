import sys
from PIL import Image
specs=sys.argv[1].split(','); ims=[]
for s in specs:
  a=Image.open(f'baked/{s}_walk.webp').convert('RGBA').crop((2*208+50,10,3*208-50,100)); a=a.resize((a.width*4,a.height*4),Image.NEAREST)
  f=Image.open(f'baked/{s}_fig.webp').convert('RGBA').crop((20,0,104,60)); f=f.resize((f.width*6,f.height*6),Image.NEAREST)
  ims.append((a,f))
W=Image.new('RGB',(max(a.width+f.width+10 for a,f in ims),sum(max(a.height,f.height) for a,f in ims)),(92,92,108));y=0
for a,f in ims: W.paste(a,(0,y),a); W.paste(f,(a.width+10,y),f); y+=max(a.height,f.height)
W.save(sys.argv[2])
