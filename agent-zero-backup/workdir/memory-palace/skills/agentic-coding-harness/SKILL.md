---
name: agentic-coding-harness
version: "1.0.0"
description: >
  Production-grade agentic coding harness combining Ralph PRD-driven loops,
  0xSero workflow principles, Karpathy coding discipline, and vibe coding task framing.
  Use for fresh builds, projects without PRDs, or any autonomous coding task requiring
  structured BUILD → VERIFY → HARDEN → GATE iteration.
trigger_patterns:
  - "start a new project"
  - "build from scratch"
  - "create a workpack"
  - "run autonomous coding"
  - "agentic coding harness"
  - "/workpack"
  - "/audit"
  - "/extract-templates"
  - "/gen-docs"
  - "/diagram"
  - "/daily-review"
  - "/log"
  - "/end"
license: MIT
metadata:
  author: tolu-agent
  version: "1.0.0"
  sources:
    - https://github.com/snarktank/ralph
    - https://emergent.sh/learn/vibe-coding-prompts
  depends_on:
    - karpathy-guidelines
    - deslop
argument-hint: <goal-or-command>
---

# Agentic Coding Harness

A complete system for autonomous, production-grade software development. Combines:

- **Ralph** — PRD-driven autonomous loop with fresh-context iterations
- **0xSero** — Modular slice architecture, workpack queuing, AGENTS.md knowledge
- **Karpathy** — Code discipline (think first, simplicity, surgical changes)
- **Vibe Coding** — Task framing (single objective, user actions, concrete examples)

## When to Use This Skill

- Starting a fresh build with no existing PRD
- Setting up autonomous coding sessions (12-16 hour runs)
- Running codebase audits against production standards
- Generating AGENTS.md documentation recursively
- Extracting reusable prompt templates from conversations
- Visualizing data flows with state machine diagrams
- Any task requiring BUILD → VERIFY → HARDEN → GATE discipline

## Slash Commands

| Command | File | Description |
|---|---|---|
| `/workpack <goal>` | skills/skill.workpack_planner.md | Break goal into workpack + PRD |
| `/audit` | skills/skill.codebase_audit.md | Check codebase against standards |
| `/extract-templates` | skills/skill.chat_template_extractor.md | Extract reusable prompts |
| `/gen-docs` | tasks/recursive_docs_generator.md | Generate AGENTS.md files |
| `/diagram <module>` | skills/skill.state_machine_visualizer.md | ASCII state machine diagram |
| `/daily-review` | tasks/daily_coding_review.md | Code review + daily plan |
| `/log` | skills/skill.session_documenter.md | Log session entry |
| `/end` | skills/skill.session_documenter.md | End session with summary |

## Instruments (Python CLI Tools)

| Tool | Path | Purpose |
|---|---|---|
| session_logger | instruments/session_logger.py | Track sessions with decisions/blockers/next steps |
| chat_template_extractor | instruments/chat_template_extractor.py | Extract and score reusable prompt templates |
| workpack_generator | instruments/workpack_generator.py | Generate workpack structure from goals |
| agents_md_generator | instruments/agents_md_generator.py | Recursively create AGENTS.md files |

## Build Loop

```
PRD → Workpack → Task → Build → Verify → Harden → Gate → Commit
  ▲                                              │
  └──────────────── FAIL (retry) ←───────────────┘
```

1. **PRD** — Define user stories with acceptance criteria (prd.json)
2. **Workpack** — Break into scoped tasks with rules (.workpack/)
3. **Task** — Pick next pending task
4. **Build** — Implement with karpathy discipline
5. **Verify** — Typecheck + tests pass
6. **Harden** — Fix issues, apply deslop pass
7. **Gate** — 300 lines/file, no `any`, AGENTS.md updated
8. **Commit** — `feat: [Story ID] - [Title]`

## File Structure

```
agentic-coding-harness/
├── SKILL.md              ← You are here
├── README.md             ← Installation and reference
├── instruments/          ← Python CLI tools
│   ├── session_logger.py
│   ├── chat_template_extractor.py
│   ├── workpack_generator.py
│   └── agents_md_generator.py
├── skills/               ← Slash command skill definitions
│   ├── skill.workpack_planner.md
│   ├── skill.session_documenter.md
│   ├── skill.chat_template_extractor.md
│   ├── skill.codebase_audit.md
│   └── skill.state_machine_visualizer.md
├── tasks/                ← Reusable task prompts
│   ├── daily_coding_review.md
│   ├── extract_chat_templates.md
│   └── recursive_docs_generator.md
├── knowledge/            ← Reference documentation
│   └── 0xsero_coding_standards.md
├── prompts/              ← System prompt addons
│   └── agent.system.addon.agentic-harness.md
└── templates/            ← File templates
    └── prd.json.example
```

## Key Principles

1. **PRD-first** — Every feature starts as user stories, not code
2. **Fresh context** — State lives in files, not agent memory
3. **300 lines max** — Files fit in one LLM context window
4. **No `any` types** — Explicit interfaces everywhere
5. **Commit on green** — Quality gates are non-negotiable
6. **AGENTS.md is knowledge** — Accumulated patterns persist across sessions
7. **One task per iteration** — Small, focused, verifiable
8. **Append-only progress** — Never delete learnings
9. **Surgical changes** — Touch only what the task requires
10. **Anti-fragile output** — No AI slop, production-grade from day one

## Dependencies

This skill works best with:
- **karpathy-guidelines** — Always loaded for code discipline
- **deslop** — Always loaded for output quality
