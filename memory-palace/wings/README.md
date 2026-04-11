# 🏛️ Wings — Spatial Memory Organization

Wings are top-level domains in the Memory Palace, inspired by the Method of Loci.
Each Wing contains Halls (category types) and Rooms (specific topics).

## Active Wings

| Wing | Purpose | Halls |
|------|---------|-------|
| **personal** | User identity, preferences, decisions | facts, events, decisions, preferences |
| **projects** | Active projects and architectures | facts, decisions, architecture |
| **people** | Contacts and interactions | facts, interactions, preferences |
| **learning** | Books, videos, courses | books, videos, courses |
| **technical** | Tools, references, howtos | tools, references, howtos |
| **domain** | Specialized domains | crypto, ai, web3, security |

## How It Works

- **Wing** = broad domain (like a building in a memory palace)
- **Hall** = category type within a wing (like a corridor)
- **Room** = specific topic or document (like a room)
- **Tunnel** = auto-generated cross-reference between rooms with shared topics across wings

## Creating a New Room

1. Create a markdown file in the appropriate `rooms/` directory
2. Name it descriptively: `topic-name.md`
3. Include YAML frontmatter for tags:
```yaml
---
title: "Topic Name"
tags: ["tag1", "tag2"]
created: "2026-04-11"
wing: "technical"
---
```
4. Run `python3 scripts/cross-reference.py build` to discover new tunnels
