# mkvid.py tag out_basename [speed]  -> out.mp4 (cropped around the pair, real speed by virtual timestamps) + out_strip.png
import json, sys, os, subprocess, tempfile, shutil
from PIL import Image, ImageDraw
tag, out = sys.argv[1], sys.argv[2]; speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
R='/workspace/alleycat/shots/raw/'; S=json.load(open(R+tag+'_boxes.json'))
fx,fy=S[0][1][4],S[0][1][5]
def crop(fn):
    im=Image.open(fn).convert('RGB'); k=im.size[0]/390
    return im.crop((int((fx-90)*k),int((fy-45)*k),int((fx+110)*k),int((fy+105)*k)))
ts=[int(os.path.basename(f)[-9:-4]) for f,_ in S]
td=tempfile.mkdtemp(); fps=30; n=0
end = ts[-1]
for i,(f,_) in enumerate(S):
    t0=ts[i]; t1=ts[i+1] if i+1<len(S) else t0+200
    c=crop(f); reps=max(1,round((t1-t0)/speed/1000*fps))
    for r in range(reps): c.save('%s/f%05d.png'%(td,n)); n+=1
subprocess.run(['ffmpeg','-v','error','-y','-framerate',str(fps),'-i',td+'/f%05d.png','-vf','scale=trunc(iw/2)*2:trunc(ih/2)*2,format=yuv420p','-c:v','libx264','-crf','20',out+'.mp4'],check=True)
shutil.rmtree(td)
# strip: ~12 evenly spaced frames over the action
idx=[round(i*(len(S)-1)/11) for i in range(12)]
cs=[crop(S[i][0]).resize((200,150)) for i in idx]
M=Image.new('RGB',(200*6,150*2+0),(0,0,0))
for j,c in enumerate(cs):
    d=ImageDraw.Draw(c); d.text((4,3),'%d ms'%ts[idx[j]],fill=(255,230,0)); M.paste(c,((j%6)*200,(j//6)*150))
M.save(out+'_strip.png'); print(out, n, 'frames')
