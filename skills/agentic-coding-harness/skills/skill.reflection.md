---
name: reflection
version: 2.0.0
triggers:
  - /reflect
  - "reflect on session"
  - "session reflection"
  - "close session"
  - "end session"
  - "wrap up session"
requires:
  - instruments/reflection_logger.py
produces:
  - work_logs/reflection_*.md
  - work_logs/handoff_*.json
  - progress.txt (appended)
  - AGENTS.md (patterns updated)
---

# Session Reflection Skill

Force the model to distill learnings, update project memory, and generate a
session handoff before closing a coding session.

## Activation

Trigger this skill when the user says any of: `/reflect`, `reflect on session`,
`session reflection`, `close session`, `wrap up session`.

## Procedure

### Step 1 — Collect Session Context

Before asking the model anything, gather the raw material:

1. Read `progress.txt` for accumulated project history.
2. Read the latest `work_logs/session_*.json` if one exists.
3. Scan `work_logs/` for any CI reports, test results, or audit outputs
   from this session.
4. Read `AGENTS.md` to see currently recorded patterns.
5. Read `prd.json` to check task completion status.

Present all of this context to the model in a single prompt (see
*The Reflection Prompt* below).

### Step 2 — Run the Reflection Prompt

Send the full reflection prompt (see below) with the gathered context
injected. The model must answer every section. Do not allow skipping.

### Step 3 — Process Model Output

From the model's structured response, extract:

| Field | Destination |
|-------|-------------|
| Summary + Surprises | Append to `progress.txt` |
| Discovered Patterns | Insert into `AGENTS.md` under `## Discovered Patterns` |
| Completed Task IDs | Update `prd.json` passes status to `done` |
| Blockers | Record in `progress.txt` and handoff JSON |
| Next Steps | Record in handoff JSON |

### Step 4 — Generate Handoff Artifacts

Run the reflection logger instrument:

```bash
python3 instruments/reflection_logger.py reflect <project_dir> \
  --summary "<extracted summary>" \
  --surprises "<extracted surprises>" \
  --blocked "<extracted blockers>" \
  --next "<extracted next steps>"
```

This writes:
- `work_logs/reflection_YYYY-MM-DD_HHMMSS.md` — human-readable handoff
- `work_logs/handoff_YYYY-MM-DD_HHMMSS.json` — machine-readable handoff

### Step 5 — Confirm and Present

Show the user:
1. The reflection markdown (or a summary of key learnings)
2. What was written to `progress.txt`
3. Any new patterns added to `AGENTS.md`
4. Updated `prd.json` task statuses
5. Path to the handoff JSON for the next session

---

## The Reflection Prompt

Copy and send the following prompt, filling in the bracketed sections with
gathered context:

```
You are closing a coding session. Before we end, perform a structured
reflection. Answer EVERY section below. Do not skip any.

---

## Session Context

### Recent Progress
<insert last 40 lines of progress.txt>

### Latest Session Log
<insert contents of latest work_logs/session_*.json>

### Current AGENTS.md Patterns
<insert the ## Discovered Patterns section from AGENTS.md>

### PRD Task Status
<insert relevant tasks from prd.json>

---

## Required Reflection

### 1. Summary
What was accomplished in this session? Be specific. List concrete changes:
files created/modified, tests passing, bugs fixed, features shipped.

### 2. Surprises
What did you discover that you didn't expect? This includes:
- Unexpected behavior in libraries or frameworks
- Architecture insights that changed your approach
- Performance characteristics you didn't anticipate
- Dependencies or constraints you only discovered mid-work
- Things that should be recorded for future sessions

### 3. Blockers
What is currently blocked or unresolved? Include:
- Open bugs or failing tests
- Missing dependencies or blocked PRs
- Architectural decisions still pending
- Anything the next session needs to address immediately

### 4. Discovered Patterns
What reusable patterns emerged? These go into AGENTS.md:
- Naming conventions that worked well
- Error handling patterns worth repeating
- Architecture decisions and their rationale
- Gotchas specific to this codebase
- Testing strategies that proved effective

### 5. PRD Task Updates
For each task in prd.json, report:
- Task ID and name
- Current status (not started / in progress / done / blocked)
- If done: brief evidence (tests pass, feature works)
- If blocked: what's blocking it

### 6. Next Steps
What should the next session tackle first? Prioritize:
- Unblock any blockers listed above
- Continue in-progress tasks
- Start the next highest-priority task
- Any prep work the next session should do before coding

---

Output your reflection in the exact section order above.
Be honest. Be specific. No filler.
```

---

## File References

- `instruments/reflection_logger.py` — CLI tool that writes the artifacts
- `progress.txt` — Running session log (appended, never overwritten)
- `AGENTS.md` — Project memory with discovered patterns section
- `prd.json` — Product requirements with task-level tracking
- `work_logs/` — Directory for session and reflection artifacts
