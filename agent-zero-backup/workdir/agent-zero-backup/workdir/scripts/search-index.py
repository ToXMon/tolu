#!/usr/bin/env python3
"""
Tolu Memory Palace — Semantic Search Index Builder & Query Tool

Builds a lightweight JSON-based search index over all markdown/text files
in the memory-palace/, prompt-library/, skills/, and context-layers/ directories.
Uses TF-IDF-like scoring with keyword matching — no external dependencies.

Usage:
    python3 search-index.py build                          # Rebuild full index
    python3 search-index.py query "search terms"           # Query the index
    python3 search-index.py query "search terms" --wing technical  # Filter by wing

Output: JSON with file, title, score, summary, wing, room, hall classification.
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

TOLU_ROOT = Path(__file__).resolve().parent.parent
INDEX_PATH = TOLU_ROOT / "context-layers" / "layer3-deep-search" / "search-index.json"

SCAN_DIRS = [
    TOLU_ROOT / "memory-palace",
    TOLU_ROOT / "prompt-library",
    TOLU_ROOT / "skills",
    TOLU_ROOT / "context-layers",
]

EXTENSIONS = {".md", ".txt", ".json"}

# Simple stop-word set (no NLTK needed)
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
    "there", "up", "down", "out", "off", "over", "under", "while",
    "as", "get", "got", "use", "used", "using", "make", "made",
    "like", "just", "know", "need", "want", "see", "go", "going",
})

# ---------------------------------------------------------------------------
# Text Processing Utilities
# ---------------------------------------------------------------------------


def tokenize(text: str) -> list[str]:
    """Lowercase, strip punctuation, split into tokens, remove stop words."""
    text = text.lower()
    # Replace common punctuation with spaces
    text = re.sub(r"[^a-z0-9]+", " ", text)
    tokens = text.split()
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 1]


def extract_title(content: str, filepath: Path) -> str:
    """Extract first H1 heading or fall back to filename stem."""
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return filepath.stem.replace("-", " ").replace("_", " ").title()


def extract_keywords(content: str) -> list[str]:
    """Extract keywords from headers, bold text, and high-frequency terms."""
    keywords = set()

    # Keywords from headers (## style)
    for match in re.finditer(r"^#+\s+(.+)$", content, re.MULTILINE):
        header_text = match.group(1).strip()
        # Strip leading # characters from the text itself
        header_text = re.sub(r"^#+\s*", "", header_text)
        for token in tokenize(header_text):
            keywords.add(token)

    # Keywords from bold text (**text** or __text__)
    for match in re.finditer(r"\*\*(.+?)\*\*", content):
        for token in tokenize(match.group(1)):
            keywords.add(token)
    for match in re.finditer(r"__(.+?)__", content):
        for token in tokenize(match.group(1)):
            keywords.add(token)

    # High-frequency terms from body
    all_tokens = tokenize(content)
    counter = Counter(all_tokens)
    total = len(all_tokens) if all_tokens else 1
    for term, count in counter.most_common(20):
        if count / total > 0.02:  # appears in > 2% of tokens
            keywords.add(term)

    return sorted(keywords)


def extract_summary(content: str, max_chars: int = 200) -> str:
    """Extract the first meaningful paragraph as summary."""
    lines = content.split("\n")
    for line in lines:
        stripped = line.strip()
        # Skip headers, empty lines, YAML frontmatter markers
        if not stripped or stripped.startswith("#") or stripped == "---":
            continue
        # Skip YAML frontmatter lines
        if ":" in stripped and stripped[0].islower():
            continue
        if len(stripped) > 20:
            return stripped[:max_chars] + ("..." if len(stripped) > max_chars else "")
    return "(no summary available)"


# ---------------------------------------------------------------------------
# Path Classification
# ---------------------------------------------------------------------------

def classify_path(filepath: Path) -> dict:
    """Determine wing, room, hall classification from the file's path."""
    rel = filepath.relative_to(TOLU_ROOT)
    parts = rel.parts

    result = {"wing": "", "hall": "", "room": ""}

    # memory-palace/wings/<wing>/halls/<hall>/... or rooms/<room>/...
    try:
        idx = parts.index("memory-palace")
        if idx + 1 < len(parts) and parts[idx + 1] == "wings":
            if idx + 2 < len(parts):
                result["wing"] = parts[idx + 2]
            # Look for halls or rooms
            for i in range(idx + 3, len(parts) - 1):
                if parts[i] == "halls" and i + 1 < len(parts):
                    result["hall"] = parts[i + 1] if not parts[i + 1].endswith(".md") else ""
                elif parts[i] == "rooms" and i + 1 < len(parts):
                    result["room"] = parts[i + 1] if not parts[i + 1].endswith(".md") else ""
        # Other memory-palace areas
        elif idx + 1 < len(parts) and parts[idx + 1] != "wings":
            result["wing"] = parts[idx + 1]  # e.g. books, youtube, references
    except (ValueError, IndexError):
        pass

    # prompt-library/<category>/...
    try:
        idx = parts.index("prompt-library")
        result["wing"] = result["wing"] or "prompts"
        if idx + 1 < len(parts):
            result["room"] = result["room"] or parts[idx + 1]
    except ValueError:
        pass

    # skills/<skill-name>/...
    try:
        idx = parts.index("skills")
        result["wing"] = result["wing"] or "skills"
        if idx + 1 < len(parts):
            result["room"] = result["room"] or parts[idx + 1]
    except ValueError:
        pass

    # context-layers/<layer>/...
    try:
        idx = parts.index("context-layers")
        result["wing"] = result["wing"] or "context"
        if idx + 1 < len(parts):
            result["room"] = result["room"] or parts[idx + 1]
    except ValueError:
        pass

    return result


# ---------------------------------------------------------------------------
# TF-IDF Index
# ---------------------------------------------------------------------------


def compute_tf(tokens: list[str]) -> dict[str, float]:
    """Compute term frequency for a list of tokens."""
    counter = Counter(tokens)
    total = len(tokens) if tokens else 1
    return {term: count / total for term, count in counter.items()}


def compute_idf(documents: list[list[str]]) -> dict[str, float]:
    """Compute inverse document frequency across all documents."""
    n = len(documents)
    if n == 0:
        return {}
    doc_freq: dict[str, int] = Counter()
    for tokens in documents:
        unique = set(tokens)
        for token in unique:
            doc_freq[token] += 1
    return {
        term: math.log((n + 1) / (df + 1)) + 1  # smoothed IDF
        for term, df in doc_freq.items()
    }


def build_index() -> dict:
    """Walk all directories and build the search index."""
    print("Scanning directories...")
    files_data = []
    all_token_lists = []

    for scan_dir in SCAN_DIRS:
        if not scan_dir.exists():
            print(f"  Skipping missing directory: {scan_dir}")
            continue
        for root, dirs, filenames in os.walk(scan_dir):
            root_path = Path(root)
            for fname in filenames:
                filepath = root_path / fname
                if filepath.suffix not in EXTENSIONS:
                    continue
                # Skip the index itself
                if filepath.name == "search-index.json":
                    continue
                try:
                    content = filepath.read_text(encoding="utf-8", errors="replace")
                except Exception as e:
                    print(f"  Error reading {filepath}: {e}")
                    continue

                # For JSON files, flatten the content for indexing
                if filepath.suffix == ".json":
                    try:
                        data = json.loads(content)
                        content = json.dumps(data, indent=2)
                    except json.JSONDecodeError:
                        pass

                title = extract_title(content, filepath)
                keywords = extract_keywords(content)
                summary = extract_summary(content)
                tokens = tokenize(content)
                classification = classify_path(filepath)

                stat = filepath.stat()
                last_modified = datetime.fromtimestamp(stat.st_mtime).isoformat()

                entry = {
                    "file": str(filepath.relative_to(TOLU_ROOT)),
                    "title": title,
                    "keywords": keywords,
                    "summary": summary,
                    "last_modified": last_modified,
                    "wing": classification["wing"],
                    "hall": classification["hall"],
                    "room": classification["room"],
                    "_tokens": tokens,  # temporary, for IDF computation
                }
                files_data.append(entry)
                all_token_lists.append(tokens)

    print(f"  Indexed {len(files_data)} files")

    # Compute IDF across all documents
    idf = compute_idf(all_token_lists)

    # Compute TF-IDF vectors and store scores
    index_entries = []
    for entry in files_data:
        tokens = entry.pop("_tokens")
        tf = compute_tf(tokens)
        # Store TF-IDF scores for query matching
        tfidf = {term: tf_val * idf.get(term, 1.0) for term, tf_val in tf.items()}
        # Keep only top 100 terms by score to keep index size manageable
        top_tfidf = dict(
            sorted(tfidf.items(), key=lambda x: x[1], reverse=True)[:100]
        )
        entry["_tfidf"] = top_tfidf
        index_entries.append(entry)

    index = {
        "version": "1.0",
        "built_at": datetime.now().isoformat(),
        "file_count": len(index_entries),
        "files": index_entries,
    }

    # Save index
    INDEX_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2, ensure_ascii=False)

    print(f"  Index saved to {INDEX_PATH}")
    return index


def load_index() -> dict | None:
    """Load the existing search index from disk."""
    if not INDEX_PATH.exists():
        print("Error: Index not found. Run 'build' first.")
        return None
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def query_index(index: dict, query: str, wing_filter: str | None = None, top_k: int = 10) -> list[dict]:
    """Query the index using TF-IDF scoring. Returns ranked results."""
    query_tokens = tokenize(query)
    if not query_tokens:
        return []

    results = []
    for entry in index["files"]:
        # Apply wing filter
        if wing_filter and entry.get("wing") != wing_filter:
            continue

        tfidf = entry.get("_tfidf", {})
        score = 0.0
        for qt in query_tokens:
            # Exact match
            if qt in tfidf:
                score += tfidf[qt] * 2.0  # boost exact matches
            # Partial match (starts with query token)
            for term, val in tfidf.items():
                if term.startswith(qt) and term != qt:
                    score += val * 0.5
                elif qt in term and term != qt:
                    score += val * 0.3

        # Also score against title and keywords (bonus)
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

    # Sort by score descending
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Tolu Memory Palace — Semantic Search Index Builder & Query Tool"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # build command
    subparsers.add_parser("build", help="Rebuild the full search index")

    # query command
    query_parser = subparsers.add_parser("query", help="Query the search index")
    query_parser.add_argument("terms", type=str, help="Search terms")
    query_parser.add_argument("--wing", type=str, default=None, help="Filter by wing name")
    query_parser.add_argument("--top", type=int, default=10, help="Number of results (default: 10)")

    args = parser.parse_args()

    if args.command == "build":
        index = build_index()
        print(f"\nBuild complete: {index['file_count']} files indexed.")

    elif args.command == "query":
        index = load_index()
        if index is None:
            sys.exit(1)
        results = query_index(index, args.terms, wing_filter=args.wing, top_k=args.top)
        if results:
            print(json.dumps(results, indent=2, ensure_ascii=False))
        else:
            print(f"No results found for: {args.terms}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
