"""R-11 / BR-4: real candidate CVs must not reach cloud AI unless explicitly switched on."""
import ast
import importlib
import sys
from pathlib import Path

ATS = Path(__file__).resolve().parents[1]
GATED = {"run_candidate_ai_screening",
         "maybe_generate_gemini_screening_report", "call_resume_analysis_llm"}


def test_every_cv_to_cloud_path_checks_the_switch():
    tree = ast.parse((ATS / "app.py").read_text(encoding="utf-8-sig"))
    found = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in GATED:
            first_checks = ast.dump(ast.Module(body=node.body[:3], type_ignores=[]))
            found[node.name] = "CLOUD_AI_FOR_CANDIDATE_DATA" in first_checks
    assert found == {name: True for name in GATED}


def test_resume_extraction_stays_local_by_default(monkeypatch):
    monkeypatch.delenv("CLOUD_AI_FOR_CANDIDATE_DATA", raising=False)
    monkeypatch.setenv("GEMINI_API_KEY", "dummy-key-not-used")
    sys.path.insert(0, str(ATS))
    pipeline = importlib.reload(importlib.import_module("ats_pipeline"))
    assert pipeline.CLOUD_AI_FOR_CANDIDATE_DATA is False

    def fail(*_args, **_kwargs):
        raise AssertionError("cloud model called with CV text")

    monkeypatch.setattr(pipeline, "_gemini_extract", fail)
    assert pipeline.llm_extract("resume", "Ravi Kumar, 9876543210, AWS architect") == {}


def test_manual_screening_button_reports_switched_off():
    src = (ATS / "app.py").read_text(encoding="utf-8-sig")
    tree = ast.parse(src)
    fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "trigger_candidate_ai_screening")
    body = ast.get_source_segment(src, fn)
    assert body.index("if not CLOUD_AI_FOR_CANDIDATE_DATA") < body.index("queue_candidate_ai_screening(")
    assert "CLOUD_AI_DISABLED_MESSAGE" in body


def _load(names):
    src = (ATS / "app.py").read_text(encoding="utf-8-sig")
    tree = ast.parse(src)
    nodes = [n for n in tree.body
             if (isinstance(n, ast.FunctionDef) and n.name in names)
             or (isinstance(n, ast.Assign) and any(getattr(t, "id", "").startswith("RETIRED_AI") for t in n.targets))]
    import re
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


def test_background_screening_never_queues():
    src = (ATS / "app.py").read_text(encoding="utf-8-sig")
    fn = next(n for n in ast.parse(src).body if isinstance(n, ast.FunctionDef) and n.name == "queue_candidate_ai_screening")
    first = fn.body[1] if isinstance(fn.body[0], ast.Expr) and isinstance(fn.body[0].value, ast.Call) else fn.body[0]
    assert isinstance(fn.body[1], ast.Return) or isinstance(first, ast.Return)
