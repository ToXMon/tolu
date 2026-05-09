# Agent Zero Harness Design Patterns Research

Date: 2026-05-09
Sources inspected locally:
- https://github.com/addyosmani/agent-skills
- https://github.com/VoltAgent/awesome-agent-skills
- https://github.com/lsdefine/GenericAgent
- https://arxiv.org/html/2604.25850v3

## Durable patterns

1. Skill anatomy should encode workflow, not reference prose: trigger conditions, core process, rationalizations, red flags, verification evidence, optional supporting files. Agent Zero skills should standardize this shape.
2. Lifecycle commands should map to IDEA/SPEC/PLAN/BUILD/VERIFY/REVIEW/SHIP and load skills automatically. Add human gates at spec/plan/ship and a rollback plan before GO.
3. Specialist profiles should act as independent reviewers. Ship gate should fan out to code reviewer, security auditor, and test engineer; main agent merges reports and owns final decision.
4. Harness evolution should target multiple editable layers: system prompt, skills, tools/plugins, middleware/extensions, long-term memory, evaluation sets. Prompt-only evolution misses large gains.
5. Evaluation needs observability and regression tracking: store traces, manifests, predicted fixes/regressions, pass@1, tokens/trial, and rollback ineffective edits.
6. GenericAgent pattern: minimal atomic toolset plus layered memory and self-crystallized SOPs. Adapt for Agent Zero via evidence-only memory writes and skill creation after verified repeated task paths.
7. Governance gaps: third-party skills are curated, not audited; scan for prompt injection/tool poisoning/malware; require scoped tools and provenance. Self-modification needs workspace bounds, manifests, rollback, and misuse prevention.
8. Domain buildout: create domain skill packs/profiles for Web3, hackathons, bug bounties, frontend, backend, QA, release; combine with safety gates and artifact evidence.

## Key citations

- addyosmani/agent-skills README: Commands lines 18-32; All 21 Skills lines 128-187; Agent Personas lines 191-199; How Skills Work lines 216-240; Project Structure lines 247-279.
- addyosmani docs/skill-anatomy.md: frontmatter lines 18-31; standard sections lines 33-67; rationalizations lines 83-87; verification lines 91-92; writing principles lines 103-110.
- addyosmani /.claude/commands/ship.md: fan-out lines 5-24; merge lines 28-38; decision/rollback lines 39-71.
- VoltAgent awesome-agent-skills README: ecosystem lines 38-44; security notice lines 1457-1468; paths lines 1472-1483; quality standards lines 1486-1499; Web3/Solana line 1428; bug/security lines 1368, 1419-1420.
- GenericAgent README: minimal/self-evolving lines 18-31; self-evolution mechanism lines 34-49; layered memory/tools loop lines 185-223.
- GenericAgent memory SOPs: plan_sop exploration/delegation/verification lines 9-22, 64-82, 175-207; verify_sop lines 1-16, 29-65; memory_management_sop lines 1-15 and 16-24.
- AHE arXiv 2604.25850v3: Setup §4.1; Main results §4.2; Transfer §4.3; Analysis §4.4; Conclusion/Limitations §5. Reported Terminal-Bench pass@1 69.7%→77.0%; evidence-driven fix precision 33.7%, recall 51.4%; regression precision/recall 11.8%/11.1%; governance limitations.
