---
name: domino-genai-tracing
description: Trace and evaluate GenAI applications including LLM calls, agents, RAG
  pipelines, and multi-step AI systems in Domino. Uses the Domino SDK (@add_tracing
  decorator, DominoRun context) with MLflow 3.2.0. Captures token usage, latency,
  cost, tool calls, and errors. Supports LLM-as-judge evaluators and custom metrics.
  Use when building agents, debugging LLM applications, or needing audit trails for
  GenAI systems.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- genai
- llm
- tracing
- evaluation
trigger_patterns:
- domino genai
- domino tracing
- domino llm trace
- genai evaluation
---

# Domino GenAI Tracing Skill

This skill provides comprehensive knowledge for tracing and evaluating GenAI applications in Domino Data Lab, including LLM calls, agents, RAG pipelines, and multi-step AI systems.

## Key Concepts

### What GenAI Tracing Captures

The Domino SDK automatically captures:
- **Token usage** - Input and output tokens per call
- **Latency** - Time for each operation
- **Cost** - Estimated cost per call
- **Tool calls** - Function/tool invocations
- **Errors** - Exceptions and failure modes
- **Model parameters** - Temperature, max_tokens, etc.

### Core Components

1. **`@add_tracing` decorator** - Wraps functions to capture traces
2. **`DominoRun` context manager** - Groups traces into runs with aggregation
3. **Evaluators** - Custom functions to score outputs
4. **MLflow integration** - View traces in Experiment Manager

## Related Documentation

- [TRACING-SETUP.md](./TRACING-SETUP.md) - Environment & SDK setup
- [ADD-TRACING-DECORATOR.md](./ADD-TRACING-DECORATOR.md) - @add_tracing usage
- [DOMINO-RUN.md](./DOMINO-RUN.md) - DominoRun context manager
- [EVALUATORS.md](./EVALUATORS.md) - LLM-as-judge, custom evaluators
- [MULTI-AGENT-EXAMPLE.md](./MULTI-AGENT-EXAMPLE.md) - Complete multi-agent example

## Quick Start

### 1. Environment Setup

Requires MLflow 3.2.0 and Domino SDK with AI systems support:

```dockerfile
RUN pip install mlflow==3.2.0
RUN pip install --no-cache-dir "git+https://github.com/dominodatalab/python-domino.git@master#egg=dominodatalab[data,aisystems]"
```

### 2. Basic Tracing

```python
import mlflow
from domino.agents.tracing import add_tracing
from domino.agents.logging import DominoRun

@add_tracing(name="my_agent", autolog_frameworks=["openai"])
def my_agent(query: str) -> str:
    response = llm.invoke(query)
    return response

# Run with tracing
with DominoRun() as run:
    result = my_agent("What is machine learning?")
```

### 3. With Evaluators

```python
def quality_evaluator(inputs, output):
    """Evaluate response quality."""
    return {"quality_score": assess_quality(output)}

@add_tracing(name="my_agent", evaluator=quality_evaluator)
def my_agent(query: str) -> str:
    return llm.invoke(query)
```

## Framework Support

| Framework | Auto-log Command |
|-----------|------------------|
| OpenAI | `mlflow.openai.autolog()` |
| Anthropic | `mlflow.anthropic.autolog()` |
| LangChain | `mlflow.langchain.autolog()` |

## Viewing Traces

1. Navigate to **Experiments** in your Domino project
2. Select the experiment (format: `tracing-{username}`)
3. Select a run
4. View the **Traces** tab for span tree visualization

## Blueprint Reference

Official GenAI Tracing Tutorial:
https://github.com/dominodatalab/GenAI-Tracing-Tutorial

## Documentation Links

- Domino GenAI Tracing: https://docs.dominodatalab.com/en/cloud/user_guide/fc1922/set-up-and-run-genai-traces/


---

## Reference Documentation


### Add Tracing Decorator

# @add_tracing Decorator Guide

The `@add_tracing` decorator is the core mechanism for capturing traces in Domino GenAI applications.

## Basic Usage

### Simple Tracing

```python
from domino.agents.tracing import add_tracing

@add_tracing(name="my_agent_function")
def my_agent_function(query: str) -> str:
    """
    The @add_tracing decorator captures:
    - Function inputs (arguments)
    - Function output (return value)
    - Execution time
    - Any LLM calls made within (if auto-logging enabled)
    - Errors and exceptions
    """
    response = llm.invoke(query)
    return response
```

### With LLM Framework

```python
import mlflow
from domino.agents.tracing import add_tracing
from openai import OpenAI

# Enable auto-tracing for OpenAI
mlflow.openai.autolog()

client = OpenAI()

@add_tracing(name="chat_agent")
def chat_agent(user_message: str) -> str:
    """All OpenAI calls within are automatically traced."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_message}]
    )
    return response.choices[0].message.content
```

## Decorator Parameters

### name (required)

The trace name shown in the UI:

```python
@add_tracing(name="incident_classifier")
def classify_incident(incident: dict) -> dict:
    pass
```

### evaluator (optional)

Function to evaluate the output:

```python
def my_evaluator(inputs, output):
    return {"quality_score": calculate_score(output)}

@add_tracing(name="my_agent", evaluator=my_evaluator)
def my_agent(query: str) -> str:
    pass
```

## What Gets Captured

### Inputs

All function arguments are captured:

```python
@add_tracing(name="process_data")
def process_data(text: str, max_length: int = 100, options: dict = None):
    pass

# Trace captures: text, max_length, options
```

### Outputs

The return value is captured:

```python
@add_tracing(name="generate_response")
def generate_response(query: str) -> dict:
    return {
        "answer": "...",
        "confidence": 0.95,
        "sources": ["doc1", "doc2"]
    }

# Trace captures the entire return dict
```

### Nested LLM Calls

With auto-logging enabled, all LLM calls within the function are captured as child spans:

```python
import mlflow
from domino.agents.tracing import add_tracing
from openai import OpenAI

mlflow.openai.autolog()
client = OpenAI()

@add_tracing(name="multi_step_agent")
def multi_step_agent(query: str) -> str:
    # First LLM call - captured as child span
    classification = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Classify: {query}"}]
    )

    # Second LLM call - captured as child span
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Respond to: {query}"}]
    )

    return response.choices[0].message.content
```

### Errors and Exceptions

Exceptions are captured in the trace:

```python
@add_tracing(name="risky_operation")
def risky_operation(data: dict) -> str:
    if not data:
        raise ValueError("Data cannot be empty")  # Captured in trace
    return process(data)
```

## Nested Tracing

Chain multiple traced functions for hierarchical traces:

```python
@add_tracing(name="classifier")
def classify(text: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Classify: {text}"}]
    )
    return response.choices[0].message.content

@add_tracing(name="responder")
def respond(text: str, category: str) -> str:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Respond as {category}: {text}"}]
    )
    return response.choices[0].message.content

@add_tracing(name="pipeline")
def pipeline(text: str) -> dict:
    # Both nested calls appear as child spans
    category = classify(text)
    response = respond(text, category)
    return {"category": category, "response": response}
```

Trace hierarchy in UI:
```
pipeline
├── classifier
│   └── [OpenAI call]
└── responder
    └── [OpenAI call]
```

## With Evaluators

### Basic Evaluator

```python
def quality_evaluator(inputs, output):
    """
    Evaluator function signature:
    - inputs: dict of argument names to values
    - output: return value of the decorated function

    Returns: dict of metric names to values
    """
    score = len(output) / 100  # Simple length-based score
    return {"quality_score": min(score, 1.0)}

@add_tracing(name="my_agent", evaluator=quality_evaluator)
def my_agent(query: str) -> str:
    return llm.invoke(query)
```

### LLM-as-Judge Evaluator

```python
def llm_judge_evaluator(inputs, output):
    """Use a separate LLM to evaluate quality."""
    judge_response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": f"""Rate this response 0-10:
            Question: {inputs['query']}
            Response: {output}
            Score (just the number):"""
        }]
    )
    score = float(judge_response.choices[0].message.content.strip()) / 10
    return {"judge_score": score}

@add_tracing(name="evaluated_agent", evaluator=llm_judge_evaluator)
def evaluated_agent(query: str) -> str:
    return llm.invoke(query)
```

### Multi-Metric Evaluator

```python
def comprehensive_evaluator(inputs, output):
    return {
        "relevance": assess_relevance(inputs["query"], output),
        "completeness": assess_completeness(output),
        "factuality": assess_factuality(output),
        "safety": assess_safety(output),
    }

@add_tracing(name="comprehensive_agent", evaluator=comprehensive_evaluator)
def comprehensive_agent(query: str) -> str:
    return llm.invoke(query)
```

## Async Functions

Tracing works with async functions:

```python
import asyncio
from domino.agents.tracing import add_tracing

@add_tracing(name="async_agent")
async def async_agent(query: str) -> str:
    response = await async_llm.invoke(query)
    return response

# Usage
async def main():
    result = await async_agent("Hello")
```

## Class Methods

Tracing works with class methods:

```python
class MyAgent:
    def __init__(self, model: str):
        self.model = model
        self.client = OpenAI()

    @add_tracing(name="agent_process")
    def process(self, query: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content

# Usage
agent = MyAgent("gpt-4o-mini")
result = agent.process("Hello")
```

## Best Practices

### 1. Use Descriptive Names

```python
# Good
@add_tracing(name="incident_classification_agent")
@add_tracing(name="customer_response_generator")

# Bad
@add_tracing(name="agent1")
@add_tracing(name="process")
```

### 2. Return Structured Data

```python
@add_tracing(name="classifier")
def classify(text: str) -> dict:
    # Return dict for better trace visibility
    return {
        "category": "technical",
        "confidence": 0.95,
        "subcategories": ["api", "authentication"]
    }
```

### 3. Include Context in Evaluators

```python
def contextual_evaluator(inputs, output):
    # Access all inputs for context
    query = inputs.get("query", "")
    context = inputs.get("context", "")

    return {
        "relevance_to_query": assess_relevance(query, output),
        "used_context": context in output,
    }
```

### 4. Handle Errors Gracefully

```python
@add_tracing(name="safe_agent")
def safe_agent(query: str) -> dict:
    try:
        result = llm.invoke(query)
        return {"success": True, "result": result}
    except Exception as e:
        # Error is captured in trace
        return {"success": False, "error": str(e)}
```

## Next Steps

- [DOMINO-RUN.md](./DOMINO-RUN.md) - Group traces with DominoRun
- [EVALUATORS.md](./EVALUATORS.md) - Advanced evaluator patterns
- [MULTI-AGENT-EXAMPLE.md](./MULTI-AGENT-EXAMPLE.md) - Complete example



### Domino Run

# DominoRun Context Manager Guide

The `DominoRun` context manager groups traces into runs, enabling aggregation, configuration tracking, and organized experiment viewing.

## Basic Usage

### Simple Run

```python
from domino.agents.logging import DominoRun

with DominoRun() as run:
    result = my_traced_function(input_data)
    print(f"Run ID: {run.run_id}")
```

### With Run Name

```python
with DominoRun(run_name="production-evaluation-2024") as run:
    for item in test_data:
        result = my_agent(item)
```

## Configuration File

### Loading Agent Configuration

Use `agent_config_path` to log configuration as MLflow parameters:

```python
from domino.agents.logging import DominoRun

with DominoRun(agent_config_path="config.yaml") as run:
    result = my_agent(query)
```

### config.yaml Example

```yaml
# Agent configuration
models:
  primary: gpt-4o-mini
  fallback: gpt-3.5-turbo
  judge: gpt-4o

agents:
  classifier:
    temperature: 0.3
    max_tokens: 500
    system_prompt: "You are a classifier..."

  responder:
    temperature: 0.7
    max_tokens: 1500
    system_prompt: "You are a helpful assistant..."

  evaluator:
    temperature: 0.1
    max_tokens: 100

settings:
  retry_count: 3
  timeout_seconds: 30
  batch_size: 10
```

### Accessing Configuration in Code

```python
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

classifier_temp = config["agents"]["classifier"]["temperature"]
```

## Aggregated Metrics

### Defining Summary Metrics

Use `custom_summary_metrics` to aggregate metrics across all traces in a run:

```python
from domino.agents.logging import DominoRun

aggregated_metrics = [
    ("classification_confidence", "mean"),
    ("impact_score", "median"),
    ("response_quality", "stdev"),
    ("processing_time", "max"),
    ("token_count", "min"),
]

with DominoRun(
    agent_config_path="config.yaml",
    custom_summary_metrics=aggregated_metrics
) as run:
    for item in batch:
        result = triage_incident(item)
```

### Aggregation Types

| Type | Description |
|------|-------------|
| `mean` | Average of all values |
| `median` | Middle value (50th percentile) |
| `stdev` | Standard deviation |
| `min` | Minimum value |
| `max` | Maximum value |

### How Aggregation Works

1. Each traced function logs individual metrics via evaluators
2. At run end, `DominoRun` aggregates metrics across all traces
3. Aggregated metrics appear in the run's metrics in Domino UI

Example:
```python
# If these traces occurred:
# Trace 1: response_quality = 0.8
# Trace 2: response_quality = 0.9
# Trace 3: response_quality = 0.85

# With aggregation: ("response_quality", "mean")
# Run metric: response_quality_mean = 0.85
```

## Complete Example with All Features

```python
import mlflow
from domino.agents.tracing import add_tracing
from domino.agents.logging import DominoRun
from openai import OpenAI

mlflow.openai.autolog()
client = OpenAI()

def quality_evaluator(inputs, output):
    return {
        "response_length": len(output.get("response", "")),
        "confidence": output.get("confidence", 0),
    }

@add_tracing(name="qa_agent", evaluator=quality_evaluator)
def qa_agent(question: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": question}]
    )
    return {
        "response": response.choices[0].message.content,
        "confidence": 0.9,
    }

# Define aggregations
aggregated_metrics = [
    ("response_length", "mean"),
    ("response_length", "max"),
    ("confidence", "mean"),
    ("confidence", "min"),
]

# Run with full configuration
with DominoRun(
    run_name="qa-evaluation-batch",
    agent_config_path="config.yaml",
    custom_summary_metrics=aggregated_metrics
) as run:
    questions = [
        "What is machine learning?",
        "How do neural networks work?",
        "What is deep learning?",
    ]

    for question in questions:
        result = qa_agent(question)
        print(f"Q: {question}")
        print(f"A: {result['response'][:100]}...")

    print(f"\nRun ID: {run.run_id}")
```

## Batch Processing Pattern

### Processing Large Datasets

```python
from domino.agents.logging import DominoRun

def process_batch(items, batch_name):
    aggregated_metrics = [
        ("accuracy", "mean"),
        ("latency", "mean"),
        ("error_count", "max"),
    ]

    with DominoRun(
        run_name=f"batch-{batch_name}",
        custom_summary_metrics=aggregated_metrics
    ) as run:
        results = []
        for item in items:
            try:
                result = process_item(item)
                results.append(result)
            except Exception as e:
                print(f"Error processing {item}: {e}")
        return results

# Process multiple batches
for i, batch in enumerate(batches):
    results = process_batch(batch, f"batch-{i}")
```

### Progress Tracking

```python
from tqdm import tqdm
from domino.agents.logging import DominoRun

with DominoRun(run_name="full-evaluation") as run:
    for item in tqdm(test_data, desc="Processing"):
        result = my_agent(item)
```

## Accessing Run Information

### During Run

```python
with DominoRun() as run:
    # Access run ID
    print(f"Run ID: {run.run_id}")

    # Access experiment info
    print(f"Experiment: {run.experiment_id}")

    result = my_agent(query)
```

### After Run

```python
import mlflow

# Get run by ID
run = mlflow.get_run(run_id)

# Access metrics
print(run.data.metrics)

# Access parameters (from config.yaml)
print(run.data.params)

# Access artifacts
artifacts = mlflow.artifacts.list_artifacts(run_id)
```

## Multiple Runs Comparison

### Sequential Runs

```python
run_ids = []

for config_version in ["v1", "v2", "v3"]:
    with DominoRun(run_name=f"config-{config_version}") as run:
        for item in test_data:
            result = my_agent(item, config=config_version)
        run_ids.append(run.run_id)

# Compare runs
import mlflow
runs = mlflow.search_runs(run_ids=run_ids)
print(runs[["run_id", "metrics.accuracy_mean"]])
```

### A/B Testing Pattern

```python
from domino.agents.logging import DominoRun

def run_ab_test(test_data, model_a, model_b):
    results = {}

    # Test Model A
    with DominoRun(run_name=f"ab-test-model-a") as run_a:
        for item in test_data:
            result = agent_with_model(item, model_a)
        results["model_a"] = run_a.run_id

    # Test Model B
    with DominoRun(run_name=f"ab-test-model-b") as run_b:
        for item in test_data:
            result = agent_with_model(item, model_b)
        results["model_b"] = run_b.run_id

    return results
```

## Error Handling

### Graceful Error Handling

```python
from domino.agents.logging import DominoRun

with DominoRun() as run:
    for item in data:
        try:
            result = my_agent(item)
        except Exception as e:
            # Error is logged in trace
            print(f"Error: {e}")
            continue  # Continue with next item
```

### Run-Level Error Tracking

```python
from domino.agents.logging import DominoRun
import mlflow

with DominoRun() as run:
    error_count = 0
    for item in data:
        try:
            result = my_agent(item)
        except Exception as e:
            error_count += 1

    # Log run-level metric
    mlflow.log_metric("total_errors", error_count)
```

## Best Practices

### 1. Use Descriptive Run Names

```python
# Good
with DominoRun(run_name="customer-support-eval-2024-01-15"):
with DominoRun(run_name="model-comparison-gpt4-vs-claude"):

# Bad
with DominoRun(run_name="test"):
with DominoRun():  # No name at all
```

### 2. Match Aggregation to Evaluator Metrics

```python
# Evaluator returns these metrics
def evaluator(inputs, output):
    return {
        "accuracy": 0.9,
        "latency_ms": 150,
    }

# Aggregations should match
aggregated_metrics = [
    ("accuracy", "mean"),      # Matches "accuracy"
    ("latency_ms", "mean"),    # Matches "latency_ms"
]
```

### 3. Use Config Files for Reproducibility

```python
# Always log configuration
with DominoRun(agent_config_path="config.yaml") as run:
    pass

# Now you can reproduce any run by checking its parameters
```

### 4. Keep Runs Focused

```python
# Good: One run per evaluation type
with DominoRun(run_name="accuracy-evaluation"):
    evaluate_accuracy(data)

with DominoRun(run_name="latency-evaluation"):
    evaluate_latency(data)

# Bad: Everything in one run
with DominoRun():
    evaluate_accuracy(data)
    evaluate_latency(data)
    do_other_stuff()
```

## Next Steps

- [EVALUATORS.md](./EVALUATORS.md) - Create custom evaluators
- [MULTI-AGENT-EXAMPLE.md](./MULTI-AGENT-EXAMPLE.md) - Complete example



### Evaluators

# GenAI Evaluators Guide

Evaluators are functions that score the outputs of traced functions. They enable quality measurement, comparison, and monitoring of GenAI applications.

## Evaluator Function Signature

```python
def evaluator(inputs: dict, output: Any) -> dict:
    """
    Args:
        inputs: Dictionary of argument names to values passed to the traced function
        output: Return value of the traced function

    Returns:
        Dictionary of metric names to numeric values
    """
    return {"metric_name": score}
```

## Basic Evaluators

### Simple Length-Based

```python
def length_evaluator(inputs, output):
    """Evaluate based on response length."""
    if isinstance(output, str):
        length = len(output)
    elif isinstance(output, dict):
        length = len(str(output))
    else:
        length = 0

    return {
        "response_length": length,
        "is_substantial": 1.0 if length > 100 else 0.0,
    }
```

### Keyword Presence

```python
def keyword_evaluator(inputs, output):
    """Check for important keywords in response."""
    keywords = ["machine learning", "neural network", "algorithm"]
    output_lower = str(output).lower()

    matches = sum(1 for kw in keywords if kw in output_lower)

    return {
        "keyword_count": matches,
        "keyword_coverage": matches / len(keywords),
    }
```

### Confidence Extraction

```python
def confidence_evaluator(inputs, output):
    """Extract confidence from structured output."""
    if isinstance(output, dict):
        confidence = output.get("confidence", 0)
        category = output.get("category", "unknown")
    else:
        confidence = 0
        category = "unknown"

    return {
        "confidence": confidence,
        "has_category": 1.0 if category != "unknown" else 0.0,
    }
```

## LLM-as-Judge Evaluators

### Basic LLM Judge

```python
from openai import OpenAI

client = OpenAI()

def llm_judge_evaluator(inputs, output):
    """Use GPT to evaluate response quality."""
    judge_prompt = f"""
    Rate the following response on a scale of 0-10.

    Question: {inputs.get('query', 'N/A')}
    Response: {output}

    Consider:
    - Relevance to the question
    - Completeness of answer
    - Clarity of explanation

    Respond with only a number 0-10.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": judge_prompt}],
        max_tokens=10,
        temperature=0.1,
    )

    try:
        score = float(response.choices[0].message.content.strip())
        score = max(0, min(10, score)) / 10  # Normalize to 0-1
    except:
        score = 0.5  # Default if parsing fails

    return {"llm_judge_score": score}
```

### Multi-Criteria LLM Judge

```python
import json

def multi_criteria_judge(inputs, output):
    """Evaluate multiple dimensions with LLM."""
    judge_prompt = f"""
    Evaluate this response on multiple criteria.

    Question: {inputs.get('query', 'N/A')}
    Response: {output}

    Rate each criterion 0-10:
    1. relevance: How relevant is the response to the question?
    2. completeness: How complete is the answer?
    3. accuracy: How accurate is the information?
    4. clarity: How clear is the explanation?

    Respond in JSON format:
    {{"relevance": X, "completeness": X, "accuracy": X, "clarity": X}}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": judge_prompt}],
        max_tokens=100,
        temperature=0.1,
    )

    try:
        scores = json.loads(response.choices[0].message.content)
        # Normalize to 0-1
        return {k: v / 10.0 for k, v in scores.items()}
    except:
        return {
            "relevance": 0.5,
            "completeness": 0.5,
            "accuracy": 0.5,
            "clarity": 0.5,
        }
```

### Pairwise Comparison Judge

```python
def pairwise_judge(inputs, output, baseline_output):
    """Compare output against a baseline."""
    judge_prompt = f"""
    Compare these two responses to the question.

    Question: {inputs.get('query', 'N/A')}

    Response A (Baseline): {baseline_output}
    Response B (New): {output}

    Which response is better? Consider relevance, completeness, and clarity.

    Respond with:
    - "A" if baseline is better
    - "B" if new is better
    - "TIE" if equal
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": judge_prompt}],
        max_tokens=10,
        temperature=0.1,
    )

    verdict = response.choices[0].message.content.strip().upper()

    return {
        "wins_vs_baseline": 1.0 if verdict == "B" else 0.0,
        "ties_vs_baseline": 1.0 if verdict == "TIE" else 0.0,
        "loses_vs_baseline": 1.0 if verdict == "A" else 0.0,
    }
```

## Domain-Specific Evaluators

### Classification Evaluator

```python
def classification_evaluator(inputs, output):
    """Evaluate classification results."""
    expected_categories = ["bug", "feature", "question", "other"]

    if isinstance(output, dict):
        category = output.get("category", "")
        confidence = output.get("confidence", 0)
    else:
        category = str(output)
        confidence = 0

    return {
        "is_valid_category": 1.0 if category in expected_categories else 0.0,
        "classification_confidence": confidence,
        "high_confidence": 1.0 if confidence > 0.8 else 0.0,
    }
```

### RAG Evaluator

```python
def rag_evaluator(inputs, output):
    """Evaluate RAG (Retrieval-Augmented Generation) responses."""
    query = inputs.get("query", "")
    context = inputs.get("context", "")

    if isinstance(output, dict):
        answer = output.get("answer", "")
        sources = output.get("sources", [])
    else:
        answer = str(output)
        sources = []

    # Check if answer uses context
    context_words = set(context.lower().split())
    answer_words = set(answer.lower().split())
    context_overlap = len(context_words & answer_words) / max(len(context_words), 1)

    return {
        "context_utilization": context_overlap,
        "source_count": len(sources),
        "has_sources": 1.0 if sources else 0.0,
        "answer_length": len(answer),
    }
```

### Safety Evaluator

```python
def safety_evaluator(inputs, output):
    """Check for safety issues in output."""
    output_str = str(output).lower()

    # Simple keyword-based safety check
    unsafe_patterns = [
        "i cannot", "i'm not able to", "harmful", "illegal",
        "violence", "hate", "discriminat"
    ]

    safety_flags = sum(1 for p in unsafe_patterns if p in output_str)

    return {
        "safety_flag_count": safety_flags,
        "is_safe": 1.0 if safety_flags == 0 else 0.0,
    }
```

## Composite Evaluators

### Combining Multiple Evaluators

```python
def composite_evaluator(inputs, output):
    """Combine multiple evaluation methods."""
    scores = {}

    # Length metrics
    scores.update(length_evaluator(inputs, output))

    # Safety metrics
    scores.update(safety_evaluator(inputs, output))

    # LLM judge metrics
    scores.update(llm_judge_evaluator(inputs, output))

    # Compute overall score
    scores["overall_score"] = (
        scores.get("llm_judge_score", 0) * 0.5 +
        scores.get("is_safe", 1) * 0.3 +
        min(scores.get("response_length", 0) / 500, 1.0) * 0.2
    )

    return scores
```

### Conditional Evaluator

```python
def conditional_evaluator(inputs, output):
    """Apply different evaluation based on input type."""
    query_type = inputs.get("query_type", "general")

    base_scores = {
        "response_length": len(str(output)),
    }

    if query_type == "classification":
        base_scores.update(classification_evaluator(inputs, output))
    elif query_type == "qa":
        base_scores.update(llm_judge_evaluator(inputs, output))
    elif query_type == "rag":
        base_scores.update(rag_evaluator(inputs, output))

    return base_scores
```

## Post-Hoc Evaluation

### Adding Evaluations to Existing Traces

```python
from domino.agents.tracing import search_traces, log_evaluation

def add_post_hoc_evaluations(run_id):
    """Add evaluations to traces after the fact."""
    # Retrieve traces from run
    traces = search_traces(run_id=run_id)

    for trace in traces.data:
        # Get trace inputs and outputs
        inputs = trace.inputs
        output = trace.outputs

        # Calculate new evaluation
        combined_score = calculate_combined_score(inputs, output)

        # Log evaluation to existing trace
        log_evaluation(
            trace_id=trace.id,
            name="combined_quality_score",
            value=round(combined_score, 2)
        )

# Usage after a run completes
add_post_hoc_evaluations(run_id="abc123")
```

### Human-in-the-Loop Evaluation

```python
from domino.agents.tracing import search_traces, log_evaluation

def collect_human_feedback(run_id):
    """Collect human feedback for traces."""
    traces = search_traces(run_id=run_id)

    for trace in traces.data:
        # Display to human reviewer
        print(f"Input: {trace.inputs}")
        print(f"Output: {trace.outputs}")

        # Collect feedback
        rating = input("Rate 1-5: ")

        # Log human evaluation
        log_evaluation(
            trace_id=trace.id,
            name="human_rating",
            value=float(rating) / 5.0
        )
```

## Evaluator Patterns

### Factory Pattern

```python
def create_threshold_evaluator(threshold: float):
    """Create evaluator with custom threshold."""
    def evaluator(inputs, output):
        confidence = output.get("confidence", 0) if isinstance(output, dict) else 0
        return {
            "meets_threshold": 1.0 if confidence >= threshold else 0.0,
            "confidence": confidence,
        }
    return evaluator

# Usage
high_confidence_evaluator = create_threshold_evaluator(0.9)
medium_confidence_evaluator = create_threshold_evaluator(0.7)

@add_tracing(name="agent", evaluator=high_confidence_evaluator)
def my_agent(query):
    pass
```

### Caching Pattern for Expensive Evaluations

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def cached_llm_judge(query: str, output: str) -> float:
    """Cache LLM judge results to avoid redundant calls."""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": f"Rate 0-10: {query} -> {output}"}],
        max_tokens=10,
    )
    return float(response.choices[0].message.content.strip()) / 10

def efficient_evaluator(inputs, output):
    query = inputs.get("query", "")
    output_str = str(output)

    # Use cached evaluation
    score = cached_llm_judge(query, output_str)

    return {"quality_score": score}
```

## Best Practices

### 1. Return Consistent Metrics

```python
# Good: Always return same metrics
def consistent_evaluator(inputs, output):
    return {
        "quality": calculate_quality(output),
        "relevance": calculate_relevance(inputs, output),
    }

# Bad: Different metrics based on condition
def inconsistent_evaluator(inputs, output):
    if condition:
        return {"quality": 1.0}
    else:
        return {"relevance": 0.5}  # Different metric!
```

### 2. Handle Edge Cases

```python
def robust_evaluator(inputs, output):
    try:
        if output is None:
            return {"quality": 0.0, "error": 1.0}

        if isinstance(output, dict):
            text = output.get("response", "")
        else:
            text = str(output)

        return {
            "quality": calculate_quality(text),
            "error": 0.0,
        }
    except Exception as e:
        return {"quality": 0.0, "error": 1.0}
```

### 3. Keep Evaluators Fast

```python
# Good: Fast local evaluation
def fast_evaluator(inputs, output):
    return {"length": len(str(output))}

# Use sparingly: Slow LLM evaluation
def slow_evaluator(inputs, output):
    # Only for critical metrics
    return {"llm_score": expensive_llm_call(output)}
```

### 4. Document Expected Metrics

```python
def documented_evaluator(inputs, output):
    """
    Evaluates agent responses.

    Returns:
        quality_score (float): 0-1 overall quality
        relevance (float): 0-1 relevance to query
        completeness (float): 0-1 answer completeness
        is_safe (float): 1.0 if safe, 0.0 if unsafe
    """
    return {
        "quality_score": ...,
        "relevance": ...,
        "completeness": ...,
        "is_safe": ...,
    }
```

## Next Steps

- [MULTI-AGENT-EXAMPLE.md](./MULTI-AGENT-EXAMPLE.md) - See evaluators in action



### Multi Agent Example

# Multi-Agent Tracing Example

This is a complete, production-ready example of a multi-agent system with full tracing, based on the Domino GenAI Tracing Blueprint.

## Incident Triage System Overview

This example implements an incident triage system with four specialized agents:

1. **Classifier Agent** - Categorizes incidents and assigns urgency
2. **Impact Agent** - Assesses blast radius and affected users
3. **Resource Agent** - Matches available responders based on skills
4. **Response Agent** - Drafts communications for stakeholders

## Project Structure

```
incident-triage/
├── agents/
│   ├── __init__.py
│   ├── classifier.py
│   ├── impact.py
│   ├── resource.py
│   └── response.py
├── evaluators/
│   ├── __init__.py
│   └── pipeline_evaluator.py
├── config.yaml
├── main.py
└── requirements.txt
```

## Configuration

### config.yaml

```yaml
models:
  primary: gpt-4o-mini
  fallback: gpt-3.5-turbo

agents:
  classifier:
    temperature: 0.3
    max_tokens: 500
    categories:
      - security
      - infrastructure
      - application
      - data
      - network
    urgency_levels:
      - critical
      - high
      - medium
      - low

  impact:
    temperature: 0.3
    max_tokens: 800

  resource:
    temperature: 0.5
    max_tokens: 600

  response:
    temperature: 0.7
    max_tokens: 1500

settings:
  retry_count: 3
  timeout_seconds: 30
```

## Agent Implementations

### agents/classifier.py

```python
import mlflow
from domino.agents.tracing import add_tracing
from openai import OpenAI
import yaml

mlflow.openai.autolog()
client = OpenAI()

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def classifier_evaluator(inputs, output):
    """Evaluate classification quality."""
    valid_categories = config["agents"]["classifier"]["categories"]
    valid_urgencies = config["agents"]["classifier"]["urgency_levels"]

    category = output.get("category", "")
    urgency = output.get("urgency", "")
    confidence = output.get("confidence", 0)

    return {
        "classification_confidence": confidence,
        "valid_category": 1.0 if category in valid_categories else 0.0,
        "valid_urgency": 1.0 if urgency in valid_urgencies else 0.0,
        "high_confidence": 1.0 if confidence > 0.8 else 0.0,
    }

@add_tracing(name="classifier_agent", evaluator=classifier_evaluator)
def classify_incident(incident: dict) -> dict:
    """
    Categorize incident and assign urgency level.

    Args:
        incident: Dict with 'title', 'description', 'source'

    Returns:
        Dict with 'category', 'urgency', 'confidence', 'reasoning'
    """
    categories = config["agents"]["classifier"]["categories"]
    urgencies = config["agents"]["classifier"]["urgency_levels"]

    prompt = f"""
    Classify this incident:

    Title: {incident.get('title', 'N/A')}
    Description: {incident.get('description', 'N/A')}
    Source: {incident.get('source', 'N/A')}

    Categories: {', '.join(categories)}
    Urgency Levels: {', '.join(urgencies)}

    Respond in JSON format:
    {{
        "category": "<category>",
        "urgency": "<urgency>",
        "confidence": <0.0-1.0>,
        "reasoning": "<brief explanation>"
    }}
    """

    response = client.chat.completions.create(
        model=config["models"]["primary"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["agents"]["classifier"]["temperature"],
        max_tokens=config["agents"]["classifier"]["max_tokens"],
    )

    import json
    result = json.loads(response.choices[0].message.content)
    return result
```

### agents/impact.py

```python
import mlflow
from domino.agents.tracing import add_tracing
from openai import OpenAI
import yaml
import json

mlflow.openai.autolog()
client = OpenAI()

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def impact_evaluator(inputs, output):
    """Evaluate impact assessment quality."""
    return {
        "impact_score": output.get("score", 0),
        "has_affected_users": 1.0 if output.get("affected_users", 0) > 0 else 0.0,
        "has_financial_estimate": 1.0 if output.get("financial_exposure") else 0.0,
    }

@add_tracing(name="impact_agent", evaluator=impact_evaluator)
def assess_impact(incident: dict, classification: dict) -> dict:
    """
    Evaluate blast radius, affected users, financial exposure.

    Args:
        incident: Original incident data
        classification: Output from classifier agent

    Returns:
        Dict with 'score', 'affected_users', 'affected_systems',
        'financial_exposure', 'reasoning'
    """
    prompt = f"""
    Assess the impact of this {classification['category']} incident:

    Title: {incident.get('title', 'N/A')}
    Description: {incident.get('description', 'N/A')}
    Urgency: {classification['urgency']}

    Estimate:
    1. Impact score (0-10)
    2. Number of affected users
    3. Affected systems
    4. Potential financial exposure

    Respond in JSON format:
    {{
        "score": <0-10>,
        "affected_users": <number>,
        "affected_systems": ["<system1>", "<system2>"],
        "financial_exposure": "<estimate or 'unknown'>",
        "reasoning": "<brief explanation>"
    }}
    """

    response = client.chat.completions.create(
        model=config["models"]["primary"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["agents"]["impact"]["temperature"],
        max_tokens=config["agents"]["impact"]["max_tokens"],
    )

    result = json.loads(response.choices[0].message.content)
    return result
```

### agents/resource.py

```python
import mlflow
from domino.agents.tracing import add_tracing
from openai import OpenAI
import yaml
import json

mlflow.openai.autolog()
client = OpenAI()

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def resource_evaluator(inputs, output):
    """Evaluate resource matching quality."""
    return {
        "responder_count": len(output.get("responders", [])),
        "has_eta": 1.0 if output.get("eta") else 0.0,
        "meets_sla": 1.0 if output.get("meets_sla", False) else 0.0,
    }

@add_tracing(name="resource_agent", evaluator=resource_evaluator)
def match_resources(
    incident: dict,
    classification: dict,
    impact: dict
) -> dict:
    """
    Identify available responders based on skills and SLA.

    Args:
        incident: Original incident data
        classification: Output from classifier agent
        impact: Output from impact agent

    Returns:
        Dict with 'responders', 'eta', 'meets_sla', 'escalation_path'
    """
    prompt = f"""
    Find appropriate responders for this incident:

    Category: {classification['category']}
    Urgency: {classification['urgency']}
    Impact Score: {impact['score']}
    Affected Systems: {impact.get('affected_systems', [])}

    Determine:
    1. Required skills
    2. Recommended responders (by role)
    3. Estimated time to respond
    4. Escalation path if needed

    Respond in JSON format:
    {{
        "required_skills": ["<skill1>", "<skill2>"],
        "responders": [
            {{"role": "<role>", "priority": <1-3>}}
        ],
        "eta": "<time estimate>",
        "meets_sla": <true/false>,
        "escalation_path": ["<level1>", "<level2>"]
    }}
    """

    response = client.chat.completions.create(
        model=config["models"]["primary"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["agents"]["resource"]["temperature"],
        max_tokens=config["agents"]["resource"]["max_tokens"],
    )

    result = json.loads(response.choices[0].message.content)
    return result
```

### agents/response.py

```python
import mlflow
from domino.agents.tracing import add_tracing
from openai import OpenAI
import yaml
import json

mlflow.openai.autolog()
client = OpenAI()

with open("config.yaml") as f:
    config = yaml.safe_load(f)

def response_evaluator(inputs, output):
    """Evaluate response draft quality."""
    message = output.get("message", "")
    return {
        "response_length": len(message),
        "has_all_audiences": 1.0 if len(output.get("audiences", [])) >= 2 else 0.0,
        "has_action_items": 1.0 if output.get("action_items") else 0.0,
    }

@add_tracing(name="response_agent", evaluator=response_evaluator)
def draft_response(
    incident: dict,
    classification: dict,
    impact: dict,
    resources: dict
) -> dict:
    """
    Generate communications for stakeholders.

    Args:
        incident: Original incident data
        classification: Output from classifier agent
        impact: Output from impact agent
        resources: Output from resource agent

    Returns:
        Dict with 'message', 'audiences', 'action_items', 'follow_up_time'
    """
    prompt = f"""
    Draft an incident response communication:

    Incident: {incident.get('title', 'N/A')}
    Category: {classification['category']}
    Urgency: {classification['urgency']}
    Impact Score: {impact['score']}
    Affected Users: {impact.get('affected_users', 'Unknown')}
    ETA: {resources.get('eta', 'Unknown')}

    Create:
    1. A clear, professional message
    2. Identify all audiences who need to be notified
    3. List action items
    4. Suggest follow-up time

    Respond in JSON format:
    {{
        "message": "<the communication message>",
        "audiences": ["<audience1>", "<audience2>"],
        "action_items": ["<action1>", "<action2>"],
        "follow_up_time": "<time>"
    }}
    """

    response = client.chat.completions.create(
        model=config["models"]["primary"],
        messages=[{"role": "user", "content": prompt}],
        temperature=config["agents"]["response"]["temperature"],
        max_tokens=config["agents"]["response"]["max_tokens"],
    )

    result = json.loads(response.choices[0].message.content)
    return result
```

## Pipeline with Tracing

### evaluators/pipeline_evaluator.py

```python
def pipeline_evaluator(inputs, output):
    """
    Evaluate the full pipeline output.

    This evaluator runs after all agents complete and scores
    the final result.
    """
    scores = {}

    # Classification quality
    classification = output.get("classification", {})
    scores["classification_confidence"] = classification.get("confidence", 0)

    # Impact assessment
    impact = output.get("impact", {})
    scores["impact_score"] = impact.get("score", 0) / 10.0  # Normalize to 0-1

    # Resource matching
    resources = output.get("resources", {})
    scores["resource_coverage"] = min(len(resources.get("responders", [])) / 3, 1.0)
    scores["meets_sla"] = 1.0 if resources.get("meets_sla", False) else 0.0

    # Response quality
    response = output.get("response", {})
    scores["response_completeness"] = (
        (1.0 if response.get("message") else 0.0) * 0.4 +
        (min(len(response.get("audiences", [])) / 2, 1.0)) * 0.3 +
        (min(len(response.get("action_items", [])) / 3, 1.0)) * 0.3
    )

    # Overall quality
    scores["overall_quality"] = (
        scores["classification_confidence"] * 0.25 +
        scores["impact_score"] * 0.25 +
        scores["resource_coverage"] * 0.25 +
        scores["response_completeness"] * 0.25
    )

    return scores
```

### main.py

```python
import mlflow
from domino.agents.tracing import add_tracing
from domino.agents.logging import DominoRun

from agents.classifier import classify_incident
from agents.impact import assess_impact
from agents.resource import match_resources
from agents.response import draft_response
from evaluators.pipeline_evaluator import pipeline_evaluator

# Enable auto-tracing
mlflow.openai.autolog()

@add_tracing(name="triage_pipeline", evaluator=pipeline_evaluator)
def triage_incident(incident: dict) -> dict:
    """
    Full incident triage pipeline.

    Orchestrates all agents and returns complete triage result.
    """
    # Step 1: Classify
    classification = classify_incident(incident)

    # Step 2: Assess Impact
    impact = assess_impact(incident, classification)

    # Step 3: Match Resources
    resources = match_resources(incident, classification, impact)

    # Step 4: Draft Response
    response = draft_response(incident, classification, impact, resources)

    return {
        "incident_id": incident.get("id"),
        "classification": classification,
        "impact": impact,
        "resources": resources,
        "response": response,
    }


def main():
    # Define aggregated metrics for the run
    aggregated_metrics = [
        ("classification_confidence", "mean"),
        ("classification_confidence", "min"),
        ("impact_score", "median"),
        ("meets_sla", "mean"),
        ("overall_quality", "mean"),
        ("overall_quality", "stdev"),
    ]

    # Sample incidents for testing
    test_incidents = [
        {
            "id": "INC-001",
            "title": "Database connection failures",
            "description": "Multiple users reporting inability to access the main application. Database logs show connection pool exhaustion.",
            "source": "monitoring-alert",
        },
        {
            "id": "INC-002",
            "title": "Suspicious login attempts detected",
            "description": "Security system flagged unusual login patterns from multiple IPs targeting admin accounts.",
            "source": "security-siem",
        },
        {
            "id": "INC-003",
            "title": "API response times degraded",
            "description": "Customer-facing API endpoints showing 5x normal latency. No errors, just slow responses.",
            "source": "apm-alert",
        },
    ]

    # Run with full tracing
    with DominoRun(
        run_name="incident-triage-evaluation",
        agent_config_path="config.yaml",
        custom_summary_metrics=aggregated_metrics
    ) as run:
        results = []

        for incident in test_incidents:
            print(f"\nProcessing: {incident['id']} - {incident['title']}")

            result = triage_incident(incident)
            results.append(result)

            # Print summary
            print(f"  Category: {result['classification']['category']}")
            print(f"  Urgency: {result['classification']['urgency']}")
            print(f"  Impact: {result['impact']['score']}/10")
            print(f"  SLA Met: {result['resources']['meets_sla']}")

        print(f"\n{'='*50}")
        print(f"Run completed: {run.run_id}")
        print(f"Processed {len(results)} incidents")

    return results


if __name__ == "__main__":
    main()
```

## Viewing Results in Domino

### Navigate to Traces

1. Go to your Domino project
2. Click **Experiments** in the sidebar
3. Find experiment: `tracing-{your-username}`
4. Click on the run: `incident-triage-evaluation`
5. View the **Traces** tab

### Trace Hierarchy

```
triage_pipeline (INC-001)
├── classifier_agent
│   └── [OpenAI gpt-4o-mini call]
├── impact_agent
│   └── [OpenAI gpt-4o-mini call]
├── resource_agent
│   └── [OpenAI gpt-4o-mini call]
└── response_agent
    └── [OpenAI gpt-4o-mini call]
```

### Aggregated Metrics

The run's metrics page shows:
- `classification_confidence_mean`
- `classification_confidence_min`
- `impact_score_median`
- `meets_sla_mean`
- `overall_quality_mean`
- `overall_quality_stdev`

## requirements.txt

```text
mlflow==3.2.0
dominodatalab[data,aisystems] @ git+https://github.com/dominodatalab/python-domino.git@master
openai>=1.0.0
pyyaml>=6.0
```

## Blueprint Reference

Full implementation available at:
https://github.com/dominodatalab/GenAI-Tracing-Tutorial



### Tracing Setup

# GenAI Tracing Setup for Domino

This guide covers setting up the environment and SDK for GenAI tracing in Domino Data Lab.

## Environment Requirements

### Compute Environment Setup

**IMPORTANT**: Domino Standard Environments (DSEs) include an older MLflow version. You must create a custom environment with MLflow 3.2.0 for GenAI tracing.

Add to your Dockerfile:

```dockerfile
USER root

# Install MLflow 3.2.0 (required for GenAI tracing)
RUN pip install mlflow==3.2.0

# Install Domino SDK with AI systems support
RUN pip install --no-cache-dir "git+https://github.com/dominodatalab/python-domino.git@master#egg=dominodatalab[data,aisystems]"

# Install your LLM framework (choose one or more)
RUN pip install openai>=1.0.0
RUN pip install anthropic>=0.18.0
RUN pip install langchain>=0.1.0

USER ubuntu
```

### Requirements File Alternative

```text
# requirements.txt
mlflow==3.2.0
dominodatalab[data,aisystems] @ git+https://github.com/dominodatalab/python-domino.git@master
openai>=1.0.0
anthropic>=0.18.0
langchain>=0.1.0
```

## Framework Auto-Logging

Enable auto-tracing for your LLM framework before making any calls:

### OpenAI

```python
import mlflow

# Enable OpenAI auto-tracing
mlflow.openai.autolog()

# Now all OpenAI calls are automatically traced
from openai import OpenAI
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Anthropic

```python
import mlflow

# Enable Anthropic auto-tracing
mlflow.anthropic.autolog()

# Now all Anthropic calls are automatically traced
from anthropic import Anthropic
client = Anthropic()

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### LangChain

```python
import mlflow

# Enable LangChain auto-tracing
mlflow.langchain.autolog()

# Now all LangChain operations are traced
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

llm = ChatOpenAI(model="gpt-4o-mini")
prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
chain = prompt | llm

response = chain.invoke({"topic": "machine learning"})
```

### Multiple Frameworks

```python
import mlflow

# Enable auto-tracing for multiple frameworks
mlflow.openai.autolog()
mlflow.anthropic.autolog()
mlflow.langchain.autolog()
```

## Verifying Setup

### Check MLflow Version

```python
import mlflow
print(f"MLflow version: {mlflow.__version__}")
# Should print: MLflow version: 3.2.0
```

### Check Domino SDK

```python
from domino.agents.tracing import add_tracing
from domino.agents.logging import DominoRun
print("Domino SDK with agents support installed successfully")
```

### Test Basic Tracing

```python
from domino.agents.tracing import add_tracing
from domino.agents.logging import DominoRun

@add_tracing(name="test_agent", autolog_frameworks=["openai"])
def test_agent(query: str) -> str:
    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}]
    )
    return response.choices[0].message.content

with DominoRun() as run:
    result = test_agent("Say hello")
    print(f"Result: {result}")
    print(f"Run ID: {run.run_id}")
```

**Note:** The `autolog_frameworks` parameter in `@add_tracing` enables automatic tracing for the specified frameworks (e.g., `["openai"]`, `["langchain"]`, `["openai", "langchain"]`).

## Environment Variables

### API Keys

Store API keys as Domino environment variables (never in code):

```python
import os

# Access in your code
openai_key = os.environ.get("OPENAI_API_KEY")
anthropic_key = os.environ.get("ANTHROPIC_API_KEY")
```

### Domino-Provided Variables

These are automatically available:

| Variable | Description |
|----------|-------------|
| `DOMINO_STARTING_USERNAME` | User who started the run |
| `DOMINO_PROJECT_NAME` | Current project name |
| `DOMINO_RUN_ID` | Domino job run ID |
| `MLFLOW_TRACKING_URI` | MLflow tracking server URL |

## Project Structure

Recommended structure for GenAI projects:

```
my-agent-project/
├── agents/
│   ├── __init__.py
│   ├── classifier.py      # Classification agent
│   ├── responder.py       # Response generation agent
│   └── evaluators.py      # Custom evaluators
├── config/
│   └── config.yaml        # Agent configuration
├── main.py                # Entry point with DominoRun
├── requirements.txt
└── Dockerfile             # Custom environment
```

## Troubleshooting Setup

### MLflow Version Mismatch

```
Error: module 'mlflow' has no attribute 'openai'
```

**Solution**: Upgrade MLflow to 3.2.0:
```bash
pip install mlflow==3.2.0
```

### Domino SDK Import Error

```
ModuleNotFoundError: No module named 'domino.agents'
```

**Solution**: Install Domino SDK with AI systems support:
```bash
pip install --no-cache-dir "git+https://github.com/dominodatalab/python-domino.git@master#egg=dominodatalab[data,aisystems]"
```

### Traces Not Appearing

1. Verify MLflow tracking URI is set (automatic in Domino)
2. Check experiment name matches expected format
3. Ensure `DominoRun` context manager is used
4. Verify auto-logging is enabled before LLM calls

### API Key Issues

```
openai.AuthenticationError: Incorrect API key provided
```

**Solution**: Set API keys in Domino environment variables, not in code.

## Next Steps

- [ADD-TRACING-DECORATOR.md](./ADD-TRACING-DECORATOR.md) - Learn about @add_tracing
- [DOMINO-RUN.md](./DOMINO-RUN.md) - Learn about DominoRun context
- [MULTI-AGENT-EXAMPLE.md](./MULTI-AGENT-EXAMPLE.md) - See complete example

