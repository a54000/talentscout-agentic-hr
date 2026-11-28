# Spike TS-E0-06: Local model selection (MacBook M2, 16 GB)

**Question:** which local model is good enough for JD and resume extraction and evidence checking, and fast enough on an M2 with 16 GB?

**Timebox:** 1 day.

| Candidate | Size (Q4) | Why |
|---|---|---|
| `qwen3:8b` | ~5 GB | Strong structured output and tool calling at 8B |
| `llama3.1:8b` | ~5 GB | Widely used baseline |
| `gemma3:4b` (or similar 3–4B) | ~3 GB | Fallback if RAM is tight |

**Method:**
1. Close Docker. Run each model on the same 5 synthetic JDs with the draft extraction prompt.
2. Record: valid JSON rate, must-have recall against a hand-labelled answer, tokens/sec (`ollama run --verbose`), and peak memory (Activity Monitor).
3. Repeat the best model with Docker running (mongo + redis + api) to check RAM headroom.

**Results:** _to be filled in during Sprint 0_

| Model | Valid JSON | Recall | Tokens/sec | Peak RAM | Notes |
|---|---|---|---|---|---|

**Decision:** _update ADR-0004 with the chosen model and the date._
