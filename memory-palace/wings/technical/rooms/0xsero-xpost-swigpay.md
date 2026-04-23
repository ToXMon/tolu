# 0xSero: X/Twitter Post + Swigpay Agentic Lessons

---

## Source 1: X/Twitter Post

**URL:** https://x.com/0xSero/status/2035762691235516508
**Author:** 0xSero (@0xSero)
**Date:** March 22, 2026 at 16:57:02 UTC
**Likes:** 631
**Conversation count (replies):** 18
**Verified:** Blue verified

### Full Tweet Text

Tons of people followed me in the last 3 days, here's my most important video for learning how to work like me.

https://t.co/HUkxDIHokU

### Linked Content

- **Expanded URL:** https://youtu.be/VgR66ybAtdg
- **YouTube Video:** "Agentic coding 101 - How I work on 8 projects at a time"
- **Card description:** "This is how i use claude code and codex to code on 8x projects at a time"
- **YouTube embed:** https://www.youtube.com/embed/VgR66ybAtdg

### Context: Agentic Coding Approach

This tweet promotes 0xSero's flagship YouTube video explaining his agentic coding workflow. The video covers how he uses Claude Code and Codex to manage 8 concurrent projects simultaneously. The approach centers on encoding project context into repo structure (via AGENTS.md files, progress.txt, centralized config) so that AI coding agents can work autonomously without repeated manual context injection. His philosophy: trust the LSP, enforce constraints via tooling, and let the agent self-correct.

### Related Transcript

Full transcript saved at: `tolu/memory-palace/youtube/transcripts/0xsero-agentic-coding-101.md`

---

## Source 2: Swigpay Agentic Lessons File

**URL:** https://github.com/ToXMon/swigpay-complete/blob/main/context/0xSero-agentic-lessons.md
**Raw URL:** https://raw.githubusercontent.com/ToXMon/swigpay-complete/main/context/0xSero-agentic-lessons.md
**File size:** 206 lines (147 loc) / 6.52 KB

### Full Verbatim Content

~~~markdown
# 0xSero Agentic Coding Hard-Won Lessons
# Source: https://youtu.be/VgR66ybAtdg — "Agentic coding 101 - How I work on 8 projects at a time"
# Applied to: SwigPay hackathon project

---

## The Core Mental Model

> "You can just trust that your LSP will provide the model the context it needs.
> You just look at the results at the end."

Stop re-explaining the codebase to the agent every session.
Instead, encode it ONCE into the repo structure and let tooling enforce it.

---

## Rule 1: File & Directory Size Limits (Enforce via LSP/tsconfig)

**Max 300 lines per file. Max 20 files per directory.**

These are ERRORS, not warnings. When Cascade violates them, the LSP flags it automatically
and the agent self-corrects without you asking.

Add to `tsconfig.base.json` (not standard TS, but enforce via ESLint plugin):
```json
// .eslintrc equivalent — add to project
// "max-lines": ["error", 300]
// "max-depth": ["error", 4]
```

**Why it matters for SwigPay:** Cascade will try to put all Squads logic in one 500-line file.
Force it to split: `squads-create.ts`, `squads-limits.ts`, `squads-execute.ts`.

---

## Rule 2: No `any` Types — Use `unknown` + Zod

```typescript
// ❌ Agent default (lazy)
const result: any = await client.callTool(name, args);

// ✅ 0xSero pattern (strict)
const result: unknown = await client.callTool(name, args);
const parsed = PaymentResultSchema.parse(result); // Zod validates shape
```

`any` types cause drift across sessions — the agent starts making inconsistent assumptions.
`unknown` + Zod forces explicit contracts that survive context window boundaries.

---

## Rule 3: Centralized Config — Single Source of Truth

**Everything imports from ONE config file. Nothing is duplicated.**

```typescript
// src/config.ts — the ONLY place constants live
export const SOLANA_CONFIG = {
  network: process.env.SOLANA_NETWORK ?? "devnet",
  rpcUrl: process.env.SOLANA_RPC_URL ?? "https://api.devnet.solana.com",
  usdcMint: "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU",
  facilitatorUrl: process.env.FACILITATOR_URL ?? "https://x402.org/facilitator",
  squadsProgram: "SQDS4ep65T869zMMBKyuUq6aD6EgTu8psMjkvj52pCf",
} as const;

// ❌ NEVER do this in a tool or agent file:
const USDC = "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU"; // duplicate!
```

When the agent edits config, it edits ONE file. Prevents the "magic string scattered
across 12 files" problem that compounds over hackathon sessions.

---

## Rule 4: Database Interface Pattern — Swap Environments

Define a typed interface, implement it twice, switch via env var.

```typescript
// For SwigPay: already done in db.ts with better-sqlite3
// If you need a hosted DB later: implement the same interface with Supabase
// Switch: DATABASE=sqlite (default) or DATABASE=supabase

interface IPaymentDB {
  insertPayment(record: Omit<PaymentRecord, "id">): number;
  getPaymentsByAgent(agentId: string, limit?: number): PaymentRecord[];
  updatePaymentStatus(id: number, status: PaymentStatus, txHash?: string): void;
  getSpentToday(agentId: string): number;
}
```

---

## Rule 5: AGENTS.md Files at Every Module Level

Each subdirectory gets its own `AGENTS.md`. Windsurf auto-loads it when Cascade
enters that directory (glob-scoped).

**For SwigPay, add these files:**

`packages/agent-wallet/AGENTS.md`:
```markdown
# agent-wallet module
- squads.ts: Squads v4 multisig create + spending limit. Use multisigCreateV2, NOT multisigCreate.
- x402client.ts: createx402MCPClient wrapper. Import ExactSvmScheme from "@x402/svm" (not /exact/server).
- spendPolicy.ts: Off-chain enforcement. Called BEFORE x402 payment attempt.
- db.ts: SQLite via better-sqlite3. All amounts stored as both amountUsdc (float) and amountRaw (integer).
- USDC decimals: 6. 1 USDC = 1_000_000 raw. Never confuse.
```

`apps/mcp-server/AGENTS.md`:
```markdown
# mcp-server module
- server.ts: @x402/mcp createPaymentWrapper. Import ExactSvmScheme from "@x402/svm/exact/server".
- tools/: Each tool is its own file. Max 100 lines each.
- Port: 4022. SOLANA_DEVNET_CAIP2 imported from @x402/svm — never hardcode.
- Free tools: no wrapper. Paid tools: wrapWithPayment(handler).
```

`apps/dashboard/AGENTS.md`:
```markdown
# dashboard module
- Next.js 15 App Router. All API routes in app/api/*/route.ts.
- DB access: import from @swigpay/agent-wallet (the workspace package).
- Polling: 5-second interval via setInterval in useEffect.
- No external API calls from frontend — all data via /api routes.
```

---

## Rule 6: progress.txt — Cross-Session Learning Log

Create this file at project root. Cascade appends to it after every work session.
Future sessions READ it first — compound learning without context bloat.

```markdown
# SwigPay Progress Log

## Codebase Patterns (agent reads this section first)
[Filled in as development progresses]

## Session Log
---
```

---

## Rule 7: 2/3 Cadence — Feature vs. Refactor

**2 days features → 3 days refactoring → repeat.**

For SwigPay in 8 hours:
- Hours 1-5: Build features (phases 1-3)
- Hours 6-7: Refactor (deduplicate, split large files, fix any types)
- Hour 8: Demo prep (README, video, submit)

**Without the refactor hour:** Cascade's code accumulates drift.
The demo demo fails because config is duplicated in 3 places.

---

## Rule 8: State Machine Diagram Before Debugging

When stuck on a Squads or x402 flow, ask Cascade:

```
"Create an ASCII state machine diagram of the x402 payment flow in this project.
Show all states, transitions, and which file handles each state."
```

This forces the agent to build a mental model before guessing at fixes.
Costs 30 seconds, saves 30 minutes of circular debugging.

---

## Rule 9: Queue Tasks, Don't Supervise

For long autonomous runs (Ralph mode):
1. Write all tasks into `prd.json` with `passes: false`
2. Start the loop: `./scripts/ralph/ralph.sh 10`
3. Come back to check — don't babysit

For interactive mode (standard Windsurf):
1. Tell Cascade: "Complete ONLY task 2.1, then stop and wait"
2. Review the output
3. Say "continue" when satisfied

**Never say "do all the tasks."** Context window degrades fast.

---

## Rule 10: Test Pyramid for SwigPay

Don't write unit tests for every function under time pressure.
Write tests that verify the things judges will check:

```typescript
// HIGH VALUE: Does the x402 payment flow end-to-end?
// HIGH VALUE: Does the Squads spending limit reject over-limit payments?
// HIGH VALUE: Does the SQLite log record the tx hash correctly?

// LOW VALUE (skip under time pressure):
// Unit test for individual helper functions
// UI snapshot tests
// Type-only tests (TypeScript catches these already)
```
~~~

---

## Cross-References

- **YouTube Transcript:** `tolu/memory-palace/youtube/transcripts/0xsero-agentic-coding-101.md`
- **Channel Videos Index:** `tolu/memory-palace/youtube/channels/0xsero-channel-videos.md`
- **SwigPay Repo:** https://github.com/ToXMon/swigpay-complete
- **Original Video:** https://youtu.be/VgR66ybAtdg
