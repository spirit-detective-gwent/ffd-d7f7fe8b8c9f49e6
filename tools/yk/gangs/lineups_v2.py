# lineups_v2.py : each gang character's existing portrait beside the v2 sprites (stand + battle). Previews only.
import sys, textwrap
from PIL import Image, ImageDraw
from sheets import F1,F2,F3,F4,BG,PAN,O,walk,tight,sc
PT='/workspace/ffd-gangs/portraits/'
def panel(title,ptfile,ptlabel,spec,note):
  if ptfile:
    p=Image.open(ptfile).convert('RGBA'); p=p.resize((int(p.width*360/p.height),360),Image.LANCZOS)
  else:
    p=Image.new('RGBA',(270,360),(60,60,72,255)); d=ImageDraw.Draw(p)
    for i,ln in enumerate(textwrap.wrap(ptlabel,22)): d.text((14,140+i*24),ln,font=F2,fill=(230,230,240))
  st=tight(walk(f'baked/{spec}_walk.webp',0,2)); st=sc(st,360/st.height*0.98 if st.height*1.5>360 else 1.5)
  fg=tight(Image.open(f'baked/{spec}_fig.webp').convert('RGBA'),4); fg=sc(fg,360/fg.height*0.98)
  W=p.width+st.width+fg.width+4*18; H=360+44+40+26*4
  P=Image.new('RGBA',(W,H),PAN+(255,)); d=ImageDraw.Draw(P); d.text((18,10),title,font=F2,fill=(255,230,160))
  x=18; y=44
  for im,lb in ((p,(ptlabel or 'Portrait (in game now)') if ptfile else 'No portrait'),(st,'Stand'),(fg,'Battle')):
    P.alpha_composite(im,(x,y+360-im.height)); d.text((x,y+366),lb,font=F4,fill=(210,210,225)); x+=im.width+18
  for i,ln in enumerate(textwrap.wrap(note,int(W/9.6))[:4]): d.text((18,y+394+i*24),ln,font=F3,fill=(235,235,235))
  return P
def sheet(name,title,items,per=3):
  ps=[panel(*it) for it in items]; rows=[ps[i:i+per] for i in range(0,len(ps),per)]
  RW=[sum(p.width for p in r)+16*(len(r)-1) for r in rows]; RH=[max(p.height for p in r) for r in rows]
  T=Image.new('RGBA',(max(RW)+40,110+sum(RH)+16*len(rows)),BG+(255,)); d=ImageDraw.Draw(T)
  d.text((20,14),title,font=F1,fill=(255,255,255)); d.text((20,56),'Each character: the existing dialogue portrait, then the redrawn cel sprite standing and in battle. Hand-painted in-engine (tools/yk). Previews only, not in the game.',font=F3,fill=(200,200,215))
  y=100
  for r,h in zip(rows,RH):
    x=20
    for p in r: T.alpha_composite(p,(x,y)); x+=p.width+16
    y+=h+16
  T.convert('RGB').save(O+name); print(O+name,T.size)
K=[('"High-Score" Jin (boss)',PT+'jin_calm.webp','', 'ksJin2','Shaggy black hair with lime tips, lime zip hoodie with the hood bunched at the neck, black tee, black headphones with lime rings, slim build, soft eyes and a smirk.'),
   ('Black-Suit Bouncer (lt.)',PT+'bouncer_neutral.webp','','ksBouncer2','Slick side-parted black hair, black shades, tanned square jaw, black single-breasted suit, white shirt open at the collar, no tie. Head drawn bigger.'),
   ('Kitsune Suit (uniform A)',PT+'c2suit_neutral.webp','','ksSuit2','Black baseball cap, black shades, charcoal pinstripe double-breasted suit with silver buttons, dark maroon shirt, no tie, stocky with a wide jaw.'),
   ('Kitsune Runner (uniform B)',None,'No portrait. Approved design kept.','ksRun2','No portrait exists, so the approved crimson bomber with the gold fox on the back is kept. Cheek scar and coat flecks fixed.'),
   ('Sabu (Nails\' crew)','ext/n13sb_fig.webp','Talk picture now (old figure)','sabu2','No portrait was made for Sabu; his talk box shows his battle figure (left, the old one). Approved purple sukajan look kept, scar fixed. Once wired, the new figure becomes his talk picture.')]
D=[('Foreman Masa (boss)',PT+'masa_calm.webp','','dpMasa2','Plain yellow hard hat, orange coverall buttoned up over a black tee, silver reflective braces and bands, chest pockets, heavy build, wide stubbled jaw, thick brows. The charcoal coat is gone (not in the portrait).'),
   ('Depot Rider (uniform A)',PT+'c2boso_neutral.webp','','dpRider2','Purple long tokkofuku stitched with rows of gold crosses, sarashi, tall black pompadour with a dark band, white surgical mask, gold wristbands. Replaces the orange/charcoal look.'),
   ('Dock hand (uniform B)',None,'No portrait. Approved design kept.','dpDock2','No portrait exists, so the approved hi-vis coverall + tenugui look is kept (matches Masa\'s orange). Scar and flecks fixed.')]
w=sys.argv[1] if len(sys.argv)>1 else 'kd'
if 'k' in w: sheet('kitsune_lineup_v2.png','Club Kitsune + Sabu v2: matched to the portraits',K)
if 'd' in w: sheet('depot_lineup_v2.png','The Depot v2: matched to the portraits',D)
