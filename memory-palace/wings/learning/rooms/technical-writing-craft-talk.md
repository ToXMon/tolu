---
title: "The Craft of Technical Writing — Interview Notes"
date: 2026-05-07
source: Microsoft Teams Meeting Transcript
interviewer: Sarah Chieng
interviewee: Thariq (trq212) — Engineer at Anthropic, works on Claude Code
tags: [technical-writing, content-creation, ai-writing, claude-code, engineering, anthropic]
---

# The Craft of Technical Writing

**Interviewer:** Sarah Chieng
**Interviewee:** Thariq (trq212) — Engineer at Anthropic working on Claude Code
**Context:** Interview on the craft of technical writing for developer/AI tools
**Duration:** ~20 minutes

---

## Core Framework: Sewing and Reaping

The writing process has two phases:

1. **Sewing** — Do interesting engineering work. Build things, solve problems, go deep. The raw material for writing comes from real work.
2. **Reaping** — Take what you've learned and turn it into content people want to read. Tell the story.

> "Follow your curiosity and do good work. This always leads to something interesting that other people want to learn from."

---

## Key Principles

### 1. Follow Your Curiosity
- Being deep into something niche means you're effectively the best in the world at it
- People want to hear from the best in the world at something
- Example: Agent coding felt niche at the time, but depth created valuable content

### 2. Simple Isn't Easy
- In agents, the end result always seems simple, but getting there takes months
- Example: "Ask User Question" tool for Claude Code — simple output, 2 months of iteration with 3 variations
- Writing took 2 days; sewing (building the thing) took 1-2 months

### 3. Share What Didn't Work
- More information often lives in what didn't work than what did
- Helps others avoid the same problems
- Makes content more believable — not just a sales pitch

### 4. Don't Sell — Be Genuine
- Align content with how you genuinely use the product
- Writing about downsides and trade-offs builds credibility
- People can tell when you haven't used what you're describing

### 5. Avoid Unnecessary Jargon
- Use simple words where possible — it shows you understand the concept
- Jargon is often used to make things seem complex rather than to clarify
- Some technical terms are load-bearing — keep those, swap the rest

---

## Using AI in Writing

### Good Uses
- **Research**: Search Slack, GitHub history — "Tell me the story of how this happened"
- **Diagrams**: Generate SVGs by pointing at codebase, iterate
- **Outlines**: Helpful for structure
- **Brainstorming**: Generate multiple narrative angles
- **Proofreading/grammar check**

### Bad Uses
- **First drafts**: Almost always throw out AI-generated prose
- **Full rewrites**: Destroys voice and authenticity
- **Writing for you**: People don't want to read purely AI-written content

> "I don't think you should get the AI to write for you. But it can be really good at brainstorming."

---

## Finding the Narrative

Every topic has multiple possible narratives. Finding the right one is critical.

**Example:** Writing about context compaction in Claude Code:
- Technical narrative: how compression works
- User narrative: session management — when to clear, how often
- After talking to users, session management was the real pain point
- The simpler, more intuitive narrative reached a wider audience

**Process for finding narratives:**
1. Talk to customers/users about their problems
2. Show drafts to people for feedback
3. Iterate between work → write → talk → inform
4. What feels "too basic" to you is often what people need most

---

## Sharing Secrets

There's a trade-off between proprietary knowledge and valuable content:

- Example: How Claude Code does system reminders between tool calls — a "secret" about agent design
- Best agent builders didn't know about this technique
- Sharing real internal techniques builds authority
- If you never share secrets, content becomes less interesting

> "People want to learn real things. There is very, very valuable content in sharing how things actually work."

---

## Format Preferences

- **Long-form articles** preferred — can pack in more quality
- **Twitter/X** harder — have to throw a lot at the wall
- **Video** — still developing skills, but AI makes it faster
  - Example: Generated slide deck with Claude, talked over it, edited with script
  - End-to-end video production: 3 hours
  - Now used by Anthropic sales team on every call

## Content That Missed

- Early posts where technical insight was right but narrative was wrong
- Example: "Your agent should be the file system" — correct insight, didn't spread because wrong framing
- Also: Writing about features you don't actually use yourself

---

## Finding Your Tone

- Hard to disentangle personal skill from Claude Code's popularity
- Content reach roughly tracks company revenue/growth
- Early mistake: writing about features without genuine personal use
- First post was about using Claude Code as a general agent — didn't use that setup much himself

---

## Actionable Takeaways

1. **Do the work first** — sewing before reaping
2. **Talk to users** — they reveal what's actually confusing
3. **Share failures and downsides** — builds trust
4. **Use AI for research, not writing** — brainstorm, diagram, outline
5. **Find the right narrative** — often simpler than you think
6. **Write about what you genuinely use** — authenticity shows
7. **Share real techniques** — secrets make content valuable
8. **Simple words > jargon** — proves understanding
9. **Long-form for quality** — articles over tweets for depth
10. **Iterate on narrative** — talk to people, show drafts, refine
