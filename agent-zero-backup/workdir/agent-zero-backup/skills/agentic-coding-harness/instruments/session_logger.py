#!/usr/bin/env python3
"""Session Logger — Tracks coding sessions with decisions, blockers, and next steps.

Usage:
    python3 session_logger.py log <project> <summary> [decisions] [blockers] [next_steps]
    python3 session_logger.py read [date]
    python3 session_logger.py summary_week

Logs to work_logs/session_YYYY-MM-DD.json relative to current working directory.
"""

import json
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path


WORK_LOGS_DIR = Path("work_logs")


def _log_path(date_str: str | None = None) -> Path:
    """Return the log file path for a given date."""
    if date_str is None:
        date_str = datetime.now().strftime("%Y-%m-%d")
    WORK_LOGS_DIR.mkdir(parents=True, exist_ok=True)
    return WORK_LOGS_DIR / f"session_{date_str}.json"


def _load_log(path: Path) -> list[dict]:
    """Load existing log entries or return empty list."""
    if path.exists():
        with open(path, "r") as f:
            data = json.load(f)
        return data.get("entries", [])
    return []


def _save_log(path: Path, entries: list[dict]) -> None:
    """Save log entries to file."""
    with open(path, "w") as f:
        json.dump({
            "date": path.stem.replace("session_", ""),
            "entries": entries,
            "total_sessions": len(entries),
        }, f, indent=2)


def log_entry(
    project: str,
    summary: str,
    decisions: str = "",
    blockers: str = "",
    next_steps: str = "",
) -> None:
    """Add a new session entry to today's log."""
    path = _log_path()
    entries = _load_log(path)

    entry = {
        "timestamp": datetime.now().isoformat(),
        "project": project,
        "summary": summary,
        "decisions": decisions.split(";") if decisions else [],
        "blockers": blockers.split(";") if blockers else [],
        "next_steps": next_steps.split(";") if next_steps else [],
        "files_changed": [],
        "tests_status": "unknown",
    }

    entries.append(entry)
    _save_log(path, entries)
    print(f"Logged entry for '{project}' at {entry['timestamp']}")
    print(f"  Summary: {summary}")
    print(f"  Log file: {path}")


def read_log(date_str: str | None = None) -> None:
    """Display log entries for a given date (default: today)."""
    path = _log_path(date_str)
    entries = _load_log(path)

    if not entries:
        print(f"No entries found for {date_str or 'today'}.")
        return

    print(f"\n=== Session Log: {date_str or datetime.now().strftime('%Y-%m-%d')} ===")
    print(f"Total entries: {len(entries)}\n")

    for i, entry in enumerate(entries, 1):
        print(f"--- Entry {i} ---")
        print(f"  Time:      {entry['timestamp']}")
        print(f"  Project:   {entry['project']}")
        print(f"  Summary:   {entry['summary']}")
        if entry.get("decisions"):
            print(f"  Decisions: {', '.join(entry['decisions'])}")
        if entry.get("blockers"):
            print(f"  Blockers:  {', '.join(entry['blockers'])}")
        if entry.get("next_steps"):
            print(f"  Next:      {', '.join(entry['next_steps'])}")
        print()


def summary_week() -> None:
    """Generate a weekly summary of all session logs."""
    today = datetime.now()
    week_ago = today - timedelta(days=7)

    all_entries: list[dict] = []
    for i in range(8):
        day = week_ago + timedelta(days=i)
        date_str = day.strftime("%Y-%m-%d")
        path = _log_path(date_str)
        entries = _load_log(path)
        for entry in entries:
            entry["date"] = date_str
        all_entries.extend(entries)

    if not all_entries:
        print("No session entries found in the past 7 days.")
        return

    projects: dict[str, list[dict]] = {}
    for entry in all_entries:
        proj = entry.get("project", "unknown")
        projects.setdefault(proj, []).append(entry)

    print(f"\n=== Weekly Summary ({week_ago.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}) ===")
    print(f"Total sessions: {len(all_entries)}")
    print(f"Projects: {', '.join(projects.keys())}\n")

    for proj, entries in projects.items():
        print(f"## {proj} ({len(entries)} sessions)")
        all_blockers: list[str] = []
        all_next: list[str] = []
        for entry in entries:
            all_blockers.extend(entry.get("blockers", []))
            all_next.extend(entry.get("next_steps", []))
        if all_blockers:
            print(f"  Blockers: {', '.join(set(all_blockers))}")
        if all_next:
            print(f"  Up next:  {', '.join(set(all_next))}")
        print()


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "log":
        if len(sys.argv) < 4:
            print("Usage: session_logger.py log <project> <summary> [decisions] [blockers] [next_steps]")
            sys.exit(1)
        log_entry(
            project=sys.argv[2],
            summary=sys.argv[3],
            decisions=sys.argv[4] if len(sys.argv) > 4 else "",
            blockers=sys.argv[5] if len(sys.argv) > 5 else "",
            next_steps=sys.argv[6] if len(sys.argv) > 6 else "",
        )
    elif command == "read":
        read_log(sys.argv[2] if len(sys.argv) > 2 else None)
    elif command == "summary_week":
        summary_week()
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
