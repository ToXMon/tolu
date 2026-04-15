#!/usr/bin/env python3
"""
Tolu Memory Palace — Auto Tunnel Generator

Scans all markdown files in memory-palace/wings/ and detects cross-references
between rooms in different wings by finding shared keywords, explicit links,
and shared tags. Generates tunnel files in memory-palace/tunnels/.

Usage:
    python3 cross-reference.py build    # Scan and generate tunnel files
    python3 cross-reference.py list     # List all discovered tunnels

Tunnel JSON format:
    {
      "topic": "authentication",
      "discovered": "2026-04-11",
      "connections": [
        {"wing": "technical", "hall": "howtos", "file": "auth-setup.md"},
        ...
      ]
    }
"""

import argparse
import json
import os
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOLU_ROOT = Path(__file__).resolve().parent.parent
WINGS_DIR = TOLU_ROOT / "memory-palace" / "wings"
TUNNELS_DIR = TOLU_ROOT / "memory-palace" / "tunnels"
INDEX_PATH = TUNNELS_DIR / "INDEX.md"

EXTENSIONS = {".md", ".txt"}

# Minimum number of connections to create a tunnel
MIN_CONNECTIONS = 2

# Stop words for keyword extraction
STOP_WORDS = frozenset({
    "a", "an", "the", "and", "or", "but", "in", "on", "at", "to", "for",
    "of", "with", "by", "from", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "it", "its", "this",
    "that", "these", "those", "i", "you", "he", "she", "we", "they", "me",
    "him", "her", "us", "them", "my", "your", "his", "our", "their", "what",
    "which", "who", "whom", "not", "no", "nor", "if", "then", "else",
    "when", "how", "all", "each", "every", "both", "few", "more", "most",
    "other", "some", "such", "only", "own", "same", "so", "than", "too",
    "very", "just", "about", "above", "after", "again", "also", "any",
    "because", "before", "between", "into", "through", "during", "here",
    "there", "up", "down", "out", "off", "over", "under", "while", "as",
    "get", "got", "use", "used", "using", "make", "made", "like", "know",
    "need", "want", "see", "go", "going", "example", "file", "also",
    "using", "used", "can", "will", "one", "two", "new", "first",
})

# ---------------------------------------------------------------------------
# Text Processing
# ---------------------------------------------------------------------------


def tokenize(text: str) -> set[str]:
    """Lowercase, strip punctuation, split into tokens, remove stop words."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    tokens = text.split()
    return {t for t in tokens if t not in STOP_WORDS and len(t) > 2}


def extract_frontmatter_tags(content: str) -> set[str]:
    """Extract tags from YAML frontmatter if present."""
    tags = set()
    if not content.startswith("---"):
        return tags
    # Find the closing ---
    end = content.find("---", 3)
    if end == -1:
        return tags
    frontmatter = content[3:end]
    # Look for tags: [tag1, tag2] or tags:\n  - tag1\n  - tag2
    tag_match = re.search(r"tags:\s*\[(.+?)\]", frontmatter)
    if tag_match:
        for tag in tag_match.group(1).split(","):
            tags.add(tag.strip().strip('"').strip("'").lower())
    else:
        tag_match = re.search(r"tags:\s*\n((?:\s+-\s+.+\n?)+)", frontmatter)
        if tag_match:
            for line in tag_match.group(1).strip().split("\n"):
                tag = line.strip().lstrip("- ").strip('"').strip("'")
                if tag:
                    tags.add(tag.lower())
    return tags


def extract_explicit_links(content: str) -> set[str]:
    """Extract explicit markdown links to other wings."""
    links = set()
    # Match [text](../other-wing/...) or [text](../../other-wing/...)
    for match in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", content):
        link_text = match.group(1).lower()
        link_target = match.group(2)
        # Check if it references another wing
        if "../" in link_target or "wings/" in link_target:
            links.add(link_text)
    return links


def extract_header_terms(content: str) -> set[str]:
    """Extract significant terms from headers."""
    terms = set()
    for match in re.finditer(r"^#+\s+(.+)$", content, re.MULTILINE):
        header = match.group(1).strip()
        # Remove markdown formatting
        header = re.sub(r"[*_`#]+", "", header)
        for token in tokenize(header):
            terms.add(token)
    return terms


def extract_bold_terms(content: str) -> set[str]:
    """Extract significant terms from bold text."""
    terms = set()
    for match in re.finditer(r"\*\*(.+?)\*\*", content):
        for token in tokenize(match.group(1)):
            terms.add(token)
    return terms


# ---------------------------------------------------------------------------
# File Metadata
# ---------------------------------------------------------------------------


def classify_file(filepath: Path) -> dict | None:
    """Determine wing, hall from file path relative to wings/ directory."""
    try:
        rel = filepath.relative_to(WINGS_DIR)
    except ValueError:
        return None

    parts = rel.parts
    if len(parts) < 1:
        return None

    wing = parts[0] if parts else ""
    hall = ""

    # Look for halls/ subdirectory
    try:
        halls_idx = parts.index("halls")
        if halls_idx + 1 < len(parts):
            hall = parts[halls_idx + 1]
    except ValueError:
        pass

    # Look for rooms/ subdirectory
    try:
        rooms_idx = parts.index("rooms")
        if rooms_idx + 1 < len(parts):
            hall = parts[rooms_idx + 1]  # use room as hall if no hall found
    except ValueError:
        pass

    return {
        "wing": wing,
        "hall": hall,
        "file": filepath.name,
    }


# ---------------------------------------------------------------------------
# Cross-Reference Detection
# ---------------------------------------------------------------------------


def scan_files() -> list[dict]:
    """Scan all markdown/text files in wings/ and extract metadata + terms."""
    files = []

    if not WINGS_DIR.exists():
        print(f"Error: Wings directory not found: {WINGS_DIR}")
        return files

    for root, dirs, filenames in os.walk(WINGS_DIR):
        root_path = Path(root)
        for fname in filenames:
            filepath = root_path / fname
            if filepath.suffix not in EXTENSIONS:
                continue

            classification = classify_file(filepath)
            if classification is None:
                continue

            try:
                content = filepath.read_text(encoding="utf-8", errors="replace")
            except Exception as e:
                print(f"  Error reading {filepath}: {e}")
                continue

            # Extract all term sources
            body_terms = tokenize(content)
            header_terms = extract_header_terms(content)
            bold_terms = extract_bold_terms(content)
            tags = extract_frontmatter_tags(content)
            links = extract_explicit_links(content)

            # Combine with weighting: headers and bold get priority
            all_terms = body_terms | header_terms | bold_terms | tags | links

            files.append({
                "classification": classification,
                "terms": all_terms,
                "tags": tags,
                "links": links,
            })

    print(f"  Scanned {len(files)} files in wings/")
    return files


def find_cross_references(files: list[dict]) -> dict[str, list[dict]]:
    """Find shared topics across different wings. Returns topic -> connections."""
    # Build term -> files mapping
    term_to_files: dict[str, list[dict]] = defaultdict(list)
    for f in files:
        for term in f["terms"]:
            term_to_files[term].append(f["classification"])

    # Build topic -> connections, only where connections span 2+ different wings
    topics: dict[str, list[dict]] = {}

    for term, connections in term_to_files.items():
        if len(connections) < MIN_CONNECTIONS:
            continue

        # Check if connections span multiple wings
        wings = {c["wing"] for c in connections}
        if len(wings) < 2:
            continue

        # Deduplicate connections by unique (wing, hall, file) tuples
        seen = set()
        unique_connections = []
        for c in connections:
            key = (c["wing"], c["hall"], c["file"])
            if key not in seen:
                seen.add(key)
                unique_connections.append(c)

        if len(unique_connections) >= MIN_CONNECTIONS:
            topics[term] = unique_connections

    return topics


def generate_tunnels(topics: dict[str, list[dict]]) -> list[str]:
    """Generate tunnel JSON files. Returns list of generated tunnel names."""
    TUNNELS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today().isoformat()
    tunnel_names = []

    for topic, connections in sorted(topics.items()):
        tunnel = {
            "topic": topic,
            "discovered": today,
            "connections": connections,
        }

        tunnel_file = TUNNELS_DIR / f"{topic}.json"
        with open(tunnel_file, "w", encoding="utf-8") as f:
            json.dump(tunnel, f, indent=2, ensure_ascii=False)

        tunnel_names.append(topic)

    return tunnel_names


def generate_index(topics: dict[str, list[dict]]) -> None:
    """Generate INDEX.md summarizing all tunnels."""
    lines = [
        "# 🚇 Tunnels — Cross-Wing Connections",
        "",
        f"> Auto-generated on {date.today().isoformat()}",
        f"> {len(topics)} cross-wing connections discovered",
        "",
        "Tunnels connect rooms across different wings by shared topics and keywords.",
        "They enable associative navigation through the Memory Palace.",
        "",
        "---",
        "",
    ]

    for topic, connections in sorted(topics.items()):
        wings = sorted({c["wing"] for c in connections})
        lines.append(f"## 🔗 {topic}")
        lines.append("")
        lines.append(f"**Wings**: {', '.join(wings)}")
        lines.append(f"**Connections**: {len(connections)}")
        lines.append("")
        for c in connections:
            wing = c["wing"]
            hall = c.get("hall", "")
            fname = c["file"]
            hall_str = f" / {hall}" if hall else ""
            lines.append(f"- [{wing}{hall_str} / {fname}](../wings/{wing}/{f'halls/{hall}/' if hall else ''}{fname})")
        lines.append("")

    lines.append("---")
    lines.append("")
    lines.append("*Run `python3 scripts/cross-reference.py build` to regenerate.*")
    lines.append("")

    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"  Generated {INDEX_PATH}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def cmd_build() -> None:
    """Build tunnels by scanning wings and detecting cross-references."""
    print("Scanning wings for cross-references...")
    files = scan_files()
    if not files:
        print("No files found. Nothing to do.")
        return

    print("Detecting cross-wing connections...")
    topics = find_cross_references(files)
    print(f"  Found {len(topics)} cross-wing topics")

    print("Generating tunnel files...")
    tunnel_names = generate_tunnels(topics)
    print(f"  Generated {len(tunnel_names)} tunnel files in {TUNNELS_DIR}")

    generate_index(topics)
    print(f"\nDone! {len(tunnel_names)} tunnels created.")


def cmd_list() -> None:
    """List all discovered tunnels."""
    if not TUNNELS_DIR.exists():
        print("No tunnels directory. Run 'build' first.")
        return

    tunnels = sorted(TUNNELS_DIR.glob("*.json"))
    if not tunnels:
        print("No tunnels found. Run 'build' first.")
        return

    print(f"Found {len(tunnels)} tunnels:\n")
    for tunnel_file in tunnels:
        try:
            with open(tunnel_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            wings = sorted({c["wing"] for c in data.get("connections", [])})
            print(f"  🔗 {data['topic']}")
            print(f"     Wings: {', '.join(wings)}")
            print(f"     Connections: {len(data.get('connections', []))}")
            print()
        except (json.JSONDecodeError, KeyError) as e:
            print(f"  ⚠️  Error reading {tunnel_file.name}: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Tolu Memory Palace — Auto Tunnel Generator"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    subparsers.add_parser("build", help="Scan wings and generate tunnel files")
    subparsers.add_parser("list", help="List all discovered tunnels")

    args = parser.parse_args()

    if args.command == "build":
        cmd_build()
    elif args.command == "list":
        cmd_list()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
