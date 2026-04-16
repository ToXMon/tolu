# Karpathy Coding Guidelines

**Source**: [Andrej Karpathy's observations](https://x.com/karpathy/status/2015883857489522876) via [forrestchang/andrej-karpathy-skills](https://github.com/forrestchang/andrej-karpathy-skills)
**Added**: 2026-04-12
**Status**: Active — adopted as behavioral rules for developer, hacker, ai-engineer profiles

## The Four Principles

| # | Principle | Core Rule |
|---|-----------|----------|
| 1 | Think Before Coding | Don't assume. Surface tradeoffs. State assumptions. Ask when uncertain. |
| 2 | Simplicity First | Minimum code solving the problem. No speculative features or over-abstraction. |
| 3 | Surgical Changes | Touch only what you must. Match existing style. Clean only your own mess. |
| 4 | Goal-Driven Execution | Define success criteria. Loop until verified. Transform tasks into verifiable goals. |

## Anti-Patterns to Avoid
- **Over-Abstraction**: Class hierarchies for single-use code
- **Speculative Features**: Caching, validation, notifications not requested
- **Drive-by Refactoring**: Reformatting/renaming adjacent code
- **Silent Assumptions**: Picking interpretations without stating them

## Integration Points

| Location | Purpose |
|----------|----------|
| `/a0/usr/skills/karpathy-guidelines/SKILL.md` | Agent Zero skill (loadable) |
| `/a0/usr/workdir/tolu/skills/karpathy-guidelines/` | Memory Palace backup |
| `/a0/usr/workdir/tolu/configs/agent-profiles/developer/` | Developer profile with guidelines |
| `/a0/usr/workdir/tolu/configs/agent-profiles/hacker/` | Hacker profile with guidelines |
| Behavioural adjustment | Applied to all coding profiles system-wide |

## Examples
See `/a0/usr/skills/karpathy-guidelines/docs/EXAMPLES.md` for detailed before/after code examples.
