---
name: deslop
description: Anti-slop writing skill that eliminates detectable AI writing patterns. Use when generating or editing any long-form text, articles, blog posts, emails, or creative writing to ensure natural, human-quality output.
version: "1.0.0"
author: compiled-for-agent-zero
tags: ["writing", "anti-slop", "deslop", "content-quality", "editing"]
trigger_patterns:
  - "write a blog post"
  - "write an article"
  - "improve this writing"
  - "make this sound more natural"
  - "deslop"
  - "remove AI writing patterns"
  - "humanize this text"
  - "edit this content"
---

# Deslop Skill — Anti-AI-Slop Writing

## Purpose
Eliminate detectable AI writing patterns from generated text. Apply these rules at generation time and during post-generation audits.

## Core Rules (Always Active)

### 1. Banned Words
Never use these words/phrases. Replace with plain alternatives:

| Banned | Replacement |
|---|---|
| delve | examine, explore, dig into |
| tapestry | mix, blend, collection |
| leverage | use, apply |
| seamlessly | smoothly, without friction |
| groundbreaking | new, major, important |
| transformative | major, significant |
| pivotal | key, critical, central |
| harness | use, tap into |
| it's worth noting | (delete entirely) |
| I cannot stress enough | (delete entirely) |
| notably | (delete or rephrase) |
| certainly | (delete entirely) |
| absolutely | yes, definitely (only in dialogue) |
| this is crucial | (show, don't tell) |
| revolutionize | change, reshape |
| unprecedented | never before, first |
| cutting-edge | latest, advanced |
| game-changing | major, important |
| paradigm shift | fundamental change |
| robust | strong, solid, reliable |
| scalable | flexible, adaptable |
| holistic | complete, full, thorough |
| synergy | cooperation, combined effect |
| empower | help, enable, support |
| streamline | simplify, speed up |
| foster | encourage, promote |
| facilitate | help, enable |
| utilize | use |
| implement | build, set up, add |
| comprehensive | complete, full |
| in conclusion | (delete — just conclude) |
| in summary | (delete — just summarize) |
| as an AI language model | (delete entirely) |
| I'd be happy to help | (delete entirely) |
| great question | (delete entirely) |
| of course | (delete entirely) |
| by the way | (use sparingly or delete) |
| it goes without saying | (then don't say it) |
| needless to say | (then don't say it) |
| at the end of the day | ultimately, finally |

### 2. Banned Structures
Never use these sentence patterns:

- **"It isn't just X, it's Y"** — restructure entirely
- **Question → immediate answer hook** — don't pose a question and answer it in the next sentence
- **Em dashes as stylistic punctuation** — use sparingly, not as a crutch
- **Sentence fragments for style** — only if it serves the content, not as affectation
- **"Topic: Sentence" bullet format** — vary structure in lists
- **Same-length sentences** — vary rhythm deliberately
- **Intro paragraph restating the question** — start with substance
- **Conclusion summarizing the entire piece** — end with impact, not recap

### 3. Structural Techniques

1. **Cut the first paragraph** — AI front-loads framing; start from the second paragraph
2. **Cut the conclusion** — End one step earlier; let the reader draw conclusions
3. **Active voice + strong verbs** — Collapse "provides a solution for" → "solves"
4. **Vary sentence length** — Short. Then longer ones with subordinate clauses. Then medium.
5. **Show, don't tell** — Replace "this is important" with evidence or specifics
6. **Specific > generic** — Replace "various methods" with named methods
7. **Concrete numbers** — Replace "many" with actual counts or percentages

### 4. Self-Audit Scoring (50-point rubric)

Before presenting final text, score yourself:

| Criterion | Points | Description |
|---|---|---|
| Directness | 0–10 | No filler, no throat-clearing, starts with substance |
| Rhythm | 0–10 | Sentence length varies; not monotonous |
| Trust | 0–10 | No hedging, no "it's worth noting", confident tone |
| Authenticity | 0–10 | Sounds human; no AI tells or banned patterns |
| Density | 0–10 | High info-per-word ratio; no fluff paragraphs |

**Minimum passing score: 35/50.** If below, revise before presenting.

## Workflow Integration

### For Generation Tasks
1. Apply banned word list during drafting
2. Vary sentence structure consciously
3. Start with substance, not framing
4. End with impact, not summary
5. Run self-audit before presenting

### For Editing Tasks
1. Load the text
2. Search for banned words (use grep or visual scan)
3. Check for banned structures
4. Apply structural techniques
5. Score on rubric
6. Present cleaned version with score

## Supporting Files
- `docs/banned-words.txt` — Full banned word list for grep/automation
- `docs/resource-links.md` — Source links and references

## Sources
- github.com/jalaalrd/anti-ai-slop-writing
- github.com/sam-paech/auto-antislop
- blog.stephenturner.us/p/deslop
- louisbouchard.ai/ai-editing
- x.com/Whats_AI/status/2034238671524647422
