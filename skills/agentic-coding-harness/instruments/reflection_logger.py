#!/usr/bin/env python3
"""Reflection Logger — Session handoff and learning distillation CLI.

Reads progress.txt and session logs from a project directory, generates a
session handoff document, appends learnings to progress.txt, and updates
AGENTS.md patterns section.

Usage:
    python3 reflection_logger.py reflect <project_dir> \
        --summary "text" --surprises "text" --blocked "text" --next "text"
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# File helpers
# ---------------------------------------------------------------------------

def _read_file(path: Path) -> str:
    """Return file contents or empty string if missing."""
    if path.is_file():
        return path.read_text(encoding="utf-8")
    return ""


def _append_file(path: Path, content: str) -> None:
    """Append content to a file, creating parent dirs as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as fh:
        fh.write(content)


def _write_file(path: Path, content: str) -> None:
    """Write content to a file, creating parent dirs as needed."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


# ---------------------------------------------------------------------------
# Data extraction
# ---------------------------------------------------------------------------

def _latest_session_log(work_logs: Path) -> Optional[dict[str, str]]:
    """Return the most recent session_*.json parsed, or None."""
    logs = sorted(work_logs.glob("session_*.json"))
    if not logs:
        return None
    raw = _read_file(logs[-1])
    try:
        data: dict[str, str] = json.loads(raw)
        return data
    except json.JSONDecodeError:
        return None


def _progress_summary(progress_path: Path, tail_lines: int = 40) -> str:
    """Return the last N lines of progress.txt for context."""
    text = _read_file(progress_path)
    if not text:
        return "(no progress.txt found)"
    lines = text.strip().splitlines()
    return "\n".join(lines[-tail_lines:])


# ---------------------------------------------------------------------------
# Reflection document generation
# ---------------------------------------------------------------------------

def _build_reflection_markdown(
    project_dir: Path,
    summary: str,
    surprises: str,
    blocked: str,
    next_steps: str,
    progress_tail: str,
    session_data: Optional[dict[str, str]],
    ts: datetime,
) -> str:
    """Build the full reflection markdown document."""
    stamp = ts.strftime("%Y-%m-%d %H:%M:%S UTC")
    session_info = ""
    if session_data:
        session_info = json.dumps(session_data, indent=2)
    else:
        session_info = "(no session log found)"

    return f"""# Session Reflection — {stamp}

## Project
`{project_dir}`

## Summary
{summary if summary else "_(no summary provided)_"}

## Surprises & Discoveries
{surprises if surprises else "_(none reported)_"}

## Blockers
{blocked if blocked else "_(none reported)_"}

## Next Steps
{next_steps if next_steps else "_(not specified)_"}

---

## Context: Recent progress.txt
```
{progress_tail}
```

## Context: Latest Session Log
```json
{session_info}
```
"""


def _build_handoff_json(
    project_dir: Path,
    summary: str,
    surprises: str,
    blocked: str,
    next_steps: str,
    ts: datetime,
) -> dict[str, str]:
    """Build the structured handoff JSON payload."""
    return {
        "timestamp": ts.isoformat(),
        "project": str(project_dir),
        "summary": summary,
        "surprises": surprises,
        "blocked": blocked,
        "next_steps": next_steps,
    }


# ---------------------------------------------------------------------------
# AGENTS.md pattern update
# ---------------------------------------------------------------------------

_PATTERNS_MARKER = "## Discovered Patterns"


def _update_agents_md(agents_path: Path, learnings: str, ts: datetime) -> None:
    """Append discovered patterns to AGENTS.md."""
    if not learnings.strip():
        return

    content = _read_file(agents_path)
    stamp = ts.strftime("%Y-%m-%d")
    entry = f"\n- [{stamp}] {learnings.strip()}"

    if _PATTERNS_MARKER in content:
        # Insert after the marker line
        lines = content.splitlines(keepends=True)
        for idx, line in enumerate(lines):
            if line.strip() == _PATTERNS_MARKER:
                lines.insert(idx + 1, entry + "\n")
                break
        _write_file(agents_path, "".join(lines))
    else:
        # Append a new section
        section = f"\n{_PATTERNS_MARKER}\n{entry}\n"
        _append_file(agents_path, section)


# ---------------------------------------------------------------------------
# progress.txt append
# ---------------------------------------------------------------------------

def _append_to_progress(progress_path: Path, summary: str, surprises: str, ts: datetime) -> None:
    """Append session learnings to progress.txt."""
    stamp = ts.strftime("%Y-%m-%d %H:%M")
    parts: list[str] = [f"\n## Session {stamp}"]
    if summary:
        parts.append(f"Summary: {summary}")
    if surprises:
        parts.append(f"Surprises: {surprises}")
    parts.append("")  # blank line
    _append_file(progress_path, "\n".join(parts))


# ---------------------------------------------------------------------------
# Main reflect command
# ---------------------------------------------------------------------------

def cmd_reflect(args: argparse.Namespace) -> int:
    """Execute the reflect sub-command."""
    project_dir = Path(args.project_dir).resolve()
    if not project_dir.is_dir():
        print(f"Error: {project_dir} is not a directory", file=sys.stderr)
        return 1

    ts = datetime.now(timezone.utc)
    ts_file = ts.strftime("%Y-%m-%d_%H%M%S")

    work_logs = project_dir / "work_logs"
    progress_path = project_dir / "progress.txt"
    agents_path = project_dir / "AGENTS.md"

    # Gather context
    progress_tail = _progress_summary(progress_path)
    session_data = _latest_session_log(work_logs)

    summary: str = args.summary or ""
    surprises: str = args.surprises or ""
    blocked: str = args.blocked or ""
    next_steps: str = args.next or ""

    # Generate outputs
    reflection_md = _build_reflection_markdown(
        project_dir, summary, surprises, blocked, next_steps,
        progress_tail, session_data, ts,
    )
    handoff = _build_handoff_json(
        project_dir, summary, surprises, blocked, next_steps, ts,
    )

    # Write outputs
    reflection_path = work_logs / f"reflection_{ts_file}.md"
    handoff_path = work_logs / f"handoff_{ts_file}.json"

    _write_file(reflection_path, reflection_md)
    _write_file(handoff_path, json.dumps(handoff, indent=2) + "\n")

    print(f"Reflection  → {reflection_path}")
    print(f"Handoff     → {handoff_path}")

    # Update side-files
    _append_to_progress(progress_path, summary, surprises, ts)
    print(f"Progress    → {progress_path}")

    if surprises.strip():
        _update_agents_md(agents_path, surprises, ts)
        print(f"Patterns    → {agents_path}")

    return 0


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    """Construct the argument parser."""
    parser = argparse.ArgumentParser(
        description="Reflection Logger — session handoff and learning distillation",
    )
    sub = parser.add_subparsers(dest="command")

    reflect = sub.add_parser("reflect", help="Generate session reflection and handoff")
    reflect.add_argument("project_dir", help="Path to the project directory")
    reflect.add_argument("--summary", default="", help="Session summary text")
    reflect.add_argument("--surprises", default="", help="Surprises and discoveries")
    reflect.add_argument("--blocked", default="", help="Current blockers")
    reflect.add_argument("--next", default="", help="Planned next steps")

    return parser


def main() -> int:
    """Entry point."""
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "reflect":
        return cmd_reflect(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
