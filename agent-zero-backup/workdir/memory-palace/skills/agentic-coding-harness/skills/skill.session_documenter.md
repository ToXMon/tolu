---
name: session-documenter
version: "1.0.0"
trigger: /log /end
description: >
  Auto-document session start and end with decision logs, changelists, and next steps.
  Tracks work across sessions for continuity.
---

# Session Documenter

Slash commands: `/log` and `/end`

## `/log` — Session Start / Mid-Session Log

### When activated:
When the user types `/log` or says "log session" or "start logging":

### Instructions:

1. **Check for existing log** — Run:
   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/session_logger.py read
   ```

2. **Identify the active project** from current working directory or user context.

3. **Log the session entry** — Capture:
   - **Project**: Current project name
   - **Summary**: What this session is about (1-2 sentences)
   - **Decisions**: Key decisions made this session (semicolon-separated)
   - **Blockers**: Any blockers encountered (semicolon-separated)
   - **Next steps**: What should happen next (semicolon-separated)

   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/session_logger.py log \
     "<project>" "<summary>" "<decisions>" "<blockers>" "<next_steps>"
   ```

4. **Display confirmation** — Show the logged entry.

## `/end` — Session End

### When activated:
When the user types `/end` or says "end session" or "wrap up":

### Instructions:

1. **Summarize the session** — Review what was accomplished:
   - Files changed (from git diff or conversation context)
   - Decisions made
   - Tests status (passing/failing)
   - Blockers encountered

2. **Log the session end entry**:
   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/session_logger.py log \
     "<project>" "Session end: <summary>" "<decisions>" "<blockers>" "<next_steps>"
   ```

3. **Update AGENTS.md** — If any code was changed, run:
   ```bash
   python3 /a0/skills/agentic-coding-harness/instruments/agents_md_generator.py update <project_dir>
   ```

4. **Update progress.txt** — If a workpack is active, append learnings:
   ```
   ## [Date] - Session End
   - Summary of what was accomplished
   - Files changed: list
   - Learnings: patterns, gotchas, conventions discovered
   - Next session priorities: what to pick up
   ---
   ```

5. **Generate session summary** — Display:
   ```
   === Session Summary ===
   Duration: [estimated]
   Project: [name]
   Files changed: [count]
   Tests: [status]
   Key decisions: [list]
   Blockers: [list]
   Next steps: [list]
   Log saved: work_logs/session_YYYY-MM-DD.json
   ```

## Session Log Format

Each session entry in `work_logs/session_YYYY-MM-DD.json`:
```json
{
  "timestamp": "2025-01-15T14:30:00",
  "project": "project-name",
  "summary": "Implemented user auth flow",
  "decisions": ["Used JWT over sessions", "SQLite for dev"],
  "blockers": ["CORS config needed for prod"],
  "next_steps": ["Add rate limiting", "Write auth tests"],
  "files_changed": ["src/auth.ts", "src/middleware.ts"],
  "tests_status": "passing"
}
```
