---
name: no-mistakes
description: Validate code changes through the no-mistakes gate pipeline before pushing to origin. Use when the user asks to gate, validate, push safely, clean PR, run no-mistakes, /no-mistakes, ship safely, or review before push.
---

# no-mistakes

`no-mistakes` is a local git proxy that validates code changes through a pipeline
(intent, rebase, review, test, document, lint, push, PR, CI) before they reach
upstream. You drive it through the `no-mistakes axi` command family, which prints
machine-readable TOON output to stdout and progress to stderr.

When the user invokes `/no-mistakes` or asks to validate/ship their changes,
run the pipeline and report the outcome.

## Tools Used

- **`code_execution_tool`** — Run all `no-mistakes axi` commands via `runtime: "terminal"`
- **`response`** — Report outcomes and escalate `ask-user` findings to the user
- **`text_editor`** — Read log files or step output when needed

## Before You Start

Check these prerequisites before running the pipeline:

1. **Work is committed** — The gate validates committed history, not uncommitted working tree.
   If uncommitted changes exist, commit or stash them first.
2. **Feature branch** — Must not be on the repository's default branch.
   Create a branch if needed: `git checkout -b <branch-name>`
3. **Repo initialized** — The repository must have `no-mistakes init` already run.
   If not, run `no-mistakes init` first.

If `axi run` returns an `error:`, read the message and act on it (commit work,
create a branch, or run the suggested fix command).

## Intent Is Required

When starting a run, pass `--intent`: **what the user set out to accomplish** — the
goal behind this work in their terms. This is not a description of the diff; it is
the objective the change is meant to achieve.

Err on the side of completeness. The review step uses `--intent` to distinguish
deliberate decisions from mistakes. A thin one-line summary makes it flag things
the user already chose. Capture:
- The user's goal
- Specific decisions and tradeoffs made
- Constraints or approaches ruled in or out
- Anything they explicitly asked for that might look surprising in the diff

A few sentences to a short paragraph is normal.

## Validate and Decide

Run the pipeline and decide on findings as they come up:

### 1. Start the Run

```sh
no-mistakes axi run --intent "<what the user set out to accomplish>"
```

Run via `code_execution_tool` with `runtime: "terminal"`. The command blocks until
the first decision point or the end.

Additional flags you can pass:
- `--skip=lint` — Skip a specific step
- `--yes` — Auto-approve all gates (only when user has given standing consent)

### 2. Handle Gate Findings

If the output contains a `gate:` object, the pipeline is waiting. Read its
`findings` table. Each finding has:

| Field | Meaning |
|-------|---------|
| `id` | Finding identifier for respond command |
| `severity` | critical, high, medium, low, info |
| `file` | File path involved |
| `description` | What was found |
| `action` | How the pipeline classified it |

**Action types:**

| Action | Meaning | Your Response |
|--------|---------|-------------|
| `auto-fix` | Mechanical, low-risk fix | Fix it yourself via `code_execution_tool` |
| `no-op` | Informational only | Approve and continue |
| `ask-user` | Needs user decision | **Stop and escalate** (see below) |

### 3. Respond to Gates

Choose one response per gate:

```sh
# Accept the step as-is and continue
no-mistakes axi respond --action approve

# Fix specific findings, then continue
no-mistakes axi respond --action fix --findings <id1,id2> --instructions "<guidance>"

# Skip this step entirely
no-mistakes axi respond --action skip
```

Each `respond` blocks until the next `gate:`, `checks-passed`, or final outcome.

### 4. Repeat Until Outcome

Keep handling gates until the output has an `outcome:` instead of `gate:`.

| Outcome | Meaning | Your Action |
|---------|---------|-------------|
| `checks-passed` | CI green, PR not merged yet | Tell user PR is ready (link in `help` line). Do NOT poll for merge. |
| `passed` | Gate cleared, PR merged/closed | Report success |
| `failed` | Did not pass | Read output, address issues |
| `cancelled` | Run was cancelled | Read output, decide next steps |

The CI step watches the PR until merged or closed. `axi run` returns `checks-passed`
the moment checks are green. **Never poll or re-run waiting for the merge.**

## Escalate ask-user Findings

A gate with only `auto-fix` or `no-op` findings: handle on your own judgment.

A finding marked `ask-user` is a decision that belongs to the user — it challenges
their deliberate intent or changes product behavior. **Do not approve, fix, or skip
it without user input.**

Instead:

1. **Stop the pipeline loop.**
2. **Relay each `ask-user` finding** to the user via `response`:
   - Include `id`, `file`, and full `description` verbatim
   - Do not paraphrase, summarize, or pre-judge
3. **Ask how they want to proceed** — fix (with guidance), approve, or skip
4. **Translate their decision** into the matching `respond` call

Exception: `--yes` mode means the user gave standing consent. Under `--yes`,
resolve `ask-user` findings automatically.

## Inspecting State

Use these commands via `code_execution_tool` when you need to inspect or recover:

```sh
no-mistakes axi               # Home view: active run, recent runs, next steps
no-mistakes axi status        # Full detail of active/most recent run
no-mistakes axi logs --step <name> --full   # Full log of one step
no-mistakes axi abort         # Cancel the active run
```

## Reading the Output

- Output is TOON format: `key: value` pairs, `name[N]{cols}:` tables, `help[N]:` hints
- The `help` list at the bottom of most responses tells you the next commands
- Errors appear as `error: ...` on stdout with a `help` list — act on the suggestion
- Exit codes: `0` success/no-op/normal gates, `1` failed/cancelled outcome, `2` bad usage

## Decision Flow Summary

```
axi run --intent "..."
  │
  ├── gate: → read findings
  │   ├── all auto-fix/no-op → respond approve or fix
  │   └── has ask-user → STOP, escalate to user, then respond
  │
  ├── gate: → repeat...
  │
  └── outcome:
      ├── checks-passed → tell user PR ready, DONE
      ├── passed → report success, DONE
      ├── failed → read output, address, DONE
      └── cancelled → read output, DONE
```
