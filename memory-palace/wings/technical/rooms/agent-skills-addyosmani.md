---
name: agent-skills-addyosmani
wing: technical
created: 2026-05-07
type: research-reference
source: https://github.com/addyosmani/agent-skills
tags: [agent-skills, ai-agents, engineering-workflows, skill-design]
---

# Addy Osmani Agent Skills — Research Reference

## What It Is
Production-grade engineering skills for AI coding agents (Claude Code, Cursor, Gemini CLI, etc.). 20 skills organized by SDLC phase, 3 agent personas, 4 reference checklists.

## Complete Skills List (20)

### Define
1. idea-refine — Structured divergent/convergent thinking
2. spec-driven-development — PRD before code

### Plan
3. planning-and-task-breakdown — Decompose specs into tasks

### Build
4. incremental-implementation — Thin vertical slices
5. test-driven-development — Red-Green-Refactor
6. context-engineering — Right info at right time
7. source-driven-development — Ground decisions in official docs
8. frontend-ui-engineering — Component architecture + accessibility
9. api-and-interface-design — Contract-first, Hyrum's Law

### Verify
10. browser-testing-with-devtools — Chrome DevTools MCP
11. debugging-and-error-recovery — Five-step triage

### Review
12. code-review-and-quality — Five-axis review
13. code-simplification — Chesterton's Fence, Rule of 500
14. security-and-hardening — OWASP Top 10
15. performance-optimization — Measure-first

### Ship
16. git-workflow-and-versioning — Trunk-based, atomic commits
17. ci-cd-and-automation — Shift Left, feature flags
18. deprecation-and-migration — Code-as-liability
19. documentation-and-adrs — Document the why
20. shipping-and-launch — Pre-launch checklists

## Agent Personas (3)
- code-reviewer (Senior Staff Engineer)
- test-engineer (QA Specialist)
- security-auditor (Security Engineer)

## Reference Checklists (4)
- testing-patterns.md
- security-checklist.md
- performance-checklist.md
- accessibility-checklist.md

## Structure Pattern
```
skills/skill-name/SKILL.md  (required)
skills/skill-name/supporting.md  (optional)
agents/persona.md
references/checklist.md
.claude/commands/  (slash commands)
```

## SKILL.md Anatomy
- YAML frontmatter (name, description)
- Overview
- When to Use
- Core Process (step-by-step)
- Common Rationalizations (anti-excuse table)
- Red Flags
- Verification (exit criteria checklist)

## Key Design Principles
1. Process, not prose — workflows agents follow
2. Anti-rationalization tables — counter agent excuses
3. Verification is non-negotiable — evidence required
4. Progressive disclosure — supporting files load on demand
5. Token-conscious — every section justifies inclusion
6. Specific over general — "run npm test" not "verify tests"
7. Evidence over assumption — checkboxes require proof

## Google Engineering Principles Embedded
- Hyrum's Law (API design)
- Beyonce Rule + test pyramid (testing)
- Change sizing + review speed (code review)
- Chesterton's Fence (simplification)
- Trunk-based development (git)
- Shift Left + feature flags (CI/CD)
- Code-as-liability (deprecation)

## Recommended Minimal Setup
1. spec-driven-development
2. test-driven-development
3. code-review-and-quality

## Lifecycle Sequence
idea-refine -> spec -> planning -> context-engineering -> source-driven -> incremental-impl -> TDD -> code-review -> git-workflow -> docs -> ship
