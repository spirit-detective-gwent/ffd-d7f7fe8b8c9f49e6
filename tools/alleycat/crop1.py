import json, sys
from PIL import Image
tag, idx = sys.argv[1], [int(x) for x in sys.argv[2].split(',')]; out=sys.argv[3]
R='/workspace/alleycat/shots/raw/'; S=json.load(open(R+tag+'_boxes.json'))
fx,fy=S[0][1][4],S[0][1][5]; cs=[]
for i in idx:
    fn,bx=S[i]; im=Image.open(fn).convert('RGB'); k=im.size[0]/390
    cs.append(im.crop((int((fx-85)*k),int((fy-10)*k),int((fx+95)*k),int((fy+110)*k))).resize((540,360)))
M=Image.new('RGB',(540*len(cs),360)); [M.paste(c,(i*540,0)) for i,c in enumerate(cs)]; M.save(out); print(out)
