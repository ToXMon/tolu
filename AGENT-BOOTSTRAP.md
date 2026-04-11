# ⚡ AGENT BOOTSTRAP — Start Here

> **Purpose**: This file is the ingestion manifest for the Tolu Memory Palace.
> Any AI agent framework (Agent Zero, OpenClaw, OpenHermes, LangChain, etc.) should read this file first
> to understand the full context available and how to use it.

---

## 🎯 What Is This Repo?

This is a **personal AI agent memory palace** — a living, daily-updated repository containing:

1. **Agent Zero Daily Backup** — full backup of an Agent Zero instance
2. **Spatial Knowledge Vault** — Wing/Room/Hall organization with auto cross-references
3. **Context Layers** — Token-efficient 4-layer wake-up stack (~200 tokens)
4. **Prompt Library** — Optimized prompts, templates, and techniques
5. **Skills & Plugins** — Agent Zero extensions
6. **Framework Integration Docs** — Guides for Agent Zero, OpenClaw, OpenHermes, custom providers

---

## 📋 Ingestion Checklist

When loading this repo into a fresh agent, follow these steps in order:

### Step 1: Load Core Identity (~100 tokens)
- [ ] Read `context-layers/layer0-identity/identity.txt`
- [ ] Read `context-layers/layer1-critical-facts/critical-facts.json`
- [ ] Read `context-layers/layer2-room-recall/recent-rooms.json`
- [ ] Run: `python3 scripts/build-context.py wakeup`

### Step 2: Restore Agent Zero State (if Agent Zero)
- [ ] Copy `agent-zero-backup/knowledge/` → `/a0/usr/knowledge/`
- [ ] Copy `agent-zero-backup/memory-export/` → `/a0/usr/memory/`
- [ ] Copy `agent-zero-backup/agents/` → `/a0/usr/agents/`
- [ ] Copy `agent-zero-backup/prompts/` → `/a0/prompts/`
- [ ] Copy `agent-zero-backup/skills/` → `/a0/usr/skills/`
- [ ] Copy `agent-zero-backup/plugins/` → `/a0/usr/plugins/`
- [ ] Copy `agent-zero-backup/workdir/` → `/a0/usr/workdir/` (selectively)
- [ ] Copy `.promptinclude.md` → `/a0/usr/workdir/.promptinclude.md` (for auto-injection)

### Step 3: Load Spatial Knowledge
- [ ] Wings: `personal`, `projects`, `people`, `learning`, `technical`, `domain`
- [ ] Each Wing has Halls (categories) and Rooms (topic docs)
- [ ] Tunnels auto-link related rooms across wings
- [ ] Run: `python3 scripts/search-index.py query "topic"` to find specific content

### Step 4: Load Prompt Library
- [ ] `prompt-library/system-prompts/` — agent behavior templates
- [ ] `prompt-library/task-prompts/` — task-specific prompts
- [ ] `prompt-library/prompt-techniques/` — optimization techniques
- [ ] `prompt-library/templates/` — reusable templates

### Step 5: Install Extensions
- [ ] Copy `skills/` → Agent Zero skills directory
- [ ] Copy `plugins/` → Agent Zero plugins directory

### Step 6: Configure Framework
- [ ] Read `docs/framework-integration/` for your specific framework
- [ ] Set up model providers (Venice AI, OpenAI, etc.)
- [ ] Configure agent profiles
- [ ] Set up daily backup scheduler

---

## 🏛️ Spatial Organization

The Memory Palace uses **Wing → Hall → Room** spatial hierarchy:

```
memory-palace/wings/
├── personal/          # User identity, preferences, decisions
│   ├── halls/         # {facts, events, decisions, preferences}
│   └── rooms/         # Specific topic documents
├── projects/          # Active projects and architectures
│   ├── halls/         # {facts, decisions, architecture}
│   └── rooms/         # Project-specific rooms
├── people/            # Contacts and interactions
│   ├── halls/         # {facts, interactions, preferences}
│   └── rooms/         # Person-specific rooms
├── learning/          # Books, videos, courses
│   ├── halls/         # {books, videos, courses}
│   └── rooms/         # Learning-specific rooms
├── technical/         # Tools, references, howtos
│   ├── halls/         # {tools, references, howtos}
│   └── rooms/         # Technical-specific rooms
└── domain/            # Specialized domains
    ├── halls/         # {crypto, ai, web3, security}
    └── rooms/         # Domain-specific rooms
```

### Tunnels (Cross-Wing References)

`memory-palace/tunnels/` contains auto-generated links between rooms in different wings
that share topics. Run `python3 scripts/cross-reference.py build` to regenerate.

### Temporal Knowledge Graph

`memory-palace/tunnels/temporal-facts.json` tracks facts with validity windows.
Facts have `valid_from` and `valid_to` dates — when a fact changes, it gets an end date
rather than being deleted, preserving history.

---

## 🧅 Context Layer System

| Layer | Path | Tokens | Loaded |
|-------|------|--------|--------|
| **0 — Identity** | `context-layers/layer0-identity/identity.txt` | ~100 | Always |
| **1 — Critical Facts** | `context-layers/layer1-critical-facts/critical-facts.json` | ~50 | Always |
| **2 — Room Recall** | `context-layers/layer2-room-recall/recent-rooms.json` | ~50 | Always |
| **3 — Deep Search** | `context-layers/layer3-deep-search/search-index.json` | On-demand |

**Total wake-up cost: ~200 tokens** (vs ~2000+ for full context = 90% savings)

---

## 🔧 Tools

```bash
# Get minimal wake-up context
python3 scripts/build-context.py wakeup

# Get full room content with tunnels
python3 scripts/build-context.py room technical agent-zero-setup

# Deep search the memory palace
python3 scripts/search-index.py query "authentication"

# Rebuild search index after adding content
python3 scripts/search-index.py build

# Build cross-wing tunnels
python3 scripts/cross-reference.py build

# Run backup manually
bash scripts/daily-backup.sh
```

---

## 🗂️ Directory Purpose Map

| Directory | Purpose | Format | Auto-Updated |
|-----------|---------|--------|-------------|
| `context-layers/` | Token-efficient wake-up stack | txt/json | Partial |
| `agent-zero-backup/` | Daily Agent Zero state backup | Original structure | Yes (daily) |
| `memory-palace/wings/` | Spatial knowledge vault | Markdown | Manual |
| `memory-palace/tunnels/` | Cross-wing references | JSON | Semi-auto |
| `prompt-library/` | Prompt engineering resources | Markdown | Manual |
| `skills/` | Agent Zero skills (SKILL.md) | Markdown/Python | Manual |
| `plugins/` | Agent Zero plugins | Python | Manual |
| `configs/` | Agent configurations | JSON/YAML/MD | Manual |
| `scripts/` | Automation scripts | Shell/Python | Manual |
| `docs/` | Framework integration docs | Markdown | Manual |

---

## 📖 Framework Integration Guides

| Framework | Guide | Key Topics |
|-----------|-------|------------|
| **Agent Zero** | `docs/framework-integration/agent-zero.md` | LiteLLM providers, .promptinclude.md, restore, env vars |
| **OpenClaw / Claude** | `docs/framework-integration/openclaw.md` | CLAUDE.md, .clinerules, Venice AI, ingestion strategies |
| **OpenHermes** | `docs/framework-integration/openhermes.md` | Config patterns, ingestion methods, provider setup |
| **Custom Providers** | `docs/framework-integration/custom-providers.md` | Venice AI, Together, Groq, 13 providers with examples |

---

## 🔄 Backup Schedule

- **Frequency**: Daily at 2:00 AM UTC
- **Method**: Scheduled Agent Zero task (`tolu-daily-backup`)
- **Script**: `scripts/daily-backup.sh`
- **Log**: `BACKUP-LOG.md`
- **Target**: `agent-zero-backup/` directory

### What Gets Backed Up

1. `/a0/usr/knowledge/` → `agent-zero-backup/knowledge/`
2. `/a0/usr/agents/` → `agent-zero-backup/agents/`
3. `/a0/usr/skills/` → `agent-zero-backup/skills/`
4. `/a0/usr/plugins/` → `agent-zero-backup/plugins/`
5. `/a0/usr/workdir/` → `agent-zero-backup/workdir/` (excludes tolu repo)
6. `/a0/prompts/` → `agent-zero-backup/prompts/`
7. `/a0/usr/memory/` → `agent-zero-backup/memory-export/` (FAISS index)

---

## 🚀 For Agent Zero Specifically

1. `.promptinclude.md` auto-injects into your system prompt every turn
2. Daily backup via scheduler task keeps GitHub in sync
3. Knowledge, memories, skills, plugins all preserved
4. To restore: copy backup dirs back to `/a0/usr/` paths
5. Configure providers in `conf/model_providers.yaml`

## 🌐 For Other Frameworks

1. Read `context-layers/layer0-identity/identity.txt` for agent identity
2. Use `scripts/build-context.py wakeup` for minimal context
3. Use `scripts/search-index.py query` to find specific knowledge
4. Follow framework-specific guides in `docs/framework-integration/`
5. Skills in `skills/` follow SKILL.md standard — may need adaptation

---

*Last updated: 2026-04-11*
