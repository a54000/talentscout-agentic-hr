"""Unit tests for the ATS security helpers (TS-EA-07).

The helpers are loaded straight from app.py's source so the test does not
start the app or touch a database.
"""
import ast
import os
import re
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "app.py"
NAMES = {"build_update_set", "path_under", "extract_google_sheet_id", "UserInputError", "user_error_message", "report_error"}
CONSTS = {"GOOGLE_SHEET_ID_RE", "GOOGLE_SHEET_URL_RE"}


def _load():
    tree = ast.parse(SRC.read_text(encoding="utf-8-sig"))
    nodes = [n for n in tree.body
             if (isinstance(n, (ast.FunctionDef, ast.ClassDef)) and n.name in NAMES)
             or (isinstance(n, ast.Assign) and any(getattr(t, "id", "") in CONSTS for t in n.targets))]
    import logging
    import secrets
    ns = {"os": os, "re": re, "secrets": secrets, "_error_log": logging.getLogger("test")}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), str(SRC), "exec"), ns)
    return ns


H = _load()


def test_update_set_ignores_unknown_and_crafted_keys():
    data = {"name": "A", "role=1; DROP TABLE candidates; --": "x", "is_admin": 1}
    sets, vals = H["build_update_set"](data, ["name", "email"])
    assert sets == "name=?"
    assert vals == ["A"]


def test_update_set_keeps_allowed_order_and_dedupes():
    sets, vals = H["build_update_set"]({"b": 2, "a": 1}, ["a", "b", "a"])
    assert sets == "a=?, b=?"
    assert vals == [1, 2]


def test_update_set_applies_transform():
    sets, vals = H["build_update_set"]({"email": "X@Y.COM"}, ["email"], lambda k, v: v.lower())
    assert vals == ["x@y.com"]


def test_update_set_empty_when_nothing_allowed():
    assert H["build_update_set"]({"x": 1}, ["a"]) == ("", [])


def test_path_under_allows_children(tmp_path):
    assert H["path_under"](str(tmp_path), "a", "b.pdf") == os.path.join(os.path.realpath(tmp_path), "a", "b.pdf")


@pytest.mark.parametrize("parts", [("..", "etc", "passwd"), ("a", "../../x"), ("/etc/passwd",)])
def test_path_under_rejects_escape(tmp_path, parts):
    with pytest.raises(ValueError):
        H["path_under"](str(tmp_path), *parts)


SHEET = "1AbCdEfGhIjKlMnOpQrStUvWxYz0123456789_-"


@pytest.mark.parametrize("url,expected", [
    (SHEET, SHEET),
    (f"https://docs.google.com/spreadsheets/d/{SHEET}/edit#gid=0", SHEET),
    (f"docs.google.com/spreadsheets/u/0/d/{SHEET}", SHEET),
    (f"https://evil.example/spreadsheets/d/{SHEET}", ""),
    (f"https://docs.google.com.evil.example/spreadsheets/d/{SHEET}", ""),
    ("short", ""),
    ("", ""),
])
def test_google_sheet_id(url, expected):
    assert H["extract_google_sheet_id"](url) == expected


def test_user_error_message_shows_only_fixed_text():
    err = H["UserInputError"]("unsupported_file")
    assert H["user_error_message"](err) == "Upload PDF, DOC, DOCX, or TXT files only"
    leaky = ValueError("could not convert '/srv/app/secret.txt' at line 3")
    assert "secret" not in H["user_error_message"](leaky)


def test_report_error_hides_exception_text(caplog):
    msg = H["report_error"](RuntimeError("password=hunter2 in /etc/app.conf"), "Backup")
    assert "hunter2" not in msg and "/etc" not in msg
    assert msg.startswith("Backup failed.") and "reference" in msg
    assert "hunter2" in caplog.text  # full detail stays in the server log
