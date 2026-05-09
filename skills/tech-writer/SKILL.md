---
name: "tech-writer"
description: "Create technical content from project work using the sewing-reaping framework. Use when writing blog posts, tutorials, case studies, or documentation from code you've built or projects you've worked on."
version: "1.0.0"
author: "Tolu (based on Thariq/trq212 interview)"
tags: ["technical-writing", "content-creation", "blog", "tutorial", "documentation"]
trigger_patterns:
  - "write a blog post"
  - "write about this project"
  - "create technical content"
  - "turn this into an article"
  - "blog about"
  - "write up this work"
  - "document this project"
  - "technical writing"
  - "write a tutorial"
---

# Tech Writer — Sew, Reap, Publish

Create technical content from project work using the sewing-reaping framework.

Based on Thariq (trq212)'s interview with Sarah Chieng on the craft of technical writing.

## When to Use

- You've built something and want to write about it
- User asks to create a blog post, tutorial, or article from project work
- User wants to document a project's journey or technical decisions
- User asks to turn code/work into shareable content

## The Four Phases

```
REAP → NARRATE → DRAFT → REFINE
```

---

## Phase 1: REAP — Harvest Your Work

The writing comes FROM the work. Before writing anything, extract what happened.

### 1.1 Scan the Project

```
Read these files to understand what was built:
- Project README, PRD, or spec
- Recent git commits (last 2-4 weeks)
- Key source files that changed
- Test files (show what behavior was added)
- Error logs or debug sessions (show what was hard)
```

**Tools:**
- `text_editor:read` — read project files
- `code_execution_tool` — run `git log --oneline -30`, `git diff --stat`
- `memory_load` — check for prior project context

### 1.2 Extract the Raw Material

From the project scan, collect:

| What to Extract | Where to Find It | Why It Matters |
|----------------|-----------------|----------------|
| **What was built** | README, spec, commit messages | The "sewing" — what work was done |
| **What was hard** | Error logs, abandoned approaches in git history | Failures carry more info than successes |
| **What surprised you** | Comments, debug sessions | Surprises = interesting insights |
| **How long it took** | Commit timestamps, PR history | Shows effort, builds credibility |
| **What didn't work** | Branches, reverted commits | Helps others avoid same problems |
| **Decisions made** | PR descriptions, architecture docs | The "why" behind the code |

### 1.3 Validate with AI Research

Use AI to fill gaps in your understanding:

```
Ask the codebase:
- "Tell me the story of how [feature] was implemented"
- "What approaches were tried before the current one?"
- "What's the hardest part of this code and why?"
```

**Tools:**
- `code_execution_tool` — search git history, grep codebase
- `document_query` — query project docs for context

> **Principle:** AI is for RESEARCH, not WRITING. Use it to understand the work. Don't use it to write the prose.

---

## Phase 2: NARRATE — Find the Right Story

Every project has multiple possible narratives. The right one is what your audience needs, not what's most technically impressive.

### 2.1 List Possible Narratives

For any project, generate 3-5 narrative angles:

```
Example — A new caching layer:
1. Technical: "How we reduced latency by 40% with a caching layer"
2. User-focused: "When to clear your cache (and when not to)"
3. Journey: "3 approaches we tried before finding the right caching strategy"
4. Opinion: "Why most developers over-engineer their caching"
5. Tutorial: "Build a caching layer in 30 minutes"
```

### 2.2 Pick the Strongest Narrative

**Selection criteria (in order):**

1. **What do users actually struggle with?** — Talk to users, check GitHub issues, read feedback
2. **What feels "too basic" to you?** — That's often what people need most
3. **What has genuine insight?** — Not just describing a feature, but explaining WHY
4. **What's timely?** — Connect to current conversations in the community

### 2.3 Test the Narrative

Before writing, validate:
- [ ] Can you explain it in one sentence?
- [ ] Does it solve a real problem someone has?
- [ ] Would you click on this headline?
- [ ] Do you have the work/sewing to back it up?

**If any answer is "no", find a different narrative.**

---

## Phase 3: DRAFT — Write with Authenticity

### 3.1 Structure First

Use AI for structure, NOT for prose:

```
Generate an outline with:
- Opening hook (the problem/pain)
- Context (what you were trying to do)
- The journey (what you tried, what failed)
- The solution (what actually worked)
- The insight (what others can learn)
- Downsides/limitations (builds trust)
```

### 3.2 Write the Draft

**Rules for authentic writing:**

1. **Use simple words** — Jargon makes things seem complex. Simple words prove you understand.
   - Bad: "We implemented a distributed event-driven architecture"
   - Good: "When one part of the system needs to tell another part something happened, we send a message"

2. **Share what didn't work** — More valuable than what did.
   - "We tried X first. It failed because Y. Then we tried Z."

3. **Don't sell** — Write about downsides. People trust honesty over hype.
   - "This approach has a limitation: it doesn't handle X well."

4. **Write about what you ACTUALLY built** — Not what the docs say, what you genuinely did.
   - If you didn't use it yourself, say so upfront.

5. **Show the work** — Include code snippets, architecture diagrams, error messages.
   - Diagrams: use AI to generate SVGs from codebase descriptions.
   - Code: real snippets from the project, not toy examples.

### 3.3 Content Types

Pick a format based on the narrative:

| Type | Best For | Length | Template |
|------|----------|--------|----------|
| **Blog Post** | Journey, insight, opinion | 1500-3000 words | `templates/blog-post.md` |
| **Tutorial** | Teaching a specific skill | 1000-2500 words | `templates/tutorial.md` |
| **Case Study** | Real project outcomes | 1500-3000 words | `templates/case-study.md` |
| **Technical Deep-Dive** | Architecture, internals | 2000-4000 words | `templates/deep-dive.md` |
| **Quick Tip** | Single insight, short | 300-600 words | `templates/quick-tip.md` |

**Tools:**
- `text_editor:write` — write the draft
- `code_execution_tool` — generate diagrams (SVG/mermaid)
- `text_editor:read` — pull real code snippets from the project

---

## Phase 4: REFINE — Polish and Publish

### 4.1 Review Checklist

Before publishing, check:

- [ ] **Authenticity**: Did you actually do this work? Can you speak to it genuinely?
- [ ] **Narrative**: Is one clear story being told? (Not three stories competing)
- [ ] **Jargon audit**: Can any technical term be replaced with a simpler word? (Keep load-bearing terms, swap the rest)
- [ ] **Failures included**: Does the content share what didn't work?
- [ ] **Downsides mentioned**: Are limitations or trade-offs discussed?
- [ ] **AI prose check**: Does any paragraph sound like AI wrote it? Rewrite in your voice.
- [ ] **Code snippets**: Are they real code from the project, not made-up examples?
- [ ] **Opening hook**: Would YOU click on this?

### 4.2 AI-Assisted Polish (Use Sparingly)

AI is good for:
- Grammar and spelling checks
- Suggesting headline alternatives
- Checking for clarity gaps
- Proofreading

AI is BAD for:
- Rewriting paragraphs (destroys voice)
- Generating first drafts (sounds generic)
- Full rewrites (loses authenticity)

### 4.3 Save and Cross-Reference

After publishing:

```
Save to memory palace:
- Content → /tolu/memory-palace/wings/projects/rooms/
- Cross-reference → python3 scripts/cross-reference.py build
- Memory → memory_save with topic tags
```

---

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Fix |
|-------------|-------------|-----|
| Writing about features you haven't used | Readers can tell — it's shallow and salesy | Only write about work you've genuinely done |
| Using AI to write the prose | Sounds generic, no voice, no authenticity | Use AI for research and structure only |
| Skipping failures | Misses the most valuable information | Always include what didn't work |
| Too much jargon | Makes things seem complex without adding clarity | Simple words prove understanding |
| Wrong narrative | Right insight, wrong framing = no reach | Test narrative before writing |
| Pure sales pitch | Destroys trust | Share downsides and limitations |
| Over-complicating | Loses readers in unnecessary detail | Start simple, add depth where needed |

---

## Quick Reference: Slash Commands

| Command | What It Does |
|---------|-------------|
| `/write-blog <project>` | Full blog post from project work |
| `/write-tutorial <topic>` | Tutorial from project code |
| `/write-deep-dive <feature>` | Technical deep-dive into a specific feature |
| `/narrative-scan <project>` | List possible narratives for a project |
| `/jargon-audit <file>` | Check content for unnecessary jargon |

---

## Example Workflow

**User:** "Write a blog post about the flashloan system I built"

**Agent:**
1. **REAP**: Read flashloan-system/ README, spec, git log. Extract: built MEV bot, tried 3 DEX integrations, 2 failed, settled on 1inch. Took 3 weeks.
2. **NARRATE**: Generate 4 narratives:
   - "How we built a flashloan MEV bot"
   - "Why 2 of our 3 DEX integrations failed"
   - "Flashloan arbitrage: what the tutorials don't tell you"
   - "A practical guide to MEV extraction"
   Pick #3 — it's the most honest and useful.
3. **DRAFT**: Generate outline, write draft with real code snippets from `/contracts/`, include the 2 failed integrations and why they failed, mention limitations (gas costs, competition).
4. **REFINE**: Jargon audit, add opening hook about losing money on the first attempt, check for AI-sounding prose, save draft.

**Output:** Draft blog post at `/a0/usr/workdir/flashloan-system/blog-post.md`
