# Typography And Cultural System

Research date: 2026-05-18

Purpose: make typography a first-class design decision. Use this when choosing
fonts, type scale, line length, localization behavior, multilingual support,
right-to-left support, culturally specific visual tone, or no-reference design
direction.

## Primary Sources

| Source | URL | Use |
| --- | --- | --- |
| Apple HIG Typography | https://developer.apple.com/design/human-interface-guidelines/typography | Platform typography, legibility, hierarchy, optical sizes, and avoiding too many typefaces. |
| Material Design typography | https://m3.material.io/styles/typography | Semantic type roles and scalable type systems for product UI. |
| Carbon typography | https://carbondesignsystem.com/elements/typography/overview/ | Productive vs expressive type sets, type tokens, and enterprise hierarchy. |
| Atlassian typography/content | https://atlassian.design/foundations/typography/applying-typography | App UI typography, content clarity, and token-backed text styles. |
| Practical Typography | https://practicaltypography.com/ | Readability, line length, point size, and professional type discipline. |
| Google Fonts FAQ | https://developers.google.com/fonts/faq | Language filters, variable fonts, and Google Fonts usage boundaries. |
| Noto docs | https://notofonts.github.io/noto-docs/website/use/ | Script-specific Noto guidance and UI/document font choices. |
| Fontsource | https://fontsource.org/docs/getting-started | Self-hosted open-source fonts for privacy/performance and subsets. |
| Typewolf | https://www.typewolf.com/ | Real-world font pairing and type inspiration. |
| W3C i18n text layout checklist | https://w3c.github.io/typography/gap-analysis/ | Script and language layout requirements across writing systems. |
| web.dev internationalization | https://web.dev/learn/design/internationalization/ | `lang`, `dir`, text expansion, line-height, and international design basics. |
| W3C RTL guidance | https://w3c.github.io/i18n-drafts/questions/qa-html-dir.en | Structural right-to-left markup and logical direction rules. |

## Typography Decision Order

1. Identify product role: dense product, editorial site, luxury brand,
   developer tool, finance/reporting, consumer/mobile, AI workspace, or
   global/multilingual product.
2. Identify script/language needs: Latin-only, extended Latin, Cyrillic, Greek,
   CJK, Arabic, Hebrew, Indic scripts, Thai, Vietnamese, mixed script, or unknown.
3. Pick type posture: neutral UI, humanist, geometric, grotesk, serif-led,
   editorial, technical mono, rounded/warm, luxury/high-contrast, playful,
   compact/dense, or multilingual-safe.
4. Pick source and delivery: system stack, Google Fonts, Fontsource self-hosted,
   local brand font, Noto/Source Han fallback, or repo-existing font.
5. Define roles: display, heading, body, label, caption, code/mono, numeric.
6. Define scale: base size, line height, weights, max line length, and mobile
   adjustments.
7. Define fallback stack and script fallbacks.
8. Stress test long content, translated strings, numerals, dates, and 200% text.

## Product Typography Recipes

| Product type | Typography posture | Good fits | Avoid |
| --- | --- | --- | --- |
| Dense SaaS/admin/CRM | Neutral or humanist UI sans, compact labels, strong weights | Inter, IBM Plex Sans, Source Sans 3, Noto Sans, system UI | expressive display fonts in data grids |
| Finance/billing/reports | Precise sans plus tabular numbers; optional restrained serif for editorial surfaces | IBM Plex Sans, Roboto Flex, Source Sans 3, Noto Sans, IBM Plex Mono | playful rounded fonts, weak numeric alignment |
| AI command center | Neutral UI sans plus mono/code for tool state and receipts | Inter, Geist, IBM Plex Sans/Mono, JetBrains Mono, Noto Sans | sci-fi novelty fonts, unreadable glow text |
| Developer/API/docs | Sans plus real mono; high code readability | IBM Plex Sans/Mono, Source Sans 3, Source Code Pro, JetBrains Mono, Fira Code | decorative display fonts in docs/code |
| Editorial SaaS/marketing | Sans + serif or expressive display with readable body | Fraunces + Inter, Libre Baskerville + Source Sans 3, DM Sans + Newsreader | too many typefaces, low-contrast thin weights |
| Luxury/minimal | High-control serif/display with quiet sans body | Cormorant Garamond + Manrope, Playfair Display + Source Sans 3, Instrument Serif + Inter | cramped type, overused all-caps, poor mobile line length |
| Warm services/health/education | Humanist/rounded sans with generous line height | Nunito Sans, Atkinson Hyperlegible, Noto Sans, Open Sans, Source Sans 3 | cold mono-heavy systems |
| Mobile-native web app | System UI or highly legible UI sans; larger tap labels | system-ui, SF/Roboto stack, Inter, Noto Sans | tiny captions, thin weights, custom fonts that load late |
| Multilingual/global app | Noto/Source Han/script-specific fallback first | Noto Sans/Serif, Noto Sans CJK, Noto Naskh Arabic, Noto Sans Devanagari, system fallbacks | Latin-only brand fonts without fallback |
| Cultural/localized campaign | Script-aware, locally appropriate font choice based on language and audience | Noto families, local brand-approved fonts, Source Han for CJK | assuming a Latin font or color meaning maps globally |

## Font Source Rules

- Prefer existing repo/brand fonts when they are readable, licensed, and
  support the needed languages.
- Use system fonts for fast native-feeling app UI when brand typography is not
  the point.
- Use Fontsource/self-hosting when privacy, performance, offline use, or build
  control matters.
- Use Google Fonts for broad accessible web choices, but inspect language
  support and font loading behavior.
- Use Noto or Source Han fallbacks when multilingual/script support matters.
- Use variable fonts when weight/width flexibility improves hierarchy without
  loading many files.
- Keep typefaces limited: usually one UI family plus optional display/accent and
  mono. More than that needs a strong brand reason.

## Cultural And Localization Rules

- Do not assume color meanings are universal. Explain color by product job,
  local expectations, semantic role, and contrast.
- Leave room for text expansion. English is often shorter than translated UI.
- Define `lang` and `dir` when language/direction is known.
- Use logical CSS properties (`inline-start`, `margin-inline`, etc.) for layouts
  that may support right-to-left languages.
- Mirror layout only when the product and platform convention support it; do
  not mirror logos, media, charts, or maps blindly.
- Dates, times, currencies, phone numbers, addresses, and names must be
  locale-aware when the product is international.
- Avoid idioms, puns, culture-specific metaphors, and unlabeled icons in
  important UI copy.
- Check line height for accents, diacritics, Arabic, Devanagari, Thai, and other
  scripts that need more vertical room.
- If a font does not support the target script, do not fake it with browser
  fallback alone; choose a deliberate fallback stack and test it.

## Typography Visual Integrity

- Body text should be readable before it is stylish.
- Control line length; broad rule: body copy often works best around 45-90
  characters per line, tighter for dense UI and wider only with care.
- Avoid negative letter spacing in UI text unless a brand system explicitly
  requires it for large display type.
- Do not use thin/light weights for small text.
- Do not truncate critical labels, prices, statuses, warnings, or legal
  commitments without a reveal path.
- Use tabular numbers for financial tables, dashboards, invoices, and aligned
  numeric comparisons when available.
- Check headings at mobile widths; large display type must not crush the first
  usable action.

## Packet Fields To Fill

- typography_posture:
- font_source:
- primary_font:
- secondary_or_display_font:
- mono_font:
- script_language_support:
- fallback_stack:
- type_scale:
- max_line_length:
- numeric_style:
- localization_expansion_rule:
- rtl_support_needed:
- cultural_notes:
- typography_stress_cases:
