#!/workspace/pwenv/bin/python3
"""Render tools/s2/preview_menus.html canvases into /workspace/v6560-review/shopmenus/preview/."""
import asyncio, http.server, socketserver, threading, functools, base64, io, os
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image

HERE = Path(__file__).resolve().parent
OUT = Path('/workspace/v6560-review/shopmenus/preview')
PORT = int(os.environ.get('PORT', '8873'))
OUT.mkdir(parents=True, exist_ok=True)

class Q(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *a): pass
class TS(socketserver.ThreadingTCPServer):
    allow_reuse_address = True
    daemon_threads = True

async def main():
    s = TS(('127.0.0.1', PORT), functools.partial(Q, directory=str(HERE)))
    threading.Thread(target=s.serve_forever, daemon=True).start()
    async with async_playwright() as p:
        b = await p.chromium.launch(args=['--use-gl=swiftshader', '--enable-unsafe-swiftshader'])
        ctx = await b.new_context(viewport={'width': 1800, 'height': 3200}, device_scale_factor=1)
        pg = await ctx.new_page()
        await pg.goto(f'http://127.0.0.1:{PORT}/preview_menus.html')
        await pg.wait_for_function('() => window.__s2menus_ready === true', timeout=20000)
        await pg.wait_for_timeout(400)
        ids = await pg.evaluate("()=>[...document.querySelectorAll('canvas')].map(c=>c.id)")
        print('canvases', ids)
        for cid in ids:
            data = await pg.evaluate("""(id)=>{
              var c=document.getElementById(id); return c.toDataURL('image/png');
            }""", cid)
            raw = data.split(',', 1)[1]
            im = Image.open(io.BytesIO(base64.b64decode(raw))).convert('RGB')
            im.save(OUT / f'{cid}.png')
            print('saved', cid, im.size)
        await b.close()
    s.server_close()

if __name__ == '__main__':
    asyncio.run(main())
