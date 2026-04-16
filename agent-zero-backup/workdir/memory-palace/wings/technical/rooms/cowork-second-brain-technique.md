# Cowork + Obsidian: Second Brain Technique

**Source:** Ruben Hassid newsletter (2026-04-15)
**Created:** 2026-04-15
**Tags:** #cowork #obsidian #second-brain #claude #context-management #prompting #skills

---

## Core Principle

**Stop prompting. Start filing.**

Instead of re-typing context (tone, audience, rules, goals) into every AI session, store it as persistent files that the AI reads automatically. The files *are* the prompt. Forever.

---

## Why Bare Prompting Fails

- No context = average, generic output
- Re-typing 500 words of instructions every time is impractical
- "Projects" features require per-topic setup and re-uploading
- Result: output sounds like everyone else's

---

## The Architecture

### 1. Cowork Folder (Local Filesystem)

A folder on your computer that the AI connects to. It reads `.md` files before every session automatically.

**Recommended structure:**

```
cowork-folder/
├── about-me/              # Your identity, style, rules (AI reads these)
│   ├── about-me.md        # Who you are, your taste, preferences
│   ├── anti-ai-style.md   # Rules to avoid generic AI-sounding output
│   └── my-company.md      # Business/project context
├── output/                # Where AI saves its work (don't touch)
├── templates/             # Saved workflow templates (don't touch)
└── skills/                # Reusable task workflows (callable via /command)
```

### 2. Global Instructions

Set at the config level: "Always read `about-me/` before starting. Never touch `output/` or `templates/`."

This ensures every session starts with your full context loaded.

### 3. Obsidian (The Editor Layer)

- Free app at obsidian.md
- Opens your Cowork folder as a "vault"
- Renders `.md` files with proper formatting (headers, bold, bullets)
- Provides sidebar navigation + full-text search across all files
- Edits sync instantly to the filesystem (no import/export)
- **Key:** Obsidian never modifies files in a way that breaks the AI's ability to read them

---

## The Daily Workflow

| Action | Tool | Purpose |
|--------|------|----------|
| Browse, search, read, edit context | Obsidian | Update your "brain" |
| Create new work, generate outputs | Cowork | Build deliverables |

Both point at the same folder. Always in sync.

**Update cycle:**
1. Hate something the AI produced? → Open Obsidian → update the rule file
2. New job/tool/preference? → Edit `about-me.md`
3. Find a better format/pattern? → Add to the relevant file
4. Next Cowork session → automatically reads the updated files

---

## Skills Pattern (Advanced)

For tasks you repeat weekly (LinkedIn posts, newsletters, client briefs, contracts):

1. Create a skill file in the `skills/` folder
2. Each skill = one `.md` file with task-specific instructions
3. Call with `/command` syntax (e.g., `/newsletter`, `/sales-email`, `/weekly-report`)
4. Edit skills in Obsidian to tweak over time

**Skill creation flow:**
1. Start a Cowork session
2. Prompt: "Create a skill called X. Interview me about [topic]. Build the skill. Save it."
3. AI asks questions → generates skill file → saves to output
4. Move skill file to `skills/` folder via Obsidian
5. Call anytime with `/command`

---

## Why This Combo Wins

| Tool | Problem |
|------|---------|
| Notion | Cloud-based, can't point at local `.md` files, needs re-import |
| Google Docs | Not `.md` files, requires format conversion |
| Apple Notes | Closed format, can't point at folder, no `.md` search |
| VS Code / Cursor | Developer-focused, intimidating UI for non-devs |
| GitHub | Requires git knowledge, too complex for editing |
| Typora | One file at a time, no sidebar/search across folder |
| **Obsidian** | Reads existing folder, free, clean UI, no file corruption |

---

## Key Takeaways for OpenClaude

1. **Context as files, not prompts** — store identity, style, rules as `.md` files the AI auto-reads
2. **Separate concerns** — `about-me/` (input), `output/` (AI writes), `skills/` (reusable workflows)
3. **Global instructions enforce structure** — AI always reads context, never touches output
4. **Human edits via Obsidian, AI works via Cowork** — same folder, different interfaces
5. **Iterate by updating files** — bad output → update rule file → fixed forever
6. **Skills for repeated tasks** — one file per workflow, callable via `/command`
7. **Files stay as `.md`** — no hidden metadata, no format corruption, portable

---

## Cross-References

- See also: `memory-palace/` (Tolu's own implementation of this pattern)
- See also: `.promptinclude.md` (Agent Zero's version of global instructions)
- See also: `context-layers/` (layered context loading pattern)
- See also: `tolu-cowork/` (Tolu's Cowork project directory)
