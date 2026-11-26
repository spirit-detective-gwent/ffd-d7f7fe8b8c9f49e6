from sheets import *
import sys
REF=[(WD+'c2_punkY1_walk.webp',WD+'c2_punkY1_fig.webp','Punk A (live)'),(WD+'c2_punkY2_walk.webp',WD+'c2_punkY2_fig.webp','Punk B (live)'),(WD+'c2_punkY3_walk.webp',WD+'c2_punkY3_fig.webp','Punk C (live)'),
     (WD+'n13flipY_walk.webp',WD+'n13flipY_fig.webp','Flip (live)'),(WD+'c2_hustlerY_walk.webp',WD+'c2_hustlerY_fig.webp','Bath boy (live)'),(WD+'c2_doormanY_walk.webp',WD+'c2_doormanY_fig.webp','Kaneda (live)'),(WD+'mb2_sentoY_walk.webp',WD+'mb2_sentoY_fig.webp','Goda (live)')]
def B(s,l): return ('baked/%s_walk.webp'%s,'baked/%s_fig.webp'%s,l)
which=sys.argv[1] if len(sys.argv)>1 else 'k'
if 'k' in which: lineup('kitsune_lineup.png','Club Kitsune + Sabu, next to the existing cel pass',[B('ksJin','High-Score Jin (boss)'),B('ksBouncer','Black-Suit Bouncer (lt.)'),B('ksSuit','Kitsune Suit (uniform A)'),B('ksRun','Kitsune Runner (uniform B)'),B('sabu','Sabu (Punk crew)')],REF)
if 'd' in which: lineup('depot_lineup.png','The Depot, next to the existing cel pass',[B('dpMasa','Foreman Masa (boss)'),B('dpRider','Depot Rider (uniform A)'),B('dpDock','Dock hand (uniform B)')],REF)
