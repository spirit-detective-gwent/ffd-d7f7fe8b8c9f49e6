import json
J={}
F4=['front','left','right','back']
for w0 in ['ryo','aoi','ryoS','aoiS','ryoL','aoiL']:
  w=w0[:3]; sfx={'':'', 'S':'s','L':'l'}[w0[3:]]; e='ext/' ; wd='world/'
  J[f'of_{w}_yankii{sfx}_walk']=dict(spec=w0,src=e+f'{w}_walk.webp',cols=8,rows=4,cw=208,ch=272)
  J[f'of_{w}_yankii{sfx}_jog']=dict(spec=w0,src=e+f'{w}_jog.webp',cols=12 if w=='ryo' else 8,rows=4,cw=208,ch=272)
  J[f'of_{w}_yankii{sfx}_rdy']=dict(spec=w0,src=e+f'{w}_rdy.webp',cols=4,rows=4,cw=208,ch=272)
  J[f'of_{w}_yankii{sfx}_kn']=dict(spec=w0,src=e+f'{w}_kn.webp',cols=4,rows=4,cw=208,ch=272)
  J[f'of_{w}_yankii{sfx}_amb']=dict(spec=w0,src=e+f'{w}_amb.webp',cols=5,rows=2,cw=384,ch=320,faces=['right','right'])
  J[f'of_{w}_yankii{sfx}_ambv']=dict(spec=w0,src=wd+f'{w}_ambv.webp',cols=5,rows=4,cw=384,ch=448,faces=['front','front','back','back'])
  J[f'of_{w}_yankii{sfx}_cact']=dict(spec=w0,src=e+f'{w}_cact.webp',cols=6,rows=5,cw=208,ch=272,faces=['front']*5)
  J[f'of_{w}_yankii{sfx}_gym']=dict(spec=w0,src=wd+f'{w}_gym.webp',cols=8,rows=3,cw=208,ch=272,faces=['right','right','right'])
P={'c2_punkY1':'punkA','c2_punkY2':'punkB','c2_punkY3':'punkC','n13flipY':'flip'}
for k,sp in P.items():
  J[k+'_walk']=dict(spec=sp,src='ext/c2_punk_walk.webp',cols=8,rows=4,cw=208,ch=272)
  J[k+'_run']=dict(spec=sp,src='ext/c2_punk_run.webp',cols=8,rows=4,cw=208,ch=272)
  J[k+'_hurt']=dict(spec=sp,src='ext/c2_punk_hurt.webp',cols=4,rows=4,cw=208,ch=272)
  J[k+'_kn']=dict(spec=sp,src='ext/c2_punk_kn.webp',cols=4,rows=4,cw=208,ch=272)
  J[k+'_map']=dict(spec=sp,src='ext/c2_punk_map.webp',cols=1,rows=1,faces=['front'])
  J[k+'_fig']=dict(spec=sp,src='ext/c2_punk_fig.webp',cols=1,rows=1,faces=['front'])
  J[k+'_fig_hurt']=dict(spec=sp,src='ext/c2_punk_fig_hurt.webp',cols=1,rows=1,faces=['front'])
  J[k+'_lie']=dict(spec=sp,src='ext/c2_punk_lie.webp',cols=2,rows=1,faces=['left'],rot=-1)
  J[k+'_fig_down']=dict(spec=sp,src='ext/c2_punk_fig_down.webp',cols=1,rows=1,faces=['right'],rot=1)
for sfx,src,c,r in [('walk','c2_punk_walk',8,4),('map','c2_punk_map',1,1)]:
  J['c2_gray_'+sfx]=dict(spec='gray',src='ext/'+src+'.webp',cols=c,rows=r,cw=208,ch=272) if c>1 else dict(spec='gray',src='ext/'+src+'.webp',cols=1,rows=1,faces=['front'])
for k,j in J.items():
  if k.startswith('of_') and any(k.endswith(s) for s in ['_amb','_ambv','_gym','_jog']): j['opts']={'coatMaxW':60}
json.dump(J,open('jobs.json','w'),indent=0); print(len(J))
