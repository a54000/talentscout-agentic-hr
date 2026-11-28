# Spike TS-E0-06: Local model selection (MacBook M2, 16 GB)

**Question:** which local model is good enough for JD and resume extraction and evidence checking, and fast enough on an M2 with 16 GB?

**Timebox:** 1 day.

| Candidate | Size (Q4) | Why |
|---|---|---|
| `qwen3:8b` | ~5 GB | Strong structured output and tool calling at 8B |
| `llama3.1:8b` | ~5 GB | Widely used baseline |
| `gemma3:4b` (or similar 3–4B) | ~3 GB | Fallback if RAM is tight |

**Method** (automated by [`scripts/model_spike/model_spike.py`](../../../scripts/model_spike/model_spike.py), using the 5 labelled synthetic JDs in [`jds.json`](../../../scripts/model_spike/jds.json)):

1. Install [Ollama](https://ollama.com) on the Mac and start it. **Quit Docker Desktop.** Then run the script, which downloads each model the first time (about 3–5 GB each):

```bash
python3 scripts/model_spike/model_spike.py --runs 2 --label "Docker stopped" --report docs/04-delivery/spikes/TS-E0-06-results.md
```

2. The script records, per model: valid JSON rate, must-have recall and precision against the labels, experience and location accuracy, tokens/sec, seconds per JD, and the model's memory. Also watch **Memory Pressure** in Activity Monitor: it should stay green.
3. Start Docker with the live ATS (`docker compose up -d ats ats-worker ats-db`) and run the best model again, to check there's enough RAM next to the ATS:

```bash
python3 scripts/model_spike/model_spike.py --models <best model> --label "Docker running" --report docs/04-delivery/spikes/TS-E0-06-results.md
```

**Decision rule:** take the model with the highest must-have recall among those with ≥ 95% valid JSON that keep Memory Pressure green with Docker running. On a tie, take the faster one. If none reaches 80% recall, try `qwen3:14b` only if RAM allows; otherwise keep the deterministic parser and revisit.

**Results:** _paste the tables from `TS-E0-06-results.md` here after the run_

| Model | Valid JSON | Recall | Tokens/sec | Peak RAM | Notes |
|---|---|---|---|---|---|

**Decision:** _update ADR-0004 with the chosen model and the date._
