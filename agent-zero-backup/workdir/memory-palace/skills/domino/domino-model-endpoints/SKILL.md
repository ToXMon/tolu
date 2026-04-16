---
name: domino-model-endpoints
description: Deploy and monitor model API endpoints in Domino. Covers creating prediction
  endpoints, version management, Grafana dashboards for latency/errors/resources,
  alerting, and GPU inference with NVIDIA Triton. Use when deploying models as APIs,
  monitoring production endpoints, or debugging endpoint issues.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- models
- deployment
- endpoints
- api
trigger_patterns:
- domino model endpoint
- domino deploy model
- domino model api
- domino prediction
---

# Domino Model Endpoints Skill

This skill provides comprehensive knowledge for deploying and monitoring model API endpoints in Domino Data Lab.

## Key Concepts

### Model Endpoints Overview

Domino Model Endpoints provide:
- REST API for model predictions
- Automatic scaling and load balancing
- Version management
- Built-in monitoring with Grafana
- Authentication via API tokens

### Endpoint Lifecycle

```
Train Model → Register → Deploy Endpoint → Monitor → Update Version
```

## Related Documentation

- [DEPLOY-ENDPOINT.md](./DEPLOY-ENDPOINT.md) - Creating model APIs
- [MONITORING.md](./MONITORING.md) - Grafana, metrics, alerts
- [SCALING.md](./SCALING.md) - GPU inference, Triton, scaling

## Environment Requirements

**Important:** Model APIs use the **default environment** set for your project. The environment must have the `uwsgi` Python package installed for model endpoints to work.

### Required Package
```dockerfile
# Add to your environment's Dockerfile instructions
RUN pip install uwsgi
```

Or in requirements.txt:
```
uwsgi
```

### Setting Default Environment
1. Go to **Project Settings** → **Execution Preferences**
2. Set the **Default Environment** that includes `uwsgi`
3. This environment will be used for all Model API deployments

## Quick Start

### 1. Create Endpoint Function

```python
# model.py
def predict(features):
    """
    Domino calls this function for predictions.

    Args:
        features: Input data (dict, list, or primitive)

    Returns:
        JSON-serializable prediction result
    """
    import pickle

    # Load model (cached after first call)
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)

    prediction = model.predict([features])
    return {"prediction": prediction.tolist()}
```

### 2. Deploy via Domino UI

1. Go to **Publish** → **Model APIs**
2. Click **New Model**
3. Configure:
   - Name: `my-classifier`
   - File: `model.py`
   - Function: `predict`
   - Environment: Select compute environment
4. Click **Publish**

### 3. Call the Endpoint

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"data": {"features": [1.0, 2.0, 3.0]}}' \
  https://your-domino.com/models/abc123/latest/model
```

## Environment Variables

When calling endpoints from apps:

| Variable | Description |
|----------|-------------|
| `MODEL_API_URL` | Full endpoint URL |
| `MODEL_API_TOKEN` | Bearer token for authentication |

## Key Metrics to Monitor

| Metric | Target |
|--------|--------|
| Latency P50 | < 100ms |
| Latency P99 | < 500ms |
| Error Rate | < 1% |
| CPU Usage | < 80% |
| Memory | Stable (no growth) |

## Documentation Links

- Domino Model APIs: https://docs.dominodatalab.com/en/latest/user_guide/8dbc91/model-apis/


---

## Reference Documentation


### Deploy Endpoint

# Deploying Model API Endpoints

This guide covers creating and managing model API endpoints in Domino Data Lab.

## Environment Requirements

**Important:** Model APIs use the **default environment** set for your project. Ensure your environment has the `uwsgi` package installed.

```dockerfile
# Add to your environment's Dockerfile instructions
RUN pip install uwsgi
```

To set the default environment:
1. Go to **Project Settings** → **Execution Preferences**
2. Set the **Default Environment** to one with `uwsgi` installed

## Creating an Endpoint

### Endpoint Function Requirements

```python
# model.py
def predict(input_data):
    """
    Requirements:
    1. Function must be importable (in .py file at project root)
    2. Can have any name (configured in UI)
    3. Takes one argument (the request data)
    4. Returns JSON-serializable data
    """
    # Your prediction logic
    return {"result": "value"}
```

### Basic Endpoint Example

```python
# model.py
import pickle
import os

# Global model cache
_model = None

def load_model():
    """Load model once and cache."""
    global _model
    if _model is None:
        model_path = os.environ.get('MODEL_PATH', 'model.pkl')
        with open(model_path, 'rb') as f:
            _model = pickle.load(f)
    return _model

def predict(features):
    """
    Predict endpoint function.

    Args:
        features: List of feature values or dict with features

    Returns:
        Dict with prediction and confidence
    """
    model = load_model()

    # Handle different input formats
    if isinstance(features, dict):
        feature_values = list(features.values())
    elif isinstance(features, list):
        feature_values = features
    else:
        return {"error": "Invalid input format"}

    # Make prediction
    prediction = model.predict([feature_values])
    probability = model.predict_proba([feature_values])

    return {
        "prediction": int(prediction[0]),
        "confidence": float(max(probability[0])),
        "probabilities": probability[0].tolist()
    }
```

### Scikit-learn Example

```python
# model.py
import joblib
import numpy as np

_model = None

def load_model():
    global _model
    if _model is None:
        _model = joblib.load('random_forest_model.joblib')
    return _model

def predict(data):
    """
    Predict using scikit-learn model.

    Input format:
    {
        "features": [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    }

    Output format:
    {
        "predictions": [0, 1],
        "model_version": "1.0"
    }
    """
    model = load_model()

    features = data.get('features', [])
    if not features:
        return {"error": "No features provided"}

    X = np.array(features)
    predictions = model.predict(X)

    return {
        "predictions": predictions.tolist(),
        "model_version": "1.0"
    }
```

### PyTorch Example

```python
# model.py
import torch
import json

_model = None
_device = None

def load_model():
    global _model, _device
    if _model is None:
        _device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        _model = torch.jit.load('model_scripted.pt')
        _model.to(_device)
        _model.eval()
    return _model, _device

def predict(data):
    """
    Predict using PyTorch model.

    Input format:
    {
        "inputs": [[1.0, 2.0, ...]]
    }
    """
    model, device = load_model()

    inputs = data.get('inputs', [])
    if not inputs:
        return {"error": "No inputs provided"}

    with torch.no_grad():
        tensor = torch.tensor(inputs, dtype=torch.float32).to(device)
        outputs = model(tensor)
        predictions = outputs.argmax(dim=1).cpu().tolist()

    return {"predictions": predictions}
```

### TensorFlow/Keras Example

```python
# model.py
import tensorflow as tf
import numpy as np
import os

_model = None

def load_model():
    global _model
    if _model is None:
        # Suppress TF warnings
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        _model = tf.keras.models.load_model('keras_model.h5')
    return _model

def predict(data):
    """
    Predict using TensorFlow/Keras model.
    """
    model = load_model()

    inputs = data.get('inputs', [])
    if not inputs:
        return {"error": "No inputs provided"}

    X = np.array(inputs)
    predictions = model.predict(X)

    return {
        "predictions": predictions.tolist(),
        "shape": list(predictions.shape)
    }
```

## Deploying via Domino UI

### Step-by-Step

1. Navigate to your project
2. Go to **Publish** → **Model APIs**
3. Click **+ New Model**
4. Fill in configuration:
   - **Name**: Descriptive name (e.g., `fraud-detector`)
   - **Description**: What the model does
   - **File**: Python file containing function (e.g., `model.py`)
   - **Function**: Function name (e.g., `predict`)
   - **Environment**: Select compute environment
   - **Hardware Tier**: Select resources (CPU/GPU)
5. Click **Publish**

### Environment Variables

Add environment variables in the UI:

```
MODEL_PATH=/mnt/artifacts/model.pkl
MODEL_VERSION=1.0
DEBUG=false
```

Access in code:
```python
import os
model_path = os.environ.get('MODEL_PATH', 'model.pkl')
```

## Deploying via API

### Using Domino Python Client

```python
from domino import Domino

domino = Domino(
    host="https://your-domino.com",
    api_key="your-api-key"
)

# Create model endpoint
model = domino.model_publish(
    file="model.py",
    function="predict",
    environment_id="env-123",
    name="my-classifier",
    description="Classification model"
)

print(f"Model ID: {model['id']}")
print(f"Model URL: {model['url']}")
```

## Calling Endpoints

Domino supports both synchronous (real-time) and asynchronous (long-running) request types.

### Synchronous Requests (Real-time)

For quick predictions that return immediately:

```python
import requests

# Synchronous endpoint URL format
url = "{DOMINO_URL}/models/{MODEL_ID}/latest/model"

# Authentication options:
# Option 1: Using auth parameter (token, token)
response = requests.post(
    url,
    auth=("{MODEL_ACCESS_TOKEN}", "{MODEL_ACCESS_TOKEN}"),
    json={"data": {"start": 1, "stop": 100}}
)

# Option 2: Using Bearer token in header
headers = {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_API_TOKEN"
}
response = requests.post(url, json={"data": {"features": [1.0, 2.0, 3.0]}}, headers=headers)

result = response.json()
print(result)
```

### Asynchronous Requests (Long-running)

For predictions that take longer to process:

```python
import requests
import time

DOMINO_URL = "https://your-domino.com"
MODEL_ID = "abc123"
MODEL_ACCESS_TOKEN = "your_token"

# Step 1: Submit async request
response = requests.post(
    f"{DOMINO_URL}/api/modelApis/async/v1/{MODEL_ID}",
    headers={
        "Authorization": f"Bearer {MODEL_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    },
    json={"parameters": {"input_file": "s3://example/filename.ext"}}
)

# Get prediction ID
prediction_id = response.json()["predictionId"]
print(f"Prediction ID: {prediction_id}")

# Step 2: Poll for results
while True:
    status_response = requests.get(
        f"{DOMINO_URL}/api/modelApis/async/v1/{MODEL_ID}/{prediction_id}",
        headers={"Authorization": f"Bearer {MODEL_ACCESS_TOKEN}"}
    )
    status = status_response.json()

    if status["status"] == "COMPLETED":
        print(f"Result: {status['result']}")
        break
    elif status["status"] == "FAILED":
        print(f"Error: {status['error']}")
        break
    else:
        print(f"Status: {status['status']}")
        time.sleep(5)  # Wait before polling again
```

### Request Parameter Formats

Depending on your function signature, format requests differently:

```python
# For function: my_function(x, y, z)
# Named parameters
{"data": {"x": 1, "y": 2, "z": 3}}
# Or positional
{"parameters": [1, 2, 3]}

# For function: my_function(dict)
{"parameters": [{"x": 1, "y": 2, "z": 3}]}

# For function: my_function(x, **kwargs)
{"data": {"x": 1, "y": 2, "z": 3}}
```

### JavaScript/React

```javascript
async function predict(features) {
    const response = await fetch(process.env.MODEL_API_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${process.env.MODEL_API_TOKEN}`,
        },
        body: JSON.stringify({ data: { features } }),
    });

    if (!response.ok) {
        throw new Error(`API error: ${response.status}`);
    }

    return response.json();
}
```

### cURL

```bash
curl -X POST \
  "https://your-domino.com/models/abc123/latest/model" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_API_TOKEN" \
  -d '{"data": {"features": [1.0, 2.0, 3.0]}}'
```

## Version Management

### Creating New Version

1. Update your model file
2. Go to Model API → Versions
3. Click **+ New Version**
4. Select updated file/function
5. Publish

### Switching Active Version

```bash
# Use specific version
curl -X POST "https://domino.com/models/abc123/v/2/model" ...

# Use latest
curl -X POST "https://domino.com/models/abc123/latest/model" ...
```

### Blue-Green Deployment

1. Deploy new version as v2
2. Test v2 endpoint directly
3. Once validated, update clients to use v2
4. Deprecate v1

## Error Handling

### In Endpoint Function

```python
def predict(data):
    try:
        # Validate input
        if not data or 'features' not in data:
            return {
                "error": "Missing 'features' in input",
                "code": "INVALID_INPUT"
            }

        features = data['features']

        # Type checking
        if not isinstance(features, list):
            return {
                "error": "Features must be a list",
                "code": "TYPE_ERROR"
            }

        # Make prediction
        model = load_model()
        prediction = model.predict([features])

        return {"prediction": prediction.tolist()}

    except Exception as e:
        # Log error for debugging
        print(f"Prediction error: {str(e)}")
        return {
            "error": "Internal prediction error",
            "code": "PREDICTION_ERROR"
        }
```

### Client-Side Handling

```python
response = requests.post(url, json=data, headers=headers)

if response.status_code == 200:
    result = response.json()
    if "error" in result:
        print(f"Model error: {result['error']}")
    else:
        print(f"Prediction: {result['prediction']}")
elif response.status_code == 401:
    print("Authentication failed")
elif response.status_code == 503:
    print("Model temporarily unavailable")
else:
    print(f"Request failed: {response.status_code}")
```

## Best Practices

### 1. Cache Model Loading

```python
# Good: Load once
_model = None
def load_model():
    global _model
    if _model is None:
        _model = load_from_disk()
    return _model

# Bad: Load every request
def predict(data):
    model = load_from_disk()  # Slow!
```

### 2. Input Validation

```python
def predict(data):
    # Validate early
    if not isinstance(data, dict):
        return {"error": "Input must be a dictionary"}

    features = data.get('features')
    if features is None:
        return {"error": "Missing 'features' key"}

    if len(features) != 4:
        return {"error": f"Expected 4 features, got {len(features)}"}
```

### 3. Response Consistency

```python
# Always return consistent structure
def predict(data):
    try:
        result = model.predict(data['features'])
        return {
            "success": True,
            "prediction": result,
            "error": None
        }
    except Exception as e:
        return {
            "success": False,
            "prediction": None,
            "error": str(e)
        }
```

### 4. Log for Debugging

```python
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def predict(data):
    logger.info(f"Received request: {data}")

    result = model.predict(data['features'])

    logger.info(f"Prediction: {result}")
    return {"prediction": result}
```



### Monitoring

# Monitoring Model Endpoints

This guide covers monitoring model API endpoints using Domino's built-in Grafana dashboards and alerting.

## Key Metrics to Monitor

| Metric | Description | Target |
|--------|-------------|--------|
| CPU Usage | Processor utilization | < 80% sustained |
| Memory Usage | RAM utilization | Stable, no growth |
| Latency P50 | Median response time | < 100ms |
| Latency P95 | 95th percentile | < 300ms |
| Latency P99 | 99th percentile | < 500ms |
| Error Rate | Percentage of 4xx/5xx | < 1% |
| Request Rate | Requests per second | Varies by use case |
| Status Codes | Distribution of responses | Mostly 2xx |

## Accessing Grafana Dashboards

### Via Domino UI

1. Navigate to your project
2. Go to **Publish** → **Model APIs**
3. Select your model
4. Click **Monitoring** tab
5. Opens Grafana dashboard

### Grafana Dashboard Features

- **Real-time metrics**: Updates every few seconds
- **Time range selection**: Last 1h, 24h, 7d, etc.
- **Multiple panels**: CPU, memory, latency, errors
- **Drill-down**: Click panels for details

## CPU and Memory Monitoring

### What to Look For

**CPU Usage:**
- Consistent patterns indicate normal operation
- Spikes correlate with request bursts
- Sustained high usage may need scaling

**Memory Usage:**
- Should stabilize after model initialization
- Continuous growth indicates memory leak
- Sudden drops may indicate restarts

### Grafana CPU Query

```promql
# CPU usage percentage
100 * (1 - avg(rate(container_cpu_usage_seconds_total{
  pod=~"model-.*"
}[5m])))
```

### Grafana Memory Query

```promql
# Memory usage in MB
container_memory_usage_bytes{pod=~"model-.*"} / 1024 / 1024
```

## Latency Monitoring

### Understanding Latency Percentiles

| Percentile | Meaning |
|------------|---------|
| P50 (median) | Half of requests faster than this |
| P95 | 95% of requests faster than this |
| P99 | 99% of requests faster than this |

### Latency Distribution Query

```promql
# P50 latency
histogram_quantile(0.50, sum(rate(nginx_ingress_controller_request_duration_seconds_bucket{
  path=~"/models/MODEL_ID.*"
}[5m])) by (le))

# P95 latency
histogram_quantile(0.95, sum(rate(nginx_ingress_controller_request_duration_seconds_bucket{
  path=~"/models/MODEL_ID.*"
}[5m])) by (le))

# P99 latency
histogram_quantile(0.99, sum(rate(nginx_ingress_controller_request_duration_seconds_bucket{
  path=~"/models/MODEL_ID.*"
}[5m])) by (le))
```

### Latency Analysis Tips

1. **Baseline**: Establish normal latency range
2. **Correlate**: Check if spikes match deployments or traffic changes
3. **Investigate**: High P99 with low P50 suggests occasional slow requests

## Error Rate Monitoring

### Status Code Analysis

```promql
# Error rate percentage
100 * (
  sum(increase(nginx_ingress_controller_requests{
    status=~"400|402|403|404|405|406|408|429|5..",
    path=~"/models/MODEL_ID.*"
  }[$__range]))
  /
  sum(increase(nginx_ingress_controller_requests{
    path=~"/models/MODEL_ID.*"
  }[$__range]))
)
```

### Status Code Breakdown

```promql
# Requests by status code
sum(increase(nginx_ingress_controller_requests{
  path=~"/models/MODEL_ID.*"
}[$__range])) by (status)
```

### Common Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| 400 | Bad Request | Check client input format |
| 401 | Unauthorized | Verify API token |
| 404 | Not Found | Check model ID/version |
| 429 | Too Many Requests | Rate limiting hit |
| 500 | Internal Error | Check model logs |
| 502 | Bad Gateway | Model pod issues |
| 503 | Service Unavailable | Model not ready |
| 504 | Gateway Timeout | Model too slow |

## Request Traffic Analysis

### Traffic Volume Query

```promql
# Requests per minute
sum(rate(nginx_ingress_controller_requests{
  path=~"/models/MODEL_ID.*"
}[1m])) * 60
```

### Traffic Patterns

- **Daily patterns**: Business hours vs. off-hours
- **Weekly patterns**: Weekday vs. weekend
- **Anomalies**: Unexpected spikes or drops

## Creating Alerts

### Alert Types

| Alert | Condition | Severity |
|-------|-----------|----------|
| High Error Rate | > 5% for 5 min | Critical |
| High Latency | P99 > 2s for 5 min | Warning |
| High CPU | > 90% for 10 min | Warning |
| Memory Leak | Growth > 10%/hour | Critical |
| Low Traffic | < 1 req/min for 15 min | Info |

### Grafana Alert Configuration

1. Open dashboard panel
2. Click **Edit** → **Alert** tab
3. Configure conditions:
   - **Query**: Metric to monitor
   - **Condition**: Threshold and duration
   - **Notifications**: Where to send alerts

### Example Alert Rules

**High Error Rate Alert:**
```yaml
name: High Error Rate
condition: error_rate > 5
for: 5m
labels:
  severity: critical
annotations:
  summary: "Model endpoint error rate above 5%"
  description: "Error rate is {{ $value }}%"
```

**High Latency Alert:**
```yaml
name: High Latency
condition: latency_p99 > 2
for: 5m
labels:
  severity: warning
annotations:
  summary: "Model P99 latency above 2 seconds"
  description: "P99 latency is {{ $value }}s"
```

## Building Custom Dashboards

### Dashboard JSON Structure

```json
{
  "title": "Model Endpoint Monitoring",
  "panels": [
    {
      "title": "Request Rate",
      "type": "graph",
      "targets": [
        {
          "expr": "sum(rate(nginx_ingress_controller_requests{path=~\"/models/MODEL_ID.*\"}[1m])) * 60"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "stat",
      "targets": [
        {
          "expr": "100 * sum(rate(nginx_ingress_controller_requests{status=~\"5..\",path=~\"/models/MODEL_ID.*\"}[5m])) / sum(rate(nginx_ingress_controller_requests{path=~\"/models/MODEL_ID.*\"}[5m]))"
        }
      ]
    }
  ]
}
```

### Useful Panel Types

| Type | Use Case |
|------|----------|
| Graph | Time series (latency, traffic) |
| Stat | Single value (current error rate) |
| Gauge | Current value with thresholds |
| Table | Breakdown by dimension |
| Heatmap | Latency distribution |

## Debugging Issues

### High Latency Investigation

1. Check CPU usage during slow requests
2. Review model logs for errors
3. Test model locally for comparison
4. Check input data size
5. Review recent code changes

### Memory Leak Investigation

```python
# Add to model.py for debugging
import tracemalloc

tracemalloc.start()

def predict(data):
    result = model.predict(data)

    # Log memory usage periodically
    current, peak = tracemalloc.get_traced_memory()
    print(f"Current: {current / 1024 / 1024:.1f}MB, Peak: {peak / 1024 / 1024:.1f}MB")

    return result
```

### Error Investigation

1. Check Grafana for error spike timing
2. Review model pod logs
3. Check for correlations with traffic or deployments
4. Test endpoint with sample requests
5. Review error response bodies

## Log Analysis

### Accessing Model Logs

1. Go to Model API in Domino UI
2. Click **Logs** tab
3. View stdout/stderr from model

### Log Patterns to Watch

```
# Startup issues
ERROR: Model failed to load

# Memory issues
MemoryError: Unable to allocate

# Timeout issues
Request timeout after 30 seconds

# Input issues
ValueError: Invalid input shape
```

## Best Practices

### 1. Set Up Baseline Monitoring

- Record metrics for 1 week before alerting
- Understand normal patterns
- Set thresholds based on baseline

### 2. Use SLOs

Define Service Level Objectives:
- Availability: 99.9%
- Latency P99: < 500ms
- Error rate: < 0.1%

### 3. Monitor Business Metrics

Beyond technical metrics:
- Predictions per customer
- Model usage by feature
- Accuracy (if labels available)

### 4. Regular Review

- Weekly: Review dashboards
- Monthly: Analyze trends
- Quarterly: Update thresholds



### Scaling

# Scaling Model Endpoints

This guide covers scaling strategies for Domino model endpoints, including GPU inference with NVIDIA Triton.

## Scaling Strategies

### Horizontal Scaling (Replicas)

Increase the number of model instances:

```
Traffic → Load Balancer → [Model Pod 1]
                       → [Model Pod 2]
                       → [Model Pod 3]
```

**When to use:**
- High request volume
- CPU-bound models
- Need high availability

### Vertical Scaling (Resources)

Increase CPU/memory per instance:

**When to use:**
- Large models
- Memory-intensive operations
- GPU requirements

## Configuring Replicas

### Via Domino UI

1. Go to Model API settings
2. Find **Scaling** section
3. Set **Minimum Replicas** and **Maximum Replicas**
4. Configure **Target CPU Utilization** for auto-scaling

### Replica Guidelines

| Traffic | Min Replicas | Max Replicas |
|---------|-------------|--------------|
| Low (< 10 RPS) | 1 | 2 |
| Medium (10-100 RPS) | 2 | 5 |
| High (> 100 RPS) | 3 | 10+ |

## Auto-Scaling

### CPU-Based Auto-Scaling

Domino automatically scales based on CPU utilization:

```yaml
autoscaling:
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

**How it works:**
1. Monitor average CPU across pods
2. If CPU > 70%, add pods
3. If CPU < 70%, remove pods (with cooldown)

### Memory-Based Considerations

- Memory doesn't trigger auto-scaling by default
- Set appropriate memory limits to prevent OOM
- Monitor memory for capacity planning

## Hardware Tiers

### Selecting Hardware

| Tier | Use Case |
|------|----------|
| small | Simple models, low traffic |
| medium | Standard ML models |
| large | Large models, high throughput |
| gpu-small | Small deep learning models |
| gpu-large | Large neural networks, LLMs |

### GPU Considerations

```python
# Check for GPU availability in your model
import torch

def load_model():
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    print(f"Using device: {device}")
    model = MyModel().to(device)
    return model, device
```

## GPU Inference with NVIDIA Triton

### What is Triton?

NVIDIA Triton Inference Server provides:
- High-performance inference
- Multiple model support
- Dynamic batching
- Model versioning
- Metrics and monitoring

### Triton Model Repository Structure

```
model_repository/
└── my_model/
    ├── config.pbtxt
    └── 1/
        └── model.onnx
```

### config.pbtxt Example

```protobuf
name: "my_model"
platform: "onnxruntime_onnx"
max_batch_size: 8
input [
  {
    name: "input"
    data_type: TYPE_FP32
    dims: [ 224, 224, 3 ]
  }
]
output [
  {
    name: "output"
    data_type: TYPE_FP32
    dims: [ 1000 ]
  }
]
instance_group [
  {
    kind: KIND_GPU
    count: 1
  }
]
dynamic_batching {
  preferred_batch_size: [ 4, 8 ]
  max_queue_delay_microseconds: 100
}
```

### Converting Models for Triton

**PyTorch to ONNX:**
```python
import torch

model = MyModel()
model.eval()

dummy_input = torch.randn(1, 3, 224, 224)
torch.onnx.export(
    model,
    dummy_input,
    "model.onnx",
    input_names=['input'],
    output_names=['output'],
    dynamic_axes={'input': {0: 'batch_size'}}
)
```

**TensorFlow to SavedModel:**
```python
import tensorflow as tf

model = tf.keras.models.load_model('my_model.h5')
model.save('model_repository/my_model/1/model.savedmodel')
```

### Dynamic Batching

Group multiple requests for efficient GPU utilization:

```protobuf
dynamic_batching {
  preferred_batch_size: [ 4, 8, 16 ]
  max_queue_delay_microseconds: 100
}
```

**Benefits:**
- Higher GPU utilization
- Better throughput
- Lower cost per prediction

## Optimizing Model Performance

### Model Optimization Techniques

| Technique | Speedup | Accuracy Impact |
|-----------|---------|-----------------|
| Quantization (INT8) | 2-4x | Minimal |
| Pruning | 2-3x | Varies |
| Knowledge Distillation | 2-10x | Some |
| ONNX Runtime | 1.5-2x | None |

### Quantization Example

```python
import torch

# Dynamic quantization
quantized_model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8
)
```

### ONNX Optimization

```python
import onnx
from onnxruntime.transformers import optimizer

# Optimize ONNX model
optimized_model = optimizer.optimize_model(
    "model.onnx",
    model_type='bert',
    num_heads=12,
    hidden_size=768
)
optimized_model.save_model_to_file("model_optimized.onnx")
```

## Caching Strategies

### In-Memory Caching

```python
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def cached_predict(features_hash):
    """Cache predictions for repeated inputs."""
    features = decode_features(features_hash)
    return model.predict(features)

def predict(data):
    features = data['features']
    features_hash = hashlib.md5(str(features).encode()).hexdigest()
    return cached_predict(features_hash)
```

### External Caching (Redis)

```python
import redis
import json
import hashlib

redis_client = redis.Redis(host='redis-host', port=6379)
CACHE_TTL = 3600  # 1 hour

def predict(data):
    features = data['features']
    cache_key = f"pred:{hashlib.md5(str(features).encode()).hexdigest()}"

    # Check cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Compute prediction
    result = model.predict(features)

    # Store in cache
    redis_client.setex(cache_key, CACHE_TTL, json.dumps(result))

    return result
```

## Load Testing

### Using Locust

```python
# locustfile.py
from locust import HttpUser, task, between

class ModelUser(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def predict(self):
        self.client.post(
            "/models/abc123/latest/model",
            json={"data": {"features": [1.0, 2.0, 3.0]}},
            headers={
                "Authorization": "Bearer TOKEN",
                "Content-Type": "application/json"
            }
        )
```

Run test:
```bash
locust -f locustfile.py --host=https://your-domino.com
```

### Performance Targets

| Metric | Development | Production |
|--------|-------------|------------|
| Latency P50 | < 200ms | < 100ms |
| Latency P99 | < 1s | < 500ms |
| Throughput | 10 RPS | 100+ RPS |
| Error Rate | < 5% | < 0.1% |

## Cost Optimization

### Right-Sizing Resources

1. Start with small hardware tier
2. Monitor CPU/memory utilization
3. Scale up only if needed
4. Use auto-scaling for variable traffic

### Spot/Preemptible Instances

For non-critical workloads:
- Lower cost
- May be interrupted
- Good for batch processing

### Idle Scaling

```yaml
# Scale to zero when not in use
autoscaling:
  minReplicas: 0
  maxReplicas: 5
  scaleDownDelaySeconds: 300  # 5 minutes idle before scale down
```

## Best Practices

### 1. Warm-Up Requests

```python
def warmup():
    """Send warm-up requests on startup."""
    sample_input = {"features": [0.0] * 10}
    for _ in range(5):
        predict(sample_input)
    print("Model warmed up")
```

### 2. Connection Pooling

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=0.1)
adapter = HTTPAdapter(pool_connections=10, pool_maxsize=10, max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)
```

### 3. Async Processing

```python
import asyncio
import aiohttp

async def predict_async(session, data):
    async with session.post(url, json=data, headers=headers) as response:
        return await response.json()

async def batch_predict(items):
    async with aiohttp.ClientSession() as session:
        tasks = [predict_async(session, item) for item in items]
        return await asyncio.gather(*tasks)
```

### 4. Monitor and Iterate

1. Establish baseline metrics
2. Test under load
3. Identify bottlenecks
4. Optimize and repeat

