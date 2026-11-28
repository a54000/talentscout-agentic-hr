"""R-11 / BR-4: the ATS must not send candidate data to cloud AI.

AI screening and JD/CV matching were removed from the ATS (TS-EA-07, TS-EA-15). These tests
keep them out: no cloud AI client or endpoint in the ATS code, retired routes stay blocked,
and resume extraction never leaves the machine.
"""
import ast
import importlib
import re
import sys
from pathlib import Path

ATS = Path(__file__).resolve().parents[1]
CLOUD_AI_PATTERNS = [
    r"\bgoogle\.genai\b", r"from google import genai", r"generativelanguage\.googleapis\.com",
    r"api-inference\.huggingface\.co", r"openrouter\.ai", r"api\.openai\.com", r"api\.anthropic\.com",
]


def _python_sources():
    return [p for p in ATS.rglob("*.py") if "tests" not in p.parts and "venv" not in p.parts]


def test_no_cloud_ai_client_or_endpoint_in_ats_code():
    hits = []
    for path in _python_sources():
        text = path.read_text(encoding="utf-8-sig", errors="ignore")
        hits += [f"{path.relative_to(ATS)}: {pat}" for pat in CLOUD_AI_PATTERNS if re.search(pat, text)]
    assert hits == []


def test_ai_packages_are_not_dependencies():
    reqs = (ATS / "requirements.txt").read_text().lower()
    for package in ("google-genai", "openai", "anthropic", "transformers"):
        assert not re.search(rf"^{package}\b", reqs, re.M), package


def _load(names):
    src = (ATS / "app.py").read_text(encoding="utf-8-sig")
    tree = ast.parse(src)
    nodes = [n for n in tree.body
             if (isinstance(n, ast.FunctionDef) and n.name in names)
             or (isinstance(n, ast.Assign) and any(getattr(t, "id", "").startswith("RETIRED_AI") for t in n.targets))]
    ns = {"re": re}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "app.py", "exec"), ns)
    return ns


def test_ai_screening_routes_are_retired():
    is_retired = _load({"is_retired_ai_screening_path"})["is_retired_ai_screening_path"]
    for path in ["/ai-screening", "/api/ai_screening_logs", "/api/jd_match", "/api/jd_match/cache/reset",
                 "/api/match_jd_cv", "/api/match/export_pdf", "/api/match/screening_questions",
                 "/api/candidate_resume/analyze", "/api/candidate/42/ai_screening",
                 "/api/candidate/42/ai_screening_report"]:
        assert is_retired(path), path
    for path in ["/api/candidates", "/api/candidate/42", "/api/parse_jd", "/api/parse_cv", "/app", "/healthz"]:
        assert not is_retired(path), path


def test_screening_code_is_gone():
    src = (ATS / "app.py").read_text(encoding="utf-8-sig")
    names = {n.name for n in ast.parse(src).body if isinstance(n, ast.FunctionDef)}
    for removed in ("queue_candidate_ai_screening", "run_candidate_ai_screening", "api_jd_match",
                    "maybe_generate_gemini_screening_report", "call_resume_analysis_llm", "parse_huggingface"):
        assert removed not in names, removed
    assert not (ATS / "services" / "gemini_screening.py").exists()


def test_resume_extraction_stays_local(monkeypatch):
    monkeypatch.delenv("CLOUD_AI_FOR_CANDIDATE_DATA", raising=False)
    monkeypatch.setenv("PARSE_LLM_PROVIDER", "api")
    sys.path.insert(0, str(ATS))
    pipeline = importlib.reload(importlib.import_module("ats_pipeline"))

    def fail(*_args, **_kwargs):
        raise AssertionError("an LLM was called with CV text")

    monkeypatch.setattr(pipeline.requests, "post", fail)
    assert pipeline.llm_extract("resume", "Ravi Kumar, 9876543210, AWS architect") == {}
