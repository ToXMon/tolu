---
name: recursive-docs-generator
version: "1.0.0"
trigger: /gen-docs
description: >
  Recursive AGENTS.md generation with root overview first, then every module.
  Generates documentation that agents and humans can read for context.
---

# Recursive Docs Generator

Slash command: `/gen-docs`

## When to use
- At project start to create initial AGENTS.md files
- After major restructuring
- When onboarding new agents or developers
- After audit reveals missing AGENTS.md files

## Execution Steps

### Step 1: Verify Project Directory

Confirm the project directory exists and identify its structure:
```bash
ls <project_dir> && echo '---' && find <project_dir> -maxdepth 2 -type d \
  ! -path '*/node_modules/*' ! -path '*/.git/*' ! -path '*/__pycache__/*' \
  ! -path '*/venv/*' ! -path '*/dist/*' ! -path '*/build/*' | head -30
```

### Step 2: Generate Root AGENTS.md

The root AGENTS.md should contain:

1. **Project overview** — Name, purpose, tech stack
2. **Architecture** — High-level module layout
3. **Development setup** — How to run, test, deploy
4. **Key conventions** — Coding standards, naming patterns
5. **Module map** — Links to all submodule AGENTS.md files
6. **Patterns section** — For agents to fill with discovered conventions

Example root AGENTS.md structure:
```markdown
# AGENTS.md — Project Root

## Overview
[Project name and purpose]

## Tech Stack
- Runtime: [Node/Python/etc]
- Framework: [Express/FastAPI/etc]
- Database: [Postgres/SQLite/etc]
- Testing: [Jest/pytest/etc]

## Architecture
[Module layout diagram]

## Commands
- Install: `npm install` / `pip install -r requirements.txt`
- Dev: `npm run dev` / `python main.py`
- Test: `npm test` / `pytest`
- Build: `npm run build` / `python setup.py build`

## Modules
- [src/auth/](src/auth/AGENTS.md) — Authentication
- [src/api/](src/api/AGENTS.md) — API routes
- [src/db/](src/db/AGENTS.md) — Database layer

## Conventions
- File size limit: 300 lines
- No `any` types
- Tests required for all new code
```

### Step 3: Generate Module-Level AGENTS.md Files

Run the generator instrument:
```bash
python3 /a0/skills/agentic-coding-harness/instruments/agents_md_generator.py generate <project_dir>
```

### Step 4: Verify Coverage

Check that all modules with source files have AGENTS.md:
```bash
python3 /a0/skills/agentic-coding-harness/instruments/agents_md_generator.py verify <project_dir>
```

### Step 5: Report Results

Display:
```
=== Documentation Generation Complete ===
Project: [name]
Root AGENTS.md: [created/updated]
Module AGENTS.md files: [count] created
Missing coverage: [count] (should be 0)

Module map:
  [project-root]/
  ├── AGENTS.md (root)
  ├── src/auth/AGENTS.md
  ├── src/api/AGENTS.md
  ├── src/db/AGENTS.md
  └── ...

Note: Patterns sections are empty. Agents will populate them during development.
```

## Update Mode

To update existing AGENTS.md files while preserving patterns:
```bash
python3 /a0/skills/agentic-coding-harness/instruments/agents_md_generator.py update <project_dir>
```

This regenerates file lists and exports while keeping hand-written pattern notes intact.
