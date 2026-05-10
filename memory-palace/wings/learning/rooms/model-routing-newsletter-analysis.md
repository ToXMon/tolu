---
title: Model Routing Newsletter Analysis
source: Tyler Folkman - The AI Architect (Substack)
date: 2026-05-10
tags: [model-routing, cost-optimization, ai-infrastructure]
---

# I Routed 2,415 AI Agent Turns Across 6 Models. It Cost $76.77

## Key Data

| Model | Turns | % Usage | Input Tokens | Est. Cost |
|-------|-------|---------|--------------|----------|
| Kimi K2.6 | 1,984 | 82.2% | 243M | $64.79 |
| GPT 5.5 | 238 | 9.9% | 1.1M | $11.04 |
| Qwen 3.6 27B local | 106 | 4.4% | 255K | $0.00 |
| DeepSeek V4 Flash | 38 | 1.6% | 1.8M | $0.26 |
| DeepSeek V4 Pro | 28 | 1.2% | 1.2M | $0.52 |
| GLM 5.1 | 21 | 0.9% | 743K | $0.15 |
| **Total** | **2,415** | **100%** | - | **$76.77** |

- All-GPT 5.5 estimate: $1,272.77
- Savings: ~94%

## Value Score Framework

`value_score = SWE-Bench Pro / ($/M input tokens)`

| Model | SWE-Bench Pro | $/M input | Value Score |
|-------|--------------|-----------|-------------|
| DeepSeek V4 Flash | 52.6 | $0.14 | 375.7 |
| Qwen 3.6 Plus | 56.6 | $0.33 | 171.5 |
| DeepSeek V4 Pro | 55.4 | $0.435 | 127.4 |
| Kimi K2.6 | 58.6 | $0.74 | 79.2 |
| Claude Opus 4.7 | 64.3 | $5.00 | 12.9 |

## 8 Route Architecture

- `/cheap` - DeepSeek V4 Flash (logging, simple edits)
- `/ask` - Qwen 3.6 Plus (explanations, summaries)
- `/workhorse` - Kimi K2.6 (default, coding, PR review)
- `/max` - GPT 5.5 via Codex (hard architecture, repeated failures)
- `/max` fallback - Claude Opus 4.7 via OpenRouter
- `/local` - Qwen 3.6 27B (private, offline, sensitive)
- Plus DeepSeek V4 Pro and GLM 5.1 as alternates

## Monthly Stack

- OpenCode Go: $10/month
- OpenRouter: ~$70/month budget
- Local/Ollama: ~$20/month
- Total: ~$100/month

## Key Takeaways

1. Most AI turns don't need frontier intelligence
2. Route-as-command pattern (think about job, not model)
3. Thinking level is a route property (low/medium/high/off)
4. Every hosted route needs a fallback provider
5. Local route has NO fallback (privacy)
6. Benchmarks are routing signals, not truth

## My Analysis

**Applicable to Agent Zero:**
- Agent Zero already does primitive model routing (main/utility split + subordinate delegation)
- Route-as-command maps well to specialist profile delegation
- Thinking level per route is an underused lever

**Pushback:**
- Regex auto-routing is brittle; author admits using explicit routing most of the time
- $100/month depends on OpenCode Go subsidies
- Missing rework rate metric (how often cheap routing fails and escalates)

## Config Pattern

```json
{
  "auto": false,
  "defaultRoute": "workhorse",
  "outputTokenEstimate": 2000,
  "routes": {
    "cheap": {
      "primary": { "provider": "opencode-go", "model": "deepseek-v4-flash" },
      "fallback": { "provider": "openrouter", "model": "deepseek/deepseek-v4-flash" },
      "thinkingLevel": "low"
    },
    "workhorse": {
      "primary": { "provider": "opencode-go", "model": "kimi-k2.6" },
      "fallback": { "provider": "openrouter", "model": "moonshotai/kimi-k2.6" },
      "thinkingLevel": "medium"
    },
    "max": {
      "primary": { "provider": "openai-codex", "model": "gpt-5.5" },
      "fallback": { "provider": "openrouter", "model": "anthropic/claude-opus-4.7" },
      "thinkingLevel": "high"
    },
    "local": {
      "primary": { "provider": "local", "model": "qwen3.6-27B" },
      "fallback": null,
      "thinkingLevel": "off"
    }
  }
}
```
