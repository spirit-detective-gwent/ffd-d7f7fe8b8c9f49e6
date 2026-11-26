import sys
from PIL import Image
BG=(92,92,108,255); ims=[]
for s in sys.argv[1].split(','):
  a=Image.open(f'baked/{s}_walk.webp').convert('RGBA').crop((2*208+30,0,3*208-30,272)); ims.append(a.resize((a.width*3,a.height*3),Image.NEAREST))
  f=Image.open(f'baked/{s}_fig.webp').convert('RGBA'); ims.append(f.resize((f.width*4,f.height*4),Image.NEAREST))
W=Image.new('RGBA',(sum(i.width for i in ims),max(i.height for i in ims)),BG); x=0
for i in ims: W.alpha_composite(i,(x,0)); x+=i.width
W.convert('RGB').save(sys.argv[2])
