---
name: domino-flows
description: Orchestrate multi-step ML workflows using Domino Flows (built on Flyte).
  Define DAGs with typed inputs/outputs, heterogeneous environments, automatic lineage,
  and reproducibility. Use when building data pipelines, multi-stage training workflows,
  or processes requiring orchestration and monitoring.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- pipelines
- workflows
- automation
trigger_patterns:
- domino flow
- domino pipeline
- domino workflow
- domino automation
---

# Domino Flows Skill

This skill provides comprehensive knowledge for orchestrating ML workflows using Domino Flows, built on the Flyte platform.

## Key Concepts

### What are Domino Flows?

Domino Flows enable:
- **DAG-based orchestration**: Define workflows as directed acyclic graphs
- **Typed interfaces**: Strong typing for inputs and outputs
- **Heterogeneous environments**: Different environments per task
- **Automatic lineage**: Track data and model provenance
- **Reproducibility**: Version-controlled workflows
- **Scalability**: Distributed execution across compute resources

### Core Components

| Component | Description |
|-----------|-------------|
| **Task** | Single unit of work (runs as a Domino Job) |
| **Workflow** | DAG connecting tasks |
| **Artifact** | Typed input/output passed between tasks |
| **Launch Plan** | Configured workflow execution |

## Related Documentation

- [FLOW-BASICS.md](./FLOW-BASICS.md) - DAG concepts, task definitions
- [EXAMPLES.md](./EXAMPLES.md) - Common flow patterns

## Quick Start

> ⚠️ **Critical**: Domino Flows does NOT support native Flyte `@task` decorators.
> Tasks must use `DominoJobTask` + `DominoJobConfig`. Only `@workflow` is unchanged.

### Basic Flow

Each task runs as a Domino Job. Stage scripts read from `/workflow/inputs/<name>`
and write to `/workflow/outputs/o0`. Pass `PYTHONPATH=/mnt/code` in the command.

```python
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

preprocess_task = DominoJobTask(
    name="Preprocess Data",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/stages/preprocess.py'",
    ),
    inputs={"input_path": str},
    outputs={"o0": str},
    use_latest=True,
)

train_task = DominoJobTask(
    name="Train Model",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/stages/train.py'",
    ),
    inputs={"preprocess_output": str},
    outputs={"o0": str},
    use_latest=True,
)

@workflow
def training_pipeline(input_path: str = "/mnt/data/raw.csv") -> str:
    preprocess_output = preprocess_task(input_path=input_path)
    result = train_task(preprocess_output=preprocess_output)
    return result
```

### Stage Script Pattern

```python
# stages/preprocess.py
import json, os

INPUTS, OUTPUTS = "/workflow/inputs", "/workflow/outputs"

def main():
    input_path = open(f"{INPUTS}/input_path").read().strip()
    # ... do work ...
    os.makedirs(OUTPUTS, exist_ok=True)
    with open(f"{OUTPUTS}/o0", "w") as f:
        f.write(json.dumps({"output_path": "/mnt/artifacts/processed.parquet"}))

if __name__ == "__main__":
    main()
```

### Running the Flow

```bash
# Always commit and push first — jobs run against remote repo state
git add -A && git commit -m "..." && git push

# Trigger remotely
PYTHONPATH=/mnt/code pyflyte run --remote \
    my_flow.py training_pipeline \
    --input_path "/mnt/data/raw.csv"
```

## When to Use Flows

### Good Use Cases

- Data processing → Model training pipelines
- ETL with ML steps
- Multi-stage training with different environments
- Processes requiring reproducibility and lineage
- Scheduled/triggered workflows

### Not Ideal For

- Single dataset with many small computations
- Tasks that write to mutable shared state
- Simple single-step processes
- Real-time inference (use Model APIs instead)

## Documentation Links

- Domino Flows: https://docs.dominodatalab.com/en/latest/user_guide/78acf5/orchestrate-with-flows/
- Flyte Documentation: https://docs.flyte.org/


---

## Reference Documentation


### Examples

# Domino Flows Examples

Complete, production-ready flow examples for Domino Flows.

> ⚠️ **Critical**: Use `DominoJobTask` + `DominoJobConfig`. Native `@task` decorators are NOT supported.

## Example 1: Data Processing Pipeline

### Flow Definition (`flows/data_pipeline.py`)

```python
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

load_task = DominoJobTask(
    name="Load Data",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/flows/stages/load.py'",
    ),
    inputs={"source_path": str, "dataset_version": str},
    outputs={"o0": str},
    use_latest=True,
)

clean_task = DominoJobTask(
    name="Clean Data",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/flows/stages/clean.py'",
    ),
    inputs={"load_output": str},
    outputs={"o0": str},
    use_latest=True,
)

feature_task = DominoJobTask(
    name="Create Features",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/flows/stages/features.py'",
    ),
    inputs={"clean_output": str},
    outputs={"o0": str},
    use_latest=True,
)

@workflow
def data_pipeline(
    source_path: str = "/mnt/data/raw.csv",
    dataset_version: str = "1.0",
) -> str:
    load_output = load_task(source_path=source_path, dataset_version=dataset_version)
    clean_output = clean_task(load_output=load_output)
    features_output = feature_task(clean_output=clean_output)
    return features_output
```

### Stage Script (`flows/stages/load.py`)

```python
import json, os
import pandas as pd

INPUTS = "/workflow/inputs"
OUTPUTS = "/workflow/outputs"

def main():
    source_path = open(f"{INPUTS}/source_path").read().strip()
    dataset_version = open(f"{INPUTS}/dataset_version").read().strip()

    df = pd.read_csv(source_path)

    # Save to shared location (e.g., /mnt/artifacts/ or /mnt/data/)
    output_path = "/mnt/artifacts/loaded_data.parquet"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_parquet(output_path, index=False)

    result = {
        "output_path": output_path,
        "row_count": len(df),
        "dataset_version": dataset_version,
    }
    os.makedirs(OUTPUTS, exist_ok=True)
    with open(f"{OUTPUTS}/o0", "w") as f:
        f.write(json.dumps(result))

if __name__ == "__main__":
    main()
```

## Example 2: Model Training Pipeline

### Flow Definition (`flows/training_pipeline.py`)

```python
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

prepare_task = DominoJobTask(
    name="Prepare Training Data",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/flows/stages/prepare.py'",
    ),
    inputs={"data_path": str, "test_size": float},
    outputs={"o0": str},
    use_latest=True,
)

train_task = DominoJobTask(
    name="Train Model",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/flows/stages/train.py'",
        # Override hardware for GPU training:
        # HardwareTierId="gpu-k8s",
    ),
    inputs={"prepare_output": str, "model_type": str},
    outputs={"o0": str},
    use_latest=True,
)

evaluate_task = DominoJobTask(
    name="Evaluate Model",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/flows/stages/evaluate.py'",
    ),
    inputs={"train_output": str},
    outputs={"o0": str},
    use_latest=True,
)

@workflow
def training_pipeline(
    data_path: str = "/mnt/data/features.parquet",
    test_size: float = 0.2,
    model_type: str = "xgboost",
) -> str:
    prepare_output = prepare_task(data_path=data_path, test_size=test_size)
    train_output = train_task(prepare_output=prepare_output, model_type=model_type)
    eval_output = evaluate_task(train_output=train_output)
    return eval_output
```

### Stage Script (`flows/stages/train.py`)

```python
import json, os
import mlflow
import pandas as pd
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score

INPUTS = "/workflow/inputs"
OUTPUTS = "/workflow/outputs"

def main():
    prepare_output = json.loads(open(f"{INPUTS}/prepare_output").read())
    model_type = open(f"{INPUTS}/model_type").read().strip()

    df = pd.read_parquet(prepare_output["train_path"])
    X = df.drop(columns=["target"])
    y = df["target"]

    with mlflow.start_run() as run:
        model = XGBRegressor(n_estimators=200, max_depth=6, learning_rate=0.1)
        model.fit(X, y)

        preds = model.predict(X)
        r2 = r2_score(y, preds)
        mlflow.log_metric("r2_score", r2)
        mlflow.xgboost.log_model(model, "model")

    result = {
        "run_id": run.info.run_id,
        "r2_score": r2,
        "model_type": model_type,
    }
    os.makedirs(OUTPUTS, exist_ok=True)
    with open(f"{OUTPUTS}/o0", "w") as f:
        f.write(json.dumps(result))
    print(f"Training complete: R²={r2:.4f}, run_id={run.info.run_id}")

if __name__ == "__main__":
    main()
```

## Example 3: Multi-Stage ML Pipeline (Full Reference)

This is the Engine Forge 7-stage pipeline — a complete production example.

### Flow Definition

```python
"""7-stage engine design pipeline."""
import logging
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

logger = logging.getLogger(__name__)

def _make_task(stage_num: int, name: str, inputs: dict, outputs: dict = None) -> DominoJobTask:
    """Helper to create a stage task with consistent config."""
    return DominoJobTask(
        name=f"Stage {stage_num}: {name}",
        domino_job_config=DominoJobConfig(
            Command=f"bash -c 'PYTHONPATH=/mnt/code python /mnt/code/app/flow/stages/stage{stage_num}_{name.lower().replace(' ', '_')}.py'",
        ),
        inputs=inputs,
        outputs=outputs or {"o0": str},
        use_latest=True,
    )

ingest_task = DominoJobTask(
    name="Stage 1: Ingest Data",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/app/flow/stages/stage1_ingest.py'",
    ),
    inputs={"dataset_version": str, "component_id": str, "spec_json": str, "n_top": int},
    outputs={"o0": str},
    use_latest=True,
)

analyze_task = DominoJobTask(
    name="Stage 2: Analyze Designs",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/app/flow/stages/stage2_analyze.py'",
    ),
    inputs={"snapshot": str},
    outputs={"o0": str},
    use_latest=True,
)

# ... stages 3-6 follow same pattern ...

@workflow
def engine_forge_pipeline(
    component_id: str = "engine-bracket",
    dataset_version: str = "1.0",
    spec_json: str = '{"max_stress_mpa": 1200.0}',
    n_top: int = 2,
) -> str:
    snapshot = ingest_task(
        dataset_version=dataset_version,
        component_id=component_id,
        spec_json=spec_json,
        n_top=n_top,
    )
    analysis_output = analyze_task(snapshot=snapshot)
    # ... chain remaining stages ...
    return analysis_output
```

## Running Flows

### Trigger Remotely

```bash
# Always commit and push first — jobs run against remote repo state
git add -A && git commit -m "..." && git push

# Trigger the flow
PYTHONPATH=/mnt/code pyflyte run --remote \
    app/flow/my_flow.py my_pipeline \
    --arg1 "value1" \
    --arg2 42
```

### Monitor Execution

```python
from flytekit.remote import FlyteRemote
from flytekit.configuration import Config
import time

remote = FlyteRemote(
    config=Config.auto(),   # reads ~/.flyte/config.yaml
    default_project="<your-project-id>",
    default_domain="development",
)

PHASES = {0:"UNDEFINED",1:"QUEUED",2:"RUNNING",3:"SUCCEEDING",4:"SUCCEEDED",
          5:"FAILING",6:"FAILED",7:"ABORTED",8:"TIMED_OUT"}

exec_id = "my-execution-name"   # from pyflyte run output
for _ in range(60):
    execution = remote.fetch_execution(name=exec_id)
    remote.sync(execution, sync_nodes=True)
    phase = PHASES[execution.closure.phase]

    node_statuses = {
        nid: PHASES[ne.closure.phase]
        for nid, ne in execution.node_executions.items()
    }
    print(f"{phase}: {node_statuses}")

    if phase in ("SUCCEEDED", "FAILED", "ABORTED"):
        break
    time.sleep(30)
```

### Debug Failed Stage

```python
for node_id, node_exec in execution.node_executions.items():
    phase = PHASES[node_exec.closure.phase]
    if phase in ("FAILED", "FAILING"):
        for te in (node_exec.task_executions or []):
            full_te = remote.client.get_task_execution(te.id)
            if full_te.closure.error:
                # Full error message includes Python traceback from the job
                print(f"=== {node_id} error ===")
                print(full_te.closure.error.message)
```

## Data Sharing Between Stages

Since each stage is an isolated Domino Job, persistent data must use shared storage:

| Storage | Path | Use Case |
|---------|------|----------|
| Domino Artifacts | `/mnt/artifacts/` | Model files, reports (persisted) |
| Domino Datasets | `/mnt/data/<name>/` | Read-only reference data |
| Flow messages | `/workflow/inputs|outputs/` | Small JSON metadata between stages |

**Pattern**: Write large files to `/mnt/artifacts/`, pass the path as a JSON string through `/workflow/outputs/o0`.

```python
# Stage 2 writes parquet to artifacts, passes path via flow
output_path = "/mnt/artifacts/analysis_results.parquet"
df_results.to_parquet(output_path)
result = {"results_path": output_path, "row_count": len(df_results)}
with open(f"{OUTPUTS}/o0", "w") as f:
    f.write(json.dumps(result))

# Stage 3 reads from artifacts using the path
analysis_output = json.loads(open(f"{INPUTS}/analysis_output").read())
df = pd.read_parquet(analysis_output["results_path"])
```



### Flow Basics

# Domino Flows Basics

This guide covers the fundamentals of building workflows with Domino Flows.

> ⚠️ **Critical**: Domino Flows does NOT support native Flyte `@task` decorators.
> All tasks must use `DominoJobTask` + `DominoJobConfig` from `flytekitplugins.domino.task`.
> Only `@workflow` from `flytekit` is used unchanged.

## Task Definition

### Basic DominoJobTask

Each task runs as a Domino Job. The `Command` in `DominoJobConfig` specifies the script to run.
Inputs and outputs are passed via files at `/workflow/inputs/<name>` and `/workflow/outputs/<name>`.

```python
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

my_task = DominoJobTask(
    name="My Task Name",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/my_script.py'",
    ),
    inputs={"input_value": str},   # type hints for each input
    outputs={"o0": str},           # outputs named o0, o1, etc.
    use_latest=True,               # resolve hardware/environment from project defaults
)
```

### Stage Script Pattern

Each task's script reads from `/workflow/inputs/<name>` and writes to `/workflow/outputs/o0`:

```python
# my_script.py
import json, os

INPUTS = "/workflow/inputs"
OUTPUTS = "/workflow/outputs"

def main():
    # Read inputs (each input is a plain text file)
    input_value = open(f"{INPUTS}/input_value").read().strip()

    # Do work
    result = {"processed": input_value, "status": "done"}

    # Write output (always named o0, o1, etc.)
    os.makedirs(OUTPUTS, exist_ok=True)
    with open(f"{OUTPUTS}/o0", "w") as f:
        f.write(json.dumps(result))

if __name__ == "__main__":
    main()
```

### PYTHONPATH Requirement

Domino Jobs do not inherit the workspace Python path. Always set `PYTHONPATH` explicitly:

```python
# ✅ Correct: Set PYTHONPATH so app imports work
Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/app/stages/my_stage.py'"

# ❌ Wrong: Module 'app' not found
Command="python /mnt/code/app/stages/my_stage.py"
```

## Workflow Definition

### Basic Sequential Workflow

```python
from flytekit import workflow
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

ingest_task = DominoJobTask(
    name="Stage 1: Ingest",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/stages/stage1.py'",
    ),
    inputs={"source_path": str},
    outputs={"o0": str},
    use_latest=True,
)

train_task = DominoJobTask(
    name="Stage 2: Train",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/stages/stage2.py'",
    ),
    inputs={"ingest_output": str},
    outputs={"o0": str},
    use_latest=True,
)

@workflow
def my_pipeline(source_path: str = "/mnt/data/raw") -> str:
    """Connect tasks in a sequential DAG."""
    ingest_output = ingest_task(source_path=source_path)
    result = train_task(ingest_output=ingest_output)
    return result
```

### Multiple Inputs

```python
multi_input_task = DominoJobTask(
    name="Multi Input Task",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/stages/multi.py'",
    ),
    inputs={
        "dataset_version": str,
        "component_id": str,
        "n_top": int,           # int inputs are written as plain text: "2"
        "threshold": float,     # float inputs: "0.95"
    },
    outputs={"o0": str},
    use_latest=True,
)
```

In the stage script, read ints/floats as:
```python
n_top = int(open(f"{INPUTS}/n_top").read().strip())
threshold = float(open(f"{INPUTS}/threshold").read().strip())
```

## Supported Input/Output Types

Domino Flows passes all data between stages as serialized text files:

| Python Type | How it appears in `/workflow/inputs/<name>` |
|-------------|----------------------------------------------|
| `str` | Plain text |
| `int` | "42" |
| `float` | "3.14" |
| `bool` | "True" or "False" |

> **Best practice**: Use `str` for complex data by JSON-serializing dicts/lists.
> This avoids type conversion issues and works reliably across all stages.

```python
# In stage script: serialize output as JSON string
result = {"key": "value", "count": 42}
with open(f"{OUTPUTS}/o0", "w") as f:
    f.write(json.dumps(result))

# In next stage: deserialize
data = json.loads(open(f"{INPUTS}/prev_output").read())
```

## Hardware and Environment Configuration

`use_latest=True` calls `resolveJobDefaults` to fetch the project's default hardware tier,
environment, and commit ID. To override, set fields explicitly on `DominoJobConfig`:

```python
DominoJobConfig(
    Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/stages/gpu_stage.py'",
    HardwareTierId="gpu-k8s",           # Override hardware tier
    EnvironmentId="698505e4701849448243f120",  # Override environment
)
```

## Triggering and Monitoring

### Run Remotely

```bash
# Trigger flow execution
PYTHONPATH=/mnt/code pyflyte run --remote \
    app/flow/my_flow.py my_pipeline \
    --source_path "/mnt/data/raw"
```

### Monitor Status

```python
from flytekit.remote import FlyteRemote
from flytekit.configuration import Config

# Use Config.auto() — reads ~/.flyte/config.yaml (endpoint: 127.0.0.1:8181)
remote = FlyteRemote(
    config=Config.auto(),
    default_project="<project-id>",
    default_domain="development",    # pyflyte run --remote uses "development"
)

PHASES = {0:"UNDEFINED",1:"QUEUED",2:"RUNNING",3:"SUCCEEDING",4:"SUCCEEDED",
          5:"FAILING",6:"FAILED",7:"ABORTED",8:"TIMED_OUT"}

execution = remote.fetch_execution(name="my-execution-name")
remote.sync(execution, sync_nodes=True)
print(f"Phase: {PHASES[execution.closure.phase]}")
for node_id, node_exec in sorted(execution.node_executions.items()):
    print(f"  {node_id}: {PHASES[node_exec.closure.phase]}")
```

### Get Error Details

```python
for node_id, node_exec in execution.node_executions.items():
    for te in (node_exec.task_executions or []):
        full_te = remote.client.get_task_execution(te.id)
        if full_te.closure.error:
            print(full_te.closure.error.message)
```

## Common Pitfalls

### 1. DatasetSnapshots — Verify Version Before Use

`DominoJobConfig.DatasetSnapshots` lets you mount Domino Datasets, but the `snapshotVersion`
must match an existing snapshot or Domino will return a 500 error at job creation time.
`resolveJobDefaults` echoes back whatever version you provide without validation.

**Safest approach**: Don't specify `DatasetSnapshots`. Instead, add a fallback in each stage:

```python
# In each stage script — self-healing data loading
try:
    df = load_features()           # Try reading from mounted/cached parquet
except FileNotFoundError:
    df = prepare_dataset()         # Generate from raw files if absent
```

### 2. resolveJobDefaults Overwrites DatasetSnapshots

When `use_latest=True`, `resolve_job_properties()` calls `resolveJobDefaults` which
**unconditionally overwrites** `DatasetSnapshots` with what the API returns.
If the project has no default datasets, `DatasetSnapshots` becomes `[]` regardless of
what you set — unless the API returns your dataset back (which only happens if the version
is valid).

### 3. CommitId Is Pinned at Registration Time

`resolveJobDefaults` returns the latest synced commit ID from the project's linked repo.
Always commit and push before triggering a flow — the job runs against the **remote repo state**,
not local files. There may be a sync delay of seconds to minutes between pushing to GitHub
and Domino's internal git mirror updating.

### 4. No `@task` Decorator

```python
# ❌ This will NOT work in Domino Flows
from flytekit import task

@task
def my_task(x: str) -> str:
    return x.upper()

# ✅ This is the correct pattern
from flytekitplugins.domino.task import DominoJobConfig, DominoJobTask

my_task = DominoJobTask(
    name="My Task",
    domino_job_config=DominoJobConfig(
        Command="bash -c 'PYTHONPATH=/mnt/code python /mnt/code/my_script.py'",
    ),
    inputs={"x": str},
    outputs={"o0": str},
    use_latest=True,
)
```

