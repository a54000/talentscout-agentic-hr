# ADR-0004: Zero-cost model routing with PII-aware policy

- **Status:** Accepted
- **Date:** 2026-11-27

## Context
- Cash budget is $0 (D-01).
- Claude Pro and ChatGPT Plus subscriptions do not include API access, so they are used for **development** only (Claude Code, Codex), not at runtime.
- Free cloud tiers have rate limits and may use inputs to improve the provider's products.
- Hardware: MacBook M2, 16 GB unified memory.

## Decision
- All model calls go through a router (LiteLLM from Sprint 6; a thin in-house router in Sprint 1).
- Every request carries `task` and `pii` tags.
- `pii=true` → **local Ollama only** (8B-class instruct model, Q4 quantised, about 5–6 GB RAM). The router raises an error if a cloud route is selected. This is a release-blocking unit test.
- `pii=false` → free cloud tiers in priority order (configurable), then Ollama as the last fallback.
- Embeddings are always local (`nomic-embed-text`, 768-dim).
- Ollama runs natively on macOS, not in Docker, to use the Metal GPU.

## Consequences
- (+) $0 cash. PII stays on HR Guru hardware. The routing policy itself is a showcase feature.
- (−) Local 8B models are weaker at complex reasoning. Mitigation: keep PII-bearing tasks narrow (extraction, evidence checks); planning works on masked summaries.
- (−) 16 GB RAM is shared with Docker. Mitigation: run one LLM at a time, set `OLLAMA_MAX_LOADED_MODELS=1`, and cap Docker at 6 GB.
- The model choice is confirmed by spike TS-E0-06 (quality and tokens/sec on golden JDs).
