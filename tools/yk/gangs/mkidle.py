# bake breathing idle sheets (Flip style: frame0 = walk col0, upper body drops 0/1/2/1 px, feet fixed, smooth seam at hips)
# breathing idle builder (method from ch2-idle: frame 0 of each walk row, upper body drops 0/1/2/1 px, feet fixed)
import sys, numpy as np
from PIL import Image
def smooth(t): t=np.clip(t,0,1); return t*t*(3-2*t)
def idle(walk_path, out_path):
    W=Image.open(walk_path).convert('RGBA'); out=Image.new('RGBA',(208*4,272*4))
    for r in range(4):
        c=np.array(W.crop((0,r*272,208,r*272+272))).astype(float)
        a=c[...,3]>0; rows=np.where(a.any(1))[0]; top,bot=rows[0],rows[-1]
        Ys=top+0.55*(bot-top); ramp=9
        pm=c.copy(); pm[...,:3]*=pm[...,3:4]/255.0
        for f,dy in enumerate((0,1,2,1)):
            o=pm.copy()
            if dy:
                ys=np.arange(272,dtype=float)
                w=1-smooth((ys-(Ys-ramp))/(2*ramp))
                src=ys-dy*w
                lo=np.clip(np.floor(src).astype(int),0,271); hi=np.clip(lo+1,0,271); fr=(src-lo)[:,None,None]
                o=pm[lo]*(1-fr)+pm[hi]*fr
            al=o[...,3:4]; rgb=np.where(al>0,o[...,:3]/np.maximum(al,1e-6)*255.0,0)
            res=np.concatenate([np.clip(rgb,0,255),al],axis=2).round().astype(np.uint8)
            out.paste(Image.fromarray(res,'RGBA'),(f*208,r*272))
    out.save(out_path,'WEBP',lossless=True,quality=100,method=6)
if __name__=='__main__':
    idle(sys.argv[1],sys.argv[2])
