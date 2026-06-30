#!/usr/bin/env python3
"""
contribution-board.py — Generate ASCII leaderboard for robotics-learnings.md
Shows last 7 days of contributions by Ethan, Erik, Raymond.
Usage: python3 contribution-board.py [--days 7]
"""
import re
import sys
import argparse
from datetime import date, timedelta, datetime
from collections import defaultdict
from pathlib import Path

LEARNINGS_FILE = Path(__file__).resolve().parent.parent.parent / "robotics-learnings.md"
PEOPLE = ["Ethan", "Erik", "Raymond"]
DAY_HEADERS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def parse_entries(text):
    """Return list of (date_obj, author) for every entry header."""
    # Match: ### YYYY-MM-DD — Author
    pattern = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2})\s+[—-]\s+(\w+)", re.MULTILINE)
    entries = []
    for m in pattern.finditer(text):
        try:
            d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            author = m.group(2).strip()
            entries.append((d, author))
        except ValueError:
            continue
    return entries


def build_grid(entries, days, today):
    """counts[author][date] = int"""
    start = today - timedelta(days=days - 1)
    counts = {p: defaultdict(int) for p in PEOPLE}
    for d, author in entries:
        if start <= d <= today and author in counts:
            counts[author][d] += 1
    return counts, start


def streak(counts_for_author, today):
    """Consecutive days back from today with at least one contribution."""
    s = 0
    d = today
    while counts_for_author.get(d, 0) > 0:
        s += 1
        d -= timedelta(days=1)
    return s


def render(counts, start, today, days):
    dates = [start + timedelta(days=i) for i in range(days)]

    # Day-of-week header row
    dow = "         "  # padding for author column
    for d in dates:
        dow += f"  {DAY_HEADERS[d.weekday()]} "
    # Date row
    date_row = "         "
    for d in dates:
        date_row += f"  {d.month}/{d.day:<2}"

    # Per-person rows
    person_rows = []
    totals = {}
    for p in PEOPLE:
        c = counts[p]
        total = sum(c.values())
        totals[p] = total
        cells = ""
        for d in dates:
            n = c.get(d, 0)
            if n == 0:
                cells += "   ·  "
            elif n == 1:
                cells += "   █  "
            elif n == 2:
                cells += "  ██  "
            elif n == 3:
                cells += " ███  "
            else:
                cells += f"  {n}x  "
        st = streak(c, today)
        streak_str = f"🔥{st}d" if st >= 2 else (" " * 5 if st == 0 else "  1d ")
        person_rows.append(f"{p:<8} [{total}]{cells}  {streak_str}")

    # Leaderboard
    rank = sorted(PEOPLE, key=lambda p: -totals[p])
    medals = ["1.", "2.", "3."]
    board = []
    for i, p in enumerate(rank):
        t = totals[p]
        bar = "█" * min(t, 12) + "·" * max(0, 4 - t)
        if t == 0:
            bar = "····"
        board.append(f"  {medals[i]} {p:<8} {bar} ({t})")

    # Final output
    lines = []
    lines.append("THE BOARD — Last 7 days of robotics learnings")
    lines.append("━" * 50)
    lines.extend(board)
    lines.append("")
    lines.append(dow)
    lines.append(date_row)
    for r in person_rows:
        lines.append(r)
    lines.append("")
    lines.append("  █ = 1 entry · ·  = no entry · 🔥 = streak (2+ days)")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--days", type=int, default=7)
    ap.add_argument("--today", type=str, default=None,
                    help="Override today (YYYY-MM-DD) for testing")
    ap.add_argument("--file", type=str, default=str(LEARNINGS_FILE))
    args = ap.parse_args()

    today = date.today()
    if args.today:
        today = datetime.strptime(args.today, "%Y-%m-%d").date()

    try:
        text = Path(args.file).read_text()
    except FileNotFoundError:
        print(f"learnings file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    entries = parse_entries(text)
    counts, start = build_grid(entries, args.days, today)
    print(render(counts, start, today, args.days))


if __name__ == "__main__":
    main()
