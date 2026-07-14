#!/usr/bin/env python3
"""Validate a minimal HTML body for Gmail-native rendering."""

from __future__ import annotations

import sys
from html.parser import HTMLParser
from pathlib import Path

# A sign-off legitimately uses a short <br> run (name, title, company);
# more than this in the final block means <br> is a line-wrap tool.
MAX_SIGNOFF_BR = 3


class GmailHtmlValidator(HTMLParser):
    forbidden_tags = {"pre", "table", "style", "font", "h1", "h2", "h3"}
    permitted_tags = {"div", "p", "ul", "ol", "li", "a", "strong", "em", "br"}
    void_tags = {"br"}

    def __init__(self) -> None:
        super().__init__()
        self.errors: list[str] = []
        self.root_seen = False
        self.root_closed = False
        self.stack: list[str] = []
        self.p_index = -1
        self.br_by_p: dict[int, int] = {}
        self.visible_chars = 0

    def _error(self, message: str) -> None:
        if message not in self.errors:
            self.errors.append(message)

    def _check_attrs(self, attrs: list[tuple[str, str | None]]) -> None:
        for name, _value in attrs:
            # The skill permits no inline styling at all; a keyword blacklist
            # (width/font/...) misses line-height, inline-size, and future
            # properties that recreate the narrow fixed layout.
            if name == "style":
                self._error("inline styling is not allowed; use semantic tags only")

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if not self.root_seen:
            if tag == "div" and dict(attrs).get("dir") == "ltr":
                self.root_seen = True
                self.stack.append("div")
                self._check_attrs(attrs)  # the style ban applies to the root too
                return
            self._error("body must start with a <div dir=\"ltr\"> wrapper as the sole root element")
            return
        if self.root_closed:
            self._error("content after the closing root wrapper is not allowed")
            return
        if tag in self.forbidden_tags:
            self._error(f"forbidden <{tag}> tag")
        if tag not in self.permitted_tags:
            self._error(f"unsupported <{tag}> tag")
        self._check_attrs(attrs)
        if tag == "br":
            if self.stack and "p" in self.stack:
                self.br_by_p[self.p_index] = self.br_by_p.get(self.p_index, 0) + 1
            else:
                self._error("use <p> blocks instead of <br> in prose; <br> belongs only in the final sign-off block")
            return  # void element, never pushed
        if tag in self.void_tags:
            return
        self.stack.append(tag)
        if tag == "p":
            self.p_index += 1

    def handle_endtag(self, tag: str) -> None:
        if tag in self.void_tags:
            return
        if not self.stack:
            self._error(f"stray closing </{tag}> without a matching open tag")
            return
        if self.stack[-1] != tag:
            # Email clients repair mismatched markup unpredictably, changing
            # paragraph and link boundaries after operator approval.
            self._error(f"mismatched closing </{tag}>; expected </{self.stack[-1]}>")
            return
        self.stack.pop()
        if not self.stack:
            self.root_closed = True

    def handle_data(self, data: str) -> None:
        stripped = data.strip()
        if not stripped:
            return
        if not self.root_seen or self.root_closed:
            self._error("visible text outside the root <div dir=\"ltr\"> wrapper is not allowed")
            return
        self.visible_chars += len(stripped)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_gmail_html.py EMAIL_BODY.html", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.is_file():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    parser = GmailHtmlValidator()
    parser.feed(text)
    parser.close()

    if not text.strip():
        parser.errors.append("body is empty")
    elif parser.visible_chars == 0:
        parser.errors.append("body has markup but no visible text content")
    if not parser.root_seen:
        parser.errors.append("body must start with a <div dir=\"ltr\"> wrapper")
    elif parser.stack:
        parser.errors.append(
            "unclosed tags at end of body: " + ", ".join(f"<{tag}>" for tag in reversed(parser.stack))
        )

    # <br> is permitted only in the sign-off — the final <p> block — and only
    # as a short run. Any <br> earlier in the body is hard-wrapped prose.
    last_p = parser.p_index
    for p_idx in sorted(parser.br_by_p):
        if p_idx != last_p:
            parser.errors.append(
                "use <p> blocks instead of <br> in prose; <br> belongs only in the final sign-off block"
            )
            break
    if parser.br_by_p.get(last_p, 0) > MAX_SIGNOFF_BR:
        parser.errors.append("use <p> blocks instead of repeated <br> tags")

    if parser.errors:
        for error in parser.errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(f"PASS: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
