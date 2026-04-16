---
name: domino-experiment-tracking
description: Track traditional ML experiments in Domino using the MLflow-based Experiment
  Manager. Covers experiment setup, auto-logging for sklearn/TensorFlow/PyTorch, manual
  logging, artifact storage, run comparison, and model registration. Use when training
  ML models, logging metrics and parameters, comparing model runs, or registering
  models.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- mlflow
- experiments
- metrics
trigger_patterns:
- domino experiment
- domino mlflow
- track experiment
- domino metrics
---

# Domino Experiment Tracking Skill

This skill provides comprehensive knowledge for tracking ML experiments in Domino Data Lab using the built-in MLflow-based Experiment Manager.

## Key Concepts

### Experiment Manager Overview

Domino's Experiment Manager is built on MLflow and provides:
- Automatic and manual logging of parameters, metrics, and artifacts
- Run comparison and visualization
- Model versioning and registry
- Integration with Domino projects and jobs

### Critical Configuration

**Experiment names must be unique across the entire Domino deployment.** Always append username or project name to ensure uniqueness.

## Related Documentation

- [MLFLOW-BASICS.md](./MLFLOW-BASICS.md) - Auto-logging, manual logging
- [COMPARING-RUNS.md](./COMPARING-RUNS.md) - Run comparison, export
- [MODEL-REGISTRY.md](./MODEL-REGISTRY.md) - Model registration & stages

## Quick Start

```python
import mlflow
import os

# CRITICAL: Experiment names must be unique across Domino deployment
username = os.environ.get('DOMINO_STARTING_USERNAME', 'unknown')
experiment_name = f"my-experiment-{username}"

# Set the experiment
mlflow.set_experiment(experiment_name)

# Enable auto-logging (easiest approach)
mlflow.autolog()

# Run training
with mlflow.start_run(run_name="my-first-run"):
    model.fit(X_train, y_train)

    # Optional: manually log additional items
    mlflow.log_param("custom_param", "value")
    mlflow.log_metric("custom_metric", 0.95)
```

## Supported Frameworks

| Framework | Auto-log Command |
|-----------|------------------|
| Scikit-learn | `mlflow.sklearn.autolog()` |
| TensorFlow/Keras | `mlflow.tensorflow.autolog()` |
| PyTorch | `mlflow.pytorch.autolog()` |
| XGBoost | `mlflow.xgboost.autolog()` |
| LightGBM | `mlflow.lightgbm.autolog()` |
| All at once | `mlflow.autolog()` |

## Environment Variables

Domino automatically configures MLflow to use the built-in tracking server. These variables are pre-set:

| Variable | Description |
|----------|-------------|
| `MLFLOW_TRACKING_URI` | Domino's MLflow server URL |
| `DOMINO_STARTING_USERNAME` | User running the experiment |
| `DOMINO_PROJECT_NAME` | Current project name |
| `DOMINO_RUN_ID` | Domino job run ID |

## Documentation Links

- Domino Experiment Tracking: https://docs.dominodatalab.com/en/latest/user_guide/da707d/track-and-monitor-experiments/
- Domino Model Registry: https://docs.dominodatalab.com/en/latest/user_guide/3b6ae5/manage-models-with-model-registry/


---

## Reference Documentation


### Comparing Runs

# Comparing and Analyzing Experiment Runs

This guide covers how to compare experiment runs, search for specific runs, and export results in Domino Data Lab.

## Viewing Runs in Domino UI

### Accessing Experiment Manager

1. Navigate to your Domino project
2. Click **Experiments** in the left sidebar
3. Select your experiment by name
4. View the runs table with metrics, parameters, and status

### Run Comparison View

1. Select multiple runs using checkboxes
2. Click **Compare** button
3. View side-by-side comparison of:
   - Parameters
   - Metrics
   - Artifacts
   - Training curves

## Programmatic Run Search

### Search by Experiment

```python
import mlflow

# Get experiment by name
experiment = mlflow.get_experiment_by_name("my-experiment-jsmith")

# Search all runs in experiment
runs = mlflow.search_runs(
    experiment_ids=[experiment.experiment_id],
    order_by=["metrics.accuracy DESC"]
)

print(runs[["run_id", "params.learning_rate", "metrics.accuracy"]])
```

### Filter Runs

```python
# Search with filter string (SQL-like syntax)
runs = mlflow.search_runs(
    experiment_names=["my-experiment-jsmith"],
    filter_string="metrics.accuracy > 0.9 AND params.model_type = 'random_forest'",
    order_by=["metrics.accuracy DESC"],
    max_results=10
)
```

### Filter String Syntax

| Operator | Example |
|----------|---------|
| `=` | `params.model = 'xgboost'` |
| `!=` | `params.model != 'baseline'` |
| `>`, `>=` | `metrics.accuracy > 0.9` |
| `<`, `<=` | `metrics.loss <= 0.1` |
| `LIKE` | `params.name LIKE '%test%'` |
| `AND` | `metrics.a > 0.8 AND metrics.b < 0.5` |
| `OR` | `params.model = 'a' OR params.model = 'b'` |

### Search by Tags

```python
runs = mlflow.search_runs(
    experiment_names=["my-experiment-jsmith"],
    filter_string="tags.team = 'ml-platform' AND tags.priority = 'high'"
)
```

### Search by Run Status

```python
# Only finished runs
runs = mlflow.search_runs(
    experiment_names=["my-experiment-jsmith"],
    filter_string="status = 'FINISHED'"
)

# Status values: RUNNING, SCHEDULED, FINISHED, FAILED, KILLED
```

## Getting Run Details

### Load Specific Run

```python
# Get run by ID
run = mlflow.get_run("abc123def456")

# Access run info
print(f"Run ID: {run.info.run_id}")
print(f"Status: {run.info.status}")
print(f"Start time: {run.info.start_time}")
print(f"End time: {run.info.end_time}")
print(f"Artifact URI: {run.info.artifact_uri}")

# Access parameters
print(f"Parameters: {run.data.params}")

# Access metrics
print(f"Metrics: {run.data.metrics}")

# Access tags
print(f"Tags: {run.data.tags}")
```

### Get Metric History

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get full history of a metric
history = client.get_metric_history(run_id="abc123", key="loss")

for metric in history:
    print(f"Step {metric.step}: {metric.value}")
```

## Downloading Artifacts

### Download All Artifacts

```python
# Download to local directory
local_path = mlflow.artifacts.download_artifacts(
    run_id="abc123def456",
    artifact_path="",  # Empty for all artifacts
    dst_path="./downloaded_artifacts"
)
```

### Download Specific Artifact

```python
# Download specific file
local_path = mlflow.artifacts.download_artifacts(
    run_id="abc123def456",
    artifact_path="model/model.pkl"
)
```

### List Artifacts

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()
artifacts = client.list_artifacts(run_id="abc123def456")

for artifact in artifacts:
    print(f"{artifact.path} - {artifact.file_size} bytes")
```

## Loading Models from Runs

### Load Model by Run ID

```python
# Load sklearn model
model = mlflow.sklearn.load_model(f"runs:/abc123def456/model")

# Make predictions
predictions = model.predict(X_test)
```

### Load Model by URI

```python
# Load from artifact URI
model = mlflow.pyfunc.load_model(
    "mlflow-artifacts:/abc123def456/artifacts/model"
)
```

## Exporting Run Data

### Export to DataFrame

```python
import pandas as pd

# Get all runs as DataFrame
runs_df = mlflow.search_runs(
    experiment_names=["my-experiment-jsmith"]
)

# Export to CSV
runs_df.to_csv("experiment_runs.csv", index=False)
```

### Export to JSON

```python
import json

runs = mlflow.search_runs(
    experiment_names=["my-experiment-jsmith"],
    output_format="list"  # Returns list of dicts
)

with open("experiment_runs.json", "w") as f:
    json.dump(runs, f, indent=2, default=str)
```

## Comparing Runs Programmatically

### Best Run by Metric

```python
# Find best run
runs = mlflow.search_runs(
    experiment_names=["my-experiment-jsmith"],
    order_by=["metrics.accuracy DESC"],
    max_results=1
)

best_run_id = runs.iloc[0]["run_id"]
best_accuracy = runs.iloc[0]["metrics.accuracy"]
print(f"Best run: {best_run_id} with accuracy {best_accuracy}")
```

### Compare Parameters Across Runs

```python
runs = mlflow.search_runs(
    experiment_names=["my-experiment-jsmith"],
    filter_string="metrics.accuracy > 0.85"
)

# Analyze parameter impact
param_analysis = runs.groupby("params.learning_rate").agg({
    "metrics.accuracy": ["mean", "std", "count"]
})
print(param_analysis)
```

### Visualize Run Comparison

```python
import matplotlib.pyplot as plt

runs = mlflow.search_runs(
    experiment_names=["my-experiment-jsmith"]
)

# Scatter plot of two metrics
plt.figure(figsize=(10, 6))
plt.scatter(
    runs["params.learning_rate"].astype(float),
    runs["metrics.accuracy"],
    c=runs["params.n_estimators"].astype(float),
    cmap="viridis"
)
plt.xlabel("Learning Rate")
plt.ylabel("Accuracy")
plt.colorbar(label="N Estimators")
plt.title("Hyperparameter Analysis")
plt.savefig("hyperparameter_analysis.png")
```

## Managing Runs

### Delete Runs

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Delete a run (moves to trash)
client.delete_run(run_id="abc123def456")

# Restore a deleted run
client.restore_run(run_id="abc123def456")
```

### Update Run Tags

```python
client = MlflowClient()

# Add or update tag
client.set_tag(run_id="abc123def456", key="reviewed", value="true")

# Delete tag
client.delete_tag(run_id="abc123def456", key="reviewed")
```

### Rename Run

```python
client = MlflowClient()
client.set_tag(
    run_id="abc123def456",
    key="mlflow.runName",
    value="new-run-name"
)
```

## Complete Comparison Example

```python
import mlflow
import pandas as pd
import matplotlib.pyplot as plt

# Search for all completed runs
experiment_name = "model-optimization-jsmith"
runs = mlflow.search_runs(
    experiment_names=[experiment_name],
    filter_string="status = 'FINISHED'",
    order_by=["metrics.test_accuracy DESC"]
)

print(f"Found {len(runs)} completed runs")

# Display top 5 runs
print("\nTop 5 Runs:")
top_runs = runs.head()[["run_id", "params.model_type", "params.learning_rate",
                         "metrics.test_accuracy", "metrics.train_accuracy"]]
print(top_runs.to_string())

# Find best run
best_run = runs.iloc[0]
print(f"\nBest Run: {best_run['run_id']}")
print(f"  Model: {best_run['params.model_type']}")
print(f"  Test Accuracy: {best_run['metrics.test_accuracy']:.4f}")

# Load best model
best_model = mlflow.sklearn.load_model(f"runs:/{best_run['run_id']}/model")

# Parameter analysis
print("\nAccuracy by Model Type:")
model_analysis = runs.groupby("params.model_type")["metrics.test_accuracy"].agg(
    ["mean", "std", "count"]
)
print(model_analysis)

# Export results
runs.to_csv(f"{experiment_name}_results.csv", index=False)
print(f"\nResults exported to {experiment_name}_results.csv")
```



### Mlflow Basics

# MLflow Basics for Domino Experiment Tracking

This guide covers the fundamentals of using MLflow for experiment tracking in Domino Data Lab.

## Setting Up an Experiment

### Unique Experiment Names

**CRITICAL**: Experiment names must be unique across the entire Domino deployment, not just your project.

```python
import mlflow
import os

def setup_experiment(base_name: str = "experiment"):
    """
    Set up a Domino-compatible MLflow experiment.

    Automatically appends username to ensure uniqueness.
    """
    username = os.environ.get('DOMINO_STARTING_USERNAME', 'unknown')
    project = os.environ.get('DOMINO_PROJECT_NAME', 'unknown')

    # Unique name format
    experiment_name = f"{base_name}-{project}-{username}"

    mlflow.set_experiment(experiment_name)
    print(f"Experiment set: {experiment_name}")

    return experiment_name
```

### Adding Domino Context as Tags

```python
def log_domino_context():
    """Log Domino environment information as tags."""
    mlflow.set_tags({
        "domino.user": os.environ.get('DOMINO_STARTING_USERNAME', 'unknown'),
        "domino.project": os.environ.get('DOMINO_PROJECT_NAME', 'unknown'),
        "domino.run_id": os.environ.get('DOMINO_RUN_ID', 'unknown'),
        "domino.hardware_tier": os.environ.get('DOMINO_HARDWARE_TIER_NAME', 'unknown'),
    })
```

## Auto-Logging

Auto-logging is the easiest way to track experiments. MLflow automatically captures parameters, metrics, and models.

### Framework-Specific Auto-Logging

```python
# Scikit-learn
mlflow.sklearn.autolog()

# TensorFlow/Keras
mlflow.tensorflow.autolog()

# PyTorch
mlflow.pytorch.autolog()

# XGBoost
mlflow.xgboost.autolog()

# LightGBM
mlflow.lightgbm.autolog()

# CatBoost
mlflow.catboost.autolog()

# Spark
mlflow.spark.autolog()

# FastAI
mlflow.fastai.autolog()
```

### Enable All Auto-Logging

```python
# Enable auto-logging for all supported frameworks
mlflow.autolog()
```

### Auto-Logging Options

```python
mlflow.sklearn.autolog(
    log_input_examples=True,      # Log sample inputs
    log_model_signatures=True,    # Log model input/output schema
    log_models=True,              # Log trained models
    log_datasets=True,            # Log dataset info
    disable=False,                # Enable/disable
    exclusive=False,              # Only log from this framework
    disable_for_unsupported_versions=False,
    silent=False,                 # Suppress warnings
    max_tuning_runs=5,            # Max hyperparameter tuning runs
    log_post_training_metrics=True,
)
```

### Complete Auto-Logging Example

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_iris

# Setup
mlflow.set_experiment("iris-classification-jsmith")
mlflow.sklearn.autolog()

# Load data
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2
)

# Train - MLflow automatically logs everything
with mlflow.start_run(run_name="random-forest-v1"):
    model = RandomForestClassifier(n_estimators=100, max_depth=5)
    model.fit(X_train, y_train)

    # Auto-logged: parameters, metrics, model artifact
    # Manual addition for custom metrics
    test_accuracy = model.score(X_test, y_test)
    mlflow.log_metric("test_accuracy", test_accuracy)
```

## Manual Logging

For finer control, log items manually.

### Parameters

```python
with mlflow.start_run(run_name="manual-logging-example"):
    # Single parameter
    mlflow.log_param("learning_rate", 0.01)

    # Multiple parameters
    mlflow.log_params({
        "epochs": 100,
        "batch_size": 32,
        "optimizer": "adam",
        "hidden_layers": [64, 32],
    })
```

### Metrics

```python
with mlflow.start_run():
    # Single metric
    mlflow.log_metric("accuracy", 0.95)

    # Metric at specific step (for training curves)
    for epoch in range(100):
        train_loss = train_epoch()
        val_loss = validate()

        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_loss", val_loss, step=epoch)

    # Multiple metrics
    mlflow.log_metrics({
        "precision": 0.94,
        "recall": 0.92,
        "f1": 0.93,
    })
```

### Artifacts

```python
with mlflow.start_run():
    # Single file
    mlflow.log_artifact("confusion_matrix.png")

    # Entire directory
    mlflow.log_artifacts("output_folder/")

    # With subdirectory in artifact store
    mlflow.log_artifact("report.pdf", artifact_path="reports")

    # Log text directly
    mlflow.log_text("Model performed well on test set", "notes.txt")

    # Log dictionary as JSON
    mlflow.log_dict({"config": "value"}, "config.json")

    # Log figure
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    mlflow.log_figure(fig, "plot.png")
```

### Models

```python
with mlflow.start_run():
    # Scikit-learn model
    mlflow.sklearn.log_model(model, "sklearn_model")

    # PyTorch model
    mlflow.pytorch.log_model(model, "pytorch_model")

    # TensorFlow/Keras model
    mlflow.tensorflow.log_model(model, "tf_model")

    # Generic Python model
    mlflow.pyfunc.log_model(
        artifact_path="custom_model",
        python_model=MyCustomModel(),
        conda_env="conda.yaml"
    )
```

## Large Artifact Upload

For large files (LLMs, deep learning models), enable multipart upload:

```python
import os

# Enable multipart upload for large files
os.environ['MLFLOW_ENABLE_PROXY_MULTIPART_UPLOAD'] = "true"
os.environ['MLFLOW_MULTIPART_UPLOAD_CHUNK_SIZE'] = "104857600"  # 100MB chunks

with mlflow.start_run():
    mlflow.log_artifact("large_model.bin")
```

## Tags

Use tags for metadata that isn't a parameter:

```python
with mlflow.start_run():
    # Single tag
    mlflow.set_tag("model_type", "classification")

    # Multiple tags
    mlflow.set_tags({
        "team": "ml-platform",
        "priority": "high",
        "dataset_version": "v2.1",
    })
```

## Run Names and Descriptions

```python
# Set run name
with mlflow.start_run(run_name="experiment-baseline-v1"):
    pass

# Set description
with mlflow.start_run(run_name="final-model", description="Production candidate"):
    pass

# Update description after run
mlflow.set_tag("mlflow.note.content", "This run achieved best results")
```

## Nested Runs

For hyperparameter tuning or cross-validation:

```python
with mlflow.start_run(run_name="hyperparameter-search"):
    # Parent run
    mlflow.log_param("search_space", "grid")

    for lr in [0.01, 0.001, 0.0001]:
        with mlflow.start_run(run_name=f"lr-{lr}", nested=True):
            # Child run
            mlflow.log_param("learning_rate", lr)
            accuracy = train_and_evaluate(lr)
            mlflow.log_metric("accuracy", accuracy)
```

## Complete Example

```python
import mlflow
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.datasets import load_wine
from sklearn.metrics import classification_report
import json

# Setup experiment with unique name
username = os.environ.get('DOMINO_STARTING_USERNAME', 'dev')
mlflow.set_experiment(f"wine-classification-{username}")

# Load data
wine = load_wine()
X_train, X_test, y_train, y_test = train_test_split(
    wine.data, wine.target, test_size=0.2, random_state=42
)

# Training run
with mlflow.start_run(run_name="random-forest-optimized"):
    # Log Domino context
    mlflow.set_tags({
        "domino.user": username,
        "domino.project": os.environ.get('DOMINO_PROJECT_NAME', 'dev'),
        "model_type": "random_forest",
    })

    # Hyperparameters
    params = {
        "n_estimators": 200,
        "max_depth": 10,
        "min_samples_split": 5,
        "random_state": 42,
    }
    mlflow.log_params(params)

    # Train model
    model = RandomForestClassifier(**params)
    model.fit(X_train, y_train)

    # Metrics
    train_accuracy = model.score(X_train, y_train)
    test_accuracy = model.score(X_test, y_test)
    cv_scores = cross_val_score(model, X_train, y_train, cv=5)

    mlflow.log_metrics({
        "train_accuracy": train_accuracy,
        "test_accuracy": test_accuracy,
        "cv_mean": cv_scores.mean(),
        "cv_std": cv_scores.std(),
    })

    # Classification report as artifact
    y_pred = model.predict(X_test)
    report = classification_report(y_test, y_pred, output_dict=True)
    mlflow.log_dict(report, "classification_report.json")

    # Feature importance
    importance = dict(zip(wine.feature_names, model.feature_importances_))
    mlflow.log_dict(importance, "feature_importance.json")

    # Log model
    mlflow.sklearn.log_model(
        model,
        "model",
        input_example=X_test[:5],
    )

    print(f"Run ID: {mlflow.active_run().info.run_id}")
    print(f"Test Accuracy: {test_accuracy:.4f}")
```



### Model Registry

# Domino Model Registry

This guide covers registering, versioning, and managing models in Domino's Model Registry.

## Overview

The Model Registry provides:
- Centralized model storage
- Version tracking
- Stage transitions (Staging → Production)
- Model lineage and metadata
- Access control

## Registering Models

### Register During Training

```python
import mlflow

with mlflow.start_run():
    # Train model
    model.fit(X_train, y_train)

    # Log and register in one step
    mlflow.sklearn.log_model(
        model,
        artifact_path="model",
        registered_model_name="wine-classifier"
    )
```

### Register Existing Run

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Register model from existing run
result = client.create_model_version(
    name="wine-classifier",
    source=f"runs:/{run_id}/model",
    run_id=run_id
)

print(f"Registered version: {result.version}")
```

### Register with URI

```python
import mlflow

# Register from artifact URI
mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="wine-classifier"
)
```

## Model Versions

### List Versions

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get all versions of a model
versions = client.search_model_versions("name='wine-classifier'")

for v in versions:
    print(f"Version {v.version}: {v.current_stage} - Run: {v.run_id}")
```

### Get Specific Version

```python
# Get version details
version = client.get_model_version(
    name="wine-classifier",
    version="3"
)

print(f"Source: {version.source}")
print(f"Stage: {version.current_stage}")
print(f"Description: {version.description}")
```

### Update Version Description

```python
client.update_model_version(
    name="wine-classifier",
    version="3",
    description="Improved accuracy with feature engineering"
)
```

## Stage Transitions

### Model Stages

| Stage | Purpose |
|-------|---------|
| `None` | Initial state, not assigned |
| `Staging` | Ready for testing/validation |
| `Production` | Approved for production use |
| `Archived` | Deprecated, kept for reference |

### Transition Model Stage

```python
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Move to staging
client.transition_model_version_stage(
    name="wine-classifier",
    version="3",
    stage="Staging"
)

# Promote to production
client.transition_model_version_stage(
    name="wine-classifier",
    version="3",
    stage="Production"
)

# Archive old version
client.transition_model_version_stage(
    name="wine-classifier",
    version="2",
    stage="Archived"
)
```

### Archive Previous Production

```python
# When promoting new version, archive previous production
client.transition_model_version_stage(
    name="wine-classifier",
    version="3",
    stage="Production",
    archive_existing_versions=True  # Archives current Production version
)
```

## Loading Registered Models

### Load by Name and Version

```python
import mlflow

# Load specific version
model = mlflow.sklearn.load_model(
    model_uri="models:/wine-classifier/3"
)

predictions = model.predict(X_test)
```

### Load by Stage

```python
# Load production model
production_model = mlflow.sklearn.load_model(
    model_uri="models:/wine-classifier/Production"
)

# Load staging model
staging_model = mlflow.sklearn.load_model(
    model_uri="models:/wine-classifier/Staging"
)

# Load latest version
latest_model = mlflow.sklearn.load_model(
    model_uri="models:/wine-classifier/latest"
)
```

## Model Metadata

### Add Tags to Model

```python
client = MlflowClient()

# Model-level tags
client.set_registered_model_tag(
    name="wine-classifier",
    key="team",
    value="ml-platform"
)

# Version-level tags
client.set_model_version_tag(
    name="wine-classifier",
    version="3",
    key="validated",
    value="true"
)
```

### Add Aliases

```python
# Create alias for easy reference
client.set_registered_model_alias(
    name="wine-classifier",
    alias="champion",
    version="3"
)

# Load by alias
model = mlflow.sklearn.load_model("models:/wine-classifier@champion")
```

### Get Model Details

```python
# Get registered model info
model_info = client.get_registered_model("wine-classifier")

print(f"Name: {model_info.name}")
print(f"Description: {model_info.description}")
print(f"Tags: {model_info.tags}")
print(f"Latest versions: {model_info.latest_versions}")
```

## Model Lineage

### View Run Associated with Version

```python
version = client.get_model_version(
    name="wine-classifier",
    version="3"
)

# Get the source run
run = mlflow.get_run(version.run_id)

print(f"Training run: {run.info.run_id}")
print(f"Parameters: {run.data.params}")
print(f"Metrics: {run.data.metrics}")
```

### Track Data and Code Lineage

```python
with mlflow.start_run():
    # Log dataset info
    mlflow.set_tags({
        "dataset.name": "wine_data_v2",
        "dataset.version": "2024-01-15",
        "code.version": "git-abc123",
    })

    # Train and register
    model.fit(X_train, y_train)
    mlflow.sklearn.log_model(
        model,
        "model",
        registered_model_name="wine-classifier"
    )
```

## Deleting Models

### Delete Model Version

```python
client = MlflowClient()

# Delete specific version
client.delete_model_version(
    name="wine-classifier",
    version="1"
)
```

### Delete Entire Model

```python
# Delete model and all versions
client.delete_registered_model(name="wine-classifier")
```

## Searching Models

### Search Registered Models

```python
from mlflow import MlflowClient

client = MlflowClient()

# Search by name pattern
models = client.search_registered_models(
    filter_string="name LIKE 'wine%'"
)

for model in models:
    print(f"{model.name}: {len(model.latest_versions)} versions")
```

### Search Model Versions

```python
# Find production models
production_versions = client.search_model_versions(
    filter_string="current_stage='Production'"
)

for v in production_versions:
    print(f"{v.name} v{v.version}")
```

## Model Signatures

### Log with Signature

```python
from mlflow.models.signature import infer_signature

with mlflow.start_run():
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    # Infer signature from data
    signature = infer_signature(X_test, predictions)

    mlflow.sklearn.log_model(
        model,
        "model",
        signature=signature,
        input_example=X_test[:5],
        registered_model_name="wine-classifier"
    )
```

### View Signature

```python
import mlflow

model_info = mlflow.models.get_model_info("models:/wine-classifier/3")
print(f"Signature: {model_info.signature}")
```

## Complete Registry Workflow

```python
import mlflow
from mlflow.tracking import MlflowClient
from mlflow.models.signature import infer_signature

# Setup
client = MlflowClient()
model_name = "wine-classifier"

# Training run
with mlflow.start_run(run_name="production-candidate"):
    # Train model
    model.fit(X_train, y_train)

    # Evaluate
    train_acc = model.score(X_train, y_train)
    test_acc = model.score(X_test, y_test)

    mlflow.log_metrics({
        "train_accuracy": train_acc,
        "test_accuracy": test_acc
    })

    # Create signature
    signature = infer_signature(X_test, model.predict(X_test))

    # Register model
    mlflow.sklearn.log_model(
        model,
        "model",
        signature=signature,
        input_example=X_test[:3],
        registered_model_name=model_name
    )

    run_id = mlflow.active_run().info.run_id

# Get newly created version
versions = client.search_model_versions(f"name='{model_name}' and run_id='{run_id}'")
new_version = versions[0].version

print(f"Created model version: {new_version}")

# Move to staging for validation
client.transition_model_version_stage(
    name=model_name,
    version=new_version,
    stage="Staging"
)

# After validation, promote to production
client.transition_model_version_stage(
    name=model_name,
    version=new_version,
    stage="Production",
    archive_existing_versions=True
)

# Set champion alias
client.set_registered_model_alias(
    name=model_name,
    alias="champion",
    version=new_version
)

print(f"Model {model_name} v{new_version} is now in Production")

# Load and use
production_model = mlflow.sklearn.load_model(f"models:/{model_name}@champion")
predictions = production_model.predict(new_data)
```

## Documentation Links

- Domino Model Registry: https://docs.dominodatalab.com/en/latest/user_guide/3b6ae5/manage-models-with-model-registry/
- MLflow Model Registry: https://mlflow.org/docs/latest/model-registry.html

