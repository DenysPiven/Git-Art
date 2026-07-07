#!/usr/bin/env python3
"""Generate GitArt-style commits: append lines to foobar.txt (skip 2024)."""
import random
import subprocess
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from tqdm import tqdm

REPO = Path("/Users/pivden2000/Projects/GitArt")
FOOBAR = REPO / "foobar.txt"
START = date(2017, 1, 1)
END = date(2026, 7, 7)
SKIP_YEAR = 2024
TZ = ZoneInfo("Europe/Kyiv")
MIN_COMMITS = 1
MAX_COMMITS = 5


def existing_dates() -> set[str]:
    result = subprocess.run(
        ["git", "log", "--format=%ai"],
        capture_output=True,
        text=True,
        cwd=REPO,
        check=True,
    )
    return {line.split()[0] for line in result.stdout.strip().split("\n") if line}


def js_date_string(d: date) -> str:
    dt = datetime(d.year, d.month, d.day, tzinfo=TZ)
    off = dt.strftime("%z")
    is_dst = dt.dst() and dt.dst().total_seconds() > 0
    tz_name = (
        "Eastern European Summer Time"
        if is_dst
        else "Eastern European Standard Time"
    )
    return dt.strftime(f"%a %b %d %Y 00:00:00 GMT{off[:3]}{off[3:]} ({tz_name})")


def plan_days(have: set[str]) -> list[tuple[date, int]]:
    random.seed(42)
    days: list[tuple[date, int]] = []
    d = START
    while d <= END:
        if d.year != SKIP_YEAR and d.isoformat() not in have:
            count = random.randint(MIN_COMMITS, MAX_COMMITS)
            days.append((d, count))
        d += timedelta(days=1)
    return days


def make_commit(date_str: str, index: int) -> None:
    line = f"{date_str} -> ({index})\n"
    with FOOBAR.open("a") as f:
        f.write(line)
    subprocess.run(["git", "add", "foobar.txt"], cwd=REPO, check=True)
    subprocess.run(
        ["git", "commit", f"--date={date_str}", "-m", date_str],
        cwd=REPO,
        capture_output=True,
        check=True,
    )


def main() -> None:
    print("Scanning existing commits...", flush=True)
    have = existing_dates()
    days = plan_days(have)
    total_commits = sum(c for _, c in days)

    if total_commits == 0:
        print("Nothing to do — all days already covered.")
        return

    print(
        f"Plan: {len(days)} days, {total_commits} commits "
        f"({MIN_COMMITS}-{MAX_COMMITS}/day, skip {SKIP_YEAR})\n",
        flush=True,
    )

    with tqdm(total=total_commits, unit="commit", dynamic_ncols=True) as bar:
        for day, count in days:
            date_str = js_date_string(day)
            bar.set_postfix_str(day.isoformat(), refresh=False)
            for i in range(count):
                make_commit(date_str, i)
                bar.update(1)

    print(f"\nDone: {len(days)} days, {total_commits} commits")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrupted.", file=sys.stderr)
        sys.exit(130)
