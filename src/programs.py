"""Countdown pages: payments, Hijri occasions, national days."""
import json
from datetime import date, timedelta

import payments  # noqa: E402  (payment rules researched from official sources)
import occasions  # noqa: E402

RELATED_ALL = [
    ("salary", "موعد الراتب"), ("citizen-account", "حساب المواطن"), ("social-security", "الضمان الاجتماعي"),
    ("pension", "رواتب التقاعد"), ("ramadan", "رمضان"), ("eid-al-fitr", "عيد الفطر"), ("eid-al-adha", "عيد الأضحى"),
    ("school-holidays", "الإجازة الدراسية"), ("end-of-service", "حاسبة نهاية الخدمة"), ("date-converter", "تحويل التاريخ"),
]


def related_for(slug, extra=None):
    out = [r for r in RELATED_ALL if r[0] != slug]
    if extra:
        out = extra + [r for r in out if r[0] not in {e[0] for e in extra}]
    return out[:7]


def countdown(ctx, *, slug, short, title, description, h1, crumb, answer_tpl, dates, facts, sources,
              table_title, table_head=None, body=(), faq=(), note=None, table_note=None, kicker=None,
              on_home=True, related=None, jsonld_extra=None):
    today = ctx["today"]
    past = [d for d in dates if d["date"] < today]
    upcoming = past[-1:] + [d for d in dates if d["date"] >= today][:12]
    nd = ctx["next_date"](dates, today)
    nxt = ctx["info"](nd["date"], today) if nd else None
    left_txt = ("اليوم" if nxt and nxt["left"] == "0" else f"باقي {nxt['left']} {nxt['unit']}") if nxt else ""
    answer_static = (answer_tpl.replace("{label}", nd.get("label", "")).replace("{weekday}", nxt["weekday"])
                     .replace("{date}", nxt["gtext"]).replace("{hijri}", nxt["htext"]).replace("{left}", left_txt)) if nxt else ""
    rows = []
    for d in upcoming:
        rows.append({"iso": d["date"].isoformat(), "label": d.get("label", ""), "weekday": ctx["wday"](d["date"]),
                     "gtext": ctx["gtext"](d["date"]), "htext": ctx["htext"](d["date"]), "moved": d.get("moved"), "note": d.get("note")})
    data = {"dates": [{"date": d["date"].isoformat(), "label": d.get("label", "")} for d in dates], "kicker": kicker or "باقي"}
    faq = list(faq)
    page = {
        "slug": slug, "template": "countdown.html", "section": "dates", "title": title, "description": description,
        "p": {
            "crumb": crumb, "h1": h1, "answer_tpl": answer_tpl, "answer_static": answer_static, "kicker": kicker or "باقي",
            "next": nxt, "facts": facts(nd) if callable(facts) else facts, "note": note, "sources": sources,
            "table_title": table_title, "table_head": table_head or ["الشهر", "التاريخ", "بالهجري", "ملاحظة"],
            "rows": rows, "has_notes": any(r["moved"] or r["note"] for r in rows), "table_note": table_note, "body": list(body), "faq": faq,
            "related": related or related_for(slug), "data_json": json.dumps(data, ensure_ascii=False),
        },
    }
    ld = {"@context": "https://schema.org", "@type": "WebPage", "name": title, "inLanguage": "ar-SA",
          "description": description}
    if jsonld_extra:
        ld.update(jsonld_extra)
    page["jsonld"] = json.dumps(ld, ensure_ascii=False)
    return {"slug": slug, "short": short, "on_home": on_home, "dates": dates, "page": page}


UQ_SOURCE = {"name": "سعوديبيديا: تقويم أم القرى", "url": "https://saudipedia.com/%D8%AA%D9%82%D9%88%D9%8A%D9%85-%D8%A3%D9%85-%D8%A7%D9%84%D9%82%D8%B1%D9%89"}


def hijri_pages(ctx):
    fh, hj = ctx["from_hijri"], ctx["hijri"]
    today = ctx["today"]
    th = hj(today)
    years = range(th[0] - 1, th[0] + 6)
    out = []

    # Ramadan
    ram = [{"date": fh(y, 9, 1), "label": f"رمضان {y}"} for y in years]
    ram = [r for r in ram if r["date"] >= date(2025, 1, 1)]
    nr = ctx["next_date"](ram, today)
    ny = hj(nr["date"])[0] if nr else th[0]
    ram_len = (fh(ny, 10, 1) - fh(ny, 9, 1)).days
    out.append(countdown(
        ctx, slug="ramadan", short="رمضان", crumb="كم باقي على رمضان",
        title=f"كم باقي على رمضان {ny}؟ العد التنازلي بتوقيت الرياض",
        description=f"كم باقي على رمضان {ny}: موعد أول أيام رمضان حسب تقويم أم القرى بالهجري والميلادي، مع عد تنازلي بالأيام والساعات وجدول السنوات القادمة.",
        h1=f"كم باقي على رمضان {ny}؟",
        answer_tpl="يبدأ {label} حسب تقويم أم القرى يوم {weekday} {date}، {left}.",
        dates=ram,
        facts=[("أول أيام رمضان", f"{ctx['wday'](fh(ny, 9, 1))} {ctx['gtext'](fh(ny, 9, 1))}"),
               ("ليلة تحري الهلال", f"مساء {ctx['wday'](fh(ny, 8, 29))} {ctx['gtext'](fh(ny, 8, 29))} (29 شعبان)"),
               ("عدد أيامه في التقويم", f"{ram_len} يومًا"),
               ("عيد الفطر حسب التقويم", f"{ctx['wday'](fh(ny, 10, 1))} {ctx['gtext'](fh(ny, 10, 1))}")],
        note="التاريخ حسب تقويم أم القرى. يُعلن دخول الشهر رسميًا بعد تحري الهلال مساء 29 شعبان، فقد يتأخر يومًا عن التقويم.",
        sources=[UQ_SOURCE],
        table_title="بداية رمضان في السنوات القادمة",
        table_head=["الشهر", "أول أيامه", "بالهجري", "ملاحظة"],
        body=[
            "<h2>كيف يُحدد أول أيام رمضان؟</h2>",
            "<p>في المملكة تدعو المحكمة العليا إلى تحري هلال رمضان مساء يوم 29 شعبان. إذا ثبتت الرؤية يكون اليوم التالي أول أيام رمضان، وإن لم تثبت يكمل شعبان ثلاثين يومًا. لذلك نعرض التاريخ حسب تقويم أم القرى، ونحدّث الصفحة فور الإعلان الرسمي.</p>",
            "<h2>رمضان يتقدم كل سنة</h2>",
            "<p>السنة الهجرية أقصر من الميلادية بنحو 11 يومًا، فيأتي رمضان كل سنة قبل موعده في السنة السابقة بنحو 11 يومًا. لهذا يمر رمضان على كل فصول السنة خلال 33 سنة تقريبًا.</p>",
        ],
        faq=[
            ("متى يتحرى الناس هلال رمضان؟", f"مساء يوم 29 شعبان، ويوافق في {ny} مساء {ctx['wday'](fh(ny, 8, 29))} {ctx['gtext'](fh(ny, 8, 29))} حسب تقويم أم القرى."),
            ("هل ممكن يتغير الموعد؟", "نعم بيوم واحد. الإعلان الرسمي يعتمد على رؤية الهلال، والتقويم تقدير فلكي معتمد للتخطيط."),
            ("كم يوم رمضان هذه السنة؟", f"في تقويم أم القرى {ram_len} يومًا، والعدد الفعلي يُحسم برؤية هلال شوال."),
            ("متى عيد الفطر؟", "اطلع على <a href=\"@@eid-al-fitr\">كم باقي على عيد الفطر</a>."),
        ],
        related=related_for("ramadan", [("eid-al-fitr", "عيد الفطر"), ("eid-al-adha", "عيد الأضحى"), ("date-converter", "تحويل التاريخ")]),
    ))

    # Eid al-Fitr
    fitr = [{"date": fh(y, 10, 1), "label": f"عيد الفطر {y}"} for y in years]
    fitr = [r for r in fitr if r["date"] >= date(2025, 1, 1)]
    nf = ctx["next_date"](fitr, today)
    fy = hj(nf["date"])[0] if nf else th[0]
    out.append(countdown(
        ctx, slug="eid-al-fitr", short="عيد الفطر", crumb="كم باقي على عيد الفطر",
        title=f"كم باقي على عيد الفطر {fy}؟ موعد العيد وإجازته",
        description=f"كم باقي على عيد الفطر {fy}: موعد أول أيام العيد حسب تقويم أم القرى بالهجري والميلادي، مع عد تنازلي وجدول السنوات القادمة.",
        h1=f"كم باقي على عيد الفطر {fy}؟",
        answer_tpl="أول أيام {label} حسب تقويم أم القرى يوم {weekday} {date}، {left}.",
        dates=fitr,
        facts=[("أول أيام العيد", f"{ctx['wday'](fh(fy, 10, 1))} {ctx['gtext'](fh(fy, 10, 1))}"),
               ("ليلة تحري هلال شوال", f"مساء {ctx['wday'](fh(fy, 9, 29))} {ctx['gtext'](fh(fy, 9, 29))} (29 رمضان)"),
               ("بالهجري", f"1 شوال {fy}هـ")],
        note="يُعلن العيد رسميًا بعد تحري هلال شوال مساء 29 رمضان، فقد يتأخر يومًا عن التقويم.",
        sources=[UQ_SOURCE] + occasions.eid_fitr(ctx, fy)[2],
        table_title="عيد الفطر في السنوات القادمة",
        table_head=["العيد", "أول أيامه", "بالهجري", "ملاحظة"],
        body=occasions.eid_fitr(ctx, fy)[0],
        faq=occasions.eid_fitr(ctx, fy)[1],
        related=related_for("eid-al-fitr", [("ramadan", "رمضان"), ("eid-al-adha", "عيد الأضحى")]),
    ))

    # Eid al-Adha
    adha = [{"date": fh(y, 12, 10), "label": f"عيد الأضحى {y}"} for y in years]
    adha = [r for r in adha if r["date"] >= date(2025, 1, 1)]
    na = ctx["next_date"](adha, today)
    ay = hj(na["date"])[0] if na else th[0]
    out.append(countdown(
        ctx, slug="eid-al-adha", short="عيد الأضحى", crumb="كم باقي على عيد الأضحى",
        title=f"كم باقي على عيد الأضحى {ay}؟ موعد يوم عرفة والعيد",
        description=f"كم باقي على عيد الأضحى {ay}: موعد يوم عرفة وأول أيام العيد حسب تقويم أم القرى بالهجري والميلادي، مع عد تنازلي.",
        h1=f"كم باقي على عيد الأضحى {ay}؟",
        answer_tpl="أول أيام {label} حسب تقويم أم القرى يوم {weekday} {date}، {left}.",
        dates=adha,
        facts=[("يوم عرفة", f"{ctx['wday'](fh(ay, 12, 9))} {ctx['gtext'](fh(ay, 12, 9))}"),
               ("أول أيام العيد", f"{ctx['wday'](fh(ay, 12, 10))} {ctx['gtext'](fh(ay, 12, 10))}"),
               ("أيام التشريق", f"من {ctx['gtext'](fh(ay, 12, 11))} إلى {ctx['gtext'](fh(ay, 12, 13))}")],
        note="يُحدد أول ذي الحجة بعد تحري الهلال مساء 29 ذي القعدة، فقد يختلف يوم عرفة والعيد بيوم عن التقويم.",
        sources=[UQ_SOURCE] + occasions.eid_adha(ctx, ay)[2],
        table_title="عيد الأضحى في السنوات القادمة",
        table_head=["العيد", "أول أيامه", "بالهجري", "ملاحظة"],
        body=occasions.eid_adha(ctx, ay)[0],
        faq=occasions.eid_adha(ctx, ay)[1],
        related=related_for("eid-al-adha", [("eid-al-fitr", "عيد الفطر"), ("ramadan", "رمضان")]),
    ))
    return out


def national_pages(ctx):
    today = ctx["today"]
    out = []
    nat = [{"date": date(y, 9, 23), "label": f"اليوم الوطني {y - 1932}"} for y in range(today.year - 1, today.year + 5)]
    nn = ctx["next_date"](nat, today)
    out.append(countdown(
        ctx, slug="national-day", short="اليوم الوطني", crumb="كم باقي على اليوم الوطني",
        title=f"كم باقي على اليوم الوطني {nn['date'].year - 1932}؟",
        description="كم باقي على اليوم الوطني السعودي، الموافق 23 سبتمبر من كل عام، مع عد تنازلي وموافقه بالهجري.",
        h1=f"كم باقي على اليوم الوطني {nn['date'].year - 1932}؟",
        answer_tpl="{label} يوم {weekday} {date}، {left}.",
        dates=nat,
        facts=[("التاريخ الثابت", "23 سبتمبر من كل عام"), ("المناسبة", "ذكرى توحيد المملكة عام 1932م")],
        sources=occasions.NATIONAL_SOURCES,
        table_title="اليوم الوطني في السنوات القادمة",
        table_head=["المناسبة", "التاريخ", "بالهجري", "ملاحظة"],
        body=occasions.NATIONAL_BODY,
        related=related_for("national-day", [("founding-day", "يوم التأسيس")]),
    ))
    fd = [{"date": date(y, 2, 22), "label": f"يوم التأسيس {y}"} for y in range(today.year - 1, today.year + 5)]
    out.append(countdown(
        ctx, slug="founding-day", short="يوم التأسيس", crumb="كم باقي على يوم التأسيس",
        title="كم باقي على يوم التأسيس؟ 22 فبراير",
        description="كم باقي على يوم التأسيس السعودي، الموافق 22 فبراير من كل عام، مع عد تنازلي وموافقه بالهجري.",
        h1="كم باقي على يوم التأسيس؟",
        answer_tpl="{label} يوم {weekday} {date}، {left}.",
        dates=fd,
        facts=[("التاريخ الثابت", "22 فبراير من كل عام"), ("المناسبة", "ذكرى تأسيس الدولة السعودية الأولى عام 1727م")],
        sources=occasions.FOUNDING_SOURCES,
        table_title="يوم التأسيس في السنوات القادمة",
        table_head=["المناسبة", "التاريخ", "بالهجري", "ملاحظة"],
        body=occasions.FOUNDING_BODY,
        related=related_for("founding-day", [("national-day", "اليوم الوطني")]),
    ))
    return out


def school_page(ctx):
    today, gt, wd = ctx["today"], ctx["gtext"], ctx["wday"]
    dates = []
    for label, a, b in occasions.SCHOOL_BREAKS:
        note = f"حتى {wd(b)} {gt(b)}" if b else "آخر يوم دراسي الخميس 24 يونيو 2027"
        dates.append({"date": a, "label": label, "note": note, "end": b})
    nd = ctx["next_date"](dates, today)
    facts = [("الإجازة القادمة", nd["label"]), ("أول يوم إجازة", f"{wd(nd['date'])} {gt(nd['date'])}")]
    if nd["end"]:
        back = nd["end"] + timedelta(days=1)
        facts += [("آخر يوم إجازة", f"{wd(nd['end'])} {gt(nd['end'])}"), ("العودة للدراسة", f"{wd(back)} {gt(back)}")]
    return countdown(
        ctx, slug="school-holidays", short="الإجازة الدراسية", crumb="كم باقي على الإجازة",
        title="كم باقي على الإجازة؟ مواعيد إجازات المدارس 1448",
        description="كم باقي على إجازة المدارس القادمة في السعودية: مواعيد إجازة الخريف ومنتصف العام ويوم التأسيس والعيدين ونهاية العام الدراسي 1448 بالهجري والميلادي.",
        h1="كم باقي على الإجازة الدراسية؟",
        answer_tpl="تبدأ {label} يوم {weekday} {date} الموافق {hijri}، {left}.",
        dates=dates, facts=facts,
        note="تختلف بداية العام الدراسي ونهايته في مكة المكرمة والمدينة المنورة وجدة والطائف: بدأت الدراسة فيها يوم 30 أغسطس 2026.",
        sources=occasions.SCHOOL_SOURCES,
        table_title="إجازات العام الدراسي 1448",
        table_head=["الإجازة", "تبدأ", "بالهجري", "تنتهي"],
        body=[
            "<h2>التقويم الدراسي 1448</h2>",
            "<p>العام الدراسي 1448 فصلان دراسيان، حسب قرار مجلس الوزراء والتقويم الذي اعتمدته وزارة التعليم لأربع سنوات. بدأت الدراسة يوم الأحد 23 أغسطس 2026، وآخر يوم دراسي الخميس 24 يونيو 2027 الموافق 19 محرم 1449.</p>",
            "<p>نعرض الإجازات كما نشرتها الصحف عن التقويم المعتمد، ونحدّثها إذا أعلنت الوزارة أي تعديل.</p>",
        ],
        faq=[
            ("متى إجازة الخريف؟", "من الجمعة 20 نوفمبر إلى السبت 28 نوفمبر 2026، والعودة للدراسة يوم الأحد 29 نوفمبر."),
            ("متى إجازة منتصف العام؟", "من الجمعة 8 يناير إلى السبت 16 يناير 2027، ويبدأ الفصل الثاني يوم الأحد 17 يناير."),
            ("كم فصل دراسي في 1448؟", "فصلان دراسيان."),
            ("متى نهاية العام الدراسي؟", "آخر يوم دراسي الخميس 24 يونيو 2027 في أغلب المناطق، ويوم 1 يوليو 2027 في مكة المكرمة والمدينة المنورة وجدة والطائف حسب ما نُشر."),
        ],
        related=related_for("school-holidays", [("weighted-percentage", "حاسبة النسبة الموزونة"), ("founding-day", "يوم التأسيس")]),
    )


def build(ctx):
    return (payments.pages(ctx, countdown, related_for) + [school_page(ctx)] + hijri_pages(ctx) + national_pages(ctx))
