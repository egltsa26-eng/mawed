# موعد: weekly upkeep

Site: https://egltsa26-eng.github.io/mawed/ is built from this repo. Every push to `main` rebuilds the site and publishes it to the `gh-pages` branch through GitHub Actions (`.github/workflows/deploy.yml`). A scheduled Claude task follows this file once a week.

## Where the dates live

| File | What it holds |
|---|---|
| `src/payments.py` | Rules for government salaries (27th), Citizen Account (10th), Developed Social Security (1st), GOSI pensions (1st). `OVERRIDES` = announced dates that differ from a rule. `PENDING` = the rule date falls in a holiday and no announcement exists yet. |
| `src/occasions.py` | Eid holiday rules, Founding Day and National Day text, the school calendar (`SCHOOL_BREAKS`). |
| `src/programs.py` | Ramadan and Eid pages (Umm al-Qura dates come from `hijri-converter`). |
| `src/content.py` | `REVIEWED_TEXT` (shown in the footer), `ADSENSE_CLIENT`, and `SEARCH_CONSOLE_FILES` (Google ownership file; never remove it). |

## Each run

1. Look for official changes since the last run:
   - Ministry of Finance payroll calendar: `https://www.mof.gov.sa/mediacenter/Payroll/Pages/<YEAR>.aspx` for this year and next. Any date that differs from the rule goes into `OVERRIDES` as `("salary", y, m): (date, "<short Arabic reason>")`.
   - Citizen Account (حساب المواطن): the announced date of the next batch. Add an `OVERRIDES` entry `("citizen", y, m)` if it differs, and remove the matching `PENDING` entry once an announcement exists.
   - Developed Social Security (الضمان الاجتماعي المطور) and GOSI pensions (معاشات التقاعد): next month's payment date (`"social"` / `"pension"` keys).
   - Within 10 days of 29 Sha'ban, 29 Ramadan or 29 Dhu al-Qa'dah (Umm al-Qura): the Supreme Court moon-sighting announcement. If the official start differs from Umm al-Qura, say so on the Ramadan or Eid page text; never change the calendar engine.
   - Ministry of Education calendar changes, and from May 2027 the 1449 school calendar once it is published.
2. Trust `*.gov.sa` and `spa.gov.sa`; otherwise require two reputable Saudi outlets that agree (okaz.com.sa, sabq.org, ajel.sa, alyaum.com, al-madina.com).
3. Change only what a source confirms, and put the source URLs in the commit message.
4. Set `REVIEWED_TEXT` in `src/content.py` to today's Riyadh date in Arabic, for example `26 أكتوبر 2026`. This also guarantees one rebuild a week, which refreshes page titles.
5. `python3 tools/build.py && python3 tools/test_calcs.py`. Never push when either fails; revert your own edits and report instead.
6. Commit, push to `main`, and confirm the "Build and publish" run for that commit succeeded.

## Never

Change the design or add pages unless the owner asks; touch other repositories or other projects' data; delete anything; log in, pay, or post on social media.

## Later switches

- **Custom domain bought** (planned: `mawedsa.com` through WordPress.com): in `tools/build.py` set `HOST = "https://mawedsa.com"` and `BASE = ""`, and have the build write `dist/CNAME` containing the domain. Point DNS to GitHub Pages (A records 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153 and `www` CNAME `egltsa26-eng.github.io`).
- **AdSense approved**: set `ADSENSE_CLIENT = "ca-pub-…"` in `src/content.py`. The build then adds the AdSense script, fills the ad slots and writes `ads.txt` (which only works at a domain root, so after the custom domain).
