# Ryan Carson — AI-First Coding Workflow & Philosophy

**Research Date**: 2026-04-16
**Subject**: Ryan Carson (snarktank on GitHub), 5x founder, Builder in Residence at Amp (Sourcegraph)

---

## Core Philosophy

- **No moat in AI coding agents**: Everything is API calls + system prompts. Winning = elbow grease + DX tuning
- **Quality remains elusive**: "All of it is dev vibes" — no reliable programmatic evals for open-ended agents
- **Slow down to speed up**: Providing proper context is the secret to faster AI development
- **Structured > vibe coding**: Vibe coding works when systematized through PRDs + task lists
- **Human as engineering manager**: Developer shifts to curating process, writing specs, guiding AI
- **No one-shot magic**: Continuous refinement and monitoring required
- **Context window discipline**: Fresh agent per task, only PRD + current task in scope
- **File-based memory persistence**: AGENTS.md, progress.txt, prd.json — no complex vector DBs needed

---

## The 3-Step (Actually 5-Step) Workflow

### Overview: Three-File System
1. PRD (Product Requirements Document)
2. Task List (generated from PRD)
3. Task Execution (one at a time, with verification)

### Detailed 5-Step Process

**Step 1: Create PRD**
- Use `create-prd.mdc` command
- Prompt: `Use @create-prd.mdc Here's the feature I want to build: [Describe in detail] Reference these files: [@file1 @file2]`
- Use voice-to-text (MacWhisper) to brain-dump context about problem, reasoning, technical details
- AI asks clarifying questions, user answers, detailed PRD generated
- Always use MAX mode with biggest/smartest model (Gemini 2.5, o3, Opus 4)

**Step 2: Generate Task List**
- Use `generate-tasks-from-prd.mdc` command
- Prompt: `Now take @MyFeature-PRD.md and create tasks using @generate-tasks-from-prd.mdc`
- AI generates top-level tasks, user reviews/edits
- AI breaks into granular sub-tasks designed for AI as junior engineer

**Step 3: Examine Task List**
- Review generated tasks and sub-tasks
- Ensure clear roadmap before execution

**Step 4: Execute Tasks**
- Use `process-task-list.mdc` command
- Ensure clean git status before starting
- Open new chat (fresh context window)
- Instruct AI to start on single specific task (e.g., task 1.1)
- Can take up to 1 hour per task

**Step 5: Review, Approve, Progress**
- Review AI changes
- If correct: reply "yes" to mark complete, commit, move to next
- If incorrect: provide feedback for correction
- Task list is a living document

---

## Complexity Thresholds

- **Don't use for**: Tasks completable in <30 minutes (overhead not worth it)
- **Don't use for**: Massive features requiring months (context window degrades, plans become vague/brittle)
- **For massive projects**: Break into smaller "build stages" and apply process recursively

---

## The Ralph Wiggum Technique

- **What**: Continuous coding loop where a script repeatedly invokes AI agent to tackle small tasks one by one
- **How**: Simple Bash/Python script runs agent, resets context each iteration, persists memory via git history and text files
- **Memory**: AGENTS.md acts as running notebook, agent appends key learnings and discovered patterns so future iterations learn from past mistakes
- **Scaling vision**: Run 10+ parallel agent loops overnight on different feature branches
- **Created by**: Geoffrey Huntley, promoted by Carson
- **Repo**: github.com/snarktank/ralph

---

## The Reflection Prompt (Critical)

When closing a chat session after human intervention:

> "I am going to close this chat session soon and you will lose all memory of this conversation. Please reflect on your progress so far and update the task list document (@tasks-prd-my-feature.md) with any details that would be helpful for you to perform the next steps in our plan more effectively. Anything that surprised you, anything that prevented your solution from working and required debugging or troubleshooting - include it all. Do not go into specifics of the current task, no need for a progress report, focus on distilling your experience into a set of general learnings for the future."

---

## Code Factory Pattern

### Overview
Setup so agents can auto-write and review 100% of code (788K views, 7.9K bookmarks on X).

### Workflow Loop
1. Coding Agent writes code, opens PR
2. Risk Policy Gate (preflight) classifies risk tier
3. CI Fanout runs tests, security checks, browser evidence
4. Code Review Agent validates PR
5. If findings: Remediation Agent fixes, pushes, re-reviews
6. If clean: Auto-resolve bot threads, Merge (auto-merge for low/medium risk)

### Risk Tiers
| Tier | Files | Requirements |
|------|-------|------------|
| Critical | DB schemas, workflows, auth | Policy gate + Greptile + CI + Browser evidence |
| High | API routes, tools, libraries | Policy gate + Greptile + CI |
| Medium | App code, components | Policy gate + CI |
| Low | Docs, README | Policy gate only |

### Key Scripts
- `risk-policy-gate.ts` - Preflight gate
- `compute-risk-tier.ts` - Classify changed files
- `review-gate.ts` - SHA-disciplined review
- `remediate.ts` - Automated fix loop
- `auto-resolve-threads.ts` - Resolve bot-only threads
- `verify-review-state.ts` - Ensure review matches HEAD SHA

---

## Design System Enforcement (5-Layer)

From tweet with 817+ likes. Layers:
1. Canonical docs
2. Agent routing
3. Custom lint rules
4. Pre-commit hooks
5. CI gates

Goal: Deterministic design enforcement so agents cannot deviate from design system.

---

## Tools Stack

### Primary
- **Cursor** - Main IDE with Agent Mode
- **Claude / Claude Code** - Primary coding agent
- **ChatGPT** - Alternative chat model
- **Gemini 2.5 Pro** - High-capability planning model

### Context Management
- **Repo Prompt** - Precise control over context sent to AI
- **MacWhisper** - Voice-to-text for brain-dumping PRD context

### Task Management
- **AI Dev Tasks (.mdc files)** - create-prd, generate-tasks, process-task-list
- **Task Master** - CLI task automation (Carson found it less reliable than manual PRD process)

### MCPs (Model Context Protocols)
- **Browserbase** - Headless browser for front-end testing
- **Stagehand** - Front-end testing automation

### CI/Review
- **Greptile** - AI code review
- **GitHub Actions** - Risk policy gates, CI fanout

### AI Agent Loops
- **Amp** (Sourcegraph) - Coding agent where Carson was Builder in Residence
- **Ralph** - Autonomous loop script (his repo)
- **Cursor Background Agent** - Background PR creation and review

---

## Cursor Agent Mode Specifics

- Always use `@` to reference specific files (e.g., `@MyFeature-PRD.md`)
- Use MAX mode for PRD creation (more thorough, higher quality)
- Only reference `@process-task-list.mdc` for first task; instructions guide AI for subsequent tasks
- Start each new task with fresh chat (clean context window)
- Keep clean git status so you can reset or check diffs at any time

---

## Cursor Background Agent Workflow

- Create PRD, Create task list, Hand off to Cursor Background Agent
- Agent works in background, creates PR
- User reviews and merges PR
- "Anyone can now have a whole team of AI junior devs working in the background"

---

## Context Window Management

- **Fresh agent per task**: New chat for each task execution, only PRD + current task in scope
- **File-based persistence**: AGENTS.md, progress.txt, prd.json
- **Reflection prompt**: Force model to distill learnings before closing session
- **Reduce scope**: Agent only needs to understand PRD + specific task, not entire project
- **Task list as living document**: Updated with learnings, pruned as development progresses

---

## GitHub Repos

| Repo | Description |
|------|-------------|
| [snarktank/ai-dev-tasks](https://github.com/snarktank/ai-dev-tasks) | 5K+ stars. The core .mdc template system |
| [snarktank/ralph](https://github.com/snarktank/ralph) | Autonomous AI agent loop that runs until PRD items complete |
| [snarktank/antfarm](https://github.com/snarktank/antfarm) | Build agent team in OpenClaw with one command |
| [lemmylabh/Ryan-Carson](https://github.com/lemmylabh/Ryan-Carson) | Community implementation of his task management system |
| [cecvic/code-factory](https://github.com/cecvic/code-factory) | Code Factory agent auto-write and review pipeline |
| [Greging/code-factory-template](https://github.com/Greging/code-factory-template) | Template repo for fully autonomous AI code writing |

---

## Key Quotes

- "All of it is dev vibes" - on AI coding agent quality evaluation
- "There is no one-shot fully autonomous magic" - via Addy Osmani
- "Slowing down to provide proper context is the secret to speeding up your AI development"
- "The entire human race is now fitting to evals" - on codifying intuitive mental models
- "Anyone can now have a whole team of AI junior devs working in the background"
- Founders can now "build entire companies with minimal engineering teams"

---

## Background Context

- **Treehouse** (teamtreehouse.com): Taught 1M+ people to code. Informs his structured teaching approach
- **Amp (Sourcegraph)**: Builder in Residence. Learned coding agent internals
- **5x founder**: 20 years building, scaling, and selling startups
- **Personal site**: ryancarson.com
- **GitHub**: github.com/snarktank
- **X/Twitter**: @ryancarson

---

## Sources

1. Lenny's Newsletter - https://www.lennysnewsletter.com/p/a-3-step-ai-coding-workflow-for-solo
2. Freeplay Blog - https://freeplay.ai/blog/real-talk-on-building-coding-agents-a-conversation-with-amp-s-builder-in-residence-ryan-carson
3. Addy Osmani - https://addyosmani.com/blog/self-improving-agents/
4. Kovyrin Blog - https://kovyrin.net/2025/06/20/prd-tasklist-process/
5. YouTube/Podcast - https://www.youtube.com/watch?v=fD4ktSkNCw4
6. GitHub AI Dev Tasks - https://github.com/snarktank/ai-dev-tasks
7. X/Twitter posts - @ryancarson (multiple)
8. Code Factory - https://www.ryancarson.com/articles/x-post-2023452909883609111
9. FusionChat - https://fusionchat.ai/news/boost-your-ai-development-practical-tips-from-ryan-carson
