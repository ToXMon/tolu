---
name: daily-coding-review
version: "1.0.0"
trigger: /daily-review
description: >
  Full code review vs main branch + daily plan workpack + state machine diagram.
  Run at session start to establish context and priorities.
---

# Daily Coding Review

Slash command: `/daily-review`

## When to use
Run this at the start of every coding session to:
- Understand what changed since last session
- Establish current state of the codebase
- Plan the day's work
- Identify blockers early

## Execution Steps

### Step 1: Read Session Context

1. Read today's session log:
   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/session_logger.py read
   ```

2. Read the weekly summary for ongoing context:
   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/session_logger.py summary_week
   ```

3. Check for active workpack:
   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/workpack_generator.py status <project_dir>
   ```

4. Read AGENTS.md files in affected directories for accumulated patterns.

### Step 2: Git Diff Review

1. Check changes since last session:
   ```bash
   cd <project_dir> && git log --oneline -10
   cd <project_dir> && git diff main...HEAD --stat
   ```

2. Review the diff for:
   - Files exceeding 300 lines (flag them)
   - New `any` types introduced
   - Missing tests for new code
   - Drive-by refactoring (changes unrelated to the task)
   - Security concerns (hardcoded secrets, missing auth)

3. Run typecheck and tests:
   ```bash
   cd <project_dir> && npm run typecheck 2>&1 || true
   cd <project_dir> && npm test 2>&1 || true
   ```
   Or for Python:
   ```bash
   cd <project_dir> && python -m mypy . --ignore-missing-imports 2>&1 || true
   cd <project_dir> && python -m pytest 2>&1 || true
   ```

### Step 3: Codebase Audit

Run a quick audit focusing on the most critical checks:
```bash
find <project_dir> -type f \( -name '*.py' -o -name '*.ts' -o -name '*.tsx' \) \
  ! -path '*/node_modules/*' ! -path '*/venv/*' \
  -exec sh -c 'lines=$(wc -l < "$1"); if [ "$lines" -gt 300 ]; then echo "$lines $1"; fi' _ {} \;
```

### Step 4: Generate State Machine Diagram

For any module with significant changes, generate a state diagram:
```
/diagram <changed_module>
```

### Step 5: Plan the Day

Based on findings, create or update the day's workpack:

1. List pending workpack tasks
2. Prioritize based on:
   - Blocking issues (fix first)
   - Test failures (fix before new features)
   - High-priority workpack tasks
   - Refactoring that enables future work
3. Generate the daily plan:

```
=== Daily Plan ===
Date: [today]
Project: [name]

Context:
  Last session: [summary from logs]
  Active workpack: [status]
  Git status: [branch, commits ahead/behind]

Priorities:
  1. [Most important task]
  2. [Second priority]
  3. [Third priority]

Health Check:
  Tests: [passing/failing]
  Typecheck: [clean/errors]
  Files >300 lines: [count]
  Missing AGENTS.md: [count]

Ready to start: python3 instruments/workpack_generator.py next <project_dir>
```

### Step 6: Log Session Start

```bash
python3 /a0/skills/agentic-coding-harness/instruments/session_logger.py log \
  "<project>" "Daily review complete" "<key_decisions>" "<blockers>" "<plan>"
```
