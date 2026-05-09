# Solo Founder Stack of 2026

**Source**: Rohit (@rohit4verse), Twitter thread, April 2026
**Theme**: The full AI-powered team for a solo founder reaching $1M revenue
**Saved**: 2026-04-24

---

## The Team Chart (5 jobs, 1 person, 0 hires)

| Role | Tool | How |
|------|------|-----|
| Engineer | Claude Code | CLAUDE.md + skills + MCP integrations |
| Content Editor | Pipeline | Video repurposing (YouTube → 10 platform posts) |
| SDR | Pipeline | Lead enrichment → first-touch email |
| Junior Analyst | Pipeline | Competitive intelligence (weekly competitor briefs) |
| Bookkeeper | Pipeline | Invoice/PDF extraction → Xero |
| Support Hire | Pipeline | Knowledge base agent drafting replies in your voice |
| Marketing Team | Higgsfield Marketing Studio | Research + strategy + production end-to-end |
| Researcher | Hermes Agent (Nous) or OpenClaw | Scheduled research jobs, subagents, persistent memory |
| Face/Brand | AI Persona | Locked-in face/voice, used forever |

---

## Claude Code as Engineer — The Setup That Matters

The leverage is in the workspace, not the prompts:

1. **CLAUDE.md** — Write conventions like a tech lead onboarding a senior hire. Database location, auth flow, test requirements, what the agent can/cannot touch.
2. **Skills** — Short markdown files teaching the agent one class of task end-to-end. `ship-feature.md`, `triage-bug.md`, `migrate-schema.md`. Write once, use forever.
3. **MCP (Model Context Protocol)** — Wire integrations once (GitHub, Postgres, Slack, Linear, filesystem). Agent uses them forever.

> "Pipe prompts into the chat without doing the setup and you have an autocomplete. Do the setup and you have a hire."

---

## The Research Layer

Two tools, both open source, install in <5 minutes:

### Hermes Agent (Nous Research)
- 70+ built-in skills (web search, browser automation, vision, image gen, TTS)
- Built-in cron for scheduled research jobs
- Subagents in parallel for concurrent workstreams
- Persistent memory across sessions
- Programmatic tool calling via `execute_code`
- Runs on $5 VPS

### OpenClaw
- 750K+ GitHub stars, 800+ community skills on ClawHub
- Local-first: reads Obsidian vaults, Notion exports, local PDFs, terminal output
- Three layers: channel (WhatsApp/Telegram/Slack), brain (LLM), body (tools/integrations)
- Better for research touching local files and inbox

### Community Move: Stack Both
- Hermes for cloud research against public web
- OpenClaw for local research (files, inbox, private notes)
- Bridge: HermesClaw for shared messaging account coordination

### Three Research Jobs to Set Up First
1. Scrape top 50 Meta ads in category every Monday → cluster hooks → brief
2. Monitor X/Reddit for viral niche posts → summarize complaints → queue as hook candidates
3. Read own support tickets weekly → surface top 3 customer pain phrases

---

## Higgsfield Marketing Studio

End-to-end marketing pipeline:

1. Paste product URL (only input needed)
2. Pick AI persona (face, voice, vibe)
3. Hermes Agent scrapes Meta Ads Library + TikTok Creative Center for converting hooks
4. Seedance 2.0 renders videos with captions, pacing, hooks
5. Output: 500+ ad-ready cuts/day in 9:16, 1:1, 16:9
6. Loop closes: Hermes tracks winners, doubles down, kills losers

---

## The Marketing Gap

> "The product was fine. The product was sometimes excellent. Nobody saw it."

- Pieter Levels: ~10% hit rate across 70 products, sitting on 10 years of audience
- Marketing is the job that didn't get automated when building did

---

## AI Persona Evidence

- **Aitana López**: 25yo fitness model from Barcelona, ~$11K/month brand deals. Does not exist.
- **Lil Miquela**: Active since 2016, 8-figure annual brand deals. Does not exist.
- In 2026, the persona is part of the stack.

---

## Core Insight

> "The bottleneck stopped being the product a long time ago. The work to fill the rest of the chart is the work that pays."

The companies hitting $1M solo will be the ones who figured out the team chart first.

---

## Cross-References
- User's OpenClaw agent profile: `/a0/usr/agents/openclaw/`
- User's active projects in workdir: flashloan, taskflow, sentient, tolutrade, chainedge, etc.
- User's solo founder aspirations (Pieter Levels model)
