"""Functional checks of every calculator in a real browser against worked examples.

python3 tools/test_calcs.py    (needs a fresh build in dist/)
"""
import functools
import http.server
import sys
import threading
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "dist"


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


CASES = [
    # (page, {selector: value}, {radio name: value}, expected text inside .result-big, label)
    ("end-of-service", {"#eos-start": "2018-01-01", "#eos-end": "2024-01-01", "#eos-basic": "7000", "#eos-housing": "1500", "#eos-transport": "500", "#eos-other": "0"},
     {"eos-reason": "employer"}, "31,500.00", "6 years, 9,000 wage (Sabbar example)"),
    ("end-of-service", {"#eos-start": "2017-01-01", "#eos-end": "2024-01-01", "#eos-basic": "10000", "#eos-housing": "0", "#eos-transport": "0", "#eos-other": "0"},
     {"eos-reason": "resign", "eos-contract": "fixed"}, "30,000.00", "resign after 7 years (Qoyod example)"),
    ("end-of-service", {"#eos-start": "2019-01-01", "#eos-end": "2024-01-01", "#eos-basic": "10000", "#eos-housing": "0", "#eos-transport": "0", "#eos-other": "0"},
     {"eos-reason": "resign", "eos-contract": "fixed"}, "8,333.33", "resign at exactly 5 years gets one third"),
    ("end-of-service", {"#eos-start": "2023-01-01", "#eos-end": "2024-07-01", "#eos-basic": "10000", "#eos-housing": "0", "#eos-transport": "0", "#eos-other": "0"},
     {"eos-reason": "resign", "eos-contract": "fixed"}, "0.00", "resign under 2 years"),
    ("end-of-service", {"#eos-start": "2016-01-01", "#eos-end": "2024-01-01", "#eos-basic": "10000", "#eos-housing": "0", "#eos-transport": "0", "#eos-other": "0"},
     {"eos-reason": "employer"}, "55,000.00", "8 years at 10,000 (page example)"),
    ("end-of-service", {"#eos-start": "2016-01-01", "#eos-end": "2024-01-01", "#eos-basic": "10000", "#eos-housing": "0", "#eos-transport": "0", "#eos-other": "0"},
     {"eos-reason": "resign", "eos-contract": "fixed"}, "36,666.67", "resign after 8 years (page example)"),
    ("end-of-service", {"#eos-start": "2016-01-01", "#eos-end": "2024-01-01", "#eos-basic": "10000", "#eos-housing": "0", "#eos-transport": "0", "#eos-other": "0"},
     {"eos-reason": "art80"}, "0.00", "Article 80 dismissal"),
    ("end-of-service", {"#eos-start": "2016-01-01", "#eos-end": "2024-01-01", "#eos-basic": "9000", "#eos-housing": "0", "#eos-transport": "0", "#eos-other": "0", "#eos-leave": "10"},
     {"eos-reason": "employer"}, "49,500.00", "award stays 49,500 when leave days are added"),
    ("overtime", {"#ot-basic": "4000", "#ot-allow": "2000", "#ot-hours": "1", "#ot-daily": "8"}, {}, "33.33", "Qoyod overtime example"),
    ("overtime", {"#ot-basic": "6000", "#ot-allow": "1500", "#ot-hours": "1", "#ot-daily": "8"}, {}, "43.75", "page overtime example"),
    ("weighted-percentage", {"#w-gpa": "95", "#w-q": "80", "#w-t": "78"}, {}, "83.70", "30/30/40 example"),
    ("weighted-percentage", {"#w-preset": "30-30-30-10", "#w-gpa": "90", "#w-q": "80", "#w-t": "70", "#w-s": "60"}, {}, "78.00", "KAU 30/30/30/10 with STEP (27+24+21+6)"),
    ("vat", {"#vat-amount": "1000"}, {"vat-mode": "add"}, "150.00", "add VAT"),
    ("vat", {"#vat-amount": "1150"}, {"vat-mode": "extract"}, "150.00", "extract VAT"),
    ("date-converter", {"#cv-y": "2027", "#cv-m": "2", "#cv-d": "8"}, {}, "1 رمضان 1448هـ", "2027-02-08 is 1 Ramadan 1448"),
]

srv = http.server.ThreadingHTTPServer(("127.0.0.1", 8766), functools.partial(Handler, directory=str(SITE)))
threading.Thread(target=srv.serve_forever, daemon=True).start()
fails = 0
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    errors = []
    pg.on("pageerror", lambda e: errors.append(str(e)))
    for page, fields, radios, want, label in CASES:
        pg.goto(f"http://127.0.0.1:8766/mawed/{page}")
        for sel, v in fields.items():
            el = pg.locator(sel)
            if el.evaluate("e => e.tagName") == "SELECT":
                el.select_option(v)
            else:
                el.fill(v)
        for name, v in radios.items():
            pg.locator(f'input[name="{name}"][value="{v}"]').check()
        pg.locator("form").dispatch_event("input")
        got = pg.locator(".result-big").first.inner_text()
        ok = want in got
        fails += not ok
        print(("PASS" if ok else "FAIL"), label, "|", got.replace("\n", " "))
    # age: someone born 1 Jan 2000 is 26 on 19 Oct 2026 (the page uses today's Riyadh date)
    pg.goto("http://127.0.0.1:8766/mawed/age")
    pg.locator("#age-cal").select_option("g")
    pg.locator("#age-y").fill("2000"); pg.locator("#age-m").select_option("1"); pg.locator("#age-d").fill("1")
    pg.locator("#age-d").dispatch_event("input")
    print("INFO age for 2000-01-01:", pg.locator(".result-big").inner_text().replace("\n", " "))
    for e in errors:
        print("JS ERROR", e)
        fails += 1
    b.close()
srv.shutdown()
print("failures:", fails)
sys.exit(1 if fails else 0)
