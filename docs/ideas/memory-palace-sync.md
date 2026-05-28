# Memory Palace Sync — Curated Knowledge Audit & Portable Export

## Problem Statement

**How might we reconcile the tolu memory palace repo with 5+ weeks of accumulated Agent Zero knowledge (90 skills, 34 agent profiles, 18 plugins, multiple project learnings) through a curated, security-cleaned, portable sync that enables specialized agents (Hermes, opencode, OpenClaw) to adopt the knowledge base on a VPS?**

## Recommended Direction

A **curated, security-gated, portable knowledge sync** — not a full mirror, not an automated pipeline. The approach blends three variations:

1. **Curated Export (V2)**: Select the 25-30 most valuable skills from the 77 untracked, rather than wholesale copying all 90. Each skill gets evaluated for reuse value across agent frameworks.

2. **Portable Knowledge Pack (V4)**: Export knowledge in architecture-agnostic formats (Markdown docs, YAML manifests, JSON metadata) so Hermes, opencode, and OpenClaw can consume it regardless of their framework. Agent Zero-specific conventions get documented alongside portable alternatives.

3. **Security-First Sweep (V3)**: Run a pragmatic secret scan (catch real secrets: API keys, tokens, passwords) before any file enters the repo. Non-sensitive references (wallet addresses in documentation, project names) are allowed. The scan runs as a gate before the sync, not after.

The output is a single clean commit pushed to `github.com/ToXMon/tolu`.

## Key Assumptions to Validate

- [ ] The 25-30 curated skills selected actually cover the needs of Hermes, opencode, and OpenClaw — verify by checking each agent's planned capabilities
- [ ] Agent Zero skill format (SKILL.md) is portable enough that other frameworks can parse it without major rework
- [ ] No secrets exist in memory palace rooms or agent profiles — the scan will confirm or refute this
- [ ] Existing 40 memory palace rooms are still accurate enough to trust without audit
- [ ] A single commit is sufficient — no need for branch-based review or staged rollout

## MVP Scope

### In Scope
- Security scan of entire tolu repo + candidate files from workdir
- Curated selection of 25-30 skills from workdir (prioritizing trading, DevOps, security, AI engineering, and agent infrastructure)
- Agent profile index: a manifest of all 34 canonical profiles with descriptions, callable names, and portability notes
- Plugin catalog: descriptive index of all 18 plugins with what they do and how to adopt them
- New memory palace rooms for: accumulated learning, agent profile audit findings, skill taxonomy, plugin capabilities
- Portable export format documentation: how each artifact maps to non-Agent-Zero frameworks
- Single commit pushed to main

### Out of Scope (Not Doing)

| Not Doing | Reason |
|-----------|--------|
| Full mirror of all 90 skills | Signal-to-noise ratio too low; most skills are Domino/JS-pattern specific |
| Audit of existing 40 memory palace rooms | User decision: trust existing rooms, add new ones only |
| Automated sync pipeline (V7) | Over-engineering for a single sync; can add later if needed |
| CI/CD integration | Single commit doesn't need CI; can add in future |
| Cross-repo sync with condor/trustclaw | Each repo has its own purpose; tolu is the knowledge layer |
| Refactoring existing room structure | Current wing/room model works; no structural changes needed |
| Paranoia-level security scan | User decision: pragmatic — catch real secrets, allow non-sensitive references |

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| Secret leak to public repo | CRITICAL | Run `gitleaks` + custom regex scan before commit. Block on any finding. |
| Curated skills miss important ones | MEDIUM | Document selection criteria and excluded list. User reviews before commit. |
| Portable format doesn't fit target frameworks | MEDIUM | Include raw SKILL.md alongside portable docs. Agents can use either. |
| Repo bloat from large files | LOW | .gitignore for binaries, images, logs. Only text/markdown/code files. |
| Git history contains secrets from prior commits | HIGH | If scan finds secrets in history, use `git filter-repo` to scrub before push. |

## Success Criteria

1. **Security clean**: `gitleaks` scan returns 0 findings on the final commit
2. **Skills curated**: 25-30 skills added to `tolu/skills/` with SKILL.md files
3. **Agent profiles indexed**: A single manifest at `tolu/docs/agent-profiles.md` listing all 34 profiles with portability notes
4. **Plugin catalog**: A single manifest at `tolu/docs/plugin-catalog.md` listing all 18 plugins with adoption guidance
5. **New knowledge rooms**: At least 5 new memory palace rooms covering: agent profiles, skill taxonomy, plugin capabilities, trading infrastructure, VPS deployment learnings
6. **Portable format docs**: A `tolu/docs/portable-format-guide.md` explaining how to adopt artifacts in non-Agent-Zero frameworks
7. **Single commit**: One clean commit with descriptive message, pushed to `origin/main`
8. **User approved**: User reviews the diff before push

## High-Level Approach for the Single Commit

```
1. SCAN     — Run gitleaks + custom regex on tolu/ and candidate workdir files
2. SELECT   — Choose 25-30 skills based on: trading infra, agent ops, security, AI/ML, DevOps
3. COPY     — Copy selected skills to tolu/skills/ (SKILL.md + supporting files)
4. INDEX    — Generate agent-profiles.md and plugin-catalog.md manifests
5. DOCUMENT — Write portable-format-guide.md
6. ADD      — Create new memory palace rooms for accumulated knowledge
7. REVIEW   — Show full diff to user for approval
8. COMMIT   — Single commit: 'Sync: curated knowledge audit — 25 skills, 34 profiles, 18 plugins, 5 rooms'
9. PUSH     — Push to origin/main after user gate approval
```

## Related Repos (No Sync Needed)

| Repo | Purpose | Overlap |
|------|---------|--------|
| `condor` | AI trading agent harness | Consumes tolu knowledge, doesn't sync back |
| `trustclaw` | Self-hostable AI agent with vector memory | Alternative architecture; shares design patterns |
| `agent-workflows` | Agent gallery portfolio | Showcase, not knowledge store |
| `ironclaw` | OpenClaw-inspired Rust implementation | Rust port; adopts patterns from tolu |

## Open Questions

- Which 25-30 skills make the final cut? (Needs selection pass during /spec or /plan)
- Should the portable format guide target a specific framework (opencode?) or stay generic?
- Does the user want a pre-push hook to prevent future secret leaks?

---

*Refined through idea-refine skill — Phase 1 (Divergent), Phase 2 (Converge), Phase 3 (Sharpen).*
*User decisions: Curated scope, portable formats, pragmatic security, add-new-only, single commit.*
