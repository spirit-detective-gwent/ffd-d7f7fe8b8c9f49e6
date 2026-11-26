# figpose.py fig.webp out_hurt.webp out_down.webp : battle hurt / down stills for a rig with no drawn ones (Club Hostess on the Hina rig),
# made from the painted stand figure: hurt = rocked back on the heels, down = laid out on the floor (head left, like the punk fig_down)
import sys
from PIL import Image
f = Image.open(sys.argv[1]).convert('RGBA'); W, H = f.size
hurt = Image.new('RGBA', (W, H)); r = f.rotate(8, resample=Image.BICUBIC, center=(W * 0.5, H - 4), translate=(-5, 0)); hurt.alpha_composite(r); hurt.save(sys.argv[2], 'WEBP', lossless=True)
bb = f.getbbox(); fig = f.crop(bb).rotate(90, expand=True, resample=Image.BICUBIC)  # head to the left
down = Image.new('RGBA', (248, 224)); s = min(1.0, 236 / fig.width); fig = fig.resize((int(fig.width * s), int(fig.height * s)), Image.LANCZOS)
down.alpha_composite(fig, ((248 - fig.width) // 2, 224 - fig.height - 6)); down.save(sys.argv[3], 'WEBP', lossless=True)
