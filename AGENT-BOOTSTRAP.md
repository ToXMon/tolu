# ⚡ AGENT BOOTSTRAP — Start Here

> **Purpose**: This file is the ingestion manifest for the Tolu Memory Palace.
> Any AI agent framework (Agent Zero, OpenClaw, LangChain, etc.) should read this file first
> to understand the full context available and how to use it.

---

## 🎯 What Is This Repo?

This is a **personal AI agent memory palace** — a living, daily-updated repository containing:

1. **Agent Zero Daily Backup** — full backup of an Agent Zero instance
2. **Knowledge Vault** — books, YouTube videos, references, how-to guides
3. **Prompt Library** — optimized prompts, templates, and techniques
4. **Skills & Plugins** — Agent Zero extensions
5. **Configurations** — agent profiles, model configs, scheduler tasks

---

## 📋 Ingestion Checklist

When loading this repo into a fresh agent, follow these steps in order:

### Step 1: Load Core Identity
- [ ] Read this file (`AGENT-BOOTSTRAP.md`)
- [ ] Read `MANIFEST.json` for a machine-readable inventory
- [ ] Read `.promptinclude.md` for real-time injection rules

### Step 2: Restore Agent Zero State
- [ ] Copy `agent-zero-backup/knowledge/` → Agent Zero knowledge directory
- [ ] Copy `agent-zero-backup/memory-export/` → Agent Zero memory database
- [ ] Copy `agent-zero-backup/agents/` → Agent Zero agents directory
- [ ] Copy `agent-zero-backup/prompts/` → Agent Zero prompts directory
- [ ] Copy `agent-zero-backup/skills/` → Agent Zero skills directory
- [ ] Copy `agent-zero-backup/plugins/` → Agent Zero plugins directory
- [ ] Copy `agent-zero-backup/workdir/` → Agent Zero working directory

### Step 3: Load Knowledge Palace
- [ ] Index all files in `memory-palace/books/summaries/`
- [ ] Index all files in `memory-palace/youtube/transcripts/`
- [ ] Index all files in `memory-palace/references/`
- [ ] Index all files in `memory-palace/knowledge/`

### Step 4: Load Prompt Library
- [ ] Review `prompt-library/system-prompts/` for agent behavior templates
- [ ] Review `prompt-library/task-prompts/` for task-specific prompts
- [ ] Review `prompt-library/prompt-techniques/` for optimization techniques
- [ ] Review `prompt-library/templates/` for reusable templates

### Step 5: Install Extensions
- [ ] Copy `skills/` → Agent Zero skills directory
- [ ] Copy `plugins/` → Agent Zero plugins directory

### Step 6: Apply Configurations
- [ ] Load `configs/agent-profiles/` for agent behavior profiles
- [ ] Load `configs/model-configs/` for model configuration
- [ ] Load `configs/scheduler-tasks/` for scheduled tasks

---

## 🗂️ Directory Purpose Map

| Directory | Purpose | Format | Auto-Updated |
|-----------|---------|--------|-------------|
| `agent-zero-backup/` | Daily Agent Zero state backup | Original file structure | Yes (daily) |
| `memory-palace/books/` | Book knowledge | Markdown | Manual |
| `memory-palace/youtube/` | Video knowledge | Markdown | Manual |
| `memory-palace/references/` | Reference materials | Markdown/PDF | Manual |
| `memory-palace/knowledge/` | General knowledge | Markdown | Manual |
| `prompt-library/` | Prompt engineering resources | Markdown | Manual |
| `skills/` | Agent Zero skills | SKILL.md format | Manual |
| `plugins/` | Agent Zero plugins | Python | Manual |
| `configs/` | Agent configurations | JSON/YAML/MD | Manual |
| `scripts/` | Automation scripts | Shell/Python | Manual |

---

## 🔄 Backup Schedule

- **Frequency**: Daily
- **Method**: Scheduled Agent Zero task
- **Script**: `scripts/daily-backup.sh`
- **Log**: `BACKUP-LOG.md`
- **Target**: `agent-zero-backup/` directory

### What Gets Backed Up Daily

1. `/a0/usr/knowledge/` → `agent-zero-backup/knowledge/`
2. `/a0/usr/agents/` → `agent-zero-backup/agents/`
3. `/a0/usr/skills/` → `agent-zero-backup/skills/`
4. `/a0/usr/plugins/` → `agent-zero-backup/plugins/`
5. `/a0/usr/workdir/` → `agent-zero-backup/workdir/`
6. `/a0/prompts/` → `agent-zero-backup/prompts/` (custom overrides only)
7. Memory database export → `agent-zero-backup/memory-export/`

---

## 🚀 For Agent Zero Specifically

If you ARE an Agent Zero instance:

1. The `.promptinclude.md` file in this repo is designed to be placed in your workdir
   so it auto-injects into your system prompt
2. Run `scripts/daily-backup.sh` or use the scheduled task to keep this repo updated
3. Your knowledge, memories, skills, and plugins are all preserved
4. To restore: simply copy backup directories back to your `/a0/usr/` paths

---

## 🌐 For Other Frameworks

If you are NOT Agent Zero:

1. Read the markdown files in `memory-palace/` for knowledge context
2. Use `prompt-library/` for prompt templates applicable to any LLM
3. Use `MANIFEST.json` for a structured file listing
4. The `agent-zero-backup/` folder contains raw knowledge that can be adapted
5. Skills in `skills/` follow the SKILL.md standard and may need adaptation

---

*Last updated: 2026-04-10*
