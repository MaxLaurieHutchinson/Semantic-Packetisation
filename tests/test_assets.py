"""Check shipped assets, not model behaviour or semantic retention."""

import json
from pathlib import Path
import re

from test_validate_packet import errors_for

ROOT = Path(__file__).resolve().parents[1]


def test_quick_start_packet_is_valid_and_matches_readme():
    packet = (ROOT / "examples" / "handoff.sp").read_text(encoding="utf-8")
    source = (ROOT / "examples" / "handoff.txt").read_text(encoding="utf-8").strip()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert errors_for(packet) == []
    assert f"```text\n{packet}```" in readme
    assert f"> {source}\n" in readme


def test_worked_packet_examples_are_structurally_valid():
    examples = (ROOT / "references" / "examples.md").read_text(encoding="utf-8")
    packets = re.findall(r"```text\n(SP/1 [A-Z]+\n.*?)```", examples, re.DOTALL)
    assert packets, "No complete packets found in the worked examples"
    for packet in packets:
        assert errors_for(packet) == [], packet


def test_scenario_catalogue_is_well_formed():
    scenarios = json.loads((ROOT / "evals" / "packetisation_scenarios.json").read_text(encoding="utf-8"))
    assert isinstance(scenarios, list) and scenarios
    ids = []
    for case in scenarios:
        for key in ("id", "purpose", "source"):
            assert isinstance(case[key], str) and case[key].strip()
        for key in ("must_preserve", "hard_failures"):
            assert isinstance(case[key], list) and case[key]
            assert all(isinstance(item, str) and item.strip() for item in case[key])
        assert case["expected_packet_type"] in {"TASK", "CONTEXT", "RESULT", "REVIEW", "NONE"}
        ids.append(case["id"])
    assert len(ids) == len(set(ids)), "Duplicate scenario IDs"
