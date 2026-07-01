---
title: DOX Framework — Hierarchical AGENTS.md System
date: 2026-06-18
tags: [dox, agents-md, documentation, context, agent-behavior, framework]
source: https://github.com/agent0ai/dox
license: MIT
---

# DOX Framework

## What It Is

DOX is a hierarchical AGENTS.md framework that gives AI agents precise project context. One Markdown file per domain. Root gives overview, children give precision. Agents read the chain before editing and update it after changes.

Source: [github.com/agent0ai/dox](https://github.com/agent0ai/dox) (MIT License, 82 lines)

## Core Problem It Solves

AI coding agents have a narrow file-level view. They find a file by name and edit it without top-down project context. They guess conventions, cross responsibility boundaries, and miss established patterns. Multiply by 50 tasks and codebases drift.

**The problem was never intelligence. It was context.**

## How It Works

1. **Read Before Editing**: Walk the AGENTS.md chain from root to target file before any edit
2. **Update After Editing**: Run a DOX pass — update the nearest owning AGENTS.md after meaningful changes
3. **Hierarchy**: Root AGENTS.md = project-wide rules + Child DOX Index. Child AGENTS.md = local rules + own Child DOX Index
4. **Closeout**: Re-check changed paths, update docs, refresh indexes, remove stale text

## Agent Zero Integration

- **Global behavior**: Installed via `.dox.promptinclude.md` (auto-injected into every session's system prompt)
- **Skill**: `/a0/usr/skills/dox/SKILL.md` with references and integration guide
- **Trigger phrases**: "initialize dox", "dox tree", "agents.md hierarchy", "project context", "set up dox", "create agents.md", "document project structure", "context boundaries"
- **Delegation protocol**: Subordinates receive DOX instructions in delegation messages
- **Compatibility**: Works with Codex, Claude Code, OpenCode — any agent that supports AGENTS.md

## Child Doc Shape

Default section order: Purpose, Ownership, Local Contracts, Work Guidance, Verification, Child DOX Index

## Key Principles

- AGENTS.md files are **binding work contracts** for their subtrees
- No child doc may weaken DOX
- Closer doc controls local work details; parent docs provide repo-wide rules
- Don't rely on memory — re-read the DOX chain in the current session
- Document stable contracts, not diary entries
- Delete stale notes instead of explaining history

## Files Created

| File | Path | Purpose |
|------|------|---------|
| SKILL.md | `/a0/usr/skills/dox/SKILL.md` | Main skill definition |
| agents-template.md | `/a0/usr/skills/dox/references/agents-template.md` | Raw DOX AGENTS.md template |
| integration-guide.md | `/a0/usr/skills/dox/references/integration-guide.md` | Agent Zero integration patterns |
| promptinclude | `/a0/usr/workdir/.dox.promptinclude.md` | Global behavior rules (always active) |
| memory palace | `tolu/memory-palace/wings/technical/rooms/dox-framework.md` | This file — knowledge reference |
