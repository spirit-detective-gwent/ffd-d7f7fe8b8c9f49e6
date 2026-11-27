"""Ch2 Kampo supply sim (v6564-healstyle). One 'cycle' = one Ch2 quest turned in (pots bloom, shops restock).
Sources after the lesson:
  mugwort: 9 top pots, seeds from Tsukikage 3 packets x3 per cycle (Y1 each); garden x2 6% / x3 1%
  ginger : 6 bottom pots, Ono ginger seed 1/buy, stock 6 per cycle (Y3, Y2 after Nails)
           wild ginger: 9 dock sprigs, regrow only on a seal (4 seals in Ch2) -> picked once per seal step
           foe drops: 4%/foe, 70% ginger 30% leaf; garden rare 0.5%/pick -> half the time ginger
  quest reward (HS_QREW): leaf+ginger per quest turned in
Each Kampo = 1 leaf + 1 ginger. Cap 5 carried.
Assumed play: CYC_MIN minutes per quest cycle, FOES foes beaten per cycle, player replants every cycle
(lazy player: plants only P_PLANT of the time), buys ginger seed if yen allows.
"""
import random, statistics as st, sys
def run(cycles=12, CYC_MIN=9, FOES=6, P_PLANT=1.0, QREW=(1,1), seals_at=(2,5,8,11), buy_gseed=6, seed=0, NEED=4):
    R=random.Random(seed); leaf=ginger=0; made=0; yen_spent=0; carry=0; short=0
    gpots=0; mpots=0; wild_mark=-1
    for c in range(cycles):
        s=sum(1 for x in seals_at if x<=c)
        if s!=wild_mark: ginger+=9; wild_mark=s           # walk the docks once after each seal
        # harvest what bloomed (planted last cycle)
        def mult():
            r=R.random(); return 3 if r<.01 else 2 if r<.07 else 1
        leaf+=sum(mult() for _ in range(mpots)); ginger+=sum(mult() for _ in range(gpots))
        for _ in range(mpots+gpots):
            if R.random()<.005 and R.random()>=.5: ginger+=1
        mpots=gpots=0
        if R.random()<P_PLANT: mpots=9; yen_spent+=3
        if R.random()<P_PLANT and buy_gseed: gpots=min(6,buy_gseed); yen_spent+=2*gpots
        for _ in range(FOES):
            if R.random()<.04:
                if R.random()<.7: ginger+=1
                else: leaf+=1
        leaf+=QREW[0]; ginger+=QREW[1]
        k=min(leaf,ginger,5-carry); made+=k; leaf-=k; ginger-=k; carry+=k   # brew at the bowl up to the cap
        use=min(carry,NEED); short+= NEED-use; carry-=use                     # drink NEED per cycle
    hours=cycles*CYC_MIN/60
    return made, made/hours, yen_spent, short/cycles
for label,kw in [('engaged (plants every cycle, buys 6 ginger seed)',{}),
                 ('lazy (plants half the cycles)',{'P_PLANT':.5}),
                 ('no garden at all (wild + drops + quest only)',{'P_PLANT':0}),
                 ('no garden, no quest herbs',{'P_PLANT':0,'QREW':(0,0)}),
                 ('engaged, slow player 14 min/cycle',{'CYC_MIN':14})]:
    rs=[run(seed=i,**kw) for i in range(400)]
    print(f"{label:52s} kampo/12 cycles {st.mean(r[0] for r in rs):5.1f}  per hour {st.mean(r[1] for r in rs):5.1f}  yen {st.mean(r[2] for r in rs):4.0f}  short/cycle {st.mean(r[3] for r in rs):.2f}")
