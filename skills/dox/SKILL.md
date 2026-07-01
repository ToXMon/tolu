---
name: dox
description: >-
  DOX framework — hierarchical AGENTS.md system that gives AI agents precise project context.
  Agents read the AGENTS.md chain from root to target before editing, and update affected
  AGENTS.md files after meaningful changes. Use when editing files in a project, initializing
  a DOX tree, maintaining project documentation, establishing context boundaries, or when
  the user says "initialize dox", "dox tree", "agents.md hierarchy", "project context",
  "set up dox", "create agents.md", "document project structure", "context boundaries".
---

# DOX — Hierarchical AGENTS.md Framework

## Purpose

DOX solves the core problem of AI coding agents: **narrow file-level view without top-down project context**. Agents guess conventions, cross responsibility boundaries, and miss established patterns. DOX fixes this with a hierarchy of AGENTS.md files that act as binding work contracts for every subtree.

**One file per domain. Root gives overview. Children give precision. Together they give the agent the full picture before it touches anything.**

Source: [github.com/agent0ai/dox](https://github.com/agent0ai/dox) (MIT License)

---

## When to Use

- **Before editing any file in a project** — read the AGENTS.md chain from root to target path
- **After meaningful changes** — update affected AGENTS.md files to keep docs current
- **User says "Initialize DOX tree"** — scan project recursively and build full AGENTS.md hierarchy
- **Starting work in a new project** — check if AGENTS.md exists, follow DOX if it does
- **Creating a new module/directory** — create a child AGENTS.md for the new boundary
- **Project documentation is stale or missing** — DOX pass brings it current

---

## Core Contract

- AGENTS.md files are **binding work contracts** for their subtrees
- Work products, source materials, instructions, records, assets, and durable docs must stay understandable from the nearest applicable AGENTS.md plus every parent AGENTS.md above it
- No child doc may weaken DOX

---

## Read Before Editing

1. Read the root AGENTS.md
2. Identify every file or folder you expect to touch
3. Walk from the repository root to each target path
4. Read every AGENTS.md found along each route
5. If a parent AGENTS.md lists a child AGENTS.md whose scope contains the path, read that child and continue from there
6. Use the nearest AGENTS.md as the local contract and parent docs for repo-wide rules
7. If docs conflict, the closer doc controls local work details, but no child doc may weaken DOX

**Do not rely on memory.** Re-read the applicable DOX chain in the current session before editing.

---

## Update After Editing

Every meaningful change requires a DOX pass before the task is done.

Update the closest owning AGENTS.md when a change affects:

- purpose, scope, ownership, or responsibilities
- durable structure, contracts, workflows, or operating rules
- required inputs, outputs, permissions, constraints, side effects, or artifacts
- user preferences about behavior, communication, process, organization, or quality
- AGENTS.md creation, deletion, move, rename, or index contents

Update parent docs when parent-level structure, ownership, workflow, or child index changes. Update child docs when parent changes alter local rules. Remove stale or contradictory text immediately. Small edits that do not change behavior or contracts may leave docs unchanged, but the DOX pass still must happen.

---

## Hierarchy

- **Root AGENTS.md** is the DOX rail: project-wide instructions, global preferences, durable workflow rules, and the top-level Child DOX Index
- **Child AGENTS.md files** own domain-specific instructions and their own Child DOX Index
- Each parent explains what its direct children cover and what stays owned by the parent
- The closer a doc is to the work, the more specific and practical it must be

---

## Child Doc Shape

Create a child AGENTS.md when a folder becomes a **durable boundary** with its own purpose, rules, responsibilities, workflow, materials, or quality standards.

Default section order:
```
- Purpose
- Ownership
- Local Contracts
- Work Guidance
- Verification
- Child DOX Index
```

- Work Guidance must reflect current standards; if none exist yet, leave empty
- Verification must reflect an existing check; if none exists yet, leave empty and update when one exists

---

## Style

- Keep docs concise, current, and operational
- Document stable contracts, not diary entries
- Put broad rules in parent docs and concrete details in child docs
- Prefer direct bullets with explicit names
- Do not duplicate rules across many files unless each scope needs a local version
- Delete stale notes instead of explaining history
- Trim obvious statements, repeated rules, misplaced detail, and warnings for risks that no longer exist

---

## Closeout

1. Re-check changed paths against the DOX chain
2. Update nearest owning docs and any affected parents or children
3. Refresh every affected Child DOX Index
4. Remove stale or contradictory text
5. Run existing verification when relevant
6. Report any docs intentionally left unchanged and why

---

## Initialize DOX Tree

When the user says "Initialize DOX tree for this project now":

1. Scan the entire project recursively
2. Evaluate the structure and complexity of each area
3. Build a full hierarchy of AGENTS.md files — one inside each meaningful subfolder
4. Each AGENTS.md describes its own domain in precise, specific terms
5. Root AGENTS.md contains project-wide instructions and the top-level Child DOX Index
6. Child AGENTS.md files contain local instructions and their own Child DOX Index
7. Write all of it — the user writes none of it

Go deep and scan files recursively to properly evaluate complexity and create nested DOX files where needed.

---

## Agent Zero Integration

### Global Behavior (Always Active)

DOX behavior is installed globally via `behaviour_adjustment`. Every agent — orchestrator and subordinates — follows DOX when editing project files:

1. **Before editing**: Check for AGENTS.md in the project root and along the path to the target file. Read the chain from root to target.
2. **After meaningful changes**: Run a DOX pass — update the nearest owning AGENTS.md and any affected parents or children.
3. **No AGENTS.md yet**: If the project has no AGENTS.md, the first edit session should offer to initialize the DOX tree.
4. **Subordinate delegation**: When delegating file editing to subordinates, instruct them to follow DOX. Include the DOX chain context in the delegation message.

### Delegation Protocol

When delegating file editing work to subordinates:

```
<message includes>
- Goal and task description
- DOX instruction: "Follow DOX framework. Read AGENTS.md chain from project root to target files before editing. Update affected AGENTS.md files after meaningful changes."
- If AGENTS.md files exist: include their content or paths in the delegation message
- If no AGENTS.md exists: instruct subordinate to create one for the project root if the work is substantial
</message>
```

### Memory Palace

DOX knowledge is saved to the memory palace at:
- `memory-palace/wings/technical/rooms/dox-framework.md` — framework reference and integration notes

---

## Verification

After DOX work:

- [ ] AGENTS.md chain read from root to target before editing
- [ ] Nearest owning AGENTS.md updated after meaningful changes
- [ ] Child DOX Index refreshed if structure changed
- [ ] Stale or contradictory text removed
- [ ] No child doc weakens DOX
- [ ] Docs are concise, current, and operational

---

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "I'll just edit the file directly" | Without reading the AGENTS.md chain, you're guessing at conventions and boundaries. |
| "The docs are probably current" | Re-read them. Memory from prior sessions is not reliable. |
| "This change is too small for a DOX pass" | Small changes can still affect contracts. The pass must happen — docs may stay unchanged if justified. |
| "I'll update the docs later" | Later never comes. Update immediately after the meaningful change. |
| "I don't need to create a child AGENTS.md for this" | If the folder is a durable boundary with its own rules, it needs one. |
| "The existing AGENTS.md is stale, I'll ignore it" | Update it as part of your DOX pass. Don't work around stale docs — fix them. |

---

## References

- `references/agents-template.md` — Raw DOX AGENTS.md template (paste into project root)
- `references/integration-guide.md` — Detailed Agent Zero integration patterns
- Source: [github.com/agent0ai/dox](https://github.com/agent0ai/dox)
