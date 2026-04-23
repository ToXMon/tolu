---
name: agentic-coding-harness
version: "2.0.0"
description: >
  Production-grade agentic coding harness combining Ralph PRD-driven loops,
  0xSero workflow principles, Ryan Carson's Code Factory and reflection patterns,
  Karpathy coding discipline, and vibe coding task framing.
  Use for fresh builds, projects without PRDs, or any autonomous coding task requiring
  structured BUILD → VERIFY → HARDEN → GATE iteration with session handoff.
trigger_patterns:
  - "start a new project"
  - "build from scratch"
  - "create a workpack"
  - "run autonomous coding"
  - "agentic coding harness"
  - "code harness"
  - "coding workflow"
  - "PRD"
  - "autonomous coding"
  - "reflection"
  - "code factory"
  - "agentic dev"
  - "plan and build"
  - "/workpack"
  - "/audit"
  - "/extract-templates"
  - "/gen-docs"
  - "/diagram"
  - "/daily-review"
  - "/log"
  - "/end"
  - "/reflect"
  - "/code-factory"
license: MIT
metadata:
  author: tolu-agent
  version: "2.0.0"
  sources:
    - https://github.com/snarktank/ralph
    - https://github.com/snarktank/ai-dev-tasks
    - https://emergent.sh/learn/vibe-coding-prompts
  depends_on:
    - karpathy-guidelines
    - deslop
argument-hint: <goal-or-command>
---

# Agentic Coding Harness v2.0

A complete system for autonomous, production-grade software development. Combines:

- **Ralph** — PRD-driven autonomous loop with fresh-context iterations
- **0xSero** — Modular slice architecture, workpack queuing, AGENTS.md knowledge
- **Ryan Carson** — 3-step workflow (PRD → Tasks → Build), Code Factory, reflection prompt
- **Karpathy** — Code discipline (think first, simplicity, surgical changes)
- **Vibe Coding** — Task framing (single objective, user actions, concrete examples)

## Quick Start

The 3 most common entry points:

**1. Start a new project:**
```
/workpack Build a task management API with auth
```

**2. Resume an existing project:**
```
/daily-review
```

**3. End a session with handoff:**
```
/reflect
```

## When to Use This Skill

- Starting a fresh build with no existing PRD
- Setting up autonomous coding sessions (12-16 hour runs)
- Running codebase audits against production standards
- Generating AGENTS.md documentation recursively
- Extracting reusable prompt templates from conversations
- Visualizing data flows with state machine diagrams
- Running Code Factory pipelines (auto-write + auto-review)
- Reflecting on session learnings before closing
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
| `/reflect` | skills/skill.reflection.md | Session reflection + handoff document |
| `/code-factory` | tasks/code_factory.md | Run Code Factory pipeline |

## Instruments (Python CLI Tools)

| Tool | Path | Purpose |
|---|---|---|
| session_logger | instruments/session_logger.py | Track sessions with decisions/blockers/next steps |
| chat_template_extractor | instruments/chat_template_extractor.py | Extract and score reusable prompt templates |
| workpack_generator | instruments/workpack_generator.py | Generate workpack structure from goals |
| agents_md_generator | instruments/agents_md_generator.py | Recursively create AGENTS.md files |
| reflection_logger | instruments/reflection_logger.py | Generate session handoff and reflection docs |

## Reflection Prompt Technique

Before closing any session, force the model to distill learnings:

> "I am going to close this chat session soon and you will lose all memory of this conversation. Please reflect on your progress so far and update the task list document with any details that would be helpful for the next steps. Anything that surprised you, anything that prevented your solution from working — include it all. Focus on distilling your experience into general learnings for the future."

This ensures:
- Learnings persist in `progress.txt` (append-only)
- Discovered patterns update `AGENTS.md`
- PRD task statuses are current
- Next session gets a handoff document

## Code Factory Pattern

Auto-write + auto-review pipeline from Ryan Carson:

```
Write Code → Risk Gate → CI Fanout → Review → Remediate → Merge
```

1. **Coding agent** writes code and opens PR
2. **Risk Policy Gate** classifies tier (Critical/High/Medium/Low)
3. **CI fanout** runs tests, security checks per tier
4. **Code Review Agent** validates (uses `/audit`)
5. **Remediation agent** fixes issues if found
6. **Auto-merge** for low/medium risk changes

See `tasks/code_factory.md` for full pipeline.

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
│   ├── agents_md_generator.py
│   └── reflection_logger.py
├── skills/               ← Slash command skill definitions
│   ├── skill.workpack_planner.md
│   ├── skill.session_documenter.md
│   ├── skill.chat_template_extractor.md
│   ├── skill.codebase_audit.md
│   ├── skill.state_machine_visualizer.md
│   └── skill.reflection.md
├── tasks/                ← Reusable task prompts
│   ├── daily_coding_review.md
│   ├── extract_chat_templates.md
│   ├── recursive_docs_generator.md
│   └── code_factory.md
├── knowledge/            ← Reference documentation
│   ├── 0xsero_coding_standards.md
│   └── agentic_coding_standards.md
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
11. **Reflect before closing** — Every session ends with distilled learnings
12. **Risk-tiered review** — Code Factory gates match change risk level

## Dependencies

This skill works best with:
- **karpathy-guidelines** — Always loaded for code discipline
- **deslop** — Always loaded for output quality
