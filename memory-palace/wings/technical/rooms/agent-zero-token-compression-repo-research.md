# Agent Zero Token Compression Repo Research

Date: 2026-05-09

Static research only, no project install. Repos cloned shallow into `/a0/usr/workdir/repo_static_research_1778329530/`:
- https://github.com/JuliusBrussee/caveman
- https://github.com/yvgude/lean-ctx

## Inspected files

caveman: `README.md`, `skills/caveman/SKILL.md`, `caveman-compress/README.md`, `caveman-compress/SKILL.md`, `caveman-compress/scripts/validate.py`, `mcp-servers/caveman-shrink/README.md`, `hooks/README.md`, `hooks/caveman-mode-tracker.js`, `hooks/caveman-activate.js`, `hooks/caveman-config.js`, `agents/cavecrew-investigator.md`, `agents/cavecrew-builder.md`, `agents/cavecrew-reviewer.md`, `evals/README.md`, `benchmarks/run.py`.

lean-ctx: `README.md`, `ARCHITECTURE.md`, `BENCHMARKS.md`, `LEANCTX_FEATURE_CATALOG.md`, `LEAN-CTX.md`, `discord-faq/02-how-it-works.md`, `discord-faq/03-shell-hook-issues.md`, `docs/premium-cache-heatmap.md`, `docs/contracts/context-ir-v1.md`, `docs/contracts/ccp-session-bundle-v1.md`, `docs/contracts/handoff-transfer-bundle-v1.md`, `docs/contracts/memory-boundary-contract-v1.md`, `rust/examples/token_impact.rs`, `rust/examples/lean-ctx-session-metrics.mdc`, `rust/src/cli/context_cmd.rs`, `rust/src/cli/pack_cmd.rs`, `rust/src/cli/session_cmd.rs`, `rust/src/cli/shell_init.rs`, `rust/src/core/context_compiler.rs`, `rust/src/core/context_ir.rs`, `rust/src/core/cache.rs`, `rust/src/core/semantic_cache.rs`, `rust/src/core/session.rs`, `rust/src/core/session_diff.rs`, `rust/src/core/context_handles.rs`, `rust/src/core/budget_tracker.rs`, `rust/src/core/compression_safety.rs`.

## Transferable ideas for Agent Zero skill

1. Caveman-style response modes: concise style can be a sticky mode with explicit off-ramp, exact preservation of code/symbols/errors, and escalation back to normal prose when compression creates ambiguity.
2. Memory-file compression: rewrite long prompt/memory docs into terse form, keep `.original.md` backup, validate headings/code/URLs/paths/inline code, and patch only failed regions instead of recompressing whole files.
3. Tool schema compression: compress tool/prompt/resource descriptions while leaving tool-call payloads and responses untouched.
4. Hook/state bridge: session-start activation plus per-turn prompt tracking can maintain mode without repeatedly injecting full instructions; flag files/config must fail safely.
5. Compressed subagents: locator/reviewer/editor agents should return file:line receipts and bounded scopes, reducing main-context tool output.
6. Honest evals: compare against a terse control, not only verbose baseline; commit snapshots; report ratios and fidelity limits.
7. lean-ctx read modes: use `full` only for edited files; default to `auto/map/signatures/diff/task/aggressive/lines` for context-only reads.
8. Cache and handles: cached read stubs, compressed-output caches, context handles, and mtime/hash validation reduce repeated file context while avoiding stale content.
9. Shell output compression safety: classify commands by safety level; preserve git status/diff/path/auth-sensitive output when loss would harm correctness; provide raw bypass.
10. Session/context packs: persist task/findings/decisions/evidence/stats and portable context packs with project identity hashes, redaction defaults, and additive imports for session recovery.

## Attribution wording

"This skill borrows ideas from Julius Brussee's caveman project for terse-but-accurate agent output, memory-file compression with preservation checks, MCP description shrinking, hook-driven mode persistence, and token-sparing subagents; and from yvgude's lean-ctx project for mode-aware file reads, shell-output compression, cache/handle based context reuse, session recovery, context packages, budgets, and token-savings measurement. This is an independent Agent Zero adaptation; no code copied unless explicitly stated."
