#!/usr/bin/env python3
"""Convert KiCad's JSON DRC output into a reviewable Markdown release report."""

from __future__ import annotations

from collections import Counter, defaultdict
import json
from pathlib import Path
import sys


RELEASE_BLOCKERS = {
    "clearance",
    "hole_clearance",
    "shorting_items",
    "tracks_crossing",
    "track_dangling",
    "unconnected_items",
    "via_dangling",
}


def finding_lines(finding: dict) -> list[str]:
    lines = [finding.get("description", "No description supplied")]
    for item in finding.get("items", []):
        position = item.get("pos", {})
        location = ""
        if position:
            location = f" at ({position.get('x')}, {position.get('y')})"
        lines.append(f"  - {item.get('description', 'item')}{location}")
    return lines


def main() -> int:
    if len(sys.argv) != 3:
        print(f"usage: {Path(sys.argv[0]).name} DRC.json DRC.md", file=sys.stderr)
        return 2

    json_path, markdown_path = map(Path, sys.argv[1:])
    report = json.loads(json_path.read_text())
    violations = report.get("violations", [])
    unconnected = report.get("unconnected_items", [])
    by_type = Counter(item["type"] for item in violations)
    blocker_count = sum(count for kind, count in by_type.items() if kind in RELEASE_BLOCKERS)
    blocker_count += len(unconnected)
    status = "HOLD — electrical DRC blockers present" if blocker_count else "PASS — no electrical DRC blockers"

    lines = [
        "# PCB design-rule report",
        "",
        f"**Status:** {status}",
        "",
        f"- Source: `{report.get('source', 'unknown')}`",
        f"- KiCad: `{report.get('kicad_version', 'unknown')}`",
        f"- Report time: `{report.get('date', 'unknown')}`",
        f"- Violations: **{len(violations)}**",
        f"- Unconnected items: **{len(unconnected)}**",
        f"- Electrical release blockers: **{blocker_count}**",
        "",
        "Do not release fabrication files while electrical release blockers remain.",
        "",
        "## Counts by rule",
        "",
        "| Count | Rule | Release gate |",
        "| ---: | --- | --- |",
    ]
    for kind, count in by_type.most_common():
        gate = "Blocker" if kind in RELEASE_BLOCKERS else "Review"
        lines.append(f"| {count} | `{kind}` | {gate} |")
    if unconnected:
        lines.append(f"| {len(unconnected)} | `unconnected_items` | Blocker |")

    blockers: dict[str, list[dict]] = defaultdict(list)
    for finding in violations:
        if finding["type"] in RELEASE_BLOCKERS:
            blockers[finding["type"]].append(finding)
    if unconnected:
        blockers["unconnected_items"].extend(unconnected)

    lines.extend(["", "## Electrical release blockers", ""])
    if not blockers:
        lines.append("None.")
    else:
        for kind in sorted(blockers):
            lines.extend([f"### `{kind}` ({len(blockers[kind])})", ""])
            for finding in blockers[kind]:
                details = finding_lines(finding)
                lines.append(f"- {details[0]}")
                lines.extend(f"  {detail}" for detail in details[1:])
            lines.append("")

    markdown_path.write_text("\n".join(lines) + "\n")
    print(f"published {markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
