# sheets.py : design sheets + lineups for the Ch2 gangs pass (previews only)
from PIL import Image, ImageDraw, ImageFont
import textwrap
FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'; FR='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F1=ImageFont.truetype(FB,30); F2=ImageFont.truetype(FB,20); F3=ImageFont.truetype(FR,18); F4=ImageFont.truetype(FB,16)
BG=(34,32,42); PAN=(78,78,94); O='/workspace/v6560-review/gangs/'; WD='/workspace/ffd-gangs/world/'
def walk(path,r,c): return Image.open(path).convert('RGBA').crop((c*208,r*272,(c+1)*208,(r+1)*272))
def tight(im,pad=6):
  b=im.getbbox(); return im.crop((max(0,b[0]-pad),max(0,b[1]-pad),min(im.width,b[2]+pad),min(im.height,b[3]+pad))) if b else im
def sc(im,k,nearest=True): return im.resize((max(1,int(im.width*k)),max(1,int(im.height*k))),Image.NEAREST if nearest else Image.LANCZOS)
def panel(ims,label,gap=14,pad=14,h=None):
  H=h or max(i.height for i in ims)+2*pad+30; W=sum(i.width for i in ims)+gap*(len(ims)-1)+2*pad
  P=Image.new('RGBA',(W,H),PAN+(255,)); d=ImageDraw.Draw(P); d.text((pad,6),label,font=F4,fill=(255,230,160)); x=pad
  for i in ims: P.alpha_composite(i,(x,H-pad-i.height)); x+=i.width+gap
  return P
def hrow(ps,gap=16):
  W=sum(p.width for p in ps)+gap*(len(ps)-1); H=max(p.height for p in ps); R=Image.new('RGBA',(W,H),BG+(255,)); x=0
  for p in ps: R.alpha_composite(p,(x,0)); x+=p.width+gap
  return R
def sheet(key,spec,title,sub,pal,notes,old=None,oldwalk=None):
  wk=f'baked/{spec}_walk.webp'; fg=Image.open(f'baked/{spec}_fig.webp').convert('RGBA')
  stand=panel([sc(tight(walk(wk,0,2)),2.4)],'Front, standing (2.4x)')
  wf=[sc(tight(walk(wk,0,0)),1.5),sc(tight(walk(wk,1,4)),1.5),sc(tight(walk(wk,2,1)),1.5),sc(tight(walk(wk,3,5)),1.5)]
  walkp=panel(wf,'Walk frames: front / left / right / back (1.5x)',h=stand.height)
  figp=panel([sc(tight(fg,4),3.2)],'Battle figure (3.2x)',h=stand.height)
  top=hrow([stand,walkp,figp])
  strip=panel([tight(walk(wk,0,c)) for c in range(8)],'Front walk cycle, all 8 frames (1x, in-game size is smaller still)')
  # palette
  sw=Image.new('RGBA',(640,40+36*len(pal)),PAN+(255,)); d=ImageDraw.Draw(sw); d.text((14,6),'Palette',font=F4,fill=(255,230,160))
  for n,(hx,nm) in enumerate(pal):
    y=36+n*36; c=tuple(int(hx[i:i+2],16) for i in (1,3,5)); d.rectangle((14,y,58,y+28),fill=c,outline=(18,16,22),width=2); d.text((70,y+4),f'{hx}  {nm}',font=F3,fill=(240,240,240))
  op=None
  if old:
    oi=[tight(walk(oldwalk,0,2))] if oldwalk else []
    of=tight(Image.open(old).convert('RGBA')); of=sc(of,min(1.0,250/of.height),False); oi.append(of)
    op=panel(oi,'Before (current art)')
  nw=max(700,top.width-sw.width-16-(op.width+16 if op else 0)); lines=[]
  for para in notes: lines+=textwrap.wrap(para,int(nw/10.4))+['']
  nh=max(sw.height,(op.height if op else 0),40+23*len(lines))
  nt=Image.new('RGBA',(nw,nh),PAN+(255,)); d=ImageDraw.Draw(nt); d.text((14,6),'Design notes',font=F4,fill=(255,230,160)); y=34
  for ln in lines: d.text((14,y),ln,font=F3,fill=(235,235,235)); y+=23 if ln else 8
  bot=hrow([sw,nt]+([op] if op else []))
  if bot.height<strip.height: pass
  Wt=max(top.width,strip.width,bot.width)
  T=Image.new('RGBA',(Wt+40,90+top.height+strip.height+bot.height+60),BG+(255,)); d=ImageDraw.Draw(T)
  d.text((20,14),title,font=F1,fill=(255,255,255)); d.text((20,52),sub,font=F2,fill=(200,200,215))
  y=90
  for part in (top,strip,bot): T.alpha_composite(part,(20,y)); y+=part.height+20
  T.convert('RGB').save(O+key+'_preview.png'); print(O+key+'_preview.png',T.size)
def lineup(name,title,items,refs):
  def col(path,figpath,label,new):
    s=sc(tight(walk(path,0,2)),1.6); f=sc(tight(Image.open(figpath).convert('RGBA'),4),1.6)
    H=440+340; C=Image.new('RGBA',(max(s.width,f.width)+20,H+40),(PAN if new else (60,60,72))+(255,)); d=ImageDraw.Draw(C)
    C.alpha_composite(s,((C.width-s.width)//2,440-s.height)); C.alpha_composite(f,((C.width-f.width)//2,H-f.height))
    for i,ln in enumerate(textwrap.wrap(label,14)[:2]): d.text((8,H+2+i*18),ln,font=F4,fill=(255,230,160) if new else (200,200,210))
    return C
  cs=[col(*r,False) for r in refs]+[col(*i,True) for i in items]
  R=hrow(cs,10); T=Image.new('RGBA',(R.width+40,R.height+110),BG+(255,)); d=ImageDraw.Draw(T)
  d.text((20,14),title,font=F1,fill=(255,255,255)); d.text((20,54),'Left, darker: existing new-pass cels (live files).  Right, lighter: this pass.  Top row standing (1.6x), bottom row battle figure.',font=F3,fill=(200,200,215))
  T.alpha_composite(R,(20,90)); T.convert('RGB').save(O+name); print(O+name,T.size)
