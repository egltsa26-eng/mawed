"""Labor-law and education calculators: end of service, overtime, weighted percentage."""

LAW_REL = {"name": "نظام العمل: علاقات العمل، المواد 50 إلى 88 (وزارة الموارد البشرية)", "url": "https://www.hrsd.gov.sa/%D8%B9%D9%84%D8%A7%D9%82%D8%A7%D8%AA-%D8%A7%D9%84%D8%B9%D9%85%D9%84"}
LAW_COND = {"name": "نظام العمل: شروط العمل وظروفه، المواد 89 إلى 118", "url": "https://www.hrsd.gov.sa/%D8%B4%D8%B1%D9%88%D8%B7-%D8%A7%D9%84%D8%B9%D9%85%D9%84-%D9%88%D8%B8%D8%B1%D9%88%D9%81%D9%87"}
LAW_DEF = {"name": "نظام العمل: التعريفات والأحكام العامة", "url": "https://www.hrsd.gov.sa/%D8%A7%D9%84%D8%AA%D8%B9%D8%B1%D9%8A%D9%81%D8%A7%D8%AA/%D8%A7%D9%84%D8%A3%D8%AD%D9%83%D8%A7%D9%85-%D8%A7%D9%84%D8%B9%D8%A7%D9%85%D8%A9"}
HRSD_CALC = {"name": "حاسبة نهاية الخدمة الرسمية (وزارة الموارد البشرية)", "url": "https://www.hrsd.gov.sa/ar/ministry-services/services/end-service-benefit-calculator"}


def pages(page, js):
    out = []
    out.append(page(
        "end-of-service", title="حاسبة مكافأة نهاية الخدمة حسب نظام العمل السعودي", crumb="حاسبة نهاية الخدمة",
        description="احسب مكافأة نهاية الخدمة حسب نظام العمل السعودي: نصف شهر عن كل سنة من أول خمس سنوات وشهر عن كل سنة بعدها، مع حالات الاستقالة.",
        h1="حاسبة مكافأة نهاية الخدمة",
        lead="اكتب تاريخ بداية العمل ونهايته وآخر أجر، واختر سبب انتهاء العلاقة. نحسب المكافأة حسب المادتين 84 و85 من نظام العمل.",
        calc="eosb", result_title="مكافأة نهاية الخدمة",
        form=(
            '<div class="row2">'
            '<div class="field"><label for="eos-start">بداية العمل</label><input id="eos-start" type="date" value="2018-03-01"></div>'
            '<div class="field"><label for="eos-end">نهاية العمل</label><input id="eos-end" type="date" value="2026-10-31"></div>'
            '</div>'
            '<div class="row2">'
            '<div class="field"><label for="eos-basic">الراتب الأساسي</label><input id="eos-basic" type="text" inputmode="decimal" dir="ltr" value="8000"></div>'
            '<div class="field"><label for="eos-housing">بدل السكن</label><input id="eos-housing" type="text" inputmode="decimal" dir="ltr" value="2000"></div>'
            '<div class="field"><label for="eos-transport">بدل النقل</label><input id="eos-transport" type="text" inputmode="decimal" dir="ltr" value="800"></div>'
            '<div class="field"><label for="eos-other">بدلات ثابتة أخرى</label><input id="eos-other" type="text" inputmode="decimal" dir="ltr" value="0"></div>'
            '</div>'
            '<div class="field"><label for="eos-leave">أيام الإجازة السنوية المتبقية (اختياري)</label><input id="eos-leave" type="text" inputmode="numeric" dir="ltr" value="0">'
            '<span class="hint">تُصرف بأجرها عند نهاية الخدمة حسب المادة 111، ونحسب اليوم بأجر شهري ÷ 30</span></div>'
            '<p class="hint" style="font-family:var(--display);font-size:var(--fs-0);color:var(--ink-2);margin:0">نحسب على آخر أجر شهري. المثال المكتوب أعلاه للتوضيح، غيّره بأرقامك.</p>'
            '<fieldset class="field" style="border:0;padding:0;margin:0"><legend class="label">نوع العقد</legend><div class="choices">'
            '<label><input type="radio" name="eos-contract" value="fixed" checked> محدد المدة</label>'
            '<label><input type="radio" name="eos-contract" value="open"> غير محدد المدة</label>'
            '</div></fieldset>'
            '<fieldset class="field" style="border:0;padding:0;margin:0"><legend class="label">سبب انتهاء العلاقة</legend><div class="choices">'
            '<label><input type="radio" name="eos-reason" value="employer" checked> انتهاء العقد أو إنهاؤه من صاحب العمل</label>'
            '<label><input type="radio" name="eos-reason" value="resign"> استقالة</label>'
            '<label><input type="radio" name="eos-reason" value="art87"> حالات المادة 87</label>'
            '<label><input type="radio" name="eos-reason" value="art80"> فصل وفق المادة 80</label>'
            '</div></fieldset>'),
        body=[
            "<h2>كيف تُحسب مكافأة نهاية الخدمة؟</h2>",
            "<p>حسب المادة 84 من نظام العمل: أجر نصف شهر عن كل سنة من السنوات الخمس الأولى، وأجر شهر كامل عن كل سنة بعدها. ويُحسب جزء السنة بنسبة ما قضاه العامل منها، والأجر المعتمد هو آخر أجر تقاضاه العامل.</p>",
            "<h2>إذا كانت استقالة</h2>",
            "<p>حسب المادة 85: لا مكافأة إذا كانت الخدمة أقل من سنتين متتاليتين. ثلث المكافأة إذا كانت من سنتين إلى خمس سنوات، وثلثاها إذا زادت على خمس سنوات ولم تبلغ عشرًا، والمكافأة كاملة إذا بلغت عشر سنوات فأكثر.</p>",
            "<p>تعديلات نظام العمل التي بدأ تطبيقها في فبراير 2025 لم تغير هذه النسب، لكنها ربطت تعريف الاستقالة بالعقد محدد المدة. إذا كان عقدك غير محدد المدة وأنهيته بإشعار، تنبهك الحاسبة إلى أن الحكم غير محسوم.</p>",
            "<h2>حالات المادة 87</h2>",
            "<p>يستحق العامل المكافأة كاملة إذا ترك العمل بسبب قوة قاهرة خارجة عن إرادته. وتستحقها العاملة كاملة إذا أنهت العقد خلال ستة أشهر من عقد زواجها أو ثلاثة أشهر من وضعها.</p>",
            "<h2>مثال محسوب</h2>",
            "<p>عامل خدم 8 سنوات وآخر أجر له 10,000 ريال، وانتهى عقده من صاحب العمل: عن أول 5 سنوات 5 × 5,000 = 25,000 ريال، وعن 3 سنوات بعدها 3 × 10,000 = 30,000 ريال. المجموع 55,000 ريال. ولو استقال بعد 8 سنوات يستحق ثلثيها: 36,666.67 ريال.</p>",
        ],
        faq=[
            ("هل يدخل بدل السكن في حساب المكافأة؟", "النظام يعتمد آخر أجر، ويعرّف الأجر الفعلي بأنه الأجر الأساسي مع الزيادات والبدلات الثابتة. لذلك تدخل البدلات الثابتة مثل السكن والنقل. إذا نص عقدك على غير ذلك فارجع لمكتب العمل."),
            ("كيف تُحسب الأشهر والأيام؟", "نحسب جزء السنة بنسبته: الشهر 1/12 من السنة، واليوم 1/365، ونحسب المدة بالتقويم الميلادي المعتمد في أغلب العقود. المادة العاشرة من النظام تحسب المدد بالهجري ما لم ينص العقد على غير ذلك، والفرق بينهما صغير."),
            ("هل تُصرف الإجازات المتبقية مع المكافأة؟", "نعم. حسب المادة 111 يستحق العامل عند ترك العمل أجر أيام إجازته السنوية التي لم يأخذها. اكتب عددها في الحقل الاختياري ونضيفها إلى النتيجة. النظام لا يحدد طريقة حساب أجر اليوم، والشائع قسمة الأجر الشهري على 30."),
            ("هل للوزارة حاسبة رسمية؟", "نعم، لوزارة الموارد البشرية <a href=\"https://www.hrsd.gov.sa/ar/ministry-services/services/end-service-benefit-calculator\" rel=\"noopener\" target=\"_blank\">حاسبة مكافأة نهاية الخدمة</a>. ننصح بمقارنة النتيجة بها."),
            ("أستقلت قبل سنتين، هل لي شيء؟", "حسب المادة 85 لا يستحق المستقيل مكافأة إذا كانت خدمته أقل من سنتين متتاليتين."),
            ("هل النتيجة ملزمة؟", "لا، النتيجة تقديرية للاسترشاد. عند الخلاف يُرجع للعقد ولمحاكم العمل أو وزارة الموارد البشرية."),
        ],
        sources=[LAW_REL, LAW_DEF, HRSD_CALC],
        related=[("overtime", "حاسبة العمل الإضافي"), ("salary", "موعد الراتب"), ("vat", "حاسبة الضريبة")],
        home_desc="حسب المادتين 84 و85، مع حالات الاستقالة.",
        script=js("eosb"),
    ))
    out.append(page(
        "overtime", title="حاسبة العمل الإضافي حسب نظام العمل السعودي", crumb="حاسبة العمل الإضافي",
        description="احسب أجر ساعات العمل الإضافي حسب المادة 107 من نظام العمل السعودي: أجر الساعة مضافًا إليه 50% من الأجر الأساسي.",
        h1="حاسبة أجر العمل الإضافي",
        lead="اكتب راتبك الأساسي والبدلات وعدد الساعات الإضافية، ونحسب أجرها حسب المادة 107 من نظام العمل.",
        calc="overtime", result_title="أجر العمل الإضافي",
        form=(
            '<div class="row2">'
            '<div class="field"><label for="ot-basic">الراتب الأساسي الشهري</label><input id="ot-basic" type="text" inputmode="decimal" dir="ltr" value="6000"></div>'
            '<div class="field"><label for="ot-allow">مجموع البدلات الثابتة</label><input id="ot-allow" type="text" inputmode="decimal" dir="ltr" value="1500"></div>'
            '</div><div class="row2">'
            '<div class="field"><label for="ot-hours">ساعات العمل الإضافي</label><input id="ot-hours" type="text" inputmode="decimal" dir="ltr" value="10"></div>'
            '<div class="field"><label for="ot-daily">ساعات الدوام اليومي</label><input id="ot-daily" type="text" inputmode="decimal" dir="ltr" value="8"><span class="hint">8 ساعات، أو 6 في رمضان للمسلمين</span></div>'
            '</div>'),
        body=[
            "<h2>طريقة الحساب</h2>",
            "<p>تنص المادة 107 على أن يدفع صاحب العمل عن ساعة العمل الإضافية أجر الساعة مضافًا إليه 50% من أجر الساعة الأساسي. نحسب أجر الساعة بقسمة الأجر الشهري على 30 يومًا ثم على ساعات الدوام اليومي.</p>",
            "<p>مثال: راتب أساسي 6,000 ريال وبدلات 1,500 ريال ودوام 8 ساعات. أجر الساعة الفعلي 7,500 ÷ 240 = 31.25 ريالًا، ونصف أجر الساعة الأساسي 6,000 ÷ 240 × 0.5 = 12.50 ريالًا. فساعة العمل الإضافي = 43.75 ريالًا.</p>",
        ],
        faq=[
            ("هل العمل يوم الإجازة الأسبوعية يُحسب إضافيًا؟", "نعم، يعد العمل في أيام العطل والأعياد عملًا إضافيًا حسب نظام العمل."),
            ("هل يجوز تعويضي بإجازة بدل أجر العمل الإضافي؟", "بعد تعديلات نظام العمل في 2025 يجوز، باتفاق العامل وصاحب العمل، أن يُعوض العامل عن ساعات العمل الإضافي بأيام إجازة مدفوعة الأجر بدل الأجر الإضافي."),
            ("كيف يُحسب أجر الساعة؟", "النظام لا يحدد طريقة القسمة. الشائع قسمة الأجر الشهري على 30 يومًا ثم على ساعات الدوام اليومي، وهذا ما تستخدمه الحاسبة."),
        ],
        sources=[LAW_COND],
        related=[("end-of-service", "حاسبة نهاية الخدمة"), ("salary", "موعد الراتب")],
        home_desc="أجر الساعة + 50% من الأساسي حسب المادة 107.",
        script=js("overtime"),
    ))
    out.append(page(
        "weighted-percentage", title="حاسبة النسبة الموزونة للقبول الجامعي", crumb="حاسبة النسبة الموزونة",
        description="احسب نسبتك الموزونة للقبول في الجامعات السعودية من درجة الثانوي والقدرات والتحصيلي، مع أشهر الأوزان أو أوزانك الخاصة.",
        h1="حاسبة النسبة الموزونة",
        lead="اكتب نسبة الثانوي ودرجة القدرات والتحصيلي، واختر الأوزان التي تعلنها الجامعة لتخصصك.",
        calc="weighted", result_title="نسبتك الموزونة",
        form=(
            '<div class="row2">'
            '<div class="field"><label for="w-gpa">نسبة الثانوي</label><input id="w-gpa" type="text" inputmode="decimal" dir="ltr" value="95"></div>'
            '<div class="field"><label for="w-q">القدرات العامة</label><input id="w-q" type="text" inputmode="decimal" dir="ltr" value="80"></div>'
            '<div class="field"><label for="w-t">التحصيلي</label><input id="w-t" type="text" inputmode="decimal" dir="ltr" value="78"></div>'
            '<div class="field" data-step hidden><label for="w-s">اختبار STEP</label><input id="w-s" type="text" inputmode="decimal" dir="ltr" value="70"></div>'
            '</div>'
            '<div class="field"><label for="w-preset">الأوزان</label><select id="w-preset">'
            '<option value="30-30-40-0">جامعة الملك سعود 1448: ثانوي 30%، قدرات 30%، تحصيلي 40%</option>'
            '<option value="30-30-30-10">جامعة الملك عبدالعزيز 1448: ثانوي 30%، قدرات 30%، تحصيلي 30%، STEP 10%</option>'
            '<option value="30-30-40-0">جامعة الإمام (دليل 1447): ثانوي 30%، قدرات 30%، تحصيلي 40%</option>'
            '<option value="custom">أوزان أخرى أكتبها بنفسي</option>'
            '</select><span class="hint">تأكد من الأوزان في دليل القبول لجامعتك، فقد تختلف حسب البرنامج.</span></div>'
            '<div class="row2" data-custom hidden>'
            '<div class="field"><label for="w-wg">وزن الثانوي %</label><input id="w-wg" type="text" inputmode="decimal" dir="ltr" value="30"></div>'
            '<div class="field"><label for="w-wq">وزن القدرات %</label><input id="w-wq" type="text" inputmode="decimal" dir="ltr" value="30"></div>'
            '<div class="field"><label for="w-wt">وزن التحصيلي %</label><input id="w-wt" type="text" inputmode="decimal" dir="ltr" value="40"></div>'
            '<div class="field"><label for="w-ws">وزن STEP %</label><input id="w-ws" type="text" inputmode="decimal" dir="ltr" value="0"></div>'
            '</div>'),
        body=[
            "<h2>كيف تُحسب النسبة الموزونة؟</h2>",
            "<p>تضرب كل درجة في وزنها ثم تجمع النواتج. مثلًا بأوزان 30% و30% و40%: ثانوي 95 × 0.30 = 28.5، وقدرات 80 × 0.30 = 24، وتحصيلي 78 × 0.40 = 31.2. فالنسبة الموزونة 83.70%.</p>",
            "<h2>أوزان الجامعات للعام 1448</h2>",
            "<p>جامعة الملك سعود تعتمد في دليل القبول للعام الجامعي 2026/2027: 30% للثانوي و30% للقدرات و40% للتحصيلي لكل المسارات، وتشترط للبرامج المتميزة نسبة موزونة لا تقل عن 95% للطب و90% لغيره. وأضافت جامعة الملك عبدالعزيز هذا العام اختبار STEP بوزن 10%، مع 30% لكل من الثانوي والقدرات والتحصيلي.</p>",
            "<p>كل جامعة تعلن أوزانها في دليل القبول، وقد تختلف حسب البرنامج أو تتغير من سنة لأخرى. إذا كانت جامعتك غير موجودة في القائمة فاختر الأوزان الخاصة واكتب ما في دليلها.</p>",
        ],
        faq=[
            ("هل التحصيلي مطلوب لكل التخصصات؟", "في جامعة الملك سعود يدخل التحصيلي في كل المسارات للعام 1448. جامعات وبرامج أخرى قد تختلف، فراجع دليل جامعتك واستخدم الأوزان الخاصة."),
            ("ما الفرق بين النسبة الموزونة والمعدل؟", "المعدل هو نسبة الثانوي فقط، أما الموزونة فتجمع الثانوي والاختبارات بأوزان تحددها الجامعة."),
        ],
        sources=[{"name": "جامعة الملك سعود: دليل القبول 2026/2027", "url": "https://dar.ksu.edu.sa/sites/dar.ksu.edu.sa/files/2026-06/admgar_1.pdf"},
                 {"name": "جامعة الملك عبدالعزيز: دليل القبول", "url": "https://kau.edu.sa/u/15Qfc"},
                 {"name": "المدينة: إضافة STEP لمعايير القبول", "url": "https://www.al-madina.com/ampArticle/961787"},
                 {"name": "جامعة الإمام: دليل القبول 1447", "url": "https://units.imamu.edu.sa/colleges/en/science/College_ad/Vice_Den/ViceDeanships/guides/Documents/admission%20Undergraduate%20_1447.pdf"}],
        related=[("age", "حساب العمر"), ("date-converter", "تحويل التاريخ")],
        home_desc="ثانوي وقدرات وتحصيلي بأوزان جامعتك.",
        script=js("weighted"),
    ))
    return out
