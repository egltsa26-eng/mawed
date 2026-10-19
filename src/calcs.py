"""Calculator pages. Formulas live in src/calc/*.js; text here."""
import json
from pathlib import Path

import labor  # noqa: E402  (end-of-service, overtime, weighted % — researched rules)

CALC_DIR = Path(__file__).resolve().parent / "calc"


def js(name):
    return (CALC_DIR / f"{name}.js").read_text()


def day_month_year(prefix, year_label="السنة", year_hint=""):
    return (
        '<div class="row2">'
        f'<div class="field"><label for="{prefix}-d">اليوم</label><input id="{prefix}-d" type="number" inputmode="numeric" min="1" max="31" value="15"></div>'
        f'<div class="field"><label for="{prefix}-m">الشهر</label><select id="{prefix}-m"></select></div>'
        f'<div class="field"><label for="{prefix}-y">{year_label}</label><input id="{prefix}-y" type="number" inputmode="numeric" value="1995">'
        f'<span class="hint" id="{prefix}-y-hint">{year_hint}</span></div>'
        '</div>'
    )


def page(slug, *, title, description, crumb, h1, lead, calc, form, result_title, body, faq, sources, related,
         home_desc, script):
    return {
        "slug": slug, "template": "calc.html", "section": "tools", "title": title, "description": description,
        "home_desc": home_desc,
        "jsonld": json.dumps({"@context": "https://schema.org", "@type": "WebApplication", "name": h1,
                              "applicationCategory": "UtilitiesApplication", "operatingSystem": "Any",
                              "inLanguage": "ar-SA", "offers": {"@type": "Offer", "price": "0", "priceCurrency": "SAR"}},
                             ensure_ascii=False),
        "p": {"crumb": crumb, "h1": h1, "lead": lead, "calc": calc, "form": form, "result_title": result_title,
              "result": '<p class="muted">جاري الحساب…</p>', "body": body, "faq": faq, "sources": sources,
              "related": related, "script": script},
    }


def build(ctx):
    pages = labor.pages(page, js)
    pages.append(page(
        "age", title="حساب العمر بالهجري والميلادي بدقة", crumb="حساب العمر",
        description="احسب عمرك بالسنوات والأشهر والأيام بالهجري والميلادي، واعرف يوم ميلادك وتاريخه المقابل حسب تقويم أم القرى.",
        h1="حساب العمر بالهجري والميلادي",
        lead="اكتب تاريخ ميلادك بالهجري أو بالميلادي، ونطلع لك عمرك بالتقويمين، ويوم ميلادك، وكم باقي على عيد ميلادك.",
        calc="age", result_title="عمرك اليوم",
        form=('<div class="field"><label for="age-cal">تقويم تاريخ الميلاد</label>'
              '<select id="age-cal"><option value="g">ميلادي</option><option value="h">هجري</option></select></div>'
              + day_month_year("age", "سنة الميلاد")),
        body=[
            "<h2>كيف نحسب العمر؟</h2>",
            "<p>نطرح تاريخ ميلادك من تاريخ اليوم بتوقيت الرياض، ونحسب السنوات ثم الأشهر ثم الأيام. في العمر الهجري نستخدم أطوال الأشهر الحقيقية في تقويم أم القرى، فبعض الأشهر 29 يومًا وبعضها 30.</p>",
            "<h2>ليش عمري بالهجري أكبر؟</h2>",
            "<p>السنة الهجرية نحو 354 يومًا، أي أقصر من الميلادية بنحو 11 يومًا. لذلك يزيد عمرك بالهجري سنة تقريبًا كل 33 سنة ميلادية.</p>",
        ],
        faq=[("هل يعتمد الحساب على تقويم أم القرى؟", "نعم، وهو التقويم المعتمد في المملكة، ويغطي المدى من 1343 إلى 1500 هـ."),
             ("من مواليد 29 فبراير، متى عيد ميلادي؟", "في السنوات غير الكبيسة نعتبره 28 فبراير.")],
        sources=[{"name": "سعوديبيديا: تقويم أم القرى", "url": "https://saudipedia.com/%D8%AA%D9%82%D9%88%D9%8A%D9%85-%D8%A3%D9%85-%D8%A7%D9%84%D9%82%D8%B1%D9%89"}],
        related=[("date-converter", "تحويل التاريخ"), ("ramadan", "كم باقي على رمضان"), ("end-of-service", "حاسبة نهاية الخدمة")],
        home_desc="عمرك بالسنوات والأشهر والأيام، بالهجري والميلادي.",
        script=js("age"),
    ))
    pages.append(page(
        "date-converter", title="تحويل التاريخ من هجري إلى ميلادي والعكس", crumb="تحويل التاريخ",
        description="حوّل أي تاريخ من الهجري إلى الميلادي أو العكس حسب تقويم أم القرى المعتمد في السعودية، مع اسم اليوم.",
        h1="تحويل التاريخ هجري ميلادي",
        lead="اختر اتجاه التحويل واكتب التاريخ، وتطلع لك النتيجة مع اسم اليوم حسب تقويم أم القرى.",
        calc="convert", result_title="التاريخ المقابل",
        form=('<div class="field"><label for="cv-dir">اتجاه التحويل</label>'
              '<select id="cv-dir"><option value="g2h">من ميلادي إلى هجري</option><option value="h2g">من هجري إلى ميلادي</option></select></div>'
              + day_month_year("cv", "السنة", "من 1925 إلى 2077 م")),
        body=[
            "<h2>عن تقويم أم القرى</h2>",
            "<p>تقويم أم القرى هو التقويم الهجري الرسمي في المملكة، ويُحسب فلكيًا مسبقًا. تعتمد عليه الجهات الحكومية في المعاملات والعقود. أما بداية رمضان والأعياد فتُعلن بعد رؤية الهلال، فقد تختلف بيوم.</p>",
            "<h2>أطوال الأشهر الهجرية</h2>",
            "<p>الشهر الهجري 29 أو 30 يومًا، ولا يتكرر النمط نفسه كل سنة. إذا كتبت يوم 30 في شهر طوله 29 يومًا ننبهك.</p>",
        ],
        faq=[("ليش يختلف التحويل بين المواقع بيوم؟", "بعض المواقع تستخدم حسابًا تقريبيًا أو تقويمًا غير أم القرى. نحن نعتمد جدول أم القرى الرسمي."),
             ("ما المدى المتاح؟", "من 1343 إلى 1500 هـ، أي من 1925 إلى 2077 م تقريبًا.")],
        sources=[{"name": "سعوديبيديا: تقويم أم القرى", "url": "https://saudipedia.com/%D8%AA%D9%82%D9%88%D9%8A%D9%85-%D8%A3%D9%85-%D8%A7%D9%84%D9%82%D8%B1%D9%89"}],
        related=[("age", "حساب العمر"), ("ramadan", "كم باقي على رمضان"), ("eid-al-adha", "كم باقي على عيد الأضحى")],
        home_desc="من هجري إلى ميلادي والعكس حسب أم القرى.",
        script=js("convert"),
    ))
    pages.append(page(
        "vat", title="حاسبة ضريبة القيمة المضافة 15% في السعودية", crumb="حاسبة الضريبة 15%",
        description="احسب ضريبة القيمة المضافة 15% في السعودية: أضف الضريبة على المبلغ، أو استخرجها من مبلغ شامل الضريبة.",
        h1="حاسبة ضريبة القيمة المضافة 15%",
        lead="أضف الضريبة على سعر قبل الضريبة، أو استخرج الضريبة من سعر شامل لها.",
        calc="vat", result_title="الضريبة",
        form=('<div class="field"><label for="vat-amount">المبلغ بالريال</label>'
              '<input id="vat-amount" type="text" inputmode="decimal" value="1000" dir="ltr"></div>'
              '<fieldset class="field" style="border:0;padding:0;margin:0"><legend class="label">المبلغ اللي كتبته</legend><div class="choices">'
              '<label><input type="radio" name="vat-mode" value="add" checked> قبل الضريبة</label>'
              '<label><input type="radio" name="vat-mode" value="extract"> شامل الضريبة</label></div></fieldset>'),
        body=[
            "<h2>طريقة الحساب</h2>",
            "<p>نسبة ضريبة القيمة المضافة في المملكة 15%. لإضافة الضريبة: اضرب المبلغ في 0.15 ثم أضفه. ولاستخراجها من مبلغ شامل: اقسم المبلغ على 1.15 لتعرف السعر قبل الضريبة، والفرق هو الضريبة.</p>",
            "<p>مثال: سعر 1,000 ريال قبل الضريبة تصبح ضريبته 150 ريالًا والإجمالي 1,150 ريالًا. ومبلغ 1,150 ريالًا شامل الضريبة قيمته قبل الضريبة 1,000 ريال.</p>",
        ],
        faq=[("متى صارت الضريبة 15%؟", "رُفعت النسبة من 5% إلى 15% ابتداءً من 1 يوليو 2020."),
             ("هل كل السلع عليها 15%؟", "أغلبها، وبعض التوريدات معفاة أو بنسبة صفر حسب نظام الضريبة. راجع هيئة الزكاة والضريبة والجمارك للتفاصيل.")],
        sources=[{"name": "هيئة الزكاة والضريبة والجمارك", "url": "https://zatca.gov.sa/ar/Pages/default.aspx"}],
        related=[("end-of-service", "حاسبة نهاية الخدمة"), ("salary", "موعد الراتب")],
        home_desc="أضف 15% أو استخرجها من مبلغ شامل.",
        script=js("vat"),
    ))
    return pages
