# sqlite-lembed Research

**Date**: 2026-04-20
**Status**: Alpha, likely stalled (no releases since Aug 2024)

## Identity
- **sqlite-lembed** = SQLite extension for generating text embeddings LOCALLY from GGUF models using llama.cpp
- **NOT a vector search solution** - it generates embeddings, sqlite-vec does the search
- Author: Alex Garcia (GitHub: asg017)
- Announced: July 24, 2024
- Blog: https://alexgarcia.xyz/blog/2024/sqlite-lembed-init/index.html
- GitHub: https://github.com/asg017/sqlite-lembed
- PyPI: https://pypi.org/project/sqlite-lembed/ (v0.0.1a8, Aug 24, 2024)
- npm: 0.0.1-alpha.8
- Language: C (73.5%), Python (14.9%), Makefile, CMake, Shell

## The sqlite-vec Ecosystem
| Extension | Purpose | Status |
|-----------|---------|--------|
| sqlite-vec | Vector storage + search (vec0 virtual tables) | Active, stable v0.1.0+ |
| sqlite-lembed | LOCAL embedding generation from GGUF models (llama.cpp) | Alpha, stalled |
| sqlite-rembed | REMOTE embedding generation (OpenAI, Nomic, Cohere, Ollama, etc.) | Work-in-progress |
| sqlite-vss | Original vector search (deprecated, predecessor to sqlite-vec) | Deprecated |

## How It Works
1. Load extension: `.load ./lembed0`
2. Register model: `INSERT INTO temp.lembed_models(name, model) SELECT 'all-MiniLM-L6-v2', lembed_model_from_file('/path/to/model.gguf');`
3. Generate embedding: `SELECT lembed('all-MiniLM-L6-v2', 'text to embed');`
4. Store in sqlite-vec: Embeddings use same BLOB format as sqlite-vec

## Supported Models (GGUF format)
- all-MiniLM-L6-v2 (384-dim float32, 1536 bytes)
- nomic-embed-text-v1.5
- mxbai-embed-large-v1
- Available at: https://huggingface.co/asg017/sqlite-lembed-model-examples

## Release Timeline
| Version | Date |
|---------|------|
| v0.0.1-alpha.1 | May 29, 2024 |
| v0.0.1-alpha.2 | Jun 4, 2024 |
| v0.0.1-alpha.3 | Jun 5, 2024 |
| v0.0.1-alpha.4 | Jun 6, 2024 |
| v0.0.1-alpha.5 | Aug 24, 2024 |
| v0.0.1-alpha.6 | Aug 24, 2024 |
| v0.0.1-alpha.7 | Aug 24, 2024 |
| v0.0.1-alpha.8 | Aug 24, 2024 (LATEST) |

## Current Status
- **Alpha / Likely Stalled**: No releases since Aug 24, 2024 (~20 months ago)
- 11 open issues, 8 open PRs on GitHub
- Pre-compiled builds do NOT use GPU
- Windows NOT supported
- WASM NOT supported
- llama.cpp dependency also under active development

## Known Users
- **Text2VectorSQL** (OpenDCAI) - ArXiv paper June 2025
- **Simon Willison** covered it on his blog (Jul 25, 2024)
- Also: sqlite-utils-sqlite-lembed on PyPI (same version)

## Limitations
- No GPU support in pre-compiled builds
- No Windows support
- No WASM support
- Beta/alpha quality
- llama.cpp dependency is heavy
- No benchmarks found

## Related: sqlite-rembed
- Remote embedding generation (OpenAI, Nomic, Cohere, Jina, MixedBread, Llamafile, Ollama)
- Written in Rust
- Same SQL API pattern (temp.rembed_clients virtual table)
- Also work-in-progress
- GitHub: https://github.com/asg017/sqlite-rembed
