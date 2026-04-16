#!/usr/bin/env python3
"""Chat Template Extractor — Scans conversation history, extracts reusable prompt templates.

Usage:
    python3 chat_template_extractor.py extract [conversation_dir] [output_dir]
    python3 chat_template_extractor.py list [output_dir]

Classifies messages by type, anonymizes specifics into {{placeholders}},
deduplicates, and outputs to templates/ directory.
"""

import json
import re
import sys
import hashlib
from pathlib import Path
from collections import defaultdict
from datetime import datetime


DEFAULT_CONV_DIR = Path("/a0/usr/chats")
DEFAULT_OUTPUT_DIR = Path("templates")

CATEGORY_KEYWORDS: dict[str, list[str]] = {
    "coding": ["implement", "function", "class", "module", "write code", "refactor",
               "variable", "import", "export", "def ", "async def", "component"],
    "research": ["find", "search", "analyze", "compare", "investigate", "what is",
                 "how does", "explain", "research"],
    "build": ["build", "compile", "bundle", "deploy", "docker", "pipeline",
              "ci/cd", "containerize", "package"],
    "deploy": ["deploy", "release", "publish", "ship", "push to", "merge",
               "tag", "version", "rollback"],
    "refactor": ["refactor", "restructure", "rename", "clean up", "simplify",
                 "extract", "abstract", "move to"],
    "debug": ["debug", "fix", "error", "bug", "traceback", "exception",
              "stack trace", "not working", "broken", "fails"],
    "test": ["test", "spec", "coverage", "assert", "mock", "fixture",
             "unit test", "integration test", "e2e"],
}


def classify_message(text: str) -> str:
    """Classify a message by type based on keyword matching."""
    text_lower = text.lower()
    scores: dict[str, int] = {}
    for category, keywords in CATEGORY_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in text_lower)
        if score > 0:
            scores[category] = score
    if not scores:
        return "general"
    return max(scores, key=scores.get)  # type: ignore[arg-type]


def anonymize(text: str) -> str:
    """Replace specifics with {{placeholders}}."""
    # File paths
    text = re.sub(r'/[a-zA-Z0-9_/.-]+(py|ts|js|tsx|jsx|md|json|yaml|yml)',
                  '{{file_path}}', text)
    # URLs
    text = re.sub(r'https?://[^<>"]+', '{{url}}', text)
    # IP addresses
    text = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '{{ip_address}}', text)
    # Email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
                  '{{email}}', text)
    # Variable names in backticks
    text = re.sub(r'`[a-zA-Z_][a-zA-Z0-9_]*`', '{{variable}}', text)
    # UUIDs
    text = re.sub(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}',
                  '{{uuid}}', text)
    # Numbers that look like ports or IDs
    text = re.sub(r'\bport\s+\d+\b', 'port {{port_number}}', text)
    text = re.sub(r'\b\d{4,}\b', '{{number}}', text)
    return text


def extract_templates(conversation_dir: Path, output_dir: Path) -> list[dict]:
    """Scan conversation files and extract reusable templates."""
    templates: list[dict] = []
    seen_hashes: set[str] = set()

    if not conversation_dir.exists():
        print(f"Conversation directory not found: {conversation_dir}")
        return templates

    for chat_dir in sorted(conversation_dir.iterdir()):
        if not chat_dir.is_dir():
            continue
        for msg_file in sorted(chat_dir.glob("*.txt")):
            try:
                content = msg_file.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue

            # Skip very short or system messages
            if len(content.strip()) < 50:
                continue

            # Extract user-facing messages (look for user_message patterns)
            parts = re.split(r'(?:user_message|assistant|system)', content)
            for part in parts:
                part = part.strip()
                if len(part) < 100 or len(part) > 5000:
                    continue

                category = classify_message(part)
                anonymized = anonymize(part)

                # Dedup by hash
                content_hash = hashlib.md5(anonymized.encode()).hexdigest()[:12]
                if content_hash in seen_hashes:
                    continue
                seen_hashes.add(content_hash)

                # Score reusability
                score = _score_reusability(anonymized, category)
                if score < 0.3:
                    continue

                templates.append({
                    "id": f"tmpl-{content_hash}",
                    "category": category,
                    "template": anonymized[:1000],
                    "reusability_score": round(score, 2),
                    "source_file": str(msg_file.relative_to(conversation_dir)),
                    "extracted_at": datetime.now().isoformat(),
                })

    return templates


def _score_reusability(text: str, category: str) -> float:
    """Score a template's reusability from 0.0 to 1.0."""
    score = 0.4  # base

    # Contains placeholders = more reusable
    placeholder_count = text.count("{{")
    score += min(placeholder_count * 0.1, 0.3)

    # Contains structured instructions
    if any(marker in text.lower() for marker in ["1.", "step", "first", "then"]):
        score += 0.1

    # Category bonus (coding/debug/test more reusable than general)
    if category in ("coding", "debug", "test", "build"):
        score += 0.1

    # Penalize very short or very long
    if len(text) < 150:
        score -= 0.1
    elif len(text) > 3000:
        score -= 0.1

    return max(0.0, min(1.0, score))


def output_results(templates: list[dict], output_dir: Path) -> None:
    """Write templates to JSON and Markdown files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    # Sort by reusability score descending
    templates.sort(key=lambda t: t["reusability_score"], reverse=True)

    # Write JSON
    json_path = output_dir / "extracted_templates.json"
    with open(json_path, "w") as f:
        json.dump({
            "extracted_at": datetime.now().isoformat(),
            "total_templates": len(templates),
            "by_category": dict(
                defaultdict(int, {t["category"]: sum(1 for x in templates if x["category"] == t["category"]) for t in templates})
            ),
            "templates": templates,
        }, f, indent=2)
    print(f"Wrote {len(templates)} templates to {json_path}")

    # Write Markdown
    md_path = output_dir / "PROMPT_TEMPLATES.md"
    with open(md_path, "w") as f:
        f.write("# Extracted Prompt Templates\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write(f"Total templates: {len(templates)}\n\n")

        by_cat: dict[str, list[dict]] = defaultdict(list)
        for t in templates:
            by_cat[t["category"]].append(t)

        for category in sorted(by_cat.keys()):
            items = by_cat[category]
            f.write(f"## {category.title()} ({len(items)})\n\n")
            for t in items:
                f.write(f"### {t['id']} (score: {t['reusability_score']})\n\n")
                f.write(f"```\n{t['template'][:500]}\n```\n\n")
    print(f"Wrote markdown to {md_path}")


def list_templates(output_dir: Path) -> None:
    """Display extracted templates."""
    json_path = output_dir / "extracted_templates.json"
    if not json_path.exists():
        print(f"No templates found at {json_path}. Run extract first.")
        return

    with open(json_path) as f:
        data = json.load(f)

    print(f"\n=== Extracted Templates ({data['total_templates']}) ===")
    for cat, count in data.get("by_category", {}).items():
        print(f"  {cat}: {count}")
    print(f"\nTop 5 by reusability:")
    for t in data["templates"][:5]:
        print(f"  [{t['reusability_score']:.2f}] {t['id']} ({t['category']}): {t['template'][:80]}...")


def main() -> None:
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "extract":
        conv_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_CONV_DIR
        out_dir = Path(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_OUTPUT_DIR
        templates = extract_templates(conv_dir, out_dir)
        if templates:
            output_results(templates, out_dir)
        else:
            print("No templates extracted.")
    elif command == "list":
        out_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else DEFAULT_OUTPUT_DIR
        list_templates(out_dir)
    else:
        print(f"Unknown command: {command}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
