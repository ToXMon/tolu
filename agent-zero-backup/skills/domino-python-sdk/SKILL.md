---
name: domino-python-sdk
description: Programmatically interact with Domino using python-domino SDK and REST
  APIs. Covers authentication, running jobs, managing projects, file operations, model
  deployment, and automation. Use when automating Domino workflows, integrating with
  CI/CD, or building custom tooling around Domino.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- python
- sdk
- api
- automation
trigger_patterns:
- domino python sdk
- domino api python
- python-domino
- domino automation
---

# Domino Python SDK Skill

## Description
This skill helps users work with the Domino Python SDK (python-domino) and REST APIs to programmatically interact with Domino.

## Activation
Activate this skill when users want to:
- Use the Domino Python SDK
- Make API calls to Domino
- Automate Domino workflows
- Integrate Domino with external systems
- Query Domino programmatically

## Overview

Domino provides two main programmatic interfaces:
- **python-domino**: Python SDK for common operations
- **REST API**: Full HTTP API for all Domino features

## Installation

### python-domino
```bash
# Install from PyPI
pip install dominodatalab

# Or install with extras
pip install "dominodatalab[data]"
```

### In Domino Environment
Add to requirements.txt:
```
dominodatalab>=1.4.0
```

Or Dockerfile:
```dockerfile
RUN pip install dominodatalab
```

## Authentication

### API Key
Get your API key from Domino:
1. Go to **Account Settings**
2. Click **API Keys**
3. Generate or copy key

### Configure SDK
```python
from domino import Domino

# Option 1: Pass credentials directly
domino = Domino(
    host="https://your-domino.com",
    api_key="your-api-key",
    project="owner/project-name"
)

# Option 2: Environment variables
import os
os.environ["DOMINO_API_HOST"] = "https://your-domino.com"
os.environ["DOMINO_USER_API_KEY"] = "your-api-key"

domino = Domino("owner/project-name")

# Option 3: Inside Domino (auto-configured)
domino = Domino("owner/project-name")  # Uses built-in auth
```

## Common Operations

### Projects

```python
from domino import Domino

domino = Domino()

# Create project
project = domino.project_create(
    project_name="my-new-project",
    owner_name="username"
)

# Get project info
info = domino.project_info()
print(f"Project: {info['name']}")
print(f"ID: {info['id']}")
```

### Jobs (Runs)

```python
# Start a job
run = domino.runs_start(
    command="python train.py --epochs 100",
    hardware_tier_name="medium",
    environment_id="env-id"
)
print(f"Run ID: {run['runId']}")

# Start job with different commit
run = domino.runs_start(
    command="python train.py",
    commit_id="abc123"
)

# Check status
status = domino.runs_status(run['runId'])
print(f"Status: {status['status']}")

# Wait for completion
domino.runs_wait(run['runId'])

# Get logs
logs = domino.runs_get_logs(run['runId'])
print(logs)

# Stop a run
domino.runs_stop(run['runId'])
```

### Workspaces

```python
# Start workspace
workspace = domino.workspace_start(
    hardware_tier_name="medium",
    environment_id="env-id",
    workspace_type="JupyterLab"
)
print(f"Workspace ID: {workspace['workspaceId']}")

# Stop workspace
domino.workspace_stop(workspace['workspaceId'])
```

### Files

```python
# Upload file
domino.files_upload(
    path="local/file.csv",
    dest_path="/mnt/code/data/"
)

# Download file
domino.files_download(
    path="/mnt/code/results/output.csv",
    dest_path="local/output.csv"
)

# List files
files = domino.files_list("/mnt/code/")
for f in files:
    print(f['path'])
```

### Datasets

```python
# Create dataset
dataset = domino.datasets_create(
    name="training-data",
    description="Training dataset"
)

# List datasets
datasets = domino.datasets_list()

# Create snapshot
snapshot = domino.datasets_snapshot(
    dataset_name="training-data",
    tag="v1.0"
)
```

### Environments

```python
# List environments
environments = domino.environments_list()
for env in environments:
    print(f"{env['name']}: {env['id']}")

# Get environment details
env = domino.environment_get("env-id")
```

### Model APIs

```python
# Publish model
model = domino.model_publish(
    file="model.py",
    function="predict",
    environment_id="env-id",
    name="my-classifier",
    description="Classification model"
)
print(f"Model ID: {model['id']}")

# List models
models = domino.models_list()

# Get model info
model_info = domino.model_get("model-id")
```

## REST API

### Direct API Calls
```python
import requests

headers = {
    "X-Domino-Api-Key": "your-api-key",
    "Content-Type": "application/json"
}

# Get projects
response = requests.get(
    "https://your-domino.com/v4/projects",
    headers=headers
)
projects = response.json()

# Start a run
response = requests.post(
    f"https://your-domino.com/v4/projects/{project_id}/runs",
    headers=headers,
    json={
        "command": "python train.py",
        "hardwareTierId": "tier-id"
    }
)
run = response.json()
```

### Common Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v4/projects` | GET | List projects |
| `/v4/projects/{id}/runs` | POST | Start a run |
| `/v4/projects/{id}/runs/{runId}` | GET | Get run status |
| `/v4/projects/{id}/files` | GET | List files |
| `/v4/gateway/runs/{runId}/logs` | GET | Get run logs |
| `/v4/models` | GET | List models |
| `/v4/models/{id}/latest/model` | POST | Call model |

## Domino Data API

Separate SDK for data access:

```python
from domino_data.data_sources import DataSourceClient

# Initialize client
client = DataSourceClient()

# List data sources
sources = client.list_data_sources()

# Query data source
df = client.get_datasource("my-datasource").query(
    "SELECT * FROM customers WHERE region = 'US'"
)
```

## Automation Examples

### CI/CD Integration
```python
# trigger_training.py - Call from CI/CD pipeline
from domino import Domino
import sys

domino = Domino("team/ml-project")

# Start training job
run = domino.runs_start(
    command="python train.py",
    hardware_tier_name="gpu-large"
)

# Wait for completion
result = domino.runs_wait(run['runId'])

if result['status'] != 'Succeeded':
    print(f"Training failed: {result['status']}")
    sys.exit(1)

print("Training completed successfully!")
```

### Batch Job Scheduler
```python
# Run multiple experiments
from domino import Domino
import itertools

domino = Domino("team/experiments")

# Parameter grid
params = {
    "learning_rate": [0.01, 0.001, 0.0001],
    "batch_size": [32, 64, 128]
}

# Generate combinations
combinations = list(itertools.product(*params.values()))
param_names = list(params.keys())

# Submit all experiments
runs = []
for combo in combinations:
    param_str = " ".join(
        f"--{name}={value}"
        for name, value in zip(param_names, combo)
    )
    run = domino.runs_start(
        command=f"python experiment.py {param_str}",
        hardware_tier_name="gpu-small"
    )
    runs.append(run['runId'])
    print(f"Started run {run['runId']} with {param_str}")

# Wait for all to complete
for run_id in runs:
    result = domino.runs_wait(run_id)
    print(f"Run {run_id}: {result['status']}")
```

### Model Deployment Pipeline
```python
from domino import Domino

domino = Domino("team/model-deployment")

# 1. Train model
train_run = domino.runs_start(command="python train.py")
domino.runs_wait(train_run['runId'])

# 2. Evaluate model
eval_run = domino.runs_start(command="python evaluate.py")
domino.runs_wait(eval_run['runId'])

# 3. Deploy if evaluation passes
# (Check evaluation results first)
model = domino.model_publish(
    file="serve.py",
    function="predict",
    name="production-model"
)

print(f"Model deployed: {model['id']}")
```

## Error Handling

```python
from domino import Domino
from domino.exceptions import DominoException

try:
    domino = Domino("team/project")
    run = domino.runs_start(command="python train.py")
except DominoException as e:
    print(f"Domino error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Best Practices

### 1. Use Environment Variables
```python
import os

# Don't hardcode credentials
api_key = os.environ.get("DOMINO_USER_API_KEY")
host = os.environ.get("DOMINO_API_HOST")
```

### 2. Handle Rate Limits
```python
import time
from domino.exceptions import DominoException

def api_call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except DominoException as e:
            if "rate limit" in str(e).lower():
                time.sleep(2 ** attempt)
            else:
                raise
    raise Exception("Max retries exceeded")
```

### 3. Log API Calls
```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def start_run(command):
    logger.info(f"Starting run: {command}")
    run = domino.runs_start(command=command)
    logger.info(f"Run ID: {run['runId']}")
    return run
```

## Detailed API Reference

For comprehensive REST API documentation, see these specialized guides:

| Guide | Description |
|-------|-------------|
| [API-PROJECTS.md](API-PROJECTS.md) | Projects, collaborators, Git repos, goals |
| [API-JOBS.md](API-JOBS.md) | Jobs, scheduled jobs, logs, tags |
| [API-DATASETS.md](API-DATASETS.md) | Datasets, snapshots, tags, grants |
| [API-MODELS.md](API-MODELS.md) | Model APIs, deployments, registry |
| [API-ENVIRONMENTS.md](API-ENVIRONMENTS.md) | Environments, revisions, Dockerfile |
| [API-APPS.md](API-APPS.md) | Apps, versions, instances, logs |
| [API-ADMIN.md](API-ADMIN.md) | Users, orgs, hardware tiers, data sources |
| [API-REFERENCE.md](API-REFERENCE.md) | Complete endpoint reference |

## Documentation Reference
- [API Guide](https://docs.dominodatalab.com/en/latest/api_guide/f35c19/api-guide/)
- [REST API Reference](https://docs.dominodatalab.com/en/latest/api_guide/8c929e/domino-platform-api-reference/)
- [python-domino Library](https://docs.dominodatalab.com/en/latest/api_guide/c5ef26/the-python-domino-library/)
- [GitHub Repository](https://github.com/dominodatalab/python-domino)


---

## Reference Documentation


### Api Admin

# Domino Admin API

## Overview
The Admin API covers administrative endpoints for managing users, organizations, hardware tiers, data sources, and platform configuration.

## Authentication
```python
import requests

headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
base_url = "https://your-domino.com"
```

---

## Users API

### Get Current User
```
GET /api/users/v1/self
```

Get information about the authenticated user.

**Example:**
```python
response = requests.get(
    f"{base_url}/api/users/v1/self",
    headers=headers
)
user = response.json()
print(f"User: {user['userName']}")
print(f"Email: {user['email']}")
```

**Response:**
```json
{
  "id": "user-123",
  "userName": "jsmith",
  "email": "jsmith@company.com",
  "firstName": "John",
  "lastName": "Smith",
  "isAdmin": false
}
```

---

### List Users
```
GET /api/users/v1/users
```

Get all users visible to the current user.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `offset` | int | Pagination offset |
| `limit` | int | Results per page |

---

### User Git Credentials
```
GET /api/users/beta/credentials/{userId}
```

Get Git credential accessor for a user.

### Update Git Credentials
```
PUT /api/users/v1/user/{userId}/tokenCredentials/{credentialId}
```

---

## Organizations API

### List Organizations
```
GET /api/organizations/v1/organizations
```

Get organizations for the current user.

**Example:**
```python
response = requests.get(
    f"{base_url}/api/organizations/v1/organizations",
    headers=headers
)
orgs = response.json()
```

---

### Create Organization
```
POST /api/organizations/v1/organizations
```

**Request Body:**
```json
{
  "name": "data-science-team",
  "description": "Data Science Team Organization"
}
```

---

### Get Organization
```
GET /api/organizations/v1/organizations/{organizationId}
```

---

### Get All Organizations (Admin)
```
GET /api/organizations/v1/organizations/all
```

Only accessible to admin users.

---

### Add User to Organization
```
PUT /api/organizations/v1/organizations/{organizationId}/user
```

**Request Body:**
```json
{
  "userId": "user-456",
  "role": "Member"
}
```

---

### Remove User from Organization
```
DELETE /api/organizations/v1/organizations/{organizationId}/user
```

**Request Body:**
```json
{
  "userId": "user-456"
}
```

---

## Hardware Tiers API

### List Hardware Tiers
```
GET /api/hardwaretiers/v1/hardwaretiers
```

Get all available hardware tiers.

**Example:**
```python
response = requests.get(
    f"{base_url}/api/hardwaretiers/v1/hardwaretiers",
    headers=headers
)
tiers = response.json()

for tier in tiers['data']:
    print(f"{tier['name']}: {tier['cores']} cores, {tier['memoryMb']}MB RAM")
```

**Response:**
```json
{
  "data": [
    {
      "id": "tier-123",
      "name": "small",
      "cores": 2,
      "memoryMb": 8192,
      "gpuCount": 0,
      "isDefault": false
    },
    {
      "id": "tier-456",
      "name": "gpu-large",
      "cores": 8,
      "memoryMb": 32768,
      "gpuCount": 1,
      "gpuType": "nvidia-tesla-v100"
    }
  ]
}
```

---

### Get Hardware Tier
```
GET /api/hardwaretiers/v1/hardwaretiers/{hardwareTierId}
```

---

### Create Hardware Tier (Admin)
```
POST /api/hardwaretiers/v1/hardwaretiers
```

**Request Body:**
```json
{
  "name": "custom-large",
  "cores": 16,
  "memoryMb": 65536,
  "gpuCount": 2
}
```

---

### Update Hardware Tier (Admin)
```
PUT /api/hardwaretiers/v1/hardwaretiers
```

---

### Archive Hardware Tier (Admin)
```
DELETE /api/hardwaretiers/v1/hardwaretiers/{hardwareTierId}
```

---

## Data Sources API

### List Data Sources
```
GET /api/datasource/v1/datasources
```

Get all active data sources the user has access to.

**Example:**
```python
response = requests.get(
    f"{base_url}/api/datasource/v1/datasources",
    headers=headers
)
sources = response.json()
```

---

### Create Data Source
```
POST /api/datasource/v1/datasources
```

**Request Body:**
```json
{
  "name": "postgres-prod",
  "type": "PostgreSQL",
  "config": {
    "host": "db.company.com",
    "port": 5432,
    "database": "analytics"
  }
}
```

---

### Get Data Source
```
GET /api/datasource/v1/datasources/{dataSourceId}
```

---

### Update Data Source
```
PATCH /api/datasource/v1/datasources/{dataSourceId}
```

---

### Delete Data Source
```
DELETE /api/datasource/v1/datasources/{dataSourceId}
```

---

### Data Source Audit
```
GET /api/datasource/v1/audit
```

Get audit logs for data source access.

---

## Service Accounts API

### List Service Accounts
```
GET /api/serviceAccounts/v1/serviceAccounts
```

---

### Create Service Account
```
POST /api/serviceAccounts/v1/serviceAccounts
```

**Request Body:**
```json
{
  "name": "ci-cd-service",
  "description": "Service account for CI/CD pipelines"
}
```

---

### Create Token
```
POST /api/serviceAccounts/v1/serviceAccounts/{serviceAccountId}/tokens
```

Create API token for service account.

---

### List Tokens
```
GET /api/serviceAccounts/v1/serviceAccounts/{serviceAccountId}/tokens
```

---

## Deployment Targets API (Admin)

### List Deployment Target Types
```
GET /api/admin/v1/deploymentTargetTypes
```

### Get Deployment Target Type
```
GET /api/admin/v1/deploymentTargetTypes/{typeId}
```

### List Deployment Targets
```
GET /api/admin/v1/deploymentTargets
```

### Create Deployment Target
```
POST /api/admin/v1/deploymentTargets
```

### Get Deployment Target
```
GET /api/admin/v1/deploymentTargets/{targetId}
```

### Update Deployment Target
```
PATCH /api/admin/v1/deploymentTargets/{targetId}
```

### Delete Deployment Target
```
DELETE /api/admin/v1/deploymentTargets/{targetId}
```

---

## Resource Configurations

### List Resource Configurations
```
GET /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations
```

### Create Resource Configuration
```
POST /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations
```

### Get Resource Configuration
```
GET /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations/{configId}
```

### Update Resource Configuration
```
PATCH /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations/{configId}
```

### Delete Resource Configuration
```
DELETE /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations/{configId}
```

---

## Cost API

### Get Cost Allocation
```
GET /api/cost/v1/allocation
```

Get detailed cost breakdown.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `startTime` | string | ISO 8601 start time |
| `endTime` | string | ISO 8601 end time |
| `aggregateBy` | string | user, project, organization |

**Example:**
```python
response = requests.get(
    f"{base_url}/api/cost/v1/allocation",
    headers=headers,
    params={
        "startTime": "2024-01-01T00:00:00Z",
        "endTime": "2024-01-31T23:59:59Z",
        "aggregateBy": "project"
    }
)
costs = response.json()
```

---

### Get Cost Summary
```
GET /api/cost/v1/allocation/summary
```

Faster summary-level cost data.

---

### Get Asset Costs
```
GET /api/cost/v1/asset
```

---

## Billing Tags

### List Billing Tags
```
GET /api/cost/v1/billingtags
```

### Create/Update Billing Tags
```
POST /api/cost/v1/billingtags
```

### Billing Tag Settings
```
GET /api/cost/v1/billingtagSettings
PUT /api/cost/v1/billingtagSettings
```

### Billing Tag Mode
```
GET /api/cost/v1/billingtagSettings/mode
PUT /api/cost/v1/billingtagSettings/mode
```

---

## Audit Events API

### Get Audit Events
```
GET /auditevents
```

Get platform audit events.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `startTime` | string | Filter start |
| `endTime` | string | Filter end |
| `eventType` | string | Filter by event type |

**Example:**
```python
response = requests.get(
    f"{base_url}/auditevents",
    headers=headers,
    params={
        "startTime": "2024-01-01T00:00:00Z",
        "endTime": "2024-01-02T00:00:00Z"
    }
)
events = response.json()
```

---

## Common Admin Tasks

### Create Service Account for CI/CD
```python
# Create service account
response = requests.post(
    f"{base_url}/api/serviceAccounts/v1/serviceAccounts",
    headers=headers,
    json={
        "name": "github-actions",
        "description": "Service account for GitHub Actions"
    }
)
sa = response.json()
sa_id = sa['id']

# Create API token
response = requests.post(
    f"{base_url}/api/serviceAccounts/v1/serviceAccounts/{sa_id}/tokens",
    headers=headers,
    json={"description": "CI/CD token"}
)
token = response.json()
print(f"API Token: {token['token']}")  # Save this securely!
```

### Get Platform Usage Report
```python
# Get cost allocation by user
response = requests.get(
    f"{base_url}/api/cost/v1/allocation",
    headers=headers,
    params={
        "startTime": "2024-01-01T00:00:00Z",
        "endTime": "2024-01-31T23:59:59Z",
        "aggregateBy": "user"
    }
)
usage = response.json()

for user in usage['data']:
    print(f"{user['name']}: ${user['totalCost']:.2f}")
```



### Api Apps

# Domino Apps API

## Overview
The Apps API allows you to create, manage, and deploy web applications in Domino.

## Authentication
```python
import requests

headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
base_url = "https://your-domino.com"
```

---

## Endpoints

### List Apps
```
GET /api/apps/beta/apps
```

Get apps visible to the user.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `projectId` | string | Filter by project |
| `status` | string | Filter by status |
| `offset` | int | Pagination offset |
| `limit` | int | Results per page |

**Status Values:**
- `Running`
- `Stopped`
- `Starting`
- `Failed`

**Example:**
```python
response = requests.get(
    f"{base_url}/api/apps/beta/apps",
    headers=headers,
    params={
        "status": "Running",
        "limit": 20
    }
)
apps = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "id": "app-123",
      "name": "Dashboard App",
      "description": "Sales analytics dashboard",
      "projectId": "project-456",
      "status": "Running",
      "url": "https://your-domino.com/apps/app-123",
      "createdAt": "2024-01-15T10:00:00Z"
    }
  ],
  "offset": 0,
  "limit": 20,
  "totalCount": 5
}
```

---

### Create App
```
POST /api/apps/beta/apps
```

Create a new application.

**Request Body:**
```json
{
  "projectId": "project-123",
  "name": "analytics-dashboard",
  "description": "Real-time analytics dashboard",
  "hardwareTierId": "small",
  "environmentId": "env-789"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/apps/beta/apps",
    headers=headers,
    json={
        "projectId": "project-123",
        "name": "customer-insights",
        "description": "Customer analytics dashboard",
        "hardwareTierId": "small",
        "environmentId": "env-789"
    }
)
app = response.json()
print(f"Created app: {app['id']}")
print(f"URL: {app['url']}")
```

---

### Get App
```
GET /api/apps/beta/apps/{appId}
```

**Example:**
```python
app_id = "app-123"
response = requests.get(
    f"{base_url}/api/apps/beta/apps/{app_id}",
    headers=headers
)
app = response.json()
```

---

### Update App
```
PATCH /api/apps/beta/apps/{appId}
```

Update app metadata.

**Request Body:**
```json
{
  "name": "new-name",
  "description": "Updated description"
}
```

---

### Delete App
```
DELETE /api/apps/beta/apps/{appId}
```

---

## App Versions

### List Versions
```
GET /api/apps/beta/apps/{appId}/versions
```

Get all versions of an app.

### Create New Version
```
POST /api/apps/beta/apps/{appId}/versions
```

Publish a new version of the app.

**Request Body:**
```json
{
  "hardwareTierId": "medium",
  "environmentId": "env-789"
}
```

### Get Version
```
GET /api/apps/beta/apps/{appId}/versions/{versionId}
```

### Update Version
```
PATCH /api/apps/beta/apps/{appId}/versions/{versionId}
```

---

## App Instances

### List Instances
```
GET /api/apps/beta/apps/{appId}/versions/{versionId}/instances
```

Get running instances of an app version.

### Get Instance
```
GET /api/apps/beta/apps/{appId}/versions/{versionId}/instances/{instanceId}
```

### Delete Instance
```
DELETE /api/apps/beta/apps/{appId}/versions/{versionId}/instances/{instanceId}
```

Stop and remove an app instance.

### Get Instance Logs
```
GET /api/apps/beta/apps/{appId}/versions/{versionId}/instances/{instanceId}/logs
```

**Example:**
```python
response = requests.get(
    f"{base_url}/api/apps/beta/apps/{app_id}/versions/{version_id}/instances/{instance_id}/logs",
    headers=headers
)
logs = response.text
print(logs)
```

### Get Real-Time Logs
```
GET /api/apps/beta/apps/{appId}/versions/{versionId}/instances/{instanceId}/realTimeLogs
```

Stream logs in real-time.

### Record View
```
POST /api/apps/beta/apps/{appId}/versions/{versionId}/instances/{instanceId}/views
```

Record an app view for analytics.

---

## App Thumbnail

### Get Thumbnail
```
GET /api/apps/beta/apps/{appId}/thumbnail
```

### Upload Thumbnail
```
POST /api/apps/beta/apps/{appId}/thumbnail
```

Upload a thumbnail image for the app.

### Delete Thumbnail
```
DELETE /api/apps/beta/apps/{appId}/thumbnail
```

### Get Thumbnail Metadata
```
GET /api/apps/beta/apps/{appId}/thumbnail/metadata
```

---

## App Views Analytics

### Get Views
```
GET /api/apps/beta/apps/{appId}/views
```

Get view statistics for an app.

**Query Parameters:**
- `startTime`: Filter start timestamp
- `endTime`: Filter end timestamp

---

## Vanity URLs

### Get by Vanity URL
```
GET /api/apps/beta/apps/vanityUrls/{vanityUrl}
```

Look up an app by its vanity URL.

---

## Filter Options

### Get Project Filter Options
```
GET /api/apps/beta/apps/projectFilterOptions
```

Get list of projects that have apps.

### Get Publisher Filter Options
```
GET /api/apps/beta/apps/publisherFilterOptions
```

Get list of users who have published apps.

---

## Access Requests

### Request Access
```
POST /api/apps/beta/apps/{appId}/access/requests
```

Request access to a private app.

---

## Complete Workflow Example

```python
import requests
import time

headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
base_url = "https://your-domino.com"

# 1. Create app
response = requests.post(
    f"{base_url}/api/apps/beta/apps",
    headers=headers,
    json={
        "projectId": "project-123",
        "name": "ml-dashboard",
        "description": "Machine learning model dashboard",
        "hardwareTierId": "small",
        "environmentId": "env-789"
    }
)
app = response.json()
app_id = app['id']
print(f"Created app: {app_id}")

# 2. Wait for app to start
while True:
    response = requests.get(
        f"{base_url}/api/apps/beta/apps/{app_id}",
        headers=headers
    )
    status = response.json()['status']

    if status == 'Running':
        print(f"App is running!")
        break
    elif status == 'Failed':
        print("App failed to start")
        break
    else:
        print(f"Status: {status}")
        time.sleep(10)

# 3. Get app URL
response = requests.get(
    f"{base_url}/api/apps/beta/apps/{app_id}",
    headers=headers
)
app_url = response.json()['url']
print(f"App URL: {app_url}")

# 4. View logs
versions = requests.get(
    f"{base_url}/api/apps/beta/apps/{app_id}/versions",
    headers=headers
).json()
version_id = versions['data'][0]['id']

instances = requests.get(
    f"{base_url}/api/apps/beta/apps/{app_id}/versions/{version_id}/instances",
    headers=headers
).json()
instance_id = instances['data'][0]['id']

logs = requests.get(
    f"{base_url}/api/apps/beta/apps/{app_id}/versions/{version_id}/instances/{instance_id}/logs",
    headers=headers
).text
print(f"Logs:\n{logs}")

# 5. Stop app (delete instance)
requests.delete(
    f"{base_url}/api/apps/beta/apps/{app_id}/versions/{version_id}/instances/{instance_id}",
    headers=headers
)
print("App stopped")
```

---

## App Types and Configuration

Apps in Domino require:
1. **app.sh**: Launch script that starts the app
2. **Proper host binding**: Bind to `0.0.0.0`
3. **Environment**: With required dependencies

Example `app.sh` for Streamlit:
```bash
#!/bin/bash
streamlit run app.py --server.port 8888 --server.address 0.0.0.0
```

Example for React/Vite:
```bash
#!/bin/bash
npm run build
npm run preview -- --host 0.0.0.0 --port 8888
```



### Api Datasets

# Domino Datasets API

## Overview
The Datasets API allows you to create, manage, and version Domino Datasets programmatically.

## Authentication
```python
import requests

headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
base_url = "https://your-domino.com"
```

---

## Endpoints

### List Datasets
```
GET /api/datasetrw/v2/datasets
```

Get datasets the user has access to.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `projectId` | string | Filter by project |
| `offset` | int | Pagination offset |
| `limit` | int | Results per page |

**Example:**
```python
response = requests.get(
    f"{base_url}/api/datasetrw/v2/datasets",
    headers=headers,
    params={"limit": 50}
)
datasets = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "id": "dataset-123",
      "name": "training-data",
      "description": "Training dataset for ML model",
      "projectId": "project-456",
      "createdAt": "2024-01-15T10:00:00Z",
      "sizeBytes": 1073741824
    }
  ],
  "offset": 0,
  "limit": 50,
  "totalCount": 1
}
```

---

### Create Dataset
```
POST /api/datasetrw/v1/datasets
```

Create a new dataset.

**Request Body:**
```json
{
  "name": "training-data",
  "description": "Training dataset for classification model",
  "projectId": "project-123"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/datasetrw/v1/datasets",
    headers=headers,
    json={
        "name": "customer-features",
        "description": "Processed customer features for modeling",
        "projectId": "project-123"
    }
)
dataset = response.json()
print(f"Created dataset: {dataset['id']}")
```

---

### Get Dataset
```
GET /api/datasetrw/v1/datasets/{datasetId}
```

**Example:**
```python
dataset_id = "dataset-123"
response = requests.get(
    f"{base_url}/api/datasetrw/v1/datasets/{dataset_id}",
    headers=headers
)
dataset = response.json()
```

---

### Update Dataset
```
PATCH /api/datasetrw/v1/datasets/{datasetId}
```

Update dataset metadata.

**Request Body:**
```json
{
  "name": "new-name",
  "description": "Updated description"
}
```

---

### Delete Dataset
```
DELETE /api/datasetrw/v1/datasets/{datasetId}
```

Delete a dataset (marks for deletion).

---

## Snapshots

### List Snapshots
```
GET /api/datasetrw/v1/datasets/{datasetId}/snapshots
```

Get all snapshots for a dataset.

**Example:**
```python
response = requests.get(
    f"{base_url}/api/datasetrw/v1/datasets/{dataset_id}/snapshots",
    headers=headers
)
snapshots = response.json()

for snapshot in snapshots['data']:
    print(f"Snapshot: {snapshot['id']} - Created: {snapshot['createdAt']}")
```

**Response:**
```json
{
  "data": [
    {
      "id": "snapshot-789",
      "datasetId": "dataset-123",
      "createdAt": "2024-01-15T10:00:00Z",
      "tags": ["v1.0", "production"]
    }
  ]
}
```

---

### Create Snapshot
```
POST /api/datasetrw/v1/datasets/{datasetId}/snapshots
```

Create a new snapshot of the current dataset state.

**Request Body:**
```json
{
  "tag": "v1.0"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/datasetrw/v1/datasets/{dataset_id}/snapshots",
    headers=headers,
    json={"tag": "v2.0"}
)
snapshot = response.json()
print(f"Created snapshot: {snapshot['id']}")
```

---

### Get Snapshot
```
GET /api/datasetrw/v1/snapshots/{snapshotId}
```

Get details for a specific snapshot.

---

## Tags

### Add Tag to Snapshot
```
POST /api/datasetrw/v1/datasets/{datasetId}/tags
```

Tag a snapshot in the dataset.

**Request Body:**
```json
{
  "snapshotId": "snapshot-789",
  "tagName": "production"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/datasetrw/v1/datasets/{dataset_id}/tags",
    headers=headers,
    json={
        "snapshotId": "snapshot-789",
        "tagName": "production"
    }
)
```

### Remove Tag
```
DELETE /api/datasetrw/v1/datasets/{datasetId}/tags/{tagName}
```

---

## Grants (Permissions)

### Get Dataset Grants
```
GET /api/datasetrw/v1/datasets/{datasetId}/grants
```

Get permission grants for a dataset.

### Add Grant
```
POST /api/datasetrw/v1/datasets/{datasetId}/grants
```

**Request Body:**
```json
{
  "principalType": "user",
  "principalId": "user-456",
  "permission": "read"
}
```

**Permission Values:**
- `read` - View dataset
- `write` - Modify dataset
- `admin` - Full control

### Remove Grant
```
DELETE /api/datasetrw/v1/datasets/{datasetId}/grants
```

**Request Body:**
```json
{
  "principalType": "user",
  "principalId": "user-456"
}
```

---

## Python SDK Examples

### Create and Manage Dataset
```python
from domino import Domino

domino = Domino("owner/project-name")

# Create dataset
dataset = domino.datasets_create(
    name="model-training-data",
    description="Preprocessed training data"
)
print(f"Created: {dataset['id']}")

# List datasets
datasets = domino.datasets_list()
for ds in datasets:
    print(f"  {ds['name']}: {ds['id']}")
```

### Create Snapshot
```python
# Create snapshot with tag
snapshot = domino.datasets_snapshot(
    dataset_name="model-training-data",
    tag="v1.0"
)
print(f"Snapshot: {snapshot['id']}")
```

---

## Working with Dataset Data

### Upload Data (In Workspace/Job)
```python
import pandas as pd

# Write to dataset mount path
df = pd.DataFrame({"col1": [1, 2, 3], "col2": ["a", "b", "c"]})
df.to_parquet("/mnt/data/my-dataset/data.parquet")
```

### Read Data
```python
import pandas as pd

# Read from dataset
df = pd.read_parquet("/mnt/data/my-dataset/data.parquet")
```

### Access Specific Snapshot
```python
# Access tagged snapshot
df = pd.read_parquet("/mnt/data/my-dataset@v1.0/data.parquet")

# Access by snapshot ID
df = pd.read_parquet("/mnt/data/my-dataset@snapshot-789/data.parquet")
```

---

## Dataset Workflow Example

```python
import requests
import pandas as pd

# Create dataset
response = requests.post(
    f"{base_url}/api/datasetrw/v1/datasets",
    headers=headers,
    json={
        "name": "feature-store",
        "description": "Centralized feature storage",
        "projectId": project_id
    }
)
dataset = response.json()
dataset_id = dataset['id']

# After uploading data, create snapshot
response = requests.post(
    f"{base_url}/api/datasetrw/v1/datasets/{dataset_id}/snapshots",
    headers=headers,
    json={"tag": "baseline"}
)

# Grant access to another user
response = requests.post(
    f"{base_url}/api/datasetrw/v1/datasets/{dataset_id}/grants",
    headers=headers,
    json={
        "principalType": "user",
        "principalId": "data-scientist-user-id",
        "permission": "read"
    }
)

print(f"Dataset ready: {dataset_id}")
```



### Api Environments

# Domino Environments API

## Overview
The Environments API allows you to create, manage, and version Domino Compute Environments programmatically.

## Authentication
```python
import requests

headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
base_url = "https://your-domino.com"
```

---

## Endpoints

### List Environments
```
GET /api/environments/beta/environments
```

Get environments visible to the user.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `offset` | int | Pagination offset |
| `limit` | int | Results per page |
| `name` | string | Filter by name |

**Example:**
```python
response = requests.get(
    f"{base_url}/api/environments/beta/environments",
    headers=headers,
    params={"limit": 50}
)
environments = response.json()

for env in environments['data']:
    print(f"{env['name']}: {env['id']}")
```

**Response:**
```json
{
  "data": [
    {
      "id": "env-123",
      "name": "Domino Standard Environment",
      "description": "Default environment with Python and R",
      "visibility": "Global",
      "latestRevisionId": "rev-456",
      "createdAt": "2024-01-01T00:00:00Z"
    }
  ],
  "offset": 0,
  "limit": 50,
  "totalCount": 10
}
```

---

### Create Environment
```
POST /api/environments/beta/environments
```

Create a new custom environment.

**Request Body:**
```json
{
  "name": "custom-ml-env",
  "description": "Custom ML environment with TensorFlow",
  "visibility": "Private",
  "baseEnvironmentId": "env-123"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/environments/beta/environments",
    headers=headers,
    json={
        "name": "pytorch-gpu-env",
        "description": "PyTorch environment with GPU support",
        "visibility": "Private",
        "baseEnvironmentId": "base-env-id"
    }
)
environment = response.json()
print(f"Created environment: {environment['id']}")
```

---

### Get Environment
```
GET /api/environments/v1/environments/{environmentId}
```

Get detailed information about an environment.

**Example:**
```python
env_id = "env-123"
response = requests.get(
    f"{base_url}/api/environments/v1/environments/{env_id}",
    headers=headers
)
environment = response.json()
```

**Response:**
```json
{
  "id": "env-123",
  "name": "custom-ml-env",
  "description": "Custom ML environment",
  "visibility": "Private",
  "latestRevision": {
    "id": "rev-789",
    "number": 3,
    "status": "Succeeded",
    "dockerImage": "docker.domino.tech/env-123:rev-789"
  },
  "dockerfileInstructions": "RUN pip install tensorflow==2.13.0"
}
```

---

### Archive Environment
```
DELETE /api/environments/v1/environments/{environmentId}
```

Archive an environment (soft delete).

**Example:**
```python
response = requests.delete(
    f"{base_url}/api/environments/v1/environments/{env_id}",
    headers=headers
)
```

---

## Environment Revisions

### Create Revision
```
POST /api/environments/beta/environments/{environmentId}/revisions
```

Create a new revision with updated Dockerfile instructions.

**Request Body:**
```json
{
  "dockerfileInstructions": "RUN pip install pandas==2.0.0 numpy scikit-learn"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/environments/beta/environments/{env_id}/revisions",
    headers=headers,
    json={
        "dockerfileInstructions": """
RUN pip install --no-cache-dir \\
    pandas==2.0.0 \\
    numpy>=1.24.0 \\
    scikit-learn==1.3.0 \\
    tensorflow==2.13.0
"""
    }
)
revision = response.json()
print(f"Created revision: {revision['id']}")
```

---

### Update Revision Restriction
```
PATCH /api/environments/beta/environments/{environmentId}/revisions/{revisionId}
```

Update revision settings (e.g., restrict usage).

**Request Body:**
```json
{
  "restricted": true
}
```

---

## Python SDK Examples

### List Environments
```python
from domino import Domino

domino = Domino("owner/project-name")

# List all environments
environments = domino.environments_list()
for env in environments:
    print(f"{env['name']}: {env['id']}")
```

### Get Environment Details
```python
env = domino.environment_get("env-123")
print(f"Name: {env['name']}")
print(f"Latest Revision: {env['latestRevision']['number']}")
```

---

## Dockerfile Instructions

When creating or updating environments, use proper Dockerfile syntax:

### Install Python Packages
```dockerfile
RUN pip install --no-cache-dir \
    pandas==2.0.0 \
    numpy>=1.24.0 \
    scikit-learn==1.3.0
```

### Install System Packages
```dockerfile
RUN apt-get update && apt-get install -y \
    libpq-dev \
    graphviz \
    && rm -rf /var/lib/apt/lists/*
```

### Install R Packages
```dockerfile
RUN R -e "install.packages(c('tidyverse', 'caret'), repos='https://cloud.r-project.org')"
```

### Set Environment Variables
```dockerfile
ENV MODEL_PATH=/mnt/artifacts/model.pkl
ENV PYTHONPATH=/opt/custom:$PYTHONPATH
```

### GPU Libraries
```dockerfile
RUN pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

---

## Environment Workflow

```python
# 1. Create new environment
response = requests.post(
    f"{base_url}/api/environments/beta/environments",
    headers=headers,
    json={
        "name": "ml-training-env",
        "description": "Environment for ML model training",
        "visibility": "Private",
        "baseEnvironmentId": "domino-standard-env-id"
    }
)
env = response.json()
env_id = env['id']

# 2. Add Dockerfile instructions via revision
response = requests.post(
    f"{base_url}/api/environments/beta/environments/{env_id}/revisions",
    headers=headers,
    json={
        "dockerfileInstructions": """
RUN pip install --no-cache-dir \\
    xgboost==2.0.0 \\
    lightgbm==4.1.0 \\
    catboost==1.2.0 \\
    optuna==3.4.0
"""
    }
)
revision = response.json()

# 3. Wait for build to complete
# Check revision status periodically
import time
while True:
    env_details = requests.get(
        f"{base_url}/api/environments/v1/environments/{env_id}",
        headers=headers
    ).json()

    status = env_details['latestRevision']['status']
    if status == 'Succeeded':
        print("Environment build complete!")
        break
    elif status == 'Failed':
        print("Environment build failed!")
        break
    else:
        print(f"Building... Status: {status}")
        time.sleep(30)

# 4. Use environment in job
response = requests.post(
    f"{base_url}/api/jobs/v1/jobs",
    headers=headers,
    json={
        "projectId": project_id,
        "commandToRun": "python train.py",
        "environmentId": env_id,
        "hardwareTierId": "medium"
    }
)
```

---

## Best Practices

1. **Base on Standard Environments**: Start from Domino Standard Environments
2. **Pin Versions**: Always specify exact package versions
3. **Combine RUN Commands**: Reduce layers by combining installations
4. **Clean Up**: Remove cache files to reduce image size
5. **Test Locally**: Verify Dockerfile syntax before creating revisions



### Api Jobs

# Domino Jobs API

## Overview
The Jobs API allows you to start, monitor, and manage batch job executions in Domino.

## Authentication
```python
import requests

headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
base_url = "https://your-domino.com"
```

---

## Endpoints

### List Jobs
```
GET /api/jobs/beta/jobs
```

Get jobs for a project.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `projectId` | string | **Required** - Filter by project |
| `offset` | int | Pagination offset |
| `limit` | int | Results per page |
| `status` | string | Filter by status |

**Status Values:**
- `Pending`
- `Running`
- `Succeeded`
- `Failed`
- `Stopped`

**Example:**
```python
response = requests.get(
    f"{base_url}/api/jobs/beta/jobs",
    headers=headers,
    params={
        "projectId": "project-123",
        "status": "Running",
        "limit": 50
    }
)
jobs = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "id": "job-456",
      "projectId": "project-123",
      "status": "Running",
      "command": "python train.py",
      "startedAt": "2024-01-15T10:00:00Z",
      "hardwareTierId": "medium",
      "environmentId": "env-789"
    }
  ],
  "offset": 0,
  "limit": 50,
  "totalCount": 1
}
```

---

### Get Job Details
```
GET /api/jobs/beta/jobs/{jobId}
```

Get detailed information about a specific job.

**Example:**
```python
job_id = "job-456"
response = requests.get(
    f"{base_url}/api/jobs/beta/jobs/{job_id}",
    headers=headers
)
job = response.json()

print(f"Status: {job['status']}")
print(f"Started: {job['startedAt']}")
print(f"Command: {job['command']}")
```

**Response:**
```json
{
  "id": "job-456",
  "projectId": "project-123",
  "status": "Succeeded",
  "command": "python train.py --epochs 100",
  "hardwareTierId": "gpu-small",
  "environmentId": "env-789",
  "startedAt": "2024-01-15T10:00:00Z",
  "endedAt": "2024-01-15T12:30:00Z",
  "commitId": "abc123def456",
  "outputCommitId": "def456abc789"
}
```

---

### Get Job Logs
```
GET /api/jobs/beta/jobs/{jobId}/logs
```

Retrieve execution logs for a job.

**Example:**
```python
job_id = "job-456"
response = requests.get(
    f"{base_url}/api/jobs/beta/jobs/{job_id}/logs",
    headers=headers
)
logs = response.text
print(logs)
```

---

### Start Job
```
POST /api/jobs/v1/jobs
```

Start a new job execution.

**Request Body:**
```json
{
  "projectId": "project-123",
  "commandToRun": "python train.py --epochs 100",
  "hardwareTierId": "gpu-small",
  "environmentId": "env-789",
  "commitId": "abc123",
  "title": "Training Run",
  "isDirectHardwareTierId": false
}
```

**Parameters:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `projectId` | string | Yes | Project to run in |
| `commandToRun` | string | Yes | Command to execute |
| `hardwareTierId` | string | Yes | Hardware tier ID or name |
| `environmentId` | string | No | Environment ID |
| `commitId` | string | No | Git commit to use |
| `title` | string | No | Job title |

**Example:**
```python
response = requests.post(
    f"{base_url}/api/jobs/v1/jobs",
    headers=headers,
    json={
        "projectId": "project-123",
        "commandToRun": "python train.py --epochs 100 --lr 0.001",
        "hardwareTierId": "gpu-small",
        "environmentId": "env-789",
        "title": "Hyperparameter Experiment"
    }
)
job = response.json()
print(f"Started job: {job['id']}")
```

**Response:**
```json
{
  "id": "job-789",
  "status": "Pending",
  "projectId": "project-123",
  "command": "python train.py --epochs 100 --lr 0.001"
}
```

---

### Stop Job
To stop a running job, use the python-domino library:

```python
from domino import Domino

domino = Domino("owner/project")
domino.runs_stop(run_id="job-789")
```

---

## Job Tags

### Add Tag to Job
```
POST /api/jobs/v1/jobs/{jobId}/tags
```

**Request Body:**
```json
{
  "name": "production"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/jobs/v1/jobs/{job_id}/tags",
    headers=headers,
    json={"name": "best-model"}
)
```

### Remove Tag from Job
```
DELETE /api/jobs/v1/jobs/{jobId}/tags/{tagId}
```

---

## Job Goals

### List Linked Goals
```
GET /api/jobs/v1/goals
```

Get goals linked to jobs.

### Link Goal to Job
```
POST /api/jobs/v1/goals
```

**Request Body:**
```json
{
  "jobId": "job-456",
  "goalId": "goal-123"
}
```

### Unlink Goal
```
DELETE /api/jobs/v1/goals/{goalId}
```

---

## Python SDK Examples

### Start and Monitor Job
```python
from domino import Domino

domino = Domino("owner/project-name")

# Start a job
run = domino.runs_start(
    command="python train.py --epochs 100",
    hardware_tier_name="gpu-small",
    environment_id="env-789"
)
print(f"Started run: {run['runId']}")

# Check status
status = domino.runs_status(run['runId'])
print(f"Status: {status['status']}")

# Wait for completion
result = domino.runs_wait(run['runId'])
print(f"Final status: {result['status']}")

# Get logs
logs = domino.runs_get_logs(run['runId'])
print(logs)
```

### Run Multiple Jobs
```python
from domino import Domino

domino = Domino("owner/project-name")

# Parameter sweep
learning_rates = [0.01, 0.001, 0.0001]
jobs = []

for lr in learning_rates:
    run = domino.runs_start(
        command=f"python train.py --lr {lr}",
        hardware_tier_name="gpu-small"
    )
    jobs.append(run['runId'])
    print(f"Started job for lr={lr}: {run['runId']}")

# Wait for all jobs
for job_id in jobs:
    result = domino.runs_wait(job_id)
    print(f"Job {job_id}: {result['status']}")
```

### Start Job with Specific Commit
```python
run = domino.runs_start(
    command="python train.py",
    hardware_tier_name="medium",
    commit_id="abc123def456"  # Use specific code version
)
```

---

## Polling for Job Completion

```python
import time

def wait_for_job(job_id, timeout=3600, poll_interval=30):
    """Wait for job to complete with timeout."""
    start_time = time.time()

    while time.time() - start_time < timeout:
        response = requests.get(
            f"{base_url}/api/jobs/beta/jobs/{job_id}",
            headers=headers
        )
        job = response.json()
        status = job['status']

        if status in ['Succeeded', 'Failed', 'Stopped']:
            return job

        print(f"Job {job_id}: {status}")
        time.sleep(poll_interval)

    raise TimeoutError(f"Job {job_id} did not complete within {timeout}s")

# Usage
job = wait_for_job("job-456")
print(f"Job completed: {job['status']}")
```



### Api Models

# Domino Models API

## Overview
The Models API covers Model APIs (deployed endpoints), Model Deployments, and the Model Registry.

## Authentication
```python
import requests

headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
base_url = "https://your-domino.com"
```

---

## Model APIs (Deployed Endpoints)

### List Model APIs
```
GET /api/modelServing/v1/modelApis
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `projectId` | string | Filter by project |
| `offset` | int | Pagination offset |
| `limit` | int | Results per page |

**Example:**
```python
response = requests.get(
    f"{base_url}/api/modelServing/v1/modelApis",
    headers=headers,
    params={"projectId": "project-123"}
)
models = response.json()
```

---

### Create Model API
```
POST /api/modelServing/v1/modelApis
```

Deploy a model as an API endpoint.

**Request Body:**
```json
{
  "projectId": "project-123",
  "name": "fraud-detector",
  "description": "Fraud detection model",
  "modelFile": "model.py",
  "modelFunction": "predict",
  "environmentId": "env-789",
  "hardwareTierId": "small"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/modelServing/v1/modelApis",
    headers=headers,
    json={
        "projectId": "project-123",
        "name": "customer-churn",
        "description": "Predicts customer churn probability",
        "modelFile": "serve.py",
        "modelFunction": "predict",
        "environmentId": "env-789",
        "hardwareTierId": "small"
    }
)
model_api = response.json()
print(f"Model API ID: {model_api['id']}")
```

---

### Get Model API
```
GET /api/modelServing/v1/modelApis/{modelApiId}
```

**Response:**
```json
{
  "id": "model-api-456",
  "name": "fraud-detector",
  "status": "Running",
  "url": "https://your-domino.com/models/model-api-456/latest/model",
  "projectId": "project-123",
  "createdAt": "2024-01-15T10:00:00Z"
}
```

---

### Update Model API
```
PUT /api/modelServing/v1/modelApis/{modelApiId}
```

---

### Delete Model API
```
DELETE /api/modelServing/v1/modelApis/{modelApiId}
```

---

## Model API Versions

### List Versions
```
GET /api/modelServing/v1/modelApis/{modelApiId}/versions
```

### Create New Version
```
POST /api/modelServing/v1/modelApis/{modelApiId}/versions
```

**Request Body:**
```json
{
  "modelFile": "model_v2.py",
  "modelFunction": "predict",
  "environmentId": "env-789"
}
```

### Get Version Details
```
GET /api/modelServing/v1/modelApis/{modelApiId}/versions/{versionId}
```

---

## Model API Logs

### Build Logs
```
GET /api/modelServing/v1/modelApis/{modelApiId}/versions/{versionId}/buildLogs
```

### Export Logs
```
GET /api/modelServing/v1/modelApis/{modelApiId}/versions/{versionId}/exportLogs
```

### Instance Logs
```
GET /api/modelServing/v1/modelApis/{modelApiId}/versions/{versionId}/instanceLogs
```

---

## Model Deployments

### List Deployments
```
GET /api/modelServing/v1/modelDeployments
```

### Create Deployment
```
POST /api/modelServing/v1/modelDeployments
```

**Request Body:**
```json
{
  "name": "production-deployment",
  "modelVersionId": "version-123",
  "hardwareTierId": "medium",
  "replicas": 2
}
```

### Get Deployment
```
GET /api/modelServing/v1/modelDeployments/{deploymentId}
```

### Update Deployment
```
PATCH /api/modelServing/v1/modelDeployments/{deploymentId}
```

### Delete Deployment
```
DELETE /api/modelServing/v1/modelDeployments/{deploymentId}
```

### Start Deployment
```
POST /api/modelServing/v1/modelDeployments/{deploymentId}/start
```

### Stop Deployment
```
POST /api/modelServing/v1/modelDeployments/{deploymentId}/stop
```

### Get Deployment Logs
```
GET /api/modelServing/v1/modelDeployments/{deploymentId}/logs/{logSuffix}
```

### Get Deployment Credentials
```
GET /api/modelServing/v1/modelDeployments/{deploymentId}/credentials
```

---

## Registered Models (Model Registry)

### List Registered Models
```
GET /api/registeredmodels/v2
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `offset` | int | Pagination offset |
| `limit` | int | Results per page |
| `name` | string | Filter by name |

### Register Model
```
POST /api/registeredmodels/v2
```

**Request Body:**
```json
{
  "name": "fraud-classifier",
  "description": "Random forest fraud classifier",
  "source": {
    "type": "experiment",
    "experimentId": "exp-123",
    "runId": "run-456"
  }
}
```

### Get Registered Model
```
GET /api/registeredmodels/v1/{modelName}
```

### Update Registered Model
```
PATCH /api/registeredmodels/v1/{modelName}
```

---

## Model Versions

### List Model Versions
```
GET /api/registeredmodels/v1/{modelName}/versions
```

### Create Model Version
```
POST /api/registeredmodels/v1/{modelName}/versions
```

### Get Model Version
```
GET /api/registeredmodels/v1/{modelName}/versions/{version}
```

### Get Model APIs for Version
```
GET /api/registeredmodels/v1/{modelName}/versions/{version}/modelapis
```

Returns list of Model APIs deployed from this version.

---

## Calling Model APIs

### Synchronous Request
```python
import requests

model_url = "https://your-domino.com/models/model-api-456/latest/model"

response = requests.post(
    model_url,
    auth=("MODEL_ACCESS_TOKEN", "MODEL_ACCESS_TOKEN"),
    json={"data": {"features": [1.0, 2.0, 3.0, 4.0]}}
)

prediction = response.json()
print(f"Prediction: {prediction['result']}")
```

### Asynchronous Request
```python
# Submit async request
response = requests.post(
    f"{base_url}/api/modelApis/async/v1/{model_api_id}",
    headers={"Authorization": f"Bearer {model_access_token}"},
    json={"parameters": {"input_file": "s3://bucket/data.csv"}}
)
prediction_id = response.json()["predictionId"]

# Poll for results
import time
while True:
    status = requests.get(
        f"{base_url}/api/modelApis/async/v1/{model_api_id}/{prediction_id}",
        headers={"Authorization": f"Bearer {model_access_token}"}
    ).json()

    if status["status"] == "COMPLETED":
        print(f"Result: {status['result']}")
        break
    elif status["status"] == "FAILED":
        print(f"Error: {status['error']}")
        break
    time.sleep(5)
```

---

## Python SDK Examples

### Deploy Model
```python
from domino import Domino

domino = Domino("owner/project-name")

# Publish model API
model = domino.model_publish(
    file="model.py",
    function="predict",
    environment_id="env-789",
    name="my-classifier",
    description="Classification model"
)
print(f"Model ID: {model['id']}")
print(f"Model URL: {model['url']}")
```

### List Models
```python
models = domino.models_list()
for m in models:
    print(f"{m['name']}: {m['status']}")
```

---

## Complete Workflow

```python
# 1. Train model in job
run = domino.runs_start(command="python train.py")
domino.runs_wait(run['runId'])

# 2. Register model (if using MLflow)
# Model automatically registered during training

# 3. Deploy as API
model_api = requests.post(
    f"{base_url}/api/modelServing/v1/modelApis",
    headers=headers,
    json={
        "projectId": project_id,
        "name": "production-model",
        "modelFile": "serve.py",
        "modelFunction": "predict",
        "environmentId": env_id,
        "hardwareTierId": "medium"
    }
).json()

# 4. Test endpoint
test_response = requests.post(
    model_api['url'],
    auth=(access_token, access_token),
    json={"data": {"features": [1, 2, 3]}}
)
print(f"Test prediction: {test_response.json()}")
```



### Api Projects

# Domino Projects API

## Overview
The Projects API allows you to create, manage, and configure Domino projects programmatically.

## Authentication
```python
import requests

headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
base_url = "https://your-domino.com"
```

---

## Endpoints

### List Projects
```
GET /api/projects/beta/projects
```

Get projects visible to the authenticated user.

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `offset` | int | Pagination offset (default: 0) |
| `limit` | int | Results per page (default: 10) |
| `name` | string | Filter by project name |
| `ownerId` | string | Filter by owner ID |

**Example:**
```python
response = requests.get(
    f"{base_url}/api/projects/beta/projects",
    headers=headers,
    params={"limit": 20, "name": "ml-project"}
)
projects = response.json()
```

**Response:**
```json
{
  "data": [
    {
      "id": "project-123",
      "name": "ml-project",
      "description": "Machine learning project",
      "ownerId": "user-456",
      "visibility": "Private",
      "createdAt": "2024-01-15T10:00:00Z"
    }
  ],
  "offset": 0,
  "limit": 20,
  "totalCount": 1
}
```

---

### Create Project
```
POST /api/projects/beta/projects
```

Create a new project.

**Request Body:**
```json
{
  "name": "my-new-project",
  "description": "Project description",
  "visibility": "Private",
  "ownerId": "user-id"
}
```

**Example:**
```python
response = requests.post(
    f"{base_url}/api/projects/beta/projects",
    headers=headers,
    json={
        "name": "fraud-detection",
        "description": "Fraud detection model",
        "visibility": "Private"
    }
)
project = response.json()
print(f"Created project: {project['id']}")
```

---

### Get Project by ID
```
GET /api/projects/v1/projects/{projectId}
```

**Example:**
```python
project_id = "project-123"
response = requests.get(
    f"{base_url}/api/projects/v1/projects/{project_id}",
    headers=headers
)
project = response.json()
```

---

### Archive Project
```
DELETE /api/projects/beta/projects/{projectId}
```

Archives a project (soft delete).

**Example:**
```python
project_id = "project-123"
response = requests.delete(
    f"{base_url}/api/projects/beta/projects/{project_id}",
    headers=headers
)
```

---

### Copy Project
```
POST /api/projects/v1/projects/{projectId}/copy-project
```

Create a copy of an existing project.

**Request Body:**
```json
{
  "name": "copied-project",
  "description": "Copy of original project"
}
```

---

### Update Project Status
```
PUT /api/projects/v1/projects/{projectId}/status
```

Update project status (active, complete, etc.).

---

## Collaborators

### Add Collaborator
```
POST /api/projects/v1/projects/{projectId}/collaborators
```

**Request Body:**
```json
{
  "userId": "user-id",
  "role": "Contributor"
}
```

**Roles:**
- `Owner`
- `Admin`
- `Contributor`
- `LauncherUser`
- `ResultsConsumer`

**Example:**
```python
response = requests.post(
    f"{base_url}/api/projects/v1/projects/{project_id}/collaborators",
    headers=headers,
    json={
        "userId": "user-789",
        "role": "Contributor"
    }
)
```

### Remove Collaborator
```
DELETE /api/projects/v1/projects/{projectId}/collaborators/{collaboratorId}
```

---

## Git Repositories

### List Repositories
```
GET /api/projects/v1/projects/{projectId}/repositories
```

Get all imported Git repositories in a project.

### Add Repository
```
POST /api/projects/v1/projects/{projectId}/repositories
```

**Request Body:**
```json
{
  "uri": "https://github.com/org/repo.git",
  "ref": "main",
  "credentialId": "cred-id"
}
```

### Remove Repository
```
DELETE /api/projects/v1/projects/{projectId}/repositories/{repositoryId}
```

---

## Project Goals

### List Goals
```
GET /api/projects/v1/projects/{projectId}/goals
```

### Add Goal
```
POST /api/projects/v1/projects/{projectId}/goals
```

**Request Body:**
```json
{
  "title": "Achieve 95% accuracy",
  "description": "Model should reach 95% test accuracy"
}
```

### Update Goal
```
PATCH /api/projects/v1/projects/{projectId}/goals/{goalId}
```

**Request Body:**
```json
{
  "status": "Complete"
}
```

### Delete Goal
```
DELETE /api/projects/v1/projects/{projectId}/goals/{goalId}
```

---

## Shared Datasets

### List Shared Datasets
```
GET /api/projects/v1/projects/{projectId}/shared-datasets
```

Get datasets shared with this project.

### Link Dataset
```
POST /api/projects/v1/projects/{projectId}/shared-datasets
```

**Request Body:**
```json
{
  "datasetId": "dataset-id"
}
```

### Unlink Dataset
```
DELETE /api/projects/v1/projects/{projectId}/shared-datasets/{datasetId}
```

---

## Project Files

### Get File Content
```
GET /api/projects/v1/projects/{projectId}/files/{commitId}/{path}/content
```

Returns the contents of a file at a specific commit.

**Example:**
```python
response = requests.get(
    f"{base_url}/api/projects/v1/projects/{project_id}/files/HEAD/train.py/content",
    headers=headers
)
file_content = response.text
```

---

## Result Settings

### Get Result Settings
```
GET /api/projects/beta/projects/{projectId}/results-settings
```

### Update Result Settings
```
PUT /api/projects/beta/projects/{projectId}/results-settings
```

---

## Python SDK Examples

```python
from domino import Domino

# Initialize client
domino = Domino("owner/project-name")

# Get project info
info = domino.project_info()
print(f"Project: {info['name']}")
print(f"ID: {info['id']}")

# Create project (v4 API)
domino = Domino()
project = domino.project_create(
    project_name="new-project",
    owner_name="username"
)
```



### Api Reference

# Domino REST API Reference

Complete reference for Domino Platform REST API endpoints.

## Authentication

All API calls require authentication via API key:

```bash
# Header authentication
curl -H "X-Domino-Api-Key: YOUR_API_KEY" \
  https://your-domino.com/api/projects/v1/projects/{projectId}

# Or via Python
import requests
headers = {"X-Domino-Api-Key": "YOUR_API_KEY"}
response = requests.get(url, headers=headers)
```

## Base URL
```
https://your-domino-instance.com
```

---

## Projects API

### List Projects
```
GET /api/projects/beta/projects
```
Get projects visible to user.

**Query Parameters:**
- `offset` (int): Pagination offset
- `limit` (int): Number of results
- `name` (string): Filter by name
- `ownerId` (string): Filter by owner

**Response:** Array of project objects

### Create Project
```
POST /api/projects/beta/projects
```
Create a new project.

**Request Body:**
```json
{
  "name": "my-project",
  "description": "Project description",
  "visibility": "Private",
  "ownerId": "user-id"
}
```

### Get Project
```
GET /api/projects/v1/projects/{projectId}
```

### Archive Project
```
DELETE /api/projects/beta/projects/{projectId}
```

### Copy Project
```
POST /api/projects/v1/projects/{projectId}/copy-project
```

### Manage Collaborators
```
POST /api/projects/v1/projects/{projectId}/collaborators
DELETE /api/projects/v1/projects/{projectId}/collaborators/{collaboratorId}
```

### Git Repositories
```
GET /api/projects/v1/projects/{projectId}/repositories
POST /api/projects/v1/projects/{projectId}/repositories
DELETE /api/projects/v1/projects/{projectId}/repositories/{repositoryId}
```

### Project Goals
```
GET /api/projects/v1/projects/{projectId}/goals
POST /api/projects/v1/projects/{projectId}/goals
PATCH /api/projects/v1/projects/{projectId}/goals/{goalId}
DELETE /api/projects/v1/projects/{projectId}/goals/{goalId}
```

### Shared Datasets
```
GET /api/projects/v1/projects/{projectId}/shared-datasets
POST /api/projects/v1/projects/{projectId}/shared-datasets
DELETE /api/projects/v1/projects/{projectId}/shared-datasets/{datasetId}
```

---

## Jobs API

### List Jobs
```
GET /api/jobs/beta/jobs
```
**Query Parameters:**
- `projectId` (string): Required - Filter by project
- `offset` (int): Pagination offset
- `limit` (int): Number of results

### Get Job Details
```
GET /api/jobs/beta/jobs/{jobId}
```

### Get Job Logs
```
GET /api/jobs/beta/jobs/{jobId}/logs
```

### Start Job
```
POST /api/jobs/v1/jobs
```
**Request Body:**
```json
{
  "projectId": "project-id",
  "commandToRun": "python train.py --epochs 100",
  "hardwareTierId": "small",
  "environmentId": "env-id",
  "commitId": "optional-commit-hash"
}
```

### Job Tags
```
POST /api/jobs/v1/jobs/{jobId}/tags
DELETE /api/jobs/v1/jobs/{jobId}/tags/{tagId}
```

### Job Goals
```
GET /api/jobs/v1/goals
POST /api/jobs/v1/goals
DELETE /api/jobs/v1/goals/{goalId}
```

---

## Workspaces API

### Create Workspace Session
```
POST /api/projects/v1/projects/{projectId}/workspaces/{workspaceId}/sessions
```
**Request Body:**
```json
{
  "hardwareTierId": "medium",
  "environmentId": "env-id",
  "workspaceType": "JupyterLab"
}
```

---

## Datasets API

### List Datasets
```
GET /api/datasetrw/v2/datasets
```
**Query Parameters:**
- `projectId` (string): Filter by project
- `offset` (int): Pagination offset
- `limit` (int): Number of results

### Create Dataset
```
POST /api/datasetrw/v1/datasets
```
**Request Body:**
```json
{
  "name": "training-data",
  "description": "Training dataset",
  "projectId": "project-id"
}
```

### Get Dataset
```
GET /api/datasetrw/v1/datasets/{datasetId}
```

### Update Dataset
```
PATCH /api/datasetrw/v1/datasets/{datasetId}
```

### Delete Dataset
```
DELETE /api/datasetrw/v1/datasets/{datasetId}
```

### Dataset Snapshots
```
GET /api/datasetrw/v1/datasets/{datasetId}/snapshots
POST /api/datasetrw/v1/datasets/{datasetId}/snapshots
GET /api/datasetrw/v1/snapshots/{snapshotId}
```

### Dataset Tags
```
POST /api/datasetrw/v1/datasets/{datasetId}/tags
DELETE /api/datasetrw/v1/datasets/{datasetId}/tags/{tagName}
```

### Dataset Grants (Permissions)
```
GET /api/datasetrw/v1/datasets/{datasetId}/grants
POST /api/datasetrw/v1/datasets/{datasetId}/grants
DELETE /api/datasetrw/v1/datasets/{datasetId}/grants
```

---

## Environments API

### List Environments
```
GET /api/environments/beta/environments
```

### Create Environment
```
POST /api/environments/beta/environments
```
**Request Body:**
```json
{
  "name": "my-environment",
  "description": "Custom environment",
  "baseEnvironmentId": "base-env-id"
}
```

### Get Environment
```
GET /api/environments/v1/environments/{environmentId}
```

### Archive Environment
```
DELETE /api/environments/v1/environments/{environmentId}
```

### Environment Revisions
```
POST /api/environments/beta/environments/{environmentId}/revisions
PATCH /api/environments/beta/environments/{environmentId}/revisions/{revisionId}
```

---

## Model APIs

### List Model APIs
```
GET /api/modelServing/v1/modelApis
```

### Create Model API
```
POST /api/modelServing/v1/modelApis
```
**Request Body:**
```json
{
  "projectId": "project-id",
  "name": "my-model-api",
  "description": "Prediction API",
  "modelFile": "model.py",
  "modelFunction": "predict",
  "environmentId": "env-id"
}
```

### Get Model API
```
GET /api/modelServing/v1/modelApis/{modelApiId}
```

### Update Model API
```
PUT /api/modelServing/v1/modelApis/{modelApiId}
```

### Delete Model API
```
DELETE /api/modelServing/v1/modelApis/{modelApiId}
```

### Model API Versions
```
GET /api/modelServing/v1/modelApis/{modelApiId}/versions
POST /api/modelServing/v1/modelApis/{modelApiId}/versions
GET /api/modelServing/v1/modelApis/{modelApiId}/versions/{versionId}
```

### Model API Logs
```
GET /api/modelServing/v1/modelApis/{modelApiId}/versions/{versionId}/buildLogs
GET /api/modelServing/v1/modelApis/{modelApiId}/versions/{versionId}/instanceLogs
```

---

## Model Deployments API

### List Deployments
```
GET /api/modelServing/v1/modelDeployments
```

### Create Deployment
```
POST /api/modelServing/v1/modelDeployments
```

### Get Deployment
```
GET /api/modelServing/v1/modelDeployments/{deploymentId}
```

### Update Deployment
```
PATCH /api/modelServing/v1/modelDeployments/{deploymentId}
```

### Delete Deployment
```
DELETE /api/modelServing/v1/modelDeployments/{deploymentId}
```

### Start/Stop Deployment
```
POST /api/modelServing/v1/modelDeployments/{deploymentId}/start
POST /api/modelServing/v1/modelDeployments/{deploymentId}/stop
```

### Deployment Logs
```
GET /api/modelServing/v1/modelDeployments/{deploymentId}/logs/{logSuffix}
```

### Deployment Credentials
```
GET /api/modelServing/v1/modelDeployments/{deploymentId}/credentials
```

---

## Registered Models API

### List Registered Models
```
GET /api/registeredmodels/v2
```

### Register Model
```
POST /api/registeredmodels/v2
```
**Request Body:**
```json
{
  "name": "my-model",
  "description": "Classification model",
  "source": {
    "type": "experiment",
    "experimentId": "exp-id",
    "runId": "run-id"
  }
}
```

### Get Model
```
GET /api/registeredmodels/v1/{modelName}
```

### Update Model
```
PATCH /api/registeredmodels/v1/{modelName}
```

### Model Versions
```
GET /api/registeredmodels/v1/{modelName}/versions
POST /api/registeredmodels/v1/{modelName}/versions
GET /api/registeredmodels/v1/{modelName}/versions/{version}
```

---

## Apps API

### List Apps
```
GET /api/apps/beta/apps
```
**Query Parameters:**
- `projectId` (string): Filter by project
- `status` (string): Filter by status
- `offset` (int): Pagination offset
- `limit` (int): Number of results

### Create App
```
POST /api/apps/beta/apps
```
**Request Body:**
```json
{
  "projectId": "project-id",
  "name": "my-app",
  "description": "Dashboard app",
  "hardwareTierId": "small",
  "environmentId": "env-id"
}
```

### Get App
```
GET /api/apps/beta/apps/{appId}
```

### Update App
```
PATCH /api/apps/beta/apps/{appId}
```

### Delete App
```
DELETE /api/apps/beta/apps/{appId}
```

### App Versions
```
GET /api/apps/beta/apps/{appId}/versions
POST /api/apps/beta/apps/{appId}/versions
GET /api/apps/beta/apps/{appId}/versions/{versionId}
PATCH /api/apps/beta/apps/{appId}/versions/{versionId}
```

### App Instances
```
GET /api/apps/beta/apps/{appId}/versions/{versionId}/instances
GET /api/apps/beta/apps/{appId}/versions/{versionId}/instances/{instanceId}
DELETE /api/apps/beta/apps/{appId}/versions/{versionId}/instances/{instanceId}
GET /api/apps/beta/apps/{appId}/versions/{versionId}/instances/{instanceId}/logs
```

### App Thumbnail
```
GET /api/apps/beta/apps/{appId}/thumbnail
POST /api/apps/beta/apps/{appId}/thumbnail
DELETE /api/apps/beta/apps/{appId}/thumbnail
```

---

## Hardware Tiers API

### List Hardware Tiers
```
GET /api/hardwaretiers/v1/hardwaretiers
```

### Create Hardware Tier
```
POST /api/hardwaretiers/v1/hardwaretiers
```

### Get Hardware Tier
```
GET /api/hardwaretiers/v1/hardwaretiers/{hardwareTierId}
```

### Update Hardware Tier
```
PUT /api/hardwaretiers/v1/hardwaretiers
```

### Archive Hardware Tier
```
DELETE /api/hardwaretiers/v1/hardwaretiers/{hardwareTierId}
```

---

## Data Sources API

### List Data Sources
```
GET /api/datasource/v1/datasources
```

### Create Data Source
```
POST /api/datasource/v1/datasources
```

### Get Data Source
```
GET /api/datasource/v1/datasources/{dataSourceId}
```

### Update Data Source
```
PATCH /api/datasource/v1/datasources/{dataSourceId}
```

### Delete Data Source
```
DELETE /api/datasource/v1/datasources/{dataSourceId}
```

### Data Source Audit
```
GET /api/datasource/v1/audit
```

---

## AI Gateway API

### List Endpoints
```
GET /api/aigateway/v1/endpoints
```

### Create Endpoint
```
POST /api/aigateway/v1/endpoints
```
**Request Body:**
```json
{
  "name": "openai-gpt4",
  "provider": "openai",
  "model": "gpt-4",
  "providerApiKey": "sk-..."
}
```

### Get Endpoint
```
GET /api/aigateway/v1/endpoints/{endpointName}
```

### Update Endpoint
```
PATCH /api/aigateway/v1/endpoints/{endpointName}
```

### Delete Endpoint
```
DELETE /api/aigateway/v1/endpoints/{endpointName}
```

### Endpoint Permissions
```
GET /api/aigateway/v1/endpoints/{endpointName}/permissions
PATCH /api/aigateway/v1/endpoints/{endpointName}/permissions
```

### AI Gateway Audit
```
GET /api/aigateway/v1/audit
```

---

## Users API

### Get Current User
```
GET /api/users/v1/self
```

### List Users
```
GET /api/users/v1/users
```

### User Git Credentials
```
GET /api/users/beta/credentials/{userId}
PUT /api/users/v1/user/{userId}/tokenCredentials/{credentialId}
```

---

## Organizations API

### List Organizations
```
GET /api/organizations/v1/organizations
```

### Create Organization
```
POST /api/organizations/v1/organizations
```

### Get Organization
```
GET /api/organizations/v1/organizations/{organizationId}
```

### Manage Members
```
PUT /api/organizations/v1/organizations/{organizationId}/user
DELETE /api/organizations/v1/organizations/{organizationId}/user
```

---

## Service Accounts API

### List Service Accounts
```
GET /api/serviceAccounts/v1/serviceAccounts
```

### Create Service Account
```
POST /api/serviceAccounts/v1/serviceAccounts
```

### Manage Tokens
```
GET /api/serviceAccounts/v1/serviceAccounts/{serviceAccountId}/tokens
POST /api/serviceAccounts/v1/serviceAccounts/{serviceAccountId}/tokens
```

---

## Cost API

### Cost Allocation
```
GET /api/cost/v1/allocation
GET /api/cost/v1/allocation/summary
```
**Query Parameters:**
- `startTime` (string): ISO 8601 timestamp
- `endTime` (string): ISO 8601 timestamp
- `aggregateBy` (string): user, project, organization

### Asset Costs
```
GET /api/cost/v1/asset
```

### Billing Tags
```
GET /api/cost/v1/billingtags
POST /api/cost/v1/billingtags
```

### Billing Settings
```
GET /api/cost/v1/billingtagSettings
PUT /api/cost/v1/billingtagSettings
GET /api/cost/v1/billingtagSettings/mode
PUT /api/cost/v1/billingtagSettings/mode
```

---

## Project Files API

### Get File Content
```
GET /api/projects/v1/projects/{projectId}/files/{commitId}/{path}/content
```

---

## Deployment Targets API (Admin)

### List Deployment Target Types
```
GET /api/admin/v1/deploymentTargetTypes
GET /api/admin/v1/deploymentTargetTypes/{typeId}
```

### Deployment Targets
```
GET /api/admin/v1/deploymentTargets
POST /api/admin/v1/deploymentTargets
GET /api/admin/v1/deploymentTargets/{targetId}
PATCH /api/admin/v1/deploymentTargets/{targetId}
DELETE /api/admin/v1/deploymentTargets/{targetId}
```

### Resource Configurations
```
GET /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations
POST /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations
GET /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations/{configId}
PATCH /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations/{configId}
DELETE /api/admin/v1/deploymentTargets/{targetId}/resourceConfigurations/{configId}
```

---

## Audit Events API

### Get Audit Events
```
GET /auditevents
```
**Query Parameters:**
- `startTime` (string): Filter start
- `endTime` (string): Filter end
- `eventType` (string): Filter by type

---

## Common Response Codes

| Code | Description |
|------|-------------|
| 200 | Success |
| 201 | Created |
| 204 | No Content |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 409 | Conflict |
| 500 | Internal Server Error |

## Pagination

Most list endpoints support pagination:
```json
{
  "offset": 0,
  "limit": 10,
  "totalCount": 100,
  "data": [...]
}
```

## Documentation Reference
- [REST API Reference](https://docs.dominodatalab.com/en/latest/api_guide/8c929e/domino-platform-api-reference/)
- [API Guide](https://docs.dominodatalab.com/en/latest/api_guide/f35c19/api-guide/)

