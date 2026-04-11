# 🏛️ TOLU — Agent Memory Palace

> A self-documenting, portable knowledge base and daily backup system for AI agent frameworks.
> Designed so **any fresh agent** (Agent Zero, OpenClaw, or similar) can ingest this repo and gain immediate context.

---

## 🚀 Quick Start for Fresh Agents

1. Read **[AGENT-BOOTSTRAP.md](./AGENT-BOOTSTRAP.md)** — this is your ingestion manifest
2. Scan **[agent-zero-backup/](./agent-zero-backup/)** — the latest Agent Zero daily backup
3. Browse **[memory-palace/](./memory-palace/)** — organized knowledge, books, YouTube, references
4. Check **[prompt-library/](./prompt-library/)** — optimized prompts and templates
5. Install **[skills/](./skills/)** and **[plugins/](./plugins/)** — Agent Zero extensions

---

## 📂 Repository Structure

```
tolu/
├── AGENT-BOOTSTRAP.md          # ⚡ START HERE — agent ingestion manifest
├── MANIFEST.json               # Machine-readable repo inventory
├── .promptinclude.md           # Auto-injected into Agent Zero system prompt
│
├── agent-zero-backup/          # 🔄 Daily automated backup of Agent Zero
│   ├── agents/                 #   Agent profiles and configurations
│   ├── knowledge/              #   Knowledge base (fragments, solutions, main)
│   ├── memory-export/          #   Memory database snapshots
│   ├── plugins/                #   Installed plugins and configs
│   ├── prompts/                #   Custom prompt overrides
│   ├── skills/                 #   Custom skills (SKILL.md files)
│   └── workdir/                #   Working directory files
│
├── memory-palace/              # 🏛️ The Knowledge Vault
│   ├── books/                  #   Book summaries, references, reading lists
│   │   ├── summaries/          #     Condensed book summaries
│   │   ├── references/         #     Key excerpts and citations
│   │   └── reading-lists/      #     Curated reading lists by topic
│   ├── youtube/                #   YouTube video knowledge
│   │   ├── channels/           #     Channel profiles and top videos
│   │   ├── playlists/          #     Curated playlist collections
│   │   └── transcripts/        #     Video transcripts and key takeaways
│   ├── references/             #   Reference materials
│   │   ├── technical/          #     Technical docs and guides
│   │   ├── academic/           #     Papers and academic references
│   │   └── tools/              #     Tool documentation
│   └── knowledge/              #   General and domain knowledge
│       ├── general/            #     Broad knowledge articles
│       ├── domain-specific/    #     Specialized domain knowledge
│       └── howtos/             #     Step-by-step guides
│
├── prompt-library/             # 📝 Prompt Engineering Vault
│   ├── system-prompts/         #   System prompt templates
│   ├── task-prompts/           #   Task-specific prompt templates
│   ├── prompt-techniques/      #   Techniques (chain-of-thought, few-shot, etc.)
│   └── templates/              #   Reusable prompt templates
│
├── skills/                    # 🛠️ Agent Zero Custom Skills
├── plugins/                   # 🔌 Agent Zero Custom Plugins
├── configs/                    # ⚙️ Configuration Files
│   ├── agent-profiles/         #   Agent profile definitions
│   ├── model-configs/          #   Model configuration presets
│   └── scheduler-tasks/        #   Scheduled task definitions
│
├── scripts/                   # 🔧 Automation Scripts
│   └── daily-backup.sh         #   The daily backup script
│
└── BACKUP-LOG.md              # 📋 Backup history log
```

---

## 🔄 Daily Backup

A scheduled task runs **daily** to backup:
- Agent Zero knowledge base
- Agent Zero memory database
- Agent Zero custom prompts
- Agent Zero skills and plugins
- Agent Zero agent profiles
- Working directory files

Backups are committed to the `agent-zero-backup/` directory with timestamps.

---

## 🏗️ Design Principles

1. **Portable** — Any agent framework can read this repo and gain context
2. **Self-Documenting** — Every directory has a README explaining its contents
3. **Machine-Readable** — MANIFEST.json provides a structured inventory
4. **Living** — Updated daily via automated backup
5. **Injectable** — `.promptinclude.md` enables real-time context injection

---

## 📜 License

Personal knowledge base — all rights reserved.
