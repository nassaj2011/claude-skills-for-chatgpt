# v0.5.0 — ChatGPT Web first-class distribution and browser verification

## Core compatibility goal

The 29 specialist skills are now distributed in **two distinct, supported forms**:

1. Native `SKILL.md` folders for Codex and compatible agent execution environments (unchanged).
2. A self-contained **ChatGPT Web Kit** for normal ChatGPT chats and Projects, with **zero Codex/CLI requirement** for end users.

In `web-kit/`:

- `CHATGPT_WEB_LIBRARY.txt` — one uploadable plain-text source containing all 29 skills.
- `CHATGPT_WEB_LIBRARY.md` — Markdown equivalent.
- `PROJECT_INSTRUCTIONS.txt` — concise source-selection rules suitable for ChatGPT Project settings.
- `cards/` — 29 fully self-contained, copy-and-paste prompts with web-specific capability boundaries.
- `index.html` — local/offline searchable library and clipboard interaction, no network/analytics/tracking.
- `README.fa.md`, `README.md` — Persian and English user instructions.

Each of the 29 card prompts includes the complete skill guidance, so a web user does not need to install another file or run a script to begin.

## Validation

- `python scripts/build_web_kit.py`: read-only verification of exact generated cards and combined library.
- `python -m unittest discover -s tests -v`: validates 29 cards, project instruction boundaries, embedded JSON, no external script dependency and content sync with the source.
- `python web-kit/browser_smoke.py`: real local Microsoft Edge test of RTL 29-card index, search, clipboard, reset, JavaScript errors and external requests.
- `python web-kit/browser_smoke.py --file-mode`: same checks against directly opened offline file, not only loopback server.
- `python examples/frontend-rtl/browser_smoke.py`: real browser testing discovered and corrected an ID collision in the reset button. Checks include invalid/valid booking, reset focus and 320/390px horizontal overflow.
- `evals/prompts/v05-release.txt` and `evals/prompts/v05-privacy.txt`: additional **prepared but not executed** evaluation prompts. No model performance claim is made for them.

The browser tests are local optional smoke checks because installing Playwright browsers during every CI run would increase dependencies; CI validates the generated kit and its testable source. The performed browser test is **not an authenticated ChatGPT Project integration test**.

## Operational safety and limits

- Plain prompt instructions never claim access to shell, private code, CI, GitHub or real system mutations.
- Web-facing guidance must mark checks NOT EXECUTED when missing tools or execution evidence.
- The offline selector does not send usernames, code, prompts or telemetry to the publisher.
- Users' own ChatGPT uploads are handled by ChatGPT under their account/workspace privacy and data controls.
- Uploading a text library to ChatGPT Projects is **not** native Agent Skills installation. Project context retrieval and automatic skill choice are not guaranteed for every turn. Explicitly name the specialist for high-impact work.
- Neither end-to-end agent auto-routing across all 29 skills nor production readiness is certified. Earlier measured A/B evidence remains exploratory.

Official ChatGPT docs:
- https://help.openai.com/en/articles/10169521-projects-in-chatgpt
- https://help.openai.com/en/articles/8555545-uploading-files-and-audio-to-chatgpt
- https://help.openai.com/en/articles/8554397-gpts

Repository: https://github.com/nassaj2011/claude-skills-for-chatgpt
