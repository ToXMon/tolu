# Agentic Coding Philosophies: 0xSero vs Ryan Carson

Extracted: 2026-04-16

## Quick Comparison

| Dimension | 0xSero | Ryan Carson |
|-----------|--------|-------------|
| Background | Web3/smart contract security, Sybil Solutions | 5x founder (Treehouse 1M+ users), Amp Builder in Residence |
| Philosophy | Encode context into repo structure, let tooling enforce | Developer becomes engineering manager for AI agents |
| Core workflow | 10 rules + Ralph autonomous loop | 3-step PRD > Tasks > Build |
| Primary tools | Claude Code, Codex-local (Rust), vLLM, OpenCode | Cursor Agent Mode, Claude, Gemini 2.5 Pro |
| Memory system | AGENTS.md per module + progress.txt | AGENTS.md + reflection prompts + living task lists |
| Scale approach | 8 concurrent projects via autonomous agents | Solo founder replacing full engineering teams |
| Infrastructure | 8x RTX 3090 homelab, custom 14B model | Cloud-first, Cursor-centric |
| Key innovation | codex-local multi-agent orchestration (Rust) | Code Factory (auto-write + auto-review pipeline) |
| Context discipline | 300 lines/file, 20 files/dir, ESLint-enforced | Fresh agent per task, MAX mode for planning |

## Shared Patterns (Both Agree On)
- AGENTS.md for cross-session context persistence
- Task queuing - never batch, one task at a time
- Context window management - fresh sessions, scoped context
- File-based memory over vector DBs
- Ralph/autonomous loop pattern for unsupervised work
- Human handles architecture, AI handles implementation
- progress.txt or similar for cross-session learning

## Key Differences
- 0xSero: infrastructure/deep-tech (local models, Rust agents, Web3 security)
- Carson: workflow/process (PRDs, Cursor templates, solo founder enablement)
- 0xSero enforces via linting/tooling; Carson enforces via process/templates
- 0xSero custom-trained his own model; Carson uses frontier models
