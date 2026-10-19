"""Monthly payment pages: government salaries, Citizen Account, Developed Social Security, GOSI pensions.

Rules (researched Oct 2026):
- Salaries: 27th of each Gregorian month; Friday -> Thursday before, Saturday -> Sunday after (MoF payroll page).
- Citizen Account: 10th of each Gregorian month; 2026 practice: Friday -> Thursday, Saturday -> Sunday.
- Developed Social Security: 1st of each Gregorian month; Friday -> Thursday; Saturday -> Thursday (Aug 2026 practice).
- GOSI pensions (all systems since May 2024): 1st; Friday or Saturday -> Thursday before (SAMA notice).
OVERRIDES hold dates that a body has announced (or must announce) differently from the rule.
"""
from datetime import date, timedelta

FRI, SAT = 4, 5

# date announced/expected differently from the rule: {(program, year, month): (date, note)}
OVERRIDES = {
    ("salary", 2026, 5): (date(2026, 5, 24), "قُدّم بسبب إجازة عيد الأضحى"),
}
# months where the rule date falls inside an Eid holiday and no announcement exists yet
PENDING = {
    ("citizen", 2027, 3): "يوافق إجازة عيد الفطر، وقد يُقدَّم",
}

MOF = {"name": "وزارة المالية: مواعيد صرف الرواتب 2026", "url": "https://www.mof.gov.sa/mediacenter/Payroll/Pages/2026.aspx"}
OKAZ_MAY = {"name": "عكاظ: تقديم رواتب مايو 2026", "url": "https://www.okaz.com.sa/economy/na/2245325"}
SABQ_CA = {"name": "سبق: مواعيد حساب المواطن", "url": "https://sabq.org/mawaeed/citizen-account"}
MAAAL_CA = {"name": "مال: إيداع حساب المواطن أكتوبر 2026", "url": "https://maaal.com/news/details/%D8%AD%D8%B3%D8%A7%D8%A8-%D8%A7%D9%84%D9%85%D9%88%D8%A7%D8%B7%D9%86-31-%D9%85%D9%84%D9%8A%D8%A7%D8%B1-%D8%B1/"}
AJEL_CA = {"name": "عاجل: موعد حساب المواطن (يونيو 2026)", "url": "https://ajel.sa/md/articles/2026/06/dvhze368cg.md"}
ALYAUM_SS = {"name": "اليوم: صرف الضمان المطور يوم 30 يوليو 2026", "url": "https://www.alyaum.com/articles/6675212/"}
SABQ_SS = {"name": "سبق: مواعيد الضمان الاجتماعي", "url": "https://sabq.org/mawaeed/social-security"}
SAMA_PEN = {"name": "البنك المركزي السعودي: موعد إيداع المعاشات", "url": "https://rulebook.sama.gov.sa/en/node/4679"}
AJEL_PEN = {"name": "عاجل: توحيد موعد صرف المعاشات (أبريل 2024)", "url": "https://ajel.sa/thehour/irxmxdj3mn"}
SABQ_PEN = {"name": "سبق: التأمينات توضح موعد صرف المعاشات", "url": "https://sabq.org/article/IKL0JVh"}


def months(today, back=2, ahead=14):
    y, m = today.year, today.month - back
    while m < 1:
        y, m = y - 1, m + 12
    for _ in range(back + ahead + 1):
        yield y, m
        m += 1
        if m > 12:
            y, m = y + 1, 1


def schedule(program, day, shifts, today, label_fn, why_fn):
    """shifts: {weekday: days to move}. Returns sorted list of {date, label, moved}."""
    out = []
    for y, m in months(today):
        base = date(y, m, day)
        d, moved = base, None
        if (program, y, m) in OVERRIDES:
            d, moved = OVERRIDES[(program, y, m)]
        elif base.weekday() in shifts:
            d = base + timedelta(days=shifts[base.weekday()])
            moved = why_fn(base)
        if (program, y, m) in PENDING:
            moved = PENDING[(program, y, m)]
        out.append({"date": d, "label": label_fn(y, m), "moved": moved})
    out.sort(key=lambda x: x["date"])
    return out


def batch_no(y, m):
    # Citizen Account batch 1 was paid in December 2017; one batch per month since.
    return (y - 2017) * 12 + m - 11


def pages(ctx, countdown, related_for):
    GM, today = ctx["GM"], ctx["today"]
    wd = ctx["wday"]

    def why(base, word):
        return ("قُدّم" if base.weekday() == FRI or word == "قبل" else "أُخّر") + f" لأن {base.day} يوافق {wd(base)}"

    out = []

    # --- Government salaries ---
    sal = schedule("salary", 27, {FRI: -1, SAT: +1}, today, lambda y, m: f"راتب {GM[m - 1]} {y}",
                   lambda b: why(b, "قبل" if b.weekday() == FRI else "بعد"))
    ns = ctx["next_date"](sal, today)
    sm = ns["label"].replace("راتب ", "")
    out.append(countdown(
        ctx, slug="salary", short="الراتب", crumb="كم باقي على الراتب",
        title=f"كم باقي على الراتب؟ موعد {ns['label']}",
        description=f"موعد صرف رواتب موظفي الدولة لشهر {sm}: {wd(ns['date'])} {ctx['gtext'](ns['date'])} حسب وزارة المالية، مع عد تنازلي وجدول الرواتب للأشهر القادمة بالهجري والميلادي.",
        h1="كم باقي على الراتب؟",
        title_tpl="كم باقي على الراتب؟ موعد {label}",
        answer_tpl="يُصرف {label} يوم {weekday} {date} الموافق {hijri}، {left}.",
        dates=sal,
        facts=[("القاعدة", "يوم 27 من كل شهر ميلادي"), ("إذا وافق الجمعة", "يُصرف الخميس الذي قبله"),
               ("إذا وافق السبت", "يُصرف الأحد الذي بعده"), ("لمن؟", "موظفو الدولة، وتصرفها وزارة المالية")],
        note="هذا موعد رواتب القطاع الحكومي. راتب القطاع الخاص يحدده عقد العمل، والمتقاعدون موعدهم يوم 1 من الشهر.",
        sources=[MOF, OKAZ_MAY],
        table_title="مواعيد الرواتب للأشهر القادمة",
        table_head=["الشهر", "يوم الصرف", "بالهجري", "ملاحظة"],
        table_note="تواريخ 2026 منشورة في تقويم وزارة المالية، وتواريخ 2027 محسوبة بالقاعدة نفسها إلى أن تنشر الوزارة تقويمها.",
        body=[
            "<h2>متى ينزل الراتب؟</h2>",
            "<p>تصرف وزارة المالية رواتب موظفي الدولة يوم 27 من كل شهر ميلادي. إذا وافق يوم 27 الجمعة يكون الصرف يوم الخميس الذي قبله، وإذا وافق السبت يكون الصرف يوم الأحد الذي بعده.</p>",
            "<h2>إذا وافق الموعد إجازة عيد</h2>",
            "<p>القاعدة المنشورة لا تذكر الأعياد، والوزارة تحدد الموعد في كل حالة. في مايو 2026 وافق يوم 27 إجازة عيد الأضحى، فصُرفت الرواتب مبكرًا يوم الأحد 24 مايو. نحدّث الجدول فور أي إعلان.</p>",
            "<h2>متى يظهر الراتب في الحساب؟</h2>",
            "<p>تُحوَّل الرواتب إلى البنوك في يوم الصرف، وقد يختلف وقت ظهورها في الحساب من بنك لآخر. إذا انتهى يوم الصرف ولم يصل راتبك فراجع جهة عملك أو بنكك.</p>",
        ],
        faq=[
            ("هل الموعد يشمل القطاع الخاص؟", "لا. هذا موعد رواتب موظفي الدولة. موعد راتب القطاع الخاص يحدده عقد العمل وسياسة الشركة."),
            ("الراتب بالهجري أو بالميلادي؟", "بالميلادي: يوم 27 من كل شهر ميلادي. نذكر الموافق الهجري في الجدول للتسهيل."),
            ("متى رواتب المتقاعدين؟", "يوم 1 من كل شهر ميلادي. اطلع على <a href=\"@@pension\">موعد رواتب التقاعد</a>."),
            ("متى ينزل حساب المواطن؟", "يوم 10 من كل شهر ميلادي. اطلع على <a href=\"@@citizen-account\">موعد حساب المواطن</a>."),
        ],
        related=related_for("salary", [("pension", "رواتب التقاعد"), ("citizen-account", "حساب المواطن"), ("end-of-service", "حاسبة نهاية الخدمة")]),
    ))

    # --- Citizen Account ---
    ca = schedule("citizen", 10, {FRI: -1, SAT: +1}, today, lambda y, m: f"الدفعة {batch_no(y, m)}",
                  lambda b: why(b, "قبل" if b.weekday() == FRI else "بعد"))
    nc = ctx["next_date"](ca, today)
    out.append(countdown(
        ctx, slug="citizen-account", short="حساب المواطن", crumb="موعد حساب المواطن",
        title=f"موعد حساب المواطن {nc['label']}: كم باقي على نزول الدعم؟",
        description=f"موعد إيداع حساب المواطن {nc['label']}: {wd(nc['date'])} {ctx['gtext'](nc['date'])}، مع عد تنازلي وجدول الدفعات القادمة بالهجري والميلادي.",
        h1=f"موعد حساب المواطن {nc['label']}",
        h1_tpl="موعد حساب المواطن {label}",
        title_tpl="موعد حساب المواطن {label}: كم باقي على نزول الدعم؟",
        answer_tpl="تُودع {label} من حساب المواطن يوم {weekday} {date} الموافق {hijri}، {left}.",
        dates=ca,
        facts=[("الموعد المعتاد", "يوم 10 من كل شهر ميلادي"), ("إذا وافق الجمعة", "أُودع في 2026 يوم الخميس الذي قبله"),
               ("إذا وافق السبت", "أُودع في 2026 يوم الأحد الذي بعده"), ("الدفعة القادمة", nc["label"])],
        note="قاعدة نهاية الأسبوع غير منشورة رسميًا، ونطبق ما فعله البرنامج في دفعات 2026. نحدّث الجدول عند أي إعلان من حساب المواطن.",
        sources=[SABQ_CA, MAAAL_CA, AJEL_CA],
        table_title="الدفعات القادمة",
        table_head=["الدفعة", "يوم الإيداع", "بالهجري", "ملاحظة"],
        table_note="تواريخ محسوبة من الموعد المعتاد وما طُبّق في 2026. وفي أبريل 2024، حين وافق يوم 10 عيد الفطر، أُودعت الدفعة قبل العيد.",
        body=[
            "<h2>متى ينزل حساب المواطن؟</h2>",
            "<p>يودع برنامج حساب المواطن الدعم يوم 10 من كل شهر ميلادي. في دفعات 2026 كان الإيداع يوم الخميس إذا وافق يوم 10 الجمعة، ويوم الأحد إذا وافق السبت.</p>",
            "<h2>رقم الدفعة</h2>",
            "<p>صُرفت الدفعة الأولى في ديسمبر 2017، ويزيد رقم الدفعة واحدًا كل شهر. لذلك دفعة نوفمبر 2026 هي الدفعة 108.</p>",
            "<h2>الأهلية ومبلغ الدعم</h2>",
            "<p>تختلف الأهلية والمبلغ حسب دخل الأسرة وعدد أفرادها. تحقق من حالتك ومبلغ دفعتك من القنوات الرسمية لبرنامج حساب المواطن.</p>",
        ],
        faq=[
            ("هل يتأخر حساب المواطن إذا وافق إجازة؟", "إذا وافق يوم 10 الجمعة أو السبت يُنقل الإيداع ليوم عمل قريب، وفي إجازة العيد يُقدَّم عادة. نحدّث الجدول عند كل إعلان."),
            ("كم رقم الدفعة القادمة؟", f"{nc['label']}، وموعدها {wd(nc['date'])} {ctx['gtext'](nc['date'])}."),
            ("متى الراتب؟", "<a href=\"@@salary\">رواتب موظفي الدولة</a> يوم 27 من كل شهر ميلادي."),
            ("متى الضمان الاجتماعي؟", "<a href=\"@@social-security\">الضمان الاجتماعي المطور</a> يوم 1 من كل شهر ميلادي."),
        ],
        related=related_for("citizen-account", [("social-security", "الضمان الاجتماعي"), ("salary", "موعد الراتب")]),
    ))

    # --- Developed Social Security ---
    ss = schedule("social", 1, {FRI: -1, SAT: -2}, today, lambda y, m: f"دفعة {GM[m - 1]} {y}",
                  lambda b: why(b, "قبل"))
    nss = ctx["next_date"](ss, today)
    ssm = nss["label"].replace("دفعة ", "")
    out.append(countdown(
        ctx, slug="social-security", short="الضمان الاجتماعي", crumb="موعد الضمان الاجتماعي",
        title=f"موعد نزول الضمان الاجتماعي المطور لشهر {ssm}",
        description=f"موعد صرف الضمان الاجتماعي المطور لشهر {ssm}: {wd(nss['date'])} {ctx['gtext'](nss['date'])}، مع عد تنازلي وجدول مواعيد الصرف القادمة بالهجري والميلادي.",
        h1="موعد نزول الضمان الاجتماعي المطور",
        answer_tpl="تُصرف {label} من الضمان الاجتماعي المطور يوم {weekday} {date} الموافق {hijri}، {left}.",
        dates=ss,
        facts=[("الموعد المعتاد", "يوم 1 من كل شهر ميلادي"), ("إذا وافق الجمعة أو السبت", "صُرف في 2026 يوم الخميس الذي قبله"),
               ("الجهة", "وزارة الموارد البشرية والتنمية الاجتماعية")],
        note="المصادر تختلف في حالة يوم السبت. في أغسطس 2026 صُرف الضمان يوم الخميس 30 يوليو بدل السبت 1 أغسطس، ونطبق ذلك حتى يصدر إعلان مختلف.",
        sources=[ALYAUM_SS, SABQ_SS],
        table_title="مواعيد الصرف القادمة",
        table_head=["الدفعة", "يوم الصرف", "بالهجري", "ملاحظة"],
        table_note="تواريخ محسوبة من الموعد المعتاد وما طُبّق في 2026، وتُحدَّث عند إعلان الوزارة.",
        body=[
            "<h2>متى ينزل الضمان المطور؟</h2>",
            "<p>تصرف وزارة الموارد البشرية والتنمية الاجتماعية معاش الضمان الاجتماعي المطور يوم 1 من كل شهر ميلادي. إذا وافق يوم 1 الجمعة يُصرف يوم الخميس الذي قبله. وفي أغسطس 2026 وافق السبت فصُرف يوم الخميس 30 يوليو.</p>",
            "<p>المبلغ والأهلية يختلفان حسب حالة كل أسرة، وتجدهما في القنوات الرسمية لوزارة الموارد البشرية والتنمية الاجتماعية.</p>",
        ],
        faq=[
            ("هل الضمان والتقاعد في اليوم نفسه؟", "كلاهما يوم 1 من الشهر الميلادي، لكن جهة الصرف مختلفة. اطلع على <a href=\"@@pension\">موعد رواتب التقاعد</a>."),
            ("متى حساب المواطن؟", "يوم 10 من كل شهر ميلادي. اطلع على <a href=\"@@citizen-account\">موعد حساب المواطن</a>."),
        ],
        related=related_for("social-security", [("citizen-account", "حساب المواطن"), ("pension", "رواتب التقاعد")]),
    ))

    # --- GOSI pensions ---
    pen = schedule("pension", 1, {FRI: -1, SAT: -2}, today, lambda y, m: f"معاش {GM[m - 1]} {y}",
                   lambda b: why(b, "قبل"))
    npn = ctx["next_date"](pen, today)
    pm = npn["label"].replace("معاش ", "")
    out.append(countdown(
        ctx, slug="pension", short="رواتب التقاعد", crumb="موعد رواتب التقاعد",
        title=f"موعد صرف رواتب المتقاعدين لشهر {pm}",
        description=f"موعد صرف معاشات المتقاعدين المدنيين والعسكريين والقطاع الخاص لشهر {pm}: {wd(npn['date'])} {ctx['gtext'](npn['date'])}، مع عد تنازلي وجدول الأشهر القادمة.",
        h1="موعد رواتب المتقاعدين",
        answer_tpl="يُصرف {label} للمتقاعدين يوم {weekday} {date} الموافق {hijri}، {left}.",
        dates=pen,
        facts=[("الموعد", "يوم 1 من كل شهر ميلادي، لكل الأنظمة"), ("إذا وافق الجمعة أو السبت", "يُصرف الخميس الذي قبله"),
               ("إذا وافق إجازة رسمية", "آخر يوم عمل قبل الإجازة"), ("الجهة", "المؤسسة العامة للتأمينات الاجتماعية")],
        sources=[SAMA_PEN, AJEL_PEN, SABQ_PEN],
        table_title="مواعيد المعاشات القادمة",
        table_head=["الشهر", "يوم الصرف", "بالهجري", "ملاحظة"],
        body=[
            "<h2>متى تنزل رواتب التقاعد؟</h2>",
            "<p>منذ مايو 2024 صار موعد صرف معاشات المتقاعدين في المؤسسة العامة للتأمينات الاجتماعية واحدًا لكل الأنظمة: المدني والعسكري والقطاع الخاص، وهو يوم 1 من كل شهر ميلادي.</p>",
            "<p>إذا وافق يوم 1 الجمعة أو السبت يُصرف المعاش يوم الخميس الذي قبله، وإذا وافق إجازة رسمية يُصرف في آخر يوم عمل قبلها.</p>",
        ],
        faq=[
            ("هل المتقاعدون العسكريون في الموعد نفسه؟", "نعم. كل الأنظمة تُصرف يوم 1 من الشهر الميلادي منذ مايو 2024."),
            ("متى رواتب الموظفين؟", "<a href=\"@@salary\">رواتب موظفي الدولة</a> يوم 27 من كل شهر ميلادي."),
        ],
        related=related_for("pension", [("salary", "موعد الراتب"), ("social-security", "الضمان الاجتماعي")]),
    ))
    return out
