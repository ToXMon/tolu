---
name: domino-workspaces
description: Work with Domino Workspaces - interactive development environments including
  Jupyter, JupyterLab, VS Code, and RStudio. Covers launching workspaces, configuring
  hardware tiers, environment selection, volume mounting, SSH access, and package
  installation. Use when setting up development environments, configuring workspace
  settings, or troubleshooting IDE issues.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- jupyter
- vscode
- rstudio
- ide
trigger_patterns:
- domino workspace
- domino jupyter
- domino vscode
- domino rstudio
---

# Domino Workspaces Skill

## Description
This skill helps users work with Domino Workspaces - interactive development environments for data science work including Jupyter notebooks, JupyterLab, VS Code, and RStudio.

## Activation
Activate this skill when users want to:
- Launch or configure a workspace in Domino
- Work with Jupyter notebooks, VS Code, or RStudio
- Configure workspace settings (hardware tier, environment, volumes)
- Understand workspace persistence and file management
- Use SSH to connect to remote workspaces
- Install packages in workspaces

## Workspace Types

### Available IDEs
Domino provides these default workspace types:
- **Jupyter Notebook**: Classic notebook interface
- **JupyterLab**: Modern Jupyter interface with file browser
- **VS Code**: Full-featured code editor with extensions
- **RStudio**: IDE for R development
- **Custom IDEs**: Can configure additional workspace types

## Launching a Workspace

### Via Domino UI
1. Navigate to your project
2. Click **Workspaces** in the navigation
3. Click **Launch Workspace**
4. Select:
   - **IDE**: Choose Jupyter, VS Code, RStudio, etc.
   - **Hardware Tier**: CPU/memory/GPU resources
   - **Compute Environment**: Docker environment with tools
   - **Volume Size**: Persistent storage (if needed)
5. Click **Launch**

### Via Python SDK
```python
from domino import Domino

domino = Domino("project-owner/project-name")

# Start a workspace
workspace = domino.workspace_start(
    environment_id="env-123",
    hardware_tier_name="small",
    workspace_type="JupyterLab"
)

print(f"Workspace ID: {workspace['workspaceId']}")
```

## File Persistence

### Persistent Directories
Work saved to these directories persists across workspace sessions:
- `/mnt/` - Project files (synced with Domino)
- `/mnt/data/` - Domino Datasets
- `/mnt/artifacts/` - Project artifacts
- `/mnt/imported/` - Imported data

### Home Directory Persistence
Domino 6.1+ supports home directory persistence:
- Installed packages persist across sessions
- User configurations (.bashrc, .vimrc) are retained
- Reduces workspace startup time

## Package Installation

### Temporary (Current Session)
```bash
# Python packages
pip install pandas numpy scikit-learn

# R packages
install.packages("tidyverse")
```

### Persistent (Via Environment)
Add to environment's Dockerfile instructions:
```dockerfile
RUN pip install pandas numpy scikit-learn
```

Or use requirements.txt in your project:
```text
pandas>=2.0.0
numpy>=1.24.0
scikit-learn>=1.3.0
```

## SSH Access to Workspaces

Domino 6.1+ allows SSH connections from local machines:

1. **Enable SSH** in workspace settings
2. **Get connection details** from running workspace
3. **Connect via SSH**:
```bash
ssh -i ~/.ssh/domino_key user@workspace-hostname
```

Benefits:
- Use local IDE (VS Code Remote, PyCharm)
- Access remote compute from local machine
- Browse files locally while computing remotely

## Git Integration in Workspaces

### Using Git
```bash
# Clone a repo in workspace
git clone https://github.com/user/repo.git

# Standard git workflow
git add .
git commit -m "Update model"
git push origin main
```

### Sync with Domino
Click **Sync** in the workspace UI to push changes back to Domino project.

## Workspace Operations

### Stop a Workspace
```python
domino.workspace_stop(workspace_id)
```

### Resume a Workspace
Stopped workspaces can be resumed to continue work.

### View Workspace Logs
Access logs for debugging through the Domino UI or API.

## Best Practices

1. **Save frequently**: Sync work to Domino regularly
2. **Use appropriate hardware**: Match resources to workload
3. **Clean up**: Stop workspaces when not in use to save resources
4. **Version control**: Use Git for code versioning
5. **Environment management**: Use Domino Environments for reproducibility

## Troubleshooting

### Workspace Won't Start
- Check hardware tier availability
- Verify environment builds successfully
- Check resource quotas

### Lost Work
- Check `/mnt/` directories for persisted files
- Review Domino project files
- Check Git history if using version control

### Slow Startup
- Use smaller base environments
- Enable package persistence
- Pre-install packages in environment Dockerfile

## Documentation Reference
- [Use Workspaces](https://docs.dominodatalab.com/en/latest/user_guide/867b72/use-workspaces/)
- [Launch a Workspace](https://docs.dominodatalab.com/en/latest/user_guide/e6e601/workspaces)
- [Start a Jupyter Workspace](https://docs.dominodatalab.com/en/latest/user_guide/93aef2/start-a-jupyter-workspace/)


---

## Reference Documentation


### Jupyter

# Jupyter Workspaces in Domino

## Overview

Domino provides both Jupyter Notebook and JupyterLab as workspace options for interactive Python development.

## Jupyter Notebook vs JupyterLab

| Feature | Jupyter Notebook | JupyterLab |
|---------|------------------|------------|
| Interface | Single notebook | Multi-tab IDE |
| File browser | Limited | Full-featured |
| Terminal | No | Yes |
| Extensions | Limited | Extensive |
| Best for | Quick analysis | Full development |

## Starting a Jupyter Workspace

### Via UI
1. Go to **Workspaces** > **Launch Workspace**
2. Select **JupyterLab** or **Jupyter Notebook**
3. Choose hardware tier and environment
4. Click **Launch**

### Via Python SDK
```python
from domino import Domino

domino = Domino("project-owner/project-name")

workspace = domino.workspace_start(
    workspace_type="JupyterLab",
    hardware_tier_name="small",
    environment_id="your-environment-id"
)
```

## Jupyter AI Integration

Domino supports Jupyter AI for in-notebook AI assistance.

### Setup
1. Use an environment with Jupyter AI installed
2. Configure AI provider credentials
3. Access via magic commands

### Usage
```python
# In a notebook cell
%ai ask "How do I load a CSV file?"

# Chat interface
%ai chat "Explain this error"
```

### Configure Provider
```python
%ai config --provider openai --model gpt-4
```

## Working with Notebooks

### Create New Notebook
1. In JupyterLab: **File** > **New** > **Notebook**
2. Select Python kernel

### Save and Sync
- Notebooks in `/mnt/` auto-sync to Domino
- Click **Sync** to manually push changes
- Use Git for version control

### Run Cells
- `Shift+Enter`: Run cell and move to next
- `Ctrl+Enter`: Run cell in place
- `Alt+Enter`: Run cell and insert new below

## Notebook Best Practices

### Structure
```python
# Cell 1: Imports
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

# Cell 2: Configuration
DATA_PATH = "/mnt/data/dataset.csv"
MODEL_PATH = "/mnt/artifacts/model.pkl"

# Cell 3: Load Data
df = pd.read_csv(DATA_PATH)

# Cell 4+: Analysis and modeling
```

### Documentation
Use Markdown cells for documentation:
```markdown
# Model Training

## Overview
This notebook trains a classification model on customer data.

## Data Sources
- `/mnt/data/customers.csv`: Customer features
- `/mnt/data/labels.csv`: Target labels
```

## Environment Variables

Access Domino environment variables in notebooks:
```python
import os

# Domino-provided variables
project_name = os.environ.get('DOMINO_PROJECT_NAME')
run_id = os.environ.get('DOMINO_RUN_ID')
username = os.environ.get('DOMINO_USER_NAME')

# Custom environment variables (set in project settings)
api_key = os.environ.get('MY_API_KEY')
```

## Accessing Data

### Domino Datasets
```python
# Datasets are mounted at /mnt/data/{dataset-name}
df = pd.read_csv("/mnt/data/my-dataset/data.csv")
```

### Project Files
```python
# Project files in /mnt/
df = pd.read_csv("/mnt/code/data/input.csv")
```

### External Data
```python
# Use data source connectors
from domino_data.data_sources import DataSourceClient

client = DataSourceClient()
df = client.get_datasource("my-datasource").get_as_df(
    "SELECT * FROM customers"
)
```

## Saving Results

### Artifacts
```python
import joblib

# Save model to artifacts (persisted)
joblib.dump(model, "/mnt/artifacts/model.joblib")
```

### Output Files
```python
# Save to project (synced)
df.to_csv("/mnt/results/predictions.csv")
```

## Converting Notebooks to Scripts

### For Scheduled Jobs
Convert notebook to Python script:
```bash
jupyter nbconvert --to script notebook.ipynb
```

### Using Papermill
Run notebooks programmatically:
```python
import papermill as pm

pm.execute_notebook(
    'input_notebook.ipynb',
    'output_notebook.ipynb',
    parameters={'data_path': '/mnt/data/new_data.csv'}
)
```

## Troubleshooting

### Kernel Dies
- Check memory usage in Domino UI
- Use larger hardware tier
- Optimize code to reduce memory

### Package Not Found
```python
# Install in notebook (temporary)
!pip install package-name

# For persistence, add to environment
```

### Notebook Won't Open
- Check file permissions
- Verify notebook JSON is valid
- Try opening in text editor first

## Documentation Reference
- [Start a Jupyter Workspace](https://docs.dominodatalab.com/en/latest/user_guide/93aef2/start-a-jupyter-workspace/)
- [Set up Jupyter AI](https://docs.dominodatalab.com/en/latest/user_guide/1f4149/set-up-jupyter-ai-in-jupyter-environment/)



### Vscode

# VS Code Workspaces in Domino

## Overview

Domino provides VS Code as a workspace option, offering a full-featured code editor with extensions, debugging, and terminal access.

## Features

- Full VS Code editor in browser
- Extension support
- Integrated terminal
- Git integration
- Debugging support
- GitHub Copilot support

## Starting a VS Code Workspace

### Via UI
1. Go to **Workspaces** > **Launch Workspace**
2. Select **VS Code**
3. Choose hardware tier and environment
4. Click **Launch**

### Via Python SDK
```python
from domino import Domino

domino = Domino("project-owner/project-name")

workspace = domino.workspace_start(
    workspace_type="VSCode",
    hardware_tier_name="medium",
    environment_id="your-environment-id"
)
```

## VS Code Extensions

### Pre-installed Extensions
Domino VS Code workspaces typically include:
- Python extension
- Jupyter extension
- Git extension

### Installing Additional Extensions
1. Open Extensions panel (`Ctrl+Shift+X`)
2. Search for extension
3. Click **Install**

Note: Extensions installed in a session may not persist. For permanent extensions, configure in the Domino Environment.

## GitHub Copilot Integration

### Setup
1. Ensure GitHub Copilot is enabled in your organization
2. Sign in with GitHub in VS Code
3. Authorize Copilot

### Usage
```python
# Start typing and Copilot suggests completions
def calculate_mean(numbers):
    # Copilot will suggest implementation
```

## Remote SSH Access

Connect to Domino workspaces from your local VS Code:

### Prerequisites
- Domino 6.1+
- VS Code Remote SSH extension locally
- SSH access enabled on workspace

### Setup
1. Install **Remote - SSH** extension in local VS Code
2. Get SSH connection string from Domino workspace
3. Add to SSH config:
```
Host domino-workspace
    HostName workspace-hostname.domino.tech
    User domino
    IdentityFile ~/.ssh/domino_key
```

4. Connect: `Remote-SSH: Connect to Host` > `domino-workspace`

### Benefits
- Use local VS Code with remote compute
- All local extensions available
- Faster response than browser-based VS Code

## Working with Python

### Select Interpreter
1. `Ctrl+Shift+P` > **Python: Select Interpreter**
2. Choose the correct Python environment

### Run Code
- `F5`: Run with debugger
- `Ctrl+F5`: Run without debugger
- Right-click > **Run Python File**

### Debug
```python
# Add breakpoints by clicking line numbers
# Press F5 to start debugging
# Use debug toolbar to step through code
```

## Working with Jupyter Notebooks

VS Code supports Jupyter notebooks natively:

1. Create new notebook: `Ctrl+Shift+P` > **Create: New Jupyter Notebook**
2. Or open existing `.ipynb` file
3. Run cells with `Shift+Enter`

## Terminal Access

Open integrated terminal:
- `Ctrl+`` (backtick)
- Or **Terminal** > **New Terminal**

```bash
# Run commands
pip install pandas
python train.py
git status
```

## File Management

### Project Files
- Located in `/mnt/` directory
- Auto-synced with Domino project
- Use Explorer panel to navigate

### Save and Sync
- Files auto-save (configurable)
- Click **Sync** in Domino UI to push to project
- Or use Git for version control

## Settings

### User Settings
`Ctrl+,` to open settings

Common settings:
```json
{
    "editor.fontSize": 14,
    "editor.tabSize": 4,
    "python.linting.enabled": true,
    "python.formatting.provider": "black",
    "files.autoSave": "afterDelay"
}
```

### Workspace Settings
Create `.vscode/settings.json` in project:
```json
{
    "python.defaultInterpreterPath": "/opt/conda/bin/python",
    "python.terminal.activateEnvironment": true
}
```

## Git Integration

### Initialize Repository
```bash
git init
git remote add origin https://github.com/user/repo.git
```

### Source Control Panel
- View changes in Source Control panel
- Stage, commit, push from UI
- View diffs inline

### Git Commands
`Ctrl+Shift+G` to open Source Control

## Keyboard Shortcuts

| Action | Shortcut |
|--------|----------|
| Command Palette | `Ctrl+Shift+P` |
| Quick Open File | `Ctrl+P` |
| Find in Files | `Ctrl+Shift+F` |
| Toggle Terminal | `Ctrl+`` |
| Toggle Sidebar | `Ctrl+B` |
| Go to Definition | `F12` |
| Find References | `Shift+F12` |

## Troubleshooting

### VS Code Slow
- Check hardware tier resources
- Close unused extensions
- Reduce number of open files

### Extensions Not Working
- Check extension compatibility with VS Code version
- Verify dependencies are installed
- Check extension logs

### Can't Connect Remote SSH
- Verify SSH is enabled on workspace
- Check firewall rules
- Verify SSH key permissions

## Documentation Reference
- [Configure native Workspaces](https://docs.dominodatalab.com/en/latest/user_guide/4e7f25/configure-native-workspaces/)
- [Use Workspaces](https://docs.dominodatalab.com/en/latest/user_guide/867b72/use-workspaces/)

