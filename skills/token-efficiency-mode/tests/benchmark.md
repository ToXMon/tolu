# token-efficiency-mode benchmark examples

Rough estimates only. Use tokenizer-backed counts later if available. Targets assume the same facts are preserved.

## 1. Normal answer vs lite/full/ultra

| Version | Example | Rough tokens | Target |
|---|---|---:|---:|
| Normal | `I inspected the project and found that the tests are failing because the login helper expects a token field that no longer exists. The next step is to update the helper and rerun the focused login test.` | 39 | baseline |
| lite | `Issue: login helper expects removed token field. Next: patch helper; rerun focused login test.` | 17 | 55% less |
| full | `Issue: removed token field. Fix helper. Test: login focused.` | 12 | 69% less |
| ultra | `Issue: token field gone. Fix helper → login test.` | 10 | 74% less |

## 2. Raw shell output vs compressed shell summary

| Version | Example | Rough tokens | Target |
|---|---|---:|---:|
| Raw | `npm test` output with install banner, 200 passing lines, repeated warnings, final failure block | 1200 | baseline |
| Compressed | `Cmd: npm test. Exit: 1. Signal: 218 passed, 1 failed. Error: auth.test.ts:88 expected 200 got 401. Next: inspect auth middleware and failing test.` | 38 | 95% less |

Rule: preserve exact failing test, file, assertion, and status. Drop repeated success noise.

## 3. Full file read request vs narrow read plan

| Version | Example | Rough tokens | Target |
|---|---|---:|---:|
| Full read | Read all of `src/auth.ts` and `src/session.ts` before deciding | 5000 | baseline |
| Narrow plan | `grep -R "function login\|class Session\|token" src tests`; read matching ranges plus imports | 45 | 99% less upfront |

Rule: full-file reads are allowed when patch safety or syntax requires them.

## 4. Long research report vs executive compressed report

| Version | Example | Rough tokens | Target |
|---|---|---:|---:|
| Long report | Full repo narrative with copied README sections, setup details, and every file inspected | 2500 | baseline |
| Compressed | `Sources: README, ARCHITECTURE, docs/contracts. Adapt: mode-aware reads, shell summaries, context packs, cache handles. Risk: hooks need framework work.` | 45 | 98% less |

Rule: keep source paths/URLs and decision impact; do not paste source text unless needed.

## 5. Debugging trace with preserved critical error detail

| Version | Example | Rough tokens | Target |
|---|---|---:|---:|
| Noisy trace | Full 400-line traceback | 3000 | baseline |
| Unsafe compression | `Build failed. Type error.` | 5 | invalid |
| Safe compression | `Cmd: npm run build. Exit: 2. Error: src/api.ts:42:13 TS2339 Property 'token' does not exist on type 'Session'. Impact: build blocked. Next: inspect Session type + caller.` | 44 | 98% less |

Rule: never hide exact causal error, path, line, code, or blocked verification.
