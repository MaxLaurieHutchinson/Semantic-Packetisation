#!/usr/bin/env python3
"""Structural validator for SP/1 semantic packets.

This checks syntax and a small set of protocol invariants. It cannot prove
semantic completeness; the skill's semantic completeness review remains required.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys

TYPES = {"TASK", "CONTEXT", "RESULT", "REVIEW"}

COMMON = {"ID", "REF", "FACT", "EVIDENCE", "UNCERTAIN", "LOSS"}
ALLOWED = {
    "TASK": COMMON
    | {
        "STATE",
        "GOAL",
        "ACTION",
        "SCOPE",
        "AUTH",
        "CASE",
        "INVARIANT",
        "GAP",
        "VERIFY",
        "STOP",
        "SIDE_EFFECT",
        "POST",
        "RETURN",
        "EXECUTE",
    },
    "CONTEXT": COMMON | {"AUTH", "INVARIANT", "GAP", "VERIFY"},
    "RESULT": COMMON
    | {
        "STATUS",
        "CHANGED",
        "VERIFIED",
        "METRIC",
        "ASSUMPTION",
        "DEVIATION",
        "RISK",
        "UNRESOLVED",
        "DECISION",
    },
    "REVIEW": COMMON
    | {
        "GOAL",
        "CRITERION",
        "RISK",
        "DECISION",
        "VERDICT",
        "REVISION",
    },
}

SINGULAR = {
    "TASK": {"EXECUTE"},
    "CONTEXT": set(),
    "RESULT": {"STATUS"},
    "REVIEW": {"VERDICT"},
}

STATUS_VALUES = {"PASS", "PARTIAL", "FAIL", "ESCALATE"}
VERDICT_VALUES = {"ACCEPT", "REVISE", "ESCALATE"}
EXECUTE_VALUES = {"yes", "no"}


@dataclass
class Record:
    line: int
    key: str
    value: str


def parse(text: str) -> tuple[str, list[Record], list[str]]:
    errors: list[str] = []
    lines = text.splitlines()
    nonempty = [(i + 1, line.strip()) for i, line in enumerate(lines) if line.strip()]
    if not nonempty:
        return "", [], ["packet is empty"]

    header_line, header = nonempty[0]
    parts = header.split()
    if len(parts) != 2 or parts[0] != "SP/1" or parts[1] not in TYPES:
        return "", [], [f"line {header_line}: expected 'SP/1 <TASK|CONTEXT|RESULT|REVIEW>'"]

    packet_type = parts[1]
    records: list[Record] = []
    for line_no, line in nonempty[1:]:
        if line.startswith("#"):
            errors.append(f"line {line_no}: comments are not part of canonical SP/1 packets")
            continue
        if " " not in line and "\t" not in line:
            errors.append(f"line {line_no}: expected 'KEY value'")
            continue
        key, value = line.split(None, 1)
        if key not in ALLOWED[packet_type]:
            errors.append(f"line {line_no}: key '{key}' is not valid for {packet_type}")
            continue
        if not value.strip():
            errors.append(f"line {line_no}: value for '{key}' is empty")
            continue
        records.append(Record(line_no, key, value.strip()))

    return packet_type, records, errors


def validate(packet_type: str, records: list[Record]) -> list[str]:
    errors: list[str] = []
    by_key: dict[str, list[Record]] = {}
    for record in records:
        by_key.setdefault(record.key, []).append(record)

    for key in SINGULAR.get(packet_type, set()):
        if len(by_key.get(key, [])) > 1:
            errors.append(f"{key} may appear only once in {packet_type}")

    if packet_type == "TASK" and "GOAL" not in by_key:
        errors.append("TASK requires GOAL")

    if packet_type == "CONTEXT":
        anchors = {"FACT", "REF", "AUTH", "INVARIANT", "GAP", "UNCERTAIN"}
        if not any(key in by_key for key in anchors):
            errors.append("CONTEXT requires at least one FACT, REF, AUTH, INVARIANT, GAP, or UNCERTAIN record")

    if packet_type == "RESULT":
        if "STATUS" not in by_key:
            errors.append("RESULT requires STATUS")
        else:
            value = by_key["STATUS"][0].value
            if value not in STATUS_VALUES:
                errors.append(f"RESULT STATUS must be one of {sorted(STATUS_VALUES)}")

    if packet_type == "REVIEW":
        if not ("GOAL" in by_key or "CRITERION" in by_key):
            errors.append("REVIEW requires GOAL or CRITERION")
        if "VERDICT" in by_key:
            value = by_key["VERDICT"][0].value
            if value not in VERDICT_VALUES:
                errors.append(f"REVIEW VERDICT must be one of {sorted(VERDICT_VALUES)}")

    if "EXECUTE" in by_key:
        value = by_key["EXECUTE"][0].value.lower()
        if value not in EXECUTE_VALUES:
            errors.append("EXECUTE must be 'yes' or 'no'")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate an SP/1 semantic packet")
    parser.add_argument("packet", type=Path, help="Path to packet text file")
    args = parser.parse_args()

    try:
        text = args.packet.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    packet_type, records, errors = parse(text)
    if packet_type:
        errors.extend(validate(packet_type, records))

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"VALID SP/1 {packet_type}: {len(records)} records (structure only)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
