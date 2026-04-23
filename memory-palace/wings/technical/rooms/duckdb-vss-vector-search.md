---
title: DuckDB VSS Extension — Vector Search for RAG
date: 2026-04-20
tags: [duckdb, vector-search, hnsw, rag, embeddings, sqlite-alternative]
status: active
---

# DuckDB VSS Extension — Vector Search for RAG

## Quick Reference

- **Extension**: duckdb-vss (official DuckDB core extension)
- **GitHub**: github.com/duckdb/duckdb-vss
- **Maturity**: EXPERIMENTAL (WAL recovery not implemented)
- **DuckDB Version**: v1.5 (April 2026)
- **Algorithm**: HNSW via USearch library
- **Metrics**: cosine, L2 (l2sq), inner product (ip)
- **Float Types**: FLOAT32 only (no FLOAT16, no INT8 quantization)

## Memory Estimates (768d FLOAT32)

| Scale | Raw Vectors | HNSW Index | Total RAM |
|-------|-----------|-----------|----------|
| 500K | ~1.4 GB | ~1.6 GB | ~3.5 GB |
| 1M | ~2.9 GB | ~3.2 GB | ~6.9 GB |

**8GB RAM verdict**: 500K viable, 1M very tight

## Key SQL

~~~sql
INSTALL vss; LOAD vss;
SET GLOBAL hnsw_enable_experimental_persistence = true;

CREATE INDEX emb_idx ON embeddings
    USING HNSW (embedding)
    WITH (metric = 'cosine', ef_construction = 128, M = 16);

SELECT id, text, array_cosine_distance(embedding, ?::FLOAT[768]) AS dist
FROM embeddings ORDER BY dist LIMIT 10;
~~~

## Critical Gotchas

1. WAL recovery NOT implemented — crash = potential index corruption
2. Index MUST fit entirely in RAM (not buffer-managed)
3. VSS incompatible with DuckLake
4. Single-row queries have 50x overhead (98% DuckDB engine)
5. Persistence requires experimental flag

## Hybrid Search

- FTS extension provides BM25 full-text search
- Combine FTS + VSS manually via SQL CTEs
- No built-in RRF — implement scoring in SQL

## Performance

- LATERAL join optimization: 66x speedup (10s → 0.15s, M3 Pro)
- Better for batch/bulk search than single lookups
- Community FAISS extension also available (GPU support on Linux)

## Verdict vs Alternatives

For 8GB RAM personal RAG:
- **500K vectors**: DuckDB VSS viable (~3.5 GB), best analytical+vector combo
- **1M vectors**: LanceDB better (~100-400 MB, disk-first)
- **Reliability**: LanceDB/FAISS more stable (experimental persistence risk)

## Full Report

See: `/a0/usr/workdir/duckdb-vss-deep-research-report.md`
