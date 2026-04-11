# 🏛️ TOLU — Agent Memory Palace

> A self-documenting, portable knowledge base and daily backup system for AI agent frameworks.
> Designed so **any fresh agent** (Agent Zero, OpenClaw, OpenHermes, or similar) can ingest this repo and gain immediate context.
> Inspired by [MemPalace](https://github.com/milla-jovovich/mempalace) spatial memory techniques.

---

## 🚀 Quick Start for Fresh Agents

1. Read **[AGENT-BOOTSTRAP.md](./AGENT-BOOTSTRAP.md)** — the ingestion manifest
2. Run **`python3 scripts/build-context.py wakeup`** — get ~200 token wake-up context
3. Scan **[agent-zero-backup/](./agent-zero-backup/)** — latest Agent Zero daily backup
4. Browse **[memory-palace/wings/](./memory-palace/wings/)** — Wing/Room/Hall knowledge vault
5. Search **`python3 scripts/search-index.py query "topic"`** — deep search across all content
6. Check **[docs/framework-integration/](./docs/framework-integration/)** — framework-specific guides

---

## 📂 Repository Structure

```
tolu/
├── AGENT-BOOTSTRAP.md          # ⚡ START HERE — agent ingestion manifest
├── MANIFEST.json               # Machine-readable repo inventory
├── .promptinclude.md           # Auto-injected into Agent Zero system prompt (~200 tokens)
│
├── context-layers/             # 🧅 Token-efficient wake-up layers
│   ├── layer0-identity/        #   Who am I, purpose, setup (~100 tokens)
│   ├── layer1-critical-facts/  #   High-confidence facts with validity windows
│   ├── layer2-room-recall/     #   Recently accessed rooms for continuity
│   └── layer3-deep-search/     #   Full TF-IDF search index (on-demand)
│
├── agent-zero-backup/          # 🔄 Daily automated backup of Agent Zero
│   ├── agents/                 #   Agent profiles and configurations
│   ├── knowledge/              #   Knowledge base (fragments, solutions, main)
│   ├── memory-export/          #   Memory database snapshots (FAISS index)
│   ├── plugins/                #   Installed plugins and configs
│   ├── prompts/                #   Prompt templates and overrides
│   ├── skills/                 #   Custom skills (SKILL.md files)
│   └── workdir/                #   Working directory files
│
├── memory-palace/              # 🏛️ The Knowledge Vault (Spatial Organization)
│   ├── wings/                  #   Top-level domains
│   │   ├── personal/           #     User identity, preferences, decisions
│   │   │   ├── halls/          #       {facts, events, decisions, preferences}
│   │   │   └── rooms/          #       Specific topic documents
│   │   ├── projects/           #     Active projects and architectures
│   │   │   ├── halls/          #       {facts, decisions, architecture}
│   │   │   └── rooms/          #       Project-specific rooms
│   │   ├── people/             #     Contacts and interactions
│   │   │   ├── halls/          #       {facts, interactions, preferences}
│   │   │   └── rooms/          #       Person-specific rooms
│   │   ├── learning/           #     Books, videos, courses
│   │   │   ├── halls/          #       {books, videos, courses}
│   │   │   └── rooms/          #       Learning-specific rooms
│   │   ├── technical/          #     Tools, references, howtos
│   │   │   ├── halls/          #       {tools, references, howtos}
│   │   │   └── rooms/          #       Technical-specific rooms
│   │   └── domain/             #     Specialized domains
│   │       ├── halls/          #       {crypto, ai, web3, security}
│   │       └── rooms/          #       Domain-specific rooms
│   └── tunnels/                #   🔗 Auto-generated cross-wing references
│       ├── temporal-facts.json #     Temporal knowledge graph
│       └── {topic}.json        #     Tunnel files linking related rooms
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
│   ├── daily-backup.sh         #   Daily backup script
│   ├── search-index.py         #   TF-IDF search index builder & query
│   ├── cross-reference.py      #   Auto tunnel generator
│   └── build-context.py        #   Context layer builder
│
├── docs/                      # 📖 Documentation
│   └── framework-integration/  #   Framework-specific guides
│       ├── agent-zero.md       #     Agent Zero integration
│       ├── openclaw.md         #     OpenClaw / Claude variants
│       ├── openhermes.md       #     OpenHermes integration
│       └── custom-providers.md #     Custom LLM provider setup
│
└── BACKUP-LOG.md              # 📋 Backup history log
```

---

## 🧅 Context Layers — Token Efficiency

Instead of loading full context files (~2000+ tokens), agents use a **4-layer wake-up stack** (~200 tokens):

| Layer | Tokens | Loaded When | Content |
|-------|--------|-------------|---------|
| **0 — Identity** | ~100 | Always on wake-up | Who am I, purpose, setup |
| **1 — Critical Facts** | ~50 | Always on wake-up | High-confidence active facts |
| **2 — Room Recall** | ~50 | Always on wake-up | Recently accessed rooms |
| **3 — Deep Search** | On-demand | When querying | Full TF-IDF search index |

**~90% token savings** compared to loading full context.

---

## 🏛️ Spatial Organization

The Memory Palace uses **Wing → Room → Hall** spatial organization:

- **Wing** = broad domain (like a building) — `personal`, `projects`, `people`, `learning`, `technical`, `domain`
- **Hall** = category type within a wing (like a corridor) — `facts`, `decisions`, `books`, `tools`, etc.
- **Room** = specific topic document (like a room) — individual markdown files
- **Tunnel** = auto-generated cross-reference linking related rooms across wings

---

## 🔄 Daily Backup

A scheduled task runs **daily at 2:00 AM UTC** to backup:
- Agent Zero knowledge base, memory DB, agent profiles
- Custom prompts, skills, plugins
- Working directory files
- Context layers and search index

Backups are committed to `agent-zero-backup/` with timestamps and pushed to GitHub.

---

## 🔧 Tools & Scripts

```bash
# Get minimal wake-up context
python3 scripts/build-context.py wakeup

# Search the memory palace
python3 scripts/search-index.py query "authentication"

# Build cross-wing tunnels
python3 scripts/cross-reference.py build

# Run backup manually
bash scripts/daily-backup.sh
```

---

## 🏗️ Design Principles

1. **Portable** — Any agent framework can read this repo and gain context
2. **Self-Documenting** — Every directory has a README
3. **Machine-Readable** — MANIFEST.json + search-index.json for structured access
4. **Spatial** — Wing/Room/Hall organization inspired by MemPalace
5. **Token-Efficient** — 4-layer context stack saves ~90% tokens
6. **Living** — Updated daily via automated backup
7. **Cross-Referenced** — Auto-generated tunnels link related knowledge
8. **Temporal** — Facts have validity windows for historical tracking

---

## 📖 Framework Integration Guides

| Framework | Guide |
|-----------|-------|
| **Agent Zero** | [docs/framework-integration/agent-zero.md](docs/framework-integration/agent-zero.md) |
| **OpenClaw / Claude variants** | [docs/framework-integration/openclaw.md](docs/framework-integration/openclaw.md) |
| **OpenHermes** | [docs/framework-integration/openhermes.md](docs/framework-integration/openhermes.md) |
| **Custom Providers** | [docs/framework-integration/custom-providers.md](docs/framework-integration/custom-providers.md) |

---

## 📜 License

Personal knowledge base — all rights reserved.
