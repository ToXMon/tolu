# Pinterest MCP Production Ecosystem

**Source**: ByteByteGo newsletter (May 2025)
**Date saved**: 2026-05-11
**Original**: https://blog.bytebytego.com/p/how-pinterest-built-a-production

## Key Architecture Decisions

### Three Bets
1. **Cloud-hosted servers over local** — Centralized auth, logging, monitoring. Local allowed for experimentation only.
2. **Many small domain-specific servers** — Not one monolithic server. Presto server for data, Spark for batch debugging, Knowledge for docs. Keeps tool list small (context window constraint).
3. **Unified deployment pipeline** — Platform handles infra, teams focus on business logic. Without this, many-small-servers would collapse under operational weight.

### MCP Registry
- Central catalog: source of truth for servers, ownership, connectivity
- Web UI for humans (browse status, ownership, tools)
- API for AI clients (programmatic discovery, auth validation)
- Only registered servers = production-approved

## Two-Layer Auth

| Layer | Scope | Mechanism |
|-------|-------|-----------|
| Layer 1 | Coarse, network edge | Envoy proxy validates JWT, converts to X-Forwarded-User/Groups headers. Blocks unauthorized surface-to-server combinations |
| Layer 2 | Fine, per-tool | `@authorize_tool(policy='...')` decorator. Business-group gating for sensitive data |

- Skipped per-server OAuth (they own the whole stack, piggyback on existing auth session)
- Service-to-service: SPIFFE-based mTLS for automated calls

## Surfaces
- Internal AI chat (majority of employees daily)
- IM bots with context-aware tool scoping (Spark tools only in Airflow channels)
- IDE plugins (Presto data in coding workflows)
- CLI agents

## Top Servers by Traffic
1. **Presto** — universal data access, highest traffic
2. **Spark** — AI-assisted debugging, log diagnosis, root-cause analysis
3. **Knowledge** — institutional docs Q&A

## Governance
- Human-in-the-loop approval for sensitive/expensive actions
- Elicitation for dangerous operations (e.g., overwriting table data)
- Batch approval supported

## Measurements (Jan 2025)
- 66,000 invocations/month
- 844 monthly active users
- ~7,000 hours saved/month (owner-provided estimates x invocation counts)

## Lessons for Our Setup
- Registry pattern would help manage 18 MCP servers
- Unified deployment pipeline is the unlock for scaling
- Two-layer auth model is worth adopting if we expose agents to others
- Context-window-aware tool grouping (small servers > big server) applies directly

## References
- Building an MCP Ecosystem at Pinterest (Pinterest Engineering Blog)
- Model Context Protocol spec: https://modelcontextprotocol.io
