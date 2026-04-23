# 0xSero GitHub Repositories - Complete Content Extraction

Extracted: 2026-04-16

---

## Task 1: codex-local (https://github.com/0xSero/codex-local)

- **Branch**: `local/llms`
- **Language**: Rust
- **Stars**: 62
- **Updated**: 2026-04-12
- **Description**: A modified Codex CLI application built to support local LLMs

### Key Architecture Components
- `codex-rs/core/src/child_agent_bridge.rs` - Parent-child agent communication
- `codex-rs/core/src/conversation_manager.rs` - Multi-agent conversation management
- `codex-rs/core/src/tools/handlers/spawn_agent.rs` - Agent spawning tool
- `codex-rs/core/src/tools/handlers/return_progress.rs` - Progress reporting tool
- `codex-rs/core/src/tools/parallel.rs` - Parallel tool execution
- `codex-rs/orchestrator/` - Full orchestrator subsystem

### Source URLs
- README: https://raw.githubusercontent.com/0xSero/codex-local/local/llms/README.md
- AGENTS.md: https://raw.githubusercontent.com/0xSero/codex-local/local/llms/AGENTS.md
- README-CODEX-LOCAL.md: https://raw.githubusercontent.com/0xSero/codex-local/local/llms/README-CODEX-LOCAL.md
- Orchestrator Workflow: https://raw.githubusercontent.com/0xSero/codex-local/local/llms/orchestrator_workflow_design.md

---

## Task 2: 0xSero Profile - All Repositories

Source: https://api.github.com/users/0xSero/repos?per_page=100&sort=updated

### Top Repositories by Stars

| Repo | Stars | Language | Description |
|------|------:|----------|-------------|
| turboquant | 1052 | Python | TurboQuant: Near-optimal KV cache quantization for LLM inference (3-bit keys, 2-bit values) with Triton kernels + vLLM integration |
| ai-data-extraction | 611 | Python | Extract all your personal data history from cursor, codex, claude-code, windsurf, and trae |
| parchi | 498 | TypeScript | Your AI friend right in your browser (browser automation extension) |
| vllm-studio | 437 | TypeScript | Control panel for VLLM, Sglang, llama.cpp, exllamav3 |
| orchestra | 272 | TypeScript | Multi-Agent Orchestration for OpenCode (hub-and-spoke architecture) |
| pi-brain | 155 | TypeScript | (undocumented) |
| moe-compress | 178 | Python | Model-agnostic MoE compression automation: build calibration bundles, run REAP/quantization/benchmark/publish stages |
| Azul | 163 | Rust | Browse the world in the comfort of your terminal |
| open-queue | 126 | TypeScript | (undocumented) |
| reap-expert-swap | 118 | Python | How much experts do we need to serve a model? |
| turboquant | 1052 | Python | KV cache quantization for LLM inference |

### All Repositories (Sorted by Updated)

See full listing in extracted data. Notable categories:

**AI/LLM Infrastructure**: turboquant, vllm-studio, codex-local, orchestra, moe-compress, reap-expert-swap, reap-mlx, exllamav3, vllm-paged-experts, zai-proxy, minimax-m2-proxy, home-rag, vlm-computer-use

**Browser/Automation**: parchi, sitegeist, agent-browser

**Data/Research**: ai-data-extraction, research-context-manager, autoresearch, Training-recipes, personal-recommendation-algo

**Smart Contracts/DeFi**: must-finance, poidh-v3, zksync-staker, solidity-weighted-averages, generalized-frontrunner, mev-bundle-generator, simple-arbitrage, apebot, fundraiser, zksync-rss

**Developer Tools**: factory-cursor-bridge, open-trees, mem-layer, codify, claude-acp-server, claude-agent-acp, claude-skill-dir, claude-code-infrastructure-showcase, cerebras-code-cli, opencode

**Agent Frameworks**: orchestra, codex-local, Mini-Agent, orchestrator, claude-scratchpad, swarm-together

---

## Task 3: vllm-studio (https://github.com/0xSero/vllm-studio)

- **Branch**: `main`
- **Language**: TypeScript
- **Stars**: 437
- **Updated**: 2026-04-16
- **Description**: Control panel for VLLM, Sglang, llama.cpp, exllamav3
- **Version**: v1.13.0

### Architecture
- `controller/` - Bun/Hono backend, orchestration, chat runtime, lifecycle, metrics
- `frontend/` - Next.js app, chat UI, proxy endpoints, client state
- `cli/` - Bun CLI for controller access
- `shared/` - shared types/contracts
- `config/` - runtime and integration configs
- `scripts/` - operational scripts (deployment + controller daemon helpers)
- `skills/` - vllm-studio skills (visual-explainer, evidence-heavy-evaluator, vllm-studio-backend)

### Source URLs
- README: https://raw.githubusercontent.com/0xSero/vllm-studio/main/README.md
- AGENTS.md: https://raw.githubusercontent.com/0xSero/vllm-studio/main/AGENTS.md
- Frontend AGENTS.md: https://raw.githubusercontent.com/0xSero/vllm-studio/main/frontend/AGENTS.md

---

## Additional: Top Repo READMEs

### parchi (498 stars)
- Source: https://raw.githubusercontent.com/0xSero/parchi/main/README.md
- Browser extension (Chrome MV3 + Firefox) for chat-driven browser automation
- Supports BYOK with any OpenAI-compatible endpoint
- Relay daemon for external tool/script control
- Electron desktop automation via CDP
- Workspaces: backend (Convex), cli, electron-agent, extension, relay-service, shared, website

### orchestra (272 stars)
- Source: https://raw.githubusercontent.com/0xSero/orchestra/main/README.md
- Multi-agent orchestration plugin for OpenCode
- Hub-and-spoke architecture with 6 built-in worker profiles: Vision, Docs, Coder, Architect, Explorer, Memory
- 5-tool async task API: start/await/peek/list/cancel
- Optional Neo4j memory graph
- Bun runtime

### turboquant (1052 stars)
- Source: https://raw.githubusercontent.com/0xSero/turboquant/main/README.md
- ICLR 2026 paper implementation
- KV cache compression: 3-bit keys, 2-bit values
- Triton kernels + vLLM integration
- Benchmarked on RTX 5090 and 8x RTX 3090
- 4.41x compression ratio, 2x context extension on dense models

### ai-data-extraction (611 stars)
- Source: https://raw.githubusercontent.com/0xSero/ai-data-extraction/main/README.md
- Extracts chat/agent data from: Cursor, Claude Code, Codex, Windsurf, Trae, Continue, Gemini CLI, OpenCode
- Output: JSONL with messages, code context, diffs, metadata
- Python 3 standard library only, no dependencies
