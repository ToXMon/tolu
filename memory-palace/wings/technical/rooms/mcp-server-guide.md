# MCP Server Setup & Usage Guide

**Created:** 2026-04-16
**Status:** Active
**Config location:** Agent Zero Settings → MCP/A2A → External MCP Servers

> **⚠️ CRITICAL:** Writing to `settings.json` does NOT initialize MCP servers. You MUST click **Apply now** in the UI (Settings → MCP/A2A → External MCP Servers) for servers to connect and tools to register. First `npx`/`uvx` run downloads packages (~30-60s per server).
---

## All 18 Configured Servers

### Crypto & Trading
| Server | Package | Purpose |
|--------|---------|---------|
| `crypto-price` | `mcp-crypto-price` (uvx) | Real-time prices, market analysis, historical trends via CoinCap API |
| `crypto-signals` | `crypto-signals-mcp` (uvx) | Volume anomaly detection, whale movements, pump signals (LOW/MODERATE/HIGH) |

### Documentation
| Server | Package | Purpose |
|--------|---------|---------|
| `context7` | `@upstash/context7-mcp` (npx) | Fetches live docs & code examples for any library/framework |

### Browser Automation
| Server | Package | Purpose |
|--------|---------|---------|
| `puppeteer` | `@modelcontextprotocol/server-puppeteer` (npx) | Headless Chrome navigation, screenshots, JS execution |
| `playwright` | `@playwright/mcp` (npx) | Cross-browser automation (Chromium, Firefox, WebKit) |
| `chrome-devtools` | `chrome-devtools-mcp` (npx) | Direct Chrome DevTools Protocol control |

### Full-Stack Dev
| Server | Package | Purpose |
|--------|---------|---------|
| `github` | `@modelcontextprotocol/server-github` (npx) | Repo management, PRs, issues, code search |
| `postgres` | `@modelcontextprotocol/server-postgres` (npx) | Direct PostgreSQL queries, schema inspection |
| `sqlite` | `mcp-server-sqlite` (uvx) | Local SQLite DB operations |
| `supabase` | `supabase-mcp-server` (npx) | Supabase project management: DB, auth, storage, edge functions |
| `vercel` | `vercel-mcp-server` (npx) | Deployments, env vars, project configuration |
| `filesystem` | `@modelcontextprotocol/server-filesystem` (npx) | Advanced file operations |
| `docker` | `@modelcontextprotocol/server-docker` (npx) | Container/image management |

### Search & Monitoring
| Server | Package | Purpose |
|--------|---------|---------|
| `brave-search` | `@modelcontextprotocol/server-brave-search` (npx) | Web search via Brave Search API |
| `sentry` | `@modelcontextprotocol/server-sentry` (npx) | Error tracking and crash report analysis |

### Communication & Design
| Server | Package | Purpose |
|--------|---------|---------|
| `slack` | `@modelcontextprotocol/server-slack` (npx) | Slack channel messaging and alerts |
| `figma` | `@modelcontextprotocol/server-figma` (npx) | Design tokens, specs, layouts |

### Memory
| Server | Package | Purpose |
|--------|---------|---------|
| `memory` | `@modelcontextprotocol/server-memory` (npx) | Persistent knowledge graph |

---

## Tokens/API Keys Needed

Replace `YOUR_*` placeholders in settings.json:

| Server | Env Variable | Where to Get |
|--------|-------------|--------------|
| github | `GITHUB_PERSONAL_ACCESS_TOKEN` | github.com/settings/tokens |
| supabase | `SUPABASE_ACCESS_TOKEN` + `SUPABASE_PROJECT_ID` | supabase.com/dashboard |
| vercel | `VERCEL_TOKEN` | vercel.com/account/tokens |
| brave-search | `BRAVE_API_KEY` | brave.com/search/api |
| sentry | `SENTRY_TOKEN` | sentry.io/settings/account/api |
| slack | `SLACK_BOT_TOKEN` + `SLACK_TEAM_ID` | api.slack.com/apps |
| figma | `FIGMA_ACCESS_TOKEN` | figma.com/settings |

**No keys needed:** context7, puppeteer, playwright, chrome-devtools, crypto-price, crypto-signals, sqlite, filesystem, docker, memory

---

## How to Use MCP Tools in Practice

### Tool Naming Convention
MCP tools are prefixed with the server name using underscores:
- Server `crypto-price` → tools like `crypto_price_get_price`
- Server `github` → tools like `github_create_issue`, `github_search_repositories`
- Server `puppeteer` → tools like `puppeteer_navigate`, `puppeteer_screenshot`

### Example Workflows

#### 1. Fetch Live Docs for Any Library
```
Ask: "What's the latest Next.js App Router API?"
Agent will use context7 to pull current Next.js docs into context.
```

#### 2. Build & Deploy a Full-Stack App
```
Ask: "Create a Next.js app with Supabase auth and deploy to Vercel"
Agent can:
- context7: Get latest Next.js/Supabase docs
- filesystem: Create project files
- supabase: Set up database, auth, storage
- github: Create repo, push code
- vercel: Deploy to production
```

#### 3. Crypto Monitoring
```
Ask: "What's BTC doing right now?"
Agent uses crypto-price for current data.

Scheduled task "Crypto Anomaly Alerts" (ID: MTwrdWh2):
- Runs every 30 minutes
- Scans for volume anomalies, whale movements, pump signals
- Alerts via notify_user for MODERATE/HIGH signals or >3% hourly moves
- Saves summaries to memory area='crypto-alerts'
```

#### 4. Headless Browser Automation
```
Ask: "Go to example.com, fill out the contact form, take a screenshot"
Agent uses puppeteer to navigate, interact, and capture.

For testing across browsers:
Ask: "Test this login flow in Chrome, Firefox, and WebKit"
Agent uses playwright for cross-browser coverage.
```

#### 5. Database Operations
```
Ask: "Create a users table in SQLite and add 5 test records"
Agent uses sqlite MCP tool.

Ask: "What's the schema of my Supabase project?"
Agent uses supabase MCP to inspect and modify.
```

#### 6. Debug Production Issues
```
Ask: "Check Sentry for recent errors in my app"
Agent uses sentry MCP to pull error reports.
Then: "Deploy a fix to Vercel"
Agent uses vercel MCP to redeploy.
```

---

## Scheduled Tasks

### Crypto Anomaly Alerts (2bD9kVCA)
- **Schedule:** Every 30 minutes
- **Dedicated context:** Yes
- **Method:** Uses direct CoinCap/CoinGecko API calls via `code_execution_tool` (curl/python)
- **Why not MCP tools:** Scheduled tasks with dedicated contexts may not inherit MCP tool registrations. Direct API calls are more reliable.
- **Actions:**
  1. Checks BTC, ETH, SOL prices via CoinCap API
  2. Scans top 20 assets for >5% 24h moves
  3. Sends `notify_user` alert (type=warning) for significant moves or >3% major token changes
  4. Saves summary to memory area='crypto-alerts'
- **To modify:** Use `scheduler:show_task` with UUID `2bD9kVCA`
- **To pause:** Use `scheduler:delete_task` with UUID `2bD9kVCA`

---

## Troubleshooting

- **Server not connecting:** First npx/uvx run downloads packages (30-60s). Check green status in Settings.
- **Tools not appearing:** Server must show connected with tool count > 0.
- **Auth errors:** Verify env variables have actual tokens, not `YOUR_*` placeholders.
- **Docker networking:** Use `host.docker.internal` on macOS/Windows, container names on Linux.
- **MCP browser tools > built-in browser agent** for reliability.

---

## Adding More Servers

1. Find servers at: [mcpservers.org](https://mcpservers.org), [mcp.so](https://mcp.so), [awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
2. Add entry to `mcpServers` in Settings → MCP/A2A → External MCP Servers
3. Click Apply now
4. Verify green status indicator
