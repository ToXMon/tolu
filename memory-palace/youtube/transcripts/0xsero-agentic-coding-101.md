# 0xSero - Agentic Coding 101: How I Work on 8 Projects at a Time

**Video**: https://www.youtube.com/watch?v=VgR66ybAtdg
**Channel**: 0xSero (@0xSero) - ~4.6K subscribers, 141 videos
**Description**: "This is how I use claude code and codex to code on 8x projects at a time"
**Source**: Extracted from GitHub notes at ToXMon/swigpay-complete + web research

---

## The Core Mental Model

> "You can just trust that your LSP will provide the model the context it needs. You just look at the results at the end."

Stop re-explaining the codebase to the agent every session. Instead, encode it ONCE into the repo structure and let tooling enforce it.

---

## Rule 1: File and Directory Size Limits (Enforce via LSP/tsconfig)

**Max 300 lines per file. Max 20 files per directory.**

These are ERRORS, not warnings. When Cascade violates them, the LSP flags it automatically and the agent self-corrects without you asking.

```
// .eslintrc equivalent -- add to project
// "max-lines": ["error", 300]
// "max-depth": ["error", 4]
```

Why it matters: AI agents will try to put all logic in one 500-line file. Force splits: `feature-create.ts`, `feature-limits.ts`, `feature-execute.ts`.

---

## Rule 2: No `any` Types -- Use `unknown` + Zod

```typescript
// Agent default (lazy)
const result: any = await client.callTool(name, args);

// 0xSero pattern (strict)
const result: unknown = await client.callTool(name, args);
const parsed = PaymentResultSchema.parse(result); // Zod validates shape
```

`any` types cause drift across sessions -- the agent starts making inconsistent assumptions. `unknown` + Zod forces explicit contracts that survive context window boundaries.

---

## Rule 3: Centralized Config -- Single Source of Truth

**Everything imports from ONE config file. Nothing is duplicated.**

```typescript
// src/config.ts -- the ONLY place constants live
export const CONFIG = {
  network: process.env.NETWORK ?? "devnet",
  rpcUrl: process.env.RPC_URL ?? "https://api.devnet.example.com",
  // ... all constants here
} as const;

// NEVER do this in a tool or agent file:
const USDC = "4zMMC9..."; // duplicate!
```

When the agent edits config, it edits ONE file. Prevents the "magic string scattered across 12 files" problem.

---

## Rule 4: Database Interface Pattern -- Swap Environments

Define a typed interface, implement it twice, switch via env var.

```typescript
interface IPaymentDB {
  insertPayment(record: Omit<PaymentRecord, "id">): number;
  getPaymentsByAgent(agentId: string, limit?: number): PaymentRecord[];
  updatePaymentStatus(id: number, status: PaymentStatus, txHash?: string): void;
  getSpentToday(agentId: string): number;
}
// Implement with SQLite for dev, Supabase for prod
// Switch: DATABASE=sqlite (default) or DATABASE=supabase
```

---

## Rule 5: AGENTS.md Files at Every Module Level

Each subdirectory gets its own `AGENTS.md`. Windsurf auto-loads it when Cascade enters that directory (glob-scoped).

Example AGENTS.md per module:
- Document which files do what
- Specify correct imports and function names
- Note gotchas ("Use multisigCreateV2, NOT multisigCreate")
- State decimals and unit conventions
- Max file sizes per module

---

## Rule 6: progress.txt -- Cross-Session Learning Log

Create at project root. Agent appends to it after every work session. Future sessions READ it first -- compound learning without context bloat.

```markdown
# Progress Log
## Codebase Patterns (agent reads this section first)
[Filled in as development progresses]
## Session Log
---
```

---

## Rule 7: 2/3 Cadence -- Feature vs. Refactor

**2 days features, 3 days refactoring, repeat.**

For a hackathon in 8 hours:
- Hours 1-5: Build features
- Hours 6-7: Refactor (deduplicate, split large files, fix any types)
- Hour 8: Demo prep

Without the refactor hour: AI agent code accumulates drift. Demo fails because config is duplicated in 3 places.

---

## Rule 8: State Machine Diagram Before Debugging

When stuck on a complex flow, ask the agent:

```
"Create an ASCII state machine diagram of the payment flow in this project.
Show all states, transitions, and which file handles each state."
```

Forces the agent to build a mental model before guessing at fixes. Costs 30 seconds, saves 30 minutes of circular debugging.

---

## Rule 9: Queue Tasks, Don't Supervise

For long autonomous runs ("Ralph mode"):
1. Write all tasks into `prd.json` with `passes: false`
2. Start the loop: `./scripts/ralph/ralph.sh 10`
3. Come back to check -- don't babysit

For interactive mode:
1. Tell agent: "Complete ONLY task 2.1, then stop and wait"
2. Review the output
3. Say "continue" when satisfied

**Never say "do all the tasks."** Context window degrades fast.

---

## Rule 10: Test Pyramid Under Time Pressure

Don't write unit tests for every function. Write tests that verify the things that matter:

- HIGH VALUE: End-to-end payment flow
- HIGH VALUE: Spending limit rejects over-limit
- HIGH VALUE: Database logs tx hash correctly
- LOW VALUE (skip): Individual helper function unit tests, UI snapshots, type-only tests

---

## Tools Mentioned

- **Claude Code** -- primary coding agent
- **OpenAI Codex** -- secondary coding agent
- **Windsurf / Cascade** -- IDE with agent integration
- **Ralph mode** -- autonomous loop for Windsurf
- **AGENTS.md** -- context files per module (Windsurf feature)
- **progress.txt** -- cross-session learning log
- **prd.json** -- task queue with pass/fail status
- **ESLint** -- enforce file size limits
- **Zod** -- runtime type validation
- **vLLM Studio** -- 0xSero's own tool for managing local AI models

## Key Workflow: Managing 8 Projects

1. Encode project context into AGENTS.md files per module
2. Use centralized config (single source of truth)
3. Let LSP/tooling enforce rules (not manual supervision)
4. Queue tasks into prd.json, run autonomous loops
5. 2/3 cadence: 2 days features, 3 days refactoring
6. progress.txt for cross-session memory
7. State machine diagrams before debugging
8. Task-by-task execution, never batch everything

## Smart Contract Security / Auditing Notes

- Use strict types (`unknown` + Zod, never `any`)
- Centralize config to prevent magic strings
- File size limits prevent monolithic contract files
- Interface patterns allow environment swapping (dev/prod)
- Cross-session learning log catches recurring vulnerabilities

---

*Note: Full video transcript could not be extracted due to YouTube blocking access from cloud IPs. This document is compiled from detailed notes taken by someone who watched the full video, plus web research on 0xSero's content.*
