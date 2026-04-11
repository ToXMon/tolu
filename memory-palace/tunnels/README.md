# 🔗 Tunnels — Cross-Wing References

Tunnels auto-connect rooms across different wings that share topics.
They are the bridges between buildings in the memory palace.

## How Tunnels Work

1. The `cross-reference.py` script scans all rooms for shared keywords
2. When 2+ rooms in different wings share a topic, a tunnel is created
3. Each tunnel is a JSON file mapping the shared topic to connected rooms
4. The `build-context.py room` command follows tunnels to provide cross-wing context

## Generating Tunnels

```bash
python3 scripts/cross-reference.py build
python3 scripts/cross-reference.py list
```

## Temporal Facts

`tunnels/temporal-facts.json` tracks facts with validity windows (start/end dates).
When a fact changes, it gets an end date rather than deletion.
