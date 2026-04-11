# 🧅 Context Layers — Token-Efficient Agent Wake-up

The context layer system minimizes token usage on agent startup while providing
deep search capability on demand. Inspired by MemPalace's 4-layer memory stack.

## Layers (ordered by wake-up priority)

| Layer | Path | Tokens | Purpose |
|-------|------|--------|---------|
| **0 — Identity** | `layer0-identity/identity.txt` | ~100 | Who am I, purpose, setup, preferences |
| **1 — Critical Facts** | `layer1-critical-facts/critical-facts.json` | ~50 | High-confidence facts with validity windows |
| **2 — Room Recall** | `layer2-room-recall/recent-rooms.json` | ~50 | Recently accessed rooms for continuity |
| **3 — Deep Search** | `layer3-deep-search/search-index.json` | On-demand | Full TF-IDF search index of all content |

## Total Wake-up Cost: ~200 tokens

Compared to loading full context files (~2000+ tokens), this saves ~90% token cost.

## Usage

```bash
# Get minimal wake-up context
python3 scripts/build-context.py wakeup

# Get full room content
python3 scripts/build-context.py room technical agent-zero-setup

# Deep search
python3 scripts/build-context.py search "authentication"
```

## Adding Facts

Edit `layer1-critical-facts/critical-facts.json` to add new facts:
```json
{
  "id": "f009",
  "fact": "Description of the fact",
  "category": "system|environment|config|preference|skill",
  "confidence": 1.0,
  "valid_from": "2026-04-11",
  "valid_to": null,
  "source": "user|setup|environment"
}
```

When a fact changes, set `valid_to` to the current date and add a new fact.
This preserves history (temporal tracking).
