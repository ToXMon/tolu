# Agentic Coding Standards — Practitioner Reference

Combines the approaches of two practitioners with proven track records building
production systems with AI coding agents.

---

## Practitioners

| | 0xSero | Ryan Carson |
|---|---|---|
| Background | Security engineer, AI-assisted coding practitioner | 5x founder, 20 years experience |
| GitHub | 0xSero | snarktank |
| Twitter | @0xSero | @ryancarson |
| Key Work | "10 Hard-Won Rules" for AI coding | ai-dev-tasks repo (5K+ GitHub stars) |
| Focus | Pitfall avoidance, context discipline | Workflow structure, quality gates |

---

## Part 1: 0xSero's 10 Hard-Won Rules

### Rule 1: Define "Done" Before You Start

Every task needs acceptance criteria written before code. If you can't state
what "done" looks like, the AI will wander.

```markdown
# Bad
Fix the login bug

# Good
## Task: Fix login redirect loop
## Done when:
- User logs in with valid credentials → redirected to /dashboard
- User logs in with invalid credentials → stays on /login with error message
- Session cookie set with httpOnly, secure, sameSite=strict
- Test: `test_login_redirect` passes
```

### Rule 2: Provide Context, Not Just Instructions

AI agents don't know your codebase. Every prompt needs:
- What files are relevant
- What the current architecture looks like
- What constraints exist

```markdown
# Bad
Add rate limiting to the API

# Good
## Context
- API is Express.js in /src/routes/
- Already uses express-rate-limit for /auth routes (see auth.ts)
- Redis client available at req.app.locals.redis
- Need to rate-limit /api/data endpoints, not /api/health

## Task
Add rate limiting to /api/data/* endpoints: 100 req/min per API key.
Use the existing express-rate-limit setup. Store counters in Redis.
```

### Rule 3: One Task Per Prompt

Compound tasks cause compound failures. Split everything.

```markdown
# Bad (3 tasks in one)
Add user registration, email verification, and password reset.

# Good (3 separate prompts)
Prompt 1: Add user registration endpoint
Prompt 2: Add email verification flow (depends on #1)
Prompt 3: Add password reset flow (depends on #1)
```

### Rule 4: Verify Before You Proceed

Never assume the AI got it right. Verify after every task:
- Run tests
- Check the actual code, not just the AI's description
- Validate against acceptance criteria

```bash
# After every task
npm test                    # run the test suite
git diff --stat            # see what actually changed
git diff src/auth.ts       # read the actual diff
```

### Rule 5: Keep Git History Clean

Every commit should be a single logical change. This makes rollback possible.

```bash
# Bad: one massive commit
git add -A && git commit -m "added auth"

# Good: atomic commits
git add src/auth/middleware.ts && git commit -m "feat: add JWT validation middleware"
git add src/auth/routes.ts && git commit -m "feat: add login/logout endpoints"
git add tests/auth.test.ts && git commit -m "test: add auth middleware and route tests"
```

### Rule 6: Lock Dependencies

Never let the AI pick versions. Pin everything.

```json
// Bad
"dependencies": { "express": "latest" }

// Good
"dependencies": { "express": "4.18.2" }
```

Use lock files. Commit them.

### Rule 7: Don't Let the AI Refactor Without Asking

Refactoring is the #1 source of silent breakage. The AI will "improve" code
that was working fine.

```markdown
## Rule for the AI agent:
Do NOT refactor, reorganize, or improve code unless the task explicitly
asks for it. If you see something that could be improved, note it in a
comment but do not change it.
```

### Rule 8: Use AGENTS.md for Project Memory

Create an `AGENTS.md` at the project root. The AI reads this every session.
It is your persistent cross-session memory.

```markdown
# AGENTS.md — Project Memory

## Architecture
- Express.js API, TypeScript, PostgreSQL
- Auth: JWT in httpOnly cookies, refresh tokens in Redis
- File structure: src/routes/ → src/services/ → src/repositories/

## Conventions
- Use Zod for input validation on all routes
- Error responses: { error: string, code: string }

## Discovered Patterns
- [2025-04-10] PostgreSQL array_agg is 3x faster than JS-side grouping
- [2025-04-12] BullMQ job priority must be set or jobs process out of order
```

### Rule 9: Test the Edge Cases the AI Won't

AI writes happy-path tests. You need boundary conditions:
- Null inputs, empty arrays, unicode strings
- Concurrent requests, network failures
- Authorization boundary cases

```typescript
// AI writes this
test('login works', async () => {
  const res = await request(app).post('/login').send({ user: 'admin', pass: 'admin' });
  expect(res.status).toBe(200);
});

// You also need this
test('login rejects SQL injection in username', async () => {
  const res = await request(app).post('/login')
    .send({ user: "admin'; DROP TABLE users;--", pass: 'anything' });
  expect(res.status).toBe(401);
});

// And this
test('login handles database connection failure', async () => {
  jest.spyOn(db, 'query').mockRejectedValue(new Error('ECONNREFUSED'));
  const res = await request(app).post('/login').send({ user: 'admin', pass: 'admin' });
  expect(res.status).toBe(503);
});
```

### Rule 10: Know When to Stop Using AI

Some tasks are faster by hand:
- One-line config changes
- Debugging that requires reading runtime state
- Changes where the cost of verification exceeds the cost of writing
- Security-critical code that needs human threat modeling first

---

## Part 2: Ryan Carson's 3-Step Workflow

A structured workflow for AI-assisted development: PRD → Tasks → Build.
Designed for projects that take 1-4 weeks, not 30-minute tasks or multi-month
epics.

### Step 1: Create the PRD

**Method:** Voice brain-dump into a PRD template. Always use MAX mode with
the biggest model available.

The PRD captures:
- What you're building and why
- User stories and acceptance criteria
- Technical constraints and dependencies
- Out of scope (explicit)

**PRD structure:**

```markdown
# Product Requirements Document
## Project: [Name]
## Overview
[2-3 sentences on what this is]

## Goals
1. [Primary goal]
2. [Secondary goal]

## User Stories
- As a [user type], I want [action] so that [outcome]

## Technical Requirements
- [Stack, integrations, constraints]

## Out of Scope
- [Explicitly list what you're NOT building]
```

### Step 2: Generate Task List

Break the PRD into atomic sub-tasks. Each task must be:
- Completable in a single AI session
- Independently testable
- Small enough to verify quickly

Store tasks in `prd.json`:

```json
{
  "project": "auth-service",
  "tasks": [
    {
      "id": "T001",
      "name": "Set up project structure",
      "status": "not_started",
      "depends_on": [],
      "acceptance": [
        "package.json exists with scripts for dev, test, build",
        "TypeScript configured and compiles",
        "ESLint + Prettier configured"
      ]
    },
    {
      "id": "T002",
      "name": "Add JWT authentication middleware",
      "status": "not_started",
      "depends_on": ["T001"],
      "acceptance": [
        "Middleware validates JWT from Authorization header",
        "Returns 401 for missing/invalid tokens",
        "Attaches decoded user to request object"
      ]
    }
  ]
}
```

### Step 3: Execute Tasks One at a Time

**Critical rules:**
- Fresh chat per task — carry forward only what's needed from AGENTS.md
- Clean git status before starting — commit or stash everything
- Complete one task fully before moving to the next
- Run `/reflect` after completing a set of tasks

**Philosophy:** "Slowing down to provide proper context is the secret to
speeding up."

---

## Part 3: Ryan Carson's Reflection Prompt

Forces the model to distill learnings before closing a session. See the
full skill definition at `skills/skill.reflection.md`.

**Core technique:** At session end, present the model with all context
(progress.txt, session logs, AGENTS.md patterns, prd.json status) and
require it to answer six structured sections:

1. **Summary** — What was accomplished, concretely
2. **Surprises** — Unexpected discoveries worth recording
3. **Blockers** — What's stuck and why
4. **Discovered Patterns** — Reusable insights for AGENTS.md
5. **PRD Task Updates** — Status changes with evidence
6. **Next Steps** — Prioritized list for the next session

The reflection output feeds three artifacts:
- `progress.txt` — appended with summary and surprises
- `AGENTS.md` — new patterns added to the Discovered Patterns section
- `work_logs/handoff_*.json` — machine-readable state for the next session

---

## Part 4: Ryan Carson's Code Factory

An auto-write + auto-review pipeline for systematic AI-assisted development.
See the full task definition at `tasks/code_factory.md`.

**Pipeline stages:**

```
Write Code → Open PR → Risk Gate → CI Fanout → Review Agent → Remediate → Merge
```

**Key innovation:** Risk-tiered review. Every PR is classified as
Critical / High / Medium / Low based on file types changed. The tier
determines how much automated scrutiny the PR receives before merge.

| Tier | CI Depth | Merge Policy |
|------|----------|-------------|
| Critical | Full DAST + human review | Never auto-merge |
| High | E2E + SAST + contract tests | Auto-merge after review approval |
| Medium | Integration + dep audit | Auto-merge with 5-min cooldown |
| Low | Lint + unit tests + build | Auto-merge immediately |

---

## Part 5: Cross-Session Memory Patterns

### AGENTS.md

The single source of truth for project conventions, architecture decisions,
and discovered patterns. Read at the start of every session, updated at the
end via reflection.

```markdown
# AGENTS.md

## Architecture
[Describe the system: stack, patterns, key decisions]

## Conventions
[Coding standards, naming, file organization]

## Known Issues
[Active bugs, tech debt, deferred decisions]

## Discovered Patterns
- [YYYY-MM-DD] [Pattern description and rationale]
```

### progress.txt

Running log of session activity. Append-only — never overwrite.

```markdown
## Session 2025-04-10 14:30
Summary: Added rate limiting to /api/data endpoints
Surprises: Redis MULTI/EXEC needed for atomic counter increment

## Session 2025-04-11 09:00
Summary: Fixed rate limit bypass via X-Forwarded-For header injection
Surprises: express-rate-limit trusts all headers by default behind proxies
```

### prd.json

Task tracking with acceptance criteria. Status values:
`not_started`, `in_progress`, `done`, `blocked`.

### work_logs/

Session artifacts:
- `session_*.json` — structured session metadata
- `reflection_*.md` — human-readable session handoff
- `handoff_*.json` — machine-readable session state

---

## Part 6: Head-to-Head Comparison

### Where They Agree

| Principle | 0xSero | Ryan Carson |
|-----------|--------|-------------|
| One task at a time | Rule 3: One Task Per Prompt | Step 3: Execute one task per session |
| Define done upfront | Rule 1: Define "Done" | Step 2: Acceptance criteria in prd.json |
| Verify everything | Rule 4: Verify Before Proceed | Code Factory: CI + Review Agent |
| Clean git state | Rule 5: Clean History | Step 3: Clean git status before starting |
| Context is king | Rule 2: Provide Context | Step 1: PRD brain-dump, AGENTS.md |

### Where They Differ

| Dimension | 0xSero | Ryan Carson |
|-----------|--------|-------------|
| Session scope | Task-level, quick iterations | Full workflow from PRD to deployment |
| Memory model | AGENTS.md (single file) | AGENTS.md + progress.txt + prd.json (multi-file) |
| Review model | Human verifies after each task | Automated Code Factory pipeline with risk tiers |
| Planning depth | Just-in-time, per-task | Upfront PRD with task decomposition |
| Reflection | Not formalized | Structured 6-section reflection prompt |
| Best for | Day-to-day coding, bug fixes, small features | Multi-day projects with clear scope |

### When to Use Which

**Use 0xSero's rules when:**
- Working on an existing codebase you know well
- Making targeted fixes or small additions
- Speed matters more than process
- You're pairing directly with the AI in real-time

**Use Ryan Carson's workflow when:**
- Starting a new project or major feature
- The work spans multiple sessions
- You need handoff between sessions or team members
- Quality gates and audit trails matter

**Use both together when:**
- You're building a new feature in an existing codebase
- Start with Carson's PRD + task breakdown
- Apply 0xSero's rules within each task execution
- Use Carson's reflection to close each session
- Let 0xSero's "know when to stop" rule prevent over-engineering

---

## Quick Reference Card

```
0xSero's Checklist (per task):
□ Done criteria defined?
□ Context provided (files, architecture, constraints)?
□ Single task, not compound?
□ Verified (tests pass, diff reviewed)?
□ Clean commit?
□ Edge cases tested?
□ No unauthorized refactors?

Carson's Checklist (per session):
□ PRD up to date?
□ Tasks broken down atomically?
□ Fresh chat, clean git?
□ One task completed fully?
□ Reflection done (summary, surprises, blockers, patterns, next)?
□ progress.txt updated?
□ AGENTS.md patterns updated?
□ prd.json statuses updated?
```
