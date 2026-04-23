# Code Factory — Auto-Write + Auto-Review Pipeline

Task prompt for systematic AI-assisted development with automated quality gates.
Based on Ryan Carson's Code Factory pattern.

---

## Overview

The Code Factory is a structured pipeline where a coding agent writes code,
opens a PR, and a series of automated gates classify risk, run checks,
and decide whether to auto-merge or escalate for human review.

```
Write Code → Open PR → Risk Gate → CI Fanout → Review Agent → Remediate → Merge
```

Every change goes through the same pipeline regardless of author.

---

## Step 1: Coding Agent Writes Code

The coding agent receives a task from `prd.json` with a clear specification.

**Rules for the coding agent:**
- Work on exactly one task at a time
- Create a feature branch: `task/<task-id>-<short-description>`
- Write the minimum code to satisfy the task spec
- Include tests that verify the stated acceptance criteria
- Commit with format: `feat(task-id): <what changed>`
- Push and open a PR against main
- The PR description must contain:
  - Task ID from `prd.json`
  - What changed and why
  - How to verify (test commands, manual steps)
  - Files changed (auto-populated by git)

**Do not merge.** The coding agent's job ends at PR creation.

---

## Step 2: Risk Policy Gate

The risk gate inspects the diff and classifies the PR into a risk tier.
Classification is deterministic based on file types and change patterns.

### Tier Classification Rules

| Tier | Criteria | Examples |
|------|----------|----------|
| **Critical** | Changes to auth, crypto, payment processing, security boundaries, or infra-as-code that controls production access | auth middleware, JWT handling, Stripe webhooks, Kubernetes RBAC, TLS config |
| **High** | Changes to data models, API contracts, database migrations, or core business logic | schema changes, API endpoint modifications, state machine logic, permission checks |
| **Medium** | Changes to application logic, new features, or refactors touching >5 files | new API routes, service layer refactors, feature flag logic, config changes |
| **Low** | Documentation, tests only, styling, dependency version bumps, or changes touching ≤3 non-critical files | README updates, test additions, CSS tweaks, package.json version bumps |

**Tier overrides:**
- If the diff touches any file matching `**/auth/**`, `**/security/**`, `**/crypto/**` → minimum High
- If the diff touches `**/middleware/**` or `**/guard/**` → minimum High
- If the diff adds new dependencies (`package.json`, `requirements.txt`, `go.mod`) → minimum Medium
- If the diff is exclusively `.md`, `.txt`, or `.json` fixture files → Low
- If the diff is only test files with no production code changes → Low

**Output:** Risk tier label attached to the PR.

---

## Step 3: CI Fanout

Based on the risk tier, CI runs the appropriate checks:

### All tiers run:
- Lint + format check
- Type check (if applicable)
- Unit tests
- Build verification

### Medium and above also run:
- Integration tests
- Dependency audit (known vulnerabilities)
- Bundle size check (frontend)

### High and Critical also run:
- Full E2E test suite
- Security scan (SAST)
- API contract validation
- Performance regression check

### Critical additionally runs:
- Full security audit (DAST)
- Infrastructure drift detection
- Manual gate: requires explicit human approval before merge

**If any check fails:** The PR is flagged, and the remediation agent (Step 5)
is activated.

---

## Step 4: Code Review Agent

An automated review agent examines the diff. This is not a rubber stamp.

**Review checklist (all items must pass):**

1. **Correctness**: Does the code do what the task spec says?
2. **Edge cases**: Are error paths handled? Null checks present?
3. **Security**: No hardcoded secrets, no SQL injection, proper input validation?
4. **Performance**: No N+1 queries, no unnecessary allocations in hot paths?
5. **Maintainability**: Functions under 30 lines? Clear naming? No dead code?
6. **Testing**: Tests cover the acceptance criteria? Tests are meaningful (not just asserting true)?
7. **Consistency**: Matches existing code style and patterns in the project?

**Review outcomes:**
- **Approve**: All checks pass. Proceed to merge decision.
- **Request Changes**: Specific issues listed. Route to remediation agent.
- **Escalate**: The agent cannot determine safety. Flag for human review.

**Optional:** The `/audit` command can be used as an additional review step,
triggering a deeper security-focused analysis on the changed files.

---

## Step 5: Remediation Agent

Activated when CI fails or the review agent requests changes.

**Process:**
1. Read the failure output or review feedback
2. Identify the root cause (not just the symptom)
3. Fix the issue on the same branch
4. Re-run only the failed checks (not the full CI fanout)
5. If the fix passes, re-submit to the review agent
6. Maximum 3 remediation cycles. After 3 failures, flag for human intervention

**Rules:**
- Do not refactor unrelated code during remediation
- Do not change the task scope
- Each remediation commit: `fix(task-id): <what was fixed>`
- If a fix requires architectural changes, stop and escalate

---

## Step 6: Merge Decision

After all checks pass and review approves:

| Risk Tier | Merge Policy |
|-----------|-------------|
| Low | Auto-merge immediately |
| Medium | Auto-merge after 5-minute cool-down (allows emergency revert) |
| High | Auto-merge after review agent approval + all CI green |
| Critical | **Never auto-merge.** Requires human approval in addition to all automated checks |

**Post-merge:**
1. Delete the feature branch
2. Update `prd.json` task status to `done`
3. Append completion to `progress.txt`
4. Run reflection if this was the last task in a session

---

## Pipeline Orchestration

The pipeline is orchestrated by a coordinator that reads the PR state and
drives each step:

```
START
  │
  ▼
Coding Agent ──► PR Created
                    │
                    ▼
              Risk Gate (classify tier)
                    │
                    ▼
              CI Fanout (run checks for tier)
                    │
              ┌─────┴─────┐
              │ Pass       │ Fail
              ▼            ▼
        Review Agent   Remediation Agent ──► (back to CI)
              │                │
        ┌─────┴─────┐    3 fails → ESCALATE
        │ Approve    │ Request Changes
        ▼            ▼
   Merge Decision   Remediation Agent
        │
        ▼
   POST-MERGE (update prd.json, progress.txt)
        │
        ▼
      DONE
```

**Failure modes:**
- CI timeout after 30 minutes → fail the PR, notify human
- Review agent escalation → block merge, notify human
- Remediation loop exceeded → block merge, notify human
- Merge conflict → rebase from main, re-run CI

---

## When to Use This Pipeline

**Use Code Factory when:**
- The task has a clear spec in `prd.json`
- Changes are testable with automated checks
- You want consistent quality enforcement
- Multiple tasks need to ship in a session

**Do NOT use Code Factory when:**
- The task is exploratory or requires human judgment at each step
- Changes are trivially small (single typo fix, version bump)
- You're in a rapid prototyping phase where speed matters more than gates
- The task will take under 30 minutes end-to-end

---

## Integration Points

- `prd.json` — Task definitions and status tracking
- `progress.txt` — Session history and completion log
- `AGENTS.md` — Project patterns the coding and review agents should follow
- `work_logs/` — CI reports, review outputs, and session artifacts
- `/reflect` skill — Run after completing a set of tasks through the factory
