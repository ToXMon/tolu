# 0xSero (Sero) - Complete Research Extraction

**Date**: 2026-04-16
**Sources**: 6 web sources + 2 local files
**Profile**: Web3/smart contract security figure, AI infrastructure builder, multi-agent orchestration specialist
**GitHub**: https://github.com/0xSero
**Blog**: https://blog.ethers.club (redirects to https://www.sybilsolutions.ai)
**X/Twitter**: https://x.com/0xSero
**Organization**: Sybil Solutions
**Bio**: "Orchestrator"
**Hardware**: 8x RTX 3090 (192GB VRAM), AMD EPYC 7443P, 512GB DDR4, 6TB NVMe

---

# SECTION 1: CODING PRINCIPLES & PHILOSOPHY

Sources: All sources combined

## Core Mental Model

> "You can just trust that your LSP will provide the model the context it needs. You just look at the results at the end."

- Stop re-explaining the codebase to the agent every session
- Encode context ONCE into repo structure, let tooling enforce it
- Design the hard parts yourself, let AI handle the repetitive stuff
- AI as amplifier, not replacement
- "The assistant complements my weaknesses. The AI has higher testing discipline and security awareness. It catches what I miss."

## 10 Hard-Won Rules for Agentic Coding

### Rule 1: File & Directory Size Limits (Enforce via LSP/tsconfig)
- Max 300 lines per file. Max 20 files per directory
- These are ERRORS, not warnings
- When agent violates them, LSP flags it automatically and agent self-corrects
- ESLint: `"max-lines": ["error", 300]`, `"max-depth": ["error", 4]`
- Force splits: `feature-create.ts`, `feature-limits.ts`, `feature-execute.ts`

### Rule 2: No `any` Types -- Use `unknown` + Zod
```typescript
// Agent default (lazy)
const result: any = await client.callTool(name, args);

// 0xSero pattern (strict)
const result: unknown = await client.callTool(name, args);
const parsed = PaymentResultSchema.parse(result); // Zod validates shape
```
- `any` types cause drift across sessions
- `unknown` + Zod forces explicit contracts that survive context window boundaries

### Rule 3: Centralized Config -- Single Source of Truth
- Everything imports from ONE config file. Nothing duplicated
- When agent edits config, it edits ONE file
- Prevents "magic string scattered across 12 files" problem

### Rule 4: Database Interface Pattern -- Swap Environments
- Define typed interface, implement twice, switch via env var
- SQLite for dev, Supabase for prod
- Switch: `DATABASE=sqlite` (default) or `DATABASE=supabase`

### Rule 5: AGENTS.md Files at Every Module Level
- Each subdirectory gets its own AGENTS.md
- Auto-loaded when agent enters that directory
- Document: which files do what, correct imports, gotchas, decimals/unit conventions, max file sizes

### Rule 6: progress.txt -- Cross-Session Learning Log
- Create at project root
- Agent appends after every work session
- Future sessions READ it first -- compound learning without context bloat

### Rule 7: 2/3 Cadence -- Feature vs. Refactor
- 2 days features, 3 days refactoring, repeat
- For hackathon in 8 hours: Hours 1-5 build, Hours 6-7 refactor, Hour 8 demo
- Without refactor hour: AI agent code accumulates drift

### Rule 8: State Machine Diagram Before Debugging
- Ask agent: "Create an ASCII state machine diagram of the payment flow"
- Forces agent to build mental model before guessing at fixes
- Costs 30 seconds, saves 30 minutes of circular debugging

### Rule 9: Queue Tasks, Don't Supervise
- Write all tasks into prd.json with passes: false
- Start loop: ./scripts/ralph/ralph.sh 10
- Come back to check -- don't babysit
- Never say "do all the tasks" -- context window degrades fast

### Rule 10: Test Pyramid Under Time Pressure
- HIGH VALUE: End-to-end flows, spending limits, database logging
- LOW VALUE (skip): Individual helper unit tests, UI snapshots, type-only tests

## Self-Analysis Data (809 conversations analyzed)

- 19,539 user messages, 11,726 assistant messages, 16,484 tool uses
- Spec completeness: 0.275 (low -- he iterates more than plans)
- Debug maturity: 0.056 (low -- he jumps straight to errors)
- Testing discipline: 0.096 user vs 0.173 assistant
- Security awareness: 0.058 user vs 0.064 assistant
- Architecture-thinking: 0.168 user vs 0.129 assistant
- 40.3% conversations included error sharing
- 0.4% had reproduction language (gap)
- 32.5% contained risky disclosure signals (gap)

### Action items from self-analysis:
1. Add repro template (Error / Expected / Actual / Minimal repro)
2. Test discipline checklist (write test before fix, run after, regression, coverage)
3. Security scan before commit (grep for sk- | pk- | 0x...)
4. Acceptance criteria for delegation (deliverables, acceptance checks)

## Architecture Patterns That Work with AI

- **Reflection Pattern**: AI generates, reviews, critiques, refines based on self-evaluation
- **Tool Use Pattern**: AI interacts with external tools (DB, web, function execution)
- **Planning Pattern**: AI creates detailed plan before implementation
- **Multiagent Pattern**: Subagents verify details while preserving main context

---

# SECTION 2: WORKFLOW STEPS & TECHNIQUES

## Managing 8 Concurrent Projects

1. Encode project context into AGENTS.md files per module
2. Use centralized config (single source of truth)
3. Let LSP/tooling enforce rules (not manual supervision)
4. Queue tasks into prd.json, run autonomous loops
5. 2/3 cadence: 2 days features, 3 days refactoring
6. progress.txt for cross-session memory
7. State machine diagrams before debugging
8. Task-by-task execution, never batch everything

## AI-Assisted Coding Workflow (Blog Post)

### Context Management
- Close all editor tabs. Open only relevant files
- Add to context using slash menu + "Reference Open Editors"
- For large codebases, create /docs/ai/ folder with: architecture, coding standards, component patterns, state management, API conventions, testing strategy

### .cursor/rules Project Instructions
```
UI and Styling:
- Use Shadcn UI and Tailwind for components and styling
- Implement mobile-first responsive design
- Prefer function components over class components

Performance:
- Minimize 'use client' directives
- Favor React Server Components
- Wrap client components in Suspense with fallback

Architecture:
- Use repository pattern for data access
- Implement clean architecture with clear separation of concerns
- Keep components under 150 lines
- Extract complex logic to custom hooks
```

### Agent Mode Best Practices
- Enable "Yolo mode" for unsupervised test execution
- Create new agent windows periodically (long conversations cause forgetting)
- Use "think hard" for extended thinking on complex problems

### TDD with AI
1. AI generates test cases
2. Implement the tests
3. AI writes code that passes
4. Integrate and run tests
5. AI fixes failing tests
6. Finalize

### Skill Preservation
- Manual coding sessions without AI for fundamentals
- Core functionality by hand: security, performance, business logic
- Review everything: understand every line before accepting
- Regular challenges without AI

## Codex-Local Multi-Agent Orchestration

Source: https://github.com/0xSero/codex-local (62 stars, Rust)

### Orchestration Flow
Parent agent receives task -> spawns child agents via spawn_agent tool -> children work independently -> report progress via return_progress tool -> parent coordinates and synthesizes

### State Machine
Idle -> Planning -> Delegating -> AwaitingResults -> ComposingResults -> ContinuationTurn

### Components
- OrchestratorRuntime: main orchestration engine
- ResultBridge: parent-child communication
- AgentDirectory: agent discoverability/auditability
- ContextLedger: tracks combined token usage across parent + all subagents
- SummaryJob: auto-summarization at 80% context capacity
- ResultComposer: synthesizes subagent outputs
- ContinuationTurn: main agent always resumes after subagents finish

### Configuration
```toml
model = "/mnt/llm_models/GLM-4.5-Air-AWQ-4bit"
model_provider = "custom-glm"
model_context_window = 120000
model_max_output_tokens = 65536
model_auto_compact_token_limit = 90000

[orchestrator]
max_concurrent_agents = 5
agent_timeout_seconds = 300
enable_progress_tracking = true

[model_providers.custom-glm]
base_url = "https://your-api-endpoint.com/v1"
wire_api = "chat"
```

### Key Files
- codex-rs/core/src/child_agent_bridge.rs
- codex-rs/core/src/conversation_manager.rs
- codex-rs/core/src/tools/handlers/spawn_agent.rs
- codex-rs/core/src/tools/handlers/return_progress.rs
- codex-rs/core/src/tools/parallel.rs
- codex-rs/orchestrator/

### Codex-Local AGENTS.md Rules
- Crate names prefixed with codex-
- Inline format! vars, collapse if statements
- Method references over closures
- Run `just fmt` automatically (no approval needed)
- Run `just fix -p <project>` before finalizing
- Never modify CODEX_SANDBOX_NETWORK_DISABLED_ENV_VAR or CODEX_SANDBOX_ENV_VAR
- Snapshot tests via cargo-insta
- TUI styling: use Stylize helpers (.red(), .dim()), avoid hardcoded white

### Pre-configured MCP Servers
brave-search, context7, image_recognition, memory, puppeteer, supabase

### Custom Slash Commands
7 custom commands (details in README-CODEX-LOCAL.md)

---

# SECTION 3: TOOLS USED & RECOMMENDED

## Primary Coding Agents
- **Claude Code** -- primary coding agent (terminal)
- **OpenAI Codex** -- secondary coding agent
- **Windsurf / Cascade** -- IDE with agent integration
- **Cursor** -- IDE with Agent mode, Yolo mode, @Docs feature
- **OpenCode** -- mentioned in orchestra integration

## Autonomous Agent Tools
- **Ralph mode** -- autonomous loop for Windsurf
- **prd.json** -- task queue with pass/fail status
- **AGENTS.md** -- context files per module
- **progress.txt** -- cross-session learning log

## Local AI Infrastructure
- **vLLM** -- primary inference server (35-50 TPS on 4x 3090)
- **llama.cpp** -- secondary (degrades with context)
- **sglang** -- alternative inference backend
- **vllm-studio** -- his own management UI (437 stars)

## Code Quality
- **Zod** -- runtime type validation
- **ESLint** -- enforce file size limits
- **cargo-insta** -- snapshot testing (Rust)

## AI Workflow Tools
- **Parchi** (498 stars) -- AI browser copilot, Chrome MV3 + Firefox, BYOK
- **Orchestra** (272 stars) -- multi-agent orchestration for OpenCode
- **ai-data-extraction** (611 stars) -- extract personal data from AI tools
- **mem-layer** (79 stars) -- graph database memory organization
- **open-trees** (69 stars) -- git worktree management for OpenCode
- **factory-cursor-bridge** (71 stars) -- BYOK proxy for Cursor

## Model Preferences (Local)

| Tier | Model | Use Case | Quantization |
|------|-------|----------|-------------|
| S Tier | GLM-4.5-Air | Daily driver, vision | AWQ-4bit |
| S Tier | GLM-4.5V | Screenshot analysis, UI | AWQ-4bit |
| S Tier | MiniMax-M2.1 | Agentic workflows, reasoning | AWQ-4bit |
| A Tier | Hermes-70B | Unrestricted queries | Q5_K_M |
| A Tier | Qwen-72B | General purpose | Q5_K_M |
| A Tier | GPT-OSS-120B | STEM work | Q4_K_M |

## Custom Trained Model
- **sero-nouscoder-14b-sft** -- LoRA adapter on NousCoder 14B
- Trained on 11,711 conversations (51.75M tokens)
- Cost: $47, 18 hours on A100
- Final loss: 0.685, accuracy: 81.6%
- Dataset: 35% Solidity/Web3, 30% TypeScript/Node, 20% Python, 10% SQL, 5% Other
- Served via vLLM at 100+ tokens/second
- HuggingFace: https://huggingface.co/0xSero/sero-nouscoder-14b-sft

---

# SECTION 4: SMART CONTRACT SECURITY / AUDITING APPROACHES

Source: Blog posts, GitHub repos, video notes

## MEV Bot Defense (Blog: MEV Bots and the Dark Forest)

- Built arbitrage bots for profitable function calls on smart contracts
- Analyzed bot competition: reactive bidding vs blind bidding
- Sophisticated bots (like 0xC0ffeEBABE5D496B2DDE509f9fa189C25cF29671) use:
  - Multi-layered obfuscation techniques
  - Transient storage to hide strategy details
  - Dynamic code execution paths
  - Complex gatekeeping mechanisms
  - WETH manipulation capabilities
  - Miner incentivization for transaction ordering
  - Handcrafted assembly to avoid detection

### Practical Defenses for Contract Designers
- Time-locked execution mechanisms (delay between intent and execution)
- Commit-reveal patterns (hide transaction details until execution)
- Strategic honeypot transactions (poison the well for blind bots)
- Unpredictable execution paths (make simulation expensive/unreliable)

### Flashbots Limitations
- Doesn't prevent MEV completely
- Bots monitor mined blocks and all transactions within
- Re-simulate transactions to uncover patterns over time
- Pattern recognition to predict profitable opportunities before mempool

### Smart Contract Security Patterns (from coding rules)
- Use strict types (`unknown` + Zod, never `any`)
- Centralize config to prevent magic strings
- File size limits prevent monolithic contract files
- Interface patterns allow environment swapping (dev/prod)
- Cross-session learning log catches recurring vulnerabilities
- Pre-commit security scan: `grep -r "sk-\|pk-\|0x[a-fA-F0-9]{64}" --exclude-dir=node_modules`

## Smart Contract / DeFi Repos

| Repo | Description |
|------|------------|
| must-finance | DeFi protocol |
| poidh-v3 | Protocol |
| zksync-staker | zkSync staking contract |
| solidity-weighted-averages | Solidity math library |
| generalized-frontrunner | MEV frontrunning bot |
| mev-bundle-generator | MEV bundle creation |
| simple-arbitrage | Arbitrage bot |
| apebot | Trading bot |

---

# SECTION 5: PROMPT ENGINEERING PATTERNS

## .cursor/rules Pattern
Project-specific instructions file that Cursor follows when generating code. Covers UI/styling, performance, architecture rules.

## AGENTS.md Pattern
Per-module context files documenting:
- Which files do what
- Correct imports and function names
- Gotchas ("Use multisigCreateV2, NOT multisigCreate")
- Decimals and unit conventions
- Max file sizes per module

## Acceptance Criteria Template
```
## Deliverables
- [ ] File A modified
- [ ] File B created
- [ ] Tests pass

## Acceptance
- [ ] Compiles without errors
- [ ] Handles edge case X
- [ ] Matches style of existing code
```

## Reproduction Template
```
## Error
[exact error message]
## Expected
[what should happen]
## Actual
[what actually happens]
## Minimal repro
[shortest code that demonstrates the issue]
```

## @Docs Feature Usage
1. Type @ in Chat/Composer, select "Docs", enter URL
2. Reference with @Name syntax
3. Auto re-indexes as docs change

## State Machine Debugging Prompt
"Create an ASCII state machine diagram of [flow] in this project. Show all states, transitions, and which file handles each state."

---

# SECTION 6: RULES & GUARDRAILS FOR AI AGENTS

## codex-local Orchestration Guardrails
- max_concurrent_agents = 5
- agent_timeout_seconds = 300
- enable_progress_tracking = true
- model_auto_compact_token_limit = 90000 (75% of 120K context)
- Auto-summarization at 80% context capacity
- ContinuationTurn ensures main agent always resumes

## vllm-studio Deployment Guardrails
1. Build check: `cd frontend && npx next build` first
2. Docker staging build + verify before deploy
3. Remote deploy via scripts
4. Desktop Electron build REQUIRED with each release
5. Clean install (rm -rf then ditto)
6. Verify bundle ID: org.vllm.studio.desktop

## Orchestra Multi-Agent Profiles
6 worker profiles: Vision, Docs, Coder, Architect, Explorer, Memory
Neo4j memory graph for persistent agent knowledge
Hub-and-spoke architecture

## Data Privacy Guardrails
- PII scan and masking on all training data
- 95,561/107,502 conversations quarantined for sensitive data
- Pattern replacements for GitHub tokens, HF tokens, OpenAI keys, Anthropic keys, Slack tokens
- Path rewrites: /Users/sero -> /<ABS>/
- Privacy-preserving analysis (no raw text storage)
- Pre-commit hooks scanning for API keys and private keys

---

# SECTION 7: COMPLETE GITHUB REPOSITORY LISTING

Source: https://github.com/0xSero
Total repos: 204 | Primary languages: TypeScript, Python, Rust

## Top Repos by Stars

| Repo | Stars | Lang | Description |
|------|------:|------|------------|
| turboquant | 1052 | Python | KV cache quantization for LLM inference (ICLR 2026). 3-bit keys, 2-bit values. Triton kernels + vLLM integration. 4.41x compression. |
| ai-data-extraction | 611 | Python | Extract ALL personal data from Cursor, Codex, Claude Code, Windsurf, Trae, Continue, Gemini CLI, OpenCode. Python stdlib only. |
| parchi | 498 | TypeScript | AI-powered browser copilot. Chrome MV3 + Firefox extension. Chat-driven automation. BYOK with any OpenAI-compatible endpoint. Relay daemon + Electron CDP automation. |
| vllm-studio | 437 | TypeScript | Unified local AI workstation. Control panel for VLLM, Sglang, llama.cpp, exllamav3. Bun/Hono + Next.js. |
| orchestra | 272 | TypeScript | Multi-agent orchestration for OpenCode. Hub-and-spoke architecture. 6 worker profiles (Vision, Docs, Coder, Architect, Explorer, Memory). Neo4j memory graph. |
| moe-compress | 178 | Python | MoE compression automation: REAP/quantization/benchmark/publish |
| Azul | 163 | Rust | Terminal browser |
| pi-brain | 155 | TypeScript | (undocumented) |
| open-queue | 126 | TypeScript | (undocumented) |
| reap-expert-swap | 118 | Python | Expert pruning for MoE models |
| factory-cursor-bridge | 71 | JavaScript | BYOK proxy wiring ~/.factory/config.json models into Cursor IDE |
| open-trees | 69 | TypeScript | Opencode plugin for managing git worktrees |
| codex-local | 62 | Rust | Modified Codex CLI for local LLMs |
| mem-layer | 79 | Python | Organise AI memories with graph database entries |
| claude-acp-server | 88 | TypeScript | Anthropic-compatible HTTP facade over claude-agent-acp |
| minimax-m2-proxy | 40 | Python | Proxy for minimax-m2 with interleaved thinking + tool calls |
| reap-mlx | 53 | TypeScript | REAP expert pruning for MoE LLMs on Apple Silicon via MLX |

## By Category

**AI/LLM Infrastructure**: turboquant, vllm-studio, codex-local, orchestra, moe-compress, reap-expert-swap, reap-mlx, exllamav3, vllm-paged-experts, zai-proxy, minimax-m2-proxy, home-rag, vlm-computer-use

**Browser/Automation**: parchi, sitegeist

**Data/Research**: ai-data-extraction, research-context-manager, autoresearch, Training-recipes

**Smart Contracts/DeFi**: must-finance, poidh-v3, zksync-staker, solidity-weighted-averages, generalized-frontrunner, mev-bundle-generator, simple-arbitrage, apebot

**Dev Tools**: factory-cursor-bridge, open-trees, mem-layer, claude-acp-server, claude-skill-dir, cerebras-code-cli, opencode

---

# SECTION 8: HOMELAB INFRASTRUCTURE

Source: Blog post "Building My Own Homelab"

## Hardware Specifications

| Component | Specification | Cost |
|-----------|-------------|------|
| GPUs | 8x RTX 3090 (24GB each = 192GB VRAM) | $7,118.64 |
| Memory | 512GB DDR4 ECC | $2,224.61 |
| Motherboard | ASRock Romed8-2T | $902.63 |
| CPU | EPYC 7443P | $739.01 |
| Storage | 2TB + 4TB Samsung NVMe | $552.54 |
| Power | 2x 1,600W Corsair + 1,000W Corsair | $723.00 |
| Case | Custom zip-tied rack | ~$100 |
| **Total** | | **~$12,360** |

## Performance Benchmarks

| Metric | Value | Configuration |
|--------|-------|-------------|
| Prefill Throughput | 3,000-9,000 TPS | 4-8x 3090 + vLLM |
| Generation Throughput | 35-50 TPS | 4x 3090 + vLLM optimized |
| Context Window | 180k tokens | 6x 3090 (174GB VRAM) |
| Peak VRAM Usage | 192GB | 8x 3090 full load |

## Cost Comparison

| Factor | Corporate AI | Homelab |
|--------|-------------|---------|
| Cost per month | $2,000+ | $50 (electricity) |
| Rate limits | Constant concern | None |
| Data privacy | Sent to servers | Never leaves home |
| Model customization | Locked | Full control |
| API stability | Changes constantly | Fixed forever |
| Context window | 200k (expensive) | 500k+ (free) |

## vLLM Launch Config
```
vllm serve /mnt/llm_model/GLM-4.5-Air-AWQ-4bit \
  --tensor-parallel-size 4 \
  --dtype bfloat16 \
  --max-model-len 131072 \
  --gpu-memory-utilization 0.95 \
  --enable-chunked-prefill
```

## Private Home RAG Stack
- Database: PostgreSQL with pgvector
- Embedding: BGE-M3 (dense + sparse + multi-vector)
- Index: HNSW for fast retrieval
- Storage: 1.2TB indexed documents
- Indexes: financial records, legal docs, contracts, photos, writing, messages, emails

---

# SECTION 9: BLOG POSTS (COMPLETE)

Source: https://blog.ethers.club -> https://www.sybilsolutions.ai

## Post 1: I ragged every conversation I ever had with AI (2026-01-17)
URL: https://www.sybilsolutions.ai/blog/01-how-i-work-with-ai

Analysis of 809 AI conversations (727MB extracted from Cursor, Claude, Codex).
19,539 user messages, 11,726 assistant messages, 16,484 tool uses.
Composite indices on 0-1 scale: Spec completeness 0.275, Debug maturity 0.056,
Testing discipline 0.096, Security awareness 0.058, Architecture-thinking 0.168.
Self-identified gaps: minimal reproduction (0.4%), test discipline, security hygiene
(32.5% risky disclosure), acceptance criteria. Action plan: repro templates,
test checklists, security scans, acceptance criteria.

## Post 2: Training My Own Coding Model (2026-01-17)
URL: https://www.sybilsolutions.ai/blog/02-training-my-coding-model-the-pipeline

Full pipeline: 107K conversations -> PII scan (89% quarantined) -> 11,711 clean ->
temporal ordering -> dedup (13,634 duplicates skipped) -> SFT on NousCoder 14B
(QLoRA 4bit, rank 64, alpha 128, dropout 0.05, batch size 2, grad accum 8,
lr 2e-5 cosine, 2.52 epochs, 18 hours on A100, $47). Final loss: 0.685,
accuracy: 81.6%. 51.75M tokens. Dataset: 35% Solidity, 30% TS, 20% Python,
10% SQL, 5% Other. DPO pairs: 4,532 prepared. Model:
https://huggingface.co/0xSero/sero-nouscoder-14b-sft

## Post 3: AI-driven NFT marketplace (2022-08-28)
URL: https://www.sybilsolutions.ai/blog/AI-and-marketing

Platform concept: AI-generated art for marketing + NFT minting for ownership/royalties.
Two user types: Creators/Sponsors and AI artist/platform users.

## Post 4: AI Workflows as an Assembly Line (2024-10-10)
URL: https://www.sybilsolutions.ai/blog/AI-workflows

DevRel workflow automation using AI agents. Key components:
Loader Agents (consume org-specific info), Conversational Agents (answer queries),
Content generation, Feedback loops, Monitoring/analytics.
Flowchart: User Question -> Q&A Agent -> Loader Agent + PII Obfuscation + Sentiment
Agent -> Discord/Slack -> Response Sent.

## Post 5: Employment Scams - Deep Dive (2024-04-03)
URL: https://www.sybilsolutions.ai/blog/Modern-day-scams

Technical analysis of SpectraChat/SpectraSocial malware:
- .exe installer copies to /Spectra, reinstalls on deletion
- Hijacks browser crypto wallet plugins
- Replaces 0x addresses via clipboard hijacking (browser-only)
- Doesn't escape VMs or infect network
- Doesn't pick up desktop seed phrases

## Post 6: AI-Assisted Coding: What Actually Works (2024-12-23)
URL: https://www.sybilsolutions.ai/blog/ai-assisted-coding-experience

Context windows: 200-line React ~1,500 tokens, Python ~1,700 tokens.
Golden rule: keep files under 400 lines.
Pattern: design hard parts yourself, AI handles repetitive stuff.
Projects built: ai-data-extraction, orchestra, azul, mem-layer,
minimax-m2-proxy, codex-local.

## Post 7: Choosing a crypto-wallet Part 1 (2022-07-24)
URL: https://www.sybilsolutions.ai/blog/choosing-a-crypto-wallet-for-your-web3-journey

Wallet fundamentals: random number -> encryption -> private key.
Public key = mailbox address. Private key = password. Never share.

## Post 8: Employment Red Flags (2022-10-26)
URL: https://www.sybilsolutions.ai/blog/employment-red-flags

Warning signs: NDAs weaponized, non-compete traps, irregular payments,
excessive demands. Personal examples of each.

## Post 9: MEV Bots and the Dark Forest (2024-12-23)
URL: https://www.sybilsolutions.ai/blog/mev-bots-and-dark-forests

Built arbitrage bots, discovered MEV depth. Bot sophistication:
multi-layered obfuscation, transient storage, handcrafted assembly.
Defenses: time-locked execution, commit-reveal, honeypot transactions,
unpredictable execution paths.

## Post 10: How to remove unwanted content from the web (2022-10-16)
URL: https://www.sybilsolutions.ai/blog/remove-unwanted-content

Social media protection, DMCA takedown process, GDPR erasure requests.

## Post 11: The Benefits Of Scrum (2022-07-08)
URL: https://www.sybilsolutions.ai/blog/the-benefits-of-scrum

Scrum pillars: Transparency, Inspection, Adaptation.

## Post 12: Choosing a crypto-wallet Part 2 (2022-07-25)
URL: https://www.sybilsolutions.ai/blog/understanding-the-types-of-cryptocurrency-wallets

Paper wallets (obsolete), Software wallets (hot, convenient), Hardware wallets
(cold, secure). When to use each.

## Post 13: Building My Own Homelab (2026-01-15)
URL: https://www.sybilsolutions.ai/blog/Building-my-own-homelab

Full journey from AI dependency to local superpower. 8x RTX 3090 rig,
$12,360 total cost. vLLM optimized: 35-50 TPS generation, 180k context.
Monthly cost: $50 electricity vs $2,000+ corporate AI.
Private home RAG: PostgreSQL + pgvector + BGE-M3, 1.2TB indexed.

---

# SECTION 10: X/TWITTER POST

Source: https://x.com/0xSero/status/2035762691235516508
Date: March 22, 2026 | Likes: 631 | Replies: 18

Tweet: "Tons of people followed me in the last 3 days, here's my most important
video for learning how to work like me."
Linked: https://youtu.be/VgR66ybAtdg ("Agentic coding 101")

---

# SOURCE URLS

1. https://github.com/0xSero/codex-local (README, AGENTS.md, README-CODEX-LOCAL.md, orchestrator_workflow_design.md)
2. https://github.com/0xSero (profile, all repos)
3. https://blog.ethers.club -> https://www.sybilsolutions.ai (13 blog posts)
4. https://github.com/0xSero/vllm-studio (README, AGENTS.md)
5. https://x.com/0xSero/status/2035762691235516508
6. https://github.com/ToXMon/swigpay-complete/blob/main/context/0xSero-agentic-lessons.md
7. https://www.youtube.com/watch?v=VgR66ybAtdg (Agentic Coding 101 video)
8. https://huggingface.co/0xSero/sero-nouscoder-14b-sft
