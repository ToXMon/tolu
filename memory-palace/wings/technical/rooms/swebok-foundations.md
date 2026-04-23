# SWEBOK v3 Foundations — Agent Zero Integration

**Source**: IEEE Computer Society, SWEBOK Guide v3.0 (2014)
**PDF**: `/a0/usr/uploads/swebok-v3.pdf`
**Created**: 2026-04-22

## 15 Knowledge Areas

| # | Knowledge Area | Agent Zero Coverage |
|---|---|---|
| 1 | Software Requirements | `swebok-quality-engineering` skill + `swebok-developer-knowledge` skill |
| 2 | Software Design | Developer profile (built-in) |
| 3 | Software Construction | `agentic-coding-harness` skill + Karpathy guidelines |
| 4 | Software Testing | `swebok-quality-engineering` skill (testing-techniques.md, test-strategy template) |
| 5 | Software Maintenance | `swebok-configuration-management` skill (maintenance-techniques.md) |
| 6 | Software Configuration Management | `swebok-configuration-management` skill (branching-strategies.md, release-checklist template) |
| 7 | Software Engineering Management | `swebok-developer-knowledge` skill (Process Measurement section) |
| 8 | Software Engineering Process | `agentic-coding-harness` BUILD→VERIFY→HARDEN→GATE loop |
| 9 | Software Engineering Models and Methods | Developer profile (built-in) |
| 10 | Software Quality | `swebok-quality-engineering` skill (defect-taxonomy.md, quality-plan template) |
| 11 | Software Engineering Professional Practice | Deslop + Karpathy skills (ethics, documentation) |
| 12 | Software Engineering Economics | `swebok-developer-knowledge` skill (Process Measurement section) |
| 13 | Computing Foundations | Developer profile (built-in) |
| 14 | Mathematical Foundations | Developer profile (built-in) |
| 15 | Engineering Foundations | Developer profile (built-in) |

## Skills Created

| Skill | Location | SWEBOK Chapters | Files |
|---|---|---|---|
| `swebok-developer-knowledge` | `/a0/usr/skills/swebok-developer-knowledge/` | 1,4,5,6,7,10 | SKILL.md (107 lines) |
| `swebok-quality-engineering` | `/a0/usr/skills/swebok-quality-engineering/` | 1,4,10 | SKILL.md + 3 knowledge + 3 templates |
| `swebok-configuration-management` | `/a0/usr/skills/swebok-configuration-management/` | 5,6 | SKILL.md + 2 knowledge + 1 template |

## Developer Profile Enhancement

- Profile moved to `/a0/usr/agents/developer/` (survives updates)
- `specifics.md`: 188 lines, SWEBOK content extracted to on-demand skill
- 3-line directive in profile loads `swebok-developer-knowledge` when needed
- 4 process steps interspersed: Requirements Traceability, Test Strategy Definition, Configuration Baseline, Quality Gate Enforcement

## Usage in New Builds

1. **Simple dev tasks**: Developer profile works as-is (no SWEBOK overhead)
2. **Quality-focused tasks**: Agent auto-loads `swebok-developer-knowledge` via trigger patterns
3. **Testing work**: Load `swebok-quality-engineering` for test strategy templates
4. **SCM/release work**: Load `swebok-configuration-management` for branching strategies and release checklists
5. **Full lifecycle**: Combine `agentic-coding-harness` + SWEBOK skills for production-grade autonomous coding
