"""TS-E0-06 spike: compare local Ollama models for JD extraction on the M2 Mac.

Standard library only, so it runs with the macOS python3. Needs Ollama running (https://ollama.com).
Synthetic JDs only (jds.json); nothing leaves the Mac.

  python3 scripts/model_spike/model_spike.py                       # default 3 models
  python3 scripts/model_spike/model_spike.py --models qwen3:8b llama3.1:8b gemma3:4b --runs 2
  python3 scripts/model_spike/model_spike.py --report docs/04-delivery/spikes/TS-E0-06-results.md

Per model it records: valid JSON rate, must-have recall and precision against the labels,
experience and location accuracy, tokens/sec, seconds per JD, and the model's memory (Ollama /api/ps).
Close Docker for the first run (spike method step 1); run the best model again with Docker up (step 3).
"""
import argparse
import json
import os
import re
import statistics
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_MODELS = ["qwen3:8b", "llama3.1:8b", "gemma3:4b"]
PROMPT = """You extract structured data from a job description. Return only JSON with exactly these keys:
{{"role_title": string, "must_have_skills": [string], "nice_to_have_skills": [string],
  "experience_min_years": number or null, "experience_max_years": number or null, "location": string}}
List each mandatory skill as a short name (e.g. "Terraform", "Spring Boot"). Do not invent skills.

Job description:
\"\"\"{jd}\"\"\"
"""


def call(base, path, payload=None, timeout=600):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(base + path, data=data, headers={"Content-Type": "application/json"},
                                 method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode())


def ensure_model(base, model):
    names = {m.get("name") for m in call(base, "/api/tags").get("models", [])}
    if model in names or f"{model}:latest" in names:
        return
    print(f"  pulling {model} (first time only, a few GB)...", flush=True)
    call(base, "/api/pull", {"model": model, "stream": False}, timeout=7200)


def norm(skill):
    return re.sub(r"[^a-z0-9/+#]", "", str(skill).lower())


def matches(label, found):
    a, b = norm(label), norm(found)
    return bool(a and b) and (a in b or b in a)


def score(jd, parsed):
    found = [s for s in parsed.get("must_have_skills") or [] if str(s).strip()]
    hit = [lab for lab in jd["must"] if any(matches(lab, f) for f in found)]
    correct = [f for f in found if any(matches(lab, f) for lab in jd["must"])]
    exp_ok = (parsed.get("experience_min_years") == jd["experience"][0]
              and parsed.get("experience_max_years") == jd["experience"][1])
    loc_ok = jd["location"].lower() in str(parsed.get("location", "")).lower()
    return {"recall": len(hit) / len(jd["must"]), "precision": (len(correct) / len(found)) if found else 0.0,
            "experience_ok": exp_ok, "location_ok": loc_ok, "missed": [m for m in jd["must"] if m not in hit]}


def memory_gb(base, model):
    for m in call(base, "/api/ps").get("models", []):
        if m.get("name", "").split(":")[0] == model.split(":")[0]:
            return round((m.get("size") or 0) / 1e9, 1)
    return None


def run_model(base, model, jds, runs):
    ensure_model(base, model)
    call(base, "/api/generate", {"model": model, "prompt": "Say OK.", "stream": False})  # load once (not timed)
    rows = []
    for _ in range(runs):
        for jd in jds:
            started = time.time()
            res = call(base, "/api/generate", {"model": model, "prompt": PROMPT.format(jd=jd["text"]), "format": "json",
                                               "stream": False, "options": {"temperature": 0}})
            seconds = time.time() - started
            tps = (res.get("eval_count") or 0) / ((res.get("eval_duration") or 1) / 1e9)
            try:
                parsed = json.loads(res.get("response") or "")
                valid = isinstance(parsed, dict) and isinstance(parsed.get("must_have_skills"), list)
            except ValueError:
                parsed, valid = {}, False
            row = {"jd": jd["id"], "valid": valid, "seconds": seconds, "tps": tps}
            row.update(score(jd, parsed) if valid else {"recall": 0.0, "precision": 0.0, "experience_ok": False,
                                                         "location_ok": False, "missed": jd["must"]})
            rows.append(row)
            print(f"  {jd['id']}: valid={valid} recall={row['recall']:.0%} {seconds:.1f}s {tps:.0f} tok/s"
                  + (f" missed={row['missed']}" if row["missed"] else ""), flush=True)
    return {
        "model": model, "n": len(rows),
        "valid": sum(r["valid"] for r in rows) / len(rows),
        "recall": statistics.mean(r["recall"] for r in rows),
        "precision": statistics.mean(r["precision"] for r in rows),
        "experience": sum(r["experience_ok"] for r in rows) / len(rows),
        "location": sum(r["location_ok"] for r in rows) / len(rows),
        "tps": statistics.median(r["tps"] for r in rows),
        "seconds": statistics.median(r["seconds"] for r in rows),
        "memory_gb": memory_gb(base, model),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--models", nargs="+", default=DEFAULT_MODELS)
    parser.add_argument("--runs", type=int, default=1, help="repeat the 5 JDs this many times per model")
    parser.add_argument("--ollama", default=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"))
    parser.add_argument("--report", help="write a markdown results table to this file")
    parser.add_argument("--label", default="Docker stopped", help="conditions, e.g. 'Docker running'")
    args = parser.parse_args()
    base = args.ollama.rstrip("/")
    try:
        version = call(base, "/api/version").get("version")
    except (urllib.error.URLError, OSError) as exc:
        raise SystemExit(f"Ollama is not reachable at {base} ({exc}). Install it from https://ollama.com and start it.")
    jds = json.load(open(os.path.join(HERE, "jds.json")))
    results = []
    for model in args.models:
        print(f"\n== {model}", flush=True)
        try:
            results.append(run_model(base, model, jds, args.runs))
        except (urllib.error.URLError, OSError, ValueError) as exc:
            print(f"  FAILED: {exc}", flush=True)
            results.append({"model": model, "error": str(exc)})
    lines = [f"Run {time.strftime('%Y-%m-%d %H:%M')} · Ollama {version} · {args.label} · {len(jds)} JDs × {args.runs}",
             "", "| Model | Valid JSON | Must-have recall | Precision | Experience | Location | Tokens/sec | s per JD | Model RAM |",
             "|---|---|---|---|---|---|---|---|---|"]
    for r in results:
        if "error" in r:
            lines.append(f"| {r['model']} | failed: {r['error'][:60]} | | | | | | | |")
            continue
        lines.append(f"| {r['model']} | {r['valid']:.0%} | {r['recall']:.0%} | {r['precision']:.0%} | {r['experience']:.0%} | "
                     f"{r['location']:.0%} | {r['tps']:.0f} | {r['seconds']:.1f} | "
                     f"{str(r['memory_gb']) + ' GB' if r['memory_gb'] else 'n/a'} |")
    table = "\n".join(lines)
    print("\n" + table)
    if args.report:
        with open(args.report, "a") as f:
            f.write(table + "\n\n")
        print(f"\nappended to {args.report}")


if __name__ == "__main__":
    main()
