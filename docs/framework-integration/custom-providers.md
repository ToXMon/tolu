# Custom Model Provider Configuration Guide

> **The definitive reference for integrating any LLM provider into any AI agent framework.**
> Every code example is copy-paste-ready.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Venice AI Setup](#2-venice-ai-setup)
3. [OpenAI-Compatible Endpoints](#3-openai-compatible-endpoints)
4. [LiteLLM Configuration Patterns](#4-litellm-configuration-patterns)
5. [Environment Variable Approach](#5-environment-variable-approach)
6. [Testing Your Provider Connection](#6-testing-your-provider-connection)
7. [Common Patterns and Tips](#7-common-patterns-and-tips)
8. [Troubleshooting](#8-troubleshooting)

---

## 1. Overview

### Why Custom Providers Matter

Most AI agent frameworks ship with a handful of built-in providers. In practice, you'll want to plug in alternatives for several reasons:

| Motivation | Description |
|------------|-------------|
| **Cost** | Provider pricing varies 10–100×. Route tasks to the cheapest acceptable model. |
| **Privacy** | Some providers log prompts; others (Venice AI, local models) don't. |
| **Performance** | Inference speed, context window size, and output quality differ dramatically. |
| **Availability** | APIs go down. Rate limits hit. Having fallbacks keeps your agents running. |
| **Compliance** | Data residency requirements may mandate specific regions or on-premise deployment. |
| **Specialization** | Code models, reasoning models, vision models — each task has an optimal provider. |

### The Universal Pattern

Nearly every LLM provider exposes an **OpenAI-compatible** API surface. Regardless of which framework you use, configuration always boils down to three values:

```
api_base  → The HTTPS endpoint URL (e.g. https://api.groq.com/openai/v1)
api_key   → Your authentication token (Bearer token in Authorization header)
model_name→ The model identifier (e.g. llama-3.3-70b)
```

### OpenAI API as the De Facto Standard

After OpenAI published their chat completions API, the industry converged on it as a common wire protocol. Most providers now implement the same `/v1/chat/completions` endpoint with the same request/response schema. This means:

- **One integration pattern works everywhere.**
- Libraries built for OpenAI (the `openai` Python/Node package) work with any compatible provider just by changing `base_url`.
- Frameworks like LangChain, LlamaIndex, and Agent Zero already speak this protocol.

### LiteLLM as a Universal Adapter

[LiteLLM](https://github.com/BerriAI/litellm) wraps 100+ providers behind a single `completion()` call. If your framework already depends on LiteLLM (Agent Zero does), you get instant access to every supported provider with zero custom code. See [Section 4](#4-litellm-configuration-patterns) for deep coverage.

---

## 2. Venice AI Setup

Venice AI is a privacy-first, uncensored inference platform that exposes a fully OpenAI-compatible API.

### API Details

| Parameter | Value |
|-----------|-------|
| **Standard API Base** | `https://api.venice.ai/api/v1` |
| **Direct Inference API Base** | `https://api.venice.ai/api/inference/v1` |
| **API Key** | Get from [venice.ai](https://venice.ai) dashboard → Settings → API Keys |
| **OpenAI-compatible** | ✅ Yes |
| **Authentication** | Bearer token in `Authorization` header |
| **Env var** | `VENICE_API_KEY` |

### Available Models

Model availability changes frequently. Query the live list:

```bash
curl -s https://api.venice.ai/api/v1/models \
  -H "Authorization: Bearer $VENICE_API_KEY" | python3 -m json.tool
```

Notable models (as of early 2025):

| Model | Description |
|-------|-------------|
| `llama-3.3-70b` | Meta Llama 3.3 70B — strong general-purpose model |
| `deepseek-r1-671b` | DeepSeek R1 671B — advanced reasoning |
| `mixtral-8x7b` | Mixtral 8×7B MoE — efficient, fast |
| `qwen2.5-72b` | Qwen 2.5 72B — multilingual, coding |
| `llama-3.1-405b` | Llama 3.1 405B — largest open model |
| `mistral-31b` | Mistral 31B — balanced performance |
| `deepseek-llm-67b` | DeepSeek 67B — general purpose |

### Venice-Specific Parameters

Venice injects its own system prompt by default. In an agent framework you almost always want to **disable** this to avoid conflicting system prompts:

```json
{
  "model": "llama-3.3-70b",
  "messages": [{"role": "user", "content": "Hello"}],
  "venice_parameters": {
    "include_venice_system_prompt": false
  }
}
```

### Configuration Examples

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  venice:
    name: Venice.ai
    litellm_provider: openai
    kwargs:
      api_base: https://api.venice.ai/api/v1
      venice_parameters:
        include_venice_system_prompt: false

embedding:
  venice:
    name: Venice.ai Embeddings
    litellm_provider: openai
    kwargs:
      api_base: https://api.venice.ai/api/v1
```

#### Direct API Call (curl)

```bash
curl https://api.venice.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $VENICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b",
    "messages": [{"role": "user", "content": "Hello"}],
    "venice_parameters": {
      "include_venice_system_prompt": false
    }
  }'
```

#### Streaming (curl)

```bash
curl https://api.venice.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $VENICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b",
    "messages": [{"role": "user", "content": "Write a poem"}],
    "stream": true,
    "venice_parameters": {"include_venice_system_prompt": false}
  }'
```

#### Python (requests)

```python
import os
import requests

response = requests.post(
    "https://api.venice.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {os.environ['VENICE_API_KEY']}",
        "Content-Type": "application/json",
    },
    json={
        "model": "llama-3.3-70b",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
        "venice_parameters": {"include_venice_system_prompt": False},
    },
)

result = response.json()
print(result["choices"][0]["message"]["content"])
```

#### Python (openai library)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["VENICE_API_KEY"],
    base_url="https://api.venice.ai/api/v1",
)

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ],
    extra_body={
        "venice_parameters": {"include_venice_system_prompt": False}
    },
)

print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm
import os

response = litellm.completion(
    model="openai/llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="https://api.venice.ai/api/v1",
    api_key=os.environ["VENICE_API_KEY"],
)

print(response.choices[0].message.content)
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.VENICE_API_KEY,
  baseURL: 'https://api.venice.ai/api/v1',
});

const response = await client.chat.completions.create({
  model: 'llama-3.3-70b',
  messages: [{ role: 'user', content: 'Hello!' }],
});

console.log(response.choices[0].message.content);
```

#### Environment Variable

```bash
export VENICE_API_KEY="your-key-here"
```

Add to `~/.bashrc`, `~/.zshrc`, or your `.env` file:

```bash
# ~/.bashrc or ~/.zshrc
export VENICE_API_KEY="vp_your_venice_api_key_here"
```

---

## 3. OpenAI-Compatible Endpoints

Every provider below follows the same three-step setup:

1. **Set the API base URL** to the provider's `/v1` endpoint.
2. **Set the API key** via env var, config file, or constructor argument.
3. **Use the model name** as documented by the provider.

### Quick Reference Table

| Provider | API Base | Key Env Var | Speed | Privacy |
|----------|----------|-------------|-------|---------|
| **Together AI** | `https://api.together.xyz/v1` | `TOGETHER_API_KEY` | Fast | Standard |
| **Fireworks AI** | `https://api.fireworks.ai/inference/v1` | `FIREWORKS_API_KEY` | Very Fast | Standard |
| **Groq** | `https://api.groq.com/openai/v1` | `GROQ_API_KEY` | Ultra Fast | Standard |
| **OpenRouter** | `https://openrouter.ai/api/v1` | `OPENROUTER_API_KEY` | Varies | Standard |
| **DeepSeek** | `https://api.deepseek.com/v1` | `DEEPSEEK_API_KEY` | Medium | Standard |
| **Mistral AI** | `https://api.mistral.ai/v1` | `MISTRAL_API_KEY` | Fast | Standard |
| **xAI (Grok)** | `https://api.x.ai/v1` | `XAI_API_KEY` | Fast | Standard |
| **SambaNova** | `https://api.sambanova.ai/v1` | `SAMBANOVA_API_KEY` | Very Fast | Standard |
| **Cerebras** | `https://api.cerebras.ai/v1` | `CEREBRAS_API_KEY` | Ultra Fast | Standard |
| **Venice AI** | `https://api.venice.ai/api/v1` | `VENICE_API_KEY` | Fast | High |
| **Ollama** (local) | `http://localhost:11434/v1` | *(none)* | Depends on HW | Full |
| **LM Studio** (local) | `http://localhost:1234/v1` | *(none)* | Depends on HW | Full |
| **vLLM** (local) | `http://localhost:8000/v1` | *(none)* | Depends on HW | Full |

---

### Together AI

[Together AI](https://together.ai) provides serverless inference for open-source models with competitive pricing.

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://api.together.xyz/v1` |
| **API Key** | [app.together.ai](https://app.together.ai) → Settings → API Keys |
| **Env Var** | `TOGETHER_API_KEY` |
| **Quirk** | Model names use the `owner/model` format |

**Notable Models:** `meta-llama/Llama-3.3-70B-Instruct-Turbo`, `mistralai/Mixtral-8x7B-Instruct-v0.1`, `databricks/dbrx-instruct`, `Qwen/Qwen2.5-72B-Instruct-Turbo`, `deepseek-ai/DeepSeek-R1-Distill-Llama-70B`

#### curl

```bash
curl https://api.together.xyz/v1/chat/completions \
  -H "Authorization: Bearer $TOGETHER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["TOGETHER_API_KEY"],
    base_url="https://api.together.xyz/v1",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Hello!"}],
    api_key=os.environ["TOGETHER_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  together:
    name: Together AI
    litellm_provider: together_ai
    kwargs:
      api_key: "${TOGETHER_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.TOGETHER_API_KEY,
  baseURL: 'https://api.together.xyz/v1',
});

const response = await client.chat.completions.create({
  model: 'meta-llama/Llama-3.3-70B-Instruct-Turbo',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### Fireworks AI

[Fireworks AI](https://fireworks.ai) offers fast inference for open-source models with a focus on latency.

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://api.fireworks.ai/inference/v1` |
| **API Key** | [app.fireworks.ai](https://app.fireworks.ai) → API Keys |
| **Env Var** | `FIREWORKS_API_KEY` |
| **Quirk** | Model names use the `accounts/fireworks/models/` prefix for some models |

**Notable Models:** `accounts/fireworks/models/llama-v3p3-70b-instruct`, `accounts/fireworks/models/mixtral-8x7b-instruct`, `accounts/fireworks/models/qwen2p5-72b-instruct`, `accounts/fireworks/models/deepseek-r1`

#### curl

```bash
curl https://api.fireworks.ai/inference/v1/chat/completions \
  -H "Authorization: Bearer $FIREWORKS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["FIREWORKS_API_KEY"],
    base_url="https://api.fireworks.ai/inference/v1",
)

response = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p3-70b-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    api_key=os.environ["FIREWORKS_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  fireworks:
    name: Fireworks AI
    litellm_provider: fireworks_ai
    kwargs:
      api_key: "${FIREWORKS_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.FIREWORKS_API_KEY,
  baseURL: 'https://api.fireworks.ai/inference/v1',
});

const response = await client.chat.completions.create({
  model: 'accounts/fireworks/models/llama-v3p3-70b-instruct',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### Groq

[Groq](https://groq.com) delivers **ultra-fast** inference using custom LPU hardware. Ideal for low-latency agent loops.

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://api.groq.com/openai/v1` |
| **API Key** | [console.groq.com](https://console.groq.com) → API Keys |
| **Env Var** | `GROQ_API_KEY` |
| **Quirk** | Very strict rate limits on free tier; very fast responses |

**Notable Models:** `llama-3.3-70b-versatile`, `llama-3.1-8b-instant`, `mixtral-8x7b-32768`, `gemma2-9b-it`

#### curl

```bash
curl https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b-versatile",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="groq/llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}],
    api_key=os.environ["GROQ_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  groq:
    name: Groq
    litellm_provider: groq
    kwargs:
      api_key: "${GROQ_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.GROQ_API_KEY,
  baseURL: 'https://api.groq.com/openai/v1',
});

const response = await client.chat.completions.create({
  model: 'llama-3.3-70b-versatile',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### OpenRouter

[OpenRouter](https://openrouter.ai) is a **model aggregator** providing a single API for 100+ models from dozens of providers.

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://openrouter.ai/api/v1` |
| **API Key** | [openrouter.ai/keys](https://openrouter.ai/keys) |
| **Env Var** | `OPENROUTER_API_KEY` |
| **Quirk** | Requires `HTTP-Referer` and `X-Title` headers for rankings; model names use `provider/model` format |

**Notable Models:** `anthropic/claude-sonnet-4`, `openai/gpt-4o`, `meta-llama/llama-3.3-70b-instruct`, `google/gemini-2.0-flash-001`, `deepseek/deepseek-r1`

#### curl

```bash
curl https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -H "HTTP-Referer: https://your-app.com" \
  -H "X-Title: Your App Name" \
  -d '{
    "model": "meta-llama/llama-3.3-70b-instruct",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["OPENROUTER_API_KEY"],
    base_url="https://openrouter.ai/api/v1",
    default_headers={
        "HTTP-Referer": "https://your-app.com",
        "X-Title": "Your App Name",
    },
)

response = client.chat.completions.create(
    model="meta-llama/llama-3.3-70b-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="openrouter/meta-llama/llama-3.3-70b-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    api_key=os.environ["OPENROUTER_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  openrouter:
    name: OpenRouter
    litellm_provider: openrouter
    kwargs:
      api_key: "${OPENROUTER_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.OPENROUTER_API_KEY,
  baseURL: 'https://openrouter.ai/api/v1',
  defaultHeaders: {
    'HTTP-Referer': 'https://your-app.com',
    'X-Title': 'Your App Name',
  },
});

const response = await client.chat.completions.create({
  model: 'meta-llama/llama-3.3-70b-instruct',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### DeepSeek

[DeepSeek](https://platform.deepseek.com) offers their own models with strong reasoning capabilities and competitive pricing.

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://api.deepseek.com/v1` |
| **API Key** | [platform.deepseek.com](https://platform.deepseek.com/api_keys) |
| **Env Var** | `DEEPSEEK_API_KEY` |
| **Quirk** | `deepseek-reasoner` returns a `reasoning_content` field in the response |

**Notable Models:** `deepseek-chat` (DeepSeek-V3), `deepseek-reasoner` (DeepSeek-R1)

#### curl

```bash
curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer $DEEPSEEK_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek-chat",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com/v1",
)

response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="deepseek/deepseek-chat",
    messages=[{"role": "user", "content": "Hello!"}],
    api_key=os.environ["DEEPSEEK_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  deepseek:
    name: DeepSeek
    litellm_provider: deepseek
    kwargs:
      api_key: "${DEEPSEEK_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.DEEPSEEK_API_KEY,
  baseURL: 'https://api.deepseek.com/v1',
});

const response = await client.chat.completions.create({
  model: 'deepseek-chat',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### Mistral AI

[Mistral AI](https://mistral.ai) provides their own models with strong multilingual and coding capabilities.

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://api.mistral.ai/v1` |
| **API Key** | [console.mistral.ai](https://console.mistral.ai) → API Keys |
| **Env Var** | `MISTRAL_API_KEY` |
| **Quirk** | Native function calling support; embedding model `mistral-embed` available |

**Notable Models:** `mistral-large-latest`, `mistral-medium-latest`, `mistral-small-latest`, `codestral-latest`, `open-mistral-nemo`

#### curl

```bash
curl https://api.mistral.ai/v1/chat/completions \
  -H "Authorization: Bearer $MISTRAL_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "mistral-large-latest",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["MISTRAL_API_KEY"],
    base_url="https://api.mistral.ai/v1",
)

response = client.chat.completions.create(
    model="mistral-large-latest",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="mistral/mistral-large-latest",
    messages=[{"role": "user", "content": "Hello!"}],
    api_key=os.environ["MISTRAL_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  mistral:
    name: Mistral AI
    litellm_provider: mistral
    kwargs:
      api_key: "${MISTRAL_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.MISTRAL_API_KEY,
  baseURL: 'https://api.mistral.ai/v1',
});

const response = await client.chat.completions.create({
  model: 'mistral-large-latest',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### xAI (Grok)

[xAI](https://x.ai) provides the Grok family of models.

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://api.x.ai/v1` |
| **API Key** | [console.x.ai](https://console.x.ai) |
| **Env Var** | `XAI_API_KEY` |
| **Quirk** | Newer provider; model list evolving rapidly |

**Notable Models:** `grok-beta`, `grok-2-1212`, `grok-3-beta`

#### curl

```bash
curl https://api.x.ai/v1/chat/completions \
  -H "Authorization: Bearer $XAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "grok-beta",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["XAI_API_KEY"],
    base_url="https://api.x.ai/v1",
)

response = client.chat.completions.create(
    model="grok-beta",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="xai/grok-beta",
    messages=[{"role": "user", "content": "Hello!"}],
    api_key=os.environ["XAI_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  xai:
    name: xAI
    litellm_provider: openai
    kwargs:
      api_base: https://api.x.ai/v1
      api_key: "${XAI_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.XAI_API_KEY,
  baseURL: 'https://api.x.ai/v1',
});

const response = await client.chat.completions.create({
  model: 'grok-beta',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### SambaNova

[SambaNova](https://sambanova.ai) provides fast inference on custom AI hardware (SN40L chip).

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://api.sambanova.ai/v1` |
| **API Key** | [sambanova.ai](https://cloud.sambanova.ai) → API Keys |
| **Env Var** | `SAMBANOVA_API_KEY` |
| **Quirk** | Model names may include version suffixes; check `/v1/models` for current list |

**Notable Models:** `Meta-Llama-3.3-70B-Instruct`, `DeepSeek-R1-Distill-Llama-70B`

#### curl

```bash
curl https://api.sambanova.ai/v1/chat/completions \
  -H "Authorization: Bearer $SAMBANOVA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Meta-Llama-3.3-70B-Instruct",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["SAMBANOVA_API_KEY"],
    base_url="https://api.sambanova.ai/v1",
)

response = client.chat.completions.create(
    model="Meta-Llama-3.3-70B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="openai/Meta-Llama-3.3-70B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="https://api.sambanova.ai/v1",
    api_key=os.environ["SAMBANOVA_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  sambanova:
    name: SambaNova
    litellm_provider: openai
    kwargs:
      api_base: https://api.sambanova.ai/v1
      api_key: "${SAMBANOVA_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.SAMBANOVA_API_KEY,
  baseURL: 'https://api.sambanova.ai/v1',
});

const response = await client.chat.completions.create({
  model: 'Meta-Llama-3.3-70B-Instruct',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### Cerebras

[Cerebras](https://cerebras.ai) delivers **ultra-fast inference** using their wafer-scale CS-3 chip. Some of the fastest LLM inference available.

| Parameter | Value |
|-----------|-------|
| **API Base** | `https://api.cerebras.ai/v1` |
| **API Key** | [cloud.cerebras.ai](https://cloud.cerebras.ai) |
| **Env Var** | `CEREBRAS_API_KEY` |
| **Quirk** | Extremely fast; limited model selection; strict context length limits on some models |

**Notable Models:** `llama-3.3-70b`, `llama-3.1-8b`

#### curl

```bash
curl https://api.cerebras.ai/v1/chat/completions \
  -H "Authorization: Bearer $CEREBRAS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

#### Python (openai)

```python
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["CEREBRAS_API_KEY"],
    base_url="https://api.cerebras.ai/v1",
)

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

#### Python (litellm)

```python
import litellm, os

response = litellm.completion(
    model="cerebras/llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello!"}],
    api_key=os.environ["CEREBRAS_API_KEY"],
)
print(response.choices[0].message.content)
```

#### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  cerebras:
    name: Cerebras
    litellm_provider: cerebras
    kwargs:
      api_key: "${CEREBRAS_API_KEY}"
```

#### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: process.env.CEREBRAS_API_KEY,
  baseURL: 'https://api.cerebras.ai/v1',
});

const response = await client.chat.completions.create({
  model: 'llama-3.3-70b',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

### Local Providers

Local providers run models on your own hardware. No API keys needed, full privacy, but performance depends on your GPU/CPU.

#### Ollama

[Ollama](https://ollama.ai) is the easiest way to run local models. Install it, pull a model, and go.

| Parameter | Value |
|-----------|-------|
| **API Base** | `http://localhost:11434/v1` |
| **API Key** | *(none needed)* |
| **Env Var** | *(none)* |
| **Quirk** | Must `ollama pull <model>` before use; models are local |

**Setup:**

```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Pull a model
ollama pull llama3.3
ollama pull qwen2.5
ollama pull codellama

# Verify it's running
curl http://localhost:11434/v1/models
```

##### curl

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.3",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

##### Python (openai)

```python
from openai import OpenAI

client = OpenAI(
    api_key="ollama",  # Required by the library but unused
    base_url="http://localhost:11434/v1",
)

response = client.chat.completions.create(
    model="llama3.3",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

##### Python (litellm)

```python
import litellm

response = litellm.completion(
    model="ollama/llama3.3",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="http://localhost:11434",
)
print(response.choices[0].message.content)
```

##### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  ollama:
    name: Ollama Local
    litellm_provider: ollama
    kwargs:
      api_base: http://localhost:11434

embedding:
  ollama:
    name: Ollama Embeddings
    litellm_provider: ollama
    kwargs:
      api_base: http://localhost:11434
```

##### Node.js

```javascript
import OpenAI from 'openai';

const client = new OpenAI({
  apiKey: 'ollama',
  baseURL: 'http://localhost:11434/v1',
});

const response = await client.chat.completions.create({
  model: 'llama3.3',
  messages: [{ role: 'user', content: 'Hello!' }],
});
console.log(response.choices[0].message.content);
```

---

#### LM Studio

[LM Studio](https://lmstudio.ai) provides a GUI for downloading and running local models with an OpenAI-compatible server.

| Parameter | Value |
|-----------|-------|
| **API Base** | `http://localhost:1234/v1` |
| **API Key** | *(none needed)* |
| **Env Var** | *(none)* |
| **Quirk** | Start the local server from LM Studio GUI first; model name shown in the app |

**Setup:**

1. Download and install [LM Studio](https://lmstudio.ai)
2. Search and download a model (e.g., Llama 3.3 70B Q4)
3. Click the "Local Server" tab → Start Server
4. The server exposes `http://localhost:1234/v1`

##### curl

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "local-model",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

##### Python (openai)

```python
from openai import OpenAI

client = OpenAI(
    api_key="lm-studio",
    base_url="http://localhost:1234/v1",
)

# List available models
models = client.models.list()
for m in models.data:
    print(m.id)

response = client.chat.completions.create(
    model=models.data[0].id,  # Use first available model
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

##### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  lmstudio:
    name: LM Studio Local
    litellm_provider: openai
    kwargs:
      api_base: http://localhost:1234/v1
      api_key: "lm-studio"
```

---

#### vLLM

[vLLM](https://github.com/vllm-project/vllm) is a high-throughput inference server for production local deployments.

| Parameter | Value |
|-----------|-------|
| **API Base** | `http://localhost:8000/v1` |
| **API Key** | *(none needed, or set via `--api-key` flag)* |
| **Env Var** | *(none)* |
| **Quirk** | Must specify `--model` path or HuggingFace ID when launching |

**Setup:**

```bash
# Install vLLM
pip install vllm

# Launch server
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-3.3-70B-Instruct \
  --host 0.0.0.0 \
  --port 8000
```

##### curl

```bash
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "meta-llama/Llama-3.3-70B-Instruct",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

##### Python (openai)

```python
from openai import OpenAI

client = OpenAI(
    api_key="vllm",
    base_url="http://localhost:8000/v1",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    messages=[{"role": "user", "content": "Hello!"}],
)
print(response.choices[0].message.content)
```

##### Agent Zero (`model_providers.yaml`)

```yaml
chat:
  vllm:
    name: vLLM Local
    litellm_provider: openai
    kwargs:
      api_base: http://localhost:8000/v1
      api_key: "vllm"
```

---

## 4. LiteLLM Configuration Patterns

### What is LiteLLM

[LiteLLM](https://docs.litellm.ai/) is a universal adapter library that translates OpenAI-format API calls to any of 100+ LLM providers. Key benefits:

- **Single interface**: Call `litellm.completion()` for every provider
- **Provider prefixes**: Route to the right provider with `provider/model` syntax
- **Error handling**: Automatic retries, fallbacks, and rate limit handling
- **Cost tracking**: Built-in spend tracking per provider and model
- **Streaming**: Uniform streaming interface across all providers

Used by **Agent Zero**, **LangChain**, **CrewAI**, **AutoGen**, and many other frameworks.

### Provider Prefixes

| Prefix | Provider | Example |
|--------|----------|---------|
| `openai/` | OpenAI | `openai/gpt-4o` |
| `anthropic/` | Anthropic | `anthropic/claude-sonnet-4-5` |
| `gemini/` | Google Gemini | `gemini/gemini-2.0-flash` |
| `groq/` | Groq | `groq/llama-3.3-70b-versatile` |
| `together_ai/` | Together AI | `together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo` |
| `fireworks_ai/` | Fireworks AI | `fireworks_ai/accounts/fireworks/models/llama-v3p3-70b-instruct` |
| `openrouter/` | OpenRouter | `openrouter/anthropic/claude-sonnet-4` |
| `mistral/` | Mistral AI | `mistral/mistral-large-latest` |
| `deepseek/` | DeepSeek | `deepseek/deepseek-chat` |
| `xai/` | xAI | `xai/grok-beta` |
| `cerebras/` | Cerebras | `cerebras/llama-3.3-70b` |
| `ollama/` | Ollama | `ollama/llama3.3` |
| `huggingface/` | HuggingFace | `huggingface/mistralai/Mistral-7B-Instruct-v0.1` |
| `azure/` | Azure OpenAI | `azure/my-deployment` |
| `bedrock/` | AWS Bedrock | `bedrock/anthropic.claude-3-sonnet` |

### Using Custom API Base with LiteLLM

When a provider isn't natively supported or you're using a custom endpoint, use the `openai/` prefix with a custom `api_base`:

```python
import litellm

# Any OpenAI-compatible provider
response = litellm.completion(
    model="openai/your-model-name",
    messages=[{"role": "user", "content": "Hello"}],
    api_base="https://your-provider.com/v1",
    api_key="your-key",
)

print(response.choices[0].message.content)
```

### Streaming with LiteLLM

```python
import litellm

response = litellm.completion(
    model="groq/llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Write a haiku about coding"}],
    stream=True,
    api_key="your-groq-key",
)

for chunk in response:
    content = chunk.choices[0].delta.content or ""
    print(content, end="", flush=True)
print()
```

### Embeddings with LiteLLM

```python
import litellm

response = litellm.embedding(
    model="openai/text-embedding-3-small",
    input=["Hello world", "Goodbye world"],
    api_key="your-openai-key",
)

for item in response.data:
    print(f"Embedding dimension: {len(item.embedding)}")
```

### LiteLLM with Config File (`litellm_config.yaml`)

For complex multi-provider setups, use a config file:

```yaml
model_list:
  # Chat models
  - model_name: primary-chat
    litellm_params:
      model: anthropic/claude-sonnet-4-5
      api_key: os.environ/ANTHROPIC_API_KEY

  - model_name: fast-chat
    litellm_params:
      model: groq/llama-3.3-70b-versatile
      api_key: os.environ/GROQ_API_KEY

  - model_name: cheap-chat
    litellm_params:
      model: together_ai/meta-llama/Llama-3.3-70B-Instruct-Turbo
      api_key: os.environ/TOGETHER_API_KEY

  - model_name: private-chat
    litellm_params:
      model: openai/llama-3.3-70b
      api_base: https://api.venice.ai/api/v1
      api_key: os.environ/VENICE_API_KEY

  - model_name: local-chat
    litellm_params:
      model: ollama/llama3.3
      api_base: http://localhost:11434

  # Embedding models
  - model_name: embedding
    litellm_params:
      model: openai/text-embedding-3-small
      api_key: os.environ/OPENAI_API_KEY

router_settings:
  routing_strategy: latency-based-routing
  allowed_fails: 3
  cooldown_time: 60
  num_retries: 2
  timeout: 30
  fallbacks:
    - {"primary-chat": ["fast-chat", "cheap-chat"]}
    - {"fast-chat": ["cheap-chat", "local-chat"]}

general_settings:
  drop_params: true
  set_verbose: false
```

### Model Routing with LiteLLM

#### Fallbacks

```python
from litellm import Router

router = Router(
    model_list=[
        {
            "model_name": "gpt-4o",
            "litellm_params": {
                "model": "openai/gpt-4o",
                "api_key": os.environ["OPENAI_API_KEY"],
            },
        },
        {
            "model_name": "gpt-4o",
            "litellm_params": {
                "model": "groq/llama-3.3-70b-versatile",
                "api_key": os.environ["GROQ_API_KEY"],
            },
        },
    ],
    fallbacks=[{"gpt-4o": ["gpt-4o"]}],  # Falls to second provider on failure
    num_retries=2,
)

response = router.completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

#### Rate Limiting

```python
from litellm import Router

router = Router(
    model_list=[
        {
            "model_name": "fast-model",
            "litellm_params": {
                "model": "groq/llama-3.3-70b-versatile",
                "api_key": os.environ["GROQ_API_KEY"],
                "rpm": 30,  # Requests per minute
                "tpm": 100000,  # Tokens per minute
            },
        },
    ],
)
```

#### Cost Tracking

```python
import litellm

# Enable cost logging
litellm.success_callback = ["langfuse"]  # or "langsmith", "helicone"

response = litellm.completion(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
)

# Access cost info
print(f"Cost: ${response._hidden_params['response_cost']}")
print(f"Usage: {response.usage}")
```

---

## 5. Environment Variable Approach

### Universal Pattern

Every provider follows the same naming convention:

```bash
PROVIDER_API_KEY     # Required: your API key
PROVIDER_API_BASE    # Optional: override the default API endpoint
```

| Provider | Key Variable | Optional Base Variable |
|----------|-------------|----------------------|
| OpenAI | `OPENAI_API_KEY` | — |
| Anthropic | `ANTHROPIC_API_KEY` | — |
| Venice AI | `VENICE_API_KEY` | `VENICE_API_BASE` |
| Together AI | `TOGETHER_API_KEY` | — |
| Fireworks AI | `FIREWORKS_API_KEY` | — |
| Groq | `GROQ_API_KEY` | — |
| OpenRouter | `OPENROUTER_API_KEY` | — |
| DeepSeek | `DEEPSEEK_API_KEY` | — |
| Mistral AI | `MISTRAL_API_KEY` | — |
| xAI | `XAI_API_KEY` | — |
| SambaNova | `SAMBANOVA_API_KEY` | — |
| Cerebras | `CEREBRAS_API_KEY` | — |

### `.env` File Setup

Create a `.env` file in your project root (add it to `.gitignore`!):

```bash
# .env — NEVER commit this file to version control

# ── Primary Providers ──────────────────────────────────────
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# ── Privacy-First Providers ────────────────────────────────
VENICE_API_KEY=vp_...

# ── Fast Inference Providers ───────────────────────────────
GROQ_API_KEY=gsk_...
CEREBRAS_API_KEY=csk-...

# ── Open-Source Model Hosts ────────────────────────────────
TOGETHER_API_KEY=together_...
FIREWORKS_API_KEY=fw_...
SAMBANOVA_API_KEY=samba_...

# ── Aggregator ─────────────────────────────────────────────
OPENROUTER_API_KEY=sk-or-...

# ── Reasoning Models ───────────────────────────────────────
DEEPSEEK_API_KEY=dsk_...

# ── Specialized Providers ──────────────────────────────────
MISTRAL_API_KEY=mist_...
XAI_API_KEY=xai-...

# ── Optional: Override default API bases ───────────────────
# VENICE_API_BASE=https://api.venice.ai/api/inference/v1

# ── LiteLLM Proxy (if using) ──────────────────────────────
# LITELLM_MASTER_KEY=sk-1234
# DATABASE_URL=postgresql://...
```

Load it in Python:

```python
from dotenv import load_dotenv
load_dotenv()  # Loads .env into os.environ

import os
print(os.environ.get("VENICE_API_KEY", "not set"))
```

### Docker Environment

#### `docker run`

```bash
docker run -d \
  --name agent-zero \
  -p 50080:8080 \
  -e VENICE_API_KEY="vp_your_key" \
  -e GROQ_API_KEY="gsk_your_key" \
  -e OPENAI_API_KEY="sk_your_key" \
  -e DEEPSEEK_API_KEY="dsk_your_key" \
  -v agent-zero-data:/a0 \
  agent-zero:latest
```

#### `docker-compose.yml`

```yaml
version: '3.8'
services:
  agent-zero:
    image: agent-zero:latest
    ports:
      - "50080:8080"
    environment:
      # Use env_file for cleaner management
      - env_file: .env
      # Or set Agent Zero config directly
      - A0_SET_chat_model_provider=venice
      - A0_SET_chat_model_name=llama-3.3-70b
      - A0_SET_utility_model_provider=groq
      - A0_SET_utility_model_name=llama-3.3-70b-versatile
      - A0_SET_embedding_model_provider=openai
      - A0_SET_embedding_model_name=text-embedding-3-small
    env_file:
      - .env
    volumes:
      - agent-zero-data:/a0

volumes:
  agent-zero-data:
```

### Kubernetes Secrets

```yaml
# secret.yaml
apiVersion: v1
kind: Secret
metadata:
  name: llm-api-keys
type: Opaque
stringData:
  VENICE_API_KEY: "vp_your_key"
  GROQ_API_KEY: "gsk_your_key"
  OPENAI_API_KEY: "sk_your_key"
  DEEPSEEK_API_KEY: "dsk_your_key"
  ANTHROPIC_API_KEY: "sk-ant_your_key"
  MISTRAL_API_KEY: "mist_your_key"
  TOGETHER_API_KEY: "together_your_key"
  OPENROUTER_API_KEY: "sk-or_your_key"
---
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: agent-zero
spec:
  replicas: 1
  selector:
    matchLabels:
      app: agent-zero
  template:
    metadata:
      labels:
        app: agent-zero
    spec:
      containers:
        - name: agent-zero
          image: agent-zero:latest
          ports:
            - containerPort: 8080
          envFrom:
            - secretRef:
                name: llm-api-keys
          env:
            - name: A0_SET_chat_model_provider
              value: "venice"
            - name: A0_SET_chat_model_name
              value: "llama-3.3-70b"
            - name: A0_SET_utility_model_provider
              value: "groq"
            - name: A0_SET_utility_model_name
              value: "llama-3.3-70b-versatile"
```

Apply:

```bash
kubectl apply -f secret.yaml
kubectl apply -f deployment.yaml
```

---

## 6. Testing Your Provider Connection

### Quick Test with curl

Universal template — replace the placeholders:

```bash
# Set your values
API_BASE="https://api.venice.ai/api/v1"
API_KEY="$VENICE_API_KEY"
MODEL="llama-3.3-70b"

# Test the connection
curl -s "$API_BASE/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d "{\"model\": \"$MODEL\", \"messages\": [{\"role\": \"user\", \"content\": \"Say 'connection successful' and nothing else.\"}]}" | python3 -m json.tool

# List models
curl -s "$API_BASE/models" \
  -H "Authorization: Bearer $API_KEY" | python3 -m json.tool
```

### Python Test Script

Save as `test_provider.py`:

```python
#!/usr/bin/env python3
"""Test an OpenAI-compatible LLM provider connection.

Usage:
    python test_provider.py --provider venice
    python test_provider.py --api-base https://api.groq.com/openai/v1 --model llama-3.3-70b-versatile
    python test_provider.py --provider venice --stream
"""

import argparse
import os
import sys
import time
import json
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    print("Installing openai package...")
    os.system(f"{sys.executable} -m pip install openai -q")
    from openai import OpenAI


PROVIDERS = {
    "venice": {
        "base_url": "https://api.venice.ai/api/v1",
        "env_key": "VENICE_API_KEY",
        "model": "llama-3.3-70b",
    },
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "env_key": "TOGETHER_API_KEY",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    },
    "fireworks": {
        "base_url": "https://api.fireworks.ai/inference/v1",
        "env_key": "FIREWORKS_API_KEY",
        "model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "env_key": "GROQ_API_KEY",
        "model": "llama-3.3-70b-versatile",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "env_key": "OPENROUTER_API_KEY",
        "model": "meta-llama/llama-3.3-70b-instruct",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "env_key": "DEEPSEEK_API_KEY",
        "model": "deepseek-chat",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "env_key": "MISTRAL_API_KEY",
        "model": "mistral-large-latest",
    },
    "xai": {
        "base_url": "https://api.x.ai/v1",
        "env_key": "XAI_API_KEY",
        "model": "grok-beta",
    },
    "sambanova": {
        "base_url": "https://api.sambanova.ai/v1",
        "env_key": "SAMBANOVA_API_KEY",
        "model": "Meta-Llama-3.3-70B-Instruct",
    },
    "cerebras": {
        "base_url": "https://api.cerebras.ai/v1",
        "env_key": "CEREBRAS_API_KEY",
        "model": "llama-3.3-70b",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "env_key": None,
        "model": "llama3.3",
    },
    "lmstudio": {
        "base_url": "http://localhost:1234/v1",
        "env_key": None,
        "model": "local-model",
    },
    "vllm": {
        "base_url": "http://localhost:8000/v1",
        "env_key": None,
        "model": "local-model",
    },
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
        "model": "gpt-4o",
    },
    "anthropic": {
        "base_url": "https://api.anthropic.com/v1",
        "env_key": "ANTHROPIC_API_KEY",
        "model": "claude-sonnet-4-5",
    },
}


def test_provider(
    base_url: str,
    api_key: str | None,
    model: str,
    test_streaming: bool = False,
    test_models_list: bool = True,
):
    """Test a provider connection and report results."""
    print(f"\n{'='*60}")
    print(f"  Provider Test")
    print(f"  Base URL: {base_url}")
    print(f"  Model:    {model}")
    print(f"{'='*60}\n")

    client = OpenAI(api_key=api_key or "unused", base_url=base_url)

    # ── Test 1: List models ────────────────────────────────
    if test_models_list:
        print("📋 Test: List Models")
        try:
            start = time.time()
            models = client.models.list()
            elapsed = time.time() - start
            model_names = [m.id for m in models.data[:10]]  # First 10
            print(f"  ✅ Found {len(models.data)} models ({elapsed:.2f}s)")
            for name in model_names:
                print(f"     • {name}")
            if len(models.data) > 10:
                print(f"     ... and {len(models.data) - 10} more")
            print()
        except Exception as e:
            print(f"  ❌ Failed: {e}\n")

    # ── Test 2: Chat completion ────────────────────────────
    print("💬 Test: Chat Completion")
    try:
        start = time.time()
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful test assistant."},
                {"role": "user", "content": "Respond with exactly: CONNECTION_OK"},
            ],
            max_tokens=20,
            temperature=0,
        )
        elapsed = time.time() - start
        content = response.choices[0].message.content.strip()
        usage = response.usage

        success = "CONNECTION_OK" in content.upper() or len(content) > 0
        status = "✅" if success else "⚠️"
        print(f"  {status} Response: {content}")
        print(f"  ⏱️  Latency: {elapsed:.2f}s")
        if usage:
            print(
                f"  📊 Tokens: {usage.prompt_tokens} prompt + {usage.completion_tokens} completion"
            )
        print()
    except Exception as e:
        print(f"  ❌ Failed: {e}\n")
        return False

    # ── Test 3: Streaming ──────────────────────────────────
    if test_streaming:
        print("🌊 Test: Streaming")
        try:
            start = time.time()
            stream = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": "Count from 1 to 5, one number per line."},
                ],
                max_tokens=50,
                stream=True,
            )
            chunks = 0
            full_response = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content or ""
                if content:
                    full_response += content
                    chunks += 1
            elapsed = time.time() - start
            print(f"  ✅ Streamed {chunks} chunks in {elapsed:.2f}s")
            print(f"  📝 Response: {full_response.strip()}")
            print()
        except Exception as e:
            print(f"  ❌ Failed: {e}\n")

    print("─" * 60)
    print("  All tests complete!\n")
    return True


def main():
    parser = argparse.ArgumentParser(description="Test LLM provider connections")
    parser.add_argument(
        "--provider",
        choices=list(PROVIDERS.keys()),
        help="Pre-configured provider name",
    )
    parser.add_argument("--api-base", help="Custom API base URL")
    parser.add_argument("--api-key", help="API key (or set env var)")
    parser.add_argument("--model", help="Model name")
    parser.add_argument("--stream", action="store_true", help="Test streaming")
    parser.add_argument(
        "--no-models-list", action="store_true", help="Skip models list test"
    )
    args = parser.parse_args()

    if args.provider:
        config = PROVIDERS[args.provider]
        base_url = args.api_base or config["base_url"]
        model = args.model or config["model"]
        if config["env_key"]:
            api_key = args.api_key or os.environ.get(config["env_key"])
            if not api_key:
                print(f"❌ Error: Set {config['env_key']} env var or use --api-key")
                sys.exit(1)
        else:
            api_key = None
    elif args.api_base:
        base_url = args.api_base
        api_key = args.api_key or os.environ.get("API_KEY")
        model = args.model or "local-model"
    else:
        parser.print_help()
        sys.exit(1)

    test_provider(
        base_url=base_url,
        api_key=api_key,
        model=model,
        test_streaming=args.stream,
        test_models_list=not args.no_models_list,
    )


if __name__ == "__main__":
    main()
```

**Usage:**

```bash
# Test a pre-configured provider
python test_provider.py --provider venice
python test_provider.py --provider groq --stream
python test_provider.py --provider deepseek
python test_provider.py --provider ollama

# Test a custom endpoint
python test_provider.py --api-base https://my-custom-llm.example.com/v1 \
  --api-key my-key --model my-model
```

### Batch Provider Tester

Test multiple providers at once and compare results:

```python
#!/usr/bin/env python3
"""Batch test multiple LLM providers and compare results.

Usage:
    python batch_test_providers.py
    python batch_test_providers.py --providers venice groq deepseek
    python batch_test_providers.py --prompt "Explain quantum computing in one sentence."
"""

import argparse
import os
import sys
import time

try:
    from openai import OpenAI
except ImportError:
    os.system(f"{sys.executable} -m pip install openai -q")
    from openai import OpenAI


PROVIDERS = {
    "venice": {
        "base_url": "https://api.venice.ai/api/v1",
        "env_key": "VENICE_API_KEY",
        "model": "llama-3.3-70b",
    },
    "groq": {
        "base_url": "https://api.groq.com/openai/v1",
        "env_key": "GROQ_API_KEY",
        "model": "llama-3.3-70b-versatile",
    },
    "deepseek": {
        "base_url": "https://api.deepseek.com/v1",
        "env_key": "DEEPSEEK_API_KEY",
        "model": "deepseek-chat",
    },
    "together": {
        "base_url": "https://api.together.xyz/v1",
        "env_key": "TOGETHER_API_KEY",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    },
    "openrouter": {
        "base_url": "https://openrouter.ai/api/v1",
        "env_key": "OPENROUTER_API_KEY",
        "model": "meta-llama/llama-3.3-70b-instruct",
    },
    "cerebras": {
        "base_url": "https://api.cerebras.ai/v1",
        "env_key": "CEREBRAS_API_KEY",
        "model": "llama-3.3-70b",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "env_key": None,
        "model": "llama3.3",
    },
}


def test_one(provider_name: str, config: dict, prompt: str) -> dict:
    """Test a single provider. Returns result dict."""
    result = {
        "provider": provider_name,
        "model": config["model"],
        "status": "skip",
        "latency": None,
        "tokens": None,
        "error": None,
        "response": None,
    }

    if config["env_key"]:
        api_key = os.environ.get(config["env_key"])
        if not api_key:
            result["error"] = f"Missing {config['env_key']}"
            return result
    else:
        api_key = None

    try:
        client = OpenAI(api_key=api_key or "unused", base_url=config["base_url"])
        start = time.time()
        response = client.chat.completions.create(
            model=config["model"],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100,
            temperature=0,
        )
        elapsed = time.time() - start

        result["status"] = "ok"
        result["latency"] = elapsed
        result["response"] = response.choices[0].message.content.strip()[:80]
        if response.usage:
            result["tokens"] = (
                f"{response.usage.prompt_tokens}+{response.usage.completion_tokens}"
            )
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)[:60]

    return result


def main():
    parser = argparse.ArgumentParser(description="Batch test LLM providers")
    parser.add_argument(
        "--providers",
        nargs="+",
        choices=list(PROVIDERS.keys()),
        default=list(PROVIDERS.keys()),
        help="Providers to test",
    )
    parser.add_argument(
        "--prompt",
        default="Say 'hello' in 5 different languages, briefly.",
        help="Test prompt",
    )
    args = parser.parse_args()

    print(f"\n🧪 Batch Provider Test")
    print(f"   Prompt: {args.prompt[:60]}...")
    print(f"{'─'*70}")

    results = []
    for name in args.providers:
        config = PROVIDERS[name]
        print(f"  Testing {name}...", end="", flush=True)
        result = test_one(name, config, args.prompt)
        results.append(result)
        status_icon = "✅" if result["status"] == "ok" else "❌" if result["status"] == "error" else "⏭️"
        print(f" {status_icon}")

    print(f"\n{'─'*70}")
    print(f"{'Provider':<12} {'Status':<8} {'Latency':<10} {'Tokens':<12} {'Response/Error'}")
    print(f"{'─'*70}")
    for r in results:
        latency = f"{r['latency']:.2f}s" if r["latency"] else "—"
        tokens = r["tokens"] or "—"
        detail = r["response"] or r["error"] or "skipped"
        print(f"{r['provider']:<12} {r['status']:<8} {latency:<10} {tokens:<12} {detail[:40]}")
    print(f"{'─'*70}\n")


if __name__ == "__main__":
    main()
```

**Usage:**

```bash
# Test all providers that have API keys set
python batch_test_providers.py

# Test specific providers
python batch_test_providers.py --providers venice groq cerebras

# Custom prompt
python batch_test_providers.py --prompt "Write a haiku about APIs."
```

### Embedding Test

```python
#!/usr/bin/env python3
"""Test embedding provider connection.

Usage:
    python test_embedding.py --provider openai --model text-embedding-3-small
    python test_embedding.py --provider ollama --model nomic-embed-text
"""

import argparse
import os
import sys
import time

try:
    from openai import OpenAI
except ImportError:
    os.system(f"{sys.executable} -m pip install openai -q")
    from openai import OpenAI


PROVIDERS = {
    "openai": {
        "base_url": "https://api.openai.com/v1",
        "env_key": "OPENAI_API_KEY",
        "model": "text-embedding-3-small",
    },
    "venice": {
        "base_url": "https://api.venice.ai/api/v1",
        "env_key": "VENICE_API_KEY",
        "model": "text-embedding-3-small",
    },
    "mistral": {
        "base_url": "https://api.mistral.ai/v1",
        "env_key": "MISTRAL_API_KEY",
        "model": "mistral-embed",
    },
    "ollama": {
        "base_url": "http://localhost:11434/v1",
        "env_key": None,
        "model": "nomic-embed-text",
    },
    "lmstudio": {
        "base_url": "http://localhost:1234/v1",
        "env_key": None,
        "model": "text-embedding-3-small",
    },
}


def main():
    parser = argparse.ArgumentParser(description="Test embedding provider")
    parser.add_argument("--provider", choices=list(PROVIDERS.keys()))
    parser.add_argument("--model", help="Override model name")
    parser.add_argument("--api-key", help="Override API key")
    args = parser.parse_args()

    if not args.provider:
        parser.print_help()
        sys.exit(1)

    config = PROVIDERS[args.provider]
    model = args.model or config["model"]
    api_key = args.api_key
    if config["env_key"] and not api_key:
        api_key = os.environ.get(config["env_key"])
        if not api_key:
            print(f"❌ Set {config['env_key']} env var or use --api-key")
            sys.exit(1)

    client = OpenAI(api_key=api_key or "unused", base_url=config["base_url"])

    texts = [
        "The quick brown fox jumps over the lazy dog.",
        "Machine learning models process text as embeddings.",
    ]

    print(f"\n📊 Embedding Test: {args.provider} / {model}")
    print(f"   Texts: {len(texts)}")

    try:
        start = time.time()
        response = client.embeddings.create(input=texts, model=model)
        elapsed = time.time() - start

        print(f"   ✅ Success in {elapsed:.2f}s")
        for i, item in enumerate(response.data):
            print(f"   Text {i}: {len(item.embedding)} dimensions")
        if response.usage:
            print(f"   Tokens used: {response.usage.total_tokens}")
    except Exception as e:
        print(f"   ❌ Failed: {e}")


if __name__ == "__main__":
    main()
```

---

## 7. Common Patterns and Tips

### Fallback Configuration

Set up a primary provider with automatic failover:

#### Agent Zero

```yaml
# model_providers.yaml — primary + fallback
chat:
  primary:
    name: Venice AI
    litellm_provider: openai
    kwargs:
      api_base: https://api.venice.ai/api/v1
      venice_parameters:
        include_venice_system_prompt: false

  fallback:
    name: Groq
    litellm_provider: groq
    kwargs:
      api_key: "${GROQ_API_KEY}"
```

Then in Agent Zero settings:

```
chat_model_provider = primary
# If primary fails, switch to:
# chat_model_provider = fallback
```

#### LiteLLM Router

```python
from litellm import Router
import os

router = Router(
    model_list=[
        {
            "model_name": "agent-llm",
            "litellm_params": {
                "model": "openai/llama-3.3-70b",
                "api_base": "https://api.venice.ai/api/v1",
                "api_key": os.environ["VENICE_API_KEY"],
                "num_retries": 2,
                "timeout": 30,
            },
        },
        {
            "model_name": "agent-llm",
            "litellm_params": {
                "model": "groq/llama-3.3-70b-versatile",
                "api_key": os.environ["GROQ_API_KEY"],
                "num_retries": 2,
                "timeout": 15,
            },
        },
        {
            "model_name": "agent-llm",
            "litellm_params": {
                "model": "ollama/llama3.3",
                "api_base": "http://localhost:11434",
            },
        },
    ],
    fallbacks=[{"agent-llm": ["agent-llm"]}],  # Try each in order
    allowed_fails=3,
    cooldown_time=60,
)

# Call — automatically falls through on failure
response = router.completion(
    model="agent-llm",
    messages=[{"role": "user", "content": "Hello!"}],
)
```

### Cost Optimization

Route expensive tasks to cheaper providers:

| Task Type | Recommended Provider | Rationale |
|-----------|---------------------|-----------|
| **Agent reasoning** (chat) | Venice AI, DeepSeek | Quality + privacy |
| **Utility tasks** (summarization, extraction) | Groq, Cerebras | Speed + low cost |
| **Embeddings** | OpenAI `text-embedding-3-small` | Cheapest quality embeddings |
| **Local/privacy** | Ollama, LM Studio | Zero cost, full privacy |
| **Testing** | Groq free tier, Ollama | No spend risk |

Agent Zero uses three model roles — configure each independently:

```
A0_SET_chat_model_provider=venice        # Primary reasoning
A0_SET_chat_model_name=llama-3.3-70b
A0_SET_utility_model_provider=groq       # Fast, cheap internals
A0_SET_utility_model_name=llama-3.3-70b-versatile
A0_SET_embedding_model_provider=openai   # Quality embeddings
A0_SET_embedding_model_name=text-embedding-3-small
```

### Latency Optimization

| Strategy | Implementation |
|----------|---------------|
| **Choose fast providers** | Groq (LPU), Cerebras (wafer-scale), Fireworks |
| **Use streaming** | Set `stream=True` — start rendering before completion finishes |
| **Pick smaller models** | 8B models are 5-10× faster than 70B models |
| **Geographic proximity** | Pick providers with data centers near you |
| **Reduce max_tokens** | Set a ceiling to avoid runaway generation |
| **Batch requests** | Send multiple inputs in one call where supported |

### Privacy Configuration

| Need | Recommended Provider | Setup |
|------|---------------------|-------|
| **No logging, no training** | Venice AI | Set `venice_parameters.include_venice_system_prompt: false` |
| **Full data control** | Ollama, LM Studio, vLLM | Run locally, no data leaves your machine |
| **Self-hosted** | vLLM + HuggingFace | Deploy on your own GPU hardware |
| **Compliance** | Check provider ToS | Verify data processing agreements |

```yaml
# Privacy-focused Agent Zero config
chat:
  venice:
    name: Venice AI
    litellm_provider: openai
    kwargs:
      api_base: https://api.venice.ai/api/v1
      venice_parameters:
        include_venice_system_prompt: false

  ollama:
    name: Ollama Local
    litellm_provider: ollama
    kwargs:
      api_base: http://localhost:11434
```

### Rate Limit Handling

```python
import litellm
import time

# Enable built-in retries
litellm.num_retries = 3

# Or handle manually
max_retries = 5
for attempt in range(max_retries):
    try:
        response = litellm.completion(
            model="groq/llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Hello!"}],
            api_key=os.environ["GROQ_API_KEY"],
        )
        break
    except litellm.RateLimitError:
        wait = (2**attempt) + 1  # Exponential backoff
        print(f"Rate limited. Waiting {wait}s...")
        time.sleep(wait)
```

**Using multiple API keys for higher throughput:**

```python
import itertools
import litellm

keys = [
    os.environ["GROQ_API_KEY_1"],
    os.environ["GROQ_API_KEY_2"],
    os.environ["GROQ_API_KEY_3"],
]
key_cycle = itertools.cycle(keys)

for prompt in prompts:
    key = next(key_cycle)
    response = litellm.completion(
        model="groq/llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        api_key=key,
    )
```

---

## 8. Troubleshooting

### Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| **401 Unauthorized** | Invalid or missing API key | Check env var is set: `echo $VENICE_API_KEY`. Verify key is correct and active. |
| **404 Not Found** | Wrong model name or API base | Check model name with `/v1/models`. Verify API base URL ends with `/v1`. |
| **429 Too Many Requests** | Rate limit exceeded | Wait and retry with exponential backoff. Check provider dashboard for limits. |
| **500 Server Error** | Provider infrastructure issue | Retry after a few seconds. Check provider status page. |
| **502/503 Bad Gateway** | Provider overloaded or down | Retry. Switch to fallback provider. |
| **Connection refused** | API base URL wrong or service not running | For local providers: check Ollama/LM Studio is running. For remote: verify URL. |
| **Timeout** | Request took too long | Increase timeout. Try smaller model. Use streaming. |
| **Context length exceeded** | Input + output too long for model | Reduce prompt size. Use a model with larger context window. |
| **Invalid model name** | Model not found at this provider | Run `curl $API_BASE/v1/models` to list available models. |

### Debug Tools

#### curl with verbose output

```bash
curl -v https://api.venice.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $VENICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama-3.3-70b", "messages": [{"role": "user", "content": "test"}]}'
```

The `-v` flag shows:
- Connection details (DNS, TLS handshake)
- Request headers sent
- Response headers received
- HTTP status code

#### Python with logging

```python
import logging
import http.client
import os

# Enable HTTP debug logging
http.client.HTTPConnection.debuglevel = 1
logging.basicConfig()
logging.getLogger().setLevel(logging.DEBUG)

from openai import OpenAI

client = OpenAI(
    api_key=os.environ["VENICE_API_KEY"],
    base_url="https://api.venice.ai/api/v1",
)

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello"}],
    max_tokens=10,
)
print(response.choices[0].message.content)
```

#### LiteLLM debug mode

```python
import litellm

# Enable verbose debug logging
litellm.set_verbose = True

response = litellm.completion(
    model="openai/llama-3.3-70b",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="https://api.venice.ai/api/v1",
    api_key=os.environ["VENICE_API_KEY"],
)

# Logs full request/response including headers, body, and timing
```

### Provider-Specific Quirks

| Provider | Quirk | Workaround |
|----------|-------|------------|
| **Venice AI** | Double system prompts by default | Set `venice_parameters.include_venice_system_prompt: false` |
| **OpenRouter** | Missing required headers | Add `HTTP-Referer` and `X-Title` headers |
| **DeepSeek Reasoner** | Extra `reasoning_content` field | Access via `choice.message.reasoning_content` or `extra_body` |
| **Groq** | Strict rate limits on free tier | Use multiple keys or upgrade plan |
| **Together AI** | Long model names with slashes | Use exact names from `/v1/models` |
| **Fireworks AI** | `accounts/fireworks/models/` prefix | Must include the full path in model name |
| **Ollama** | Must pull model first | Run `ollama pull <model>` before querying |
| **LM Studio** | Server must be started manually | Open LM Studio → Local Server → Start |
| **vLLM** | Must specify model at server launch | Pass `--model` flag when starting vLLM server |

### Quick Diagnostic Commands

```bash
# Check if a remote provider is reachable
curl -s -o /dev/null -w "%{http_code}" https://api.venice.ai/api/v1/models \
  -H "Authorization: Bearer $VENICE_API_KEY"

# Check if a local provider is running
curl -s http://localhost:11434/v1/models 2>/dev/null && echo "Ollama: OK" || echo "Ollama: DOWN"
curl -s http://localhost:1234/v1/models 2>/dev/null && echo "LM Studio: OK" || echo "LM Studio: DOWN"
curl -s http://localhost:8000/v1/models 2>/dev/null && echo "vLLM: OK" || echo "vLLM: DOWN"

# Check if an env var is set
[ -n "$VENICE_API_KEY" ] && echo "VENICE_API_KEY: set" || echo "VENICE_API_KEY: NOT SET"

# Time a request
start=$(date +%s%N)
curl -s https://api.groq.com/openai/v1/chat/completions \
  -H "Authorization: Bearer $GROQ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": "hi"}]}' > /dev/null
end=$(date +%s%N)
echo "Latency: $(( (end - start) / 1000000 ))ms"
```

---

## Quick Reference

### Minimal Config Template

```yaml
# model_providers.yaml — minimal template for any OpenAI-compatible provider
chat:
  my-provider:
    name: My Custom Provider
    litellm_provider: openai
    kwargs:
      api_base: https://api.your-provider.com/v1
      api_key: "${YOUR_PROVIDER_API_KEY}"
```

```bash
# .env
YOUR_PROVIDER_API_KEY=your-key-here
```

```bash
# Test it
curl https://api.your-provider.com/v1/chat/completions \
  -H "Authorization: Bearer $YOUR_PROVIDER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model": "model-name", "messages": [{"role": "user", "content": "Hello"}]}'
```

### Provider Decision Matrix

| Need | Best Provider | Runner-Up |
|------|--------------|-----------|
| **Best quality** | OpenAI GPT-4o, Anthropic Claude | DeepSeek R1 |
| **Fastest inference** | Groq, Cerebras | Fireworks, SambaNova |
| **Cheapest** | Groq free tier, Together AI | DeepSeek |
| **Most models** | OpenRouter | Together AI |
| **Privacy** | Venice AI | Ollama (local) |
| **Full control** | Ollama, vLLM, LM Studio | Venice AI |
| **Reasoning** | DeepSeek R1 | Claude, OpenAI o3 |
| **Embeddings** | OpenAI | Mistral, Ollama |
| **Self-hosted** | vLLM | Ollama |

---

*Last updated: April 2025. Provider APIs, models, and pricing change frequently. Always verify against the provider's current documentation.*
