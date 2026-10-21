# مهارت‌های کلاد برای چت‌جی‌پی‌تی

### مجموعه متن‌باز اسکیل‌های ساخت پلتفرم از ایده تا محیط تولید

[English](README.md) · [نقشه گردش کار](docs/WORKFLOW.md) · [تقویت نسخه ۰٫۳](docs/V0_3_RELEASE.md) · [حریم خصوصی و منشأ انتشار](docs/PROVENANCE_AND_PRIVACY.md) · [ارزیابی اسکیل‌ها](evals/README.md) · [مقایسه با Anthropic](docs/ANTHROPIC_COMPARISON.md)

این مخزن شامل **۲۹ اسکیل اصیل و قابل‌استفاده مجدد** برای عامل‌های برنامه‌نویسی مبتنی بر استاندارد `SKILL.md` است: از کشف نیاز و طراحی محصول تا معماری، UX، برنامه‌نویسی، دیباگ، تست، استقرار و مانیتورینگ.

> **این پروژه مستقل و اجتماعی است.** از ایده و رویکرد [Anthropic Skills](https://github.com/anthropics/skills) الهام می‌گیرد، اما محصول رسمی، ترجمه تحت حمایت یا وابسته به Anthropic یا OpenAI نیست. متن اسکیل‌ها اختصاصاً برای این پروژه نوشته شده و کپی فایل‌های اصلی Claude نیست.

## هدف

تفاوت اصلی با فهرست‌های حجیم اسکیل این است که مهارت‌ها یک **فرایند تحویل نرم‌افزار با تحویل‌دادنی، وابستگی و معیار پذیرش** می‌سازند. یک اسکیل به‌تنهایی کد را اجرا، تست را پاس یا محصول را منتشر نمی‌کند؛ این عملیات به ابزار و مجوز واقعی عامل نیاز دارد.

## بخش‌های پوشش‌داده‌شده

| مرحله | مهارت‌ها |
| --- | --- |
| کشف و برنامه‌ریزی | `product-business-analyst`، `technical-project-orchestrator` |
| معماری و داده | `software-architect`، `database-transaction-integrity` |
| امنیت و حریم خصوصی | `security-authorization-auditor`، `privacy-data-governance` |
| طراحی بصری | `frontend-design-direction`، `theme-design-system`، `visual-assets-design` |
| توسعه وب | `react-artifacts-builder`، `backend-api-engineer`، `performance-accessibility` |
| API و یکپارچه‌سازی | `mcp-integration-builder`، `llm-api-integration` |
| عیب‌یابی و آزمون | `backend-debugging`، `playwright-webapp-testing`، `qa-test-strategy` |
| تحویل و بهره‌برداری | `devops-ci-cd`، `qa-release-gatekeeper`، `observability-monitoring`، `documentation-handover` |
| توسعه و ارزیابی اسکیل | `skill-authoring-toolkit`، `skill-evaluation-benchmark` |
| بازبینی و امنیت توسعه | `code-review-pr`، `agent-skill-security-auditor`، `dependency-supply-chain-auditor` |
| بازیابی، ظرفیت و راه‌اندازی | `backup-disaster-recovery`، `load-resilience-testing`، `project-bootstrap-environments` |

## استفاده سریع در ChatGPT وب (بدون نصب)

۱. [کتابخانه ۲۹ مهارت در قالب TXT](web-kit/CHATGPT_WEB_LIBRARY.txt) را در ChatGPT وب پیوست کنید.

۲. در صورت استفاده از Projects، [دستورالعمل آماده پروژه](web-kit/PROJECT_INSTRUCTIONS.txt) را در بخش Project settings بگذارید.

۳. یا [انتخاب‌گر آفلاین](web-kit/index.html) را دانلود و باز کنید و یک پرامپت را کپی کنید. [راهنمای کامل فارسی](web-kit/README.fa.md) را بخوانید.

این قابلیت برای کاربر وب است و احتیاجی به Codex یا اجرای فایل Python ندارد. دسترسی به ابزارها و اجرای واقعی کد همچنان تابع امکانات و مجوزهای هر گفت‌وگو است.

## نصب در Codex

```bash
git clone https://github.com/nassaj2011/claude-skills-for-chatgpt.git
cd claude-skills-for-chatgpt
python scripts/install.py --target ~/.agents/skills
python scripts/install.py --target ~/.agents/skills --apply
```

در PowerShell ویندوز:

```powershell
python .\scripts\install.py --target "$env:USERPROFILE\.agents\skills" --apply
```

اگر `CODEX_HOME` به مسیر سفارشی اشاره می‌کند، می‌توانید `"$env:CODEX_HOME\skills"` را به‌عنوان هدف بدهید. برای نصب مختص یک مخزن نیز پوشه `.agents/skills` همان مخزن را انتخاب کنید.

نصب‌کننده به‌صورت پیش‌فرض فقط پیش‌نمایش نشان می‌دهد و **هیچ فایل موجودی را جایگزین نمی‌کند**؛ پیش از نصب، اسکن امنیتی ایستا انجام می‌شود. نتیجه پاک این اسکن به معنی تضمین ایمنی نیست.

## استفاده در نسخه وب ChatGPT — بدون Codex

نسخه مخصوص مرورگر: [راهنمای فارسی](web-kit/README.fa.md) · [کتابخانه یک‌فایلی TXT](web-kit/CHATGPT_WEB_LIBRARY.txt) · [دستورالعمل آماده Projects](web-kit/PROJECT_INSTRUCTIONS.txt) · [انتخاب‌گر آفلاین ۲۹ مهارت](web-kit/index.html).

**چت معمولی:** فایل TXT را پیوست کنید یا پرامپت اسکیل موردنظر را از فایل HTML کپی کنید و سپس مسئله خود را بنویسید.

**ChatGPT Projects:** فایل TXT را به منابع پروژه اضافه کنید و متن Project Instructions را در تنظیمات پروژه بگذارید. نصب ترمینالی یا Codex لازم نیست. این مسیر با نصب بومی Agent Skills یکسان نیست و اجرای کد/دسترسی به مخزن فقط در صورت وجود و مجوز ابزار مربوطه ممکن است.

## شروع کار

برای نمونه عملی گام‌به‌گام، فایل [ساخت پلتفرم رزرو فرضی](examples/from-idea-to-production.md) را بخوانید؛ این مثال از پروژه‌های خصوصی واقعی استفاده نمی‌کند.

برای اعتبارسنجی:

```bash
python scripts/validate_skills.py
python scripts/audit_skills.py --root skills --fail-on review
python scripts/provenance.py
python -m unittest discover -s tests -v
```

## مشارکت و مجوز

مشارکت از طریق Issue و Pull Request آزاد است. قواعد در [CONTRIBUTING.md](CONTRIBUTING.md) نوشته شده‌اند. متن اصلی این مخزن با مجوز [MIT](LICENSE) منتشر می‌شود. مجوز فایل‌های مخازن دیگر ممکن است متفاوت باشد و پیش از کپی باید بررسی شود.

**وضعیت:** نسخه ۰٫۷؛ اعتبارسنجی ساختار، اسکن امنیتی محدود پیش از نصب، چارچوب ارزیابی A/B و تست‌های خودکار اضافه شده است. بهبود عملکرد همه اسکیل‌ها روی پروژه واقعی هنوز اثبات نشده است.

### نسخه ۰٫۲: امنیت، ابزارهای اجرایی و ارزیابی واقعی

هفت اسکیل جدید و ابزارهای ممیزی امنیت پیش از نصب، بررسی PR، کنترل یکپارچگی فایل پشتیبان و امتیازدهی مقایسه‌ای اضافه شدند. [تغییرات نسخه](docs/V0_2_RELEASE.md)، [پروتکل آزمون](evals/README.md) و [اولین آزمایش واقعی مدل](evals/PILOT_RESULT.md) منتشر شده‌اند. در آزمایش یک سناریوی PR، امتیاز بدون اسکیل و با دستورالعمل اسکیل هر دو ۱۰۰٪ بود؛ بنابراین **بهبود قابل‌اثباتی در این نمونه دیده نشد** و این نتیجه به کل ۲۹ اسکیل قابل تعمیم نیست.

### نسخه ۰٫۳: منشأ قابل بررسی، حریم خصوصی و نصب سخت‌گیرانه

[سیاست امنیت و حریم خصوصی](docs/PROVENANCE_AND_PRIVACY.md) و [تغییرات نسخه ۰٫۳](docs/V0_3_RELEASE.md) منتشر شدند. فایل [CATALOG.json](CATALOG.json) شامل هش SHA-256 اسکیل‌های عمومی و نشانی مخزن رسمی است؛ این هش‌ها به‌تنهایی امضای دیجیتال معتبر ناشر نیستند.

```bash
python scripts/provenance.py
python scripts/audit_skills.py --root skills --fail-on review
python scripts/install.py --target ~/.agents/skills --only code-review-pr
python scripts/install.py --target ~/.agents/skills --only code-review-pr --apply
```

نصب‌کننده فایل‌های موجود را جایگزین نمی‌کند و هنگام یافتن مورد مشکوک نصب را متوقف می‌کند؛ پس از بررسی دستی، فقط برای موارد REVIEW می‌توان با `--accept-review` نصب را تأیید کرد. ثبت رسید محلی با `--receipt` اختیاری است، هیچ گزارشی آپلود نمی‌شود و شناسه کاربران یا کدهای تولیدشده جمع‌آوری نمی‌شود. اسکریپت‌های اجرایی در نسخه منبع GitHub هستند و با نصب صرف فایل SKILL.md منتقل نمی‌شوند.

### نسخه ۰٫۴: نمونه‌های اجرایی و ارزیابی قابل بازتولید

- [گزارش تغییرات v0.4](docs/V0_4_RELEASE.md): نمونه رزرو تراکنشی با SQLite، رابط RTL فارسی و گیت آفلاین معیارهای سرویس.
- [سناریوهای مستقل ۲۹ اسکیل](evals/29-skill-benchmark.json): هر کدام مسئله، معیار پذیرش و شرط عدم فعال‌سازی دارند. این فایل به معنای اجرای تمام سناریوها نیست.
- [دو مقایسه واقعی جدید با Codex](evals/V0_4_RESULTS.md): در دو مسئله ساختگی دیتابیس و امنیت، دستورالعمل اسکیل پاسخ تخصصی کامل‌تری ایجاد کرد. آزمایش‌ها تک‌نمونه‌ای و فاقد داوری کور بوده‌اند؛ هیچ ادعای افزایش عمومی ۳۰٫۸ درصدی کیفیت یا رسیدن تمام اسکیل‌ها به ۸٫۵ از ۱۰ مطرح نیست.

اجرای `python scripts/validate_benchmark.py` و تست‌های مثال‌های عملی پیش از مشارکت پیشنهاد می‌شود. این نمونه‌ها به هیچ حساب کاربری واقعی، سامانه تولیدی یا داده خصوصی دسترسی ندارند.

### نسخه ۰٫۶: تقویت کیفیت سه اسکیل تخصصی

سه مهارت [حریم خصوصی داده](skills/privacy-data-governance/SKILL.md)، [آزمون بار و تاب‌آوری](skills/load-resilience-testing/SKILL.md) و [طراحی دارایی بصری](skills/visual-assets-design/SKILL.md) بازنویسی و به نمونه‌های **قابل‌اجرا و دارای آزمون** مجهز شدند.

برای کاربران ChatGPT وب، همان متن‌های تقویت‌شده به‌طور خودکار در [کتابخانه یک‌فایلی](web-kit/CHATGPT_WEB_LIBRARY.txt) و [۲۹ پرامپت مستقل](web-kit/cards/) قرار گرفتند؛ نصب Codex لازم نیست.

[جزئیات نسخه ۰٫۶](docs/V0_6_RELEASE.md) · [شواهد و محدودیت آزمون‌ها](evals/V0_6_RESULTS.md)

در این نسخه به‌دلیل خطای ۴۰۴ سرویس Codex، مقایسه واقعی جدید «با اسکیل / بدون اسکیل» به نتیجه نرسید و **امتیاز عملکرد جدیدی ادعا نمی‌کنیم**.

### نسخه ۰٫۷: تقویت شش مهارت دیگر

اسکیل‌های **LLM API Integration، MCP Integration Builder، DevOps CI/CD، Dependency Supply Chain، Backup Disaster Recovery و Performance Accessibility** با قراردادهای فنی دقیق‌تر، آزمون منفی و نمونه‌های اجرایی ارتقا یافتند.

برای هر شش حوزه، یک اجرای واقعی Codex با اسکیل و یک اجرا بدون اسکیل ذخیره شده است: **۱۲ خروجی قابل بازبینی** با شناسه اجرا و هش. [گزارش شواهد](evals/V0_7_RESULTS.md) و [شرح نسخه](docs/V0_7_RELEASE.md).

این شواهد هنوز **داوری مستقل و امتیازدهی کور ندارند**؛ به همین دلیل افزایش قطعی امتیاز یا رسیدن مجموعه به ۸٫۵ را ادعا نمی‌کنیم. تمام اصلاحات در [بسته مخصوص ChatGPT وب](web-kit/CHATGPT_WEB_LIBRARY.txt) نیز اعمال می‌شوند.

### نسخه ۰٫۷: تقویت شش مهارت دیگر

اسکیل‌های **LLM API Integration، MCP Integration Builder، DevOps CI/CD، Dependency Supply Chain، Backup Disaster Recovery و Performance Accessibility** با قراردادهای فنی دقیق‌تر، آزمون منفی و نمونه‌های اجرایی تقویت شدند.

برای هر شش حوزه یک اجرای واقعی Codex با اسکیل و یک اجرا بدون اسکیل ذخیره شده است: **۱۲ خروجی قابل بازبینی** با شناسه اجرا و هش. [گزارش شواهد](evals/V0_7_RESULTS.md) و [شرح نسخه](docs/V0_7_RELEASE.md).

این شواهد هنوز **داوری مستقل و امتیازدهی کور ندارند**؛ بنابراین افزایش قطعی امتیاز یا رسیدن مجموعه به ۸٫۵ ادعا نمی‌شود. اصلاحات در [بسته مخصوص ChatGPT وب](web-kit/CHATGPT_WEB_LIBRARY.txt) نیز اعمال می‌شوند.

### نسخه آزمایشی ۰٫۸ — آزمون سه‌گروهی با گروه کنترل

[بانک ۸۷ سناریویی](evals/v08/heldout_87.json) برای ۲۹ اسکیل (۳ سناریو برای هر کدام) آماده شده است. [گزارش اجرای واقعی](evals/v08/PILOT_REPORT.md) سه مسئله کدنویسی با گروه‌های بدون اسکیل، راهنمای عمومی هم‌طول و اسکیل تخصصی را مستند می‌کند. **نتیجه پایلوت: ۲۹/۳۲، ۳۲/۳۲ و ۳۲/۳۲.** در این نمونه کوچک، اسکیل تخصصی نسبت به راهنمای عمومی مزیت مشاهده‌شده ندارد. ۸۴ سناریوی دیگر اجرا نشده‌اند و امتیاز هدف ۸٫۵ اثبات نشده است.

### آزمون دشوارتر نسخه ۰٫۹ — توازن توکن و تکرار

[گزارش آزمایش](evals/v09/RESULTS.md): سه مسئله سخت‌تر، سه گروه، دو تکرار مستقل و ۷۵ آزمون ساختگی. **بدون اسکیل: ۱۴۸/۱۵۰؛ راهنمای عمومی هم‌تعداد توکن: ۱۴۹/۱۵۰؛ اسکیل تخصصی: ۱۴۹/۱۵۰.** مزیت اختصاصی اسکیل‌ها در این آزمون مشاهده نشد؛ نتیجه برای کل ۲۹ مهارت قابل تعمیم نیست و نسخه اصلی اسکیل‌ها تغییری نکرده است.
