# Spec: Memory Palace Sync — Curated Knowledge Audit & Portable Export

> **Status:** DRAFT
> **Created:** 2026-05-27
> **Idea doc:** `/tolu/docs/ideas/memory-palace-sync.md`

---

## Objective

Reconcile the tolu memory palace repo with 5+ weeks of accumulated Agent Zero knowledge through a curated, security-cleaned, portable sync. The output enables specialized agents (Hermes, opencode, OpenClaw) to adopt the knowledge base on a VPS.

**User:** Tolu (repo owner) + future agent frameworks consuming the exported knowledge.

**Done when:** Single clean commit pushed to `origin/main` with 25-30 curated skills, 34-profile manifest, 18-plugin catalog, 5+ new rooms, and 0 secret findings.

---

## 1. Security Scan Methodology

### 1.1 Tool Selection

| Tool | Purpose | Install Command |
|------|---------|----------------|
| `gitleaks` v8.x | Primary secret scanner — detects API keys, tokens, passwords, private keys, certificates | `apt-get install -y gitleaks` or download binary from GitHub releases |
| Custom regex scan | Supplement gitleaks — catch patterns gitleaks misses (mnemonic phrases, bare wallet private keys, custom token formats) | Bash script using `grep -rn` |

### 1.2 Scan Targets

```
SCAN_TARGETS=(
  "/a0/usr/workdir/tolu/"                          # Existing repo content
  "/a0/usr/skills/<selected-skill>/"               # Each selected skill before copy
  "/a0/usr/plugins/a0_agent_skills/skills/<sel>/"  # Plugin skills before copy
  "/a0/usr/plugins/<plugin>/"                      # Plugin dirs for catalog metadata
  "/a0/usr/agents/"                                # Agent profiles before indexing
)
```

### 1.3 What Counts as a Real Secret (BLOCK)

| Pattern | Example | Action |
|---------|---------|--------|
| API keys (any service) | `sk-...`, `key_...`, `AKIA...` | BLOCK |
| Bearer/auth tokens | `Bearer ey...`, `token: ...` | BLOCK |
| Passwords in config | `password = "..."`, `"pass": "..."` | BLOCK |
| Private keys (crypto) | `0x` + 64 hex chars on a line alone, `private_key` fields | BLOCK |
| Mnemonic seed phrases | 12/24 word sequences matching BIP-39 wordlist | BLOCK |
| `§§secret(...)` aliases with inline values | `AAAAAAAAAAAAAAAAAAAAAPHl9QEAAAAA8vgRWUyYpmmMe%2FSEF6cvuKVIAW8%3DqpMn6ebX6JUibM5gjitFhMvDxR6PV7DywNZvJqB1UbdtNKh5hg = "eyJ..."` | BLOCK if resolved value present; template references alone are OK |
| `.env` files with real values | `API_KEY=sk_live_...` | BLOCK |
| OAuth credentials | `client_secret: "..."` | BLOCK |

### 1.4 What is NOT a Secret (ALLOW)

| Pattern | Rationale |
|---------|-----------|
| Wallet addresses (public identifiers) | `0xcd83...` — public on chain |
| Project names, URLs, framework names | Not sensitive |
| `§§secret(...)` template aliases without values | Secret-alias placeholders only; never store real values |
| Contract addresses | Public on chain |
| RPC endpoint URLs (public free tier) | `https://rpc.ankr.com/eth` — public |
| Agent profile descriptions, skill descriptions | Text content, not credentials |
| Example/placeholder values | `your-api-key-here`, `INSERT_TOKEN` |

### 1.5 Custom Regex Patterns

```bash
PATTERNS=(
  # Mnemonic seed phrases (12 or 24 BIP-39 words)
  '(?:abandon|ability|able|about|above|absent|absorb|abstract|absurd|abuse)(?:\s+(?:[a-z]+)){11,23}'
  # Bare hex private keys (64 hex chars on own line)
  '^[0-9a-fA-F]{64}$'
  # Inline private key assignments
  'private[_-]?key\s*[=:]\s*['"][0-9a-fA-F]{64}'
  # Mnemonic assignment
  'mnemonic\s*[=:]\s*['"][a-z]+(\s+[a-z]+){11,23}'
)
```

### 1.6 Remediation Procedure

```
FOR EACH finding:
  1. Record: file path, line number, pattern matched, severity
  2. Classify:
     - TRUE POSITIVE (real secret) → STOP. Remove the secret. Re-scan.
     - FALSE POSITIVE (public address, placeholder) → Document exemption in scan log.
  3. If TRUE POSITIVE found in git history:
     - Use `git filter-repo --invert-paths --path <file>` to scrub
     - Force-push if already pushed to remote
     - Rotate the compromised credential
  4. Do NOT proceed to commit until all TRUE POSITIVE findings are resolved.
```

### 1.7 Git History Check

```bash
# Scan full git history for secrets
cd /a0/usr/workdir/tolu
gitleaks detect --source . --log-opts="--all" --report-format json --report-path /tmp/gitleaks-history.json

# If findings exist in history only (not in working tree):
#   git filter-repo --invert-paths --path <file-with-secret>
#   Re-scan to confirm clean
```

### Acceptance Criteria — Section 1

- [ ] `gitleaks` installed and returns version
- [ ] `gitleaks detect` on tolu working tree returns 0 findings
- [ ] `gitleaks detect --log-opts="--all"` on git history returns 0 findings
- [ ] Custom regex scan on all candidate files returns 0 TRUE POSITIVE findings
- [ ] Scan log saved to `tolu/docs/security-scan-log.md` with date, tools used, findings, exemptions

---

## 2. Skill Curation Criteria

### 2.1 Selection Rubric

Each candidate skill is scored on a 4-point scale (0-3) across four dimensions:

| Dimension | Weight | 3 (High) | 2 (Medium) | 1 (Low) | 0 |
|-----------|--------|----------|-------------|---------|---|
| **Reusability** | 40% | Applicable to any agent framework | Needs minor adaptation | Agent Zero specific only | Single-use script |
| **Domain Value** | 30% | Trading/DeFi/security/infra — core user domains | AI/ML, DevOps, writing — secondary domains | Domino/platform-specific | Niche tutorial |
| **Quality** | 20% | Has SKILL.md + examples + validation | Has SKILL.md + examples | SKILL.md only | Incomplete |
| **Breadth** | 10% | Covers multiple use cases | Covers one deep use case | Covers one narrow task | Trivial |

**Minimum score to include: 5.0 / 12**

### 2.2 Categories to Prioritize (in order)

1. **Trading Infrastructure** — strategy generation, backtesting, market data, on-chain analysis, DeFi scanning, liquidation, funding/basis
2. **Agent Operations** — skill creation, context engineering, incremental implementation, test-driven development, spec-driven development, debugging
3. **Security** — code review, security hardening, on-chain analysis, contract safety
4. **AI/ML** — prompt engineering, AI engineer workflows, data storytelling
5. **DevOps** — CI/CD, deployment, Akash, git workflows
6. **Writing & Content** — deslop, technical writing, content strategy, copywriting
7. **Knowledge Management** — source validation, research synthesis, knowledge structuring
8. **Web3** — Solidity, Uniswap, BattleChain

### 2.3 Exclusion Criteria (Automatic EXCLUDE)

| Criterion | Skills Excluded |
|-----------|----------------|
| All `domino-*` skills (platform-specific) | 16 skills: domino-ai-gateway through domino-workspaces |
| `patterns.dev-skills` counts as ONE entry | Contains 30+ JS pattern sub-skills; include as single indexed entry |
| Duplicate of existing tolu skill | Skills already in `tolu/skills/` — no re-copy |
| Empty or broken SKILL.md | Skills with < 10 lines in SKILL.md |

### 2.4 Preliminary Selection (30 skills)

Based on the rubric applied to the 77 untracked skills:

**Tier 1 — Trading/DeFi Infrastructure (8 skills)**

| Skill | Source | Score | Rationale |
|-------|--------|-------|-----------|
| `strategy-generation` | skills/ | 10 | Core trading infra; any agent framework benefits |
| `backtest-validation` | skills/ | 9 | Backtest verification; portable validation patterns |
| `market-data-loader` | skills/ | 9 | OHLCV fetching; any trading agent needs this |
| `perp-funding-basis` | skills/ | 9 | Funding rate analysis; DeFi-specific but high value |
| `liquidation-heatmap` | skills/ | 9 | Liquidation analysis; unique trading tool |
| `crypto-swarm-desk` | skills/ | 8 | Multi-agent trading desk; shows swarm patterns |
| `onchain-analysis-trading` | skills/ | 8 | Trading-focused on-chain; Alchemy integration |
| `uniswap-trading-api` | skills/ | 8 | DEX integration; Web3 trading infra |

**Tier 2 — Agent Operations & Engineering (7 skills)**

| Skill | Source | Score | Rationale |
|-------|--------|-------|-----------|
| `spec-driven-development` | plugins/ | 10 | Core engineering workflow; universal |
| `incremental-implementation` | plugins/ | 9 | Slice-based implementation; universal |
| `context-engineering` | plugins/ | 9 | Context loading patterns; universal |
| `test-driven-development` | plugins/ | 9 | TDD workflow; universal |
| `code-simplification` | plugins/ | 8 | Refactoring discipline; universal |
| `source-driven-development` | plugins/ | 8 | Doc-first development; universal |
| `using-agent-skills` | plugins/ | 8 | Skill discovery meta-pattern; universal |

**Tier 3 — Security & Code Quality (4 skills)**

| Skill | Source | Score | Rationale |
|-------|--------|-------|-----------|
| `security-and-hardening` | plugins/ | 9 | OWASP prevention; universal |
| `code-review-and-quality` | plugins/ | 9 | Multi-axis review; universal |
| `debugging-and-error-recovery` | plugins/ | 8 | Systematic debugging; universal |
| `onchain-analyzer` | skills/ | 8 | Contract safety + rug detection; Web3 specific |

**Tier 4 — AI/ML & Prompting (3 skills)**

| Skill | Source | Score | Rationale |
|-------|--------|-------|-----------|
| `prompt-engineering-harness` | skills/ | 9 | Structured prompting; universal for AI agents |
| `deslop` | skills/ | 7 | Anti-AI writing; content quality gate |
| `knowledge-structuring` | skills/ | 7 | Knowledge organization; universal |

**Tier 5 — DevOps & Infrastructure (4 skills)**

| Skill | Source | Score | Rationale |
|-------|--------|-------|-----------|
| `ci-cd-and-automation` | plugins/ | 8 | Pipeline automation; universal |
| `devops-assistant` | skills/ | 7 | Git workflow + deployment; universal |
| `akash` | skills/ | 7 | Decentralized cloud; VPS deployment relevant |
| `git-workflow-and-versioning` | plugins/ | 7 | Commit discipline; universal |

**Tier 6 — Writing & Content (2 skills)**

| Skill | Source | Score | Rationale |
|-------|--------|-------|-----------|
| `tech-writer` | skills/ | 7 | Already synced — keep |
| `data-storyteller` | skills/ | 7 | Data narrative patterns; universal |

**Tier 7 — Web3 & Niche (2 skills)**

| Skill | Source | Score | Rationale |
|-------|--------|-------|-----------|
| `solidity` | skills/ | 8 | Already synced — keep |
| `patterns.dev-skills` | skills/ | 7 | 30+ JS patterns as ONE entry |

### 2.5 Portable Export Format

Each copied skill preserves this structure:

```
tolu/skills/<skill-name>/
├── SKILL.md              # Required — main skill document
├── examples/             # Optional — worked examples
├── validation/           # Optional — validation scripts
├── references/           # Optional — reference docs
├── scripts/              # Optional — helper scripts
└── metadata.json         # Generated — portable manifest entry
```

**`metadata.json` format:**

```json
{
  "name": "strategy-generation",
  "description": "Turn plain-English trading ideas into backtest strategies",
  "source": "skills/",
  "categories": ["trading", "defi", "backtesting"],
  "framework": "agent-zero",
  "framework_version": ">=0.7",
  "portability": {
    "format": "SKILL.md (markdown)",
    "dependencies": ["market-data-loader", "backtest-engine-plugin"],
    "consuming": {
      "hermes": "Parse SKILL.md instructions section as system prompt",
      "opencode": "Load as plugin skill via a0_agent_skills format",
      "openclaw": "Convert to agent instruction set — see portable-format-guide.md"
    }
  },
  "files": ["SKILL.md", "examples/"],
  "added_date": "2026-05-27"
}
```

### Acceptance Criteria — Section 2

- [ ] Exactly 25-30 new skills copied to `tolu/skills/` (excluding the 15 already tracked)
- [ ] Each skill has a valid `SKILL.md` with > 10 lines
- [ ] Each skill has a `metadata.json` with required fields
- [ ] No `domino-*` skills included
- [ ] `patterns.dev-skills` counted as 1 entry
- [ ] Selection scoring documented in `tolu/docs/skill-selection-scoring.md`
- [ ] Skills not selected are listed with reason in `tolu/docs/skill-exclusion-list.md`

---

## 3. Agent Profile Manifest

### 3.1 Source Data

The 34 canonical profiles come from `/a0/usr/workdir/agent-profile-audit.md`, sourced from:
- Core framework: `/a0/agents/` (5 profiles: agent0, default, developer, hacker, researcher)
- User-space overrides: `/a0/usr/agents/` (10 profiles)
- Skills plugin: `/a0/usr/plugins/a0_agent_skills/agents/` (7 profiles)
- ASE harness plugin: `/a0/usr/plugins/autonomous_software_engineer_harness/agents/` (12 profiles)

### 3.2 Manifest Format

File: `tolu/docs/agent-profiles.md`

```markdown
# Agent Profile Manifest

> 34 canonical Agent Zero profiles with portability notes.
> Generated: 2026-05-27

## Profile Index

| # | Name | Source | Has role.md | Primary Use | Portability |
|---|------|--------|-------------|-------------|-------------|
| 1 | agent0 | core | no | Default orchestrator | HIGH — generic agent concepts |
| 2 | developer | core+user | yes | Software development | HIGH — maps to generic "coder" role |
| ... | ... | ... | ... | ... | ... |

## Profile Details

### agent0

- **Source:** core (/a0/agents/agent0/)
- **Description:** Primary orchestrator agent that manages conversations, classifies requests, delegates specialist work
- **Context:** This is the default top-level agent. Delegates to specialist profiles...
- **Triggers:** Default for all direct user interactions
- **Has role.md:** No (uses default prompt)
- **Portability Notes:** Maps to generic "orchestrator" or "router" agent pattern. The delegation model (classify → delegate → synthesize) is framework-agnostic.
- **Framework Mapping:**
  - Hermes: `orchestrator` role
  - opencode: `coordinator` agent
  - OpenClaw: `master` agent

### developer
...
```

### 3.3 Fields Per Profile

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Profile directory name (exact) |
| `source` | yes | `core`, `user`, `skills-plugin`, `ase-plugin` |
| `description` | yes | 1-2 sentence description of what the agent does |
| `context` | yes | Brief context on when to use this profile |
| `triggers` | yes | Natural language triggers that activate this profile |
| `has_role.md` | yes | Whether the profile includes a custom role.md file |
| `portability_notes` | yes | How portable this profile is to other frameworks |
| `framework_mapping` | yes | Suggested role name for Hermes, opencode, OpenClaw |
| `collision_notes` | no | Only for profiles with naming collisions (ai-engineer, security-auditor) |

### 3.4 Naming Collision Handling

Two collisions exist and are documented as-is:

1. **`ai-engineer` (user-space) vs `ai_engineer` (ASE plugin)** — different profiles, different scopes. User-space is a general AI engineering profile; ASE plugin is part of the autonomous SE harness.
2. **`security-auditor` (skills plugin) vs `security_auditor` (ASE plugin)** — different profiles. Skills plugin version is OWASP-focused; ASE version is part of the full engineering lifecycle.

Both entries are listed with `collision_notes` field explaining the distinction.

### 3.5 Mapping Agent Zero Profiles to Generic Concepts

| Agent Zero Category | Generic Pattern | Description |
|---------------------|-----------------|-------------|
| Orchestrator (agent0) | Router/Dispatcher | Classifies and delegates tasks |
| Builder (developer, backend, frontend, fullstack) | Specialist Workers | Execute implementation tasks |
| Reviewer (code-reviewer, security-auditor) | Quality Gates | Verify work before merge |
| Researcher | Knowledge Worker | Information gathering and analysis |
| Hacker | Red/Blue Team | Security operations |
| Planner (architect, product_manager) | Strategist | Design and specification |
| Shipper (release_manager, devops) | Operator | Deployment and infrastructure |
| Tester (test-engineer, qa_engineer) | Verifier | Test creation and validation |

### Acceptance Criteria — Section 3

- [ ] All 34 profiles listed in `tolu/docs/agent-profiles.md`
- [ ] Each profile has all required fields populated
- [ ] Naming collisions documented with `collision_notes`
- [ ] Framework mapping table included for Hermes, opencode, OpenClaw
- [ ] Generic concept mapping table included
- [ ] 19 profiles missing `role.md` are explicitly noted

---

## 4. Plugin Catalog

### 4.1 Catalog Format

File: `tolu/docs/plugin-catalog.md`

```markdown
# Plugin Catalog

> 18 Agent Zero plugins with adoption guidance.
> Generated: 2026-05-27

## Plugin Index

| # | Name | Type | Has README | Description | Adoptable |
|---|------|------|------------|-------------|----------|
| 1 | a0_agent_skills | user-facing | yes | Engineering workflow skills | YES |
| 2 | _browser | internal | no | Browser automation | NO (framework internal) |
| ... | ... | ... | ... | ... | ... |

## Plugin Details

### a0_agent_skills

- **Type:** user-facing
- **Directory:** `/a0/usr/plugins/a0_agent_skills/`
- **Description:** Agent Skills plugin v0.3.1 — 22 engineering workflow skills for development lifecycle
- **Has README:** Yes
- **Has manifest.json:** No
- **Dependencies:** None (self-contained skill files)
- **Configuration:** None required — skills load on demand
- **Framework Compatibility:**
  - Agent Zero: Native plugin
  - opencode: Skills can be loaded via a0_agent_skills adapter
  - Hermes: Parse SKILL.md files as instruction sets
  - OpenClaw: Convert skills to agent modules
- **Adoption Notes:** Most portable plugin. Skills are Markdown files with no code dependencies. Start here for cross-framework adoption.
- **Included Skills:** api-and-interface-design, browser-testing-with-devtools, ci-cd-and-automation, code-review-and-quality, code-simplification, context-engineering, debugging-and-error-recovery, deprecation-and-migration, documentation-and-adrs, frontend-ui-engineering, git-workflow-and-versioning, idea-refine, incremental-implementation, performance-optimization, planning-and-task-breakdown, security-and-hardening, shipping-and-launch, skill-creator, source-driven-development, spec-driven-development, test-driven-development, using-agent-skills

### _browser

- **Type:** internal (underscore-prefixed)
- **Description:** Internal browser automation plugin
- **Adoption Notes:** NOT user-facing. Part of Agent Zero's built-in browser tool infrastructure. Not portable.
...
```

### 4.2 Fields Per Plugin

| Field | Required | Description |
|-------|----------|-------------|
| `name` | yes | Plugin directory name |
| `type` | yes | `user-facing` or `internal` |
| `description` | yes | What the plugin does |
| `has_readme` | yes | Whether README.md exists |
| `has_manifest` | yes | Whether manifest.json exists |
| `dependencies` | yes | External dependencies (None if self-contained) |
| `configuration` | yes | What config is needed to use it |
| `framework_compatibility` | yes | Notes for each target framework |
| `adoption_notes` | yes | Practical guidance for adoption |

### 4.3 Plugin Classifications

**User-facing (11 plugins):**

| Plugin | Description | Adoptable |
|--------|-------------|----------|
| `a0_agent_skills` | 22 engineering workflow skills | YES — most portable |
| `a0_playwright_cli` | Browser automation via Playwright | YES — standard tool |
| `alpha_zoo` | Alpha factor library | PARTIAL — depends on backtest plugin |
| `autonomous_software_engineer_harness` | Devin-like SE harness | PARTIAL — complex integration |
| `backtest_engine` | Trading backtesting engine | YES — self-contained |
| `commands` | YAML slash commands | YES — simple format |
| `docker_terminal` | Multi-session terminal | NO — Agent Zero UI specific |
| `parallel_swarm` | Parallel subordinate dispatch | PARTIAL — core A0 concept |
| `pwa_fullscreen` | PWA meta tags | YES — simple web feature |
| `trade_journal` | Trade history analysis | YES — self-contained |
| `youtube_transcribe` | YouTube transcription | YES — self-contained |

**Internal (7 plugins):** NOT portable, NOT user-facing

`_browser`, `_email_integration`, `_model_config`, `_oauth`, `_office`, `_skills`, `_whisper_stt`

### 4.4 Plugin Files Copied

For user-facing plugins, copy only metadata (README.md) — not the full plugin source. The catalog indexes them; source stays in the Agent Zero runtime.

```
tolu/plugins/<plugin-name>/
└── README.md    # Plugin README only (not full source)
```

### Acceptance Criteria — Section 4

- [ ] All 18 plugins listed in `tolu/docs/plugin-catalog.md`
- [ ] Each plugin has all required fields populated
- [ ] Internal plugins clearly marked as `internal` with adoption note "NOT portable"
- [ ] User-facing plugins have framework compatibility notes
- [ ] Plugin READMEs copied to `tolu/plugins/<name>/README.md` for user-facing plugins

---

## 5. Memory Palace Rooms

### 5.1 New Rooms to Add (7 rooms)

| # | Wing | Room File | Topic | Rationale |
|---|------|-----------|-------|----------|
| 1 | `technical/rooms/` | `agent-profile-taxonomy.md` | 34 agent profiles categorized by role type | Agent ops knowledge accumulated over 5 weeks |
| 2 | `technical/rooms/` | `skill-taxonomy-2026-05.md` | 107 skills categorized by domain and portability | Skill selection audit findings |
| 3 | `technical/rooms/` | `plugin-ecosystem-2026-05.md` | 18 plugins with adoption tiers | Plugin catalog findings |
| 4 | `domain/rooms/` | `trading-infrastructure-stack.md` | Trading tools: backtesting, market data, strategies, DeFi scanning | Accumulated trading infra knowledge |
| 5 | `learning/rooms/` | `vps-deployment-patterns-2026.md` | Akash deployment, agent hosting, knowledge base hosting | VPS deployment learnings from kronos/condor work |
| 6 | `technical/rooms/` | `portable-knowledge-format.md` | How to make agent knowledge portable across frameworks | Cross-framework compatibility research |
| 7 | `technical/rooms/` | `agent-operations/memory-palace-sync-methodology.md` | The sync methodology itself — security scan, curation, commit process | Meta-knowledge for future syncs |

### 5.2 Room Format

Each room file follows the existing spatial model:

```markdown
# Room Title

> **Wing:** [wing-name]
> **Added:** YYYY-MM-DD
> **Status:** active

## Summary
[2-3 sentence description of what this room contains]

## Key Contents
- [Item 1]
- [Item 2]
- [Item N]

## Cross-References
- Related: `memory-palace/wings/[other-wing]/rooms/[related-room].md`

## Source
[Where this knowledge came from]
```

### 5.3 File Naming Conventions

- Lowercase, hyphen-separated: `agent-profile-taxonomy.md`
- Date suffix when content is time-sensitive: `skill-taxonomy-2026-05.md`
- No date suffix when content is evergreen: `trading-infrastructure-stack.md`
- Match existing room naming patterns in each wing

### Acceptance Criteria — Section 5

- [ ] 7 new room files created in correct wing directories
- [ ] Each room follows the format template (Wing, Added, Status, Summary, Key Contents, Cross-References, Source)
- [ ] File naming follows conventions
- [ ] Room content is substantive (> 20 lines per room, not stubs)
- [ ] Cross-references link to related existing rooms where applicable

---

## 6. Portable Format Guide

### 6.1 Document Structure

File: `tolu/docs/portable-format-guide.md`

```markdown
# Portable Format Guide — Consuming Tolu Knowledge in Agent Frameworks

## Overview
This guide explains how to consume the knowledge artifacts exported from
Agent Zero's tolu memory palace in other agent frameworks.

## Artifact Types

| Artifact | Location | Format | Consumer |
|----------|----------|--------|----------|
| Skills | `skills/<name>/SKILL.md` | Markdown | All frameworks |
| Agent Profiles | `docs/agent-profiles.md` | Markdown table + detail sections | All frameworks |
| Plugin Catalog | `docs/plugin-catalog.md` | Markdown table + detail sections | All frameworks |
| Memory Rooms | `memory-palace/wings/*/rooms/*.md` | Markdown | All frameworks |
| Skill Metadata | `skills/<name>/metadata.json` | JSON | Automated consumers |

## How to Parse SKILL.md

### Structure
Every SKILL.md has:
1. Title (# Skill Name)
2. Overview section — what the skill does
3. When to Use section — trigger conditions
4. Process sections — numbered steps to follow
5. (Optional) Examples, Validation, Anti-Patterns sections

### For Hermes
- Load SKILL.md content as system prompt instructions
- Match trigger phrases from "When to Use" to activation conditions
- Follow numbered steps as execution workflow

### For opencode
- Use a0_agent_skills plugin format — SKILL.md is already compatible
- Load via skills_tool with skill_name parameter
- Trigger phrases map to agent routing rules

### For OpenClaw
- Parse SKILL.md into agent instruction modules
- Extract process steps as action sequences
- Map triggers to intent recognition patterns
- Use metadata.json for automated registration

## Metadata Schema (metadata.json)

{
  "name": "string",
  "description": "string",
  "source": "skills/ | plugins/",
  "categories": ["string"],
  "framework": "agent-zero",
  "portability": {
    "format": "SKILL.md (markdown)",
    "dependencies": ["string"],
    "consuming": {
      "hermes": "string",
      "opencode": "string",
      "openclaw": "string"
    }
  },
  "files": ["string"],
  "added_date": "YYYY-MM-DD"
}

## Agent Profile Adoption

[Explains the 8 generic agent categories and how to map them]

## Plugin Adoption Tiers

[Explains the YES/PARTIAL/NO adoption classification]
```

### 6.2 Content Requirements

The guide must explain:
1. **Artifact inventory** — what exists and where
2. **SKILL.md parsing** — how to extract instructions from each skill
3. **Metadata schema** — JSON format for automated consumers
4. **Framework-specific adoption** — Hermes, opencode, OpenClaw
5. **Agent profile mapping** — 8 generic categories to framework roles
6. **Plugin adoption tiers** — YES/PARTIAL/NO classification explained
7. **Memory palace navigation** — wing/room spatial model

### Acceptance Criteria — Section 6

- [ ] Document exists at `tolu/docs/portable-format-guide.md`
- [ ] Covers all 7 content requirements listed above
- [ ] Includes concrete examples for parsing SKILL.md
- [ ] Includes the metadata.json schema
- [ ] Framework-specific guidance for all 3 target frameworks
- [ ] Document is self-contained — a developer unfamiliar with Agent Zero can understand and consume the artifacts

---

## 7. File Organization

### 7.1 Directory Structure (post-sync)

```
tolu/
├── docs/
│   ├── specs/
│   │   └── memory-palace-sync-SPEC.md      # THIS SPEC
│   ├── ideas/
│   │   └── memory-palace-sync.md           # IDEA DOC (already exists)
│   ├── agent-profiles.md                   # NEW — 34 profile manifest
│   ├── plugin-catalog.md                   # NEW — 18 plugin catalog
│   ├── portable-format-guide.md            # NEW — format adoption guide
│   ├── security-scan-log.md                # NEW — scan results
│   ├── skill-selection-scoring.md          # NEW — selection rubric results
│   ├── skill-exclusion-list.md             # NEW — excluded skills with reasons
│   └── framework-integration/              # EXISTING — no changes
├── skills/
│   ├── README.md                           # EXISTING
│   ├── [15 existing skills]/               # EXISTING — no changes
│   └── [25-30 new skills]/                 # NEW — curated skills with SKILL.md + metadata.json
├── plugins/
│   ├── README.md                           # EXISTING
│   └── [11 user-facing plugin dirs]/       # NEW — each with README.md only
├── memory-palace/
│   └── wings/
│       ├── technical/rooms/
│       │   ├── [18 existing rooms]          # EXISTING — no changes
│       │   ├── agent-profile-taxonomy.md    # NEW
│       │   ├── skill-taxonomy-2026-05.md    # NEW
│       │   ├── plugin-ecosystem-2026-05.md  # NEW
│       │   ├── portable-knowledge-format.md # NEW
│       │   └── agent-operations/memory-palace-sync-methodology.md  # NEW
│       ├── domain/rooms/
│       │   ├── [1 existing room]            # EXISTING
│       │   └── trading-infrastructure-stack.md  # NEW
│       └── learning/rooms/
│           ├── [6 existing rooms]           # EXISTING
│           └── vps-deployment-patterns-2026.md  # NEW
└── [everything else — EXISTING, no changes]
```

### 7.2 Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Skill directory | `skills/<kebab-case-name>/` | `skills/strategy-generation/` |
| Skill file | `SKILL.md` (always) | `skills/strategy-generation/SKILL.md` |
| Skill metadata | `metadata.json` (always) | `skills/strategy-generation/metadata.json` |
| Plugin directory | `plugins/<kebab-case-name>/` | `plugins/a0_agent_skills/` |
| Plugin file | `README.md` (only metadata) | `plugins/a0_agent_skills/README.md` |
| Room file | `<kebab-case>.md` | `technical/rooms/agent-profile-taxonomy.md` |
| Dated room | `<kebab-case>-YYYY-MM.md` | `technical/rooms/skill-taxonomy-2026-05.md` |
| Doc file | `<kebab-case>.md` | `docs/agent-profiles.md` |

### 7.3 What Gets Committed

| Category | Committed | Excluded |
|----------|-----------|----------|
| New skill directories (SKILL.md + supporting files + metadata.json) | YES | — |
| Existing skills (15 already tracked) | NO | Already in repo |
| New doc files (agent-profiles.md, plugin-catalog.md, etc.) | YES | — |
| New room files (7 rooms) | YES | — |
| Plugin READMEs (11 user-facing) | YES | — |
| BACKUP-LOG.md changes | YES | Tracked, auto-updated |
| Security scan log | YES | Evidence of clean scan |
| .gitignore | NO | No changes needed |
| Binary files, images, logs | — | Excluded by .gitignore |
| domino-* skills | — | Excluded by selection criteria |
| Internal plugin source code | — | Not copied (catalog only) |

### Acceptance Criteria — Section 7

- [ ] All new files are in their correct locations per the directory structure
- [ ] No files exist outside the documented structure
- [ ] File naming follows conventions
- [ ] `.gitignore` covers all exclusion cases (already verified)

---

## 8. Commit Plan

### 8.1 Pre-Commit Verification Steps

```bash
# Step 1: Security scan
 gitleaks detect --source /a0/usr/workdir/tolu/ --no-git --report-format json --report-path /tmp/gitleaks-staging.json
 # EXPECTED: 0 findings

# Step 2: Git history scan
 cd /a0/usr/workdir/tolu && gitleaks detect --source . --log-opts="--all" --report-format json --report-path /tmp/gitleaks-history.json
 # EXPECTED: 0 findings

# Step 3: Custom regex scan on all new files
 bash /tmp/custom-secret-scan.sh /a0/usr/workdir/tolu/
 # EXPECTED: 0 TRUE POSITIVE findings

# Step 4: Count new skills
 NEW_SKILLS=$(ls -d /a0/usr/workdir/tolu/skills/*/ | wc -l)
 echo "Total skills: $NEW_SKILLS (existing 15 + new)"
 # EXPECTED: 40-45 total (15 existing + 25-30 new)

# Step 5: Count new rooms
 NEW_ROOMS=$(find /a0/usr/workdir/tolu/memory-palace/wings/ -name '*.md' ! -name 'README.md' | wc -l)
 echo "Total rooms: $NEW_ROOMS (existing 30 + new 7)"
 # EXPECTED: 37 total (30 existing + 7 new)

# Step 6: Verify required docs exist
 for f in agent-profiles.md plugin-catalog.md portable-format-guide.md security-scan-log.md skill-selection-scoring.md skill-exclusion-list.md; do
   test -f "/a0/usr/workdir/tolu/docs/$f" && echo "OK: $f" || echo "MISSING: $f"
 done
 # EXPECTED: All OK

# Step 7: Verify each new skill has SKILL.md and metadata.json
 for d in /a0/usr/workdir/tolu/skills/*/; do
   name=$(basename "$d")
   test -f "${d}SKILL.md" && echo "OK: $name/SKILL.md" || echo "MISSING: $name/SKILL.md"
   test -f "${d}metadata.json" && echo "OK: $name/metadata.json" || echo "MISSING: $name/metadata.json"
 done
 # EXPECTED: All OK

# Step 8: Stage all changes
 cd /a0/usr/workdir/tolu && git add -A

# Step 9: Review diff
 git diff --cached --stat
 # Human reviews before proceeding
```

### 8.2 Commit Message

```
Sync: curated knowledge audit — 28 skills, 34 profiles, 18 plugins, 7 rooms

- Security: gitleaks + custom regex scan — 0 findings
- Skills: 28 new curated skills (85→13→28 selected from 77 untracked)
- Profiles: 34 canonical agent profiles with portability notes
- Plugins: 18 plugins cataloged with adoption guidance
- Rooms: 7 new memory palace rooms (trading infra, agent ops, skill taxonomy)
- Docs: portable format guide, selection scoring, exclusion list
- Plugins tracked: 11 user-facing plugin READMEs added

Excluded: 16 domino-* skills (platform-specific), 7 internal plugins,
patterns.dev-skills counted as 1 entry

Source: /a0/usr/skills/ + /a0/usr/plugins/ + /a0/usr/agents/
Target: github.com/ToXMon/tolu
```

### 8.3 Commit Flow

```
1. Run all pre-commit verification steps
2. Present diff to user for review (human gate)
3. User approves → proceed
4. User rejects → address feedback, re-verify
5. git commit with message above
6. git push origin main
7. Verify push succeeded
8. Run post-push gitleaks scan on remote (optional safety net)
```

### 8.4 Rollback Plan

If issues are discovered post-push:

```bash
# Option A: Revert the commit
git revert HEAD

# Option B: Reset to previous commit (if caught quickly)
git reset --hard HEAD~1
git push --force origin main

# Option C: If secrets leaked, rotate credentials + git filter-repo
```

### Acceptance Criteria — Section 8

- [ ] All 9 pre-commit verification steps pass
- [ ] User reviewed the full diff before commit
- [ ] Commit message matches the specified format
- [ ] Push to `origin/main` succeeds
- [ ] Post-push `git log --oneline -1` shows the commit
- [ ] `gitleaks` on the pushed commit returns 0 findings

---

## Success Criteria (Complete)

| # | Criterion | Verification |
|---|-----------|--------------|
| 1 | `gitleaks` returns 0 findings | `gitleaks detect --source tolu/` exits 0 |
| 2 | 25-30 curated skills added | `ls tolu/skills/ | wc -l` = 40-45 |
| 3 | Agent profile manifest complete | `grep -c '^### ' tolu/docs/agent-profiles.md` = 34 |
| 4 | Plugin catalog complete | `grep -c '^### ' tolu/docs/plugin-catalog.md` = 18 |
| 5 | 5+ new memory palace rooms | `find tolu/memory-palace -name '*.md' -newer tolu/.git/refs/heads/main` |
| 6 | Portable format guide exists | `test -f tolu/docs/portable-format-guide.md` |
| 7 | Single clean commit | `git log --oneline -1` shows sync commit |
| 8 | User approved diff | Human gate approval recorded |

---

## Open Questions

None — all resolved during idea refinement and assumption validation.

---

## Boundaries

### Always
- Run security scan before committing
- Include metadata.json with every skill
- Follow existing room format conventions
- Document all decisions (selections, exclusions, exemptions)

### Ask First
- Adding skills not in the preliminary selection
- Changing existing room content
- Modifying .gitignore
- Any deviation from this spec

### Never
- Commit without security scan passing
- Include domino-* skills
- Copy full plugin source code (catalog + README only)
- Modify existing tracked content without explicit approval
- Skip the human gate before push
