"""Render docs/04-delivery/backlog.json into backlog.md, sprint-plan.md and task-checklist.md.

backlog.json is the single source of truth for epics, stories and sprints.
It is also what gets imported into Jira. Run: python scripts/backlog_to_md.py
"""
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIVERY = ROOT / "docs" / "04-delivery"
VELOCITY = 26
STATUS_LABEL = {"done": "Done", "in_progress": "In progress", "todo": "To do", "blocked": "Blocked"}


def short_description(story: dict) -> str:
    """'As a X I want Y so that Z' -> 'Y (so that Z)', trimmed for a checklist line."""
    m = re.search(r"I want (.+?)(?: so that (.+?))?\.?$", story["story"])
    if not m:
        return story["story"]
    want, why = m.group(1), m.group(2)
    return f"{want[0].upper()}{want[1:]}" + (f", so that {why}." if why else ".")


def write_checklist(data: dict, sprints: dict, by_sprint: dict) -> None:
    stories = data["stories"]
    counts = defaultdict(int)
    for s in stories:
        counts[s.get("status", "todo")] += 1
    out = ["# Task Checklist", "",
           "_Generated from `backlog.json` by `scripts/backlog_to_md.py`. Update a story's `status` "
           "(`todo`, `in_progress`, `blocked`, `done`) in the JSON, then re-run the script._", "",
           "| Done | In progress | Blocked | To do | Total |", "|---|---|---|---|---|",
           f"| {counts['done']} | {counts['in_progress']} | {counts['blocked']} | {counts['todo']} | {len(stories)} |", "",
           "## Your actions (outside the backlog)", ""]
    for a in data.get("owner_actions", []):
        box = "x" if a.get("status") == "done" else " "
        out.append(f"- [{box}] **{a['task']}**: {a['why']}")
    out.append("")
    for sid, sp in sprints.items():
        out += [f"## {sp['name']} ({sp['start']} → {sp['end']})", ""]
        for s in by_sprint[sid]:
            st = s.get("status", "todo")
            box = "x" if st == "done" else " "
            tag = "" if st in ("done", "todo") else f" **[{STATUS_LABEL[st]}]**"
            jira = f", Jira {s['jira']}" if s.get("jira") else ""
            out.append(f"- [{box}] **{s['id']} {s['title']}**{tag}: {short_description(s)} "
                       f"_({s['points']} pts, owner: {s.get('owner', 'Claude')}{jira})_")
        out.append("")
    (DELIVERY / "task-checklist.md").write_text("\n".join(out))


def main() -> None:
    data = json.loads((DELIVERY / "backlog.json").read_text())
    epics = {e["id"]: e for e in data["epics"]}
    sprints = {s["id"]: s for s in data["sprints"]}
    by_epic: dict[str, list[dict]] = defaultdict(list)
    by_sprint: dict[int, list[dict]] = defaultdict(list)
    for story in data["stories"]:
        by_epic[story["epic"]].append(story)
        by_sprint[story["sprint"]].append(story)

    out = ["# Product Backlog", "",
           "_Generated from `backlog.json` by `scripts/backlog_to_md.py`. Edit the JSON, not this file._", "",
           "| Epic | Name | Stories | Points |", "|---|---|---|---|"]
    for eid, epic in epics.items():
        stories = by_epic[eid]
        out.append(f"| {eid} | {epic['name']} | {len(stories)} | {sum(s['points'] for s in stories)} |")
    total = sum(s["points"] for s in data["stories"])
    out += [f"| **Total** | | **{len(data['stories'])}** | **{total}** |", ""]
    for eid, epic in epics.items():
        out += [f"## {eid}: {epic['name']}", "", epic["summary"], ""]
        for s in by_epic[eid]:
            fr = ", ".join(s["fr"]) or "n/a"
            status = STATUS_LABEL[s.get("status", "todo")]
            jira = f", Jira {s['jira']}" if s.get("jira") else ""
            out += [f"### {s['id']}: {s['title']}  ({s['points']} pts, Sprint {s['sprint']}, {status}{jira})", "",
                    f"*{s['story']}*", "", f"Traces to: {fr}", "", "Acceptance criteria:"]
            out += [f"- {ac}" for ac in s["ac"]]
            out.append("")
    (DELIVERY / "backlog.md").write_text("\n".join(out))

    plan = ["# Sprint Plan", "",
            "_Generated from `backlog.json`. Two-week sprints; planned velocity "
            f"{VELOCITY} points (recalibrated after Sprints 0 and 1)._", "",
            "| Sprint | Dates | Goal | Points | Load |", "|---|---|---|---|---|"]
    for sid, sp in sprints.items():
        pts = sum(s["points"] for s in by_sprint[sid])
        load = "OK" if pts <= VELOCITY else f"+{pts - VELOCITY} over (stretch items flagged in planning)"
        plan.append(f"| {sid} | {sp['start']} → {sp['end']} | {sp['goal']} | {pts} | {load} |")
    plan.append("")
    for sid, sp in sprints.items():
        plan += [f"## {sp['name']}", "", f"**Dates:** {sp['start']} → {sp['end']}  ", f"**Goal:** {sp['goal']}", "",
                 "| Story | Title | Points | Status |", "|---|---|---|---|"]
        plan += [f"| {s['id']} | {s['title']} | {s['points']} | {STATUS_LABEL[s.get('status', 'todo')]} |" for s in by_sprint[sid]]
        plan.append("")
    plan += ["Holiday break: 2026-12-25 → 2027-01-01 (no sprint).", ""]
    (DELIVERY / "sprint-plan.md").write_text("\n".join(plan))
    write_checklist(data, sprints, by_sprint)
    print(f"Wrote backlog.md, sprint-plan.md and task-checklist.md ({len(data['stories'])} stories, {total} points)")


if __name__ == "__main__":
    main()
