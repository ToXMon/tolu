---
name: karpathy-guidelines
description: >
  Behavioral guidelines to reduce common LLM coding mistakes. Use when writing,
  reviewing, or refactoring code to avoid overcomplication, make surgical changes,
  surface assumptions, and define verifiable success criteria.
  Trigger: code review, refactoring, implementation, surgical changes, simplicity,
  over-engineering, code quality, karpathy.
license: MIT
metadata:
  author: forrestchang
  version: "1.0.0"
  source: https://github.com/forrestchang/andrej-karpathy-skills
  argument-hint: <task-description>
---

# Karpathy Guidelines

Behavioral guidelines to reduce common LLM coding mistakes, derived from [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) on LLM coding pitfalls.

**Tradeoff:** These guidelines bias toward caution over speed. For trivial tasks, use judgment.

## How to Use This Skill

When this skill is loaded, apply the four principles below to **every code task**:
- Before writing code, reason through assumptions and ambiguities
- During implementation, favor the simplest solution that meets requirements
- When editing existing code, change only what the task requires
- After implementation, verify against explicit success criteria

If a task is trivial (typo fix, obvious one-liner), these guidelines can be relaxed.

## The Four Principles

### 1. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them - don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.

### 3. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it - don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that YOUR changes made unused.
- Don't remove pre-existing dead code unless asked.

The test: Every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
3. [Step] → verify: [check]
```

Strong success criteria let you loop independently. Weak criteria ("make it work") require constant clarification.

## Anti-Patterns to Avoid

### Over-Abstraction
❌ Don't create class hierarchies, strategies, or factories for single-use code.
✅ Write a simple function. Refactor only when a second use case emerges.

### Speculative Features
❌ Don't add caching, validation, notifications, or logging that wasn't requested.
✅ Implement exactly what was asked. Mention improvements as suggestions, not code.

### Drive-by Refactoring
❌ Don't reformat, rename, or "improve" code adjacent to your changes.
✅ Match existing style. Only change lines directly related to the task.

### Silent Assumptions
❌ Don't pick an interpretation and run with it.
✅ State your interpretation. If ambiguous, present options and ask.

## Examples

See §§include(/a0/usr/skills/karpathy-guidelines/docs/EXAMPLES.md) for detailed before/after examples.

## Success Indicators

These guidelines are working if you see:
- **Fewer unnecessary changes in diffs** — Only requested changes appear
- **Fewer rewrites due to overcomplication** — Code is simple the first time
- **Clarifying questions come before implementation** — Not after mistakes
- **Clean, minimal PRs** — No drive-by refactoring or "improvements"
