---
name: domino-domino-data-sdk
description: Use the domino-data Python SDK (dominodatalab-data) for programmatic
  data access in Domino. Covers DataSourceClient for SQL queries and object storage,
  DatasetClient for dataset files, TrainingSets for ML data versioning, Feature Store,
  and VectorDB (Pinecone) integration. Use when querying data sources, downloading
  datasets, managing training sets, or working with vector databases in Domino.
version: 1.0.0
author: Domino Data Lab / Tolu
tags:
- domino
- mlops
- data-access
- sdk
trigger_patterns:
- domino data sdk
- domino-data-sdk
- access domino data
---

# Domino Data SDK Skill

This skill provides comprehensive knowledge for working with the `domino-data` Python SDK (`dominodatalab-data`) - the official library for Domino's Access Data features.

## Installation

```bash
# Via pip
pip install -U dominodatalab-data

# Via Poetry
poetry add dominodatalab-data

# In Domino environment (requirements.txt)
dominodatalab-data>=6.0.0
```

## Key Components

| Module | Purpose |
|--------|---------|
| `DataSourceClient` | Query SQL databases and access object stores |
| `DatasetClient` | Read files from Domino Datasets |
| `TrainingSets` | Version and manage ML training data |
| `Feature Store` | Manage ML features with Git integration |
| `VectorDB` | Pinecone vector database integration |

## Related Documentation

- [DATA-SOURCES.md](./DATA-SOURCES.md) - SQL queries and object storage
- [DATASETS.md](./DATASETS.md) - Dataset file operations
- [TRAINING-SETS.md](./TRAINING-SETS.md) - Training data versioning
- [VECTORDB.md](./VECTORDB.md) - Pinecone integration

## Quick Start

### Query a Data Source

```python
from domino_data.data_sources import DataSourceClient

# Initialize client (auto-configured in Domino)
client = DataSourceClient()

# Get a data source by name
ds = client.get_datasource("my-redshift-db")

# Execute SQL query
result = ds.query("SELECT * FROM customers WHERE region = 'US'")

# Convert to pandas DataFrame
df = result.to_pandas()

# Or save to parquet
result.to_parquet("output.parquet")
```

### Access Object Storage

```python
from domino_data.data_sources import DataSourceClient

client = DataSourceClient()
ds = client.get_datasource("my-s3-bucket")

# List objects
objects = ds.list_objects(prefix="data/", page_size=100)

# Download a file
ds.download_file("data/input.csv", "local_input.csv")

# Upload a file
ds.put("data/output.csv", open("results.csv", "rb").read())

# Get signed URL
url = ds.get_key_url("data/file.csv", is_read_write=False)
```

### Read from Datasets

```python
from domino_data.datasets import DatasetClient

client = DatasetClient()

# Get dataset by name
dataset = client.get_dataset("training-data")

# List files
files = dataset.list_files(prefix="images/")

# Download file
dataset.download("model.pkl", "local_model.pkl", max_workers=4)

# Get file content as bytes
content = dataset.get("config.json")
```

### Training Sets

```python
from domino_data.training_sets import (
    create_training_set_version,
    get_training_set,
    list_training_sets
)
import pandas as pd

# Create training set version from DataFrame
df = pd.DataFrame({
    "id": [1, 2, 3],
    "feature_a": [0.1, 0.2, 0.3],
    "label": [1, 0, 1]
})

version = create_training_set_version(
    training_set_name="customer-churn",
    df=df,
    key_columns=["id"],
    description="Initial training data"
)

# Get training set
ts = get_training_set("customer-churn")

# List all training sets
all_sets = list_training_sets()
```

### Vector Database (Pinecone)

```python
from domino_data.vectordb import (
    domino_pinecone3x_init_params,
    domino_pinecone3x_index_params
)
from pinecone import Pinecone

# Initialize Pinecone client with Domino credentials
init_params = domino_pinecone3x_init_params("my-pinecone-ds")
pc = Pinecone(**init_params)

# Get index parameters
index_params = domino_pinecone3x_index_params("my-pinecone-ds", "embeddings")
index = pc.Index(**index_params)

# Query vectors
results = index.query(
    vector=[0.1, 0.2, 0.3, ...],
    top_k=10,
    include_metadata=True
)
```

## Authentication

The library auto-configures authentication inside Domino workspaces and jobs:

```python
# Environment variables used automatically:
# DOMINO_USER_API_KEY - API key for authentication
# DOMINO_TOKEN_FILE - Token file location
# DOMINO_API_PROXY - API proxy URL
# DOMINO_DATA_API_GATEWAY - Data API gateway (default: http://127.0.0.1:8766)
```

For external use:

```python
import os
os.environ["DOMINO_USER_API_KEY"] = "your-api-key"
os.environ["DOMINO_API_HOST"] = "https://your-domino.com"

from domino_data.data_sources import DataSourceClient
client = DataSourceClient()
```

## Error Handling

```python
from domino_data.data_sources import DominoError, UnauthenticatedError

try:
    result = ds.query("SELECT * FROM table")
except UnauthenticatedError:
    print("Authentication failed - check API key")
except DominoError as e:
    print(f"Domino error: {e}")
```

## Best Practices

1. **Use within Domino**: Auth is automatic in workspaces/jobs
2. **Parallel downloads**: Use `max_workers` for large files
3. **Pagination**: Use `page_size` when listing many objects
4. **Training Sets**: Version your training data for reproducibility
5. **Connection reuse**: Reuse client instances when possible

## Package Info

- **PyPI**: `dominodatalab-data`
- **GitHub**: https://github.com/dominodatalab/domino-data
- **License**: Apache 2.0
- **Python**: 3.8+


---

## Reference Documentation


### Data Sources

# Domino Data Sources

The `DataSourceClient` provides access to configured data sources in Domino, including SQL databases and object stores.

## DataSourceClient

### Initialization

```python
from domino_data.data_sources import DataSourceClient

# Auto-configured inside Domino
client = DataSourceClient()
```

### Get Data Source

```python
# Fetch by name (as configured in Domino)
ds = client.get_datasource("my-data-source")

# Properties
print(ds.name)           # Data source name
print(ds.datasource_type) # Type (e.g., 'redshift', 's3')
print(ds.auth_type)      # Authentication type
print(ds.owner)          # Owner username
```

## Tabular Data Sources (SQL)

For SQL-queryable sources like Redshift, Snowflake, PostgreSQL:

### Execute Queries

```python
# Get tabular data source
ds = client.get_datasource("analytics-db")

# Execute SQL query
result = ds.query("""
    SELECT customer_id, revenue, region
    FROM sales
    WHERE date >= '2024-01-01'
    LIMIT 10000
""")

# Convert to pandas DataFrame
df = result.to_pandas()
print(df.head())

# Save directly to parquet
result.to_parquet("sales_data.parquet")
```

### Configuration Override

```python
from domino_data.data_sources import DatasourceConfig

# Override configuration for this session
config = DatasourceConfig(
    schema="production",
    warehouse="COMPUTE_WH"
)
ds.update(config)

# Query with new config
result = ds.query("SELECT * FROM users")

# Reset to default
ds.reset_config()
```

## Object Store Data Sources (S3, GCS, Azure Blob)

For object storage sources:

### List Objects

```python
ds = client.get_datasource("data-lake")

# List all objects
objects = ds.list_objects()

# List with prefix filter
objects = ds.list_objects(prefix="raw/2024/", page_size=500)

for obj in objects:
    print(obj.key)
```

### Download Files

```python
# Download single file
ds.download_file("data/input.csv", "local_input.csv")

# Get object and download with parallelism
obj = ds.Object("large-file.parquet")
obj.download("local_file.parquet", max_workers=8)

# Get content as bytes
content = ds.get("config.json")
data = json.loads(content)
```

### Upload Files

```python
# Upload bytes
ds.put("output/results.json", json.dumps(data).encode())

# Upload file
obj = ds.Object("output/model.pkl")
obj.upload_file("trained_model.pkl")
```

### Signed URLs

```python
# Get read-only signed URL
read_url = ds.get_key_url("data/file.csv", is_read_write=False)

# Get read-write signed URL
write_url = ds.get_key_url("output/file.csv", is_read_write=True)
```

## Object Operations

The `_Object` class represents individual objects:

```python
obj = ds.Object("path/to/file.csv")

# Get content
content = obj.get()

# Download to file
obj.download_file("local.csv")

# Download with parallelism (for large files)
obj.download("local.csv", max_workers=4)

# Upload content
obj.put(b"new content here")

# Upload from file
obj.upload_file("source.csv")

# Get HTTP client for custom operations
http_client = obj.http()
```

## Supported Data Source Types

| Type | Class | Operations |
|------|-------|------------|
| Redshift | TabularDatasource | SQL queries |
| Snowflake | TabularDatasource | SQL queries |
| PostgreSQL | TabularDatasource | SQL queries |
| MySQL | TabularDatasource | SQL queries |
| S3 | ObjectStoreDatasource | Object CRUD |
| GCS | ObjectStoreDatasource | Object CRUD |
| Azure Blob | ObjectStoreDatasource | Object CRUD |
| ADLS Gen2 | ObjectStoreDatasource | Object CRUD |

## Error Handling

```python
from domino_data.data_sources import (
    DominoError,
    UnauthenticatedError
)

try:
    result = ds.query("SELECT * FROM table")
    df = result.to_pandas()
except UnauthenticatedError:
    # Handle auth failure with exponential backoff
    print("Authentication failed")
except DominoError as e:
    print(f"Query failed: {e}")
```

## Performance Tips

1. **Use pagination**: Set `page_size` when listing many objects
2. **Parallel downloads**: Use `max_workers` for large files
3. **Stream results**: Use `to_parquet()` for large query results
4. **Reuse clients**: Keep `DataSourceClient` instance for multiple queries
5. **Config override**: Use `update()` for session-specific settings



### Datasets

# Domino Datasets API

The `DatasetClient` provides programmatic access to Domino Datasets for reading files.

## DatasetClient

### Initialization

```python
from domino_data.datasets import DatasetClient

# Auto-configured inside Domino
client = DatasetClient()
```

### Environment Variables

The client uses these environment variables (auto-set in Domino):

| Variable | Purpose |
|----------|---------|
| `DOMINO_USER_API_KEY` | API key for authentication |
| `DOMINO_TOKEN_FILE` | Token file location |
| `DOMINO_API_PROXY` | API proxy URL |

## Get Dataset

```python
# Fetch dataset by name
dataset = client.get_dataset("training-data")

# Dataset is now ready for file operations
```

## List Files

```python
# List all files
files = dataset.list_files()

# List with prefix filter
files = dataset.list_files(prefix="images/train/", page_size=500)

# Iterate through files
for f in files:
    print(f.name)
```

## Download Files

### Simple Download

```python
# Download file to local path
dataset.download_file("model.pkl", "local_model.pkl")
```

### Parallel Download (Large Files)

```python
# Download with multiple workers for speed
dataset.download(
    dataset_file_name="large_dataset.parquet",
    local_file_name="local_data.parquet",
    max_workers=8
)
```

### Download to File Object

```python
# Download to file-like object
with open("output.bin", "wb") as f:
    dataset.download_fileobj("binary_file.bin", f)

# Useful for streaming or in-memory processing
import io
buffer = io.BytesIO()
dataset.download_fileobj("data.json", buffer)
buffer.seek(0)
data = json.load(buffer)
```

## Get File Content

```python
# Get file content as bytes
content = dataset.get("config.json")

# Parse JSON
import json
config = json.loads(content)

# Read CSV
import pandas as pd
import io
csv_content = dataset.get("data.csv")
df = pd.read_csv(io.BytesIO(csv_content))
```

## Get Signed URLs

```python
# Get signed URL for direct access
url = dataset.get_file_url("large_file.zip")

# Use with requests or other HTTP clients
import requests
response = requests.get(url)
```

## File Object Operations

The `_File` class represents individual files:

```python
# Get file object
file = dataset.File("path/to/file.csv")

# Get content as bytes
content = file.get()

# Download to local file
file.download_file("local.csv")

# Download with parallelism
file.download("local.csv", max_workers=4)

# Download to file-like object
with open("output.csv", "wb") as f:
    file.download_fileobj(f)
```

## Configuration Override

```python
from domino_data.datasets import DatasetConfig

# Override configuration for this session
config = DatasetConfig(
    # Configuration options
)
dataset.update(config)

# Reset to default
dataset.reset_config()
```

## Error Handling

```python
from domino_data.datasets import DominoError, UnauthenticatedError

try:
    content = dataset.get("file.txt")
except UnauthenticatedError:
    print("Authentication failed - check credentials")
except DominoError as e:
    print(f"Dataset error: {e}")
except FileNotFoundError:
    print("File not found in dataset")
```

## Common Patterns

### Load Parquet Dataset

```python
import pandas as pd
import pyarrow.parquet as pq
import io

content = dataset.get("data.parquet")
df = pd.read_parquet(io.BytesIO(content))
```

### Load Multiple Files

```python
import pandas as pd

# List CSV files
files = dataset.list_files(prefix="data/", page_size=1000)
csv_files = [f for f in files if f.name.endswith('.csv')]

# Load and concatenate
dfs = []
for f in csv_files:
    content = dataset.get(f.name)
    dfs.append(pd.read_csv(io.BytesIO(content)))

combined_df = pd.concat(dfs, ignore_index=True)
```

### Stream Large Files

```python
# For very large files, use parallel download
dataset.download(
    "huge_file.parquet",
    "/tmp/huge_file.parquet",
    max_workers=16
)

# Then read with memory mapping
df = pd.read_parquet("/tmp/huge_file.parquet")
```

## Best Practices

1. **Use parallel downloads**: Set `max_workers` for large files
2. **Pagination**: Use `page_size` when listing many files
3. **Stream when possible**: Use `download_fileobj` for processing
4. **Cache locally**: Download frequently-used files once
5. **Handle errors**: Wrap operations in try/except



### Training Sets

# Domino Training Sets

Training Sets provide versioned, reproducible datasets for machine learning. The `training_sets` module enables programmatic management of training data.

## Overview

Training Sets help you:
- Version your training data for reproducibility
- Track schema and metadata across versions
- Query and filter training set versions
- Integrate with ML pipelines

## Installation

```python
from domino_data.training_sets import (
    create_training_set_version,
    get_training_set,
    get_training_set_version,
    list_training_sets,
    list_training_set_versions,
    update_training_set,
    update_training_set_version,
    delete_training_set,
    delete_training_set_version
)
```

## Create Training Set Version

```python
import pandas as pd
from domino_data.training_sets import create_training_set_version

# Prepare your training data
df = pd.DataFrame({
    "customer_id": [1, 2, 3, 4, 5],
    "feature_a": [0.1, 0.2, 0.3, 0.4, 0.5],
    "feature_b": [10, 20, 30, 40, 50],
    "label": [1, 0, 1, 0, 1]
})

# Create a new version
version = create_training_set_version(
    training_set_name="customer-churn-model",
    df=df,
    key_columns=["customer_id"],
    description="Initial training data - Q1 2024"
)

print(f"Created version: {version.number}")
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `training_set_name` | str | Name of the training set |
| `df` | DataFrame | Training data |
| `key_columns` | List[str] | Columns that uniquely identify rows |
| `description` | str | Version description |

## Get Training Set

```python
from domino_data.training_sets import get_training_set

# Retrieve training set metadata
ts = get_training_set("customer-churn-model")

print(f"Name: {ts.name}")
print(f"Created: {ts.created_at}")
print(f"Versions: {ts.version_count}")
```

## Get Specific Version

```python
from domino_data.training_sets import get_training_set_version

# Get version by number
version = get_training_set_version(
    training_set_name="customer-churn-model",
    number=1
)

print(f"Version: {version.number}")
print(f"Description: {version.description}")
print(f"Row count: {version.row_count}")
```

## List Training Sets

```python
from domino_data.training_sets import list_training_sets

# List all training sets
all_sets = list_training_sets()

for ts in all_sets:
    print(f"{ts.name}: {ts.version_count} versions")

# Filter with metadata
filtered = list_training_sets(
    meta={"project": "churn-prediction"},
    asc=False,
    offset=0,
    limit=10
)
```

## List Versions

```python
from domino_data.training_sets import list_training_set_versions

# List all versions of a training set
versions = list_training_set_versions(
    training_set_name="customer-churn-model"
)

for v in versions:
    print(f"v{v.number}: {v.description}")

# Filter versions
recent = list_training_set_versions(
    training_set_name="customer-churn-model",
    meta={"status": "production"},
    asc=False,
    limit=5
)
```

## Update Training Set

```python
from domino_data.training_sets import update_training_set

# Update metadata
ts = get_training_set("customer-churn-model")
ts.description = "Updated description"
ts.meta = {"project": "churn-v2", "team": "ml-ops"}

update_training_set(ts)
```

## Update Version

```python
from domino_data.training_sets import update_training_set_version

# Update version metadata
version = get_training_set_version("customer-churn-model", 1)
version.description = "Production training data"
version.meta = {"status": "production"}

update_training_set_version(version)
```

## Delete Training Set

```python
from domino_data.training_sets import delete_training_set

# Only works if no versions exist
delete_training_set("old-training-set")
```

## Delete Version

```python
from domino_data.training_sets import delete_training_set_version

# Delete specific version
delete_training_set_version(
    training_set_name="customer-churn-model",
    number=1
)
```

## Error Handling

```python
from domino_data.training_sets import (
    ServerException,
    SchemaMismatchException
)

try:
    version = create_training_set_version(
        training_set_name="my-data",
        df=df,
        key_columns=["id"]
    )
except SchemaMismatchException:
    print("DataFrame columns don't match existing schema")
except ServerException as e:
    print(f"Server rejected request: {e}")
```

## Best Practices

1. **Meaningful names**: Use descriptive training set names
2. **Key columns**: Always specify columns that uniquely identify rows
3. **Versioning**: Create new versions for each training run
4. **Metadata**: Use `meta` field for filtering and organization
5. **Descriptions**: Document what changed in each version
6. **Schema consistency**: Maintain consistent columns across versions

## Common Patterns

### Training Pipeline Integration

```python
from domino_data.training_sets import (
    create_training_set_version,
    get_training_set_version
)
import mlflow

# Create training version
version = create_training_set_version(
    training_set_name="model-training-data",
    df=training_df,
    key_columns=["id"],
    description=f"Training run {mlflow.active_run().info.run_id}"
)

# Log to MLflow
mlflow.log_param("training_set_version", version.number)
```

### Data Validation

```python
# Validate before creating version
def validate_training_data(df):
    assert not df.isnull().any().any(), "No nulls allowed"
    assert len(df) > 100, "Need at least 100 samples"
    return True

if validate_training_data(df):
    create_training_set_version(
        training_set_name="validated-data",
        df=df,
        key_columns=["id"]
    )
```



### Vectordb

# Domino Vector Database Integration

The `vectordb` module provides integration with Pinecone vector databases through Domino's data source framework.

## Overview

Domino's VectorDB integration allows you to:
- Connect to Pinecone through Domino data sources
- Use Domino's credential management for API keys
- Access vector indexes for similarity search
- Build RAG (Retrieval Augmented Generation) applications

## Prerequisites

1. Pinecone data source configured in Domino
2. Pinecone Python client installed:
   ```bash
   pip install pinecone-client>=3.0.0
   ```

## Pinecone 3.x Integration

### Initialize Pinecone Client

```python
from domino_data.vectordb import domino_pinecone3x_init_params
from pinecone import Pinecone

# Get initialization parameters from Domino data source
init_params = domino_pinecone3x_init_params("my-pinecone-datasource")

# Initialize Pinecone client
pc = Pinecone(**init_params)

# List indexes
indexes = pc.list_indexes()
print(indexes)
```

### Access Index

```python
from domino_data.vectordb import domino_pinecone3x_index_params
from pinecone import Pinecone

# Initialize client
init_params = domino_pinecone3x_init_params("my-pinecone-datasource")
pc = Pinecone(**init_params)

# Get index parameters
index_params = domino_pinecone3x_index_params(
    datasource_name="my-pinecone-datasource",
    index_name="embeddings-index"
)

# Connect to index
index = pc.Index(**index_params)
```

## Vector Operations

### Upsert Vectors

```python
# Prepare vectors with metadata
vectors = [
    {
        "id": "doc1",
        "values": [0.1, 0.2, 0.3, ...],  # 1536 dimensions for OpenAI
        "metadata": {"text": "Document content", "source": "wiki"}
    },
    {
        "id": "doc2",
        "values": [0.4, 0.5, 0.6, ...],
        "metadata": {"text": "Another document", "source": "blog"}
    }
]

# Upsert to index
index.upsert(vectors=vectors, namespace="default")
```

### Query Vectors

```python
# Query by vector
results = index.query(
    vector=[0.1, 0.2, 0.3, ...],
    top_k=10,
    include_metadata=True,
    namespace="default"
)

# Process results
for match in results.matches:
    print(f"ID: {match.id}, Score: {match.score}")
    print(f"Metadata: {match.metadata}")
```

### Query with Filters

```python
# Query with metadata filter
results = index.query(
    vector=query_vector,
    top_k=5,
    filter={"source": {"$eq": "wiki"}},
    include_metadata=True
)
```

### Delete Vectors

```python
# Delete by ID
index.delete(ids=["doc1", "doc2"], namespace="default")

# Delete by filter
index.delete(filter={"source": {"$eq": "old-source"}})

# Delete all in namespace
index.delete(delete_all=True, namespace="test")
```

## Configuration

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `DOMINO_DATA_API_GATEWAY` | Data API gateway URL (default: `http://127.0.0.1:8766`) |

### Headers

The module adds these headers for Domino routing:

| Header | Purpose |
|--------|---------|
| `X-Domino-Datasource` | Data source identifier |
| `X-Domino-Pinecone-Index` | Target Pinecone index |

## RAG Application Example

```python
from domino_data.vectordb import (
    domino_pinecone3x_init_params,
    domino_pinecone3x_index_params
)
from pinecone import Pinecone
from openai import OpenAI

# Initialize clients
pc = Pinecone(**domino_pinecone3x_init_params("pinecone-ds"))
index = pc.Index(**domino_pinecone3x_index_params("pinecone-ds", "docs"))
openai_client = OpenAI()

def get_embedding(text):
    """Get embedding from OpenAI."""
    response = openai_client.embeddings.create(
        model="text-embedding-3-small",
        input=text
    )
    return response.data[0].embedding

def search_documents(query, top_k=5):
    """Search for relevant documents."""
    query_embedding = get_embedding(query)
    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )
    return [match.metadata["text"] for match in results.matches]

def generate_answer(query, context_docs):
    """Generate answer using context."""
    context = "\n\n".join(context_docs)
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Answer based on this context:\n{context}"},
            {"role": "user", "content": query}
        ]
    )
    return response.choices[0].message.content

# RAG query
query = "What is Domino Data Lab?"
docs = search_documents(query)
answer = generate_answer(query, docs)
print(answer)
```

## Best Practices

1. **Batch operations**: Upsert vectors in batches of 100
2. **Namespaces**: Use namespaces to organize vectors
3. **Metadata**: Store useful context in metadata fields
4. **Dimensionality**: Match vector dimensions to your embedding model
5. **Index management**: Create indexes appropriate for your use case

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Connection timeout | Check DOMINO_DATA_API_GATEWAY is accessible |
| Authentication error | Verify data source credentials in Domino |
| Index not found | Confirm index name matches Pinecone |
| Dimension mismatch | Ensure vectors match index dimensions |

