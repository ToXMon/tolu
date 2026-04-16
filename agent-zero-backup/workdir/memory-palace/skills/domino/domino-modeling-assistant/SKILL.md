---
name: domino-modeling-assistant
description: Enable AI-assisted model development within Domino by writing needed
  model and training code and using MCP (Model Context Protocol) servers to execute
  domino jobs. AI coding assistants like Cursor and GitHub Copilot can execute commands
  as Domino jobs, maintaining security, governance, and reproducibility. Use when
  setting up AI code assistants to work with Domino, configuring MCP servers, or enabling
  vibe modeling workflows.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- modeling
- assistant
- ai
trigger_patterns:
- domino modeling assistant
- domino model assistant
- domino ai modeling
---

# Introduction

This skill provides comprehensive knowledge for enabling modeling assistant within Domino Data Lab, allowing AI coding assistants to interact with the platform.

Vibe modeling refers to using AI code assistants to go beyond pure code generation and assist with:
- Experiment setup and configuration
- Data analysis and exploration
- Model training and evaluation
- Results interpretation

## Key Components

### MCP (Model Context Protocol)

MCP servers bridge AI coding assistants with the Domino platform APIs we typically need for running jobs (because its better to run analysis and training scripts via jobs than locally), checking job activity and results, saving files to DFS (domino file system) in cases where the project isn't using a git repo.

The Domino MCP Server is **bundled with this plugin** and starts automatically when the plugin is enabled. No manual MCP server installation or configuration is needed.

- **Inside a Domino workspace:** Authentication and project detection are fully automatic.
- **Outside Domino (laptop):** Set `DOMINO_API_KEY` and `DOMINO_HOST` environment variables in your shell. See [SETUP.md](./SETUP.md) for details.

## Related Documentation

- [SETUP.md](./SETUP.md) - Complete setup guide for the modeling assistant


## Important Considerations

You are a Domino Data Lab powered agentic coding tool that helps write code in addition to running tasks on the Domino Data Lab platform on behalf of the user using available tool functions provided by the domino_server MCP server. Whenever possible run commands as domino jobs rather than on the local terminal.

At the start of every session, call the get_domino_environment_info tool to detect the current environment. This tells you whether you are running inside a Domino workspace or on a laptop, provides the project owner and project name, indicates whether the project uses DFS or Git, and which authentication mode is active. When running inside a Domino workspace the project owner, project name, and DFS/Git mode are auto-detected — you do not need to read domino_project_settings.md. When running outside Domino (on a laptop), fall back to domino_project_settings.md for the project name, user name, and dfs setting.

When running a job, always check its status and results if completed and briefly explain any conclusions from the result of the job run. If a job result ever includes an mlflow or experiment run URL, always share that with the user using the open_web_browser tool.

Any requests related to understanding or manipulating project data should assume a dataset file is already part of the domino project and accessible via job runs. Always create scripts to understand and transform data via job runs. The script can assume all project data is accessible under the '/mnt/data/' directory or the '/mnt/imported/data/' directory, be sure to understand the full path to a dataset file before using it by running a job to list all folder contents recursively. Analytical outputs should be in plain text tabular format sent to stdout, this makes it easier to check results from the job run.

If the project is DFS instead of Git based (auto-detected inside Domino, or dfs=true in domino_project_settings.md when outside Domino), the datasets path is under /domino/datasets/*

Any scripts used to analyze or transform data within a Domino project should not be deleted. When performing analysis, generate useful summary charts in an image format and save to the project files.

Always check if our local project has uncommitted changes. For Git-based projects, you must commit and push changes before attempting to run any domino jobs otherwise domino can't see the new file changes. For DFS-based projects (auto-detected or dfs=true in domino_project_settings.md), use the MCP Server file sync functions (upload_file_to_domino_project, smart_sync_file, etc.) instead of git before running any jobs.

When training a model use mlflow instrumentation assuming a server is running, no need to set the url or anything, it should just work.


If domino_project_settings.md is not present, the owner and project_name can potentially be determined by environment variables if running inside a Domino workspace:

DOMINO_PROJECT_NAME
DOMINO_PROJECT_OWNER

## MCP Server Tools

The Domino MCP Server (bundled at `mcp-servers/domino_mcp_server/`) provides tools for interacting with jobs and the DFS file system (if not using git).

| Tool | Description |
|------|-------------|
| `get_domino_environment_info` | Detect workspace vs laptop, project info, auth mode |
| `run_domino_job` | Execute commands as Domino jobs |
| `check_domino_job_run_status` | Check if a job is finished, in-progress, or errored |
| `check_domino_job_run_results` | Retrieve stdout results from a completed job |
| `open_web_browser` | Open a URL (e.g. MLflow experiment link) in the browser |
| `list_domino_project_files` | List files in a DFS project |
| `upload_file_to_domino_project` | Upload a file to a DFS project |
| `download_file_from_domino_project` | Download a file from a DFS project |
| `sync_local_file_to_domino` | Read a local file and upload it to a DFS project |
| `smart_sync_file` | Upload with conflict detection for DFS projects |

Upstream source: https://github.com/dominodatalab/domino_mcp_server


---

## Reference Documentation


### Setup

# Complete Modeling Assistant Setup Guide

This guide covers setup for the Domino modeling assistant. The Domino MCP Server is **bundled with this plugin** and starts automatically — no manual cloning, installation, or MCP configuration is required.

**Inside a Domino workspace:** Everything is auto-detected (project, auth, DFS/Git mode). Skip straight to [Step 3: Test the Integration](#step-3-test-the-integration).

**Outside Domino (laptop):** You need to set two environment variables and create a project settings file. Follow the full guide below.

## Prerequisites

- Domino Data Lab account with API access
- Claude Code or Cursor IDE (or compatible MCP-enabled assistant)
- Python 3.11+
- `uv` package manager ([install guide](https://github.com/astral-sh/uv))
- Git

## Step 1: Set Domino Credentials (Laptop Only)

> **Skip this step if you are working inside a Domino workspace.** Authentication is handled automatically via ephemeral tokens.

### Generate API Key

1. Log into Domino
2. Go to **Account Settings** (click your profile icon)
3. Navigate to **API Keys**
4. Click **Generate New Key**
5. Copy and save the key securely

### Set Environment Variables

Add these to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.):

```bash
export DOMINO_API_KEY="your_api_key_here"
export DOMINO_HOST="https://your-domino.company.com"
```

Then reload your shell:

```bash
source ~/.zshrc  # or ~/.bashrc
```

The plugin's bundled MCP server picks these up automatically via the `.mcp.json` configuration — no `.env` file is needed.

## Step 2: Configure Your Project (Laptop Only)

> **Skip this step if you are working inside a Domino workspace.** The project owner, project name, and DFS/Git mode are auto-detected from platform environment variables.

### Create Project Settings

In your Domino project directory, create `domino_project_settings.md`:

```markdown
# Domino Project Settings

## Project Information
- **Project Owner**: your-username
- **Project Name**: your-project-name

## Default Configuration
- **Compute Environment**: Default Python 3.10
- **Hardware Tier**: small-k8s

## Data Locations
- Input data: /mnt/data/
- Imported datasets: /mnt/imported/data/
- Output artifacts: /mnt/artifacts/

## Notes
- Always commit changes before running Domino jobs
- Use MLflow for experiment tracking
```

## Step 3: Test the Integration

### Create a Test Script

In your project, create `test_domino.py`:

```python
import os
print("Hello from Domino!")
print(f"Project: {os.environ.get('DOMINO_PROJECT_NAME', 'unknown')}")
print(f"User: {os.environ.get('DOMINO_STARTING_USERNAME', 'unknown')}")
```

### Commit the Script

```bash
git add test_domino.py
git commit -m "Add test script for modeling assistant"
git push
```

### Run via Your AI Assistant

Prompt:
```
Run test_domino.py as a Domino job
```

The MCP server should:
1. Create a Domino job
2. Execute the script
3. Return the output

## Step 4: Set Up Domino Environment (Optional)

### Option A: Domino Standard Environment with AI Tools (Recommended)

If your Domino instance has the **Standard Environment with AI Tools** available, use that — it comes preconfigured with everything needed for the modeling assistant workflow. No additional setup required.

In your Domino project:

1. Go to **Settings** → **Compute Environment**
2. Select the **Standard Environment with AI Tools** from the list

### Option B: Custom Vibe Modeling Image (Fallback)

If you don't have access to the Standard Environment with AI Tools, use the custom Docker image instead.

In your Domino project:

1. Go to **Settings** → **Compute Environment**
2. Create new environment with base image:
   ```
   quay.io/domino/field:vibe-modeling
   ```

This image includes:
- MCP server dependencies
- Common ML libraries
- Preconfigured for modeling assistant workflows

## Workflow Example

### Complete Modeling Assistant Session

1. **Start in your AI assistant** with your project open

2. **Analyze data** (prompt):
   ```
   Load the sales data from /mnt/data/sales.csv and show me
   a summary of the key metrics
   ```

3. **Assistant creates script**, commits, runs in Domino

4. **Review results** returned through MCP

5. **Iterate on analysis** (prompt):
   ```
   Now create a visualization of sales by region and save it
   to /mnt/artifacts/sales_by_region.png
   ```

6. **Train a model** (prompt):
   ```
   Train a random forest model to predict sales using the
   processed data. Log the results to MLflow.
   ```

7. **All work is tracked** in Domino's experiment manager

## Troubleshooting

### "MCP server not found" or tools not appearing

1. Ensure `uv` is installed and in your PATH
2. Restart Claude Code / Cursor after installing the plugin
3. Check plugin is enabled: `/plugin` → Installed tab
4. Run `claude --debug` to see MCP server initialization errors

### "Unauthorized" errors

1. **Workspace:** This shouldn't happen — auth is automatic. Restart the workspace if it persists.
2. **Laptop:** Verify `DOMINO_API_KEY` and `DOMINO_HOST` are set in your shell environment (`echo $DOMINO_API_KEY`)

### "Project not found"

1. **Workspace:** Project info is auto-detected. Check that `DOMINO_PROJECT_OWNER` and `DOMINO_PROJECT_NAME` env vars are set.
2. **Laptop:** Check that `domino_project_settings.md` exists in your project root with the correct owner and project name.

### Jobs fail immediately

1. Check compute environment is available
2. Verify hardware tier is valid
3. Review Domino job logs for errors

## Next Steps

- [SKILL.md](./SKILL.md) - Overview of modeling assistant capabilities and MCP server tool reference
- [Domino Blueprints](https://domino.ai/resources/blueprints/vibe-modeling) - Official documentation

