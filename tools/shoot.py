"""Screenshot built production pages at phone and desktop widths, light and dark.

python3 tools/shoot.py OUT_DIR slug1 slug2 ...   (slug "index" for the home page)
Serves dist/ on localhost the way Cloudflare Pages does (extensionless URLs).
"""
import functools
import http.server
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dist"
OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)
slugs = sys.argv[2:]


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path.startswith("/mawed"):
            path = path[len("/mawed"):] or "/"
        p = super().translate_path(path)
        if not Path(p).suffix and Path(p + ".html").exists():
            return p + ".html"
        return p

    def log_message(self, *a):
        pass


srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8765), functools.partial(Handler, directory=str(SITE)))
threading.Thread(target=srv.serve_forever, daemon=True).start()

with sync_playwright() as pw:
    b = pw.chromium.launch()
    for scheme in ("light", "dark"):
        for w, h in ((390, 1600), (1280, 1000)):
            ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme)
            pg = ctx.new_page()
            errors = []
            pg.on("pageerror", lambda e: errors.append(str(e)))
            pg.on("console", lambda m: errors.append(m.text) if m.type == "error" else None)
            for s in slugs:
                pg.goto(f"http://127.0.0.1:8765/mawed/{'' if s == 'index' else s}")
                pg.wait_for_timeout(1400)
                pg.screenshot(path=str(OUT / f"{s}-{w}-{scheme}.png"), full_page=(w == 390))
                sw = pg.evaluate("document.documentElement.scrollWidth")
                if sw > w:
                    print(f"OVERFLOW {s} {w}px: scrollWidth={sw}")
            for e in errors:
                print("CONSOLE", scheme, w, e)
            ctx.close()
    b.close()
srv.shutdown()
print("done")
