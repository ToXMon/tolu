# 0xSero Blog - Complete Content Extraction

**Source**: https://blog.ethers.club (redirects to https://www.sybilsolutions.ai)
**Author**: Sero (@0xSero on Twitter/X)
**Organization**: Sybil Solutions
**Extracted**: 2026-04-16
**Total Posts**: 13

---

## Post Index

### AI & Machine Learning
- [Part 1: I ragged every conversation I ever had with AI](https://www.sybilsolutions.ai/blog/01-how-i-work-with-ai) (2026-01-17)
- [Part 2: Training My Own Coding Model — The SFT and DPO Pipeline](https://www.sybilsolutions.ai/blog/02-training-my-coding-model-the-pipeline) (2026-01-17)
- [AI-driven NFT marketplace](https://www.sybilsolutions.ai/blog/AI-and-marketing) (2022-08-28)
- [AI Workflows as an Assembly Line](https://www.sybilsolutions.ai/blog/AI-workflows) (2024-10-10)
- [Employment Scams - Deep Dive](https://www.sybilsolutions.ai/blog/Modern-day-scams) (2024-04-03)
- [AI-Assisted Coding: What Actually Works](https://www.sybilsolutions.ai/blog/ai-assisted-coding-experience) (2024-12-23)
- [Choosing a crypto-wallet for your Web3 journey. (Part 1) -Understanding wallets](https://www.sybilsolutions.ai/blog/choosing-a-crypto-wallet-for-your-web3-journey) (2022-07-24)
- [The Benefits Of Scrum](https://www.sybilsolutions.ai/blog/the-benefits-of-scrum) (2022-07-08)
- [Choosing a crypto-wallet for your Web3 journey. (Part 2) -The different types of wallets](https://www.sybilsolutions.ai/blog/understanding-the-types-of-cryptocurrency-wallets) (2022-07-25)
- [Building My Own Homelab: From AI Dependency to Local Superpower](https://www.sybilsolutions.ai/blog/Building-my-own-homelab) (2026-01-15)

### Security & Crypto
- [Employment Red Flags](https://www.sybilsolutions.ai/blog/employment-red-flags) (2022-10-26)
- [MEV Bots and the Dark Forest](https://www.sybilsolutions.ai/blog/mev-bots-and-dark-forests) (2024-12-23)
- [How to remove unwanted content from the web.](https://www.sybilsolutions.ai/blog/remove-unwanted-content) (2022-10-16)

---

## Post 1: Part 1: I ragged every conversation I ever had with AI

- **URL**: https://www.sybilsolutions.ai/blog/01-how-i-work-with-ai
- **Date**: 2026-01-17
- **Description**: I ran a privacy preserving analysis on 809 conversations. The results were humbling, surprising, and exactly what I needed to see.
- **Tags**: Productivity, Reflection, Metrics, Self-Analysis

### Full Content (Verbatim)

I extracted 727MB of conversations from Cursor, Claude, and Codex. Then I ran a privacy preserving analysis on 809/100,000 conversations spanning 4 months. What I found changed how I think about working with AI.

## The Setup

I built a pipeline that:

1. Extracted conversations from local AI tools:GitHub
2. Analyzed behavioral signals without storing raw text
3. Removed all environment variables and sensitive information
4. Generated composite indices from keyword patterns

Total: 19,539 user messages, 11,726 assistant messages, 16,484 tool uses.

## The Strengths According to Data

### 1. Bias toward actionability

My spec completeness score averaged 25%~ of all my conversations. I try to frame problems with clear next steps rather than abstract discussions.

Examples, my most common conversations are debugging related loops:

> "Fix the TypeScript error in file X. Error: Property 'toString' does not exist on type 'never'."

Not "I have a problem." Just the problem, the file, the error, the ask.

### 2. Debug loops over single-shot asks

40.3% of my conversations included error sharing. I iterate. I share the error, get a fix, encounter the next error, share that, repeat. This is incredibly wasteful, given i am in the loop when i shouldn't be. I jump straight to the errors as opposed to having the model lint, typecheck, and fix the errors autonomously.

### 3. Multi-system orchestration

Top languages by conversation:

- Bash: 175
- Go: 156
- Rust: 133
- Solidity: 55
- TypeScript: 335
- SQL: 95

I move between frontend (React, Next.js), backend (Go, TypeScript), infrastructure (Docker, AWS), automation (n8n, Slack integrations).

### 4. Testing awareness

43.6% of conversations mentioned testing. I do not think of myself as test-disciplined. But I mention tests frequently even if I am bad at writing them. I actually wish I was more disciplined about testing, it saves a lot of time specifically because it helps catch bugs early and reduces the need for manual in-the-loop debugging.

## The Improvement Opportunities

The report was honest. Here are the gaps.

### 1. Minimal reproduction

User conversations with reproduction language: 0.4% That means 99.6% of the time, I ask for help without providing a minimal reproducible example. I just dump the error and expect the AI to figure it out, but it's not always enough. I need to improve my minimal reproduction skills.

### 2. Test discipline

In repositories where I have tests I did much less debugging, and much more feature development. In repositories without tests I did much more debugging, and much less feature development. This is very obvious, but it's not always easy to remember. I need to improve my test discipline.

### 3. Security hygiene

Risky disclosure signals: 32.5%

32.5% of my conversations contained signals that could indicate sensitive data exposure. API keys, environment variables, addresses. The heuristics do not store tokens, but they flag patterns. This makes life easier, but if I had spent more time configuring my tools and environment I wouldn't have to rely on the AI to flag them. I need to improve my security hygiene.

### 4. Acceptance criteria

When delegating multi-file changes, I rarely specify acceptance criteria upfront. This shows up in the spec completeness index being barely above 25%. The data caught what I knew was true. I get vague, then iterate, instead of being clear, then shipping. This habit is not sustainable and has made me actively less productive. I need to improve my acceptance criteria.

## The Time-Series Trends

The weekly breakdown told a story.

| Week | n | Spec | Debug | Test | Security | Risky% | Tool Uses |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-09-22 | 19 | 0.487 | 0.049 | 0.357 | 0.113 | 42.1% | 0 |
| 2025-10-13 | 156 | 0.323 | 0.073 | 0.078 | 0.036 | 20.5% | 0 |
| 2025-12-22 | 117 | 0.237 | 0.073 | 0.110 | 0.093 | 41.9% | 6,261 |
| 2026-01-05 | 70 | 0.213 | 0.050 | 0.098 | 0.118 | 38.6% | 3,044 |

### Spec completeness degrades with volume

As conversations increased, spec completeness dropped. More volume, less care. This is the classic trade-off. Speed over quality. It's easy to surrender to the temptation of shipping quickly, but it's important to prioritize quality over speed. By taking the time to write clear acceptance criteria, I can ensure that my work meets the necessary standards and reduces the risk of errors or security vulnerabilities.

Specification, planning, and tests all improve my mental map of the system. By taking the time to write clear acceptance criteria, I can ensure that my work meets the necessary standards and reduces the risk of errors or security vulnerabilities.

### Security awareness is cyclical

Security mentions spiked in weeks 50 (0.135), 47 (0.133), and 46 (0.118). These correlate with integration work, adding new tools, connecting new systems.

## The Composite Indices

The report included heuristic proxies (0-1 scale):

| Index | User (Me) | Assistant |
| --- | --- | --- |
| Spec completeness | 0.275 | 0.277 |
| Debug maturity | 0.056 | 0.040 |
| Testing discipline | 0.096 | 0.173 |
| Security awareness | 0.058 | 0.064 |
| Architecture-thinking | 0.168 | 0.129 |

The assistant beats me on testing (0.173 vs 0.096). It beats me on security (0.064 vs 0.058). But I beat it on architecture (0.168 vs 0.129).

This is telling. I think about structure more than execution. The AI executes better than I do.

## What This Taught Me

### 1. I am an action-oriented, high-volume developer

100,000+ conversations in 8 months. I use AI as for practically everything from code generation to debugging to testing to security to architecture, I also over use it when I want to run commands, setup docker, even when I want to commit and push. I use it for everything. This is telling, I need to be more intentional about how I can decrease my token usage andoptimize my workflows.

### 2. I iterate more than I plan

40% error sharing but only 0.4% repro language. I debug in public. This is efficient for me but exhausting for collaborators.

### 3. I delegate testing, rarely doing it myself

Talking about tests (43.6%) is not writing tests. The assistant has higher testing discipline than I do.

### 4. I leak too much sensitive data

32.5% of conversations contained risky disclosure signals. This is a concrete, measurable hygiene problem.

### 5. The assistant complements my weaknesses

The AI has higher testing discipline and security awareness. It catches what I miss. This is the right mental model. AI as amplifier, not replacement.

## The Action Plan

Based on the data, here is what I am changing.

### 1. Add repro template

~~~
## Error
[exact error message]

## Expected
[what should happen]

## Actual
[what actually happens]

## Minimal repro
[shortest code that demonstrates the issue]
```

### 2. Test discipline checklist

~~~

- [ ] Write test before fix
- [ ] Run tests after fix
- [ ] Add regression check
- [ ] Document test coverage

~~~

### 3. Security scan before commit

```bash
# Pre-commit hook
grep -r "sk-\\|pk-\\|0x[a-fA-F0-9]{64}" --exclude-dir=node_modules

~~~

### 4. Acceptance criteria for delegation

~~~
## Deliverables
- [ ] File A modified
- [ ] File B created
- [ ] Tests pass

## Acceptance
- [ ] Compiles without errors
- [ ] Handles edge case X
- [ ] Matches style of existing code
```

## The Bigger Picture

The question is not whether I use AI. I clearly do, aggressively.

The question is: am I using it to grow, or to avoid growth?
The data suggests both. I ship faster (actionability is high). I think less (spec completeness is low). I delegate testing (assistant beats me).

This is a trade-off. Every speedup has a cost. Every delegation has a gap.

## What I Would Tell Someone Else

If you are analyzing your own AI usage:

1. Extract your data. It is easier than it sounds, and worth it
2. Run privacy-preserving analysis. Do not store raw conversations
3. Look for patterns, not scores. The indices are heuristics. Trends are truth
4. Find gaps. Where are you delegating what you should own?
5. Set concrete changes. Vague improvement goals produce vague results

## The Verdict

The workstyle report was humbling. It confirmed suspicions I had and revealed blind spots I did not.

I am not a great debugger (low debug maturity). I do not write tests (low testing discipline). I leak sensitive data (high risky disclosure).

But I am action-oriented (high constraint framing), multi-system (broad language distribution), and iterative (high error sharing).

The profile is not good or bad. It is just true.

And now that it is true, I can work with it.

---

Continue to Part 2: Training My Own Coding Model, where I take these insights and my actual conversations to train sero-nouscoder [I trained a model on all my chats](https://www.sybilsolutions.ai/blog/02-training-my-coding-model-the-pipeline)

```

```

~~~

---

## Post 2: Part 2: Training My Own Coding Model — The SFT and DPO Pipeline

- **URL**: https://www.sybilsolutions.ai/blog/02-training-my-coding-model-the-pipeline
- **Date**: 2026-01-17
- **Description**: What happens when you fine-tune a 14B parameter model on your own coding conversations? Real numbers, real costs, and real frustrations.
- **Tags**: Machine Learning, Personal Projects, Fine-tuning, AI

### Full Content (Verbatim)

This is the full pipeline: PII scan, masking, temporal ordering, dedup, SFT, and DPO pairs.

## What the raw data looked like

Over 12 months I collected AI coding conversations from three main sources:

- Claude Projects exports
- Cursor IDE logs
- Codex sessions

Total raw data was around 727MB, about 107k conversations. A lot of it was not safe or not usable.

107,502 conversations total. After scanning for secrets, 95,561 got quarantined. That is 89% of my data flagged for potential API keys, private keys, or AWS credentials.

11,711 conversations survived security checks. 51.75 million tokens. Enough to fill 1,200 copies of The Great Gatsby with nothing but code and error messages.

## Reconstruction and temporal ordering

A big chunk of the work was reconstructing the conversations so they were in the right order.

Cursor v2 stores Composer and Agent chats in a different place than old chat mode. The Composer bubbles live in:

~~~
~/Library/Application Support/Cursor/User/globalStorage/state.vscdb
Table: cursorDiskKV
Keys: composerData:{uuid} and bubbleId:{composer-id}:{bubble-id}

~~~

Those bubbles include timestamps. I sorted messages by timestamp so the conversation order is stable before anything else happens.

For Claude, I grouped raw events by sessionId, dropped sidechain messages for SFT, and chunked long sessions into windows so they fit context limits. This gives me real multi turn conversations, not random message shards.

## Dedup that survives time

After reconstruction and ordering, I deduplicate by a stable trace id derived from the conversation content. That catches duplicates across sources and across time.

Numbers from the build:

- Duplicates skipped: 13,634
- Sessions rebuilt from raw Claude logs: 4,747
- Chunks written from those sessions: 5,007

This matters because the raw logs contain the same thread in multiple places. If you dedup before ordering, the hashes are unstable. Order first, then dedup.

## PII scan and masking

I did not trust myself to manually review 100k conversations. Everything goes through a scan and masking step first.

What I scan for:

- API keys and tokens
- Private keys
- Database URLs
- Local paths like /Users/sero

Then I apply a redaction policy that masks patterns and rewrites local paths to/<ABS>/.

From the final SFT run:

- 95,561 conversations quarantined
- High risk markers quarantined: 79
- Path rewrites: 75,127
- Pattern replacements included GitHub tokens, HF tokens, OpenAI keys, Anthropic keys, Slack tokens

Prepared outputs are scanned again and come back clean with 0 hits. The quarantine file only stores row pointers and reasons. No raw text leaks.

## Did I train on single pairs

No. The SFT dataset uses full multi turn conversations. Some sources are only pairs, but most are not. The final SFT output has:

- Average 8.4 messages per conversation
- p50 of 2 messages, p90 of 19

The model sees real back and forth, not just single question and answer pairs.

## The SFT dataset

Final split:

- Train: 11,711
- Validation: 107
- Test: 123

Domain mix from samples:

- Solidity and Web3 around 35%
- TypeScript and Node around 30%
- Python around 20%
- SQL around 10%
- Other around 5%

This matches what I actually work on.

## SFT training config

I trained a LoRA adapter on top of NousCoder 14B.

- QLoRA 4 bit
- LoRA rank 64, alpha 128, dropout 0.05
- Target modules: q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- Batch size 2, grad accumulation 8
- Max length 4096, packing enabled
- Learning rate 2e-5, cosine schedule
- 3 epochs target, timed out at 2.52

Infra:

- HuggingFace Jobs
- A100 80GB
- 18 hours
- Cost around $47

## Results

- Final loss: 0.685
- Token accuracy: 81.6%
- Total tokens: 51.75M

The checkpoint still works.

## What it learned

The model absorbed my patterns:

- OpenZeppelin imports (35% of training data was Solidity)
- ethers.js v6 (not v5, because I debugged the differences)
- Type annotations in TypeScript
- Error handling that actually catches things
- Concise explanations followed by code blocks

First test: "Write a Solidity ERC20 token"

It generated valid code with OpenZeppelin. Used the correct import paths. Included permit functionality (EIP-2612) without being asked. The model remembered my style better than I do.

## The Artifacts

Three problems emerged immediately:

- Besides measuring loss on the training data, how am I suppose to measure the model's performance on unseen data?
- Is the dataset representative of what I want to do moving forward?
- If I have been incentivizing the model to learn my style, how do I ensure it doesn't overfit?

## Deploying to production

The model lives on my linux serverhttps://github.com/0xSero/vllm-studio. It is serving at 100+ tokens/second. I am using it in opencode, and vllm-studio. It suggests code that looks like code I would write but lacks the flexibility of a larger model.

## DPO pairs and alignment plan

I prepared preference pairs for DPO. These are mined from Claude sidechains where the draft response becomes rejected and the final response becomes chosen.

- Total pairs: 4,532
- Train: 4,443
- Validation: 46
- Test: 43

## Where the model lives

Model card and files:

- https://huggingface.co/0xSero/sero-nouscoder-14b-sft

It is a LoRA adapter, not a merged model. I serve it via vLLM with a base model behind the API.

## How I use it

I run it through an OpenAI compatible endpoint:

~~~
curl https://api.homelabai.org/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <YOUR_TOKEN>" \
  -d '{
    "model": "sero-nouscoder",
    "messages": [{"role": "user", "content": "Write a Solidity ERC20 token"}],
    "max_tokens": 500,
    "temperature": 0.7
  }'

~~~

## The economics

This is where it gets interesting:

Total project cost:47Remainingbudget:47 Remaining budget:47Remainingbudget:103 (started with $150) Time investment: 2 days data prep, 18 hours training Result: A coding assistant that knows my preferences

Compare to ChatGPT Pro at $20/month. This cost me 2.3 months of subscription, but I own the model. No rate limits. No context windows shared with millions. Actual privacy.

## What I am thinking next

- Can this scale to a distributed set of training datasets sources from OSS developers?
- What size model would make this actually useful on a day to day basis as a daily driver?
- How can I better structure the dataset to not just show it what i've done but also push it towards better overall behaviour?
- I need to learn more about RL, SFT, etc..

## The verdict

This project changed my mental model of AI. I thought fine tuning required PhDs and data centers. Reality: one person, one weekend, $47.

The model is not perfect. It shows training artifacts. But it codes like me, understands my project patterns, and runs on hardware I control.

---

Continued from Part 1: How I actually work with AI

Training: $47, 18 hours on A100, 51.75M tokens. Final loss: 0.685, accuracy: 81.6%.

---

## Post 3: AI-driven NFT marketplace

- **URL**: https://www.sybilsolutions.ai/blog/AI-and-marketing
- **Date**: 2022-08-28
- **Description**: What if we could use AI and NFTs to create, market, and own our products
- **Tags**: NFTs, Marketing, AI, nextJS

### Full Content (Verbatim)

## A place for artist to create and grow together.

Marketing is the key to success of any product, but it's often the most difficult part of growing a business. With over5 billionpeople using the internet there's a lot of opportunity to grow, but there's also competition for these opportunities. A study showed that information paired with an image improved people's retention of that content from 10% after 3 days, up to 65%.Source

Our platform allows writers, content creators, and media users to market themselves with the assistance of text-to-image AI technology. Creators Can upload or link their content and sponsor platform users to generate unique artwork for marketing after viewing said content. To ensure that creators and platform users are both incentivized, the winners artwork will be minted to an NFT collection, giving recognition and a percentage of earnings to both the sponsors and the users.

We can categorize our users as:

1. Creators/Sponsors
2. AI artist/platform users

### AI as a tool to visualize content and boost growth.

Unique art is eye-catching, exciting, and memorable, but it's also difficult to create for most people. This puts businesses and creators who rely on video, audio and written text at a disadvantage. It's been well recorded how important banner art is for building and engaging an audience.

We can leverage image-generating AI to create captivating, unique and impactful art using text collected from content and user-provided information. Those without artistic background can now easily sponsor the creation of original art relevant to their needs for marketing, and adding a special twist to their work.

Usecases for the generated art include:

- Profile pictures and banners
- Book and cover art
- Badges for rewarding community
- Music album covers
- Social media marketing
- Thumbnails, channel art, personas
- Music videos
- Memes

### Using NFTs to give artists and sponsors the recognition they deserve

Most artists would argue that they are not given the right compensation and recognition for their art. The internet has been known to use content without giving credit, often leaving the creators with not much to show for their work while the art has millions of views and downloads. NFTs help mitigate this problem, it is a standard that most tech giants are now adopting and incorporating into their platforms.

All winner collections will be minted onto the blockchain and viewable in our application. The creators will be credited and they will earn a royalty fee for the legal use and sale of their art. While sponsors get the NFT to prove ownership and provide protection for the content they paid to have created.

Usecases for the NFTs include:

- Proof of work token for platform users
- A portfolio of art generated for users
- Content protection for both sponsors and users
- A marketing strategy
- Community building and token gating
- Censorship resistant art

### Why?

We want to give everyone the opportunity to create captivating and useful content regardless of their artistic background. To own the content they create, and to get the credit they deserve for their work.

Find my links through:https://www.serotonindesigns.com

---

## Post 4: AI Workflows as an Assembly Line

- **URL**: https://www.sybilsolutions.ai/blog/AI-workflows
- **Date**: 2024-10-10
- **Description**: How can we automate the repetitive parts of our day to day work?
- **Tags**: AI

### Full Content (Verbatim)

# AI / Web3 - DevRel Workflow Automation: Unlocking Efficiency in Developer Relations

In an open source ecosystems,Developer Relations (DevRel)has emerged as a critical function for growing and nurturing communities. But as these ecosystems expand in complexity, managing developer engagement, providing timely support, and creating consistent technical content becomes more challenging.

This challenge is compounded by the fact that more users, adopters, and builders doesn't necessarily equal more stable revenue. Despite that, your organisation will be expected to answer questions, update docs, and trouble shoot in a timely manner.

Some organisations are pressured into expanding their teams, and hiring more people to accomodate the growth, this unfortunately causes tension when revenue drops and downsizes are needed.

In the last two years we've seen anincreasing adoption of AIto assist dev rels in keeping up with the ever growing demand and list of tasks, we’ll explore how AI-powered automation is redefining DevRel operations across Web3, and how we've seen teams leverage this to boost efficiency, enhance developer experience, and scale engagement effortlessly.

## 1. What is Workflow Automation?

The question of what is a workflow maps to the question: "What is an assembly line?"

> An assembly line is a production process that breaks the manufacture of a good into steps that are completed in a pre-defined sequence.

A workflow is an assembly line producing a specific outcome,AI agents are responsible for a single task within this workflow.These tasks range from answering common support questions to automating the production and maintenance of technical content.

Below is an example of a Q&A workflow:

~~~
flowchart TD
    A[User Question] -->|User submits query| Q1(Q&A Agent)
    Q1 -->|Processes question, retrieves data| B(Loader Agent)
    B -->|Loads relevant data| C(Discord/Slack)
    Q1 -->|Checks for personal data| D(PII Obfuscation Agent)
    Q1 -->|Analyzes tone and context| E(Sentiment Agent)
    D -->|Masks sensitive information| C
    E -->|Adjusts response tone| C
    C -->|Sends response| F[Response Sent]

~~~

Key components of a DevRel Workflow Automation system include:

- Loader Agents:Agents which are configured to consume information specific to your organisation, allowing the conversational agents to respond with accurate, and relevant data
- Conversational Agents:Agents which are configured to identify and respond to common queries.
- Content generation:AI tools that create, update, or recommend technical documentation and blog content.
- Feedback loops:Automated systems to collect and analyze developer feedback, providing real-time insights into community sentiment and product needs.
- Monitoring and analytics:Dashboards that track developer engagement and measure the effectiveness of documentation or community interactions.

This shift towards automation empowers devrels to be more agile, responsive, and scalable-while still maintaining a human touch.

## 2. Why Is Workflow Automation Essential for DevRels?

As projects and ecosysems grow, developer communities become more diverse and dispersed. This introduces new challenges for managing developer interactions, addressing support needs, and maintaining up-to-date resources. Here's why automation is becoming a necessity:

### Scaling Support for a Global Developer Base

Web3 and AI projects often attract developers from around the globe, creating a 24/7 need for support. With AI-driven automation, DevRel teams can offer around-the-clock assistance, resolving common queries with chatbots or pre-built FAQs. This ensures developers receive the support they need without overwhelming human teams.

### Keeping Documentation Up to Date

Documentation is a cornerstone of any successful projects, however as a project grows docs will become less relevant. A combination or product growth, internal changes, and community growth requires your organisation allocate significant resources in upkeeping your documentation.

### Developer Onboarding

With product growth, communities follows suit. There will be an inflow of developers and potential customers seeking to onboard onto the codebase/project.

Working through thelogistics of offering human supportand structuring documentation to accomodate for onboarding can be tough, a global audience means the need for multi-lingual support, online team members at varying timezones, and many hours that humans can't keep up with.

### Optimizing Community Feedback and Iteration

Collecting and analyzing developer feedback can be time-intensive, but it’s crucial for improving the developer experience. Automated systems cangather feedback in real-time, flagging common pain points, feature requests, or issues with the documentation. DevRel teams can use these insights to make data-driven decisions, improving community engagement and retention.

## 3. How to Automate Your DevRel Workflows

Transitioning to Workflow Automation is all about setting up clear, reproducible processes. Not only can you significantly boost your devrels impact, but you'll be able to gain insight into the workings of your organisation.

Here are the steps we'll use:

- Identify High-Volume, Repetitive Tasks
- Document the steps involved in fulfilling these tasks
- Identify the KPIs related to these tasks
- Introduce automations that eliminate the most tedious and predictible elements
- Automate Feedback Loops
- Set Up Monitoring and Analytics

Automating systems can save DevRel teams countless hours of manual tracking. Use AI-powered analytics tools to monitor developer engagement across various touchpoints-whether that’s in your documentation, on social media, or within community forums. Track key metrics such as content performance, issue resolution times, and developer satisfaction scores to make informed decisions.

## 4. Automation Challenges

It's clear that AI is changing the work landscape, but it still comes with significant challenges thatprevent most companies for taking full advantage of these tools.Most technical individuals can use ChatGPT, Gemini, and Claude toboost their personal productivity, but to truly leverage AI to it's full potential requires more than a chat bot.

- Scaling AI and putting it into production environments is costly, and requires significant optimisations and constant monitoring
- Currently AI models have a limited training sets, which cannot be customised to fit your specific needs without fine tuning, you can train a small model or build a RAG, both approaches come with pros-cons and time-cost considerations.
- The sourcing and categorisation of data needs to be close to real-time, which as of now requires custom coded scrapers and integrations.
- Chatbot responses can range from uninformed, to unhelpful, to down-right misleading, without proper accuracy controls relying on AI data can lead to a lot of wasted time.
- Content generation is only a piece of the puzzle, to automate an entire workflow we need many agents which require a lot of custom coding as of now.

Over the last year we've tackled many of these challenges which have been incorporated into the new Katara stack which includes a data enrichment layer combined with vector search and a growing library of AI-enabled agents that can be combined to tackle exceedingly complex workflows.

---

## Post 5: Employment Scams - Deep Dive

- **URL**: https://www.sybilsolutions.ai/blog/Modern-day-scams
- **Date**: 2024-04-03
- **Description**: Investigating a modern day employment scam
- **Tags**: Privacy, Security, Blockchain, Cryptocurrency

### Full Content (Verbatim)

## Modern scams:

Where there is money, there are thieves trying to steal it. The internet has exposed people to an infinite variations of scams, and while we might think we are "too smart to get scammed", or "not dumb enough to fall for something so obvious" we can all be victims. You could be opening awork email, and compromise your company. You can wake up to a scary looking SMS, and log in to your "bank" to fix the issue, only to give away your credentials to someone from across the world.

### Phishing scams:

It is well known that unsophisticated scammers and hackers purposefully spam crazy offers of 1000x returns, filled with grammatical errors to thousands of people a day. Think the Nigerian prince scam, the scams are formatted in a way to repel technically savvy, and well off people. The goal is to catch an older crowd, with unreasonable expectations, and desperation.

These scammers typically rely on convincing the victim to give access to valuable accounts, or send funds directly willingly. Early in 2023, my friend had made a twitter/x post about his birthday coming soon. I know him IRL he's a huge BTC maxi, so I commented I'd send him some BTC. That day a twitter account was created, a blue checkmark purchased, and this fake account began retweeting everything on my friend's timeline. On the day of my friend's birthday, he had sent me a DM with his BTC address, I had recently woken up, and after a quick glance at his profile, I sent him 100$ in BTC. Turns out, it's a scammer.

## Employment scams:

Some scams are more sophisticated, and insidious. They require proper identification of prospects, story arcs, reasonable returns, and technical tooling to take a lot, from a few people. These scams rely on looking aslegit as possible, they have well designed websites, proper marketing, social media accounts with blue checkmarks, a high follower count, and seemingly decent social validation. Today we will be breaking down thesocial, and technical implementations of employment scams in a Web3 context. Here the scammerslure you into installing executables, or signing transactions, your seemingly innocent action will trigger a series of event in which your entire portfolio will be drained, and sent to the scammers.

### Part 1: Prospect identification

In Web3, (almost) all transactions are public, a lot of people own ENS domains and share them on their socials, ENS assigns a human readable text to ethereum addresses.

#### Example of an ENS:

This will allow a malicious actor to follow my ENS and view all my holdings,if I have a cetain amount of funds, say more than 10k USD I will be marked as a target.An organised operation of scammers will find dozens, of targets, and mark them down in a spreadsheet somewhere. Along with their social usernames, professions, and any information that could help in establishing a relationship with the target.

### Part 2: Human connection as bait

Once a list of prospects is established, a group of chatters will begin to send friend requests, follow, and DM the targets. The goal is to create a connection, establish a friendship.

#### Example of DMs from scammer:

0xEddy (on the left) began messaging with a target, doing introductions, and bonding with the lead. Once a connection is built, a job opportunity will be offered, a few more individuals will jump in, have calls, and convince the prospect this is a valid job opportunity.

### Step 3: Do you want the job?

Now that the stage is ready, and the victim is convinced this will lead to a job, the scammers will connect the last piece of the puzzle: "Install our software/connect to our site/clone and run this repository to familiarize yourself with our workspace, and prove you can do this job"

At this point, the victim has 1 of 2 choices, take the bait for the work opportunity, or reject it which lead to hours of wasted time, and harsh aggressive treatment from the scammers.

### Step 4: Get drained

In the case of SpectraChat/SpectraSocial:

#### Installation:

1. The malware is a .exe installer which will install a folder of c++ files to the local machine in a folder called /Spectra.
2. The malware will also copy the installer, rename it, and move it into some random folder, so that when you delete it, it will reinstall itself.
3. Once installed, it will error out "C++ Drivers missing", this is meant as a signal for the hackers, as it will push you to message them.
4. Because you're installing an installer, and not the malware itself, Windows defender fails to alert you that there is an issue.

#### Behaviours:

1. The software will hijack your browser, detect your browser plugins crypto wallets, and either:Allow the scammers to control your browser remotely (in this case this is the most likely exploit)It will run automated commands to your browser to sell and transfer all the assets out of your wallets.
2. Additionally, this malware hijacks copy/paste mechanismswithinthe browser, when you try to copy a hex string starting with 0x, it will replace it with the scammers wallet. This issue wasn't occuring outside the browser, which hints towards this whole malware chromium browsers specifically.This is done to prevent the victim from stopping the attack by transferring whatever remains to another walletIt is done to continue leeching funds off the client, in the case that they don't realise their browser is still hijacked. In fact the wallet address pasted by the malware had more incoming transfers then the wallets used by the drainer.
3. Deleting the software seemed very difficult, as it would reinstall itself, and the fact that windows relies on the apps having a provided uninstaller.

#### What this malware doesn't do:

1. As an expirement we left a seed phrase, and secret key in a note on the desktop, the wallet had a decent bit of money, and we were monitoring to see if it would be taken.The malware had not picked up on this, leading us to believe that the malware doesn't take control of the host device, just the browser.
2. Escape virtual machines: we installed the executable on a linux VM, and ran it with Wine. It didn't seem to do anything, and it never effected the host machine's Windows OS
3. Infect the network: we monitored the network traffic, no other machines were affected, and there was not suspicious activity.

### Conclusion

Despite the sophisticated tactics employed by scammers, there are steps individuals can take to protect themselves:

- Avoid installing unknown executable files.
- Exercise caution and skepticism when presented with enticing offers.
- Implement security measures such as multi-factor authentication.
- Verify the legitimacy of job opportunities and websites.

By staying vigilant and informed, individuals can mitigate the risks posed by modern scams and protect their financial assets. I want to extend my gratitude toAlexfor bravely sharing his experience, highlighting the importance of awareness and caution in today's digital landscape. If more people shared their experiences, we would realize that anyone can fall victim to scams, emphasizing the need for collective vigilance.

If you want to read more about this scam, I can't recommend a better breakdown than:Alex's blog post

---

## Post 6: AI-Assisted Coding: What Actually Works

- **URL**: https://www.sybilsolutions.ai/blog/ai-assisted-coding-experience
- **Date**: 2024-12-23
- **Description**: Months of optimizing my workflow with Cursor and Claude Code. The techniques that actually multiply productivity.
- **Tags**: AI, Developer Tools, Productivity, Claude, Cursor

### Full Content (Verbatim)

AI-assisted coding changed how I build software. After months optimizing my workflow with Cursor and Claude Code, here are the techniques that actually multiply productivity without turning you into a prompt monkey.

## Context Windows Matter

Understanding context windows is the difference between useful AI and garbage output.

Cursor's Claude 3.7 Sonnet gives you about 48K tokens in standard mode. Max mode bumps that to 200K (costs extra, $0.05 per prompt and tool call).

Real numbers:

- 200-line React component: ~1,500 tokens
- Python file same length: ~1,700 tokens

You can fit multiple files in standard context, but be strategic. The golden rule: keep files under 400 lines. Break larger files into modules with clear responsibilities. Complex projects, aim for under 1k lines per file.

## Smart Context Management

The technique that changed everything: strategic context management.

Close all editor tabs. Open only the relevant files. Add them to context using slash (/) menu and "Reference Open Editors". The AI gets exactly what it needs, nothing more.

For large codebases, create a/docs/aifolder with:

- Architecture approach
- Coding standards
- Component patterns
- State management philosophy
- API conventions
- Testing strategy

The AI references these automatically. Consistency across your entire codebase without repeating yourself.

## .cursor/rules

Underutilized feature. The.cursor/rulesfile gives project-specific instructions that Cursor follows when generating code.

Example for React projects:

~~~
UI and Styling:
- Use Shadcn UI and Tailwind for components and styling
- Implement mobile-first responsive design
- Prefer function components over class components
- Use CSS modules for component-specific styles

Performance:
- Minimize 'use client' directives
- Favor React Server Components
- Wrap client components in Suspense with fallback
- Use dynamic loading for non-critical components
- Optimize images with next/image

Architecture:
- Use the repository pattern for data access
- Implement clean architecture with clear separation of concerns
- Keep components under 150 lines
- Extract complex logic to custom hooks

~~~

Your patterns, applied consistently, without repeating instructions every prompt.

## @Docs Feature

Cursor's @Docs lets you integrate external documentation directly into AI interactions. No more tab-switching for reference material.

Provide a documentation link, Cursor indexes it, reference it with @Doc or the document name in prompts.

Setup:

1. Type @ in Chat or Composer, select "Docs," enter URL, name it (e.g., "TensorFlow")
2. Reference with @Name syntax: "Implement a custom loss function using @TensorFlow documentation"
3. Manage under Settings > Features > Docs. Auto re-indexes as docs change.

Built-in docs for popular libraries via @LibraryName (@React, @Python). Extend with specialized libraries, version-specific docs, internal API docs.

## Agent Mode

Cursor Agent mode (cmd + Ior dropdown) is the most powerful feature. It loops Claude until the goal is achieved: searching files, gathering context, running tests, installing packages.

For maximum efficiency:

- Enable "Yolo mode" in settings. Cursor runs tests without confirmation prompts.
- Create new agent windows periodically. Long conversations cause Claude to forget earlier instructions.
- Use "think hard" to trigger extended thinking on complex problems.

## Claude Code: Command Line

Claude Code brings similar capabilities to the terminal. It understands project context and takes real actions. No manual file context needed.

Graduated thinking triggers allocate more thinking budget, letting Claude evaluate alternatives before acting.

For long sessions, use/clearfrequently between tasks. Context windows get cluttered with irrelevant conversation, file contents, commands.

## What I Built With This

These tools powered most of my recent projects:

AI Data Extraction(121 stars): Extract personal data from Cursor, Codex, Claude Code, Windsurf, Trae. Built the core extraction logic manually, used AI for file parsing and edge cases.

Open Orchestra(96 stars): Multi-agent coordination. Designed the architecture myself, let AI handle boilerplate and tests.

Azul(68 stars): Terminal web browser with AI. Manual design for the browser core, AI for rendering and interface polish.

mem-layer(55 stars): Graph database memory organization for AI. Manually designed the graph structure, AI generated CRUD operations.

minimax-m2-proxy(33 stars): Proxy enabling interleaved thinking and tool calls. Critical protocol logic done by hand, AI handled HTTP scaffolding.

codex-local(29 stars): Modified Codex CLI for local LLMs. Forked and modified manually, AI helped with configuration options.

The pattern: design the hard parts yourself, let AI handle the repetitive stuff.

## Architecture Patterns That Work

Certain patterns work exceptionally well with AI:

Reflection Pattern:AI generates a solution, then reviews and critiques its own code, refining based on self-evaluation.

Tool Use Pattern:AI interacts with external tools. Databases, web searches, function execution.

Planning Pattern:AI creates a detailed plan before implementation. Provide feedback before coding starts.

Multiagent Pattern:Use "subagents" to verify details or investigate questions while preserving main context.

More autonomous assistance, higher quality results.

## TDD with AI

AI excels at generating tests. TDD becomes powerful:

1. AI generates test cases for your feature
2. Implement the tests
3. AI writes code that passes the tests
4. Integrate and run tests
5. AI fixes failing tests
6. Finalize

Claude Code is especially effective for TDD, debugging complex issues, large-scale refactoring.

## Project Structure

Organize files for AI comprehension:

- Include PRD (Product Requirements Document) as Markdown in the repo
- Clear, descriptive file and directory names
- Keep related files close in directory structure
- Use.cursorignorefor large files AI should skip

## Preserving Your Skills

Valid concern: skill atrophy from AI tools. My approach:

Manual coding sessions:Dedicated time without AI. Focus on algorithms, data structures, system design.

Core functionality by hand:Security, performance, business logic. Written by you.

Review everything:Understand every line before accepting. Ask AI to explain complex sections. Modify manually to ensure understanding.

Regular challenges:Solve coding problems without AI periodically.

Track progress:Baseline your skills, identify areas for improvement, create practice plans.

## Workflow by Project Type

### Frontend Development

- Manually design component hierarchy
- AI generates project scaffold
- AI handles boilerplate components
- Manual effort on complex interactions and state
- Manually design API integrations, AI implements calls
- AI generates test cases, manually add edge cases

### Backend API Development

- Manually design data models and relationships
- AI generates OpenAPI/Swagger specs
- Alternate between AI-generated code and manual implementation
- Manually implement validation logic, AI generates tests
- AI generates comprehensive API documentation

### Refactoring

- Claude Code excels here
- Point it at legacy code, describe target architecture
- Review changes carefully before committing

## The Balance

As these tools evolve, successful developers will balance AI assistance with human judgment. AI enhances capabilities. It doesn't replace them.

Design the architecture. Understand the code. Let AI handle the tedious parts. Ship faster without becoming dependent.

---

## Post 7: Choosing a crypto-wallet for your Web3 journey. (Part 1) -Understanding wallets

- **URL**: https://www.sybilsolutions.ai/blog/choosing-a-crypto-wallet-for-your-web3-journey
- **Date**: 2022-07-24
- **Description**: Cryptocurrency wallets allow anyone, from anywhere in the world to interact with the world financial system.
- **Tags**: Web3, Cryptocurrency, Wallets, Blockchain, Metamask

### Full Content (Verbatim)

## What exactly is a cryptocurrency wallet and how does it work?

Interacting with web3 and blockchain technology typically requires you to have a wallet. In this series we will learn about the different kinds of wallets to understand the use-cases of each one. But we can't learn about the different types without first gaining some insight into what exactly is a crypto-wallet

A cryptocurrency wallet is created by randomly generating a number, then using a set of instructions to encrypt that number. The result of the encryption is what is called a private-key. As you might have guessed, private-keys are not to be shared! What you can share is your public key, generated by running another algorithm on your private key.

Private keys prove your ownership of your funds and assets, just like a password proves that you own your social media and bank accounts. Anyone asking you to share your private key is attempting to scam you. Keep this in mind because scams are unfortunately quite common with new technology blockchain isn't any different.

Think of public keys as, like a mailbox with your home address, it allows anyone with the key to locate you and send you information.Public keys are also traditionally used in asymmetric cryptography. People would share the key with an individual that will use it to encrypt messages intended for the key owner. The only way to read messages encrypted with a public key is by using the private key to decrypt the information.

A cryptocurrency wallet will then be at the center of everything you do in Web-3, connecting you to the world and providing you with the means to send, receive, trade, and own digital property from anywhere. This technology democratizes and decentralizes finance, lowering the barrier of entry to the flow of money to memorizing a set of 24 characters or words. Finding and creating a wallet that fits your needs is the first step in gaining financial and digital freedom.In the next post, we will discuss the different types of wallets. So that by the end of this series you can confidently choose your wallet to begin your web-3 journey.

Read part 2 to learn about the different wallets, and which one could be right for you:Part 2: Choosing a type of wallet

---

## Post 8: Employment Red Flags

- **URL**: https://www.sybilsolutions.ai/blog/employment-red-flags
- **Date**: 2022-10-26
- **Description**: Getting a job is not easy, and bad employers make this process even more difficult.git
- **Tags**: Guide, Privacy, Security, Content Creators

### Full Content (Verbatim)

## How do we find a good job?

Regardless of how early or far into a career you are, this is a question you will have to ask yourself whenever you enter into the job market. Your work relationships will be some of the most important in your life. You will spend a big chunk of your life interacting with your employer and co-workers. You will be relying on your job to support your family, grow your skills and plan your future.

Working a bad job will take more from you than it will give. It might seem like asafe choice to take the first offer you get, or settle for a sketchy positionwhen you are hunting for a new position. Research however shows otherwise.

Let's take a look at some of the concequences of taking a bad job:Research references

- Increase in mental health symptoms such as anxiety and depression.
- Less time to spend on family, hobbies, and self improvement.
- Increase in stress and burdens on social relationships.
- Difficulty finding quality employment later on.
- Decrease in quality and quantity of sleep.
- Stagnation in growth of skills.

If you've worked in a dead end job for any amount of time you will recognise the damage it can do to all aspects of your life.

## Red Flags and how to avoid them.

On your job hunt you will run into a lot of people who want tobenefit from your situation even if it hurts you. Wether it be recruiters from LinkedIn, connections you've made at events, or even well known companies- Watch out for these signs:

- NDAs:

Non disclosure agreements are very common these days, but are they necessary? In some situations it'd make sense like if you're working directly with government or on large scale projects. But a lot of the time NDAs are weaponised to make it more difficult for workers to share their experiences. The fear of prosecution and law suits can deter people from seeking help when they're wronged.

- Non-compete contracts:

If you work as a freelancer, or contractor you should look close at the contracts you sign, especially if they contain non-compete clauses. Malicious employers will often make their workers sign contracts that prevent them from working in whole industries.

Example: I am a blockchain engineer, an employer had attempted to make me sign a contract that would prevent me from working in my industry for a year after the termination of a 3 month deal! If I had signed that I would open my self up to a lawsuit when working in my field!

- Irregular payment structures:

Withholding a percentage of your first check, late payments, and delays should not be tolerated. If this is brought up or if it happens even once then you should stop work immediately to cut your losses. Bad employers will often use late payments to manipulate their workers and test their limits.

An example from my life:One of the jobs I've had delayed due payments for 2 weeks, I stopped working the day the delays began.While chasing down the employer for the payment I got in touch with one of the workers who's been working without pay for over 2 months! This worker had signed an NDA, preventing him from seeking help. He kept working because he had no other options.

- Excessive demands and unrealistic expectations:

Some employers either don't understand or don't care about the efforts involved in doing quality work. They will expect you to work unrealistic hours, they will force you to be available always on demand. They will underpay you and increase the scope of required work every chance they get.

An example from my life:"Our product can't have less features then salesforce."I once took a contract building a Public Private relations app that aided employers in identifying the needs of their workers. The irony is that the client didn't care about the needs of their workers. Infact they required the 2 person team to build a Salesforce competitor. The scope got unberable and caused me immense stress for weeks.

Pushy, unrealistic employers and clients will waste your time, and damage your reputation and self esteem.

## Conclusions:

You are valuable, your time is important, there will always be a better job waiting for you. Don't settle for employers that don't care about you.

---

## Post 9: MEV Bots and the Dark Forest

- **URL**: https://www.sybilsolutions.ai/blog/mev-bots-and-dark-forests
- **Date**: 2024-12-23
- **Description**: What I learned building arbitrage bots and discovering just how deep the MEV rabbit hole goes.
- **Tags**: Smart Contracts, Ethereum, Security, MEV

### Full Content (Verbatim)

I've been building bots to arbitrage profitable function calls on smart contracts. I knew MEV existed-I've seen their addresses in action dozens of times.

What I didn't know is the depth of their operations, and how shallow my understanding of what they exploit really was.

## How Bots Compete

It's fascinating how bots compete against each other to claim profitable transactions in a public mempool.

They do this by increasing the fee paid per unit of gas:

- Reactively- checking what the last bot bid and bidding more
- Blindly- increasing the bid by a static amount every X seconds

Over time, this drives fees so high the transaction becomes unprofitable. The miner wins, everyone else loses.

So instead, with no formal agreements, bots begin to bid the minimum extra amount the network allows. Leaving it to chance. Reducing gas fees paid to miners.

Game theory in action.

## Sophistication Levels

Looking at advanced bots like0xC0ffeEBABE5D496B2DDE509f9fa189C25cF29671(c0ffeebabe.eth) reveals a different level of discipline.

These sophisticated MEV hunters don't just use simple frontrunning. They employ complex smart contracts with:

- Multi-layered obfuscation techniques
- Transient storage to hide strategy details
- Dynamic code execution paths
- Complex gatekeeping mechanisms
- WETH manipulation capabilities
- Miner incentivization for better transaction ordering

The level of sophistication is mind-blowing. Examining their bytecode reveals handcrafted assembly specifically built to avoid detection, competition, and disruption.

## Flashbots Isn't Enough

While improving my bots, I reached for Flashbots-a promising solution to MEV extraction. But it doesn't prevent it completely.

These same bots monitor not just public mempools, but mined blocks and all transactions within.

This allows bots to re-simulate transactions and uncover patterns over time. I've seen this myself when a profitable transaction from over a day before was copied and resubmitted once found to be profitable again.

The machine learning angle is interesting. Advanced MEV operators use pattern recognition to build predictive models that anticipate profitable opportunities before they even appear in the mempool.

## No Easy Defenses

Basic protection mechanisms like token ownership requirements fail because of addresses like0x3d782C0C69101358a8267Ba116c86726fDF35F91, which take flashloans of tokens to bypass these checks.

This challenges all contracts implementing profitable open transaction calls. TheEthereum is a Dark Forestarticle by Paradigm outlines this well using CryptoKitties as an example.

## Solutions: Fight Fire with Fire

One approach: disallow this behavior at the protocol level. But given humans can't build perfect systems, other exploits will be found and consolidated.

Another: make it simply unprofitable.

These bots are dangerous but blind. Their operators analyze mistakes over time, but that's wasted effort.

One well-crafted script can confuse thousands of bots for days. It's reasonable to build a system where blind bots can't profit in a sea of millions of unprofitable-looking-but-profitable transactions. Only specialized, knowledge-driven bots will win.

## Practical Defenses for Contract Designers

Smart contract designers need to implement:

- Time-locked execution mechanisms- delay between intent and execution
- Commit-reveal patterns- hide transaction details until execution
- Strategic honeypot transactions- poison the well for blind bots
- Unpredictable execution paths- make simulation expensive or unreliable

The MEV landscape is evolving quickly. Understanding these predators is essential to designing systems that maintain economic integrity while discouraging exploitative extraction.

---

## Resources

For more on MEV and baiting bots:

- Baiting MEV Bots: UniV2 Token Trapby degatchi
- Ethereum is a Dark Forestby Dan Robinson & Georgios Konstantopoulos
- Escaping the Dark Forestby samczsun
- Flashbots Researchby Phil Daian and team
- MEV-Exploreby Flashbots
- Scott Bigelow's MEV Example- great walkthrough

Still building. Still learning. The dark forest is deeper than I thought.

---

## Post 10: How to remove unwanted content from the web.

- **URL**: https://www.sybilsolutions.ai/blog/remove-unwanted-content
- **Date**: 2022-10-16
- **Description**: A guide to removing unnwanted content and information of yourself from the web.
- **Tags**: Guide, Privacy, Security, Content Creators

### Full Content (Verbatim)

## Your content and personal information is very valuable, it is important to learn how to keep it safe.

Leaked information, copyright infringements and identity theft are issues that online creators, developer, and artists know too well.But this is a problem anybody could face at some point in their lives or careers- In this guide I will be discussing possible ways toremoveyour personal information and/or protect your content from being used without your consent.

### 1 - Social Media:

We all use social media, which is why it's the first point at which your information can bestolenand used against your will. In fact, theOSINT FRAMEWORK, an information gathering tool for hackers and law enforcementcan be used by anyone to gather and use information collected from your social media.

Example of information that can be collected from your social accounts:

Example:https://osintframework.com/

- Watermark all your content.(Preferably somewhere that would be difficult to crop out.)
- Limited postingpersonal or identifiableinformation online. (Adresses, real names, pet names, numbers etc..)
- Use your social media reporting system, it is important tofollow throughwith reports until they are resolved.
- Report identity theft through platforms Email directly, if the platform is reputable you can send a written request with information they request and infringing account will be taken down. If you are having issues with this contact me:https://x.com/0xSero

Do not directly click on links sent by people you don't know, a simple click is all someone needs to get ahold of your IP address.

### 2- DMCA for copyright infringement:

If you've come across websites, apps or content that directly uses your personal information or content without your consent there are ways to get it removed. All websites that publish content are mandated to have a DCMA Contact form in the footer of their websites.

- A list of free DMCA takedown notice templates:https://www.template.net/business/notice-templates/dmca-notice-template/

How to request content takedown:

- 1 - Use this Template takedown notice, add in your information.
- 2 - Find the DMCA/COPYRIGHT infringement contact form. (This might be difficult but it's definitely there).
- 3 - Send it and wait for a response. - 0 to 3 weeks response time

If you own the content it will be taken down the majority of the time, but if not then don't worry as we still have more approaches to take.

### 3- GDPR Takedown requests:

For the European and British readers, you have an additional solution which ensures you can remain private online.

In European nations there is a lawhttps://gdpr.eu/what-is-gdpr/which prevents anyone from using your personal information without your consent. Any website or app which holds records of you, or content you've created is mandated to provide you a copy of that information as well as delete any records they have by international law. These laws apply everywhere, regardless of whether the websites are European. To use this approach follow the steps bellow.

- 1 - You can search the website for the GDPR notice link that they are mandated to have. If you don't find it a contact form or email is enough.
- 2 - Fill out a copy of this form and email it to the website.https://gdpr.eu/right-to-erasure-request-form/
- 3 - Follow up, the maximum time they can put it off is 4 weeks, i'd suggest emailing weekly.
- 4 - If your content is not taken down follow the gdpr website's instructions.

For more on GDPR:https://termly.io/resources/articles/gdpr-for-dummies/

### Conclusions:

If you get your information stolen, or doxxed don't panic. There are tools to navigate finding solutions to these problems.Remember that your privacy is something worth fighting for.If you need help feel free to contact me on:

https://serotonindesigns.com

---

## Post 11: The Benefits Of Scrum

- **URL**: https://www.sybilsolutions.ai/blog/the-benefits-of-scrum
- **Date**: 2022-07-08
- **Description**: Scrum is an agile framework made to help bring software developers and project managers together.
- **Tags**: workflow, development, agile

### Full Content (Verbatim)

## Time is precious

In our industry staying ahead means you have to give a lot of time researching new tech, learning languages, and having conversations with coworkers.

On top of that, you also have to market yourself if you're a freelancer or hit your quotas if you're already employed.

### How can we save our time?

When I landed some clients and my career started kicking off I quickly realised that developing and maintaining projects is a huge time investment, everything felt chaotic and my goals seemed out of reach.

To understand why I was struggling and how to solve the problem I made it my mission to reach out to senior developers, business people, project managers and professionals in tech. More often than not people sympathised with this issue and I would get recommended an agile-based framework called SCRUM.

### What is Scrum?

Scrum is a philosophy built around time and resource management. Whatever you want to create whether it be a creating a website, launching a startup or learning a new technology stack it is beneficial to approach your goals by treating them like a project.

Scrum recommends that these values be upheld for the success of the project:

1. Transparency: Everyone involved in the project must maintain complete transparency in all their work. They have to trust, and encourage each other to hit their goals. Even if you work alone there is a benefit to writing things down on paper and having a discussion with your self.
2. Inspection: To learn you must gain insight into what you've done, this builds on the first pillar. We look back at our work objectively, and make assessments of our performance and quality of work. We then collect feedback around all of our actions and interactions, and we keep an open mind even to criticism.
3. Adaptation: Continuous improvement is the final pillar, the ability to grow based on what you learned during inspection is what makes all your work ultimately worthwhile, regardless of whether or not you failed at the end of the day you documented your wrongs, and learned how to make them right. Now you won't spend time on something pointless, and the mistakes you've made become part of your success. By adapting you offer your clients, friends, and users constant improvements, keeping them around for just one more day, every single day.

### Conclusions

Work is difficult and life is short, you have to treat each day like it's a gift. There is value in every situation as long as you stay honest, open-minded, and adaptive.

Find my links through:https://www.serotonindesigns.com

---

## Post 12: Choosing a crypto-wallet for your Web3 journey. (Part 2) -The different types of wallets

- **URL**: https://www.sybilsolutions.ai/blog/understanding-the-types-of-cryptocurrency-wallets
- **Date**: 2022-07-25
- **Description**: There are many kinds of cryptocurrency wallets, some optimise for security, some for connectivity. We will take a deep dive into learning the different usecases.
- **Tags**: Web3, Cryptocurrency, Wallets, Blockchain, Exchange, Coinbase Wallet, Metamask, Ledger

### Full Content (Verbatim)

## What are the different types of cryptocurrency wallets, and which would should you choose?

One of the choices people have to make when deciding on their cryptocurrency wallet is what form it comes in. You might know that a cryptocurrency wallet is made by finding a random number, then applying cryptographic hashing on it to create private and public keys.If you haven't, and you'd like to learn more. Look at my last post on this topic. read:Part 1

- Paper wallets
- Hardware wallets
- Software wallets.

### 1 Paper wallets:

The first type of wallet that we'll be discussing is a paper wallet.A paper wallet is a printed piece of paper containing keys and QR codes used to facilitate your cryptocurrency transactions. Users would choose to store their wallets in this form to maximize the security of their assets, ensuring only the holder of the paper can access the funds in the wallet. As of 2016, this method is no longer in use, with people choosing more convenient wallets.

### 2 Software wallets:

The second type of wallet is called a software wallet.This type of wallet typically takes the form of a browser plugin or mobile application.Software wallets are created on a web server or site and remain connected to the internet as long as the host device is connected.

By remaining online, software wallets ensure users can trade or interact with web3 projects without delay. For most users, this is the ideal wallet as it provides access to all the conveniences and features of web3 right from their device. The convenience of instant connectivity comes with the trade-off of decreasing overall security, as knowledgeable hackers can access and hack these wallets with little effort. This flaw is especially true if users store big funds in their software wallet.

### 3 Hardware wallets:

The third and final type of wallet on this list is hardware wallets.

This type of wallet typically comes in the form of a USB stick which can be plugged into a computer to access its contents. Entry-level hardware wallets typically cost between 50−200- 200−200, making them a good choice for those who store more than 200$ in their crypto wallets at a time. The benefit of hardware wallets is that unless they're connected to a computer, the funds inside cannot be accessed. In crypto terms these types of devices allow you to put your assets into "cold storage".

As we've established software wallets' constantly online approach introduces safety threats in the form of hackers, bugs, and malicious contracts.

To recap:

Choose paper wallets if:

- You're old
- Have trust issues
- Only want to do things on paper
- You store your money under the bed

Choose software wallets if:

- Fast access to assets is a priority.
- You use real team financial products
- You only hold small amounts of crypto
- You are knowledgeable about basic security
- You are a developer that wants to build in the web-3 space.

Choose hardware wallets if:

- You are a long-term holder of crypto
- Instant access to funds is not a priority
- You hold large amounts of cryptocurrency
- You need additional features offered only by hardware wallets

If you like what I do and you want to stay in touch find my links:

My website

---

## Post 13: Building My Own Homelab: From AI Dependency to Local Superpower

- **URL**: https://www.sybilsolutions.ai/blog/Building-my-own-homelab
- **Date**: 2026-01-15
- **Description**: My journey from spending thousands monthly on AI subscriptions to building a custom 8x 3090 AI rig for local inference
- **Tags**: Open Source, AI, DIY, Hardware, Deep Learning

### Full Content (Verbatim)

## The awakening

August 2022. I tried DALL-E for the first time and instantly felt both endlessly excited and terrified.

> "Callback to August 2022 when I immediately knew we would end up here after seeing a picture made by the beta of dalle" —@seroxdesigns

I thought it was cool but not particularly practical. That changed fast.

Within months, LLMs became my go to tool for handling many of the day to day challenges we all have to live with:

- Budgeting analysis
- Code generation
- Health tracking
- Language learning
- Legal advice

I launched AI-powered side projects. Consulted for companies building AI products. Then I discovered ElizaOS in late 2024.

> "ElizaOS was a huge double edged sword, on 1 hand they did agentic better than any other framework at the time. When Eliza was running X accounts there was no MCP, cursor was still young, and there were no Open Source frameworks for curious people to work with." —@seroxdesigns

## Why Machines Learn

December 2023. I readWhy Machines Learnby Anil Ananthaswamy.

I expected a dry theoretical textbook. What I got felt tailored made for me. Just technical enough to give me a deep level of understanding without being too complex.

> "It's honestly incredible what we can do with some math. If you're into AI I highly recommend 'why machines learn' - @anilananth" —@seroxdesigns

Slowly but surely I understood:

- Backpropagationhow models learn from mistakes
- Gradient descentthe path to optimal solutions
- Vector mathematicsthe language of AI

I learned about perceptrons, activation functions, loss surfaces. My software development background meant I could map these concepts to code I had already written. I even coded a few by hand.

> "Meet big daddy perceptron. One of the first iterations of machine learning. The basic perceptron as a concept takes in 3 parameters, and outputs a single value" —@seroxdesigns

I started running small models locally on my MacBook. Curious to see how they would handle basic tasks. This only got more interesting after GPT-OSS models were released.

## The Breakpoint

In June of 2025, it hit me hard. I was hopelessly dependent on corporations.

> "This age is coming to a close, models are using 6x the tokens, we have hit the token price floor with most of our favorite models, and frontier companies are realizing they can't do infinite usage plans anymore. What this means for us is 30-100$ a day in usage if you use this" —@seroxdesigns

This anxiety stirred in me after Cursor had switched its pricing model, and Claude Code was beginning to follow suit.

- I could not access my own data
- I could not inspect the models I was using
- I could not customize behavior
- I was limited by API policies, usage caps, pricing tiers

I was spending thousands monthly on AI subscriptions.

Looking back at my detailed usage analysis from October 2025:

> "I dug deep into my usage patterns over the last year with AI subscriptions" —@seroxdesigns

> "Token and Cost efficiency for my 4x 3090 Rig. I have systematically analyzed the cost of my AI usage since companies Cursor switched to token based pricing." —@seroxdesigns

| Platform | Inference Value | Cost | Value Ratio |
| --- | --- | --- | --- |
| Cursor Pro | $2,400 | $542 | 4.4x |
| Claude API | $3,750 | $720 | 5.2x |
| Other Tools | ~$4,000 | $750 | 5.3x |
| Total Monthly | ~$10,000 | $2,012 | 5.0x |

> "Claude is the highest value AI subscription for software developers. Insane how fast it can template stuff." —@seroxdesigns

I was spending about200amonthtogetupto200 a month to get up to200amonthtogetupto5000 p/m in token usage. This was unsustainable and it was starting to show.

More importantly:zero ownership.

The minute Cursor raised prices 30%? There was nothing I could do but continue to shell out money, otherwise my capacity of output decreases.

## Making the Decision

The solution was obvious:invest in my own hardware.

I started small. Running models on my MacBook using llama.cpp. Building MCPs for them, experimenting with different quantization levels and configurations.

Here is what I discovered:

We are at a point where intelligence can fit on 36GB of RAM.

- Llama-3-70B quantized to Q4 runs decently
- Mistral-7x22B fits in similar memory with aggressive quantization

> "I have a MacBook and love macOS and generally dislike Linux/windows. But the metrics don't lie, Linux server with 3090s is the best bang for buck out there. Mac ultras are able to run huge models but not at any usable speeds" —@seroxdesigns

## My Journey

### August 26, 2025

> "Just picked up 4x 3090s and an AMD epyc. Building out a beast at home, let's see how this goes. Fully off Claude in 3 months." —@seroxdesigns

### August 30, 2025

> "Building an AI rig at home - 96 VRAM (4x 3090s) - 512 GB DDR4 - 6 TB NVMe - Epyc 7443p - Corsair AX1600i - Thermal Core p90 open tower. I should be able to run: GPT-OSS-120B, Qwen 3 coder, GLM 4.5 Air, Smaller image models, Control my 3d printer, Build my own recommendation Algo" —@seroxdesigns

### August 31, 2025

> "I'm realizing this is going to be a bit more difficult than expected, of course. These gosh darn GPUs draw up to 450w each at spikes. So I need 2 run 2 PSUs, and connect them together via an adapter, which means I need to separate the GPUs." —@seroxdesigns

### September 6, 2025

> "Now how the hell do I fit 4 3090s near this thing. I've never seen bigger GPUs" —@seroxdesigns

### September 16, 2025 — The Disaster

This is where everything went wrong.

> "Crashing out > Gets 4 GPUs mailed out > Gets CPU / RAM / MB > Huge PSU > Sets everything up perfectly over 20 hours > 1 GPU busted > mail it back, get replacement > BUSTED > fix it > PCIe riser cable BUSTED > PSU pcie cables only split > GPUs too fat for split cables" —@seroxdesigns

I spent 20+ hours setting everything up. Case planned carefully. Airflow optimized. All connections verified. First run: success.

Then: crash.

After 22 hours, I discovered the problem. One GPU had overheated and failed. Shipped it back for replacement. Replacement arrived, installed it, and it failed immediately. Another day troubleshooting revealed a second bad GPU.

And that was just the beginning.

The Cascade of Problems:

1. Dead GPUs2 defective units, multiple shipping cycles
2. Broken PCIe riserThe cable connecting motherboard to GPU 2 had snapped
3. Power supply nightmareMy 1,200W PSU had enough wattage but could not deliver enough PCIe power simultaneously. I needed 24 PCIe power lines (8 GPUs x 3 connectors). My PSU only had 8 cables with capacity for maybe 10.
4. Upgrade requiredHad to upgrade to dual 1,600W Corsair units, bridged with specialized cable
5. Power distribution hellSpent hours with a multimeter verifying each cable's source because PSU rear panel naming was confusing
6. Physical fit issuesGPUs kept hitting each other and motherboard slots. Needed premium braided riser cables from a mining-specific supplier
7. PCIe lane mathEPYC CPU has 128 lanes but they are shared. Had to calculate exactly which GPUs get x16 vs x8 bandwidth

> "PCIe riser cables gen 4.0, between 20-40cm in length. The goal is to minimize the length of the cables to prevent latency issues, you also should pick risers with flexible cables" —@seroxdesigns

Lesson learned:Building an 8-GPU rig is not plug-and-play.

### September 17, 2025

> "It's a glorious day all 4 GPUs are live. This was one of the most fun projects I have ever done." —@seroxdesigns

### September 20, 2025

> "There was nothing I could buy that fit the gpus, fans, etc.. I had ziptie this from scratch. Cost 100$ for the parts" —@seroxdesigns

### September 26, 2025

> "I have a MacBook and love macOS and generally dislike Linux/windows. But the metrics don't lie, Linux server with 3090s is the best bang for buck out there. Mac ultras are able to run huge models but not at any usable speeds" —@seroxdesigns

### September 28, 2025

> "GLM-4.5-Air at full context. I ran benchmarks to see the tokens per second generated at various context lengths, what's incredible is it is faster than Claude Opus 3, and ranks way way way higher on every metric. Just 18 months ago that was the golden standard, and now I can run it at home" —@seroxdesigns

### October 3, 2025

> "Yes, I am running a quad 3090 rig. My highest tps is 4k prefill/s and 55 tps which falls to 15 tps by end, write speed with air in llama cpp. But the best is with vLLM it stays consistently at 35tps" —@seroxdesigns

Testing GLM-4.5-Air-AWQ-4bit with vLLM:

| Configuration | Prefill TPS | Generation TPS | Notes |
| --- | --- | --- | --- |
| Basic (4x GPU TP) | ~2,500 | 12-25 | Default settings, no optimization |
| Optimized (vLLM) | ~3,000 | 35 | KV cache tuning, PCIe alignment |
| llama.cpp | ~1,000 | 10 | Degrades with context |

### October 23, 2025

> "9k tps throughput, 50~ output 25% in. Wild what 6 3090s can do." —@seroxdesigns

### November 7, 2025

> "I am quite concerned to say this, I need 2 more gpus." —@seroxdesigns

### November 14, 2025

> "The prophecy has been fulfilled. - 8x 3090s 192gb VRAM - 512GB DDR4 - 6 TB NVMe. I am in computer heaven" —@seroxdesigns

> "Cap the GPU wattage at 200w, I have 2 PSUs and a P2P adapter, the whole thing is 1.5k watts max, usually around half" —@seroxdesigns

### November 16, 2025

> "GPU Rich" —@seroxdesigns

## Hardware Specifications

> "3 months ago I built this beast, let's check the costs today." —@seroxdesigns

| Component | Specification | Cost |
| --- | --- | --- |
| GPUs | 8x RTX 3090 (24GB each = 192GB VRAM) | $7,118.64 |
| Memory | 512GB DDR4 ECC | $2,224.61 |
| Motherboard | ASRock Romed8-2T | $902.63 |
| CPU | EPYC 7443P | $739.01 |
| Storage | 2TB + 4TB Samsung NVMe | $552.54 |
| Power | 2x 1,600W Corsair + 1,000W Corsair | $723.00 |
| Case | Custom zip-tied rack | ~$100 |
| Total |  | ~$12,360 |

Minimum viable setup:2x 3090s with 64GB RAM =$3,000 USD

## Performance Metrics

| Metric | Value | Configuration |
| --- | --- | --- |
| Prefill Throughput | 3,000-9,000 TPS | 4-8x 3090 + vLLM |
| Generation Throughput | 35-50 TPS | 4x 3090 + vLLM optimized |
| Context Window | 180k tokens | 6x 3090 (174GB VRAM) |
| Peak VRAM Usage | 192GB | 8x 3090 full load |

> "196k 4-6H bpw 8Q kvcache 700 tokens per second processing and 18 tokens per second generation. 180k 3.22bpw fp 16 kV 700 tps processing 30 tps generation" —@seroxdesigns

## The Models I Trust

> "MiniMax and GLM are it. I have a slight preference towards MiniMax right now (:" —@seroxdesigns

> "#1 Minimax m2 #2 GLM 4.5 Air / GLM 4.6 reap #3 Hermes 70B #4 GPT-OSS-120B" —@seroxdesigns

| Tier | Model | Use Case | Quantization |
| --- | --- | --- | --- |
| S Tier | GLM-4.5-Air | Daily driver, vision tasks | AWQ-4bit |
|  | GLM-4.5V | Screenshot analysis, UI understanding | AWQ-4bit |
|  | MiniMax-M2.1 | Agentic workflows, complex reasoning | AWQ-4bit |
| A Tier | Hermes-70B | Unrestricted queries | Q5_K_M |
|  | Qwen-72B | General purpose | Q5_K_M |
|  | GPT-OSS-120B | STEM work | Q4_K_M |

> "Way better, GLM-4.6 does better working on a single narrow task. Minimax is way better at doing things until they're done, it's smarter, doesn't get stuck in loops, and tool calls almost never fail." —@seroxdesigns

## Cerebras REAP

> "I spent the last few days running Cerebras' REAP models. I ran GLM-4.5-Air-Reap-82b - 12A bpw-8bit at full context: Prompt Processing - Peak: 1,012 T/s - Average: 920-980 T/s - Range: 754-1,012 T/s. Generation Speed: 43-44 T/s (consistent across context window)" —@seroxdesigns

## Software Stack

> "I built lmstudio for vLLM and sglang. I can't begin to explain how much of a pain in the ass it is not having a simple system to store, share, and build recipes with vLLM and sglang. Now I can request a model by hitting the oai api and if it's not loaded into memory it'll evict whatever is running and load the requested model" —@seroxdesigns

~~~
vllm serve /mnt/llm_model/GLM-4.5-Air-AWQ-4bit \
  --tensor-parallel-size 4 \
  --dtype bfloat16 \
  --max-model-len 131072 \
  --gpu-memory-utilization 0.95 \
  --enable-chunked-prefill

~~~

Key optimizations:

- Contiguous KV cache reduces memory overhead
- Appropriate block size matched to specific model
- GPU memory tuning based on available VRAM
- Chunked prefill for better batching of large contexts

> "MiniMax-M2.1 running at 100 tps servicing 2 clients, 200tps?" —@seroxdesigns

## Why I Switched

| Factor | Corporate AI | Homelab |
| --- | --- | --- |
| Cost per month | $2,000+ | $50 (electricity) |
| Rate limits | Constant concern | None |
| Data privacy | Sent to servers | Never leaves home |
| Model customization | Locked | Full control |
| API stability | Changes constantly | Fixed forever |
| Context window | 200k (expensive) | 500k+ (free) |

> "1 week of my local llms working 24/7 nearly fully autonomously (Needs help every 8 hours or so.) 10% of this is output. 9.6M output tokens with claude sonnet = ~150.85Minputtokenswithsonnet=240. 85M input tokens with sonnet = ~ 240.85Minputtokenswithsonnet=240. This would have cost me 400$ on api prices." —@seroxdesigns

## Practical Use Case: Private Home RAG

This is my most valuable use case by far.

> "Here's my list of usecases so far: 1. Private home rag, all my finances, legal documents, pics, writing, messages, emails are in a rag with private llms 2. Scrapers, I have scraped a few gigabytes of research paper, books, code, etc.. 3. Free claude code and codex" —@seroxdesigns

> "I'm going to make a list of mini-blogs, X threads and repos that make it possible to run a local AI browser extension, home-rag, and mem-layer with just 24GB VRAM" —@seroxdesigns

What it indexes:

- Financial records from multiple banks
- Legal documents
- Scanned contracts
- Photos of physical documents
- My writing
- Personal messages
- Important emails

I can ask natural language questions about years of data and get comprehensive answers with source citations. This would be impossible with traditional search without weeks of manual processing.

Technical stack:

- Database:PostgreSQL with pgvector
- Embedding:BGE-M3 (dense + sparse + multi-vector)
- Index:HNSW for fast retrieval
- Storage:1.2TB indexed documents

## Mobile App for Local LLMs

> "Did you know you can run local models in xcode? I am building a mobile app for my local llms with MCP access & full private data, it's going pretty well." —@seroxdesigns

## What I Do With AI Now

> "I do my: dev work, research, financial budgeting, private recommendation algo, workout tracking, medical advice, government paperwork, home research, memory management. All using AI/MCP. I have never been more impactful than I am today, because of AI" —@seroxdesigns

## Key Takeaways

1. Research saves money and frustration2 months of research prevented me from buying MagSafe-only setup or underpowered machine
2. Standard cases do not work with large GPUsUse custom rack or crypto-mining server chassis
3. Power is your limiting factor1,200W is practical ceiling. Measure everything before buying
4. Speed mattersllama.cpp initial speed might feel good but context degradation destroys quality
5. vLLM is the pathComplex setup vs blazing fast performance. Worth every hour
6. Your data stays yoursThis is freedom. Not perfect, but yours
7. Do not settle for corporate AIIf you use AI daily, build your own infrastructure. It pays off quickly

> "I am telling you, MiniMax-M2.1 and GLM-4.7 are top tier, and MiniMax specifically is soooo fast, frontier model running at home. Never thought this could be possible." —@seroxdesigns

---

This post was compiled from tweets and research spanning August-December 2025.Follow me on Xfor updates.

---
