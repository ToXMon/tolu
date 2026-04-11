#!/usr/bin/env python3
"""
Tolu Memory Palace — Context Layer Builder

Reads all context layers and builds the wake-up context string for an agent.
Compacts multiple layers into a single text block suitable for injection into
a system prompt (~170 tokens for the minimal wake-up).

Usage:
    python3 build-context.py wakeup                    # Output minimal wake-up context
    python3 build-context.py room <wing> <room>        # Output full room context
    python3 build-context.py search "query"             # Deep search across all wings

Context Layers:
    Layer 0 — Identity:    context-layers/layer0-identity/identity.txt
    Layer 1 — Critical:    context-layers/layer1-critical-facts/critical-facts.json
    Layer 2 — Room Recall: context-layers/layer2-room-recall/recent-rooms.json
    Layer 3 — Deep Search: context-layers/layer3-deep-search/search-index.json
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOLU_ROOT = Path(__file__).resolve().parent.parent
CONTEXT_DIR = TOLU_ROOT / "context-layers"
MEMORY_PALACE_DIR = TOLU_ROOT / "memory-palace"
WINGS_DIR = MEMORY_PALACE_DIR / "wings"

LAYER0_PATH = CONTEXT_DIR / "layer0-identity" / "identity.txt"
LAYER1_PATH = CONTEXT_DIR / "layer1-critical-facts" / "critical-facts.json"
LAYER2_PATH = CONTEXT_DIR / "layer2-room-recall" / "recent-rooms.json"
LAYER3_PATH = CONTEXT_DIR / "layer3-deep-search" / "search-index.json"

# ---------------------------------------------------------------------------
# Layer Readers
# ---------------------------------------------------------------------------


def read_layer0() -> str:
    """Read Layer 0 — Identity."""
    if not LAYER0_PATH.exists():
        return "# Identity\nTolu Memory Palace Agent"
    try:
        return LAYER0_PATH.read_text(encoding="utf-8").strip()
    except Exception as e:
        return f"# Identity\n(Error reading identity: {e})"


def read_layer1() -> list[dict]:
    """Read Layer 1 — Critical Facts."""
    if not LAYER1_PATH.exists():
        return []
    try:
        with open(LAYER1_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Warning: Error reading critical facts: {e}", file=sys.stderr)
        return []


def read_layer2() -> list[dict]:
    """Read Layer 2 — Recent Room Recall."""
    if not LAYER2_PATH.exists():
        return []
    try:
        with open(LAYER2_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Warning: Error reading recent rooms: {e}", file=sys.stderr)
        return []


def load_search_index() -> dict | None:
    """Load Layer 3 — Search Index."""
    if not LAYER3_PATH.exists():
        return None
    try:
        with open(LAYER3_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"Warning: Error reading search index: {e}", file=sys.stderr)
        return None


# ---------------------------------------------------------------------------
# Wake-Up Context Builder
# ---------------------------------------------------------------------------

def build_wakeup() -> str:
    """Build the minimal wake-up context (~170 tokens).

    Combines:
    - Layer 0 identity (compact)
    - Layer 1 critical facts (top facts)
    - Layer 2 recent rooms (last 5)
    """
    lines = []

    # Layer 0: Identity
    identity = read_layer0()
    # Compact identity to essential lines only
    id_lines = [l for l in identity.split("\n") if l.strip() and not l.strip().startswith("# ")]
    if id_lines:
        lines.append("## Identity")
        lines.extend(id_lines[:5])  # max 5 identity lines
        lines.append("")

    # Layer 1: Critical Facts
    facts = read_layer1()
    if facts:
        lines.append("## Critical Facts")
        if isinstance(facts, list):
            for fact in facts[:10]:  # max 10 facts
                if isinstance(fact, dict):
                    text = fact.get("fact", fact.get("text", str(fact)))
                    lines.append(f"- {text}")
                else:
                    lines.append(f"- {fact}")
        elif isinstance(facts, dict):
            for key, val in list(facts.items())[:10]:
                lines.append(f"- **{key}**: {val}")
        lines.append("")

    # Layer 2: Recent Rooms
    recent = read_layer2()
    if recent:
        lines.append("## Recent Rooms")
        for room in recent[:5]:
            if isinstance(room, dict):
                wing = room.get("wing", "?")
                room_name = room.get("room", room.get("name", "?"))
                accessed = room.get("accessed", room.get("last_accessed", ""))
                lines.append(f"- {wing}/{room_name} ({accessed})" if accessed else f"- {wing}/{room_name}")
            else:
                lines.append(f"- {room}")
        lines.append("")

    # Footer
    lines.append("Use `python3 scripts/build-context.py search <query>` for deep search.")
    lines.append("Use `python3 scripts/build-context.py room <wing> <room>` for full room context.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Room Context Builder
# ---------------------------------------------------------------------------

def build_room_context(wing: str, room_name: str) -> str:
    """Build full room context by reading the room's files."""
    lines = [f"# Room Context: {wing}/{room_name}", ""]

    # Try multiple path patterns to find the room
    possible_paths = [
        WINGS_DIR / wing / "rooms" / room_name,
        WINGS_DIR / wing / "halls" / room_name,
        WINGS_DIR / wing / "rooms" / f"{room_name}.md",
        WINGS_DIR / wing / "halls" / f"{room_name}.md",
    ]

    room_path = None
    for p in possible_paths:
        if p.exists():
            room_path = p
            break

    if room_path is None:
        # Try a broader search
        wing_dir = WINGS_DIR / wing
        if wing_dir.exists():
            for root, dirs, files in os.walk(wing_dir):
                for fname in files:
                    stem = Path(fname).stem
                    if stem == room_name or fname == room_name:
                        room_path = Path(root) / fname
                        break
                if room_path:
                    break

    if room_path is None:
        return f"Error: Room '{wing}/{room_name}' not found. Searched in {WINGS_DIR}"

    lines.append(f"**Path**: `{room_path.relative_to(TOLU_ROOT)}`")
    lines.append("")

    if room_path.is_file():
        # Single file room
        try:
            content = room_path.read_text(encoding="utf-8")
            lines.append(content)
        except Exception as e:
            lines.append(f"Error reading room file: {e}")
    elif room_path.is_dir():
        # Directory room — read all files
        for root, dirs, files in os.walk(room_path):
            dirs.sort()
            for fname in sorted(files):
                fpath = Path(root) / fname
                if fname.endswith((".md", ".txt")):
                    rel = fpath.relative_to(room_path)
                    lines.append(f"### {rel}")
                    lines.append("")
                    try:
                        content = fpath.read_text(encoding="utf-8")
                        lines.append(content)
                    except Exception as e:
                        lines.append(f"*(Error reading: {e})*")
                    lines.append("")

    # Also find any tunnels connected to this room
    tunnels_dir = MEMORY_PALACE_DIR / "tunnels"
    if tunnels_dir.exists():
        connected_tunnels = []
        for tunnel_file in tunnels_dir.glob("*.json"):
            try:
                with open(tunnel_file, "r", encoding="utf-8") as f:
                    tunnel = json.load(f)
                for conn in tunnel.get("connections", []):
                    if conn.get("wing") == wing and (
                        conn.get("hall") == room_name or conn.get("file", "").startswith(room_name)
                    ):
                        connected_tunnels.append(tunnel["topic"])
                        break
            except (json.JSONDecodeError, KeyError):
                continue
        if connected_tunnels:
            lines.append("---")
            lines.append("")
            lines.append("**Connected Tunnels**: " + ", ".join(connected_tunnels))
            lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Deep Search
# ---------------------------------------------------------------------------

def search_context(query: str, top_k: int = 10) -> str:
    """Perform deep search across all wings using the search index."""
    index = load_search_index()
    if index is None:
        return "Error: Search index not found. Run `python3 scripts/search-index.py build` first."

    # Import query function from search-index
    # Inline the query logic to avoid import issues
    import re
    from collections import Counter
    import math

    STOP_WORDS = frozenset({
        "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
        "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
        "being", "have", "has", "had", "do", "does", "did", "will", "would",
        "could", "should", "may", "might", "shall", "can", "it", "its", "this",
        "that", "these", "those", "i", "you", "he", "she", "we", "they", "me",
        "him", "her", "us", "them", "my", "your", "his", "our", "their",
    })

    def tokenize(text):
        text = text.lower()
        text = re.sub(r"[^a-z0-9]+", " ", text)
        return [t for t in text.split() if t not in STOP_WORDS and len(t) > 1]

    query_tokens = tokenize(query)
    if not query_tokens:
        return "Error: No valid search terms provided."

    results = []
    for entry in index.get("files", []):
        tfidf = entry.get("_tfidf", {})
        score = 0.0
        for qt in query_tokens:
            if qt in tfidf:
                score += tfidf[qt] * 2.0
            for term, val in tfidf.items():
                if term.startswith(qt) and term != qt:
                    score += val * 0.5
                elif qt in term and term != qt:
                    score += val * 0.3

        title_lower = entry.get("title", "").lower()
        keywords = entry.get("keywords", [])
        for qt in query_tokens:
            if qt in title_lower:
                score += 3.0
            if qt in keywords:
                score += 1.0

        if score > 0:
            results.append({
                "file": entry["file"],
                "title": entry["title"],
                "score": round(score, 4),
                "summary": entry["summary"],
                "wing": entry.get("wing", ""),
                "room": entry.get("room", ""),
                "hall": entry.get("hall", ""),
            })

    results.sort(key=lambda x: x["score"], reverse=True)
    results = results[:top_k]

    if not results:
        return f"No results found for: {query}"

    lines = [f"# Search Results: \"{query}\"", ""]
    lines.append(f"Found {len(results)} results (showing top {min(top_k, len(results))}):")
    lines.append("")

    for i, r in enumerate(results, 1):
        lines.append(f"## {i}. {r['title']}")
        lines.append(f"**Score**: {r['score']} | **Wing**: {r['wing']} | **Path**: `{r['file']}`")
        lines.append(f"**Summary**: {r['summary']}")
        lines.append("")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Tolu Memory Palace — Context Layer Builder"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # wakeup command
    subparsers.add_parser("wakeup", help="Output minimal wake-up context (~170 tokens)")

    # room command
    room_parser = subparsers.add_parser("room", help="Output full room context")
    room_parser.add_argument("wing", type=str, help="Wing name")
    room_parser.add_argument("room_name", type=str, help="Room name")

    # search command
    search_parser = subparsers.add_parser("search", help="Deep search across all wings")
    search_parser.add_argument("query", type=str, help="Search query")
    search_parser.add_argument("--top", type=int, default=10, help="Number of results (default: 10)")

    args = parser.parse_args()

    if args.command == "wakeup":
        context = build_wakeup()
        print(context)

    elif args.command == "room":
        context = build_room_context(args.wing, args.room_name)
        print(context)

    elif args.command == "search":
        result = search_context(args.query, top_k=args.top)
        print(result)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
