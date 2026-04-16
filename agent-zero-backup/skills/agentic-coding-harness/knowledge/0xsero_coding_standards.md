# 0xSero + Ralph Coding Standards Reference

Compiled from 0xSero's agentic coding workflow and Ralph's PRD-driven autonomous loop.

## Modular Slice Architecture

Every feature is a self-contained slice with these layers centralized:

- **Config** — Environment variables, feature flags, constants in one place
- **Types** — All interfaces, types, and schemas defined explicitly
- **Database** — Schema, migrations, and queries co-located with the feature
- **API** — Route handlers validate input, call business logic, return typed responses
- **UI** — Components consume typed data, no prop drilling past one level

Each slice can be understood and tested in isolation. Cross-slice communication goes through typed interfaces, not direct imports of internals.

## File and Directory Size Limits

| Constraint | Limit | Reason |
|---|---|---|
| Max lines per file | 300 | Fits in a single LLM context window |
| Max files per directory | 20 | Keeps navigation fast and focused |
| Max function length | 50 lines | Forces decomposition |
| Max function params | 4 | Use options object/dict beyond that |

**Why 300 lines matters for AI agents:**
- Each iteration spawns fresh context
- Agents read files to understand current state
- Large files exceed context windows or crowd out instructions
- Small files = faster comprehension = fewer errors

## JSON DB Stub Pattern

For local development and testing:

```python
# data/stub_users.json
[
  {"id": 1, "name": "Alice", "email": "alice@example.com"},
  {"id": 2, "name": "Bob", "email": "bob@example.com"}
]
```

```typescript
// src/db/stub.ts
import data from "../../data/stub_users.json";

export async function getUsers(): Promise<User[]> {
  if (process.env.NODE_ENV === "test") {
    return data as User[];
  }
  return db.query("SELECT * FROM users");
}
```

Benefits:
- No database required for local dev
- Tests are deterministic
- Stubs live in `data/` directory, version-controlled
- Easy to swap for real DB in production

## Type Safety

**Rule: No `any` types. Ever.**

```typescript
// WRONG
function process(data: any) { ... }
const result = response as any;

// RIGHT
interface ProcessInput {
  id: string;
  payload: Record<string, unknown>;
}
function process(data: ProcessInput) { ... }
const result = response as ProcessOutput;
```

```python
# WRONG
def process(data: Any) -> Any:
    ...

# RIGHT
from typing import TypedDict

class ProcessInput(TypedDict):
    id: str
    payload: dict[str, Any]  # only top-level unknown

def process(data: ProcessInput) -> ProcessOutput:
    ...
```

When you need a generic type:
1. Define an explicit interface/type
2. Use `unknown` with type narrowing
3. Create a union type for known variants
4. Use generic type parameters `<T>` when the shape varies

## Test Patterns

### Integration Tests with JSON Output

```typescript
// tests/integration/api_users.test.ts
import { readFileSync, writeFileSync } from "fs";
import { User } from "../../src/types";

test("GET /users returns typed list", async () => {
  const response = await fetch("/api/users");
  const users: User[] = await response.json();

  // Write actual output for verification
  writeFileSync("data/test_output_users.json", JSON.stringify(users, null, 2));

  expect(users.length).toBeGreaterThan(0);
  expect(users[0]).toHaveProperty("id");
  expect(users[0]).toHaveProperty("email");
});
```

### Test Naming Convention

- `test_<feature>_<scenario>_<expected>.py`
- `<feature>.spec.ts` for unit tests
- `tests/integration/<feature>.test.ts` for integration

## Workpack Queuing Pattern

For 12-16 hour autonomous runs:

1. **Create PRD** — Define all user stories with acceptance criteria
2. **Generate workpack** — Convert PRD into task-XXXX.md files
3. **Queue tasks** — Each task is one context window of work
4. **Execute sequentially** — One task at a time, commit on green
5. **Track progress** — Append-only progress.txt with learnings
6. **Stop condition** — All tasks complete and quality gates pass

### Workpack Structure
```
.workpack/
├── scope.md       — Objective and constraints
├── rules.md       — Autonomous execution rules
├── progress.txt   — Append-only learnings log
├── task-0001.md   — First task
├── task-0002.md   — Second task
└── task-NNNN.md   — Nth task
```

## PRD-Driven Development (from Ralph)

### PRD Format
```json
{
  "project": "ProjectName",
  "branchName": "feature/description",
  "description": "One-line objective",
  "userStories": [
    {
      "id": "US-001",
      "title": "Short title",
      "description": "As a <role>, I need <capability> so <outcome>.",
      "acceptanceCriteria": ["Measurable criterion 1", "Measurable criterion 2"],
      "priority": 1,
      "passes": false,
      "notes": "Implementation hints"
    }
  ]
}
```

### Ralph Loop
1. Read `prd.json` — Get all user stories
2. Read `progress.txt` — Get accumulated learnings
3. Read `AGENTS.md` files — Get codebase patterns
4. Pick highest priority story where `passes: false`
5. Implement that single story
6. Run quality checks (typecheck, tests)
7. If green: commit with `feat: [Story ID] - [Title]`
8. Update `prd.json` — Set `passes: true` for completed story
9. Append learnings to `progress.txt`
10. Update `AGENTS.md` with discovered patterns
11. Repeat until all stories pass

### Key Ralph Principles
- **Fresh context each iteration** — No state carried between runs except files
- **One story per iteration** — Small, focused changes
- **Quality gates are mandatory** — Never commit broken code
- **Progress is append-only** — Never delete, only append
- **AGENTS.md is the knowledge store** — Agents read it automatically

## Cadence

- **2 days for new features** — Plan on Monday/Tuesday, build Wednesday/Thursday
- **3 days for refactors** — Longer because tests must remain green throughout
- **1 day for bug fixes** — Write a failing test first, then fix

## State Machine Diagram Practice

Before implementing complex data flows:

1. **Draw the states** — What are all possible states of the data?
2. **Draw the transitions** — What triggers each state change?
3. **Draw the guards** — What conditions must be true for a transition?
4. **Draw the side effects** — What happens on each transition?

Save diagrams to `work_logs/state_machines/<module>-states.md`

## Voice Prompting and Context Curation

- Use voice for high-level goals, not implementation details
- Curate context by reading AGENTS.md before each session
- Keep a running list of decisions in the session log
- Extract reusable templates after each session

## Session Logging Standards

Every session gets logged to `work_logs/session_YYYY-MM-DD.json`:

```json
{
  "timestamp": "2025-01-15T14:30:00",
  "project": "project-name",
  "summary": "One-two sentence summary",
  "decisions": ["Decision 1", "Decision 2"],
  "blockers": ["Blocker description"],
  "next_steps": ["Next priority 1", "Next priority 2"],
  "files_changed": ["path/to/file.py"],
  "tests_status": "passing|failing|unknown"
}
```

## AGENTS.md Conventions

Every module with source files gets an `AGENTS.md`:

```markdown
# AGENTS.md — module-name/

## Overview
[Brief description of what this module does]

## Source Files
- `file1.py` — [purpose]
- `file2.ts` — [purpose]

## Key Exports
- `functionName()` — [what it does]
- `TypeName` — [what it represents]

## Patterns & Conventions
<!-- Agents fill this in during development -->
- When modifying X, also update Y
- This module uses Z pattern for all API calls

## Dependencies
<!-- Cross-module dependencies -->
- Depends on `src/types/` for shared interfaces
- `src/db/` calls into this module for X
```

**Rules:**
- Never auto-delete content from AGENTS.md
- Patterns section is hand-curated, not auto-generated
- Update after every meaningful change
- Root AGENTS.md links to all submodule AGENTS.md files
