# DOX Agent Zero Integration Guide

Detailed patterns for integrating DOX into Agent Zero's orchestrator-subordinate architecture.

---

## 1. Orchestrator Behavior

### Before Delegating File Editing Work

When the orchestrator delegates file editing to a subordinate:

1. **Check for AGENTS.md** in the project root and along the path to target files
2. **Read the DOX chain** from root to target files
3. **Include DOX context** in the delegation message:
   - The relevant AGENTS.md content (or file paths if too long)
   - The instruction: "Follow DOX framework. Read AGENTS.md chain before editing. Update affected AGENTS.md files after meaningful changes."
4. **If no AGENTS.md exists**: instruct the subordinate to create a root AGENTS.md using the DOX template if the work is substantial

### After Subordinate Returns

1. **Verify DOX pass was done** — check that affected AGENTS.md files were updated
2. **If subordinate skipped DOX pass** — either run it yourself or re-delegate with explicit DOX instructions
3. **Check for stale docs** — if the subordinate created/deleted/moved files, ensure Child DOX Index entries are current

---

## 2. Subordinate Behavior

### Developer / Backend Engineer / Frontend Engineer / Fullstack Engineer

When receiving a file editing task:

1. Check if the delegation message includes DOX instructions or AGENTS.md paths
2. If DOX is mentioned: read the AGENTS.md chain from root to target files before editing
3. After meaningful changes: update the nearest owning AGENTS.md and any affected parents/children
4. If no AGENTS.md exists and the work is substantial: create a root AGENTS.md with the DOX template
5. Report which AGENTS.md files were read and updated in the final summary

### Test Engineer

When writing or modifying tests:

1. Read the AGENTS.md chain to understand testing conventions for the area
2. After adding tests: update the nearest AGENTS.md's Verification section if it's empty or outdated
3. If a new test directory is created: create a child AGENTS.md for it

### Code Reviewer

When reviewing code:

1. Read the AGENTS.md chain for the changed files to understand the local contracts
2. Check if the changes violate any AGENTS.md contracts
3. Verify that a DOX pass was done — are the AGENTS.md files current?
4. Flag missing or stale AGENTS.md updates as a review finding

---

## 3. Initialization Workflow

When the user says "Initialize DOX tree for this project now":

```
1. Scan the project recursively (find . -type f -not -path '*/.git/*')
2. Identify meaningful boundaries — directories with their own purpose, rules, or complexity
3. Create root AGENTS.md with:
   - Project-wide instructions
   - Global preferences
   - Durable workflow rules
   - Top-level Child DOX Index
4. For each meaningful subdirectory, create a child AGENTS.md with:
   - Purpose
   - Ownership
   - Local Contracts
   - Work Guidance
   - Verification
   - Child DOX Index (if it has children)
5. Walk back up the tree to fill in all Child DOX Index entries
6. Report the full tree structure to the user
```

### Delegation for Large Projects

For large projects, the orchestrator can delegate the DOX initialization to a developer subordinate using `call_subordinate`:

```
"Initialize DOX tree for this project. 
1. Scan the project recursively.
2. Create a hierarchy of AGENTS.md files — one per meaningful subfolder.
3. Root AGENTS.md: project-wide instructions + top-level Child DOX Index.
4. Child AGENTS.md: Purpose, Ownership, Local Contracts, Work Guidance, Verification, Child DOX Index.
5. Go deep — create nested DOX files where needed.
6. Report the full tree of created files."
```

For very large projects, use `call_swarm` to parallelize: each subordinate handles a subtree.

---

## 4. Memory Palace Integration

DOX knowledge is persisted in the memory palace:

| What | Where |
|------|-------|
| Framework reference | `memory-palace/wings/technical/rooms/dox-framework.md` |
| Agent Zero integration | This file (skill reference) |
| AGENTS.md template | `skills/dox/references/agents-template.md` |

---

## 5. Conflict Resolution

When AGENTS.md docs conflict:

- **Closer doc wins** for local work details
- **No child doc may weaken DOX** — the core contract is non-negotiable
- **Parent docs provide repo-wide rules** — children inherit and specialize
- If a child contradicts a parent on a repo-wide rule, the parent wins

---

## 6. Existing AGENTS.md Files

If a project already has AGENTS.md files (from Codex, Claude Code, etc.):

1. DOX is compatible — AGENTS.md is a native convention
2. Check if the existing content follows DOX structure
3. If not, offer to migrate to DOX format (user must approve)
4. If yes, simply follow the existing DOX hierarchy

---

## 7. Skill Discovery

The DOX skill is discoverable via `skills_tool:search` with these trigger phrases:

- "initialize dox"
- "dox tree"
- "agents.md hierarchy"
- "project context"
- "set up dox"
- "create agents.md"
- "document project structure"
- "context boundaries"

When any of these appear in a user request, the orchestrator loads the DOX skill and follows its instructions.
