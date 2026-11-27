import json, sys
from PIL import Image, ImageDraw
tag=sys.argv[1]; step=int(sys.argv[2]) if len(sys.argv)>2 else 2; out=sys.argv[3] if len(sys.argv)>3 else '/tmp/%s_strip.png'%tag
R='/workspace/alleycat/shots/raw/'
S=json.load(open(R+tag+'_boxes.json'))
fr=[s for s in S[::step]]
# fixed crop centred on foe start
fx,fy=S[0][1][4],S[0][1][5]
crops=[]
for fn,bx in fr:
    im=Image.open(fn).convert('RGB'); k=im.size[0]/390
    cx=fx+20; cy=fy+30
    c=im.crop((int((cx-95)*k),int((cy-90)*k),int((cx+95)*k),int((cy+70)*k)))
    d=ImageDraw.Draw(c); d.text((4,4),fn[-8:-4]+'ms',fill=(255,255,0)); crops.append(c)
cw,ch=crops[0].size; cols=8; rows=(len(crops)+cols-1)//cols
M=Image.new('RGB',(cw*cols,ch*rows))
for i,c in enumerate(crops): M.paste(c,((i%cols)*cw,(i//cols)*ch))
M.save(out); print(out, M.size, len(crops))
