"""All site content and date rules. Rendered by tools/build.py."""
import json
import warnings
from datetime import date, timedelta
from pathlib import Path

warnings.filterwarnings("ignore")
from hijri_converter import convert  # noqa: E402

import static_pages  # noqa: E402
import programs  # noqa: E402
import calcs  # noqa: E402

REVIEWED_TEXT = "أكتوبر 2026"
ADSENSE_CLIENT = None  # set to "ca-pub-..." once AdSense approves the site

GM = ['يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو', 'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر']
HM = ['محرم', 'صفر', 'ربيع الأول', 'ربيع الآخر', 'جمادى الأولى', 'جمادى الآخرة', 'رجب', 'شعبان', 'رمضان', 'شوال', 'ذو القعدة', 'ذو الحجة']
WD = ['الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 'الجمعة', 'السبت', 'الأحد']  # Python weekday() order


def hijri(d):
    h = convert.Gregorian(d.year, d.month, d.day).to_hijri()
    return (h.year, h.month, h.day)


def from_hijri(y, m, d):
    g = convert.Hijri(y, m, d).to_gregorian()
    return date(g.year, g.month, g.day)


def gtext(d):
    return f"{d.day} {GM[d.month - 1]} {d.year}"


def htext(d):
    h = hijri(d)
    return f"{h[2]} {HM[h[1] - 1]} {h[0]}هـ"


def wday(d):
    return WD[d.weekday()]


def days_word(n):
    if n in (1, 2):
        return "يوم"
    if 3 <= n <= 10:
        return "أيام"
    return "يومًا"


def info(d, today, name=None):
    left = (d - today).days
    h = hijri(d)
    return {
        "iso": d.isoformat(), "left": left if left else "0", "unit": days_word(left) if left else "موعده اليوم",
        "weekday": wday(d), "gtext": gtext(d), "htext": htext(d),
        "gmonth": f"{GM[d.month - 1]} {d.year}", "hmonth": f"{HM[h[1] - 1]} {h[0]}",
        "gmonth_short": GM[d.month - 1], "day": d.day, "name": name,
    }


def next_date(dates, today):
    for item in dates:
        if item["date"] >= today:
            return item
    return None


def build_pages(today):
    ctx = {"today": today, "hijri": hijri, "from_hijri": from_hijri, "gtext": gtext, "htext": htext,
           "wday": wday, "info": info, "next_date": next_date, "days_word": days_word, "GM": GM, "HM": HM}
    countdowns = programs.build(ctx)       # list of countdown page dicts (with 'dates')
    tools = calcs.build(ctx)               # list of calculator page dicts
    link = _link_stub

    # Home
    items = []
    for c in countdowns:
        if not c.get("on_home", True):
            continue
        nd = next_date(c["dates"], today)
        if nd:
            i = info(nd["date"], today, c["short"])
            i["slug"] = c["slug"]
            items.append(i)
    items.sort(key=lambda i: int(i["left"]))
    home_data = {"items": [{"name": c["short"], "href": "@@" + c["slug"],
                            "dates": [{"date": x["date"].isoformat()} for x in c["dates"]]}
                           for c in countdowns if c.get("on_home", True)]}
    home = {
        "slug": "index", "template": "home.html", "section": None,
        "title": "موعد: كم باقي على الراتب ورمضان والعيد في السعودية",
        "description": "كم باقي على الراتب وحساب المواطن والضمان والتقاعد ورمضان والعيد، بتوقيت الرياض ومن المصادر الرسمية. وحاسبات نهاية الخدمة والنسبة الموزونة والعمر بالهجري.",
        "home": {
            "first": items[0], "rows": items,
            "tools": [{"slug": t["slug"], "name": t["p"]["crumb"], "desc": t["home_desc"]} for t in tools],
            "data_json": json.dumps(home_data, ensure_ascii=False),
        },
        "jsonld": json.dumps({
            "@context": "https://schema.org", "@type": "WebSite", "name": "موعد", "url": "https://mawedsa.com/",
            "inLanguage": "ar-SA"}, ensure_ascii=False),
    }
    pages = [home] + [c["page"] for c in countdowns] + tools + [
        static_pages.about(link), static_pages.contact(link), static_pages.privacy(link),
        static_pages.terms(link), static_pages.not_found(link)]
    return pages


def _link_stub(slug):
    # Static pages are written before the Site object exists; the build swaps @@slug for the real link.
    return "@@" + slug


def static_files(origin, pages):
    urls = [p for p in pages if p["slug"] not in ("404",)]
    from datetime import datetime
    from zoneinfo import ZoneInfo
    today = datetime.now(ZoneInfo("Asia/Riyadh")).date().isoformat()
    sm = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in urls:
        loc = origin + ("/" if p["slug"] == "index" else "/" + p["slug"])
        sm.append(f"  <url><loc>{loc}</loc><lastmod>{today}</lastmod></url>")
    sm.append("</urlset>")
    files = {
        "sitemap.xml": "\n".join(sm) + "\n",
        "robots.txt": f"User-agent: *\nAllow: /\n\nSitemap: {origin}/sitemap.xml\n",
        "favicon.svg": (
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect x="3" y="5" width="26" height="24" rx="5" '
            'fill="#fff" stroke="#D9DEE8"/><path d="M3 10a5 5 0 0 1 5-5h16a5 5 0 0 1 5 5v2H3z" fill="#C8102E"/>'
            '<circle cx="11" cy="8.5" r="1.4" fill="#F2F4F8"/><circle cx="21" cy="8.5" r="1.4" fill="#F2F4F8"/>'
            '<text x="16" y="25" text-anchor="middle" font-family="Tahoma,sans-serif" font-weight="700" font-size="11" '
            'fill="#18203A">27</text></svg>\n'),
        "_headers": (
            "/*\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n"
            "  Permissions-Policy: camera=(), microphone=(), geolocation=()\n\n"
            "/assets/*\n  Cache-Control: public, max-age=604800\n\n"
            "/assets/fonts/*\n  Cache-Control: public, max-age=31536000, immutable\n"),
    }
    if ADSENSE_CLIENT:
        files["ads.txt"] = f"google.com, {ADSENSE_CLIENT.replace('ca-', '')}, DIRECT, f08c47fec0942fa0\n"
    return files
