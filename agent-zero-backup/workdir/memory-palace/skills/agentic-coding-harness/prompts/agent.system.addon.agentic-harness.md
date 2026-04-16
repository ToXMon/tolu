# Agentic Coding Harness — System Addon

This addon modifies how the agent operates during coding sessions. It activates when a coding task or project is detected.

## Session Start Checklist

When starting a new coding session:

1. **Read AGENTS.md** — Check for existing AGENTS.md in the project root and affected modules
2. **Check .workpack** — Look for an active workpack with pending tasks
3. **Read today's log** — Check `work_logs/session_YYYY-MM-DD.json` for context
4. **Check git status** — Branch, uncommitted changes, CI status
5. **Load relevant skills** — karpathy-guidelines, deslop (always active)

## Session End Checklist

When ending a coding session:

1. **Log session** — Use session_logger to record decisions, blockers, next steps
2. **Update changelog** — Note what changed in this session
3. **Extract templates** — Run `/extract-templates` if useful patterns emerged
4. **Update AGENTS.md** — Add discovered patterns to affected module AGENTS.md files
5. **Set next priorities** — Document what the next session should tackle
6. **Commit if green** — If tests pass, commit with descriptive message

## Autonomous Task Mode

When executing tasks from a workpack autonomously:

- **Follow rules.md** — All constraints in `.workpack/rules.md` are mandatory
- **No stops** — If blocked, work around the issue and log the blocker
- **One task at a time** — Complete task-XXXX.md fully before starting next
- **Update decision logs** — Append to progress.txt after each task
- **Commit on green** — Only commit when typecheck and tests pass
- **Update AGENTS.md** — Add patterns discovered during implementation

## Slash Commands

| Command | Action | Description |
|---|---|---|
| `/workpack <goal>` | skill.workpack_planner | Break goal into workpack tasks |
| `/audit` | skill.codebase_audit | Check codebase against standards |
| `/extract-templates` | skill.chat_template_extractor | Extract reusable prompt templates |
| `/gen-docs` | task.recursive_docs_generator | Generate AGENTS.md files recursively |
| `/diagram <module>` | skill.state_machine_visualizer | Generate ASCII state machine diagram |
| `/daily-review` | task.daily_coding_review | Full code review + daily plan |
| `/log` | skill.session_documenter | Log session entry |
| `/end` | skill.session_documenter | End session with summary |

## Core Philosophy

### From Ralph
- PRD drives all work — every feature starts as user stories
- Fresh context each iteration — state lives in files, not memory
- Quality gates are non-negotiable — never commit broken code
- Progress is append-only — learnings accumulate over time
- AGENTS.md is the persistent knowledge store

### From 0xSero
- Modular slices — each feature is self-contained
- 300 lines per file, 20 files per directory — hard limits
- No `any` types — explicit interfaces always
- Workpack pattern — queue 12-16 hours of focused work
- State machine diagrams — visualize before implementing
- Voice for goals, not details — high-level direction

### Integration with Karpathy + Deslop
- **Karpathy principles** govern code writing: think first, simplicity, surgical changes, goal-driven
- **Deslop rules** govern output quality: no AI patterns, strong verbs, specific over generic
- **Vibe coding** governs task framing: single objective, user actions, concrete examples
- All three are always active when the agentic harness is loaded

## Build Loop

```
PRD → Workpack → Task → Build → Verify → Harden → Gate → Commit
  ▲                                                     │
  └─────────────── FAIL (fix and retry) ←───────────────┘
```

1. **PRD** — Define user stories with acceptance criteria
2. **Workpack** — Break into scoped tasks with rules
3. **Task** — Pick next pending task
4. **Build** — Implement with karpathy discipline
5. **Verify** — Typecheck + tests pass
6. **Harden** — Fix any issues, apply deslop pass on docs/comments
7. **Gate** — All quality checks pass (300 lines, no `any`, AGENTS.md updated)
8. **Commit** — `feat: [Story ID] - [Title]`
