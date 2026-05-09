# token-efficiency-mode Agent Zero skill

Date: 2026-05-09

Created `token-efficiency-mode` skill to reduce Agent Zero token usage while preserving correctness.

Paths:
- `/a0/usr/skills/token-efficiency-mode/SKILL.md`
- `/a0/usr/skills/token-efficiency-mode/tests/benchmark.md`
- `/a0/usr/workdir/tolu/skills/token-efficiency-mode/SKILL.md`
- `/a0/usr/workdir/tolu/skills/token-efficiency-mode/tests/benchmark.md`

Core behavior:
- Output modes: `lite`, `full`, `ultra`, `off`.
- Preserves commands, paths, errors, security findings, test failures, and user-visible decisions.
- Uses lean context selection: search/discover first, narrow file ranges, full reads only when needed.
- Compresses shell/tool results into command, exit status, signal, errors, next action.
- Requires compact handoff notes and memory-palace saves for durable discoveries.

Attribution: independently adapts ideas from JuliusBrussee/caveman and yvgude/lean-ctx.
