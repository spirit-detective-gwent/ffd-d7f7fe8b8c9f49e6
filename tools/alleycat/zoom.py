import json, sys
from PIL import Image, ImageDraw
tag=sys.argv[1]; a,b=int(sys.argv[2]),int(sys.argv[3]); n=int(sys.argv[4]) if len(sys.argv)>4 else 8; out=sys.argv[5] if len(sys.argv)>5 else '/tmp/zoom.png'
R='/workspace/alleycat/shots/raw/'; S=json.load(open(R+tag+'_boxes.json')); fx,fy=S[0][1][4],S[0][1][5]
ts=[int(f[-9:-4]) for f,_ in S]; sel=[i for i,t in enumerate(ts) if a<=t<=b]
sel=[sel[round(j*(len(sel)-1)/(n-1))] for j in range(n)] if len(sel)>n else sel
cs=[]
for i in sel:
    im=Image.open(S[i][0]).convert('RGB'); k=im.size[0]/390
    c=im.crop((int((fx-55)*k),int((fy-50)*k),int((fx+75)*k),int((fy+95)*k))).resize((260,290)); ImageDraw.Draw(c).text((3,3),str(ts[i]),fill=(255,0,0)); cs.append(c)
M=Image.new('RGB',(260*len(cs),290)); [M.paste(c,(j*260,0)) for j,c in enumerate(cs)]; M.save(out)
