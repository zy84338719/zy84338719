#!/usr/bin/env python3
"""Rewrite README stats-card accent colors based on Beijing time of day."""

from __future__ import annotations

import datetime as dt
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

README = Path(__file__).resolve().parents[1] / "README.md"
MARKER_START = "<!-- STATS_CARDS:theme-sync:start -->"
MARKER_END = "<!-- STATS_CARDS:theme-sync:end -->"

# Palettes keep the vue light-card base; only accents shift with the clock.
# accent: headings / icons / streak numbers   fire: streak flame
PALETTES = {
    "dawn": {"accent": "3AA675", "fire": "E8A23A"},  # 05-009 soft mint
    "day": {"accent": "41B883", "fire": "E25822"},  # 10-16 brand green
    "dusk": {"accent": "D97B29", "fire": "E25822"},  # 17-20 amber
    "night": {"accent": "6C5CE7", "fire": "E25822"},  # 21-04 violet
}


def period_for(hour: int) -> str:
    if 5 <= hour < 10:
        return "dawn"
    if 10 <= hour < 17:
        return "day"
    if 17 <= hour < 21:
        return "dusk"
    return "night"


def extract_block(text: str) -> tuple[str, str, str]:
    try:
        start = text.index(MARKER_START)
        end = text.index(MARKER_END) + len(MARKER_END)
    except ValueError as exc:
        raise SystemExit(f"markers not found in {README}") from exc
    return text[:start], text[start:end], text[end:]


def recolor(block: str, accent: str, fire: str) -> str:
    # github-readme-stats / pin / top-langs
    block = re.sub(r"(title_color=)[0-9a-fA-F]{6}", rf"\g<1>{accent}", block)
    block = re.sub(r"(icon_color=)[0-9a-fA-F]{6}", rf"\g<1>{accent}", block)
    # streak-stats
    block = re.sub(r"(ring=)[0-9a-fA-F]{6}", rf"\g<1>{accent}", block)
    block = re.sub(r"(currStreakNum=)[0-9a-fA-F]{6}", rf"\g<1>{accent}", block)
    block = re.sub(r"(sideNums=)[0-9a-fA-F]{6}", rf"\g<1>{accent}", block)
    block = re.sub(r"(fire=)[0-9a-fA-F]{6}", rf"\g<1>{fire}", block)
    return block


def main() -> int:
    now = dt.datetime.now(ZoneInfo("Asia/Shanghai"))
    period = period_for(now.hour)
    palette = PALETTES[period]

    original = README.read_text(encoding="utf-8")
    prefix, block, suffix = extract_block(original)
    updated_block = recolor(block, palette["accent"], palette["fire"])
    if updated_block == block:
        print(f"stats cards already match {period} ({palette['accent']})")
        return 0

    README.write_text(prefix + updated_block + suffix, encoding="utf-8")
    print(f"stats cards → {period} accent=#{palette['accent']} fire=#{palette['fire']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
