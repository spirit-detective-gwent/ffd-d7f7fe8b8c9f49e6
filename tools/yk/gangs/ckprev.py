from PIL import Image, ImageDraw
ROWS=[('Club Hostess (ck_hostess) + coat check','ckHostess','/workspace/ffd-ports/portraits/ckhostess_neutral.webp'),
      ('Club Dealer (ck_dealer) = bartender too','ckDealer','/workspace/ffd-ports/portraits/ckdealer_neutral.webp'),
      ('Chip-cage cashier: PREVIEW, no portrait yet','ckCashier',None)]
BG=(52,48,58,255); rows=[]
for title,s,port in ROWS:
  parts=[]
  if port: p=Image.open(port).convert('RGBA'); parts.append(p.resize((int(p.width*272/p.height),272),Image.LANCZOS))
  w=Image.open(f'baked/{s}_walk.webp').convert('RGBA')
  for r in range(4): parts.append(w.crop((0,r*272,208,r*272+272)))
  for c in (1,3): parts.append(w.crop((c*208,272,c*208+208,544)))
  f=Image.open(f'baked/{s}_fig.webp').convert('RGBA'); parts.append(f.resize((f.width*272//192,272),Image.LANCZOS))
  for k in ('fig_hurt','fig_down'):
    try: g=Image.open(f'baked/{s}_{k}.webp').convert('RGBA'); sc=min(272/g.height,1.4); parts.append(g.resize((int(g.width*sc),int(g.height*sc)),Image.LANCZOS))
    except FileNotFoundError: pass
  W=sum(p.width for p in parts)+12*len(parts)+12; o=Image.new('RGBA',(W,272+34),BG); x=12
  for p in parts: o.alpha_composite(p,(x,34+272-p.height)); x+=p.width+12
  ImageDraw.Draw(o).text((12,8),title,fill=(240,230,210,255)); rows.append(o)
W=max(r.width for r in rows); O=Image.new('RGBA',(W,sum(r.height for r in rows)),BG); y=0
for r in rows: O.alpha_composite(r,(0,y)); y+=r.height
O.convert('RGB').save('/workspace/v6560-review/gangs/club_staff_preview.png'); print(O.size)
