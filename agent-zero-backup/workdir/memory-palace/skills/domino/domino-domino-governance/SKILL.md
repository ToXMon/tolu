---
name: domino-domino-governance
description: Manage model risk governance in Domino using policies, bundles, and evidence.
  Covers creating governance bundles, attaching model artifacts and MLflow results
  as evidence, progressing through policy stages, and documenting findings. Use when
  the user mentions governance, compliance, bundles, policies, model risk management,
  SR 11-7, NIST AI RMF, or audit trails.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- governance
- compliance
- catalog
trigger_patterns:
- domino governance
- domino catalog
- domino compliance
---

# Domino Governance Skill

This skill provides knowledge for managing model risk governance in Domino Data Lab using the Governance API.

## Configuration

```bash
API_KEY="$DOMINO_USER_API_KEY"
BASE="${DOMINO_GOVERNANCE_HOST:-$DOMINO_API_HOST}/api/governance/v1"
```

Some deployments expose governance on a different host than the internal API. If so, set `DOMINO_GOVERNANCE_HOST` to override the base URL. Check `domino_project_settings.md` for project-specific overrides.

## Key Concepts

### Policy (Template)
A **policy** is a reusable governance template that defines the stages, evidence requirements, and approval gates a model must pass through. Examples: SR 11-7, NIST AI RMF, internal model risk frameworks. Policies are created by administrators in the Domino UI.

### Bundle (Living Document)
A **bundle** is the compliance document for a *specific model* in a *specific project*. It follows a policy and accumulates evidence as the model progresses through development, validation, and approval. One project can have multiple bundles (e.g., one per model version).

### Evidence (Proof)
Evidence comes in two forms:
1. **Attachments** — Files, model versions, and reports attached to the bundle (visible in the "Attachments" tab)
2. **EvidenceSet answers** — Responses to policy-defined form questions (visible in the "Evidence" tab for each stage)

### Finding (Issue)
A **finding** documents a problem, risk, or concern discovered during review. Findings have severity levels and are tracked as part of the audit trail.

## Related Documentation

- [BUNDLE-LIFECYCLE.md](./BUNDLE-LIFECYCLE.md) - Stage sequences, creating bundles, progressing stages
- [EVIDENCE-WORKFLOW.md](./EVIDENCE-WORKFLOW.md) - Attachment types, evidence submission, findings

## Governance API Reference

All endpoints are under `$BASE` (`/api/governance/v1`). Authenticate with `X-Domino-Api-Key: $API_KEY`.

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/policy-overviews` | GET | List available policy templates |
| `/bundles` | POST | Create a new governance bundle |
| `/bundles/{bundleId}` | GET | Inspect bundle: stages, attachments, status |
| `/bundles` | GET | List all bundles (filter by `projectId`) |
| `/bundles/{bundleId}/attachments` | POST | Attach evidence (model versions, reports) |
| `/rpc/submit-result-to-policy` | POST | Answer policy evidence questions |
| `/bundles/{bundleId}/stages/{stageId}` | PATCH | Update stage status (In Progress, Complete) |
| `/policies/{policyId}` | GET | Get full policy with evidenceSet IDs |
| `/findings` | POST | Create a finding (issue) during review |

## Standard 8-Step Governance Workflow

Follow these steps when setting up governance for a model:

### Step 1: Discover Policies
```bash
curl -s "$BASE/policy-overviews" \
  -H "X-Domino-Api-Key: $API_KEY"
```
Review available templates. Note the `id` of the policy you want to use.

### Step 2: Get the Project ID
The project ID is needed to create a bundle. Use the `DOMINO_PROJECT_ID` environment variable (available inside Domino) or look it up via the gateway API.

### Step 3: Create a Bundle
```bash
curl -X POST "$BASE/bundles" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "your-project-id",
    "name": "My Model v1.0",
    "description": "Description of the model being governed",
    "policyId": "policy-uuid"
  }'
```
Save the returned `id` as your `BUNDLE_ID`.

### Step 4: Inspect the Bundle
```bash
curl -s "$BASE/bundles/$BUNDLE_ID" \
  -H "X-Domino-Api-Key: $API_KEY"
```
This reveals the policy's stage structure, attachments, and approval status. **Note**: This does NOT return evidenceSet IDs — see Step 6 for how to discover those.

### Step 5: Attach Evidence
See [EVIDENCE-WORKFLOW.md](./EVIDENCE-WORKFLOW.md) for full details. Two attachment types are supported:

```bash
# Attach a registered model version
curl -X POST "$BASE/bundles/$BUNDLE_ID/attachments" \
  -H "X-Domino-Api-Key: $API_KEY" -H "Content-Type: application/json" \
  -d '{"type":"ModelVersion","identifier":{"name":"model-name","version":5},"name":"Display Name"}'

# Attach a project file (notebook, report, etc.)
curl -X POST "$BASE/bundles/$BUNDLE_ID/attachments" \
  -H "X-Domino-Api-Key: $API_KEY" -H "Content-Type: application/json" \
  -d '{"type":"Report","identifier":{"branch":"main","commit":"abc...","source":"git","filename":"path/to/file"},"name":"Display Name"}'
```

### Step 6: Answer Evidence Questions (EvidenceSet)

Evidence questions are the interactive forms shown in the Domino UI under each stage's "Evidence" tab. They are defined in the policy YAML as `evidenceSet` items.

#### 6a. Discover EvidenceSet IDs

EvidenceSet IDs are NOT in the bundle response. Fetch them from the **policy** endpoint:

```bash
curl -s "$BASE/policies/$POLICY_ID" \
  -H "X-Domino-Api-Key: $API_KEY"
```

The response contains `stages[]` → `evidenceSet[]` → `artifacts[]` with full UUIDs for each evidence item and artifact.

#### 6b. Submit Answers

```bash
curl -X POST "$BASE/rpc/submit-result-to-policy" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "bundleId": "bundle-uuid",
    "policyId": "policy-uuid",
    "evidenceId": "evidence-uuid",
    "content": {
      "artifact-uuid": "value"
    }
  }'
```

**Key details**:
- Use `policyId` (NOT `policyVersionId`)
- `evidenceId` is the evidence set item UUID (from policy response)
- `content` is a map of `{artifactId: value}`
- For **radio/textinput/textarea/select**: value is a string
- For **checkbox/multiSelect**: value is an array of strings
- Submit one artifact at a time per call, or multiple artifacts in the same evidence item together

### Step 7: Progress Stages
As evidence is collected and approvals obtained:
```bash
curl -X PATCH "$BASE/bundles/$BUNDLE_ID/stages/$STAGE_ID" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "Complete"}'
```

### Step 8: Document Findings (if any)
```bash
curl -X POST "$BASE/findings" \
  -H "X-Domino-Api-Key: $API_KEY" -H "Content-Type: application/json" \
  -d '{
    "bundleId": "bundle-uuid",
    "policyVersionId": "policy-version-uuid",
    "name": "Finding title",
    "title": "Finding title",
    "description": "Detailed description...",
    "severity": "High",
    "approver": {"id": "org-uuid", "name": "model-gov-org"},
    "assignee": {"id": "user-uuid", "name": "username"}
  }'
```
Get the `policyVersionId` and user/org IDs from the bundle response (Step 4).

## Viewing in Domino UI

After creating a bundle and attaching evidence, the bundle is visible in the Domino UI:
**Project** > **Govern** > **Bundles** > click the bundle name

The UI shows:
- **Overview** — Stage progression and classification
- **Evidence** tab (per stage) — Interactive forms for evidenceSet questions
- **Attachments** tab — Files, model versions, and reports
- **Findings** tab — Documented issues with severity


---

## Reference Documentation


### Bundle Lifecycle

# Bundle Lifecycle

This document explains how governance bundles progress through policy stages in Domino.

## How Policies Define Stage Sequences

A policy template defines an ordered sequence of stages that a model must pass through. A typical MRM policy might use stages like:

```
Model Initiation → Development → Validation & Testing → Deployment Approval → Ongoing Monitoring → Decommission
```

Each stage has:
- **Stage ID**: A UUID (discovered via `GET /bundles/{bundleId}` → `stages[]`)
- **Name**: Human-readable label
- **Approvals**: Organizations that must sign off before the stage can advance
- **EvidenceSet**: Form-based questions to be answered (discovered via `GET /policies/{policyId}`)
- **Attachments**: Files, model versions, and reports linked to the bundle

### Stage Gating

Policies with `enforceSequentialOrder: true` require stages to be completed in order. A stage typically requires:
1. All evidence questions answered
2. Approval from the designated organization(s)

## Creating a Bundle

### Prerequisites
1. **Project ID**: Available as `DOMINO_PROJECT_ID` env var inside Domino, or from the bundle creation response
2. **Policy ID**: Discover via `GET /policy-overviews`

### Create the Bundle
```bash
curl -X POST "$BASE/bundles" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "projectId": "your-project-id",
    "name": "My Model v1.0",
    "description": "Description of the model being governed",
    "policyId": "policy-uuid"
  }'
```

The response includes:
- `id` — The bundle ID (use this for all subsequent operations)
- `policyId` — The policy UUID (used for evidence submission)
- `policyVersionId` — The policy version UUID (used for findings)
- `stages` — The full stage structure inherited from the policy
- `stageApprovals` — Approval requirements per stage with org/user IDs
- `attachments` — Evidence attached to the bundle
- `classificationValue` — Auto-populated if policy has classification rules

### One Bundle Per Model Version
Best practice: create a new bundle for each significant model version. This keeps the audit trail clean:
- `My Model v1.0` — initial model
- `My Model v1.1` — retrained with new features
- `My Model v2.0` — architecture change

## Discovering Stage IDs

After creating a bundle, inspect it to find the stage IDs:

```bash
curl -s "$BASE/bundles/$BUNDLE_ID" \
  -H "X-Domino-Api-Key: $API_KEY"
```

The response includes a `stages` array:
```json
{
    "bundleId": "...",
    "stageId": "3a32d944-...",
    "stage": {
        "id": "3a32d944-...",
        "name": "Model Initiation",
        "policyVersionId": "102f6b3b-..."
    }
}
```

**Important**: The bundle response does NOT include evidenceSet IDs. To get those, fetch the policy directly:
```bash
curl -s "$BASE/policies/$POLICY_ID" -H "X-Domino-Api-Key: $API_KEY"
```

## Progressing Through Stages

### Starting a Stage
When you begin work on a stage:
```bash
curl -X PATCH "$BASE/bundles/$BUNDLE_ID/stages/$STAGE_ID" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "In Progress"}'
```

### Completing a Stage
After all evidence is attached and questions answered:
```bash
curl -X PATCH "$BASE/bundles/$BUNDLE_ID/stages/$STAGE_ID" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "Complete"}'
```

If the policy enforces gating and required questions are unanswered, this may fail.

### Typical Stage Progression

1. **Model Initiation** — Business case, risk tier, scope, data compliance, registration
2. **Development** — MLflow logging, data docs, methodology, code reproducibility, limitations
3. **Validation & Testing** — Out-of-sample metrics, fairness, SHAP, findings, stress tests
4. **Deployment Approval** — Findings resolved, committee approval, deployment plan, access controls
5. **Ongoing Monitoring** — Performance review, drift checks, alerts, re-validation
6. **Decommission** — Replacement plan, archive, endpoint removal, stakeholder notification

## Approval Gating

Each stage has designated approver organizations. Approval typically requires a member of the organization to sign off in the Domino UI. The `stageApprovals` section of the bundle response shows:
- Which organizations need to approve each stage
- Current approval status
- Approver IDs (useful for creating findings)

## Checking Bundle Status

At any point, inspect the current state:
```bash
curl -s "$BASE/bundles/$BUNDLE_ID" \
  -H "X-Domino-Api-Key: $API_KEY"
```

Look at:
- `stage` — Current stage name
- `state` — Bundle state (e.g., "Active")
- `classificationValue` — Auto-detected risk tier
- `attachments` — What evidence has been attached (count and details)
- `stageApprovals` — Approval status per stage

## Listing All Bundles in a Project

To see all bundles:
```bash
curl -s "$BASE/bundles?projectId=$PROJECT_ID" \
  -H "X-Domino-Api-Key: $API_KEY"
```

This returns summaries of all bundles, useful for checking if a bundle already exists before creating a duplicate.



### Evidence Workflow

# Evidence Workflow

This document explains how to attach evidence, answer policy questions, and create findings in governance bundles.

## Setup

```bash
API_KEY="$DOMINO_USER_API_KEY"
BASE="${DOMINO_GOVERNANCE_HOST:-$DOMINO_API_HOST}/api/governance/v1"
```

## Attachment Types

The attachments API endpoint is `POST /bundles/{bundleId}/attachments`. It supports **two attachment types**:

### ModelVersion

Attaches a registered model version from the Domino Model Registry.

**Identifier format**: JSON object `{"name": "model-name", "version": N}`

```bash
curl -X POST "$BASE/bundles/$BUNDLE_ID/attachments" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "ModelVersion",
    "identifier": {"name": "my-model", "version": 5},
    "name": "My Model v5",
    "description": "Model description and metrics."
  }'
```

**When to use**: When the model is registered in Domino's Model Registry. Use the model name and version number (integer).

### Report

Attaches a file from the project repository (git or DFS).

**Identifier format**: JSON object with branch, commit, source, and filename.

```bash
# For git-based projects:
curl -X POST "$BASE/bundles/$BUNDLE_ID/attachments" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "Report",
    "identifier": {
      "branch": "main",
      "commit": "abc123def...",
      "source": "git",
      "filename": "notebooks/02_train.ipynb"
    },
    "name": "02 Model Training",
    "description": "Training notebook with MLflow logging."
  }'

# For DFS-based projects:
# Use "source": "DFS" instead of "git"
```

**When to use**: For any project file — notebooks, scripts, plots, reports, config files. The filename is the path relative to the project root. Get the commit hash with `git rev-parse HEAD`.

### Important Notes on Attachment Types

The only valid types are:
- `ModelVersion` — with `identifier: {"name": "...", "version": N}`
- `Report` — with `identifier: {"branch": "...", "commit": "...", "source": "git"|"DFS", "filename": "..."}`

The `identifier` field must be a **JSON object**, not a flat string. Types like "File" or "ExternalLink" are not supported by the API.

---

## Answering Evidence Questions (EvidenceSet)

Policies define evidence questions via `evidenceSet` items in the YAML. These appear as interactive forms in the Domino UI under each stage's "Evidence" tab.

### Discovering EvidenceSet IDs

**IMPORTANT**: The bundle response (`GET /bundles/{bundleId}`) does NOT contain evidenceSet IDs. You must fetch them from the **policy** endpoint:

```bash
curl -s "$BASE/policies/$POLICY_ID" \
  -H "X-Domino-Api-Key: $API_KEY"
```

The response structure is:
```
stages[] → evidenceSet[] → artifacts[]
```

Each `evidenceSet` entry has:
- `id` — The evidence UUID (used as `evidenceId` in submission)
- `name` — Display name
- `artifacts[]` — Individual form fields, each with:
  - `id` — The artifact UUID (used as the key in `content`)
  - `inputType` — Form type (radio, textinput, textarea, select, checkbox, etc.)

### Submitting Answers

Use the `submit-result-to-policy` RPC endpoint:

```bash
curl -X POST "$BASE/rpc/submit-result-to-policy" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "bundleId": "bundle-uuid",
    "policyId": "policy-uuid",
    "evidenceId": "evidence-set-uuid",
    "content": {
      "artifact-uuid": "value"
    }
  }'
```

### Field Reference

| Field | Description | Where to Find |
|-------|-------------|---------------|
| `bundleId` | The bundle ID | From `POST /bundles` or `GET /bundles/{id}` |
| `policyId` | The policy ID (**NOT** `policyVersionId`) | From bundle response → `policyId` field |
| `evidenceId` | The evidenceSet item UUID | From `GET /policies/{policyId}` → `stages[].evidenceSet[].id` |
| `content` | Map of `{artifactId: value}` | Keys from `stages[].evidenceSet[].artifacts[].id` |

### Content Value Types

| Input Type | Value Format | Example |
|------------|-------------|---------|
| `radio` | String matching an option label | `"Yes"` |
| `textinput` | Plain text string | `"Jane Smith"` |
| `textarea` | Multi-line text string | `"Detailed description..."` |
| `select` | String matching an option label | `"Tier 2 — High"` |
| `checkbox` | Array of selected option labels | `["Claims prediction", "Reserving"]` |
| `multiSelect` | Array of selected option labels | `["Option A", "Option B"]` |
| `date` | Date string | `"2026-03-04"` |
| `numeric` | Number as string | `"0.628"` |

### Submission Tips

- You can submit one artifact at a time or multiple artifacts for the same evidenceId in one call
- Each successful submission returns the full bundle JSON
- If a policy has `classification` rules tied to an artifact, the bundle's `classificationValue` updates automatically
- The `policyId` field is the policy UUID, NOT the `policyVersionId` — this is a common gotcha

---

## Creating Findings

Findings document issues discovered during review.

### Required Fields

```bash
curl -X POST "$BASE/findings" \
  -H "X-Domino-Api-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "bundleId": "bundle-uuid",
    "policyVersionId": "policy-version-uuid",
    "name": "Finding title",
    "title": "Finding title",
    "description": "Detailed description of the issue...",
    "severity": "High",
    "approver": {"id": "org-or-user-uuid", "name": "org-name"},
    "assignee": {"id": "user-uuid", "name": "username"}
  }'
```

Get the `policyVersionId` from the bundle response (`GET /bundles/{bundleId}`). Get user/org IDs from the `stageApprovals` section of the bundle response.

### Severity Levels

| Severity | When to Use | Example |
|----------|-------------|---------|
| Low | Minor concern, no action needed | "Training data has 2% missing values in a field" |
| Medium | Should be addressed, not blocking | "High correlation between two input features" |
| High | Must be addressed before deployment | "Model AUC below policy threshold" |
| Critical | Blocks deployment, immediate action | "Data leakage detected — future data used as feature" |

---

## Helper: Batch Attach Files

```bash
# Attach multiple project files in one go
API_KEY="$DOMINO_USER_API_KEY"
BASE="${DOMINO_GOVERNANCE_HOST:-$DOMINO_API_HOST}/api/governance/v1"
BUNDLE="your-bundle-id"
COMMIT=$(git rev-parse HEAD)
BRANCH=$(git rev-parse --abbrev-ref HEAD)

for file in "notebooks/01_eda.ipynb" "notebooks/02_train.ipynb" "notebooks/03_validate.ipynb"; do
  name=$(basename "$file")
  curl -s -X POST "$BASE/bundles/$BUNDLE/attachments" \
    -H "X-Domino-Api-Key: $API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"type\": \"Report\",
      \"identifier\": {\"branch\": \"$BRANCH\", \"commit\": \"$COMMIT\", \"source\": \"git\", \"filename\": \"$file\"},
      \"name\": \"$name\",
      \"description\": \"Attached from project repository.\"
    }"
done
```

