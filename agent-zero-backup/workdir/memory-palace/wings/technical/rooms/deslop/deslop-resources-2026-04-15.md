# Deslop Resources for AI Writing
> Compiled for Agent Zero — April 15, 2026
> Purpose: Anti-slop techniques, tools, skills, and knowledge for improving AI-generated content quality

---

## GitHub Repositories

### 1. Anti-AI-Slop Writing Skill
- **URL:** https://github.com/jalaalrd/anti-ai-slop-writing
- **Type:** Plug-and-play writing skill
- **Compatibility:** Claude Code, Codex, Cursor, Gemini CLI, and 8+ AI agents
- **Use Case:** Eliminates detectable AI writing patterns at generation time
- **Action:** Clone or load as a skill file directly into agent workflows

---

### 2. Auto-Antislop (sam-paech)
- **URL:** https://github.com/sam-paech/auto-antislop
- **Type:** Inference-level slop suppression framework
- **Key Components:**
  - **Antislop Sampler** — Suppresses 8,000+ slop patterns at token sampling time via backtracking
  - **Automated Profiling Pipeline** — Generates training data by comparing model output vs. human baselines
  - **FTPO (Final Token Preference Optimization)** — Fine-tuning method achieving 90% slop reduction
- **Benchmarks:** Maintains quality on GSM8K, MMLU, and creative writing evals
- **Paper:** https://arxiv.org/abs/2510.15061
- **Action:** Integrate sampler into LLM inference pipeline; use FTPO for fine-tuning

---

### 3. NousResearch AutoNovel — ANTI-SLOP.md
- **URL:** https://github.com/NousResearch/autonovel/blob/master/ANTI-SLOP.md
- **Type:** Reference catalog / field guide
- **Use Case:** Catalog of AI writing slop signatures for detection and elimination
- **Action:** Load as knowledge document; use as a checklist for post-generation audits

---

## Research Papers

### 4. Antislop: A Comprehensive Framework
- **URL:** https://arxiv.org/abs/2510.15061
- **Published:** October 2025 (arXiv)
- **Summary:** Academic paper behind auto-antislop. Introduces Antislop Sampler, profiling pipeline, and FTPO.
- **Action:** Feed full paper as knowledge context for understanding slop suppression at the model level

---

## Blog Posts & Skill Files

### 5. De-slop the Text You Shouldn't Be Writing Anyway (Stephen Turner)
- **URL:** https://blog.stephenturner.us/p/deslop
- **Published:** March 2026
- **Type:** Claude skill + essay
- **Key Details:**
  - Strips ~30 categories of AI writing tropes at generation time
  - Scores output on a 50-point rubric: directness, rhythm, trust, authenticity, density
  - Includes before/after examples
- **Action:** Load skill file into Claude Code or claude.ai project

---

### 6. How to Clean Up AI-Generated Drafts (Louis Bouchard)
- **URL:** https://www.louisbouchard.ai/ai-editing/
- **Published:** January 2026
- **Key Rules:**
  - Cut the first paragraph (AI front-loads unnecessary framing)
  - Active voice + strong verbs (collapse noun-verb bloat)
  - End one step earlier to remove "AI feel" at the conclusion
- **Action:** Incorporate rules as system prompt instructions

---

### 7. Stop the Slop: Make AI Content That's Actually Good (Surfer SEO)
- **URL:** https://surferseo.com/blog/ai-generated-content/
- **Published:** November 2025

### 8. How to Humanize AI Generated Content (Buildship)
- **URL:** https://buildship.com/humanize-your-ai-content
- **Published:** March 2026

---

## X (Twitter) Experts & Resources

### 9. @Whats_AI — Anti-Slop Prompt Template
- **Post:** https://x.com/Whats_AI/status/2034238671524647422
- **Template Includes:** 7-section framework, 60+ banned words, banned sentence structures, style rules, two-model workflow

### 10. @videojenna (Jenna Potter) — Claude Anti-Slop Skill
- **LinkedIn:** https://www.linkedin.com/posts/videojenna_i-built-a-claude-skill-that-stops-ai-from-activity-7445889349021265920-yWnV
- **Skill Includes:** 60+ banned words with replacements, 8 banned phrase categories, structural patterns to avoid, 4-question self-filter

### 11. @karpathy (Andrej Karpathy)
- **Focus:** LLM behavior, model quality, why models produce slop

### 12. @dair_ai (DAIR.AI)
- **Focus:** Weekly LLM paper threads, output quality benchmarks
