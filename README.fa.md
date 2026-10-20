# مهارت‌های کلاد برای چت‌جی‌پی‌تی

### مجموعه متن‌باز اسکیل‌های ساخت پلتفرم از ایده تا محیط تولید

[English](README.md) · [نقشه گردش کار](docs/WORKFLOW.md) · [مقایسه با Anthropic](docs/ANTHROPIC_COMPARISON.md)

این مخزن شامل **۲۲ اسکیل اصیل و قابل‌استفاده مجدد** برای عامل‌های برنامه‌نویسی مبتنی بر استاندارد `SKILL.md` است: از کشف نیاز و طراحی محصول تا معماری، UX، برنامه‌نویسی، دیباگ، تست، استقرار و مانیتورینگ.

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
| توسعه اسکیل‌های جدید | `skill-authoring-toolkit` |

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

نصب‌کننده به‌صورت پیش‌فرض فقط پیش‌نمایش نشان می‌دهد و **هیچ فایل موجودی را جایگزین نمی‌کند**.

## استفاده در ChatGPT

توجه: صرفاً Clone کردن GitHub، اسکیل را به‌صورت سراسری در حساب ChatGPT نصب نمی‌کند. امکانات بارگذاری Skill بسته به محصول و حساب متفاوت است. می‌توان متن `SKILL.md` مرتبط را در دستورالعمل‌های یک پروژه/عامل قرار داد یا در Codex و محیط‌های سازگار استفاده کرد.

## شروع کار

برای نمونه عملی گام‌به‌گام، فایل [ساخت پلتفرم رزرو فرضی](examples/from-idea-to-production.md) را بخوانید؛ این مثال از پروژه‌های خصوصی واقعی استفاده نمی‌کند.

برای اعتبارسنجی:

```bash
python scripts/validate_skills.py
python -m unittest discover -s tests -v
```

## مشارکت و مجوز

مشارکت از طریق Issue و Pull Request آزاد است. قواعد در [CONTRIBUTING.md](CONTRIBUTING.md) نوشته شده‌اند. متن اصلی این مخزن با مجوز [MIT](LICENSE) منتشر می‌شود. مجوز فایل‌های مخازن دیگر ممکن است متفاوت باشد و پیش از کپی باید بررسی شود.

**وضعیت:** نسخه اولیه ۰٫۱؛ آزمون ساختار مهارت‌ها موجود است، اما تأیید عملیاتی همه مهارت‌ها روی پروژه واقعی ادعا نمی‌شود.
