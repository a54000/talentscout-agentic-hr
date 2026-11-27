"""Render docs/04-delivery/backlog.json into backlog.md and sprint-plan.md.

backlog.json is the single source of truth for epics, stories and sprints.
It is also what gets imported into Jira. Run: python scripts/backlog_to_md.py
"""
from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DELIVERY = ROOT / "docs" / "04-delivery"
VELOCITY = 26


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
            out += [f"### {s['id']}: {s['title']}  ({s['points']} pts, Sprint {s['sprint']})", "",
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
                 "| Story | Title | Points |", "|---|---|---|"]
        plan += [f"| {s['id']} | {s['title']} | {s['points']} |" for s in by_sprint[sid]]
        plan.append("")
    plan += ["Holiday break: 2026-12-25 → 2027-01-01 (no sprint).", ""]
    (DELIVERY / "sprint-plan.md").write_text("\n".join(plan))
    print(f"Wrote backlog.md and sprint-plan.md ({len(data['stories'])} stories, {total} points)")


if __name__ == "__main__":
    main()
