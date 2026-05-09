---
name: token-efficiency-mode
description: >
  Reduces Agent Zero token usage through terse output, lean context reads,
  compressed tool results, and session context discipline. Use for token
  efficiency mode, reduce token usage, less tokens, lean context, caveman mode,
  compress context, or make this session cheaper.
version: 1.0.0
tags:
  - token-efficiency
  - context-engineering
  - agent-zero
  - compression
  - prompting
trigger_patterns:
  - token efficiency mode
  - reduce token usage
  - less tokens
  - lean context
  - caveman mode
  - compress context
  - make this session cheaper
---

# Token Efficiency Mode

## Purpose

Cut Agent Zero token use while preserving correctness, evidence, and the JSON tool-call contract.

Use this skill to reduce both token sources:

| Side | Target | Method |
|---|---|---|
| Output | Final replies, tool summaries, subordinate prompts | Short labels, bullets, tables, no filler |
| Input/context | Files, logs, research sources, session state | Narrow reads, grep-first discovery, compressed summaries, handoff notes |

Attribution: inspired by JuliusBrussee/caveman for terse-but-accurate agent output, mode persistence, filler removal, memory-file compression checks, and token-sparing subagents; inspired by yvgude/lean-ctx for mode-aware file reads, shell-output compression, cache/handle context reuse, context packs, session recovery, budgets, and token-savings measurement. This is an independent Agent Zero adaptation; no source code is copied.

## Activation Modes

| Mode | Use when | Style | Target reduction |
|---|---|---|---|
| `lite` | User wants cheaper but polished output | Concise professional prose; grammar preserved | 20-35% |
| `full` | User asks for `caveman mode` or maximum terseness with normal safety | Terse technical fragments; filler removed | 35-55% |
| `ultra` | User asks for maximum compression or context is very large | Tables, symbols, abbreviations when safe | 50-70% |
| `off` | User asks for normal detail or a high-risk section needs expansion | Normal Agent Zero style | 0% |

Default to `lite` for vague token-saving requests. Switch modes only when requested or when context pressure requires it. Temporary expansion is allowed for correctness-critical details, then return to the selected mode.

## Output Compression Rules

Preserve Agent Zero's required JSON response shape for tool calls. Never tell the agent to output non-JSON tool calls. Compress the text inside `thoughts`, `headline`, final `response` text, subordinate prompts, and user-facing tool-result summaries only when safe.

Do:

- Put the answer first.
- Prefer tables for dense technical output.
- Prefer bullets over paragraphs for operational status.
- Use short labels: `Done:`, `Issue:`, `Fix:`, `Test:`, `Risk:`, `Need:`, `Next:`.
- Keep uncertainty visible with short markers: `Unknown:`, `Need:`, `Risk:`.
- Remove greetings, restatements, filler, generic praise, and repeated caveats.
- Use exact names for commands, files, functions, tests, tools, commits, issues, and URLs.
- Keep user-requested explanations complete, but structure them tightly.

Never compress away:

- Commands.
- File paths.
- Error messages.
- Security findings.
- Test failures.
- User-visible decisions.
- Destructive-action warnings.
- Legal, financial, medical, or safety-critical caveats.
- Evidence required to prove success or failure.

Fail safe: if compressed wording could create technical ambiguity, expand that section.

## Context/Input Compression Rules

Before adding context, choose the smallest slice that can answer or advance the task.

Context selection ladder:

1. Existing conversation facts.
2. Known file paths and directory map.
3. `find`, `grep`, `rg`, `git grep`, or manifest inspection.
4. Narrow line ranges.
5. Larger file sections.
6. Full file only when structure, syntax, or patch safety needs it.

When delegating:

- Delegate normally when specialist work improves quality: implementation → `developer`; tests → `test-engineer`; review → `code-reviewer`; security → `security-auditor`/`hacker`; research → `researcher`; skill work → `skill-creator`.
- Answer directly for simple definitions, small rewrites, one-step guidance, and facts already in context.
- Keep subordinate prompts short: role, goal, constraints, inputs, expected output.
- Send paths and exact ranges instead of pasting long files when the worker can read them.
- Ask subordinates for file:line receipts and short findings unless full evidence is required.
- Use `§§include(abs_path)` for long existing content where supported.

## Tool Result Handling

After each tool result, extract signal and avoid raw replay.

| Result type | Compress to | Preserve raw detail when |
|---|---|---|
| Successful shell command | command, exit status, changed paths, key signal, next action | Output proves success or contains required artifact text |
| Failed shell command | command, exit status, exact causal error, impact, next action | Debugging needs stack trace head/tail or first causal error |
| Test run | command, pass/fail count, failing test names, exact failure lines | User asks for full log or failure is ambiguous |
| Search/read | source path/URL, matching lines, decision impact | The source text is contractual or safety-critical |
| Subordinate output | conclusion, evidence paths, decisions, open risks | Reviewer/security findings need severity and exact rationale |

Shell summary template:

```text
Cmd: <exact command>
Exit: <0|nonzero>
Signal: <key result>
Errors: <exact key error or none>
Next: <next action>
```

Do not summarize tool schemas, JSON keys, commands, patches, or code in ways that change semantics.

## File Reading Discipline

Use mode-aware reads.

| Need | Read mode |
|---|---|
| Locate relevant code | `find`/`grep`/`rg`, manifests, filenames |
| Understand interfaces | signatures, imports, headings, symbol blocks |
| Patch code | local range around target plus imports/callers/tests |
| Debug failure | failing command, first causal error, stack head/tail, related file ranges |
| Review/security | diff first, touched files, call sites, config boundaries |
| Research | README/headings first, relevant docs, cited lines only |

Rules:

- Know why a file is needed before reading it.
- Read narrow ranges first.
- Read surrounding context before patching.
- Avoid rereading unchanged content.
- Read full files only when exact structure matters.
- For generated/noisy files, inspect metadata or targeted snippets first.
- For shell logs, keep first error, final status, affected paths, and next action.

## Session Memory and Handoff Rules

Keep long sessions recoverable without dumping history.

Maintain compact state for multi-turn tasks:

```markdown
## Handoff
- Goal:
- Mode: lite|full|ultra|off
- Status:
- Changed:
- Verified:
- Errors:
- Decisions:
- Next:
```

Save durable discoveries to the memory palace only when they matter beyond the current chat:

- Path: `/a0/usr/workdir/tolu/memory-palace/wings/{wing}/rooms/`.
- Use the best wing: `technical`, `projects`, `learning`, `domain`, `people`, or `personal`.
- Include date when facts can change.
- End-date or mark outdated facts when replacing prior knowledge.
- Run backup before ending major sessions.

For large tasks, write or update handoff notes before context gets large, before tool-heavy phase changes, and before final response.

## Mode Controls

User commands:

| Command | Effect |
|---|---|
| `token efficiency mode` | Enable `lite` unless another mode is named |
| `lite mode` | Concise professional output |
| `full caveman mode` | Terse technical fragments |
| `ultra mode` | Maximum safe compression |
| `normal detail`, `full detail`, `turn off token efficiency` | Switch `off` |
| `expand this section` | Temporarily expand one section, then return |
| `show raw output` | Preserve requested raw output exactly |

Mode markers in final replies may be omitted unless useful. If included, keep short: `Mode: lite`.

## Examples

### Coding task

User: `Token efficiency mode. Fix the failing login test.`

Good behavior:

```text
Mode: lite
Plan: inspect failing test → read login code range → patch minimal fix → run focused test.
Done: patched /repo/src/auth/login.ts.
Test: npm test -- login.test.ts passed, 12/12.
Next: optional full suite.
```

Avoid: long architecture recap, repeated logs, unrelated file reads.

### Research task

User: `Lean context. Compare these two repos for ideas we can adapt.`

Good behavior:

```text
Mode: lite
Sources read: README.md, docs/architecture.md, examples/*.md.
Adaptable ideas:
| Repo | Idea | Agent Zero fit |
|---|---|---|
| A | mode switch | final response style |
| B | context packs | handoff notes |
Need: deeper code read only if implementing hooks.
```

Avoid: pasting full READMEs or opening every file.

### Debugging task

User: `Caveman mode. Why is the build failing?`

Good behavior:

```text
Mode: full
Cmd: npm run build
Exit: 2
Error: src/api.ts:42:13 - TS2339: Property 'token' does not exist on type 'Session'.
Cause: code expects Session.token; type exposes Session.accessToken.
Fix: update caller or type mapping.
Need: read /repo/src/api.ts:34-48 and session type definition.
```

Avoid: dropping the exact TypeScript error or file path.

### Failure case: do not hide important error detail

Bad compressed output:

```text
Build failed. Type issue. Fix session.
```

Why bad: it hides file path, line, exact property, and type name.

Correct compressed output:

```text
Build failed.
Error: src/api.ts:42:13 - TS2339: Property 'token' does not exist on type 'Session'.
Impact: cannot verify build.
Next: inspect Session type and patch caller.
```

## Quality Gates

Before final response or phase transition, verify:

| Gate | Pass condition |
|---|---|
| Correctness | No command, path, error, finding, failure, or decision was compressed away |
| Evidence | Claims cite command, file path, URL, test result, or exact source where needed |
| Context discipline | Reads were narrow first; full reads have a reason |
| Tool summaries | No noisy log replay; causal errors preserved |
| Delegation | Specialist work delegated when it improves outcome; simple work answered direct |
| JSON contract | Tool calls remain valid Agent Zero JSON with exact tool names and args |
| Uncertainty | Unknowns use `Unknown:`, `Need:`, or `Risk:` instead of being hidden |
| User preference | Requested detail level overrides compression when necessary |

## Anti-Rationalization

| Rationalization | Reality |
|---|---|
| `Shorter is always better` | Wrong. Short is good only when meaning survives. |
| `The user can ask if they need details` | Errors, security findings, commands, and decisions must be visible now. |
| `I should read the whole file to be safe` | Narrow reads plus targeted search are safer for context and usually enough. |
| `Tool output should be pasted for proof` | Proof needs signal: command, status, key output, path, not noise. |
| `Compression means no delegation` | Delegate normally when specialist skill improves correctness. Compress the prompt and returned summary. |
| `I can skip memory to save tokens` | Durable facts belong in the memory palace so future sessions spend fewer tokens. |
| `I can change tool-call format for terse mode` | Agent Zero's JSON contract is fixed. Compress content, not the framework envelope. |

## Verification Checklist

- [ ] Skill loaded for a matching trigger or explicit user request.
- [ ] Mode selected: `lite`, `full`, `ultra`, or `off`.
- [ ] Final response is concise but preserves required evidence.
- [ ] Commands, paths, errors, security findings, test failures, and decisions are exact.
- [ ] File reads followed discovery → narrow range → broader read only if needed.
- [ ] Shell output summarized as command, exit status, signal, errors, next action.
- [ ] Long-session handoff exists or is updated when context grows.
- [ ] Durable discoveries saved under `/a0/usr/workdir/tolu/memory-palace/wings/{wing}/rooms/` when useful later.
- [ ] Major sessions run backup before ending.
- [ ] Agent Zero JSON tool-call contract remains intact.
