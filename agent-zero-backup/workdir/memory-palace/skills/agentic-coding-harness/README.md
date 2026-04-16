# Agentic Coding Harness

Production-grade autonomous coding system for Agent Zero. Combines Ralph PRD-driven loops, 0xSero workflow principles, Karpathy coding discipline, and vibe coding task framing.

## Quick Start

```bash
# 1. Skill is already installed at /a0/skills/agentic-coding-harness/
# 2. Load the skill in any conversation:
#    Say: "load agentic-coding-harness" or use any slash command below

# 3. Start a new project:
#    /workpack Build a task management API with auth

# 4. Or run a daily review:
#    /daily-review
```

## Installation

### Already Installed (Default)
The skill lives at `/a0/skills/agentic-coding-harness/`. Agent Zero discovers it automatically.

### Manual Install (Fresh Agent Zero Instance)

```bash
# Copy the entire skill directory
SKILL_DIR="/a0/skills/agentic-coding-harness"
mkdir -p "$SKILL_DIR"

# If copying from memory palace backup
cp -r /a0/usr/workdir/memory-palace/skills/agentic-coding-harness/* "$SKILL_DIR/"

# Verify all files are present
find "$SKILL_DIR" -type f | sort
```

### Wire the System Addon (Optional)

To make the harness behavior persistent across all sessions, add the system addon to your agent's prompt:

**File to edit:** `/a0/prompts/agent.system.main.md`

**Add this line** near the end of the file, after other includes:
```
{{ include "agent.system.addon.agentic-harness.md" }}
```

**Or for a specific agent profile**, add to:
```
/a0/agents/<profile>/prompts/agent.system.main.specifics.md
```

**Or copy the addon to the prompts directory:**
```bash
cp /a0/skills/agentic-coding-harness/prompts/agent.system.addon.agentic-harness.md \
   /a0/prompts/default/agent.system.addon.agentic-harness.md
```

Then add the include directive to your main system prompt.

### Make Python Instruments Executable

```bash
chmod +x /a0/skills/agentic-coding-harness/instruments/*.py
```

## File Map

| Path | Purpose | Lines |
|---|---|---|
| `SKILL.md` | Main skill definition with triggers | ~140 |
| `README.md` | This file — installation & reference | ~170 |
| **Instruments** | **Python CLI tools** | |
| `instruments/session_logger.py` | Log sessions with decisions/blockers/next steps | ~175 |
| `instruments/chat_template_extractor.py` | Extract & score reusable prompt templates | ~241 |
| `instruments/workpack_generator.py` | Generate workpack structure from goals | ~384 |
| `instruments/agents_md_generator.py` | Recursively create AGENTS.md files | ~318 |
| **Skills** | **Slash command definitions** | |
| `skills/skill.workpack_planner.md` | `/workpack` — break goals into tasks | ~107 |
| `skills/skill.session_documenter.md` | `/log` `/end` — session tracking | ~103 |
| `skills/skill.chat_template_extractor.md` | `/extract-templates` — prompt library | ~80 |
| `skills/skill.codebase_audit.md` | `/audit` — codebase health check | ~122 |
| `skills/skill.state_machine_visualizer.md` | `/diagram` — ASCII state machines | ~119 |
| **Tasks** | **Reusable prompt templates** | |
| `tasks/daily_coding_review.md` | `/daily-review` — session start routine | ~125 |
| `tasks/extract_chat_templates.md` | End-of-session template extraction | ~91 |
| `tasks/recursive_docs_generator.md` | `/gen-docs` — AGENTS.md generation | ~117 |
| **Knowledge** | **Reference documentation** | |
| `knowledge/0xsero_coding_standards.md` | Full coding standards reference | ~268 |
| **Prompts** | **System prompt addons** | |
| `prompts/agent.system.addon.agentic-harness.md` | Behavioral defaults | ~88 |
| **Templates** | **File templates** | |
| `templates/prd.json.example` | Ralph-format PRD template | ~62 |

## Slash Command Reference

| Command | What It Does |
|---|---|
| `/workpack <goal>` | Create PRD + workpack with scoped tasks for autonomous execution |
| `/audit` | Check codebase: files >300 lines, dirs >20 files, `any` types, missing AGENTS.md, missing tests |
| `/extract-templates` | Scan conversations, extract reusable prompt templates, score by reusability |
| `/gen-docs` | Recursively generate AGENTS.md in every module with source files |
| `/diagram <module>` | Generate ASCII state machine diagram for data flows |
| `/daily-review` | Full code review vs main branch + daily plan + health check |
| `/log` | Log current session entry (decisions, blockers, next steps) |
| `/end` | End session with summary, update AGENTS.md, set next priorities |

## 10 Core Principles

1. **PRD-first development** — Every feature starts as user stories with acceptance criteria, not code. Convert goals to `prd.json` before writing implementation.

2. **Fresh context iterations** — State lives in files (`prd.json`, `progress.txt`, `AGENTS.md`), not in agent memory. Each iteration reads state fresh.

3. **300 lines per file** — Hard limit. Files that exceed this must be split. This ensures every file fits in one LLM context window.

4. **No `any` types** — Explicit interfaces everywhere. Use `unknown` with type narrowing, generic type parameters, or explicit casts.

5. **Commit on green only** — Quality gates are non-negotiable. Typecheck and tests must pass before any commit.

6. **AGENTS.md is persistent knowledge** — Accumulated patterns, gotchas, and conventions live in AGENTS.md files. Agents read them automatically.

7. **One task per iteration** — Complete one workpack task fully before starting the next. Small, focused, verifiable.

8. **Append-only progress** — Never delete from `progress.txt`. Learnings accumulate. Future iterations benefit from past discoveries.

9. **Surgical changes** — Touch only what the task requires. No drive-by refactoring. No speculative features. Match existing style.

10. **Anti-fragile output** — No AI slop. Production-grade from day one. Apply deslop rules to all generated text.

## Build Loop

```
PRD → Workpack → Task → Build → Verify → Harden → Gate → Commit
  ▲                                              │
  └──────────────── FAIL (retry) ←───────────────┘
```

- **PRD**: User stories with acceptance criteria
- **Workpack**: Scoped tasks with rules and constraints
- **Task**: Single focused unit of work
- **Build**: Implement with karpathy discipline
- **Verify**: Typecheck + tests pass
- **Harden**: Fix failures, apply deslop
- **Gate**: File sizes, types, AGENTS.md, tests all clean
- **Commit**: `feat: [Story ID] - [Title]`

## Workflow Example

```
# Day start
/daily-review                    → Review yesterday, plan today
/workpack Build user auth flow   → Create PRD + 6 tasks

# Autonomous execution
python3 instruments/workpack_generator.py next ./my-project
# ... agent completes task-0001 ...
python3 instruments/workpack_generator.py complete ./my-project 0001
# ... repeat for each task ...

# Day end
/end                             → Log session, update AGENTS.md, set next priorities
```

## Dependencies

- **karpathy-guidelines** — Always active for code discipline
- **deslop** — Always active for output quality
- **Python 3.10+** — Required for instruments (uses `str | None` union syntax)

## Sources

- [Ralph](https://github.com/snarktank/ralph) — PRD-driven autonomous loop
- [Vibe Coding Prompts](https://emergent.sh/learn/vibe-coding-prompts) — Task framing patterns
- [Karpathy Guidelines](https://x.com/karpathy/status/2015883857489522876) — LLM coding discipline
