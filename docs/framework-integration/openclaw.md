# OpenClaw & Claude-Based Agent Integration Guide — Tolu Memory Palace

> **Complete guide for integrating the Tolu Memory Palace into OpenClaw, Claude Code, Cline, Continue.dev, Aider, and similar Claude-based / IDE-integrated agent frameworks.**
> All code blocks are copy-paste-ready.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Understanding the Memory Palace Structure](#2-understanding-the-memory-palace-structure)
3. [Context Injection Methods](#3-context-injection-methods)
4. [Ingesting the Memory Palace](#4-ingesting-the-memory-palace)
5. [Venice AI as a Provider for Claude-Compatible Tools](#5-venice-ai-as-a-provider-for-claude-compatible-tools)
6. [Adding Custom OpenAI-Compatible Providers](#6-adding-custom-openai-compatible-providers)
7. [Memory Palace Workflow for Claude Agents](#7-memory-palace-workflow-for-claude-agents)
8. [Example Configurations](#8-example-configurations)
9. [Troubleshooting](#9-troubleshooting)

---

## 1. Overview

### What Are Claude-Based Agent Frameworks?

Claude-based and IDE-integrated agent frameworks use **context files** — plain-text or YAML configuration files placed in the project root or home directory — to define agent behavior, available tools, and injected knowledge. These files are automatically loaded when the agent starts a session.

The major frameworks covered in this guide:

| Framework | Context File(s) | Type |
|-----------|----------------|------|
| **Claude Code** | `CLAUDE.md` | Anthropic's official CLI agent |
| **OpenClaw** | `CLAUDE.md` | Open-source Claude Code alternative |
| **Cline** | `.clinerules` | VS Code extension for agentic coding |
| **Continue.dev** | `.continue/config.json` + context files | Open-source AI code assistant |
| **Aider** | `.aider.conf.yml` | Terminal-based AI pair programmer |
| **Cursor** | `.cursorrules` | AI-native IDE |
| **Windsurf** | `.windsurfrules` | AI-powered IDE by Codeium |

### How Tolu Integrates

Tolu Memory Palace provides **structured, organized knowledge** that these frameworks can ingest as context. The integration points are:

| Integration Point | Mechanism | Purpose |
|---|---|---|
| **Context files** | CLAUDE.md, .clinerules, etc. | Inject Memory Palace paths and conventions |
| **Direct file references** | Agent reads palace files directly | Load book summaries, references, howtos |
| **Concatenated context** | Build a single mega-context file | Fit maximum palace knowledge into one injection |
| **RAG-like search** | Script to find relevant files | Load only what's needed per task |
| **Custom providers** | OpenAI-compatible endpoints | Use Venice AI, Ollama, or other LLMs |

---

## 2. Understanding the Memory Palace Structure

### Spatial Organization: Wing → Room → Hall

Tolu organizes knowledge using a **spatial memory palace** metaphor:

- **Wings** = Top-level sections (books, youtube, references, knowledge)
- **Rooms** = Subject categories within each wing
- **Halls** = Specific topics or individual files

### Directory Tree

```
tolu/
├── AGENT-BOOTSTRAP.md          # ← Ingestion manifest (read this first)
├── MANIFEST.json                # ← Machine-readable inventory
├── .promptinclude.md            # ← Auto-injection rules (Agent Zero)
├── README.md
│
├── memory-palace/               # Knowledge Vault (the "palace")
│   ├── books/
│   │   ├── summaries/           # Book summaries and key takeaways
│   │   ├── references/          # Cross-references and citations
│   │   └── reading-lists/       # Curated reading lists
│   ├── youtube/
│   │   ├── transcripts/         # Video transcripts and notes
│   │   ├── channels/            # Channel-level summaries
│   │   └── playlists/           # Playlist-level summaries
│   ├── references/
│   │   ├── tools/               # Tool documentation and API refs
│   │   ├── technical/           # Technical references
│   │   └── academic/            # Academic papers and research
│   └── knowledge/
│       ├── domain-specific/     # Specialized domain knowledge
│       ├── general/             # General knowledge
│       └── howtos/              # Step-by-step guides
│
├── prompt-library/              # Prompt engineering resources
│   ├── system-prompts/          # Agent behavior templates
│   ├── task-prompts/            # Task-specific prompts
│   ├── prompt-techniques/      # Optimization techniques
│   └── templates/               # Reusable prompt templates
│
├── skills/                     # Agent Zero skills (SKILL.md format)
├── plugins/                    # Agent Zero plugins
├── configs/                    # Agent configurations
│   ├── agent-profiles/          # Agent behavior profiles
│   ├── model-configs/           # Model configuration
│   └── scheduler-tasks/        # Scheduled tasks
│
├── scripts/                    # Automation scripts
│   └── daily-backup.sh
│
└── agent-zero-backup/          # Daily Agent Zero state backup
    ├── knowledge/
    ├── agents/
    ├── skills/
    ├── plugins/
    ├── prompts/
    ├── workdir/
    └── memory-export/
```

### Context Layers (Priority Order)

When loading context, follow this priority order:

| Priority | Layer | File | Purpose |
|----------|-------|------|--------|
| 1 (highest) | Identity | `AGENT-BOOTSTRAP.md` | What this repo is, ingestion checklist |
| 2 | Inventory | `MANIFEST.json` | Machine-readable file listing |
| 3 | Injection rules | `.promptinclude.md` | Runtime path conventions |
| 4 | Room recall | Relevant `memory-palace/` files | Domain-specific knowledge |
| 5 (lowest) | Deep search | Full directory scan | Only when needed |

### Key Files

| File | Purpose |
|------|---------|
| `AGENT-BOOTSTRAP.md` | Start-here ingestion manifest for any agent |
| `MANIFEST.json` | Machine-readable directory inventory |
| `.promptinclude.md` | Auto-injection rules (Agent Zero specific) |
| `memory-palace/README.md` | Palace navigation guide |
| `BACKUP-LOG.md` | Backup history and timestamps |

---

## 3. Context Injection Methods

Each framework uses different files for behavior configuration. Below are complete, copy-paste-ready examples for every supported framework.

### CLAUDE.md (Claude Code, OpenClaw)

Claude Code and OpenClaw auto-load `CLAUDE.md` from the **project root** directory (and optionally from `~/.claude/CLAUDE.md` for global rules). The file is plain Markdown.

```markdown
# CLAUDE.md — Project Context with Tolu Memory Palace

## Project Overview
This project integrates with the Tolu Memory Palace for persistent knowledge management.

## Memory Palace Location
The Memory Palace is at: /path/to/tolu/

## Key Paths
| Resource | Path |
|----------|------|
| Bootstrap Guide | /path/to/tolu/AGENT-BOOTSTRAP.md |
| Manifest | /path/to/tolu/MANIFEST.json |
| Books | /path/to/tolu/memory-palace/books/summaries/ |
| YouTube | /path/to/tolu/memory-palace/youtube/transcripts/ |
| References | /path/to/tolu/memory-palace/references/ |
| Knowledge | /path/to/tolu/memory-palace/knowledge/ |
| Howtos | /path/to/tolu/memory-palace/knowledge/howtos/ |
| Prompts | /path/to/tolu/prompt-library/ |

## Behavior Rules
- When the user asks about a topic, check the Memory Palace first
- Read AGENT-BOOTSTRAP.md for the full ingestion checklist
- Save new knowledge to the appropriate memory-palace/ subdirectory
- Use MANIFEST.json to discover available files
- Follow the Wing/Room/Hall organization when creating new files

## Knowledge Conventions
- Book summaries go to: memory-palace/books/summaries/
- YouTube video notes go to: memory-palace/youtube/transcripts/
- Technical references go to: memory-palace/references/technical/
- How-to guides go to: memory-palace/knowledge/howtos/
- Tool documentation goes to: memory-palace/references/tools/
- File names: use lowercase with hyphens (e.g., `building-microservices.md`)

## Saving Knowledge
When the user shares knowledge to save:
1. Determine the correct Memory Palace room (books, youtube, references, knowledge)
2. Create a markdown file with a descriptive name
3. Include: title, date, source, summary, key points
4. Cross-reference related files when applicable
```

**Setup:**

```bash
# Place at project root
cp CLAUDE.md /path/to/your/project/CLAUDE.md

# Or set global rules for all projects
mkdir -p ~/.claude
cp CLAUDE.md ~/.claude/CLAUDE.md
```

### .clinerules (Cline)

Cline reads `.clinerules` from the **project root**. The format is plain text (one rule per line) or Markdown.

```markdown
# Cline Rules — Tolu Memory Palace Integration

## Memory Palace
Location: /path/to/tolu/

## Context Files (read these first)
- /path/to/tolu/AGENT-BOOTSTRAP.md
- /path/to/tolu/MANIFEST.json

## Knowledge Directories
- Books: /path/to/tolu/memory-palace/books/summaries/
- YouTube: /path/to/tolu/memory-palace/youtube/transcripts/
- References: /path/to/tolu/memory-palace/references/
- Knowledge: /path/to/tolu/memory-palace/knowledge/
- Howtos: /path/to/tolu/memory-palace/knowledge/howtos/
- Prompts: /path/to/tolu/prompt-library/

## Behavior
- Check Memory Palace files before answering questions
- Save new knowledge to the appropriate subdirectory
- Use lowercase-hyphen file names
- Include title, date, source, and summary in all knowledge files
- Cross-reference related files when creating new entries

## File Organization (Wing/Room/Hall)
- Wing = top-level section (books, youtube, references, knowledge)
- Room = category within a wing
- Hall = specific file or topic
```

**Setup:**

```bash
# Place at project root
cp .clinerules /path/to/your/project/.clinerules
```

### .continue/ directory (Continue.dev)

Continue.dev uses `.continue/config.json` for configuration and `.continue/context/` for context files. You can also use `~/.continue/config.json` for global settings.

**config.json:**

```json
{
  "models": {
    "title": "Tolu Config"
  },
  "contextProviders": [
    {
      "name": "file",
      "params": {}
    },
    {
      "name": "folder",
      "params": {}
    }
  ],
  "customCommands": [
    {
      "name": "palace",
      "description": "Load Tolu Memory Palace context",
      "prompt": "Read and internalize the Tolu Memory Palace structure. Check these files in order: 1) /path/to/tolu/AGENT-BOOTSTRAP.md 2) /path/to/tolu/MANIFEST.json. The Memory Palace is at /path/to/tolu/. When answering questions, check the relevant room first (books/summaries, youtube/transcripts, references/, knowledge/)."
    },
    {
      "name": "book",
      "description": "Save book knowledge to palace",
      "prompt": "Save this book knowledge to the Tolu Memory Palace. Create a markdown file at /path/to/tolu/memory-palace/books/summaries/ with a descriptive lowercase-hyphen name. Include: title, author, date, summary, key takeaways, and cross-references."
    },
    {
      "name": "howto",
      "description": "Save how-to guide to palace",
      "prompt": "Save this how-to guide to the Tolu Memory Palace. Create a markdown file at /path/to/tolu/memory-palace/knowledge/howtos/ with a descriptive lowercase-hyphen name. Include: title, date, prerequisites, steps, and tips."
    }
  ]
}
```

**Setup:**

```bash
# Create .continue directory at project root
mkdir -p /path/to/your/project/.continue
cp config.json /path/to/your/project/.continue/config.json

# Or global
mkdir -p ~/.continue
cp config.json ~/.continue/config.json
```

### .aider.conf.yml (Aider)

Aider reads `.aider.conf.yml` from the project root or home directory.

```yaml
# Aider Configuration — Tolu Memory Palace Integration

# Model selection (uncomment one)
# model: claude-sonnet-4-20250514
# model: gpt-4o
# model: openai/llama-3.3-70b    # via OpenAI-compatible endpoint

# Read these files at startup for Memory Palace context
read:
  - /path/to/tolu/AGENT-BOOTSTRAP.md
  - /path/to/tolu/.promptinclude.md
  # Add specific knowledge files as needed:
  # - /path/to/tolu/memory-palace/knowledge/howtos/deploy-guide.md
  # - /path/to/tolu/memory-palace/references/tools/some-api.md

# File patterns to watch
file_patterns:
  - "*.md"
  - "*.py"
  - "*.js"
  - "*.ts"
  - "*.yaml"
  - "*.json"

# Custom instructions (multi-line)
# Aider also reads .aiderignore for excluded files

# Disable auto-commits if you prefer manual control
auto_commits: false

# Dark mode
dark_mode: true
```

You can also create a separate **instructions file** and reference it:

```bash
# Create custom instructions
mkdir -p /path/to/your/project/.aider
cat > /path/to/your/project/.aider/instructions.md << 'EOF'
# Tolu Memory Palace Integration

## Knowledge Lookup
Before answering questions about tools, techniques, or domain knowledge,
check the Memory Palace at /path/to/tolu/memory-palace/.

## Key Paths
- Books: /path/to/tolu/memory-palace/books/summaries/
- YouTube: /path/to/tolu/memory-palace/youtube/transcripts/
- References: /path/to/tolu/memory-palace/references/
- Knowledge: /path/to/tolu/memory-palace/knowledge/

## Saving Knowledge
- Book summaries → memory-palace/books/summaries/
- Video notes → memory-palace/youtube/transcripts/
- Technical docs → memory-palace/references/technical/
- How-to guides → memory-palace/knowledge/howtos/
- Use lowercase-hyphen file names
EOF

# Reference it in .aider.conf.yml
echo 'instructions_file: .aider/instructions.md' >> .aider.conf.yml
```

### Generic Approach: .cursorrules / .windsurfrules

For **Cursor**, **Windsurf**, and similar IDE agents that read a single rules file:

```markdown
# AI Assistant Rules — Tolu Memory Palace Integration

## Memory Palace
Location: /path/to/tolu/
Bootstrap: /path/to/tolu/AGENT-BOOTSTRAP.md
Manifest: /path/to/tolu/MANIFEST.json

## Context Loading Order
1. Read AGENT-BOOTSTRAP.md for full ingestion checklist
2. Check MANIFEST.json for available files
3. Load relevant room based on the current task

## Directory Map
- memory-palace/books/summaries/    → Book summaries
- memory-palace/books/references/   → Book cross-references
- memory-palace/books/reading-lists/ → Curated reading lists
- memory-palace/youtube/transcripts/ → Video transcripts and notes
- memory-palace/youtube/channels/    → Channel summaries
- memory-palace/youtube/playlists/   → Playlist summaries
- memory-palace/references/tools/    → Tool documentation
- memory-palace/references/technical/ → Technical references
- memory-palace/references/academic/ → Academic papers
- memory-palace/knowledge/domain-specific/ → Specialized domains
- memory-palace/knowledge/general/   → General knowledge
- memory-palace/knowledge/howtos/    → Step-by-step guides
- prompt-library/                    → Prompt engineering resources

## Behavior Rules
1. Check Memory Palace before answering domain questions
2. Save new knowledge to the correct room
3. File names: lowercase with hyphens (e.g., `api-design-patterns.md`)
4. Every knowledge file needs: title, date, source, summary
5. Cross-reference related files in the palace

## Knowledge File Template
```
# [Title]

> Source: [where this knowledge came from]
> Date: [YYYY-MM-DD]
> Tags: [comma-separated tags]

## Summary
[2-3 sentence overview]

## Key Points
- Point 1
- Point 2

## Details
[Full content]

## See Also
- [[related-file.md]]
```
```

**Setup:**

```bash
# For Cursor
cp .cursorrules /path/to/your/project/.cursorrules

# For Windsurf
cp .windsurfrules /path/to/your/project/.windsurfrules

# Or use the global settings in the IDE
```

---

## 4. Ingesting the Memory Palace

### Strategy 1: Direct File References

The simplest approach: reference key files in your context configuration. The agent reads them on demand.

**Best for:** Small-to-medium palaces, frameworks that support file reading.

In your context file (CLAUDE.md, .clinerules, etc.), list the paths:

```markdown
## Memory Palace — Read These First
- /path/to/tolu/AGENT-BOOTSTRAP.md
- /path/to/tolu/MANIFEST.json

## Then Load As Needed
- /path/to/tolu/memory-palace/books/summaries/    # for book questions
- /path/to/tolu/memory-palace/youtube/transcripts/ # for video content
- /path/to/tolu/memory-palace/references/          # for technical lookups
- /path/to/tolu/memory-palace/knowledge/            # for general knowledge
```

For Aider, add files to the `read:` list:

```yaml
read:
  - /path/to/tolu/AGENT-BOOTSTRAP.md
  - /path/to/tolu/memory-palace/knowledge/howtos/deploy-guide.md
```

For Claude Code / OpenClaw, use the `@file` syntax in conversation:

```
Read @/path/to/tolu/AGENT-BOOTSTRAP.md and @/path/to/tolu/MANIFEST.json
then help me find information about [topic]
```

### Strategy 2: Concatenated Context

Build a single context file from all palace content. Useful when you need everything loaded at once.

**Best for:** When context window is large enough, or you want zero-latency knowledge access.

```bash
#!/usr/bin/env bash
# build-context.sh — Concatenate Memory Palace into a single context file
#
# Usage: ./build-context.sh /path/to/tolu > palace-context.md

set -euo pipefail

TOLU_ROOT="${1:?Usage: $0 /path/to/tolu}"
OUTPUT="${2:-palace-context.md}"

echo "# Tolu Memory Palace — Combined Context"
echo "# Generated: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

# Section header helper
section() {
  echo ""
  echo "---"
  echo "## $1"
  echo ""
}

# Core files
section "Bootstrap Manifest"
cat "$TOLU_ROOT/AGENT-BOOTSTRAP.md"

section "Directory Inventory"
cat "$TOLU_ROOT/MANIFEST.json"

# Memory Palace rooms
for wing in books youtube references knowledge; do
  wing_dir="$TOLU_ROOT/memory-palace/$wing"
  if [ -d "$wing_dir" ]; then
    section "Wing: $wing"
    find "$wing_dir" -name '*.md' -type f | sort | while read -r file; do
      room=$(dirname "${file#$wing_dir/}")
      section "$wing / $room / $(basename "$file")"
      cat "$file"
    done
  fi
done

# Prompt library
if [ -d "$TOLU_ROOT/prompt-library" ]; then
  section "Prompt Library"
  find "$TOLU_ROOT/prompt-library" -name '*.md' -type f | sort | while read -r file; do
    section "Prompts / $(basename "$file")"
    cat "$file"
  done
fi

echo ""
echo "---"
echo "# End of Memory Palace Context"

# Report
count=$(grep -c '^## ' "$OUTPUT" 2>/dev/null || echo '?')
echo "Built context with $count sections → $OUTPUT" >&2
```

**Usage:**

```bash
chmod +x build-context.sh
./build-context.sh /path/to/tolu palace-context.md

# Now reference this single file in your context config
# CLAUDE.md: "Read palace-context.md for full Memory Palace context"
# Aider: add to read: list
```

### Strategy 3: Selective Loading

Load only the rooms relevant to the current task. This conserves context window space.

**Best for:** Large palaces, focused tasks, limited context windows.

```bash
#!/usr/bin/env bash
# load-room.sh — Load specific Memory Palace rooms
#
# Usage: ./load-room.sh /path/to/tolu books summaries
#        ./load-room.sh /path/to/tolu youtube transcripts
#        ./load-room.sh /path/to/tolu references technical
#        ./load-room.sh /path/to/tolu knowledge howtos

set -euo pipefail

TOLU_ROOT="${1:?Usage: $0 /path/to/tolu wing [room]}"
WING="${2:?Specify a wing: books, youtube, references, knowledge}"
ROOM="${3:-}"  # optional sub-room

if [ -n "$ROOM" ]; then
  TARGET="$TOLU_ROOT/memory-palace/$WING/$ROOM"
else
  TARGET="$TOLU_ROOT/memory-palace/$WING"
fi

if [ ! -d "$TARGET" ]; then
  echo "Error: Directory not found: $TARGET" >&2
  echo "Available wings: books youtube references knowledge" >&2
  exit 1
fi

echo "# Memory Palace Room: $WING${ROOM:+/$ROOM}"
echo "# Loaded: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
echo ""

find "$TARGET" -name '*.md' -type f | sort | while read -r file; do
  echo ""
  echo "---"
  echo "## File: ${file#$TOLU_ROOT/memory-palace/}"
  echo ""
  cat "$file"
done

file_count=$(find "$TARGET" -name '*.md' -type f | wc -l)
echo "" >&2
echo "Loaded $file_count files from $WING${ROOM:+/$ROOM}" >&2
```

**Usage examples:**

```bash
# Load all book summaries
./load-room.sh /path/to/tolu books summaries > context-books.md

# Load all YouTube transcripts
./load-room.sh /path/to/tolu youtube transcripts > context-youtube.md

# Load all technical references
./load-room.sh /path/to/tolu references technical > context-tech.md

# Load the entire knowledge wing
./load-room.sh /path/to/tolu knowledge > context-knowledge.md
```

### Strategy 4: RAG-like Approach (Semantic Search)

Use embeddings to find and load only the most relevant files for the current task. This is the most context-efficient approach.

**Best for:** Very large palaces, complex tasks spanning multiple rooms, minimal context budgets.

```python
#!/usr/bin/env python3
"""palace-search.py — Semantic search across the Tolu Memory Palace.

Uses sentence-transformers for local embeddings (no API key needed).
Finds the most relevant files for a given query.

Usage:
    python palace-search.py /path/to/tolu "how to deploy microservices"
    python palace-search.py /path/to/tolu "kubernetes patterns" --top 5
    python palace-search.py /path/to/tolu "API design" --output context.md

Install:
    pip install sentence-transformers
"""

import argparse
import os
import sys
from pathlib import Path


def find_markdown_files(root: str) -> list[Path]:
    """Find all markdown files in the Memory Palace."""
    palace_dir = Path(root) / "memory-palace"
    if not palace_dir.exists():
        palace_dir = Path(root)
    return sorted(palace_dir.rglob("*.md"))


def build_index(files: list[Path], model) -> tuple[list[dict], list]:
    """Build embedding index from files."""
    from sentence_transformers import SentenceTransformer
    import numpy as np

    documents = []
    for f in files:
        try:
            content = f.read_text(encoding="utf-8", errors="ignore")
            if content.strip():
                documents.append({
                    "path": str(f),
                    "content": content,
                    "name": f.name,
                    "rel_path": str(f.relative_to(f.parents[3])),  # relative to tolu/
                })
        except Exception:
            continue

    if not documents:
        print("No documents found.", file=sys.stderr)
        sys.exit(1)

    # Build embeddings
    texts = [f"{d['name']}: {d['content'][:500]}" for d in documents]
    embeddings = model.encode(texts, show_progress_bar=True)

    return documents, embeddings


def search(query: str, documents: list[dict], embeddings, model, top_k: int = 3) -> list[dict]:
    """Find the most relevant documents for a query."""
    import numpy as np

    query_embedding = model.encode([query])
    # Cosine similarity
    similarities = np.dot(embeddings, query_embedding.T).flatten()
    top_indices = np.argsort(similarities)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            **documents[idx],
            "score": float(similarities[idx]),
        })

    return results


def main():
    parser = argparse.ArgumentParser(description="Search the Tolu Memory Palace")
    parser.add_argument("root", help="Path to Tolu repo root")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--top", type=int, default=3, help="Number of results")
    parser.add_argument("--output", "-o", help="Output file for combined context")
    parser.add_argument("--model", default="all-MiniLM-L6-v2",
                        help="Sentence transformer model name")
    args = parser.parse_args()

    from sentence_transformers import SentenceTransformer

    print(f"Loading model: {args.model}...", file=sys.stderr)
    model = SentenceTransformer(args.model)

    print("Indexing Memory Palace...", file=sys.stderr)
    files = find_markdown_files(args.root)
    print(f"Found {len(files)} markdown files", file=sys.stderr)

    documents, embeddings = build_index(files, model)

    print(f"Searching for: {args.query}", file=sys.stderr)
    results = search(args.query, documents, embeddings, model, top_k=args.top)

    # Output
    output_lines = []
    for i, result in enumerate(results, 1):
        print(f"\n{i}. {result['rel_path']} (score: {result['score']:.3f})")
        print(f"   {result['content'][:150]}...")

        output_lines.append(f"## Result {i}: {result['rel_path']}")
        output_lines.append(f"> Relevance: {result['score']:.3f}")
        output_lines.append("")
        output_lines.append(result['content'])
        output_lines.append("")

    if args.output:
        with open(args.output, "w") as f:
            f.write(f"# Memory Palace Search: {args.query}\n")
            f.write(f"# Generated: {__import__('datetime').datetime.utcnow().isoformat()}Z\n")
            f.write("\n")
            f.write("\n".join(output_lines))
        print(f"\nContext written to: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
```

**Usage:**

```bash
# Install dependency
pip install sentence-transformers

# Search the palace
python palace-search.py /path/to/tolu "microservices deployment patterns" --top 3

# Search and save context file
python palace-search.py /path/to/tolu "API authentication best practices" --top 5 -o context.md
```

---

## 5. Venice AI as a Provider for Claude-Compatible Tools

[Venice AI](https://venice.ai) provides an **OpenAI-compatible API** that works with any tool accepting OpenAI-formatted endpoints. This is useful for:

- **Privacy**: No prompt logging or training on your data
- **Uncensored models**: Access to models without content restrictions
- **Cost-effective**: Competitive pricing for powerful models
- **OpenAI-compatible**: Drop-in replacement for OpenAI API

### API Details

| Setting | Value |
|---------|-------|
| **Chat API Base** | `https://api.venice.ai/api/inference/v1` |
| **Alt Chat API Base** | `https://api.venice.ai/api/v1` |
| **Models List** | `https://api.venice.ai/api/inference/v1/models` |
| **Auth Header** | `Authorization: Bearer <VENICE_API_KEY>` |
| **API Key Env Var** | `VENICE_API_KEY` |

### Continue.dev — Venice AI Configuration

Edit `.continue/config.json`:

```json
{
  "models": [
    {
      "title": "Venice AI — Llama 3.3 70B",
      "provider": "openai",
      "model": "llama-3.3-70b",
      "apiBase": "https://api.venice.ai/api/inference/v1",
      "apiKey": "${VENICE_API_KEY}"
    },
    {
      "title": "Venice AI — Mistral 31B",
      "provider": "openai",
      "model": "mistral-31b",
      "apiBase": "https://api.venice.ai/api/inference/v1",
      "apiKey": "${VENICE_API_KEY}"
    },
    {
      "title": "Venice AI — DeepSeek R1",
      "provider": "openai",
      "model": "deepseek-r1-671b",
      "apiBase": "https://api.venice.ai/api/inference/v1",
      "apiKey": "${VENICE_API_KEY}"
    }
  ]
}
```

Set your API key:

```bash
export VENICE_API_KEY="your-venice-api-key-here"
```

### Cline — Venice AI Configuration

In Cline's settings (VS Code → Settings → Cline):

1. Set **API Provider** to `OpenAI Compatible`
2. Set **Base URL** to `https://api.venice.ai/api/inference/v1`
3. Set **API Key** to your Venice API key
4. Set **Model** to e.g., `llama-3.3-70b`

Or via VS Code `settings.json`:

```json
{
  "cline.apiProvider": "openai-compatible",
  "cline.openAiCompatibleBaseUrl": "https://api.venice.ai/api/inference/v1",
  "cline.openAiCompatibleApiKey": "your-venice-api-key",
  "cline.openAiCompatibleModelId": "llama-3.3-70b"
}
```

### Aider — Venice AI Configuration

```bash
# Using --openai-api-base flag
aider --openai-api-base https://api.venice.ai/api/inference/v1 \
      --model openai/llama-3.3-70b

# Set API key
export OPENAI_API_KEY="your-venice-api-key"
```

Or in `.aider.conf.yml`:

```yaml
model: openai/llama-3.3-70b
openai-api-base: https://api.venice.ai/api/inference/v1
# Set OPENAI_API_KEY env var to your Venice key
```

### Claude Code / OpenClaw — Venice AI Configuration

Claude Code and OpenClaw are Anthropic-native and don't natively support OpenAI-compatible endpoints. However, you can:

1. **Use a proxy**: Run [LiteLLM Proxy](https://docs.litellm.ai/docs/proxy/user_keys) to translate OpenAI ↔ Anthropic:

```bash
pip install litellm[proxy]

# Start proxy translating Venice to Anthropic format
litellm --model openai/llama-3.3-70b \
        --api_base https://api.venice.ai/api/inference/v1 \
        --port 4000

# Then point Claude Code at the proxy
export ANTHROPIC_API_KEY=anything  # proxy handles auth
export ANTHROPIC_BASE_URL=http://localhost:4000
```

2. **Use OpenRouter**: OpenRouter provides Venice models via their unified API.

3. **Stick with Anthropic models**: Use Claude natively and use Venice for other tools (Cline, Aider, Continue.dev).

---

## 6. Adding Custom OpenAI-Compatible Providers

Any service with an OpenAI-compatible API follows the same pattern:

```
api_base  +  api_key  +  model_name
```

### Common Providers

| Provider | API Base | Env Var |
|----------|----------|--------|
| **Venice AI** | `https://api.venice.ai/api/inference/v1` | `VENICE_API_KEY` |
| **Together AI** | `https://api.together.xyz/v1` | `TOGETHER_API_KEY` |
| **Fireworks AI** | `https://api.fireworks.ai/inference/v1` | `FIREWORKS_API_KEY` |
| **Groq** | `https://api.groq.com/openai/v1` | `GROQ_API_KEY` |
| **OpenRouter** | `https://openrouter.ai/api/v1` | `OPENROUTER_API_KEY` |
| **Ollama (local)** | `http://localhost:11434/v1` | (none) |
| **LM Studio (local)** | `http://localhost:1234/v1` | (none) |

### Per-Tool Configuration

#### Continue.dev

```json
{
  "models": [
    {
      "title": "Together — Llama 3.1 70B",
      "provider": "openai",
      "model": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
      "apiBase": "https://api.together.xyz/v1",
      "apiKey": "${TOGETHER_API_KEY}"
    },
    {
      "title": "Groq — Llama 3.3 70B",
      "provider": "openai",
      "model": "llama-3.3-70b-versatile",
      "apiBase": "https://api.groq.com/openai/v1",
      "apiKey": "${GROQ_API_KEY}"
    },
    {
      "title": "Ollama — Local",
      "provider": "ollama",
      "model": "llama3.1:70b",
      "apiBase": "http://localhost:11434"
    },
    {
      "title": "Fireworks — Llama 3.1 70B",
      "provider": "openai",
      "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
      "apiBase": "https://api.fireworks.ai/inference/v1",
      "apiKey": "${FIREWORKS_API_KEY}"
    }
  ]
}
```

#### Cline

```json
{
  "cline.apiProvider": "openai-compatible",
  "cline.openAiCompatibleBaseUrl": "https://api.together.xyz/v1",
  "cline.openAiCompatibleApiKey": "your-key",
  "cline.openAiCompatibleModelId": "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
}
```

#### Aider

```bash
# Together AI
export OPENAI_API_KEY="your-together-key"
aider --openai-api-base https://api.together.xyz/v1 \
      --model openai/meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo

# Groq
export OPENAI_API_KEY="your-groq-key"
aider --openai-api-base https://api.groq.com/openai/v1 \
      --model openai/llama-3.3-70b-versatile

# Local Ollama (no key needed)
aider --openai-api-base http://localhost:11434/v1 \
      --model openai/llama3.1:70b

# LM Studio (no key needed)
aider --openai-api-base http://localhost:1234/v1 \
      --model openai/the-model-you-loaded
```

#### Cursor / Windsurf

In the IDE settings under **Models** → **Add Custom Model**:

- **OpenAI API Base**: Your provider's API base URL
- **API Key**: Your provider's API key
- **Model Name**: The model identifier

---

## 7. Memory Palace Workflow for Claude Agents

### Reading from the Palace (Lookup Context)

When a user asks a question that might be answered by palace content:

1. **Check the manifest first** — `MANIFEST.json` tells you what's available
2. **Navigate to the correct wing** — books, youtube, references, or knowledge
3. **Scan the relevant room** — list files in the target directory
4. **Read the most relevant files** — use `cat` or file reading tools
5. **Synthesize and answer** — combine palace knowledge with your own

**Example lookup flow:**

```
User: "What did I save about microservices from that YouTube video?"

Agent steps:
1. List files in memory-palace/youtube/transcripts/
2. Find: building-microservices-2024.md
3. Read the file
4. Summarize and answer
```

### Writing to the Palace (Save New Knowledge)

When the user wants to save knowledge:

1. **Determine the correct room** using this decision tree:

```
Is it from a book?          → memory-palace/books/summaries/
Is it from a YouTube video? → memory-palace/youtube/transcripts/
Is it a tool/API reference? → memory-palace/references/tools/
Is it a technical concept?  → memory-palace/references/technical/
Is it academic research?    → memory-palace/references/academic/
Is it domain-specific?      → memory-palace/knowledge/domain-specific/
Is it a general fact?       → memory-palace/knowledge/general/
Is it a how-to guide?       → memory-palace/knowledge/howtos/
```

2. **Create the file** using the standard template:

```markdown
# [Title]

> Source: [Book title / YouTube URL / URL / etc.]
> Date: YYYY-MM-DD
> Tags: tag1, tag2, tag3

## Summary
[2-3 sentence overview]

## Key Points
- Point 1
- Point 2
- Point 3

## Details
[Full content — methods, arguments, examples, etc.]

## See Also
- [[related-file-in-the-palace.md]]
- [[another-related-file.md]]
```

3. **File naming convention**:
   - Lowercase with hyphens: `building-microservices.md`
   - Include year for dated content: `kubernetes-patterns-2024.md`
   - Be descriptive but concise: `api-auth-jwt.md` not `notes.md`

### Cross-Referencing Between Rooms

Use `[[wikilink]]`-style references within knowledge files:

```markdown
# Kubernetes Deployment Guide

> Date: 2025-01-15
> Tags: kubernetes, devops, deployment

## Summary
Step-by-step guide for deploying applications to Kubernetes clusters.

## See Also
- [[kubernetes-patterns.md]]           # in references/technical/
- [[building-microservices-2024.md]]   # in youtube/transcripts/
- [[docker-best-practices.md]]         # in knowledge/howtos/
```

### Updating Existing Entries

When the user provides updated information:

1. Find the existing file
2. Append an update section rather than overwriting:

```markdown
## Update — YYYY-MM-DD

Additional information from [source]:
- New point 1
- New point 2
```

---

## 8. Example Configurations

### Complete CLAUDE.md (Claude Code / OpenClaw)

```markdown
# CLAUDE.md

## Project: My Application
This is a [description] built with [stack].

## Architecture
- Backend: [framework/language]
- Frontend: [framework]
- Database: [database]
- Deployment: [platform]

## Conventions
- [coding style, naming, patterns]
- [testing requirements]
- [commit message format]

## Tolu Memory Palace
Palace root: /path/to/tolu/
Bootstrap: /path/to/tolu/AGENT-BOOTSTRAP.md
Manifest: /path/to/tolu/MANIFEST.json

### Key Paths
| Resource | Path |
|----------|------|
| Books | /path/to/tolu/memory-palace/books/summaries/ |
| YouTube | /path/to/tolu/memory-palace/youtube/transcripts/ |
| References | /path/to/tolu/memory-palace/references/ |
| Knowledge | /path/to/tolu/memory-palace/knowledge/ |
| Howtos | /path/to/tolu/memory-palace/knowledge/howtos/ |
| Prompts | /path/to/tolu/prompt-library/ |

### Rules
- Check palace files before answering domain questions
- Save new knowledge to the appropriate room
- Use lowercase-hyphen file names
- Include: title, date, source, summary in every file
- Cross-reference related palace files
```

### Complete .clinerules (Cline)

```
# Cline Project Rules

## Stack
- Language: TypeScript
- Framework: Next.js 14
- Styling: Tailwind CSS
- Database: PostgreSQL with Prisma

## Memory Palace
Root: /path/to/tolu/
Bootstrap: /path/to/tolu/AGENT-BOOTSTRAP.md
Rooms:
  books: /path/to/tolu/memory-palace/books/summaries/
  youtube: /path/to/tolu/memory-palace/youtube/transcripts/
  references: /path/to/tolu/memory-palace/references/
  knowledge: /path/to/tolu/memory-palace/knowledge/
  howtos: /path/to/tolu/memory-palace/knowledge/howtos/

## Rules
- Check Memory Palace for relevant context before coding
- Save new patterns and solutions to the palace
- Follow the Wing/Room/Hall structure
- File names: lowercase-hyphen.md
- Every file: title, date, source, summary

## Code Style
- Use strict TypeScript
- Prefer const over let
- Use named exports
- Error handling: try/catch with typed errors
- Tests: vitest with Testing Library
```

### Complete Continue.dev config.json

```json
{
  "models": [
    {
      "title": "Claude Sonnet 4",
      "provider": "anthropic",
      "model": "claude-sonnet-4-20250514",
      "apiKey": "${ANTHROPIC_API_KEY}"
    },
    {
      "title": "Venice — Llama 3.3 70B",
      "provider": "openai",
      "model": "llama-3.3-70b",
      "apiBase": "https://api.venice.ai/api/inference/v1",
      "apiKey": "${VENICE_API_KEY}"
    },
    {
      "title": "Ollama — Local",
      "provider": "ollama",
      "model": "llama3.1:70b",
      "apiBase": "http://localhost:11434"
    }
  ],
  "tabAutocompleteModel": {
    "title": "Tab Autocomplete",
    "provider": "ollama",
    "model": "qwen2.5-coder:1.5b"
  },
  "customCommands": [
    {
      "name": "palace",
      "description": "Load Tolu Memory Palace context",
      "prompt": "Read /path/to/tolu/AGENT-BOOTSTRAP.md and internalize the Memory Palace structure. The palace is at /path/to/tolu/. Check relevant rooms (books/summaries, youtube/transcripts, references/, knowledge/) for context before answering."
    },
    {
      "name": "book",
      "description": "Save book knowledge to palace",
      "prompt": "Save this book knowledge to /path/to/tolu/memory-palace/books/summaries/ as a markdown file with lowercase-hyphen name. Include: title, author, date, summary, key takeaways."
    },
    {
      "name": "ref",
      "description": "Save technical reference to palace",
      "prompt": "Save this reference to /path/to/tolu/memory-palace/references/technical/ as a markdown file. Include: title, date, source, summary, details."
    },
    {
      "name": "howto",
      "description": "Save how-to guide to palace",
      "prompt": "Save this guide to /path/to/tolu/memory-palace/knowledge/howtos/ as a markdown file. Include: title, date, prerequisites, steps, tips."
    }
  ],
  "contextProviders": [
    { "name": "file" },
    { "name": "folder" },
    { "name": "codebase" }
  ]
}
```

### Complete Aider Configuration

**`.aider.conf.yml`:**

```yaml
# Aider Configuration with Tolu Memory Palace

# Model
model: claude-sonnet-4-20250514

# Files to read at startup
read:
  - /path/to/tolu/AGENT-BOOTSTRAP.md
  - /path/to/tolu/memory-palace/knowledge/howtos/
  # Add task-relevant files:
  # - /path/to/tolu/memory-palace/references/technical/some-topic.md

# Custom instructions file
instructions_file: .aider/instructions.md

# File patterns
file_patterns:
  - "*.md"
  - "*.py"
  - "*.ts"
  - "*.tsx"
  - "*.js"
  - "*.yaml"
  - "*.json"

# Behavior
auto_commits: false
dark_mode: true
map_tokens: 2048

# Alternative: Venice AI as provider
# model: openai/llama-3.3-70b
# openai-api-base: https://api.venice.ai/api/inference/v1
# (set OPENAI_API_KEY to your Venice key)
```

**`.aider/instructions.md`:**

```markdown
# Tolu Memory Palace Integration

## Context Loading
The Memory Palace is at /path/to/tolu/.
Read AGENT-BOOTSTRAP.md for the full ingestion checklist.

## Key Paths
- Books: memory-palace/books/summaries/
- YouTube: memory-palace/youtube/transcripts/
- References: memory-palace/references/
- Knowledge: memory-palace/knowledge/
- Howtos: memory-palace/knowledge/howtos/

## Rules
1. Check palace files for relevant context
2. Save solutions and patterns to the palace
3. File names: lowercase-hyphen.md
4. Every file: title, date, source, summary
```

---

## 9. Troubleshooting

### Context Window Limits

**Problem:** The Memory Palace is too large to fit in a single context window.

**Solutions:**

1. **Use Selective Loading** (Strategy 3) — only load relevant rooms
2. **Use RAG-like Search** (Strategy 4) — find only the most relevant files
3. **Use Concatenation with Size Limits:**

```bash
# Build context limited to ~50KB
./build-context.sh /path/to/tolu | head -c 50000 > context.md
```

4. **Reduce file content** — strip boilerplate before loading:

```bash
# Strip lines starting with '#' and empty lines
find memory-palace/ -name '*.md' -exec cat {} \; \
  | grep -v '^#' | grep -v '^$' > compact-context.md
```

5. **Use a two-phase approach** — first load MANIFEST.json to find relevant files, then load only those:

```
Phase 1: "Read MANIFEST.json and tell me which files relate to [topic]"
Phase 2: "Now read [specific-files] and answer my question"
```

### File Encoding Issues

**Problem:** Agent can't read files with special characters.

**Solutions:**

```bash
# Check file encoding
file -i /path/to/tolu/memory-palace/**/*.md

# Convert to UTF-8
find /path/to/tolu/memory-palace/ -name '*.md' -exec \
  iconv -f ISO-8859-1 -t UTF-8 {} -o {}.utf8 \; \
  -exec mv {}.utf8 {} \;

# Fix line endings
find /path/to/tolu/memory-palace/ -name '*.md' -exec \
  sed -i 's/\r$//' {} \;
```

### Path Resolution

**Problem:** Agent can't find files — wrong paths.

**Solutions:**

1. Always use **absolute paths** in context files
2. Test paths manually:

```bash
ls /path/to/tolu/AGENT-BOOTSTRAP.md
ls /path/to/tolu/memory-palace/books/summaries/
```

3. Use environment variables for portability:

```bash
export TOLU_ROOT=/path/to/tolu

# Then in context files reference:
# $TOLU_ROOT/AGENT-BOOTSTRAP.md
# $TOLU_ROOT/memory-palace/books/summaries/
```

4. For relative paths, ensure they're relative to the **project root** (where the context file lives), not the user's home directory.

### Provider Connection Issues

**Problem:** Can't connect to Venice AI or other providers.

**Solutions:**

```bash
# Test Venice AI connectivity
curl -s https://api.venice.ai/api/inference/v1/models \
  -H "Authorization: Bearer $VENICE_API_KEY" | head -20

# Test a chat completion
curl -s https://api.venice.ai/api/inference/v1/chat/completions \
  -H "Authorization: Bearer $VENICE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama-3.3-70b",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 50
  }'

# Test Ollama locally
curl -s http://localhost:11434/v1/models

# Test Together AI
curl -s https://api.together.xyz/v1/models \
  -H "Authorization: Bearer $TOGETHER_API_KEY" | head -20
```

**Common issues:**

| Symptom | Cause | Fix |
|---------|-------|-----|
| 401 Unauthorized | Wrong or missing API key | Check env var is set and exported |
| 404 Not Found | Wrong model name | Check model ID with `curl /v1/models` |
| Connection refused | Local server not running | Start Ollama/LM Studio first |
| Timeout | Network or proxy issue | Check firewall, VPN, proxy settings |
| 429 Rate Limit | Too many requests | Add retry logic or reduce request rate |

### Framework-Specific Issues

#### Claude Code / OpenClaw
- `CLAUDE.md` must be in the **project root** where `claude` is launched
- Global rules go in `~/.claude/CLAUDE.md`
- File references with `@file` syntax work only for paths within the project

#### Cline
- `.clinerules` must be in the **workspace root**
- For multi-root workspaces, place `.clinerules` in each root
- VS Code settings override `.clinerules` if both define the same setting

#### Continue.dev
- `.continue/` directory must be in the **workspace root**
- `config.json` must be valid JSON (no comments)
- `${ENV_VAR}` syntax works for API keys in config

#### Aider
- `.aider.conf.yml` can be in project root or `~/.aider.conf.yml`
- `read:` files are loaded at startup — too many files slows startup
- Use `--model` flag to override config file model

#### Cursor / Windsurf
- `.cursorrules` / `.windsurfrules` must be in project root
- Rules file has a size limit (~8KB for Cursor) — use concise instructions
- For larger context, reference external files and let the agent read them

---

*Last updated: 2025-04-11*
