"""Build the موعد site.

python3 tools/build.py            -> dist/ (production) and preview/ (artifact preview)
Content and rules live in src/content.py; this file only renders.
"""
import json
import re
import shutil
import sys
import warnings
from datetime import date, datetime
from zoneinfo import ZoneInfo
from pathlib import Path

warnings.filterwarnings("ignore")
from jinja2 import Environment, FileSystemLoader, select_autoescape  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))
import content  # noqa: E402

# Where the site lives. Free GitHub Pages address for now; when a custom domain is bought,
# set HOST to "https://<domain>" and BASE to "" (the build and all links follow).
HOST = "https://egltsa26-eng.github.io"
BASE = "/mawed"
ORIGIN = HOST + BASE
UQ_JSON = (SRC / "data" / "ummalqura.json").read_text()
CSS = (SRC / "assets" / "site.css").read_text()
JS = (SRC / "assets" / "site.js").read_text()

FONT_FILES = [
    ("Readex Pro", 400, "readex-pro", "arabic"), ("Readex Pro", 400, "readex-pro", "latin"),
    ("Readex Pro", 500, "readex-pro", "arabic"), ("Readex Pro", 500, "readex-pro", "latin"),
    ("Readex Pro", 600, "readex-pro", "arabic"), ("Readex Pro", 600, "readex-pro", "latin"),
    ("Readex Pro", 700, "readex-pro", "arabic"), ("Readex Pro", 700, "readex-pro", "latin"),
    ("Noto Naskh Arabic", 400, "noto-naskh-arabic", "arabic"), ("Noto Naskh Arabic", 400, "noto-naskh-arabic", "latin"),
    ("Noto Naskh Arabic", 600, "noto-naskh-arabic", "arabic"), ("Noto Naskh Arabic", 600, "noto-naskh-arabic", "latin"),
]
UNICODE = {
    "arabic": "U+0600-06FF, U+0750-077F, U+0870-088E, U+0890-0891, U+0897-08E1, U+08E3-08FF, U+200C-200E, U+2010-2011, U+204F, U+2E41, U+FB50-FDFF, U+FE70-FE74, U+FE76-FEFC, U+102E0-102FB, U+10E60-10E7E, U+10EC2-10EC4, U+10EFC-10EFF, U+1EE00-1EEF1",
    "latin": "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD",
}

AD_LABEL = "مساحة إعلان"


class Site:
    def __init__(self, mode):
        self.mode = mode
        self.production = mode == "production"
        self.fragment = False
        self.inline_css = not self.production
        self.inline_js = not self.production
        self.css = CSS
        self.js = JS
        self.origin = HOST
        self.base = BASE if self.production else ""
        self.root = ORIGIN
        self.uq_json = UQ_JSON
        self.reviewed = content.REVIEWED_TEXT
        self.adsense_client = content.ADSENSE_CLIENT

    def link(self, slug):
        if self.production:
            return BASE + ("/" if slug == "index" else "/" + slug)
        return ("home" if slug == "index" else slug) + ".html"

    def asset(self, name):
        return BASE + "/assets/" + name if self.production else "assets/" + name

    def ad(self, where):
        if self.production:
            if not self.adsense_client:
                return ""
            return ('<div class="ad-slot"><ins class="adsbygoogle" style="display:block" data-ad-client="%s" '
                    'data-ad-format="auto" data-full-width-responsive="true"></ins>'
                    '<script>(adsbygoogle=window.adsbygoogle||[]).push({});</script></div>') % self.adsense_client
        return '<div class="ad-slot preview" aria-hidden="true">%s</div>' % AD_LABEL


def riyadh_today():
    return datetime.now(ZoneInfo("Asia/Riyadh")).date()


def fix_links(html, site):
    return re.sub(r"@@([a-z0-9-]+)", lambda m: site.link(m.group(1)), html)


def render_all(mode, out_dir):
    env = Environment(loader=FileSystemLoader(str(SRC / "templates")), autoescape=select_autoescape(["html"]))
    site = Site(mode)
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True)
    pages = content.build_pages(riyadh_today(), ORIGIN)
    for pg in pages:
        tpl = env.get_template(pg["template"])
        page = {
            "title": pg["title"], "description": pg["description"], "path": site.link(pg["slug"]) if site.production else "",
            "section": pg.get("section"), "jsonld": pg.get("jsonld"), "og_title": pg.get("og_title"),
        }
        html = fix_links(tpl.render(site=site, page=page, p=pg.get("p", {}), home=pg.get("home")), site)
        name = ("index" if pg["slug"] == "index" else pg["slug"]) + ".html" if site.production else site.link(pg["slug"])
        (out_dir / name).write_text(html)
        if not site.production and pg["slug"] == "index":
            # The artifact's main page is wrapped by the viewer, so it gets a fragment version.
            site.fragment = True
            page = dict(page, title="موقع موعد")
            (out_dir / "_main.html").write_text(fix_links(tpl.render(site=site, page=page, p=pg.get("p", {}), home=pg.get("home")), site))
            site.fragment = False
    if site.production:
        assets = out_dir / "assets"
        (assets / "fonts").mkdir(parents=True)
        (assets / "site.css").write_text(CSS)
        (assets / "site.js").write_text(JS)
        faces = []
        for fam, w, pkg, sub in FONT_FILES:
            fn = f"{pkg}-{sub}-{w}-normal.woff2"
            shutil.copy(ROOT / "node_modules" / "@fontsource" / pkg / "files" / fn, assets / "fonts" / fn)
            faces.append(
                f"@font-face{{font-family:'{fam}';font-style:normal;font-weight:{w};font-display:swap;"
                f"src:url(fonts/{fn}) format('woff2');unicode-range:{UNICODE[sub]}}}")
        (assets / "fonts.css").write_text("\n".join(faces) + "\n")
        for name, text in content.static_files(ORIGIN, pages).items():
            (out_dir / name).write_text(text)
    return pages


if __name__ == "__main__":
    pages = render_all("production", ROOT / "dist")
    render_all("preview", ROOT / "preview")
    print(f"built {len(pages)} pages")
