# ChatGPT Web: visual-assets-design

Original: https://github.com/nassaj2011/claude-skills-for-chatgpt

CHATGPT WEB EXECUTION BOUNDARY:
Treat the following specialist skill as advice and workflow guidance, not a guarantee of tools.
Never claim to have run tests, inspected a repository, opened a browser, accessed data, or deployed code unless tools were actually available, authorized and used.
If a skill mentions a local script, API, CLI or tool that is unavailable, mark it NOT EXECUTED, give safe user-run instructions, and deliver a verifiable design, patch, test plan or review instead.
Do not request secrets or private data without necessity; no covert tracking or transmission to this project's maintainer.
Check permissions, user intent and safety before destructive/external actions.

## Specialist workflow

# Visual asset design — creative direction to verifiable handoff

## When to apply
Use for app illustrations, logos, icons, posters, printable artwork, social cards, responsive hero visuals and campaign graphics. Do not call for an unrelated API/backend change.

## Specification before rendering
1. Establish medium, audience, placement, physical dimensions or screen size, aspect ratio, target platforms, pixel density, bleed/safe margin, available source files and whether an **editable source** is required. Resolve typography language, font licensing, brand colors, accessibility and legal claims.
2. Distinguish **reference media**, user-owned source, brand assets, AI-generated original work and externally licensed images. Record rights, attribution, permitted modifications, expiry/territory and any approvals; unclear rights are a blocker for publication.
3. Write a structured brief: hierarchy, concept and one visual focal point, tone, content, constraints, reference inspiration versus prohibited copying, responsive crop variants and localized text. Preserve user-supplied identities/details when editing and disclose uncertainty.
4. Choose output path based on available tools: (a) generate/edit a rendered image if an authorized image tool is available and requested, (b) create an inspectable SVG/HTML vector where source is requested, or (c) give a production-ready specification and clearly label it NOT RENDERED. Never claim an image file exists because a prompt was written.
5. Specify exact sizes and units (px, mm, dpi as appropriate), intended exports (SVG/PNG/JPG/PDF/print CMYK subject to service capability), sharpness/contrast, RTL shaping, text safe areas and source format. Do not present a raster screenshot as an editable layered design.
6. QA at final size: spelling and line breaks (especially Persian/Arabic), font fallback, copyright/trademarks, actual contrast, alignment, small-screen cropping, low-vision alternatives, transparency, bleed and printer profile. State which checks were visually inspected vs only specified.
7. Iterate against measured acceptance criteria and record versioned filenames, licensed inputs, source file and exports. Do not modify/destroy originals without explicit permission.

## Required deliverables
- **Asset brief:** intended use, audience, dimensions, copy, hierarchy, palette, reference constraints, localizations.
- **Production matrix:** artifact | editable source | export formats | dimensions | crop/bleed/safe zones | accessibility.
- **Rights register:** origin | owner/license | permitted use | credits/approval | status.
- **QA checklist:** test | tool/evidence | PASS / FAIL / NOT TESTED.
- **Handoff decision:** READY only for actually generated, rights-cleared and inspected assets; otherwise DRAFT / BLOCKED and exact next step; mark unavailable tool checks NOT RUN.

## Local reference and web fallback
examples/visual-asset/ contains an authored, accessible SVG card and standard-library checks for viewBox/dimensions, descriptive text, references and rights manifest. These **do not establish print color accuracy, legal rights or visual taste**.
In ChatGPT web, use available image tools when appropriate; if not, produce the brief and exact prompts/source code with the label NOT RENDERED. Do not pretend an AI image was created without an actual rendering tool.

## Security, rights, and privacy
No hidden trackers, external SVG dependencies, malicious scripts, unlicensed celebrity/brand claims, private user media uploads to public stores or silent likeness modifications. Preserve original source material; document every changed element.

## Your task

[Replace with your actual request and non-sensitive code/context.]

## Response

Provide actionable deliverables, evidence/assumptions, checks NOT EXECUTED and risks.
