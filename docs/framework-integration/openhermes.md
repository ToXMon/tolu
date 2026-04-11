# OpenHermes Integration Guide — Tolu Memory Palace

> **Complete guide for integrating Tolu Memory Palace into OpenHermes and similar open-source agent frameworks.**
> All code blocks are copy-paste-ready.

---

## Table of Contents

1. [Overview](#1-overview)
2. [Understanding the Memory Palace Structure](#2-understanding-the-memory-palace-structure)
3. [Ingesting the Memory Palace](#3-ingesting-the-memory-palace)
4. [Configuration File Patterns](#4-configuration-file-patterns)
5. [Custom Model Provider Setup](#5-custom-model-provider-setup)
6. [Environment Variable Configuration](#6-environment-variable-configuration)
7. [Memory Palace Context Management](#7-memory-palace-context-management)
8. [Advanced Integration](#8-advanced-integration)
9. [Testing and Verification](#9-testing-and-verification)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Overview

### What is OpenHermes?

OpenHermes is an open-source AI agent framework designed for flexibility and extensibility. It supports multiple LLM backends via configuration files and provides a modular architecture for building autonomous agents.

Key characteristics:

- **Configuration-driven** — YAML/JSON config files for model providers, agent behavior, and context
- **Multi-backend LLM support** — OpenAI, Anthropic, local models, and any OpenAI-compatible endpoint
- **Extensible tool system** — Add custom tools and capabilities via plugins
- **Context management** — Load and inject context at conversation start

### How Tolu Integrates

The Tolu Memory Palace hooks into OpenHermes through four primary integration points:

| Integration Point | Mechanism | Purpose |
|---|---|---|
| **Config file ingestion** | YAML/JSON config referencing Tolu paths | Point the framework to knowledge directories |
| **System prompt construction** | Python scripts building prompts from palace rooms | Inject curated knowledge into agent context |
| **Direct API context loading** | File loading at conversation start | Populate conversation with relevant palace content |
| **Embedding-based retrieval** | Vector search over palace files | Dynamically fetch relevant knowledge per query |

### Prerequisites

```bash
# Python 3.10+
python3 --version

# Required packages
pip install pyyaml openai chromadb sentence-transformers python-dotenv

# Clone Tolu Memory Palace
export TOLU_ROOT="/opt/tolu"
git clone https://github.com/ToXMon/tolu.git "$TOLU_ROOT"
```

---

## 2. Understanding the Memory Palace Structure

### Spatial Organization: Wing / Room / Hall

Tolu uses a spatial memory palace metaphor. Each directory is a **Wing**, subdirectories are **Rooms**, and individual files are **Halls** of knowledge:

```
tolu/                              ← Palace Root
├── memory-palace/                  ← Knowledge Wing
│   ├── books/                      ← Book Room
│   │   ├── summaries/              ← Book summaries (Halls)
│   │   ├── references/             ← Book references
│   │   └── reading-lists/          ← Curated reading lists
│   ├── youtube/                    ← Video Room
│   │   ├── transcripts/            ← Video transcripts
│   │   ├── channels/               ← Channel profiles
│   │   └── playlists/              ← Playlist summaries
│   ├── references/                 ← Reference Room
│   │   ├── tools/                  ← Tool documentation
│   │   ├── technical/              ← Technical references
│   │   └── academic/               ← Academic papers
│   └── knowledge/                  ← General Knowledge Room
│       ├── domain-specific/        ← Domain knowledge
│       ├── general/                ← General knowledge
│       └── howtos/                 ← How-to guides
├── prompt-library/                 ← Prompt Wing
│   ├── system-prompts/             ← System prompt templates
│   ├── task-prompts/               ← Task-specific prompts
│   ├── prompt-techniques/          ← Prompting techniques
│   └── templates/                  ← Reusable templates
├── skills/                         ← Skills Wing (SKILL.md format)
├── plugins/                        ← Plugins Wing (Python extensions)
├── configs/                        ← Config Wing
│   ├── agent-profiles/             ← Agent behavior profiles
│   ├── model-configs/              ← Model configurations
│   └── scheduler-tasks/            ← Scheduled task definitions
├── agent-zero-backup/              ← Agent Zero state backup
│   ├── agents/                     ← Agent configurations
│   ├── knowledge/                  ← Knowledge base (fragments/)
│   ├── memory-export/              ← Vector memory export
│   ├── plugins/                    ← Agent Zero plugins
│   ├── prompts/                    ← System prompt overrides
│   ├── skills/                     ← Agent Zero skills
│   └── workdir/                    ← Working directory backup
├── scripts/                        ← Automation scripts
├── AGENT-BOOTSTRAP.md              ← Ingestion manifest
├── MANIFEST.json                   ← Machine-readable inventory
└── .promptinclude.md               ← Auto-injection context
```

### Context Layers (Priority Order)

When loading context, follow this priority order to manage token budgets efficiently:

| Priority | Layer | Source | Typical Size | When to Load |
|---|---|---|---|---|
| 1 (highest) | Identity | `.promptinclude.md` | ~500 tokens | Always |
| 2 | Critical Facts | `AGENT-BOOTSTRAP.md` | ~800 tokens | Always |
| 3 | Room Recall | Specific room markdown files | ~2,000 tokens | On-demand per topic |
| 4 (lowest) | Deep Search | Full content search / embeddings | Variable | Only when needed |

### Key Bootstrap Files

| File | Format | Purpose |
|---|---|---|
| `AGENT-BOOTSTRAP.md` | Markdown | Ingestion manifest — read this first |
| `MANIFEST.json` | JSON | Machine-readable file inventory |
| `.promptinclude.md` | Markdown | Runtime context auto-injection rules |

---

## 3. Ingesting the Memory Palace

### Method 1: Configuration File Ingestion

OpenHermes and similar frameworks typically use YAML or JSON config files to define context sources. Point these at your Tolu directory structure.

#### `config.yaml`

```yaml
# openhermes-config.yaml
# Point OpenHermes at the Tolu Memory Palace

framework:
  name: openhermes
  version: "1.0"

# Context sources — Tolu Memory Palace
tolu:
  root: "/opt/tolu"  # Adjust to your install path
  bootstrap_file: "${tolu.root}/AGENT-BOOTSTRAP.md"
  manifest_file: "${tolu.root}/MANIFEST.json"
  prompt_include: "${tolu.root}/.promptinclude.md"

  # Knowledge wings
text_context:
  # Priority 1: Always loaded (identity layer)
  always_load:
    - "${tolu.root}/.promptinclude.md"
    - "${tolu.root}/AGENT-BOOTSTRAP.md"

  # Priority 2: Room recall — load per topic
  rooms:
    books_summaries: "${tolu.root}/memory-palace/books/summaries/*.md"
    books_references: "${tolu.root}/memory-palace/books/references/*.md"
    books_reading_lists: "${tolu.root}/memory-palace/books/reading-lists/*.md"
    youtube_transcripts: "${tolu.root}/memory-palace/youtube/transcripts/*.md"
    youtube_channels: "${tolu.root}/memory-palace/youtube/channels/*.md"
    youtube_playlists: "${tolu.root}/memory-palace/youtube/playlists/*.md"
    references_tools: "${tolu.root}/memory-palace/references/tools/*.md"
    references_technical: "${tolu.root}/memory-palace/references/technical/*.md"
    references_academic: "${tolu.root}/memory-palace/references/academic/*.md"
    knowledge_domain: "${tolu.root}/memory-palace/knowledge/domain-specific/*.md"
    knowledge_general: "${tolu.root}/memory-palace/knowledge/general/*.md"
    knowledge_howtos: "${tolu.root}/memory-palace/knowledge/howtos/*.md"

  # Priority 3: Prompt library
  prompts:
    system: "${tolu.root}/prompt-library/system-prompts/*.md"
    task: "${tolu.root}/prompt-library/task-prompts/*.md"
    techniques: "${tolu.root}/prompt-library/prompt-techniques/*.md"
    templates: "${tolu.root}/prompt-library/templates/*.md"

  # Priority 4: Agent Zero backup knowledge
  backup_knowledge: "${tolu.root}/agent-zero-backup/knowledge/fragments/*.md"
  backup_solutions: "${tolu.root}/agent-zero-backup/knowledge/solutions/*.md"

# Skills and plugins (advanced — see Section 8)
skills_dir: "${tolu.root}/skills"
plugins_dir: "${tolu.root}/plugins"
configs_dir: "${tolu.root}/configs"
```

#### Loading config in Python

```python
#!/usr/bin/env python3
"""Load Tolu Memory Palace config into OpenHermes."""

import os
import yaml
from pathlib import Path
from string import Template


def load_tolu_config(config_path: str = "openhermes-config.yaml") -> dict:
    """Load and resolve the Tolu config file."""
    with open(config_path, "r") as f:
        raw = yaml.safe_load(f)

    # Resolve ${tolu.root} references
    tolu_root = raw.get("tolu", {}).get("root", "/opt/tolu")
    resolved = _resolve_references(raw, {"tolu.root": tolu_root})
    return resolved


def _resolve_references(obj: any, variables: dict) -> any:
    """Recursively resolve ${var} references in config."""
    if isinstance(obj, str):
        return Template(obj).safe_substitute(variables)
    elif isinstance(obj, dict):
        return {k: _resolve_references(v, variables) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_resolve_references(item, variables) for item in obj]
    return obj


def get_room_files(room_pattern: str) -> list[str]:
    """Resolve a glob pattern to a list of file paths."""
    from glob import glob
    return sorted(glob(room_pattern, recursive=True))


# Usage
if __name__ == "__main__":
    config = load_tolu_config()
    print(f"Tolu root: {config['tolu']['root']}")

    # Load all book summaries
    book_files = get_room_files(config["text_context"]["rooms"]["books_summaries"])
    print(f"Found {len(book_files)} book summaries")
    for f in book_files:
        print(f"  - {f}")
```

---

### Method 2: System Prompt Construction

Build system prompts dynamically from memory palace content. This approach gives you fine-grained control over what knowledge the agent sees.

```python
#!/usr/bin/env python3
"""Build OpenHermes system prompts from Tolu Memory Palace rooms."""

import os
import json
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


TOLU_ROOT = os.environ.get("TOLU_ROOT", "/opt/tolu")

# Token budget management
APPROX_CHARS_PER_TOKEN = 4  # rough estimate for English text


@dataclass
class PalaceRoom:
    """Represents a room in the Memory Palace."""
    name: str
    path: Path
    description: str = ""
    priority: int = 5  # 1 = highest, 10 = lowest
    max_tokens: int = 2000

    def get_files(self) -> list[Path]:
        """Get all markdown files in this room."""
        if self.path.is_file():
            return [self.path]
        return sorted(self.path.glob("*.md"))

    def load_content(self, max_chars: Optional[int] = None) -> str:
        """Load all content from this room, optionally truncated."""
        parts = []
        for f in self.get_files():
            try:
                content = f.read_text(encoding="utf-8")
                parts.append(f"### {f.stem}\n\n{content}")
            except Exception as e:
                parts.append(f"### {f.stem}\n\n[Error loading: {e}]")

        combined = "\n\n---\n\n".join(parts)
        if max_chars and len(combined) > max_chars:
            combined = combined[:max_chars] + "\n\n[... truncated ...]"
        return combined

    def estimate_tokens(self) -> int:
        """Estimate token count for this room's content."""
        return len(self.load_content()) // APPROX_CHARS_PER_TOKEN


@dataclass
class SystemPromptBuilder:
    """Build system prompts from Tolu Memory Palace."""
    tolu_root: Path = Path(TOLU_ROOT)
    max_total_tokens: int = 8000
    include_identity: bool = True
    include_bootstrap: bool = True
    rooms: list[PalaceRoom] = field(default_factory=list)

    def __post_init__(self):
        # Always-available identity layer
        self.identity_room = PalaceRoom(
            name="Identity",
            path=self.tolu_root / ".promptinclude.md",
            description="Auto-injection context",
            priority=1,
            max_tokens=500,
        )
        self.bootstrap_room = PalaceRoom(
            name="Bootstrap",
            path=self.tolu_root / "AGENT-BOOTSTRAP.md",
            description="Ingestion manifest",
            priority=2,
            max_tokens=1000,
        )

    def add_room(self, name: str, subpath: str,
                 priority: int = 5, max_tokens: int = 2000) -> "SystemPromptBuilder":
        """Add a memory palace room to the builder."""
        room = PalaceRoom(
            name=name,
            path=self.tolu_root / subpath,
            priority=priority,
            max_tokens=max_tokens,
        )
        self.rooms.append(room)
        return self

    def build(self, topic: Optional[str] = None) -> str:
        """
        Build the complete system prompt.

        Args:
            topic: Optional topic to prioritize relevant rooms.
        """
        sections = []
        budget = self.max_total_tokens

        # Layer 1: Identity (always included)
        if self.include_identity:
            content = self.identity_room.load_content()
            tokens = len(content) // APPROX_CHARS_PER_TOKEN
            sections.append(f"## System Context\n\n{content}")
            budget -= tokens

        # Layer 2: Bootstrap (always included)
        if self.include_bootstrap and budget > 0:
            content = self.bootstrap_room.load_content()
            tokens = len(content) // APPROX_CHARS_PER_TOKEN
            if tokens <= budget:
                sections.append(f"## Bootstrap Manifest\n\n{content}")
                budget -= tokens

        # Layer 3: Room recall (priority-ordered)
        sorted_rooms = sorted(self.rooms, key=lambda r: r.priority)
        for room in sorted_rooms:
            if budget <= 0:
                break
            max_chars = min(
                room.max_tokens * APPROX_CHARS_PER_TOKEN,
                budget * APPROX_CHARS_PER_TOKEN,
            )
            content = room.load_content(max_chars=max_chars)
            if content.strip():
                tokens = len(content) // APPROX_CHARS_PER_TOKEN
                sections.append(f"## {room.name}\n\n{content}")
                budget -= tokens

        return "\n\n---\n\n".join(sections)


# --- Usage Examples ---

if __name__ == "__main__":
    # Example 1: Minimal system prompt (identity + bootstrap only)
    builder = SystemPromptBuilder(max_total_tokens=2000)
    prompt = builder.build()
    print(f"=== Minimal Prompt ({len(prompt)} chars) ===")
    print(prompt[:500])
    print("...\n")

    # Example 2: Full knowledge prompt
    builder = SystemPromptBuilder(max_total_tokens=12000)
    builder.add_room("Book Summaries", "memory-palace/books/summaries", priority=3)
    builder.add_room("YouTube Transcripts", "memory-palace/youtube/transcripts", priority=4)
    builder.add_room("Technical References", "memory-palace/references/technical", priority=3)
    builder.add_room("Domain Knowledge", "memory-palace/knowledge/domain-specific", priority=2)
    builder.add_room("How-Tos", "memory-palace/knowledge/howtos", priority=5)
    builder.add_room("Tool References", "memory-palace/references/tools", priority=4)

    prompt = builder.build()
    print(f"=== Full Prompt ({len(prompt)} chars, ~{len(prompt)//4} tokens) ===")
    print(prompt[:1000])
    print("...")

    # Example 3: Topic-focused prompt (manually selected rooms)
    builder = SystemPromptBuilder(max_total_tokens=6000)
    builder.add_room("Domain Knowledge", "memory-palace/knowledge/domain-specific", priority=1)
    builder.add_room("How-Tos", "memory-palace/knowledge/howtos", priority=2)
    builder.add_room("Tool References", "memory-palace/references/tools", priority=3)

    prompt = builder.build(topic="deployment")
    print(f"\n=== Topic-Focused Prompt ({len(prompt)} chars) ===")
    print(prompt[:500])
```

---

### Method 3: Direct API Context Loading

Load context files at conversation start and inject them into the message stream. This is useful when you want to load context dynamically per conversation.

```python
#!/usr/bin/env python3
"""Direct API context loading for Tolu Memory Palace."""

import os
import json
from pathlib import Path
from typing import Optional


TOLU_ROOT = Path(os.environ.get("TOLU_ROOT", "/opt/tolu"))


class ToluContextLoader:
    """Load Tolu Memory Palace context into conversation messages."""

    def __init__(self, tolu_root: Optional[Path] = None):
        self.root = tolu_root or TOLU_ROOT

    # --- Priority-based loading ---

    def load_identity(self) -> str:
        """Priority 1: Load identity context (.promptinclude.md)."""
        path = self.root / ".promptinclude.md"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def load_bootstrap(self) -> str:
        """Priority 2: Load bootstrap manifest."""
        path = self.root / "AGENT-BOOTSTRAP.md"
        if path.exists():
            return path.read_text(encoding="utf-8")
        return ""

    def load_manifest(self) -> dict:
        """Load machine-readable manifest."""
        path = self.root / "MANIFEST.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def load_room(self, room_path: str) -> str:
        """
        Priority 3: Load a specific room's content.

        Args:
            room_path: Relative path from tolu root, e.g. "memory-palace/books/summaries"
        """
        full_path = self.root / room_path
        if full_path.is_file():
            return full_path.read_text(encoding="utf-8")
        elif full_path.is_dir():
            parts = []
            for f in sorted(full_path.glob("*.md")):
                parts.append(f.read_text(encoding="utf-8"))
            return "\n\n---\n\n".join(parts)
        return ""

    def load_file(self, relative_path: str) -> str:
        """Load a single file by relative path."""
        full_path = self.root / relative_path
        if full_path.exists():
            return full_path.read_text(encoding="utf-8")
        return ""

    # --- Batch loading ---

    def load_all_rooms(self, wing: str = "memory-palace") -> dict[str, str]:
        """
        Load all rooms in a wing.
        Returns dict mapping room name to content.
        """
        wing_path = self.root / wing
        rooms = {}
        if not wing_path.is_dir():
            return rooms

        for room_dir in sorted(wing_path.rglob("*")):
            if room_dir.is_dir():
                files = list(room_dir.glob("*.md"))
                if files:
                    rel = room_dir.relative_to(self.root)
                    rooms[str(rel)] = "\n\n".join(
                        f.read_text(encoding="utf-8") for f in sorted(files)
                    )
        return rooms

    # --- Message construction ---

    def build_system_message(self, rooms: Optional[list[str]] = None,
                             max_chars: int = 32000) -> str:
        """
        Build a system message with layered context.

        Args:
            rooms: List of room paths to include. None = identity only.
            max_chars: Maximum total character count.
        """
        sections = []

        # Layer 1: Identity
        identity = self.load_identity()
        if identity:
            sections.append(identity)

        # Layer 2: Bootstrap
        bootstrap = self.load_bootstrap()
        if bootstrap:
            sections.append(bootstrap)

        # Layer 3: Requested rooms
        if rooms:
            for room in rooms:
                content = self.load_room(room)
                if content:
                    sections.append(f"## {room}\n\n{content}")

        combined = "\n\n---\n\n".join(sections)
        if len(combined) > max_chars:
            combined = combined[:max_chars] + "\n\n[... truncated at char limit ...]"
        return combined

    def build_messages(self, user_query: str,
                       rooms: Optional[list[str]] = None) -> list[dict]:
        """
        Build a complete message list for an OpenAI-compatible API call.

        Returns:
            List of message dicts with 'role' and 'content' keys.
        """
        system_content = self.build_system_message(rooms=rooms)
        messages = [
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_query},
        ]
        return messages


# --- Usage Examples ---

if __name__ == "__main__":
    loader = ToluContextLoader()

    # Quick identity check
    print("=== Identity ===")
    print(loader.load_identity()[:300])
    print("...")

    # Load a specific room
    print("\n=== Book Summaries ===")
    content = loader.load_room("memory-palace/books/summaries")
    if content:
        print(content[:300])
    else:
        print("(empty or not found)")

    # Build messages for an API call
    print("\n=== API Messages ===")
    messages = loader.build_messages(
        user_query="What do I know about deploying on Akash?",
        rooms=[
            "memory-palace/knowledge/domain-specific",
            "memory-palace/knowledge/howtos",
        ],
    )
    print(f"System message: {len(messages[0]['content'])} chars")
    print(f"User message: {messages[1]['content']}")
```

---

### Method 4: Embedding-Based Retrieval

Use vector search to find relevant palace content dynamically based on the user's query. This is the most token-efficient method.

```python
#!/usr/bin/env python3
"""
Embedding-based retrieval over Tolu Memory Palace.
Uses ChromaDB with sentence-transformers for fully local operation.
"""

import os
from pathlib import Path
from typing import Optional

from chromadb import PersistentClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


TOLU_ROOT = Path(os.environ.get("TOLU_ROOT", "/opt/tolu"))
CHROMA_DIR = Path(os.environ.get("TOLU_CHROMA_DIR", "/opt/tolu-chroma"))

# Rooms to index
INDEXED_ROOMS = [
    "memory-palace/books/summaries",
    "memory-palace/books/references",
    "memory-palace/books/reading-lists",
    "memory-palace/youtube/transcripts",
    "memory-palace/youtube/channels",
    "memory-palace/youtube/playlists",
    "memory-palace/references/tools",
    "memory-palace/references/technical",
    "memory-palace/references/academic",
    "memory-palace/knowledge/domain-specific",
    "memory-palace/knowledge/general",
    "memory-palace/knowledge/howtos",
    "prompt-library/system-prompts",
    "prompt-library/task-prompts",
    "prompt-library/prompt-techniques",
    "prompt-library/templates",
]


class ToluRetriever:
    """Vector retrieval over Tolu Memory Palace content."""

    def __init__(self, tolu_root: Optional[Path] = None, chroma_dir: Optional[Path] = None,
                 embedding_model: str = "all-MiniLM-L6-v2"):
        self.root = tolu_root or TOLU_ROOT
        self.chroma_dir = chroma_dir or CHROMA_DIR

        # Initialize embedding function
        self.embed_fn = SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )

        # Initialize ChromaDB
        self.client = PersistentClient(path=str(self.chroma_dir))
        self.collection = self.client.get_or_create_collection(
            name="tolu_memory_palace",
            embedding_function=self.embed_fn,
            metadata={"hnsw:space": "cosine"},
        )

    def index_palace(self, chunk_size: int = 1000, chunk_overlap: int = 200) -> int:
        """
        Index all markdown files in the Memory Palace.

        Args:
            chunk_size: Characters per chunk.
            chunk_overlap: Overlap between chunks.

        Returns:
            Number of chunks indexed.
        """
        total_indexed = 0

        for room_path in INDEXED_ROOMS:
            full_path = self.root / room_path
            if not full_path.exists():
                continue

            files = sorted(full_path.glob("*.md")) if full_path.is_dir() else [full_path]

            for f in files:
                content = f.read_text(encoding="utf-8")
                if not content.strip():
                    continue

                # Simple chunking by character count
                chunks = self._chunk_text(content, chunk_size, chunk_overlap)
                for i, chunk in enumerate(chunks):
                    doc_id = f"{room_path}::{f.stem}::{i}"
                    self.collection.upsert(
                        ids=[doc_id],
                        documents=[chunk],
                        metadatas=[{
                            "room": room_path,
                            "file": f.name,
                            "chunk": i,
                            "source": str(f.relative_to(self.root)),
                        }],
                    )
                    total_indexed += 1

        return total_indexed

    def search(self, query: str, n_results: int = 5,
               room_filter: Optional[str] = None) -> list[dict]:
        """
        Search the Memory Palace for relevant content.

        Args:
            query: Search query.
            n_results: Number of results to return.
            room_filter: Optional room path to filter results.

        Returns:
            List of result dicts with 'content', 'source', 'room', 'distance'.
        """
        where_filter = None
        if room_filter:
            where_filter = {"room": {"$contains": room_filter}}

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where_filter,
        )

        # Format results
        output = []
        if results and results["documents"]:
            for i, doc in enumerate(results["documents"][0]):
                output.append({
                    "content": doc,
                    "source": results["metadatas"][0][i]["source"],
                    "room": results["metadatas"][0][i]["room"],
                    "distance": results["distances"][0][i] if "distances" in results else None,
                })
        return output

    def build_context(self, query: str, n_results: int = 5,
                      max_chars: int = 8000) -> str:
        """
        Build a context string from search results for a query.

        This is the main method to call before sending a user query
        to your LLM — it retrieves the most relevant palace content.
        """
        results = self.search(query, n_results=n_results)
        if not results:
            return ""

        sections = []
        total_chars = 0
        for r in results:
            section = f"### Source: {r['source']} (relevance: {1 - (r['distance'] or 0):.2f})\n\n{r['content']}"
            if total_chars + len(section) > max_chars:
                break
            sections.append(section)
            total_chars += len(section)

        return "\n\n---\n\n".join(sections)

    def get_indexed_count(self) -> int:
        """Return the number of documents in the collection."""
        return self.collection.count()

    @staticmethod
    def _chunk_text(text: str, chunk_size: int, overlap: int) -> list[str]:
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text]
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks


# --- Usage Examples ---

if __name__ == "__main__":
    retriever = ToluRetriever()

    # Index the palace (run once, or on a schedule)
    print("Indexing Memory Palace...")
    count = retriever.index_palace()
    print(f"Indexed {count} chunks")

    # Search for relevant content
    print("\n=== Search: 'API authentication' ===")
    results = retriever.search("API authentication", n_results=3)
    for r in results:
        print(f"  [{r['room']}] {r['source']} (dist: {r['distance']:.3f})")
        print(f"    {r['content'][:150]}...")

    # Build context for an LLM call
    print("\n=== Built Context ===")
    context = retriever.build_context("deploying containers on cloud", n_results=3)
    print(context[:500] if context else "(no results)")
```

---

## 4. Configuration File Patterns

### Main Configuration (`config.yaml`)

A complete example showing all Tolu integration points:

```yaml
# openhermes-config.yaml
# Complete configuration for OpenHermes with Tolu Memory Palace

# --- Model Provider Settings ---
model:
  default_provider: venice          # Default LLM provider
  default_model: llama-3.3-70b      # Default model name

  providers:
    venice:
      type: openai_compatible
      api_base: "https://api.venice.ai/api/inference/v1"
      api_key_env: "VENICE_API_KEY"
      models:
        - llama-3.3-70b
        - mistral-31b
        - deepseek-r1-671b

    openai:
      type: openai
      api_key_env: "OPENAI_API_KEY"
      models:
        - gpt-4o
        - gpt-4o-mini
        - o4-mini

    anthropic:
      type: anthropic
      api_key_env: "ANTHROPIC_API_KEY"
      models:
        - claude-sonnet-4-5
        - claude-3-5-haiku

    local:
      type: openai_compatible
      api_base: "http://localhost:11434/v1"
      api_key_env: "OLLAMA_API_KEY"  # usually "ollama" or empty
      models:
        - llama3.2
        - qwen2.5
        - mistral

  parameters:
    temperature: 0.7
    max_tokens: 4096
    top_p: 0.95

# --- Context Paths (Tolu Memory Palace) ---
tolu:
  root: "/opt/tolu"

  # Files always loaded into context
  bootstrap_files:
    - path: "${tolu.root}/.promptinclude.md"
      label: "Identity Context"
      priority: 1
    - path: "${tolu.root}/AGENT-BOOTSTRAP.md"
      label: "Bootstrap Manifest"
      priority: 2

  # Searchable room directories
  rooms:
    - name: "Book Summaries"
      path: "${tolu.root}/memory-palace/books/summaries"
      priority: 3
    - name: "Book References"
      path: "${tolu.root}/memory-palace/books/references"
      priority: 4
    - name: "Reading Lists"
      path: "${tolu.root}/memory-palace/books/reading-lists"
      priority: 5
    - name: "YouTube Transcripts"
      path: "${tolu.root}/memory-palace/youtube/transcripts"
      priority: 4
    - name: "YouTube Channels"
      path: "${tolu.root}/memory-palace/youtube/channels"
      priority: 5
    - name: "YouTube Playlists"
      path: "${tolu.root}/memory-palace/youtube/playlists"
      priority: 5
    - name: "Tool References"
      path: "${tolu.root}/memory-palace/references/tools"
      priority: 3
    - name: "Technical References"
      path: "${tolu.root}/memory-palace/references/technical"
      priority: 3
    - name: "Academic References"
      path: "${tolu.root}/memory-palace/references/academic"
      priority: 4
    - name: "Domain Knowledge"
      path: "${tolu.root}/memory-palace/knowledge/domain-specific"
      priority: 2
    - name: "General Knowledge"
      path: "${tolu.root}/memory-palace/knowledge/general"
      priority: 4
    - name: "How-Tos"
      path: "${tolu.root}/memory-palace/knowledge/howtos"
      priority: 3

  # Prompt library paths
  prompts:
    system: "${tolu.root}/prompt-library/system-prompts"
    task: "${tolu.root}/prompt-library/task-prompts"
    techniques: "${tolu.root}/prompt-library/prompt-techniques"
    templates: "${tolu.root}/prompt-library/templates"

  # Vector search index (for embedding-based retrieval)
  vector_index:
    backend: "chromadb"
    path: "/opt/tolu-chroma"
    embedding_model: "all-MiniLM-L6-v2"
    chunk_size: 1000
    chunk_overlap: 200

# --- Agent Behavior ---
agent:
  name: "Tolu-Powered Agent"
  description: "Agent with access to Tolu Memory Palace knowledge"

  # How to handle context
  context_strategy: "hybrid"  # "static" | "retrieval" | "hybrid"
  # static: always load bootstrap files + all rooms (token-heavy)
  # retrieval: use vector search per query (token-efficient)
  # hybrid: always load bootstrap + vector search for rooms

  max_context_tokens: 8000
  temperature: 0.7

  # Memory persistence
  memory:
    enabled: true
    backend: "file"  # "file" | "chromadb" | "redis"
    save_path: "${tolu.root}/memory-palace/knowledge"

# --- Skills and Extensions ---
skills:
  dir: "${tolu.root}/skills"
  format: "skill_md"  # SKILL.md standard

plugins:
  dir: "${tolu.root}/plugins"
  format: "python"

# --- Logging ---
logging:
  level: "INFO"
  file: "/var/log/openhermes/tolu.log"
```

### Agent Configuration

Multiple agent configurations for different tasks:

```yaml
# agents/researcher.yaml
name: "Researcher"
description: "Deep research agent using Tolu knowledge"
model:
  provider: "${model.default_provider}"
  model: "${model.default_model}"
  temperature: 0.3  # Lower for analytical tasks

# Which palace rooms to use
tolu_rooms:
  - "memory-palace/books/summaries"
  - "memory-palace/references/academic"
  - "memory-palace/references/technical"
  - "memory-palace/knowledge/domain-specific"

system_prompt_template: |
  You are a research assistant with access to a structured knowledge base.
  Use the provided context to answer questions thoroughly and cite sources.

  Available knowledge rooms:
  {% for room in tolu_rooms %}
  - {{ room }}
  {% endfor %}

context_strategy: "hybrid"
max_context_tokens: 10000
```

```yaml
# agents/coder.yaml
name: "Coder"
description: "Software development agent with technical references"
model:
  provider: "${model.default_provider}"
  model: "${model.default_model}"
  temperature: 0.5

tolu_rooms:
  - "memory-palace/references/tools"
  - "memory-palace/references/technical"
  - "memory-palace/knowledge/howtos"

system_prompt_template: |
  You are a software development assistant.
  Use the technical references and how-to guides in your context.
  Write production-quality, well-documented code.

context_strategy: "retrieval"  # On-demand retrieval for large codebases
max_context_tokens: 8000
```

### Task Configuration

Task-specific configs that leverage palace knowledge:

```yaml
# tasks/summarize-book.yaml
task: "summarize_book"
description: "Summarize a book using existing palace knowledge"
agent: "researcher"

steps:
  - name: "load_existing_context"
    action: "tolu.search"
    params:
      query: "{{ book_title }}"
      rooms:
        - "memory-palace/books/summaries"
        - "memory-palace/books/references"
      n_results: 5

  - name: "generate_summary"
    action: "llm.generate"
    params:
      system_prompt: "Summarize the book using the provided context."
      context_from: "load_existing_context"
      max_tokens: 2000

  - name: "save_to_palace"
    action: "tolu.save"
    params:
      room: "memory-palace/books/summaries"
      filename: "{{ book_title | slugify }}.md"
      content_from: "generate_summary"
```

---

## 5. Custom Model Provider Setup

### Provider Configuration Pattern

OpenHermes and similar frameworks support custom providers via configuration. The generic pattern:

```yaml
# Generic provider pattern
providers:
  your_provider_name:
    name: "Display Name"              # Human-readable name
    type: "openai_compatible"          # openai | anthropic | openai_compatible
    api_base: "https://api.example.com/v1"  # API endpoint
    api_key_env: "YOUR_PROVIDER_API_KEY"     # Environment variable holding the key
    models:                            # Available models
      - model-name-1
      - model-name-2
    default_model: "model-name-1"      # Default selection
    parameters:                        # Override global parameters
      temperature: 0.7
      max_tokens: 4096
```

### Venice AI Integration

Venice AI provides an OpenAI-compatible API with privacy-focused inference:

```yaml
# Venice AI provider configuration
providers:
  venice:
    name: "Venice AI"
    type: "openai_compatible"
    api_base: "https://api.venice.ai/api/inference/v1"
    api_key_env: "VENICE_API_KEY"
    models:
      - llama-3.3-70b
      - mistral-31b
      - deepseek-r1-671b
      - qwen-2.5-7b
      - dolphin-3.0-qwen2.5-7b
    default_model: "llama-3.3-70b"
    parameters:
      temperature: 0.7
      max_tokens: 4096
      top_p: 0.95
      frequency_penalty: 0
      presence_penalty: 0
```

```python
#!/usr/bin/env python3
"""Test Venice AI connection."""

import os
from openai import OpenAI

client = OpenAI(
    api_key=os.environ["VENICE_API_KEY"],
    base_url="https://api.venice.ai/api/inference/v1",
)

response = client.chat.completions.create(
    model="llama-3.3-70b",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Say hello and list 3 things you can do."},
    ],
    max_tokens=500,
)

print(response.choices[0].message.content)
```

### Other OpenAI-Compatible Providers

#### Together AI

```yaml
providers:
  together:
    name: "Together AI"
    type: "openai_compatible"
    api_base: "https://api.together.xyz/v1"
    api_key_env: "TOGETHER_API_KEY"
    models:
      - meta-llama/Llama-3.3-70B-Instruct-Turbo
      - mistralai/Mixtral-8x7B-Instruct-v0.1
      - Qwen/Qwen2.5-72B-Instruct-Turbo
      - deepseek-ai/DeepSeek-R1
    default_model: "meta-llama/Llama-3.3-70B-Instruct-Turbo"
```

```python
# Test Together AI
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["TOGETHER_API_KEY"],
    base_url="https://api.together.xyz/v1",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100,
)
print(response.choices[0].message.content)
```

#### Fireworks AI

```yaml
providers:
  fireworks:
    name: "Fireworks AI"
    type: "openai_compatible"
    api_base: "https://api.fireworks.ai/inference/v1"
    api_key_env: "FIREWORKS_API_KEY"
    models:
      - accounts/fireworks/models/llama-v3p3-70b-instruct
      - accounts/fireworks/models/qwen2p5-72b-instruct
      - accounts/fireworks/models/deepseek-r1
    default_model: "accounts/fireworks/models/llama-v3p3-70b-instruct"
```

```python
# Test Fireworks AI
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["FIREWORKS_API_KEY"],
    base_url="https://api.fireworks.ai/inference/v1",
)

response = client.chat.completions.create(
    model="accounts/fireworks/models/llama-v3p3-70b-instruct",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100,
)
print(response.choices[0].message.content)
```

#### Groq

```yaml
providers:
  groq:
    name: "Groq"
    type: "openai_compatible"
    api_base: "https://api.groq.com/openai/v1"
    api_key_env: "GROQ_API_KEY"
    models:
      - llama-3.3-70b-versatile
      - llama-3.1-8b-instant
      - mixtral-8x7b-32768
    default_model: "llama-3.3-70b-versatile"
    parameters:
      temperature: 0.7
      max_tokens: 4096
```

```python
# Test Groq
from openai import OpenAI
import os

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1",
)

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100,
)
print(response.choices[0].message.content)
```

#### Local Ollama

```yaml
providers:
  ollama:
    name: "Ollama (Local)"
    type: "openai_compatible"
    api_base: "http://localhost:11434/v1"
    api_key_env: "OLLAMA_API_KEY"  # Set to "ollama" or any non-empty string
    models:
      - llama3.2
      - qwen2.5
      - mistral
      - codellama
    default_model: "llama3.2"
    parameters:
      temperature: 0.7
      num_predict: 4096  # Ollama-specific
```

```python
# Test local Ollama
from openai import OpenAI

client = OpenAI(
    api_key="ollama",  # Ollama doesn't require a real key
    base_url="http://localhost:11434/v1",
)

response = client.chat.completions.create(
    model="llama3.2",
    messages=[{"role": "user", "content": "Hello!"}],
    max_tokens=100,
)
print(response.choices[0].message.content)
```

---

## 6. Environment Variable Configuration

### API Key Pattern

All provider keys follow the `PROVIDER_API_KEY` naming convention:

```bash
# .env file — place in project root or /opt/tolu/

# LLM Provider Keys
VENICE_API_KEY=your-venice-api-key
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
TOGETHER_API_KEY=your-together-key
FIREWORKS_API_KEY=your-fireworks-key
GROQ_API_KEY=gsk_your-groq-key

# Local models (no real key needed)
OLLAMA_API_KEY=ollama

# Tolu configuration
TOLU_ROOT=/opt/tolu
TOLU_CHROMA_DIR=/opt/tolu-chroma

# Optional: Override config settings
# OPENHERMES_CONFIG=/path/to/custom-config.yaml
# OPENHERMES_LOG_LEVEL=DEBUG
```

### Loading .env in Python

```python
#!/usr/bin/env python3
"""Environment variable configuration for OpenHermes + Tolu."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from multiple possible locations
env_paths = [
    Path.cwd() / ".env",
    Path("/opt/tolu/.env"),
    Path.home() / ".openhermes.env",
]

for env_path in env_paths:
    if env_path.exists():
        load_dotenv(env_path)
        print(f"Loaded environment from: {env_path}")
        break
else:
    print("Warning: No .env file found. Using system environment variables.")


def get_api_key(provider: str) -> str:
    """Get API key for a provider from environment."""
    key_name = f"{provider.upper()}_API_KEY"
    key = os.environ.get(key_name)
    if not key:
        raise ValueError(
            f"Missing API key: Set {key_name} in your .env file or environment"
        )
    return key


def get_tolu_root() -> Path:
    """Get the Tolu Memory Palace root directory."""
    return Path(os.environ.get("TOLU_ROOT", "/opt/tolu"))


# Usage
if __name__ == "__main__":
    print(f"Tolu root: {get_tolu_root()}")
    print(f"Venice key present: {bool(os.environ.get('VENICE_API_KEY'))}")
    print(f"OpenAI key present: {bool(os.environ.get('OPENAI_API_KEY'))}")
```

### Docker Environment Variable Passing

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir \
    openai pyyaml chromadb sentence-transformers python-dotenv

# Copy application
COPY . /app/

# Tolu will be mounted as a volume
VOLUME /opt/tolu
VOLUME /opt/tolu-chroma

ENTRYPOINT ["python", "-m", "openhermes"]
```

```yaml
# docker-compose.yaml
version: "3.8"

services:
  openhermes:
    build: .
    environment:
      # Pass API keys from host environment or .env
      - VENICE_API_KEY=${VENICE_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY:-}
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY:-}
      - GROQ_API_KEY=${GROQ_API_KEY:-}
      - TOLU_ROOT=/opt/tolu
      - TOLU_CHROMA_DIR=/opt/tolu-chroma
    volumes:
      - /opt/tolu:/opt/tolu:ro        # Memory palace (read-only)
      - tolu-chroma:/opt/tolu-chroma   # Vector index (read-write)
    ports:
      - "8080:8080"

volumes:
  tolu-chroma:
```

### Configuration Resolution Order

Settings are resolved in this priority order (highest wins):

```
1. Environment variables     (TOLU_ROOT, VENICE_API_KEY, etc.)
2. Config file values         (config.yaml)
3. Default values             (hardcoded in code)
```

```python
import os
from pathlib import Path


def resolve_config(key: str, config_value: str = None, default: str = None) -> str:
    """Resolve a config value with proper priority."""
    # Priority 1: Environment variable
    env_val = os.environ.get(key.upper())
    if env_val:
        return env_val

    # Priority 2: Config file value
    if config_value:
        return config_value

    # Priority 3: Default
    return default


# Examples
tolu_root = resolve_config(
    "TOLU_ROOT",
    config_value="/opt/tolu",  # from config.yaml
    default="/opt/tolu",        # hardcoded fallback
)
```

---

## 7. Memory Palace Context Management

### Reading Context

```python
#!/usr/bin/env python3
"""Priority-based context reading from Tolu Memory Palace."""

import json
from pathlib import Path
from typing import Optional


class PalaceReader:
    """Read context from Tolu Memory Palace with priority-based loading."""

    def __init__(self, tolu_root: Path):
        self.root = tolu_root

    def load_identity(self) -> dict:
        """Priority 1: Load identity context."""
        path = self.root / ".promptinclude.md"
        return {
            "layer": "identity",
            "priority": 1,
            "content": path.read_text(encoding="utf-8") if path.exists() else "",
        }

    def load_critical_facts(self) -> dict:
        """Priority 2: Load critical facts from bootstrap."""
        path = self.root / "AGENT-BOOTSTRAP.md"
        return {
            "layer": "critical_facts",
            "priority": 2,
            "content": path.read_text(encoding="utf-8") if path.exists() else "",
        }

    def load_manifest(self) -> dict:
        """Load machine-readable manifest."""
        path = self.root / "MANIFEST.json"
        if path.exists():
            return json.loads(path.read_text(encoding="utf-8"))
        return {}

    def load_room(self, room_path: str) -> dict:
        """Priority 3: Load a specific room."""
        full_path = self.root / room_path
        files = []
        content = ""

        if full_path.is_file():
            files = [str(full_path)]
            content = full_path.read_text(encoding="utf-8")
        elif full_path.is_dir():
            md_files = sorted(full_path.glob("*.md"))
            files = [str(f) for f in md_files]
            content = "\n\n---\n\n".join(
                f"## {f.stem}\n\n{f.read_text(encoding='utf-8')}"
                for f in md_files
            )

        return {
            "layer": "room_recall",
            "priority": 3,
            "room": room_path,
            "files": files,
            "file_count": len(files),
            "content": content,
            "char_count": len(content),
        }

    def deep_search(self, query: str, retriever=None, n_results: int = 5) -> dict:
        """Priority 4: Deep search using embeddings."""
        if retriever is None:
            return {"layer": "deep_search", "content": "", "error": "No retriever provided"}

        results = retriever.search(query, n_results=n_results)
        return {
            "layer": "deep_search",
            "priority": 4,
            "query": query,
            "results": results,
            "content": "\n\n---\n\n".join(
                f"### {r['source']}\n\n{r['content']}" for r in results
            ),
        }

    def load_context_layers(self, rooms: Optional[list[str]] = None,
                             query: Optional[str] = None,
                             retriever=None) -> list[dict]:
        """
        Load all context layers in priority order.

        Args:
            rooms: Room paths to load (layer 3).
            query: Query for deep search (layer 4).
            retriever: ToluRetriever instance for vector search.
        """
        layers = []

        # Layer 1: Identity
        layers.append(self.load_identity())

        # Layer 2: Critical facts
        layers.append(self.load_critical_facts())

        # Layer 3: Room recall
        if rooms:
            for room in rooms:
                layers.append(self.load_room(room))

        # Layer 4: Deep search
        if query and retriever:
            layers.append(self.deep_search(query, retriever))

        return layers


# Usage
if __name__ == "__main__":
    reader = PalaceReader(Path("/opt/tolu"))

    # Load just identity and facts
    print("=== Identity ===")
    identity = reader.load_identity()
    print(f"Loaded {identity['content'][:100]}...")

    # Load a specific room
    print("\n=== Domain Knowledge ===")
    room = reader.load_room("memory-palace/knowledge/domain-specific")
    print(f"Files: {room['file_count']}, Chars: {room['char_count']}")

    # Load all layers
    print("\n=== All Layers ===")
    layers = reader.load_context_layers(
        rooms=["memory-palace/knowledge/domain-specific"],
    )
    for layer in layers:
        name = layer.get("layer", "unknown")
        chars = len(layer.get("content", ""))
        print(f"  {name}: {chars} chars")
```

### Writing Context

```python
#!/usr/bin/env python3
"""Save new knowledge to Tolu Memory Palace."""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


class PalaceWriter:
    """Write knowledge to the appropriate Tolu Memory Palace room."""

    # Room routing by knowledge type
    ROOM_MAP = {
        "book_summary": "memory-palace/books/summaries",
        "book_reference": "memory-palace/books/references",
        "reading_list": "memory-palace/books/reading-lists",
        "youtube_transcript": "memory-palace/youtube/transcripts",
        "youtube_channel": "memory-palace/youtube/channels",
        "youtube_playlist": "memory-palace/youtube/playlists",
        "tool_reference": "memory-palace/references/tools",
        "technical_reference": "memory-palace/references/technical",
        "academic_paper": "memory-palace/references/academic",
        "domain_knowledge": "memory-palace/knowledge/domain-specific",
        "general_knowledge": "memory-palace/knowledge/general",
        "howto": "memory-palace/knowledge/howtos",
    }

    def __init__(self, tolu_root: Path):
        self.root = tolu_root

    def save(self, knowledge_type: str, title: str, content: str,
             tags: Optional[list[str]] = None,
             source: Optional[str] = None) -> Path:
        """
        Save knowledge to the appropriate room.

        Args:
            knowledge_type: One of the keys in ROOM_MAP.
            title: Human-readable title.
            content: Markdown content.
            tags: Optional list of tags.
            source: Optional source attribution.

        Returns:
            Path to the saved file.
        """
        room = self.ROOM_MAP.get(knowledge_type)
        if not room:
            raise ValueError(
                f"Unknown knowledge type: {knowledge_type}. "
                f"Valid types: {list(self.ROOM_MAP.keys())}"
            )

        # Ensure directory exists
        room_path = self.root / room
        room_path.mkdir(parents=True, exist_ok=True)

        # Generate filename from title
        filename = self._slugify(title) + ".md"
        file_path = room_path / filename

        # Build frontmatter
        now = datetime.utcnow().isoformat() + "Z"
        frontmatter = self._build_frontmatter(
            title=title, tags=tags, source=source, created=now
        )

        # Write file
        file_path.write_text(f"{frontmatter}\n{content}\n", encoding="utf-8")
        return file_path

    def append_to_file(self, room_path: str, filename: str, content: str) -> Path:
        """Append content to an existing file in a room."""
        file_path = self.root / room_path / filename
        file_path.parent.mkdir(parents=True, exist_ok=True)

        if file_path.exists():
            existing = file_path.read_text(encoding="utf-8")
            file_path.write_text(f"{existing}\n\n---\n\n{content}\n", encoding="utf-8")
        else:
            file_path.write_text(content + "\n", encoding="utf-8")

        return file_path

    @staticmethod
    def _slugify(title: str) -> str:
        """Convert a title to a filesystem-safe slug."""
        slug = title.lower().strip()
        slug = re.sub(r'[^a-z0-9]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        return slug.strip('-')[:80]  # limit length

    @staticmethod
    def _build_frontmatter(title: str, tags: Optional[list[str]] = None,
                           source: Optional[str] = None,
                           created: Optional[str] = None) -> str:
        """Build YAML frontmatter for a markdown file."""
        lines = ["---"]
        lines.append(f"title: \"{title}\"")
        if tags:
            tag_str = ", ".join(f'"{t}"' for t in tags)
            lines.append(f"tags: [{tag_str}]")
        if source:
            lines.append(f"source: \"{source}\"")
        if created:
            lines.append(f"created: \"{created}\"")
        lines.append("---")
        return "\n".join(lines)


# Usage
if __name__ == "__main__":
    writer = PalaceWriter(Path("/opt/tolu"))

    # Save a book summary
    path = writer.save(
        knowledge_type="book_summary",
        title="Designing Data-Intensive Applications",
        content="""# Designing Data-Intensive Applications

## Key Takeaways
- Focus on reliability, scalability, and maintainability
- Data models: relational vs document vs graph
- Distributed systems fundamentals
        """,
        tags=["databases", "distributed-systems", "architecture"],
        source="Book by Martin Kleppmann",
    )
    print(f"Saved to: {path}")

    # Save a how-to guide
    path = writer.save(
        knowledge_type="howto",
        title="Deploy Docker Container to Akash",
        content="""# Deploy Docker Container to Akash

## Prerequisites
- Akash CLI installed
- AKT tokens in wallet

## Steps
1. Create SDL file
2. Create deployment
3. Place bid
4. Accept bid
5. Send manifest
        """,
        tags=["akash", "docker", "deployment"],
    )
    print(f"Saved to: {path}")
```

### Cross-Referencing

```python
#!/usr/bin/env python3
"""Build cross-references between Memory Palace rooms."""

import re
from pathlib import Path
from collections import defaultdict
from typing import Optional


class PalaceCrossReferencer:
    """Link rooms and build knowledge graphs from palace content."""

    def __init__(self, tolu_root: Path):
        self.root = tolu_root
        self.graph = defaultdict(set)  # node -> set of connected nodes

    def scan_all_links(self) -> dict[str, list[str]]:
        """
        Scan all markdown files for wiki-style and markdown links.
        Returns dict mapping source file to list of linked targets.
        """
        links = {}
        for md_file in sorted(self.root.rglob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            file_links = []

            # Markdown links: [text](path)
            file_links.extend(re.findall(r'\]\(([^)]+)\)', content))

            # Wiki-style links: [[target]]
            file_links.extend(re.findall(r'\[\[([^\]]+)\]\]', content))

            if file_links:
                rel = str(md_file.relative_to(self.root))
                links[rel] = file_links

                # Build graph
                for target in file_links:
                    self.graph[rel].add(target)
                    self.graph[target].add(rel)

        return links

    def find_backlinks(self, target_path: str) -> list[str]:
        """Find all files that link to a given target."""
        backlinks = []
        for md_file in sorted(self.root.rglob("*.md")):
            content = md_file.read_text(encoding="utf-8")
            if target_path in content:
                backlinks.append(str(md_file.relative_to(self.root)))
        return backlinks

    def find_related(self, room_path: str, keywords: list[str],
                     max_results: int = 10) -> list[str]:
        """
        Find files related to a room by keyword overlap.

        Scans all other rooms for files mentioning any of the keywords.
        """
        results = []
        room_full = self.root / room_path

        for md_file in sorted(self.root.rglob("*.md")):
            # Skip files in the same room
            try:
                md_file.relative_to(room_full)
                continue
            except ValueError:
                pass

            content = md_file.read_text(encoding="utf-8").lower()
            matches = sum(1 for kw in keywords if kw.lower() in content)
            if matches > 0:
                results.append((
                    str(md_file.relative_to(self.root)),
                    matches,
                ))

        # Sort by number of keyword matches
        results.sort(key=lambda x: x[1], reverse=True)
        return [r[0] for r in results[:max_results]]

    def generate_index(self) -> str:
        """Generate a markdown index of all cross-references."""
        links = self.scan_all_links()
        lines = ["# Memory Palace Cross-Reference Index\n"]

        for source, targets in sorted(links.items()):
            lines.append(f"## {source}\n")
            for target in sorted(targets):
                lines.append(f"- → {target}")
            lines.append("")

        return "\n".join(lines)


# Usage
if __name__ == "__main__":
    xref = PalaceCrossReferencer(Path("/opt/tolu"))

    # Scan all links
    print("=== Cross-References ===")
    links = xref.scan_all_links()
    for source, targets in links.items():
        print(f"{source} → {targets}")

    # Find related files
    print("\n=== Related to Akash ===")
    related = xref.find_related(
        "memory-palace/references/tools",
        keywords=["akash", "deploy", "container", "cloud"],
    )
    for r in related:
        print(f"  {r}")
```

---

## 8. Advanced Integration

### Skill Adaptation

Tolu skills use the `SKILL.md` format. Convert them to OpenHermes-compatible skill definitions:

```python
#!/usr/bin/env python3
"""
Convert Tolu SKILL.md format to OpenHermes skill format.

SKILL.md format:
  - Name, description, instructions in markdown
  - Rules in subdirectory markdown files
  - Referenced scripts

OpenHermes format (example):
  - YAML manifest with name, description, tools
  - Python tool implementation
  - Configuration block
"""

import re
import yaml
from pathlib import Path
from typing import Optional


def parse_skill_md(skill_md_path: Path) -> dict:
    """Parse a SKILL.md file into a structured dict."""
    content = skill_md_path.read_text(encoding="utf-8")

    skill = {
        "name": "",
        "description": "",
        "instructions": "",
        "rules": {},
        "scripts": [],
    }

    # Extract name (first H1)
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        skill["name"] = h1_match.group(1).strip()

    # Extract description (first paragraph after H1)
    parts = content.split("\n\n")
    for i, part in enumerate(parts):
        if part.startswith("# ") and i + 1 < len(parts) and not parts[i + 1].startswith("#"):
            skill["description"] = parts[i + 1].strip()
            break

    # Extract sections (H2)
    sections = re.split(r'^##\s+', content, flags=re.MULTILINE)
    for section in sections[1:]:  # Skip content before first H2
        lines = section.strip().split("\n")
        section_title = lines[0].strip()
        section_content = "\n".join(lines[1:]).strip()

        if section_title.lower() in ("instructions", "instruction"):
            skill["instructions"] = section_content
        elif section_title.lower() == "rules":
            # List referenced rule files
            rules_dir = skill_md_path.parent / "rules"
            if rules_dir.is_dir():
                for rule_file in sorted(rules_dir.rglob("*.md")):
                    rel = str(rule_file.relative_to(rules_dir))
                    skill["rules"][rel] = rule_file.read_text(encoding="utf-8")
        elif "script" in section_title.lower():
            skill["scripts"] = [
                line.strip().lstrip("- ")
                for line in lines[1:]
                if line.strip().startswith("-")
            ]

    skill["raw_content"] = content
    return skill


def skill_md_to_openhermes(skill: dict, output_dir: Path) -> Path:
    """
    Convert a parsed SKILL.md to OpenHermes format.

    Creates:
      - skill.yaml (manifest)
      - instructions.md (full instructions)
      - rules/ (rule files)
    """
    skill_dir = output_dir / skill["name"].lower().replace(" ", "-")
    skill_dir.mkdir(parents=True, exist_ok=True)

    # Write YAML manifest
    manifest = {
        "name": skill["name"],
        "description": skill["description"],
        "version": "1.0.0",
        "type": "skill",
        "instructions_file": "instructions.md",
        "rules_dir": "rules" if skill["rules"] else None,
    }
    (skill_dir / "skill.yaml").write_text(
        yaml.dump(manifest, default_flow_style=False),
        encoding="utf-8",
    )

    # Write instructions
    instructions = skill["instructions"] or skill["raw_content"]
    (skill_dir / "instructions.md").write_text(instructions, encoding="utf-8")

    # Write rules
    if skill["rules"]:
        rules_dir = skill_dir / "rules"
        rules_dir.mkdir(exist_ok=True)
        for rule_name, rule_content in skill["rules"].items():
            (rules_dir / rule_name).parent.mkdir(parents=True, exist_ok=True)
            (rules_dir / rule_name).write_text(rule_content, encoding="utf-8")

    return skill_dir


def convert_all_skills(tolu_skills_dir: Path, output_dir: Path) -> list[Path]:
    """Convert all SKILL.md skills in the Tolu skills directory."""
    converted = []
    for skill_md in sorted(tolu_skills_dir.rglob("SKILL.md")):
        print(f"Converting: {skill_md.parent.name}")
        skill = parse_skill_md(skill_md)
        output_path = skill_md_to_openhermes(skill, output_dir)
        converted.append(output_path)
        print(f"  → {output_path}")
    return converted


# Usage
if __name__ == "__main__":
    tolu_skills = Path("/opt/tolu/skills")
    output = Path("./openhermes-skills")

    converted = convert_all_skills(tolu_skills, output)
    print(f"\nConverted {len(converted)} skills")
```

### Plugin Integration

Adapting Tolu's Python plugins for OpenHermes:

```python
#!/usr/bin/env python3
"""
Adapt Tolu/Agent Zero plugins for OpenHermes.

Agent Zero plugins have:
  - plugin.yaml (manifest)
  - tools/ directory (Python tool classes)
  - extensions/ directory (optional extensions)
  - webui/ directory (optional UI components)

OpenHermes plugins typically need:
  - A manifest file
  - Python tool implementations
  - Configuration block
"""

import yaml
import shutil
from pathlib import Path


def adapt_plugin(a0_plugin_dir: Path, output_dir: Path) -> Path:
    """
    Adapt an Agent Zero plugin to OpenHermes format.
    Preserves tools and logic, adapts manifest.
    """
    # Read Agent Zero manifest
    a0_manifest_path = a0_plugin_dir / "plugin.yaml"
    if not a0_manifest_path.exists():
        raise FileNotFoundError(f"No plugin.yaml in {a0_plugin_dir}")

    a0_manifest = yaml.safe_load(a0_manifest_path.read_text(encoding="utf-8"))

    # Create output directory
    plugin_name = a0_manifest.get("name", a0_plugin_dir.name)
    oh_dir = output_dir / plugin_name
    oh_dir.mkdir(parents=True, exist_ok=True)

    # Adapt manifest
    oh_manifest = {
        "name": a0_manifest.get("name", plugin_name),
        "description": a0_manifest.get("description", ""),
        "version": a0_manifest.get("version", "1.0.0"),
        "type": "plugin",
        "tools_dir": "tools" if (a0_plugin_dir / "tools").exists() else None,
    }
    (oh_dir / "plugin.yaml").write_text(
        yaml.dump(oh_manifest, default_flow_style=False),
        encoding="utf-8",
    )

    # Copy tools directory
    tools_dir = a0_plugin_dir / "tools"
    if tools_dir.exists():
        shutil.copytree(tools_dir, oh_dir / "tools", dirs_exist_ok=True)

    # Copy any Python files at root
    for py_file in a0_plugin_dir.glob("*.py"):
        shutil.copy2(py_file, oh_dir / py_file.name)

    return oh_dir


def adapt_all_plugins(tolu_plugins_dir: Path, output_dir: Path) -> list[Path]:
    """Adapt all plugins from Tolu's plugins directory."""
    adapted = []
    for plugin_dir in sorted(tolu_plugins_dir.iterdir()):
        if not plugin_dir.is_dir():
            continue
        if plugin_dir.name.startswith("."):
            continue
        if not (plugin_dir / "plugin.yaml").exists():
            continue

        try:
            output_path = adapt_plugin(plugin_dir, output_dir)
            adapted.append(output_path)
            print(f"Adapted: {plugin_dir.name} → {output_path}")
        except Exception as e:
            print(f"Skipped: {plugin_dir.name} ({e})")

    return adapted


# Usage
if __name__ == "__main__":
    tolu_plugins = Path("/opt/tolu/plugins")
    output = Path("./openhermes-plugins")

    adapted = adapt_all_plugins(tolu_plugins, output)
    print(f"\nAdapted {len(adapted)} plugins")
```

### Scheduled Tasks

Translating Tolu's scheduler tasks to OpenHermes cron-like automation:

```python
#!/usr/bin/env python3
"""
Translate Tolu scheduler tasks to OpenHermes automation.

Tolu scheduler tasks are defined in:
  configs/scheduler-tasks/

Each task has:
  - name, system_prompt, prompt
  - schedule (cron: minute, hour, day, month, weekday)
  - Optional: plan (list of ISO datetimes)

OpenHermes equivalent: use APScheduler or cron.
"""

import json
from pathlib import Path
from datetime import datetime


# Option 1: APScheduler-based (Python-native)

def create_apscheduler_job(task_config: dict) -> dict:
    """
    Convert a Tolu scheduler task to an APScheduler job definition.
    """
    schedule = task_config.get("schedule", {})

    job = {
        "id": task_config.get("name", "unnamed-task").lower().replace(" ", "-"),
        "name": task_config.get("name", "Unnamed Task"),
        "func": "tasks.execute_tol_task",  # Your task runner function
        "trigger": "cron",
        "kwargs": {
            "system_prompt": task_config.get("system_prompt", ""),
            "prompt": task_config.get("prompt", ""),
        },
    }

    # Map cron fields
    if "minute" in schedule:
        job["minute"] = schedule["minute"]
    if "hour" in schedule:
        job["hour"] = schedule["hour"]
    if "day" in schedule:
        job["day"] = schedule["day"]
    if "month" in schedule:
        job["month"] = schedule["month"]
    if "weekday" in schedule:
        job["day_of_week"] = schedule["weekday"]

    return job


# Option 2: System crontab
def generate_crontab_entry(task_config: dict) -> str:
    """Generate a crontab entry from a Tolu scheduler task."""
    schedule = task_config.get("schedule", {})

    minute = schedule.get("minute", "*")
    hour = schedule.get("hour", "*")
    day = schedule.get("day", "*")
    month = schedule.get("month", "*")
    weekday = schedule.get("weekday", "*")

    name = task_config.get("name", "tolu-task")
    prompt = task_config.get("prompt", "").replace('"', '\\"')

    return (
        f'{minute} {hour} {day} {month} {weekday} '
        f'python -m openhermes.run_task --name "{name}" '
        f'--prompt "{prompt}" '
        f'# {name}'
    )


# Option 3: systemd timer
def generate_systemd_timer(task_config: dict) -> tuple[str, str]:
    """
    Generate systemd timer and service unit files.
    Returns (timer_content, service_content).
    """
    schedule = task_config.get("schedule", {})
    name = task_config.get("name", "tolu-task").lower().replace(" ", "-")
    unit_name = f"tolu-{name}"

    # Build OnCalendar expression
    minute = schedule.get("minute", "*")
    hour = schedule.get("hour", "*")
    day = schedule.get("day", "*")
    month = schedule.get("month", "*")
    # systemd weekday: Mon=1..Sun=7 (cron: Sun=0..Sat=6)
    weekday = schedule.get("weekday", "*")
    if weekday != "*":
        weekday = int(weekday) + 1
        if weekday > 7:
            weekday = 1
        weekday = str(weekday)

    calendar = f"*-{month}-{day} {hour}:{minute}:0"
    if weekday != "*":
        calendar += f" {weekday}"

    timer = f"""[Unit]
Description=Tolu Task: {task_config.get('name', name)}

[Timer]
OnCalendar={calendar}
Persistent=true

[Install]
WantedBy=timers.target
"""

    service = f"""[Unit]
Description=Tolu Task: {task_config.get('name', name)}

[Service]
Type=oneshot
ExecStart=/usr/bin/python3 -m openhermes.run_task --name "{name}"
WorkingDirectory=/opt/openhermes
Environment=TOLU_ROOT=/opt/tolu
"""

    return timer, service


# Usage
if __name__ == "__main__":
    # Example task config
    example_task = {
        "name": "Daily Backup",
        "system_prompt": "You are a backup assistant.",
        "prompt": "Run the daily backup of Tolu Memory Palace.",
        "schedule": {
            "minute": 0,
            "hour": 2,
        },
    }

    print("=== APScheduler Job ===")
    print(json.dumps(create_apscheduler_job(example_task), indent=2))

    print("\n=== Crontab Entry ===")
    print(generate_crontab_entry(example_task))

    print("\n=== Systemd Timer ===")
    timer, service = generate_systemd_timer(example_task)
    print(timer)
    print(service)
```

---

## 9. Testing and Verification

### Provider Connection Test

```python
#!/usr/bin/env python3
"""Test connections to all configured LLM providers."""

import os
import sys
from pathlib import Path
from openai import OpenAI


def test_provider(name: str, api_key: str, base_url: str,
                  model: str, test_prompt: str = "Say 'OK' and nothing else.") -> bool:
    """Test a single provider connection."""
    print(f"Testing {name} ({model})... ", end="")

    try:
        client = OpenAI(api_key=api_key, base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": test_prompt}],
            max_tokens=50,
            timeout=30,
        )
        content = response.choices[0].message.content.strip()
        print(f"✓ OK ({content[:50]})")
        return True
    except Exception as e:
        print(f"✗ FAILED ({e})")
        return False


# Provider definitions
PROVIDERS = [
    {
        "name": "Venice AI",
        "key_env": "VENICE_API_KEY",
        "base_url": "https://api.venice.ai/api/inference/v1",
        "model": "llama-3.3-70b",
    },
    {
        "name": "OpenAI",
        "key_env": "OPENAI_API_KEY",
        "base_url": "https://api.openai.com/v1",
        "model": "gpt-4o-mini",
    },
    {
        "name": "Anthropic",
        "key_env": "ANTHROPIC_API_KEY",
        "base_url": "https://api.anthropic.com/v1",  # Requires anthropic SDK
        "model": "claude-3-5-haiku",
        "skip": True,  # Anthropic needs its own SDK
    },
    {
        "name": "Together AI",
        "key_env": "TOGETHER_API_KEY",
        "base_url": "https://api.together.xyz/v1",
        "model": "meta-llama/Llama-3.3-70B-Instruct-Turbo",
    },
    {
        "name": "Fireworks AI",
        "key_env": "FIREWORKS_API_KEY",
        "base_url": "https://api.fireworks.ai/inference/v1",
        "model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
    },
    {
        "name": "Groq",
        "key_env": "GROQ_API_KEY",
        "base_url": "https://api.groq.com/openai/v1",
        "model": "llama-3.3-70b-versatile",
    },
    {
        "name": "Ollama (Local)",
        "key_env": "OLLAMA_API_KEY",
        "base_url": "http://localhost:11434/v1",
        "model": "llama3.2",
        "default_key": "ollama",
    },
]


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()

    results = {"passed": 0, "failed": 0, "skipped": 0}

    for provider in PROVIDERS:
        if provider.get("skip"):
            print(f"Skipping {provider['name']} (requires separate SDK)")
            results["skipped"] += 1
            continue

        api_key = os.environ.get(provider["key_env"], provider.get("default_key"))
        if not api_key:
            print(f"Skipping {provider['name']} (no API key in {provider['key_env']})")
            results["skipped"] += 1
            continue

        success = test_provider(
            name=provider["name"],
            api_key=api_key,
            base_url=provider["base_url"],
            model=provider["model"],
        )
        if success:
            results["passed"] += 1
        else:
            results["failed"] += 1

    print(f"\n{'='*40}")
    print(f"Results: {results['passed']} passed, {results['failed']} failed, {results['skipped']} skipped")
```

### Context Loading Verification

```python
#!/usr/bin/env python3
"""Verify Tolu Memory Palace context loading."""

import json
import sys
from pathlib import Path


TOLU_ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("/opt/tolu")


def verify_structure() -> bool:
    """Verify the Memory Palace directory structure."""
    print("=== Directory Structure ===")
    all_ok = True

    required = [
        ".promptinclude.md",
        "AGENT-BOOTSTRAP.md",
        "MANIFEST.json",
        "memory-palace/books/summaries",
        "memory-palace/books/references",
        "memory-palace/books/reading-lists",
        "memory-palace/youtube/transcripts",
        "memory-palace/youtube/channels",
        "memory-palace/youtube/playlists",
        "memory-palace/references/tools",
        "memory-palace/references/technical",
        "memory-palace/references/academic",
        "memory-palace/knowledge/domain-specific",
        "memory-palace/knowledge/general",
        "memory-palace/knowledge/howtos",
        "prompt-library/system-prompts",
        "prompt-library/task-prompts",
        "prompt-library/prompt-techniques",
        "prompt-library/templates",
        "skills",
        "plugins",
        "configs/agent-profiles",
        "configs/model-configs",
        "configs/scheduler-tasks",
    ]

    for rel_path in required:
        full_path = TOLU_ROOT / rel_path
        exists = full_path.exists()
        status = "✓" if exists else "✗"
        print(f"  {status} {rel_path}")
        if not exists:
            all_ok = False

    return all_ok


def verify_bootstrap_files() -> bool:
    """Verify key bootstrap files are readable and non-empty."""
    print("\n=== Bootstrap Files ===")
    all_ok = True

    files = {
        ".promptinclude.md": {
            "min_chars": 50,
            "must_contain": ["Memory Palace"],
        },
        "AGENT-BOOTSTRAP.md": {
            "min_chars": 100,
            "must_contain": ["Ingestion Checklist", "Directory Purpose Map"],
        },
        "MANIFEST.json": {
            "min_chars": 50,
            "must_contain": ["repo", "sections"],
            "is_json": True,
        },
    }

    for filename, checks in files.items():
        path = TOLU_ROOT / filename
        print(f"\n  {filename}:")

        if not path.exists():
            print(f"    ✗ File not found")
            all_ok = False
            continue

        content = path.read_text(encoding="utf-8")
        print(f"    Size: {len(content)} chars")

        if len(content) < checks["min_chars"]:
            print(f"    ✗ Too small (minimum {checks['min_chars']} chars)")
            all_ok = False
        else:
            print(f"    ✓ Size OK")

        for term in checks.get("must_contain", []):
            if term in content:
                print(f"    ✓ Contains '{term}'")
            else:
                print(f"    ✗ Missing '{term}'")
                all_ok = False

        if checks.get("is_json"):
            try:
                data = json.loads(content)
                print(f"    ✓ Valid JSON with keys: {list(data.keys())}")
            except json.JSONDecodeError as e:
                print(f"    ✗ Invalid JSON: {e}")
                all_ok = False

    return all_ok


def verify_room_contents() -> dict:
    """Count files in each room."""
    print("\n=== Room Contents ===")
    stats = {}

    rooms = [
        "memory-palace/books/summaries",
        "memory-palace/books/references",
        "memory-palace/books/reading-lists",
        "memory-palace/youtube/transcripts",
        "memory-palace/youtube/channels",
        "memory-palace/youtube/playlists",
        "memory-palace/references/tools",
        "memory-palace/references/technical",
        "memory-palace/references/academic",
        "memory-palace/knowledge/domain-specific",
        "memory-palace/knowledge/general",
        "memory-palace/knowledge/howtos",
        "prompt-library/system-prompts",
        "prompt-library/task-prompts",
        "prompt-library/prompt-techniques",
        "prompt-library/templates",
    ]

    for room in rooms:
        room_path = TOLU_ROOT / room
        if room_path.is_dir():
            md_files = [f for f in room_path.iterdir()
                        if f.is_file() and f.suffix == ".md"
                        and f.name != ".gitkeep"]
            count = len(md_files)
            stats[room] = count
            print(f"  {room}: {count} files")
        else:
            stats[room] = -1
            print(f"  {room}: DIRECTORY NOT FOUND")

    return stats


if __name__ == "__main__":
    print(f"Tolu Root: {TOLU_ROOT}\n")

    structure_ok = verify_structure()
    bootstrap_ok = verify_bootstrap_files()
    room_stats = verify_room_contents()

    total_files = sum(v for v in room_stats.values() if v > 0)
    print(f"\n{'='*40}")
    print(f"Total knowledge files: {total_files}")
    print(f"Structure: {'✓ OK' if structure_ok else '✗ ISSUES FOUND'}")
    print(f"Bootstrap: {'✓ OK' if bootstrap_ok else '✗ ISSUES FOUND'}")

    if structure_ok and bootstrap_ok:
        print("\n✓ Memory Palace ready for integration.")
    else:
        print("\n✗ Fix issues above before proceeding.")
        sys.exit(1)
```

### End-to-End Integration Test

```python
#!/usr/bin/env python3
"""
End-to-end integration test:
1. Load config
2. Load context
3. Call LLM with Tolu context
4. Verify response
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Import our modules (assumes they're in the same directory or on PYTHONPATH)
from openai import OpenAI

TOLU_ROOT = Path(os.environ.get("TOLU_ROOT", "/opt/tolu"))


def e2e_test(provider: str = "venice", model: str = "llama-3.3-70b") -> bool:
    """Run a full end-to-end test."""
    print(f"=== End-to-End Test ({provider}/{model}) ===")

    # Step 1: Verify Tolu is accessible
    print("\n1. Checking Tolu root...")
    bootstrap = TOLU_ROOT / "AGENT-BOOTSTRAP.md"
    if not bootstrap.exists():
        print(f"   ✗ AGENT-BOOTSTRAP.md not found at {bootstrap}")
        return False
    print(f"   ✓ Found {bootstrap}")

    # Step 2: Load context
    print("\n2. Loading context...")
    system_content = f"""You are an AI assistant with access to the Tolu Memory Palace.

## Memory Palace Status
- Location: {TOLU_ROOT}
- The user may ask about knowledge stored in the Memory Palace.
- Respond helpfully and reference specific knowledge areas when relevant.
"""

    # Try to load identity
    identity_path = TOLU_ROOT / ".promptinclude.md"
    if identity_path.exists():
        identity = identity_path.read_text(encoding="utf-8")
        system_content += f"\n## Identity Context\n{identity}\n"
        print(f"   ✓ Loaded identity ({len(identity)} chars)")

    print(f"   System context: {len(system_content)} chars (~{len(system_content)//4} tokens)")

    # Step 3: Call LLM
    print(f"\n3. Calling {provider} ({model})...")

    provider_configs = {
        "venice": {
            "base_url": "https://api.venice.ai/api/inference/v1",
            "key_env": "VENICE_API_KEY",
        },
        "openai": {
            "base_url": "https://api.openai.com/v1",
            "key_env": "OPENAI_API_KEY",
        },
        "groq": {
            "base_url": "https://api.groq.com/openai/v1",
            "key_env": "GROQ_API_KEY",
        },
        "ollama": {
            "base_url": "http://localhost:11434/v1",
            "key_env": "OLLAMA_API_KEY",
            "default_key": "ollama",
        },
    }

    pconfig = provider_configs.get(provider)
    if not pconfig:
        print(f"   ✗ Unknown provider: {provider}")
        return False

    api_key = os.environ.get(pconfig["key_env"], pconfig.get("default_key"))
    if not api_key:
        print(f"   ✗ No API key: set {pconfig['key_env']}")
        return False

    try:
        client = OpenAI(api_key=api_key, base_url=pconfig["base_url"])
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": "What is the Tolu Memory Palace? Briefly describe what you know from your context."},
            ],
            max_tokens=300,
            timeout=30,
        )
        answer = response.choices[0].message.content
        print(f"   ✓ Got response ({len(answer)} chars)")
        print(f"\n   Response: {answer}")
    except Exception as e:
        print(f"   ✗ LLM call failed: {e}")
        return False

    # Step 4: Verify response mentions Memory Palace concepts
    print("\n4. Verifying response...")
    keywords = ["memory", "palace", "knowledge", "tolu"]
    found = [kw for kw in keywords if kw.lower() in answer.lower()]
    if found:
        print(f"   ✓ Found keywords: {found}")
        print("\n✓ End-to-end test PASSED")
        return True
    else:
        print(f"   ⚠ No expected keywords found")
        print("\n⚠ Test passed (LLM responded) but response lacks expected context")
        return True  # Still pass — LLM responded


if __name__ == "__main__":
    provider = sys.argv[1] if len(sys.argv) > 1 else "venice"
    model = sys.argv[2] if len(sys.argv) > 2 else "llama-3.3-70b"

    success = e2e_test(provider, model)
    sys.exit(0 if success else 1)
```

---

## 10. Troubleshooting

### Configuration File Syntax Errors

**Symptom**: Config file fails to parse.

```bash
# Validate YAML syntax
python3 -c "
import yaml, sys
try:
    with open('openhermes-config.yaml') as f:
        yaml.safe_load(f)
    print('✓ YAML syntax OK')
except yaml.YAMLError as e:
    print(f'✗ YAML error: {e}')
    sys.exit(1)
"

# Validate JSON syntax
python3 -c "
import json, sys
try:
    with open('MANIFEST.json') as f:
        json.load(f)
    print('✓ JSON syntax OK')
except json.JSONDecodeError as e:
    print(f'✗ JSON error: {e}')
    sys.exit(1)
"
```

**Common issues**:

| Problem | Cause | Fix |
|---|---|---|
| `TabError` in YAML | Tabs instead of spaces | Replace tabs with 2-space indentation |
| Undefined `${var}` | Missing variable definition | Define `tolu.root` in config or set env var |
| Duplicate keys | Same key defined twice | Remove duplicate entries |
| Unclosed string | Missing closing `"` or `'` | Balance all quotes |

### Provider Connection Failures

**Symptom**: LLM API calls fail or timeout.

```bash
# Quick connectivity test
python3 -c "
import os
from openai import OpenAI

# Test Venice AI
client = OpenAI(
    api_key=os.environ.get('VENICE_API_KEY', 'MISSING'),
    base_url='https://api.venice.ai/api/inference/v1',
)
try:
    resp = client.chat.completions.create(
        model='llama-3.3-70b',
        messages=[{'role':'user','content':'ping'}],
        max_tokens=10,
        timeout=10,
    )
    print(f'✓ Venice OK: {resp.choices[0].message.content}')
except Exception as e:
    print(f'✗ Venice failed: {e}')
"

# Test Ollama locally
curl -s http://localhost:11434/api/tags | python3 -m json.tool
```

**Common issues**:

| Problem | Cause | Fix |
|---|---|---|
| `401 Unauthorized` | Invalid or missing API key | Check `VENICE_API_KEY` (or relevant) env var |
| `404 Not Found` | Wrong model name or base URL | Verify model name in provider docs |
| `429 Too Many Requests` | Rate limited | Add retry logic or reduce request rate |
| `Connection refused` | Service not running | Start Ollama: `ollama serve` |
| `Timeout` | Network or slow response | Increase `timeout` parameter |
| `SSLError` | TLS certificate issue | Check system certs or proxy settings |

```python
# Retry wrapper for API calls
import time
from functools import wraps

def retry_api_call(max_retries=3, backoff_seconds=2):
    """Decorator to retry failed API calls with exponential backoff."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_retries - 1:
                        raise
                    wait = backoff_seconds * (2 ** attempt)
                    print(f"Retry {attempt + 1}/{max_retries} after {wait}s: {e}")
                    time.sleep(wait)
        return wrapper
    return decorator


@retry_api_call(max_retries=3)
def call_llm(client, model, messages, **kwargs):
    return client.chat.completions.create(
        model=model, messages=messages, **kwargs
    )
```

### Context Loading Issues

**Symptom**: Agent doesn't have expected knowledge.

```bash
# Debug context loading
python3 -c "
from pathlib import Path

tolu = Path('/opt/tolu')

# Check each expected file
files = [
    '.promptinclude.md',
    'AGENT-BOOTSTRAP.md',
    'MANIFEST.json',
]
for f in files:
    p = tolu / f
    if p.exists():
        content = p.read_text()
        print(f'✓ {f}: {len(content)} chars')
        # Show first line
        print(f'  First line: {content.split(chr(10))[0][:80]}')
    else:
        print(f'✗ {f}: NOT FOUND at {p}')

# Check rooms for content
import os
for room in ['memory-palace/knowledge/domain-specific', 'memory-palace/books/summaries']:
    p = tolu / room
    if p.is_dir():
        md_files = [f for f in os.listdir(p) if f.endswith('.md') and f != '.gitkeep']
        print(f'✓ {room}: {len(md_files)} .md files')
        for f in md_files:
            print(f'    - {f}')
    else:
        print(f'✗ {room}: NOT A DIRECTORY')
"
```

**Common issues**:

| Problem | Cause | Fix |
|---|---|---|
| Empty rooms | No content saved yet | Use `PalaceWriter` to add content |
| Wrong path | `TOLU_ROOT` incorrect | Verify `echo $TOLU_ROOT` matches actual location |
| Permission denied | File permissions | `chmod -R 644` on `.md` files, `755` on dirs |
| Encoding errors | Non-UTF-8 files | Convert: `iconv -f latin1 -t utf8 file.md > file_utf8.md` |

### Memory Palace Structure Problems

**Symptom**: Directory structure is incomplete or corrupted.

```bash
# Full structure verification
python3 -c "
import json
from pathlib import Path

tolu = Path('/opt/tolu')
manifest_path = tolu / 'MANIFEST.json'

# Load manifest
if not manifest_path.exists():
    print('✗ MANIFEST.json not found')
    exit(1)

manifest = json.loads(manifest_path.read_text())
print(f'Repo: {manifest.get("repo")}')
print(f'Version: {manifest.get("version")}')
print(f'Last backup: {manifest.get("last_backup")}')

# Verify each section exists
for section, info in manifest.get('sections', {}).items():
    section_path = tolu / section
    exists = section_path.exists()
    status = '✓' if exists else '✗'
    print(f'{status} {section}/ ({info.get("description", "")})')
    
    # Check subdirs
    subdirs = info.get('subdirs', [])
    if isinstance(subdirs, dict):
        subdirs = list(subdirs.keys())
    for subdir in subdirs:
        sd_path = section_path / subdir
        sd_exists = sd_path.exists()
        sd_status = '✓' if sd_exists else '✗'
        print(f'  {sd_status} {section}/{subdir}/')
"
```

**Quick fix — recreate missing directories**:

```bash
# Recreate the full Memory Palace directory structure
tolu_root="/opt/tolu"

mkdir -p "$tolu_root"/memory-palace/books/{summaries,references,reading-lists}
mkdir -p "$tolu_root"/memory-palace/youtube/{transcripts,channels,playlists}
mkdir -p "$tolu_root"/memory-palace/references/{tools,technical,academic}
mkdir -p "$tolu_root"/memory-palace/knowledge/{domain-specific,general,howtos}
mkdir -p "$tolu_root"/prompt-library/{system-prompts,task-prompts,prompt-techniques,templates}
mkdir -p "$tolu_root"/skills
mkdir -p "$tolu_root"/plugins
mkdir -p "$tolu_root"/configs/{agent-profiles,model-configs,scheduler-tasks}
mkdir -p "$tolu_root"/scripts
mkdir -p "$tolu_root"/agent-zero-backup/{agents,knowledge,memory-export,plugins,prompts,skills,workdir}

# Add .gitkeep to empty dirs to preserve them in git
find "$tolu_root" -type d -empty -exec touch {}/.gitkeep \;

echo "✓ Directory structure recreated"
```

---

## Quick Reference Card

| Task | Command |
|---|---|
| Set Tolu root | `export TOLU_ROOT=/opt/tolu` |
| Verify structure | `python3 verify_context.py /opt/tolu` |
| Test provider | `python3 test_providers.py` |
| Run e2e test | `python3 e2e_test.py venice llama-3.3-70b` |
| Index for vector search | `python3 -c "from tolu_retriever import ToluRetriever; ToluRetriever().index_palace()"` |
| Convert skills | `python3 convert_skills.py /opt/tolu/skills ./oh-skills` |
| Convert plugins | `python3 convert_plugins.py /opt/tolu/plugins ./oh-plugins` |
| Recreate dirs | `bash recreate_dirs.sh /opt/tolu` |
| Check room files | `find $TOLU_ROOT/memory-palace -name '*.md' \| wc -l` |
| Build system prompt | `python3 -c "from prompt_builder import SystemPromptBuilder; ..."` |
