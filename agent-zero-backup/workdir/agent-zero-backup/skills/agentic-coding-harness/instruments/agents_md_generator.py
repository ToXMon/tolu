#!/usr/bin/env python3
"""AGENTS.md Generator — Recursively creates AGENTS.md files in project modules.

Usage:
    python3 agents_md_generator.py generate <project_dir> [--dry-run]
    python3 agents_md_generator.py update <project_dir> [--dry-run]
    python3 agents_md_generator.py verify <project_dir>

Ignores: .git, node_modules, __pycache__, dist, build, .next, venv, .venv
"""

import sys
import re
import os
from pathlib import Path
from datetime import datetime


IGNORE_DIRS = {
    ".git", "node_modules", "__pycache__", "dist", "build",
    ".next", "venv", ".venv", "env", ".env", ".tox",
    ".mypy_cache", ".pytest_cache", ".ruff_cache", "coverage",
    ".hg", ".svn", "target", "vendor", "Pods", ".gradle",
}

SOURCE_EXTENSIONS = {
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".rb",
    ".java", ".kt", ".swift", ".c", ".cpp", ".h", ".hpp",
    ".cs", ".scala", ".clj", ".ex", ".exs", ".erl", ".hs",
    ".lua", ".php", ".r", ".R", ".m", ".mm",
}

CONFIG_EXTENSIONS = {
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
}


def _has_source_files(directory: Path) -> bool:
    """Check if directory contains source files (not just configs/docs)."""
    for item in directory.iterdir():
        if item.is_file() and item.suffix in SOURCE_EXTENSIONS:
            return True
    return False


def _count_source_files(directory: Path) -> int:
    """Count source files in a directory."""
    return sum(1 for f in directory.iterdir() if f.is_file() and f.suffix in SOURCE_EXTENSIONS)


def _analyze_module(directory: Path) -> dict:
    """Analyze a module directory for AGENTS.md content."""
    source_files = []
    config_files = []
    submodules = []
    test_files = []
    exports: list[str] = []
    imports: list[str] = []

    for item in sorted(directory.iterdir()):
        if item.is_file():
            if item.suffix in SOURCE_EXTENSIONS:
                source_files.append(item.name)
                if "test" in item.name.lower() or "spec" in item.name.lower():
                    test_files.append(item.name)
                # Scan for exports
                try:
                    content = item.read_text(encoding="utf-8", errors="ignore")[:2000]
                    if item.suffix == ".py":
                        for match in re.finditer(r'^(?:def |class |async def )(\w+)', content, re.MULTILINE):
                            exports.append(match.group(1))
                    elif item.suffix in {"ts", "tsx", "js", "jsx"}:
                        for match in re.finditer(r'(?:export\s+(?:default\s+)?(?:function|class|const|interface|type)\s+)(\w+)', content):
                            exports.append(match.group(1))
                except Exception:
                    pass
            elif item.suffix in CONFIG_EXTENSIONS:
                config_files.append(item.name)
        elif item.is_dir() and item.name not in IGNORE_DIRS and not item.name.startswith("."):
            submodules.append(item.name)

    return {
        "source_files": source_files,
        "config_files": config_files,
        "submodules": submodules,
        "test_files": test_files,
        "exports": exports[:20],  # limit
        "has_existing_agents_md": (directory / "AGENTS.md").exists(),
    }


def _generate_agents_md(directory: Path, analysis: dict, project_root: Path) -> str:
    """Generate AGENTS.md content for a directory."""
    rel_path = directory.relative_to(project_root) if directory != project_root else Path(".")
    module_name = directory.name if directory != project_root else project_root.name

    lines: list[str] = []
    lines.append(f"# AGENTS.md — {module_name}/")
    lines.append("")
    lines.append(f"Module: `{rel_path}`")
    lines.append(f"Updated: {datetime.now().strftime('%Y-%m-%d')}")
    lines.append("")

    # Overview
    lines.append("## Overview")
    lines.append("")
    lines.append(f"This module contains {len(analysis['source_files'])} source files"
                 f" and {len(analysis['submodules'])} submodules.")
    lines.append("")

    # Files
    if analysis["source_files"]:
        lines.append("## Source Files")
        lines.append("")
        for f in analysis["source_files"]:
            icon = "🧪" if f in analysis["test_files"] else "📄"
            lines.append(f"- {icon} `{f}`")
        lines.append("")

    # Exports
    if analysis["exports"]:
        lines.append("## Key Exports")
        lines.append("")
        for exp in analysis["exports"]:
            lines.append(f"- `{exp}`")
        lines.append("")

    # Submodules
    if analysis["submodules"]:
        lines.append("## Submodules")
        lines.append("")
        for sub in analysis["submodules"]:
            lines.append(f"- [`{sub}/`]({sub}/AGENTS.md)")
        lines.append("")

    # Patterns section (to be filled by agents during development)
    lines.append("## Patterns & Conventions")
    lines.append("")
    lines.append("<!-- Agents: Add discovered patterns and gotchas here -->")
    lines.append("")

    # Dependencies
    lines.append("## Dependencies")
    lines.append("")
    lines.append("<!-- Agents: Note cross-module dependencies here -->")
    lines.append("")

    return "\n".join(lines)


def generate_agents_files(project_dir: str, dry_run: bool = False) -> list[Path]:
    """Recursively generate AGENTS.md files in all modules with source files."""
    root = Path(project_dir).resolve()
    if not root.exists():
        print(f"Project directory not found: {root}")
        return []

    created: list[Path] = []
    dirs_to_process: list[Path] = [root]

    while dirs_to_process:
        current = dirs_to_process.pop(0)

        # Skip ignored directories
        if current.name in IGNORE_DIRS:
            continue

        if not current.is_dir():
            continue

        # Check if this directory has source files
        if _has_source_files(current):
            analysis = _analyze_module(current)
            content = _generate_agents_md(current, analysis, root)
            agents_path = current / "AGENTS.md"

            if dry_run:
                print(f"[DRY RUN] Would create: {agents_path}")
                print(f"  Files: {len(analysis['source_files'])}, Exports: {len(analysis['exports'])}")
            else:
                agents_path.write_text(content)
                print(f"Created: {agents_path}")
            created.append(agents_path)

        # Add subdirectories to process
        try:
            for child in current.iterdir():
                if child.is_dir() and child.name not in IGNORE_DIRS and not child.name.startswith("."):
                    dirs_to_process.append(child)
        except PermissionError:
            continue

    print(f"\nTotal AGENTS.md files: {len(created)}")
    return created


def update_agents_files(project_dir: str, dry_run: bool = False) -> list[Path]:
    """Update existing AGENTS.md files, preserving the Patterns section."""
    root = Path(project_dir).resolve()
    if not root.exists():
        print(f"Project directory not found: {root}")
        return []

    updated: list[Path] = []

    for agents_path in root.rglob("AGENTS.md"):
        # Skip ignored paths
        if any(part in IGNORE_DIRS for part in agents_path.parts):
            continue

        directory = agents_path.parent
        analysis = _analyze_module(directory)

        # Preserve existing patterns section
        existing = agents_path.read_text(encoding="utf-8", errors="ignore")
        patterns_match = re.search(
            r'(## Patterns & Conventions\n.*?)(?=## |$)',
            existing,
            re.DOTALL,
        )
        patterns_content = patterns_match.group(1) if patterns_match else ""

        new_content = _generate_agents_md(directory, analysis, root)
        if patterns_content.strip() != "## Patterns & Conventions":
            # User has added content — preserve it
            new_content = re.sub(
                r'## Patterns & Conventions\n.*?()(?=## |$)',
                patterns_content,
                new_content,
                flags=re.DOTALL,
            )

        if dry_run:
            print(f"[DRY RUN] Would update: {agents_path}")
        else:
            agents_path.write_text(new_content)
            print(f"Updated: {agents_path}")
        updated.append(agents_path)

    print(f"\nTotal updated: {len(updated)}")
    return updated


def verify_agents_files(project_dir: str) -> dict:
    """Check which directories with source files are missing AGENTS.md."""
    root = Path(project_dir).resolve()
    missing: list[str] = []
    present: list[str] = []
    empty_patterns: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Filter out ignored directories
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".")]

        dp = Path(dirpath)
        has_source = any(Path(f).suffix in SOURCE_EXTENSIONS for f in filenames)

        if has_source:
            agents_path = dp / "AGENTS.md"
            if agents_path.exists():
                present.append(str(dp.relative_to(root)))
                content = agents_path.read_text(encoding="utf-8", errors="ignore")
                if "<!-- Agents: Add discovered patterns" in content:
                    empty_patterns.append(str(dp.relative_to(root)))
            else:
                missing.append(str(dp.relative_to(root)))

    report = {
        "present": len(present),
        "missing": len(missing),
        "empty_patterns": len(empty_patterns),
        "missing_dirs": missing,
        "empty_pattern_dirs": empty_patterns,
    }

    print(f"\n=== AGENTS.md Verification ===")
    print(f"Present: {report['present']}")
    print(f"Missing: {report['missing']}")
    print(f"Empty patterns: {report['empty_patterns']}")
    if missing:
        print(f"\nMissing in:")
        for d in missing:
            print(f"  - {d}")

    return report


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    if command == "generate":
        if len(sys.argv) < 3:
            print("Usage: agents_md_generator.py generate <project_dir> [--dry-run]")
            sys.exit(1)
        generate_agents_files(sys.argv[2], dry_run)
    elif command == "update":
        if len(sys.argv) < 3:
            print("Usage: agents_md_generator.py update <project_dir> [--dry-run]")
            sys.exit(1)
        update_agents_files(sys.argv[2], dry_run)
    elif command == "verify":
        if len(sys.argv) < 3:
            print("Usage: agents_md_generator.py verify <project_dir>")
            sys.exit(1)
        verify_agents_files(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
