# Agent Zero Integration Guide — Tolu Memory Palace

> **Complete guide for restoring and integrating Tolu Memory Palace into a fresh or existing Agent Zero instance.**
> All code blocks are copy-paste-ready.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Restoring from Backup](#2-restoring-from-backup)
3. [Context Auto-Injection (.promptinclude.md)](#3-context-auto-injection-promptincludemd)
4. [Model Provider Configuration](#4-model-provider-configuration)
5. [Adding Venice AI as a Provider](#5-adding-venice-ai-as-a-provider)
6. [Adding Any OpenAI-Compatible Endpoint](#6-adding-any-openai-compatible-endpoint)
7. [Agent Profiles](#7-agent-profiles)
8. [Environment Variable Configuration](#8-environment-variable-configuration)
9. [Testing Your Setup](#9-testing-your-setup)
10. [Troubleshooting](#10-troubleshooting)
11. [Quick Reference Card](#quick-reference-card)

---

## 1. Overview

### What is Agent Zero?

Agent Zero is a hierarchical autonomous AI agent framework written in Python, powered by [LiteLLM](https://github.com/BerriAI/litellm) for universal LLM access. It features:

- **Hierarchical agent orchestration** — superior agents delegate to specialized subordinates
- **Tool-based execution** — JSON-structured tool calls for terminal, code, browser, memory, and more
- **Web UI** on port `50001` with real-time WebSocket communication
- **Plugin system** for extending tools, API handlers, and UI components
- **Memory system** using FAISS vector embeddings for persistent knowledge

### Three LLM Roles

| Role | Purpose | Config Key |
|------|---------|------------|
| **chat_llm** | Main reasoning, tool calling, complex tasks | `chat_model` in Settings |
| **utility_llm** | Lightweight tasks: summaries, classifications, formatting | `utility_model` in Settings |
| **embedding_llm** | Vector embeddings for memory/knowledge search | `embedding_model` in Settings |

### How Tolu Integrates

Tolu Memory Palace hooks into Agent Zero through six integration points:

| Integration Point | Mechanism | Purpose |
|---|---|---|
| **File-based restore** | `cp` / `rsync` from backup dirs | Restore knowledge, skills, plugins, agents, prompts, memory |
| **`.promptinclude.md`** | Auto-injected into system prompt | Runtime context: paths, reminders, status |
| **`model_providers.yaml`** | YAML config in `/a0/conf/` | Add custom LLM providers (Venice, local models, etc.) |
| **Agent profiles** | YAML + prompt overrides in `configs/agent-profiles/` | Specialized subordinate behavior |
| **A0_SET_ env vars** | Docker env or `.env` file | Inject API keys and configuration |
| **Scheduler tasks** | Built-in task scheduler | Automate backups and maintenance |

---

## 2. Restoring from Backup

### Backup Structure

The Tolu daily backup script (`scripts/daily-backup.sh`) mirrors Agent Zero state into the `agent-zero-backup/` directory using `rsync`:

```
Agent Zero Source                ->    Backup Destination
----------------------                ----------------------
/a0/usr/knowledge/               ->   agent-zero-backup/knowledge/
/a0/usr/agents/                  ->   agent-zero-backup/agents/
/a0/usr/skills/                  ->   agent-zero-backup/skills/
/a0/usr/plugins/                 ->   agent-zero-backup/plugins/
/a0/usr/workdir/                 ->   agent-zero-backup/workdir/
/a0/prompts/                     ->   agent-zero-backup/prompts/
/a0/usr/memory/default/          ->   agent-zero-backup/memory-export/
```

### Option A: Full Restore (Overwrite)

**Warning:** This replaces existing files in the target Agent Zero instance.

```bash
# From the Tolu repo root (where agent-zero-backup/ lives)
cd /path/to/tolu

# Restore all directories
cp -r agent-zero-backup/knowledge/    /a0/usr/knowledge/
cp -r agent-zero-backup/agents/       /a0/usr/agents/
cp -r agent-zero-backup/skills/       /a0/usr/skills/
cp -r agent-zero-backup/plugins/      /a0/usr/plugins/
cp -r agent-zero-backup/prompts/      /a0/prompts/
cp -r agent-zero-backup/workdir/      /a0/usr/workdir/

# Restore FAISS memory index
cp -r agent-zero-backup/memory-export/default/  /a0/usr/memory/default/

echo "Full restore complete"
```

### Option B: Selective Restore

Restore only specific components:

```bash
# Just skills
cp -r agent-zero-backup/skills/ /a0/usr/skills/

# Just the memory database (FAISS index)
cp -r agent-zero-backup/memory-export/default/ /a0/usr/memory/default/

# Just knowledge fragments
cp -r agent-zero-backup/knowledge/ /a0/usr/knowledge/

# Just the .promptinclude.md for context injection
cp .promptinclude.md /a0/usr/workdir/tolu/.promptinclude.md
```

### Option C: rsync Restore (Safer - Preserves Existing Files)

`rsync` with `--ignore-existing` keeps files already present in the target:

```bash
cd /path/to/tolu

# Sync everything without overwriting existing files
rsync -av --ignore-existing agent-zero-backup/knowledge/   /a0/usr/knowledge/
rsync -av --ignore-existing agent-zero-backup/agents/      /a0/usr/agents/
rsync -av --ignore-existing agent-zero-backup/skills/      /a0/usr/skills/
rsync -av --ignore-existing agent-zero-backup/plugins/     /a0/usr/plugins/
rsync -av --ignore-existing agent-zero-backup/prompts/     /a0/prompts/
rsync -av --ignore-existing agent-zero-backup/memory-export/default/ /a0/usr/memory/default/

# For workdir, exclude tolu's own directory to avoid recursion
rsync -av --ignore-existing --exclude='tolu/' agent-zero-backup/workdir/ /a0/usr/workdir/

echo "Safe restore complete (existing files preserved)"
```

### Verification Commands

```bash
# Check restored directories exist and have content
echo "=== Knowledge ===" && ls /a0/usr/knowledge/ | head -5
echo "=== Skills ==="    && ls /a0/usr/skills/    | head -5
echo "=== Plugins ==="   && ls /a0/usr/plugins/   | head -5
echo "=== Prompts ==="   && ls /a0/prompts/        | head -5
echo "=== Memory ==="    && ls /a0/usr/memory/default/

# Verify FAISS index files
ls -la /a0/usr/memory/default/index.faiss
ls -la /a0/usr/memory/default/index.pkl

# Check .promptinclude.md is in place
cat /a0/usr/workdir/tolu/.promptinclude.md | head -10

# Count restored files
echo "Knowledge files: $(find /a0/usr/knowledge/ -type f | wc -l)"
echo "Skill files:     $(find /a0/usr/skills/   -type f | wc -l)"
echo "Plugin files:    $(find /a0/usr/plugins/  -type f | wc -l)"
```

---

## 3. Context Auto-Injection (.promptinclude.md)

### How It Works

Agent Zero automatically discovers and reads all `*.promptinclude.md` files found **recursively** under `/a0/usr/workdir/`. Their contents are injected into the system prompt at runtime.

- **Discovery**: Recursive glob of `/a0/usr/workdir/**/*.promptinclude.md`
- **Ordering**: Alphabetical by full path
- **Injection**: Merged into the system prompt as a section
- **Hot-reload**: Changes take effect on the next message (no restart needed)

### Tolu's .promptinclude.md

The Tolu Memory Palace includes a `.promptinclude.md` at `/a0/usr/workdir/tolu/.promptinclude.md` that provides:

- **Memory Palace status**: GitHub repo, backup schedule
- **Quick reference paths**: All important directories in a table
- **Behavioral reminders**: Where to save knowledge, YouTube summaries, book notes
- **Backup reminders**: When to trigger backups

### Setup

```bash
# If you restored from backup, it is already in place.
# Otherwise, copy or symlink:

# Option 1: Copy
cp /path/to/tolu/.promptinclude.md /a0/usr/workdir/tolu/.promptinclude.md

# Option 2: Symlink (updates automatically if repo is pulled)
ln -s /path/to/tolu/.promptinclude.md /a0/usr/workdir/tolu/.promptinclude.md
```

### Create Custom Prompt Includes

You can create additional `.promptinclude.md` files anywhere under `/a0/usr/workdir/`:

```bash
# Example: Project-specific context
cat > /a0/usr/workdir/my-project/.promptinclude.md << 'EOF'
# My Project Context

## Conventions
- All Python code follows PEP 8 with 88-char line length (Black formatter)
- API responses use JSend spec: {status, data, message}
- Tests go in tests/ directory, mirror src/ structure

## Key Paths
- Source: /a0/usr/workdir/my-project/src/
- Tests: /a0/usr/workdir/my-project/tests/
- Config: /a0/usr/workdir/my-project/config.yml

## Reminders
- Always run linting before committing
- Use semantic versioning for releases
EOF
```

### Priority and Conflicts

- Multiple `.promptinclude.md` files are all injected - they do not override each other
- Files are injected **alphabetically by full path**, so `/a0/usr/workdir/a-project/` loads before `/a0/usr/workdir/z-project/`
- If two files define conflicting instructions, the **last one loaded** (alphabetically last path) takes precedence - but this is soft guidance, not hard override
- All includes are appended under a `### Includes` section in the system prompt with the directive: *"obey all rules preferences instructions below"*

---

## 4. Model Provider Configuration

### Configuration File

```
/a0/conf/model_providers.yaml
```

This YAML file defines all available LLM providers. It has two top-level sections:

```yaml
chat:        # Providers for chat_llm and utility_llm
  provider_id:
    name: "Human Name"
    litellm_provider: litellm_backend_name
    # ... optional fields

embedding:   # Providers for embedding_llm
  provider_id:
    name: "Human Name"
    litellm_provider: litellm_backend_name
    # ... optional fields
```

### Required Fields

| Field | Description |
|-------|-------------|
| `name` | Human-readable name shown in the Web UI dropdown |
| `litellm_provider` | The LiteLLM provider identifier (determines API protocol) |

### Optional Fields

```yaml
kwargs:                         # Extra parameters passed to LiteLLM
  api_base: https://...         # Custom API endpoint
  extra_headers:                # Custom HTTP headers
    "Header-Name": "value"
  venice_parameters:            # Provider-specific params
    include_venice_system_prompt: false

models_list:                    # Model listing configuration (for UI dropdown)
  endpoint_url: "https://..."   # URL to fetch available models
  format: "openai"              # Response format: "openai" (default), "google", "ollama"
  params:                       # Query parameters for the listing request
    limit: "1000"
  default_base: "https://..."   # Default base for local/self-hosted providers
```

### All Built-in Chat Providers

| Provider ID | Name | LiteLLM Provider |
|---|---|---|
| `a0_venice` | Agent Zero API | `openai` |
| `anthropic` | Anthropic | `anthropic` |
| `azure` | OpenAI Azure | `azure` |
| `bedrock` | AWS Bedrock | `bedrock` |
| `cometapi` | CometAPI | `cometapi` |
| `deepseek` | DeepSeek | `deepseek` |
| `github_copilot` | GitHub Copilot | `github_copilot` |
| `google` | Google | `gemini` |
| `groq` | Groq | `groq` |
| `huggingface` | HuggingFace | `huggingface` |
| `lm_studio` | LM Studio | `lm_studio` |
| `mistral` | Mistral AI | `mistral` |
| `moonshot` | Moonshot AI | `moonshot` |
| `ollama` | Ollama | `ollama` |
| `openai` | OpenAI | `openai` |
| `openrouter` | OpenRouter | `openrouter` |
| `other` | Other OpenAI compatible | `openai` |
| `sambanova` | Sambanova | `sambanova` |
| `venice` | Venice.ai | `openai` |
| `xai` | xAI | `xai` |
| `zai` | Z.AI | `openai` |
| `zai_coding` | Z.AI Coding | `openai` |

### All Built-in Embedding Providers

| Provider ID | Name | LiteLLM Provider |
|---|---|---|
| `azure` | OpenAI Azure | `azure` |
| `bedrock` | AWS Bedrock | `bedrock` |
| `google` | Google | `gemini` |
| `huggingface` | HuggingFace | `huggingface` |
| `lm_studio` | LM Studio | `lm_studio` |
| `mistral` | Mistral AI | `mistral` |
| `ollama` | Ollama | `ollama` |
| `openai` | OpenAI | `openai` |
| `openrouter` | OpenRouter | `openai` |
| `other` | Other OpenAI compatible | `openai` |

### Selecting Providers in the Web UI

1. Open Agent Zero Web UI at **`http://localhost:50001`**
2. Click **Settings** (gear icon)
3. Under **Chat Model**, select a provider from the dropdown, then select a model
4. Under **Utility Model**, select a provider and model (typically a cheaper/faster model)
5. Under **Embedding Model**, select an embedding provider and model
6. Changes take effect immediately - no restart required

---

## 5. Adding Venice AI as a Provider

Venice AI is **pre-configured** in Agent Zero's `model_providers.yaml`. You just need to add your API key.

### Current Configuration

The built-in Venice provider entry:

```yaml
# In /a0/conf/model_providers.yaml -> chat section
venice:
  name: Venice.ai
  litellm_provider: openai
  kwargs:
    api_base: https://api.venice.ai/api/v1
    venice_parameters:
      include_venice_system_prompt: false
```

### Set Your API Key

```bash
# Option 1: Standard environment variable
export VENICE_API_KEY="your-venice-api-key-here"

# Option 2: A0_SET_ prefix (strips prefix, injects into Agent Zero environment)
export A0_SET_VENICE_API_KEY="your-venice-api-key-here"

# Option 3: Docker -e flag
docker run -e VENICE_API_KEY="your-venice-api-key-here" ...

# Option 4: .env file
echo 'VENICE_API_KEY=your-venice-api-key-here' >> /a0/.env
```

### Alternative: Direct Inference Endpoint

Venice also provides a direct inference endpoint that bypasses the chat API:

```yaml
# Add a custom provider entry for Venice inference endpoint
venice_inference:
  name: Venice.ai Inference
  litellm_provider: openai
  models_list:
    endpoint_url: "https://api.venice.ai/api/inference/v1/models"
  kwargs:
    api_base: https://api.venice.ai/api/inference/v1
    venice_parameters:
      include_venice_system_prompt: false
```

### Select Venice in the UI

1. Open **Settings** in the Web UI
2. Under **Chat Model**, select **Venice.ai** from the provider dropdown
3. Select your desired model (e.g., `llama-3.3-70b`, `mistral-31b`)
4. The API key is picked up automatically from the environment variable

---

## 6. Adding Any OpenAI-Compatible Endpoint

Any service that exposes an OpenAI-compatible API can be added using the `litellm_provider: openai` pattern with a custom `api_base`.

### Basic Pattern

```yaml
# In /a0/conf/model_providers.yaml -> chat section
my_provider:
  name: My Custom Provider
  litellm_provider: openai
  kwargs:
    api_base: https://api.my-provider.com/v1
  models_list:
    endpoint_url: "https://api.my-provider.com/v1/models"
```

Then set the API key:
```bash
export MY_PROVIDER_API_KEY="your-key-here"
# or
export A0_SET_MY_PROVIDER_API_KEY="your-key-here"
```

### Example: Together AI

```yaml
together:
  name: Together AI
  litellm_provider: openai
  kwargs:
    api_base: https://api.together.xyz/v1
  models_list:
    endpoint_url: "https://api.together.xyz/v1/models"
```
```bash
export TOGETHER_API_KEY="your-together-key"
```

### Example: Fireworks AI

```yaml
fireworks:
  name: Fireworks AI
  litellm_provider: openai
  kwargs:
    api_base: https://api.fireworks.ai/inference/v1
  models_list:
    endpoint_url: "https://api.fireworks.ai/inference/v1/models"
```
```bash
export FIREWORKS_API_KEY="your-fireworks-key"
```

### Example: Groq (Already Built-in)

Groq is pre-configured, just set the key:
```bash
export GROQ_API_KEY="your-groq-key"
```

### Example: Ollama (Local)

Ollama is pre-configured with a default base URL. If Agent Zero runs in Docker:

```yaml
# Already built-in, just customize if needed:
ollama:
  name: Ollama
  litellm_provider: ollama
  models_list:
    endpoint_url: "/api/tags"
    format: "ollama"
    default_base: "http://host.docker.internal:11434"
```

If running natively on the host:
```yaml
ollama:
  name: Ollama
  litellm_provider: ollama
  models_list:
    endpoint_url: "/api/tags"
    format: "ollama"
    default_base: "http://localhost:11434"
```

### Example: LM Studio (Local)

LM Studio is pre-configured similarly to Ollama:
```yaml
lm_studio:
  name: LM Studio
  litellm_provider: lm_studio
  models_list:
    endpoint_url: "/v1/models"
    default_base: "http://host.docker.internal:1234"
```

### Quick Test: Using the `other` Provider

The `other` provider is a catch-all for quick testing - no config edits needed:

```yaml
# Already in model_providers.yaml:
other:
  name: Other OpenAI compatible
  litellm_provider: openai
```

Just set the API base and key in the Settings UI, or:
```bash
export OTHER_API_KEY="your-key"
export OTHER_API_BASE="https://your-endpoint.com/v1"
```

---

## 7. Agent Profiles

### Profile Structure

Agent profiles customize subordinate agent behavior. Each profile is a directory containing:

```
configs/agent-profiles/my-profile/
  agent.yaml                          # Profile metadata
  prompts/
    agent.system.main.communication.md    # Communication style override
    agent.system.main.specifics.md        # Domain-specific instructions
```

### agent.yaml Fields

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Display name shown in profile listings |
| `description` | string | Short description of the profile's specialization |
| `context` | string | Detailed context injected when the profile is active |

### Example: Security Researcher Profile

```yaml
# configs/agent-profiles/security-researcher/agent.yaml
title: Security Researcher
description: Agent specialized in cybersecurity, penetration testing, and vulnerability analysis.
context: >
  Use this agent for cybersecurity tasks including penetration testing,
  vulnerability assessment, security auditing, OSINT gathering, and
  threat modeling. Always follow responsible disclosure practices.
  Prioritize OWASP Top 10 and MITRE ATT&CK frameworks in analysis.
```

```markdown
<!-- configs/agent-profiles/security-researcher/prompts/agent.system.main.specifics.md -->
## Security Researcher Specifics

### Methodology
- Follow PTES (Penetration Testing Execution Standard) for engagements
- Document all findings with CVSS scores and proof-of-concept steps
- Use MITRE ATT&CK for threat classification

### Tool Preferences
- Network: nmap, masscan, rustscan
- Web: burpsuite, nikto, gobuster, ffuf
- Exploitation: metasploit, crackmapexec
- Post-exploitation: bloodhound, mimikatz
- OSINT: theHarvester, sherlock, spiderfoot

### Reporting
- Executive summary with risk ratings
- Technical findings with reproduction steps
- Remediation recommendations prioritized by impact
```

### Built-in Profiles

| Profile | Title | Description |
|---------|-------|-------------|
| `default` | Default | Base profile, inherited and overridden by specialized profiles |
| `developer` | Developer | Complex software development, debugging, refactoring, architecture |
| `researcher` | Researcher | Information gathering, data analysis, topic research, reporting |
| `hacker` | Hacker | Cyber security, penetration testing, vulnerability analysis |
| `ai-engineer` | AI Engineer | LLM integration, RAG pipelines, ML deployment, prompt engineering |

### Using Profiles with call_subordinate

In your agent conversations, specify a profile when delegating tasks:

```json
{
  "tool_name": "call_subordinate",
  "tool_args": {
    "profile": "hacker",
    "message": "Perform a security audit of the authentication module at /src/auth/",
    "reset": true
  }
}
```

```json
{
  "tool_name": "call_subordinate",
  "tool_args": {
    "profile": "researcher",
    "message": "Research the latest CVEs for Node.js Express framework and summarize.",
    "reset": true
  }
}
```

### Adding Profiles to Tolu

Store custom profiles in the Tolu repo for backup:

```bash
# Create a new profile
mkdir -p /a0/usr/workdir/tolu/configs/agent-profiles/my-profile/prompts

# Write agent.yaml
cat > /a0/usr/workdir/tolu/configs/agent-profiles/my-profile/agent.yaml << 'EOF'
title: My Custom Profile
description: Description of what this agent does.
context: Detailed context for when and how to use this agent.
EOF

# Write prompt overrides (optional)
cat > /a0/usr/workdir/tolu/configs/agent-profiles/my-profile/prompts/agent.system.main.specifics.md << 'EOF'
## My Profile Specifics

Custom instructions for this agent profile.
EOF
```

> **Note:** For Agent Zero to discover profiles, they should also exist in `/a0/usr/agents/` or be referenced by the profile system. The Tolu backup captures `/a0/usr/agents/` to `agent-zero-backup/agents/`.

---

## 8. Environment Variable Configuration

### API Key Pattern

Agent Zero uses LiteLLM's standard API key convention:

```bash
export PROVIDER_API_KEY="your-key"
```

The provider ID from `model_providers.yaml` determines the variable name:

| Provider ID | Environment Variable |
|---|---|
| `anthropic` | `ANTHROPIC_API_KEY` |
| `deepseek` | `DEEPSEEK_API_KEY` |
| `google` | `GOOGLE_API_KEY` |
| `groq` | `GROQ_API_KEY` |
| `mistral` | `MISTRAL_API_KEY` |
| `ollama` | (no key needed for local) |
| `openai` | `OPENAI_API_KEY` |
| `openrouter` | `OPENROUTER_API_KEY` |
| `other` | `OTHER_API_KEY` |
| `venice` | `VENICE_API_KEY` |
| `xai` | `XAI_API_KEY` |

### A0_SET_ Prefix

Agent Zero supports a special prefix for environment variables:

```
A0_SET_VARIABLE_NAME  ->  VARIABLE_NAME is injected into Agent Zero's environment
```

The prefix is stripped automatically. This is useful when running in Docker to avoid conflicts with host environment variables.

```bash
export A0_SET_OPENAI_API_KEY="sk-..."
export A0_SET_VENICE_API_KEY="vp-..."
export A0_SET_CUSTOM_ENDPOINT="https://..."
```

### Docker: -e Flags

```bash
docker run \
  -e OPENAI_API_KEY="sk-..." \
  -e ANTHROPIC_API_KEY="sk-ant-..." \
  -e VENICE_API_KEY="vp-..." \
  -e A0_SET_CUSTOM_CONFIG="value" \
  -p 50001:50001 \
  agent-zero
```

### Docker: .env File

```bash
# Create .env file
cat > /path/to/.env << 'EOF'
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
VENICE_API_KEY=vp-your-key-here
DEEPSEEK_API_KEY=your-key-here
GROQ_API_KEY=gsk_your-key-here
EOF

# Reference in docker run
docker run --env-file /path/to/.env -p 50001:50001 agent-zero
```

### Docker Compose

```yaml
version: "3.8"
services:
  agent-zero:
    image: agent-zero:latest
    ports:
      - "50001:50001"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - VENICE_API_KEY=${VENICE_API_KEY}
      - A0_SET_CUSTOM_FLAG=true
    env_file:
      - .env
    volumes:
      - ./agent-zero-data:/a0/usr
```

---

## 9. Testing Your Setup

### Test Provider Connection (Python)

```python
"""Test LLM provider connectivity from within Agent Zero."""
import sys
sys.path.insert(0, '/a0')

# Quick test - adjust model string as needed
# Format: provider_id/model_name
test_model = "venice/llama-3.3-70b"

try:
    from litellm import completion
    response = completion(
        model=test_model,
        messages=[{"role": "user", "content": "Say 'Agent Zero connected!' and nothing else."}],
        max_tokens=20
    )
    print(f"OK: {test_model}: {response.choices[0].message.content}")
except Exception as e:
    print(f"FAIL: {test_model}: {e}")
```

### Test Embedding Provider (Python)

```python
"""Test embedding provider connectivity."""
from litellm import embedding

try:
    response = embedding(
        model="openai/text-embedding-3-small",
        input=["Test embedding connectivity"]
    )
    dims = len(response.data[0]['embedding'])
    print(f"OK: Embedding -- dimensions: {dims}")
except Exception as e:
    print(f"FAIL: Embedding -- {e}")
```

### Verify Memory Palace Restore (Bash)

```bash
#!/bin/bash
echo "=== Tolu Memory Palace Restore Verification ==="
echo ""

# Check core directories
for dir in knowledge skills plugins agents; do
    count=$(find /a0/usr/$dir -type f 2>/dev/null | wc -l)
    if [ "$count" -gt 0 ]; then
        echo "OK: /a0/usr/$dir -- $count files"
    else
        echo "WARN: /a0/usr/$dir -- empty or missing"
    fi
done

# Check memory
echo ""
if [ -f "/a0/usr/memory/default/index.faiss" ]; then
    size=$(du -h /a0/usr/memory/default/index.faiss | cut -f1)
    echo "OK: FAISS index -- $size"
else
    echo "FAIL: FAISS index -- not found"
fi

# Check promptinclude
echo ""
if [ -f "/a0/usr/workdir/tolu/.promptinclude.md" ]; then
    echo "OK: .promptinclude.md -- found"
else
    echo "WARN: .promptinclude.md -- not found"
fi

# Check backup manifest
if [ -f "/a0/usr/workdir/tolu/MANIFEST.json" ]; then
    echo "OK: MANIFEST.json -- found"
else
    echo "WARN: MANIFEST.json -- not found"
fi

echo ""
echo "=== Verification Complete ==="
```

### Run the Verification

```bash
# Save and run
chmod +x verify-restore.sh
bash verify-restore.sh
```

---

## 10. Troubleshooting

### Provider Not Showing in UI Dropdown

**Cause:** YAML syntax error in `model_providers.yaml` or the provider ID does not match the expected format.

**Fix:**
```bash
# Validate YAML syntax
python3 -c "import yaml; yaml.safe_load(open('/a0/conf/model_providers.yaml'))" && echo "Valid YAML" || echo "YAML error"

# Check the provider entry exists
grep -A5 "my_provider:" /a0/conf/model_providers.yaml
```

**Common mistakes:**
- Incorrect indentation (YAML requires consistent spaces, not tabs)
- Missing `name` or `litellm_provider` fields
- Provider ID contains special characters

### API Key Not Recognized

**Cause:** Environment variable name does not match the provider ID convention.

**Fix:**
```bash
# Check what is set
env | grep -i "API_KEY"

# The variable name must be {PROVIDER_ID}_API_KEY (uppercase)
# For provider "venice", the variable is VENICE_API_KEY
# For provider "my_custom", the variable is MY_CUSTOM_API_KEY

# Verify the key is accessible inside the container
docker exec <container_id> env | grep API_KEY
```

### Model Not Listed in UI

**Cause:** The `models_list` configuration is missing or the endpoint is unreachable.

**Fix:**
```bash
# Test the model listing endpoint directly
curl -s -H "Authorization: Bearer $VENICE_API_KEY" \
  https://api.venice.ai/api/v1/models | python3 -m json.tool | head -30

# If using a custom endpoint, verify connectivity
curl -s https://your-api-endpoint.com/v1/models | head -20
```

**Workaround:** Type the model name manually in the UI model text field instead of using the dropdown.

### Memory Palace Not Loading

**Cause:** FAISS index files are missing, corrupted, or the embedding model changed.

**Fix:**
```bash
# Check FAISS files exist
ls -la /a0/usr/memory/default/
# Expected: index.faiss, index.pkl, embedding.json

# Verify index integrity
python3 -c "
import faiss
index = faiss.read_index('/a0/usr/memory/default/index.faiss')
print(f'FAISS index loaded: {index.ntotal} vectors')
"

# If embedding model changed, re-embed all memories via the Memory Dashboard
# in the Web UI (Settings -> Memory -> Re-embed)
```

### Agent Profile Not Used

**Cause:** Profile directory is not in the correct location or `agent.yaml` is malformed.

**Fix:**
```bash
# Check profile location -- must be discoverable by Agent Zero
find /a0 -name "agent.yaml" -path "*/agent-profiles/*" 2>/dev/null

# Validate YAML
python3 -c "
import yaml
data = yaml.safe_load(open('/path/to/agent.yaml'))
assert 'title' in data, 'Missing title'
assert 'description' in data, 'Missing description'
assert 'context' in data, 'Missing context'
print('Valid profile')
"

# When calling subordinate, use exact profile directory name
# If profile is at configs/agent-profiles/hacker/, use profile: "hacker"
```

### .promptinclude.md Not Taking Effect

**Cause:** File is not under `/a0/usr/workdir/` or does not have the exact `.promptinclude.md` extension.

**Fix:**
```bash
# Verify file location and name
find /a0/usr/workdir -name "*.promptinclude.md" 2>/dev/null

# Must end with exactly .promptinclude.md (not .promptinclude or .promptincludes.md)
# Must be under /a0/usr/workdir/ (not /a0/ or /a0/usr/)

# Test: create a simple one and check if instructions appear in agent behavior
echo "TEST: Always start responses with 'INCLUDE_LOADED'" > /a0/usr/workdir/test.promptinclude.md
# Ask the agent something -- if it starts with INCLUDE_LOADED, injection works
```

---

## Quick Reference Card

```bash
# =================================================================
# TOLU MEMORY PALACE -- AGENT ZERO QUICK REFERENCE
# =================================================================

# --- FULL RESTORE ---
cp -r /path/to/tolu/agent-zero-backup/knowledge/  /a0/usr/knowledge/
cp -r /path/to/tolu/agent-zero-backup/skills/     /a0/usr/skills/
cp -r /path/to/tolu/agent-zero-backup/plugins/    /a0/usr/plugins/
cp -r /path/to/tolu/agent-zero-backup/agents/     /a0/usr/agents/
cp -r /path/to/tolu/agent-zero-backup/prompts/    /a0/prompts/
cp -r /path/to/tolu/agent-zero-backup/memory-export/default/ /a0/usr/memory/default/

# --- SAFE RESTORE (no overwrite) ---
rsync -av --ignore-existing /path/to/tolu/agent-zero-backup/knowledge/ /a0/usr/knowledge/

# --- CONTEXT INJECTION ---
cp /path/to/tolu/.promptinclude.md /a0/usr/workdir/tolu/.promptinclude.md
# Or symlink:
ln -s /path/to/tolu/.promptinclude.md /a0/usr/workdir/tolu/.promptinclude.md

# --- API KEYS ---
export VENICE_API_KEY="vp-..."
export OPENAI_API_KEY="sk-..."
export A0_SET_CUSTOM_VAR="value"    # A0_SET_ prefix stripped automatically

# --- ADD CUSTOM PROVIDER ---
# Edit /a0/conf/model_providers.yaml:
#   chat:
#     my_provider:
#       name: My Provider
#       litellm_provider: openai
#       kwargs:
#         api_base: https://api.my-provider.com/v1
#       models_list:
#         endpoint_url: "https://api.my-provider.com/v1/models"

# --- ADD CUSTOM PROFILE ---
mkdir -p /a0/usr/workdir/tolu/configs/agent-profiles/my-profile/prompts
# Create agent.yaml with title, description, context
# Create prompts/*.md for instruction overrides

# --- VERIFY EVERYTHING ---
find /a0/usr/workdir -name "*.promptinclude.md"
ls -la /a0/usr/memory/default/index.faiss
env | grep API_KEY
python3 -c "import yaml; yaml.safe_load(open('/a0/conf/model_providers.yaml')); print('OK')"
```

---

*Last updated: 2026-04-11 | Tolu Memory Palace v1.0 | Agent Zero Framework*
