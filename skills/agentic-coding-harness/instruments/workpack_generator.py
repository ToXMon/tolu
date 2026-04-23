#!/usr/bin/env python3
"""Workpack Generator — Creates structured workpack files for long autonomous runs.

Usage:
    python3 workpack_generator.py create <project_dir> <goal> [max_tasks]
    python3 workpack_generator.py status <project_dir>
    python3 workpack_generator.py next <project_dir>
    python3 workpack_generator.py complete <project_dir> <task_id>

Generates .workpack/scope.md, .workpack/rules.md, and .workpack/task-XXXX.md files.
"""

import json
import sys
import re
from pathlib import Path
from datetime import datetime


WORKPACK_DIR = ".workpack"

RULES_TEMPLATE = """# Workpack Rules — Autonomous Execution Constraints

These rules govern all autonomous task execution within this workpack.

## Mandatory Constraints

1. **No questions** — Make decisions based on available context. Document assumptions.
2. **No stops** — If blocked, work around the blocker and log it.
3. **File size limit** — No file shall exceed 300 lines. Split if approaching limit.
4. **Directory size limit** — No directory shall contain more than 20 source files.
5. **No `any` types** — All TypeScript/Python types must be explicit. Use proper interfaces.
6. **Update AGENTS.md** — After every meaningful change, update the nearest AGENTS.md.
7. **Commit on green** — Only commit when tests pass and typechecks are clean.
8. **One task per iteration** — Complete one task-XXXX.md fully before moving to next.
9. **Progress logging** — Append to progress.txt after each task completion.
10. **No drive-by refactoring** — Only change code directly related to the current task.

## Quality Gates

Before marking a task complete:
- [ ] All new code has corresponding tests
- [ ] No type errors (typecheck passes)
- [ ] No lint errors
- [ ] No file exceeds 300 lines
- [ ] AGENTS.md updated in affected directories
- [ ] No `any` types introduced

## Autonomous Mode Behavior

When executing tasks autonomously:
- Read the full scope.md before starting any task
- Read progress.txt for accumulated learnings
- Follow task-XXXX.md acceptance criteria exactly
- If a task is unclear, make a reasonable assumption and document it
- Never batch multiple tasks — one at a time
- After completing a task, update its status and append learnings to progress.txt
"""

SCOPE_TEMPLATE = """# Workpack Scope: {goal}

Created: {date}
Project: {project_dir}
Total Tasks: {task_count}

## Objective

{goal}

## Architecture Constraints

- Modular slice architecture: config, types, DB centralized
- File size limit: 300 lines max
- Directory limit: 20 files max
- No `any` types — explicit casts always
- JSON DB stub pattern for local dev
- Integration tests write JSON to data/

## Success Criteria

- [ ] All tasks have status: complete
- [ ] All quality gates pass
- [ ] No regressions in existing tests
- [ ] AGENTS.md updated across all affected modules
- [ ] Code review checklist satisfied

## Task Summary

{task_summary}
"""

TASK_TEMPLATE = """# Task {task_id}: {title}

Status: {status}
Priority: {priority}
Created: {date}

## Description

{description}

## Acceptance Criteria

{acceptance_criteria}

## Implementation Notes

{implementation_notes}

## Files to Create/Modify

{files}

## Verification Steps

1. Implement the changes listed above
2. Run typecheck: confirm no type errors
3. Run tests: confirm all pass
4. Check file sizes: none exceed 300 lines
5. Update AGENTS.md in affected directories
6. Mark this task complete in the status field

## Completion Log

<!-- Append completion details here when done -->
"""


def _workpack_path(project_dir: str) -> Path:
    return Path(project_dir) / WORKPACK_DIR


def _next_task_id(wp_dir: Path) -> str:
    """Determine the next task ID based on existing tasks."""
    existing = list(wp_dir.glob("task-*.md"))
    if not existing:
        return "0001"
    nums = []
    for f in existing:
        match = re.search(r"task-(\d+)", f.name)
        if match:
            nums.append(int(match.group(1)))
    return f"{max(nums) + 1:04d}"


def _parse_tasks_from_goal(goal: str, max_tasks: int) -> list[dict]:
    """Break a goal into discrete tasks based on common patterns."""
    tasks = []
    goal_lower = goal.lower()

    # Detect common patterns and generate appropriate tasks
    if any(kw in goal_lower for kw in ["api", "endpoint", "server", "backend"]):
        tasks.extend([
            {"title": "Define data models and types",
             "description": "Create type definitions and database schema for the API.",
             "priority": 1},
            {"title": "Implement API routes",
             "description": "Build route handlers with proper validation and error handling.",
             "priority": 2},
            {"title": "Add database layer",
             "description": "Implement database connection, migrations, and query functions.",
             "priority": 3},
            {"title": "Write integration tests",
             "description": "Test all endpoints with valid and invalid inputs.",
             "priority": 4},
        ])

    if any(kw in goal_lower for kw in ["ui", "frontend", "page", "component", "web"]):
        tasks.extend([
            {"title": "Create component structure",
             "description": "Set up component files with proper type definitions.",
             "priority": 1},
            {"title": "Implement UI components",
             "description": "Build all UI components with proper state management.",
             "priority": 2},
            {"title": "Add styling and responsiveness",
             "description": "Apply styles and ensure responsive layout.",
             "priority": 3},
            {"title": "Test UI interactions",
             "description": "Verify all user flows work correctly.",
             "priority": 4},
        ])

    if any(kw in goal_lower for kw in ["auth", "login", "security", "user"]):
        tasks.extend([
            {"title": "Implement authentication flow",
             "description": "Build login/signup/logout with proper session management.",
             "priority": 1},
            {"title": "Add authorization middleware",
             "description": "Create role-based access control checks.",
             "priority": 2},
            {"title": "Security hardening",
             "description": "Add rate limiting, input sanitization, CSRF protection.",
             "priority": 3},
        ])

    # If no patterns matched, create generic tasks
    if not tasks:
        tasks = [
            {"title": "Analyze requirements and create plan",
             "description": f"Break down the goal into implementation steps.",
             "priority": 1},
            {"title": "Implement core logic",
             "description": f"Build the main functionality for: {goal}",
             "priority": 2},
            {"title": "Add tests and validation",
             "description": "Write comprehensive tests for all new code.",
             "priority": 3},
            {"title": "Documentation and cleanup",
             "description": "Update AGENTS.md, add comments, verify quality gates.",
             "priority": 4},
        ]

    return tasks[:max_tasks]


def create_workpack(project_dir: str, goal: str, max_tasks: int = 8) -> None:
    """Create a new workpack with scope, rules, and task files."""
    wp_dir = _workpack_path(project_dir)
    wp_dir.mkdir(parents=True, exist_ok=True)

    tasks = _parse_tasks_from_goal(goal, max_tasks)
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")

    # Write rules.md
    (wp_dir / "rules.md").write_text(RULES_TEMPLATE)
    print(f"Created rules.md")

    # Write task files
    task_summary_lines = []
    for i, task in enumerate(tasks):
        task_id = f"{i + 1:04d}"
        criteria = "- [ ] Typecheck passes\n- [ ] Tests pass\n- [ ] No file > 300 lines\n- [ ] AGENTS.md updated"
        files_section = "<!-- List files to create or modify -->"
        notes = f"Part of workpack: {goal}"

        task_content = TASK_TEMPLATE.format(
            task_id=task_id,
            title=task["title"],
            status="pending",
            priority=task["priority"],
            date=date_str,
            description=task["description"],
            acceptance_criteria=criteria,
            implementation_notes=notes,
            files=files_section,
        )

        task_path = wp_dir / f"task-{task_id}.md"
        task_path.write_text(task_content)
        task_summary_lines.append(f"- [{task_id}] {task['title']} (priority: {task['priority']})")

    # Write scope.md
    scope_content = SCOPE_TEMPLATE.format(
        goal=goal,
        date=date_str,
        project_dir=project_dir,
        task_count=len(tasks),
        task_summary="\n".join(task_summary_lines),
    )
    (wp_dir / "scope.md").write_text(scope_content)
    print(f"Created scope.md")

    # Initialize progress.txt
    progress_path = wp_dir / "progress.txt"
    if not progress_path.exists():
        progress_path.write_text(f"# Progress Log\nStarted: {date_str}\nGoal: {goal}\n---\n")
        print(f"Created progress.txt")

    print(f"\nWorkpack created at {wp_dir}/")
    print(f"Tasks: {len(tasks)}")
    print(f"\nNext: python3 workpack_generator.py next {project_dir}")


def status_workpack(project_dir: str) -> None:
    """Display workpack status."""
    wp_dir = _workpack_path(project_dir)
    if not wp_dir.exists():
        print(f"No workpack found at {wp_dir}")
        return

    print(f"\n=== Workpack Status: {project_dir} ===")
    tasks = sorted(wp_dir.glob("task-*.md"))
    pending = 0
    complete = 0
    for task_path in tasks:
        content = task_path.read_text()
        if "Status: complete" in content:
            complete += 1
            status_icon = "✓"
        else:
            pending += 1
            status_icon = "○"
        # Extract title from first heading
        title_match = re.search(r"# Task \d+: (.+)", content)
        title = title_match.group(1) if title_match else task_path.name
        print(f"  {status_icon} {task_path.name}: {title}")

    print(f"\nComplete: {complete}/{complete + pending}")


def next_task(project_dir: str) -> None:
    """Display the next pending task."""
    wp_dir = _workpack_path(project_dir)
    if not wp_dir.exists():
        print(f"No workpack found at {wp_dir}")
        return

    for task_path in sorted(wp_dir.glob("task-*.md")):
        content = task_path.read_text()
        if "Status: pending" in content or "Status: in_progress" not in content:
            if "Status: complete" not in content:
                print(f"\n=== Next Task: {task_path.name} ===")
                print(content)
                return

    print("All tasks complete!")


def complete_task(project_dir: str, task_id: str) -> None:
    """Mark a task as complete."""
    wp_dir = _workpack_path(project_dir)
    task_path = wp_dir / f"task-{task_id}.md"

    if not task_path.exists():
        print(f"Task file not found: {task_path}")
        return

    content = task_path.read_text()
    content = content.replace("Status: pending", "Status: complete")
    content = content.replace("Status: in_progress", "Status: complete")

    # Add completion timestamp
    completion_log = f"\n**Completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}**\n"
    content = content.replace(
        "<!-- Append completion details here when done -->",
        completion_log,
    )

    task_path.write_text(content)

    # Append to progress.txt
    progress_path = wp_dir / "progress.txt"
    title_match = re.search(r"# Task \d+: (.+)", content)
    title = title_match.group(1) if title_match else task_id
    with open(progress_path, "a") as f:
        f.write(f"\n## {datetime.now().strftime('%Y-%m-%d %H:%M')} - Task {task_id}\n")
        f.write(f"- Completed: {title}\n")
        f.write("---\n")

    print(f"Task {task_id} marked complete.")
    status_workpack(project_dir)


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) < 4:
            print("Usage: workpack_generator.py create <project_dir> <goal> [max_tasks]")
            sys.exit(1)
        max_tasks = int(sys.argv[4]) if len(sys.argv) > 4 else 8
        create_workpack(sys.argv[2], sys.argv[3], max_tasks)
    elif command == "status":
        status_workpack(sys.argv[2])
    elif command == "next":
        next_task(sys.argv[2])
    elif command == "complete":
        if len(sys.argv) < 4:
            print("Usage: workpack_generator.py complete <project_dir> <task_id>")
            sys.exit(1)
        complete_task(sys.argv[2], sys.argv[3])
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
