# Localization Readiness Checklist

Research date: 2026-05-18

Purpose: catch design failures that appear when UI leaves English, Latin-only
type, left-to-right layout, US dates, and short labels.

Primary sources:

- W3C internationalization: https://www.w3.org/International/
- W3C language tags: https://www.w3.org/International/articles/language-tags/index.en
- W3C right-to-left HTML guidance: https://www.w3.org/International/questions/qa-html-dir
- W3C i18n quick tips: https://www.w3.org/International/quicktips/index
- web.dev internationalization: https://web.dev/learn/design/internationalization/
- MDN logical properties: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values
- FormatJS: https://formatjs.io/
- next-intl: https://next-intl.dev/

## Rules

- Use `lang` and `dir` when language/direction is known.
- Use logical properties (`inline-start`, `margin-inline`, etc.) for layouts
  that may support RTL.
- Do not assemble dates, times, currencies, numbers, phone numbers, or addresses
  by hand when locale-aware formatters exist.
- Do not assume first/last name order, address shape, plural rules, or calendar
  conventions are universal.
- Keep labels visible; placeholders are not localization-safe labels.
- Leave room for translated strings and taller scripts.
- Define what mirrors in RTL and what does not: directional icons usually mirror;
  media controls, clocks, charts, maps, logos, and physical objects usually do
  not automatically mirror.
- Mixed-language strings need string-level language/direction metadata when
  needed for correct display.

## Packet Fields

- supported_locales:
- required_scripts:
- default_language:
- text_direction:
- locale_formatting_owner:
- date_time_currency_rules:
- name_address_rules:
- pluralization_rules:
- rtl_support_needed:
- logical_properties_needed:
- mirror_policy:
- translation_expansion_risk:
- fallback_fonts:

## Done Gate

- `lang`/`dir` plan exists when relevant.
- Long translated strings do not break layout.
- Date/number/currency formatting is locale-safe.
- RTL behavior is defined or explicitly out of scope.
- Font fallback supports required scripts.
