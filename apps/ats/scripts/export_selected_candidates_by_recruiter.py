#!/usr/bin/env python3
"""Export selected/offered/joined candidates for a recruiter.

Designed for production use on EC2 with PostgreSQL, but also works against the
local SQLite database through the app DB adapter.
"""

from __future__ import annotations

import argparse
import csv
import os
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import get_db  # noqa: E402

try:
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter
except Exception:  # pragma: no cover - CSV export still works without openpyxl
    Workbook = None


SELECTION_STATUSES = ("selected", "offered", "joined", "hired")


def load_env_file() -> None:
    env_path = ROOT / ".env"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export selected candidates for one recruiter.")
    parser.add_argument("--name", default="Harshita Pruthi", help="Recruiter/team member name.")
    parser.add_argument("--email", default="harshita.hrgp@gmail.com", help="Recruiter/team member email.")
    parser.add_argument("--team-member-id", type=int, default=0, help="Optional team_members.id for exact matching.")
    parser.add_argument("--output-dir", default=str(ROOT / "reports"), help="Folder where CSV/XLSX files are written.")
    parser.add_argument("--prefix", default="", help="Optional filename prefix.")
    return parser.parse_args()


def clean(value: object) -> str:
    return str(value or "").strip()


def detect_selection_date_column(conn) -> bool:
    try:
        conn.execute("SELECT selection_date FROM candidates LIMIT 1").fetchone()
        return True
    except Exception:
        return False


def export_rows(conn, name: str, email: str, team_member_id: int) -> list[dict]:
    selection_expr = "COALESCE(NULLIF(c.updated_at,''), c.created_at, '')"
    if detect_selection_date_column(conn):
        selection_expr = "COALESCE(NULLIF(c.selection_date,''), NULLIF(c.updated_at,''), c.created_at, '')"

    match_clauses = [
        "lower(trim(COALESCE(c.recruiter_name,''))) = lower(trim(?))",
        "lower(trim(COALESCE(c.recruiter_email,''))) = lower(trim(?))",
        "lower(trim(COALESCE(tm.name,''))) = lower(trim(?))",
        "lower(trim(COALESCE(tm.email,''))) = lower(trim(?))",
    ]
    match_params: list[object] = [name, email, name, email]
    if team_member_id:
        match_clauses.insert(0, "c.sourcer_id = ?")
        match_params.insert(0, team_member_id)

    placeholders = ",".join("?" for _ in SELECTION_STATUSES)
    query = f"""
        SELECT
            c.id AS candidate_id,
            c.candidate_name,
            c.status,
            substr({selection_expr}, 1, 10) AS selection_or_status_date,
            c.created_at AS submitted_at,
            c.updated_at,
            c.recruiter_name,
            c.recruiter_email,
            tm.name AS sourcer_name,
            tm.email AS sourcer_email,
            r.client_name,
            r.title AS requirement_title,
            r.requisition_id,
            r.location AS requirement_location,
            c.current_company,
            c.current_role,
            c.phone,
            c.email_addr,
            c.current_location,
            c.preferred_location,
            c.notice_period,
            c.experience_years,
            c.cv_filename,
            c.candidate_feedback,
            c.remarks
        FROM candidates c
        LEFT JOIN team_members tm ON tm.id = c.sourcer_id
        LEFT JOIN requirements r ON r.id = c.requirement_id
        WHERE lower(trim(COALESCE(c.status,''))) IN ({placeholders})
          AND COALESCE(c.is_duplicate, 0) = 0
          AND ({' OR '.join(match_clauses)})
        ORDER BY selection_or_status_date DESC, c.updated_at DESC, c.id DESC
    """
    params = list(SELECTION_STATUSES) + match_params
    return [dict(row) for row in conn.execute(query, params).fetchall()]


def status_counts(conn, name: str, email: str, team_member_id: int) -> list[dict]:
    match_clauses = [
        "lower(trim(COALESCE(c.recruiter_name,''))) = lower(trim(?))",
        "lower(trim(COALESCE(c.recruiter_email,''))) = lower(trim(?))",
        "lower(trim(COALESCE(tm.name,''))) = lower(trim(?))",
        "lower(trim(COALESCE(tm.email,''))) = lower(trim(?))",
    ]
    match_params: list[object] = [name, email, name, email]
    if team_member_id:
        match_clauses.insert(0, "c.sourcer_id = ?")
        match_params.insert(0, team_member_id)
    query = f"""
        SELECT c.status, COUNT(*) AS count
        FROM candidates c
        LEFT JOIN team_members tm ON tm.id = c.sourcer_id
        WHERE COALESCE(c.is_duplicate, 0) = 0
          AND ({' OR '.join(match_clauses)})
        GROUP BY c.status
        ORDER BY count DESC, c.status
    """
    return [dict(row) for row in conn.execute(query, match_params).fetchall()]


def write_csv(path: Path, headers: list[str], rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8-sig") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers)
        writer.writeheader()
        for row in rows:
            writer.writerow({header: row.get(header, "") for header in headers})


def write_xlsx(path: Path, headers: list[str], rows: list[dict], counts: list[dict], args: argparse.Namespace) -> None:
    if Workbook is None:
        return
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Selected Candidates"
    sheet.append(headers)
    for row in rows:
        sheet.append([row.get(header, "") for header in headers])

    header_fill = PatternFill("solid", fgColor="1F2937")
    header_font = Font(color="FFFFFF", bold=True)
    for cell in sheet[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center")
    sheet.freeze_panes = "A2"
    for idx, header in enumerate(headers, 1):
        values = [len(str(row.get(header, ""))) for row in rows]
        sheet.column_dimensions[get_column_letter(idx)].width = min(max([len(header), *values]) + 2, 42)

    summary = workbook.create_sheet("Summary")
    summary.append(["Export generated at", datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    summary.append(["Recruiter", args.name])
    summary.append(["Recruiter email", args.email])
    summary.append(["Team member id", args.team_member_id or "Not specified"])
    summary.append(["Selection statuses included", "Selected, Offered, Joined, Hired"])
    summary.append(["Selected candidate rows found", len(rows)])
    summary.append([])
    summary.append(["All status counts for matched recruiter"])
    summary.append(["Status", "Count"])
    for item in counts:
        summary.append([item.get("status") or "(blank)", item.get("count")])
    for row in summary.iter_rows(min_row=1, max_row=summary.max_row):
        row[0].font = Font(bold=True)
    summary.column_dimensions["A"].width = 38
    summary.column_dimensions["B"].width = 36
    workbook.save(path)


def main() -> int:
    load_env_file()
    args = parse_args()
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    safe_name = "_".join((args.prefix or args.name).lower().replace("@", "_").split())
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = output_dir / f"{safe_name}_selected_candidates_{stamp}"

    conn = get_db(timeout=20)
    try:
        rows = export_rows(conn, args.name, args.email, args.team_member_id)
        counts = status_counts(conn, args.name, args.email, args.team_member_id)
    finally:
        conn.close()

    headers = [
        "candidate_id",
        "candidate_name",
        "status",
        "selection_or_status_date",
        "submitted_at",
        "updated_at",
        "recruiter_name",
        "recruiter_email",
        "sourcer_name",
        "sourcer_email",
        "client_name",
        "requirement_title",
        "requisition_id",
        "requirement_location",
        "current_company",
        "current_role",
        "phone",
        "email_addr",
        "current_location",
        "preferred_location",
        "notice_period",
        "experience_years",
        "cv_filename",
        "candidate_feedback",
        "remarks",
    ]

    csv_path = base.with_suffix(".csv")
    xlsx_path = base.with_suffix(".xlsx")
    write_csv(csv_path, headers, rows)
    write_xlsx(xlsx_path, headers, rows, counts, args)

    print(f"Rows exported: {len(rows)}")
    print(f"CSV: {csv_path.resolve()}")
    if Workbook is not None:
        print(f"XLSX: {xlsx_path.resolve()}")
    print("Status counts:")
    for item in counts:
        print(f"  {item.get('status') or '(blank)'}: {item.get('count')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
