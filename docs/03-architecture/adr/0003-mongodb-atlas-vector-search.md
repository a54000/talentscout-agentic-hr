# ADR-0003: MongoDB Atlas for documents, vector and keyword search

- **Status:** Accepted
- **Date:** 2026-11-27

## Context
Hybrid search needs vector and BM25 search. Options: Atlas Vector Search + Atlas Search; Postgres + pgvector; a dedicated vector DB (Qdrant, Weaviate).

## Decision
MongoDB Atlas (free cluster) for the pilot and demo. Use `mongodb/mongodb-atlas-local` in Docker for development and CI, which offers the same `$vectorSearch`/`$search` APIs locally at no cost.

## Consequences
- (+) One database for business data, embeddings, checkpoints and memory. It stays MERN.
- (−) The free cluster has about 500 MB, 100 ops/s and **3 search/vector indexes**. We use 2 (vector + text), leaving 1 for feedback memory.
- (−) 50k profiles × chunks × 768-dim embeddings may exceed 500 MB. Mitigation: store chunk embeddings for the pilot subset only, use 384-dim embeddings if needed, and keep the full set on atlas-local on the Mac. Tracked as R-04.
