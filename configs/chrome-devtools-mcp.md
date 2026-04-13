# Chrome DevTools MCP Configuration

## Setup Checklist (for Akash redeployment)

1. Install Chromium:
```bash
apt-get update && apt-get install -y chromium
```

2. MCP server config (add to `usr/settings.json` → `mcp_servers`):
```json
{
  "mcpServers": {
    "chrome-devtools": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "chrome-devtools-mcp@latest",
        "--headless",
        "--executablePath=/usr/bin/chromium",
        "--chromeArg=--no-sandbox",
        "--chromeArg=--disable-setuid-sandbox",
        "--chromeArg=--disable-dev-shm-usage",
        "--acceptInsecureCerts"
      ],
      "env": {
        "CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS": "1",
        "CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS": "1"
      }
    }
  }
}
```

3. Restart Agent Zero to load the MCP tools.

## Docker / Akash Persistence

To survive redeployment, set via environment variable:
```
A0_SET_mcp_servers='{"mcpServers":{"chrome-devtools":{"type":"stdio","command":"npx","args":["-y","chrome-devtools-mcp@latest","--headless","--executablePath=/usr/bin/chromium","--chromeArg=--no-sandbox","--chromeArg=--disable-setuid-sandbox","--chromeArg=--disable-dev-shm-usage","--acceptInsecureCerts"],"env":{"CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS":"1","CHROME_DEVTOOLS_MCP_NO_UPDATE_CHECKS":"1"}}}'
```

Also add to Akash SDL:
```yaml
env:
  - A0_SET_mcp_servers=<the JSON above>
```

And ensure Chromium is in the Docker image or install via init script.

## Tools Provided

| Category | Tools |
|----------|-------|
| Performance | start_trace, stop_trace, analyze_insight, memory_snapshot |
| Network | list_requests, get_request |
| Debugging | evaluate_script, list_console_messages, get_console_message |
| Browser | screenshot, snapshot, lighthouse_audit |
| Emulation | viewport, geolocation, etc. |

## Flags Explained

| Flag | Why |
|------|-----|
| `--headless` | No display in Docker container |
| `--executablePath=/usr/bin/chromium` | Points to system Chromium |
| `--chromeArg=--no-sandbox` | Required when running as root |
| `--chromeArg=--disable-setuid-sandbox` | Required when running as root |
| `--chromeArg=--disable-dev-shm-usage` | Prevents shared memory issues in containers |
| `--acceptInsecureCerts` | Allows self-signed certs in testing |

## Source
https://github.com/ChromeDevTools/chrome-devtools-mcp
