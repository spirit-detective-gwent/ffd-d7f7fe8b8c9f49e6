"""Repaint the Lunch Line menu board in the baked cf_line room background to the v6.5.66 prices (Erik).
Same board and frame; the chalk is re-set in Liberation Sans, the face the original board was set in (fit: 15.2 px,
4x supersample, 1 px stroke at 4x, box-filtered down; mean error 11/255 vs the original line), same chalk + purple EAT."""
import sys
from PIL import Image, ImageDraw, ImageFont
src, out = sys.argv[1], sys.argv[2]
im = Image.open(src).convert('RGB')
FONT = '/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'
CHALK, PURPLE, GREEN = (212, 230, 214), (172, 152, 207), (58, 91, 71)
X0, Y0, X1, Y1 = 227, 29, 405, 95           # inside the board's dark frame
SS, SZ, CX = 4, 13.2, (232 + 399) / 2 + 0.75
lines = [('TODAY: MELON BREAD', CHALK, 35), ('MELON BREAD  \u00a57', CHALK, 50), ('HOT LUNCH  \u00a512', CHALK, 65), ('EAT.', PURPLE, 81)]
W, H = (X1 - X0 + 1) * SS, (Y1 - Y0 + 1) * SS
pan = Image.new('RGB', (W, H), GREEN); g = ImageDraw.Draw(pan); f = ImageFont.truetype(FONT, SZ * SS); cap = f.getbbox('T')
for t, col, capy in lines:
    b = f.getbbox(t)
    g.text(((CX - X0) * SS - (b[2] - b[0]) / 2, (capy - 0.25 - Y0) * SS - cap[1]), t, font=f, fill=col, stroke_width=1, stroke_fill=col)
im.paste(pan.resize((X1 - X0 + 1, Y1 - Y0 + 1), Image.BOX), (X0, Y0))
im.save(out)
