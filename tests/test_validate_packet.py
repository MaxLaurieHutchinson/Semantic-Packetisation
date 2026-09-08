from pathlib import Path
import importlib.util
import sys
import re

import pytest

MODULE_PATH = Path(__file__).parents[1] / "scripts" / "validate_packet.py"
spec = importlib.util.spec_from_file_location("validate_packet", MODULE_PATH)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
assert spec.loader is not None
spec.loader.exec_module(module)


def errors_for(text: str):
    packet_type, records, errors = module.parse(text)
    if packet_type:
        errors.extend(module.validate(packet_type, records))
    return errors


def test_valid_task():
    text = """SP/1 TASK
GOAL implement_feature
INVARIANT no_public_api_change
RETURN test_status
EXECUTE yes
"""
    assert errors_for(text) == []


def test_task_requires_goal():
    assert "TASK requires GOAL" in errors_for("SP/1 TASK\nACTION implement\n")


def test_result_status_validation():
    errors = errors_for("SP/1 RESULT\nSTATUS MAYBE\n")
    assert any("STATUS must be one of" in error for error in errors)


def test_unknown_key_rejected():
    errors = errors_for("SP/1 TASK\nGOAL test\nMYSTERY value\n")
    assert any("MYSTERY" in error for error in errors)


@pytest.mark.parametrize("text", [
    "SP/1 CONTEXT\nGAP load testing\n",
    "SP/1 RESULT\nSTATUS PARTIAL\nUNRESOLVED load testing\n",
    "SP/1 REVIEW\nCRITERION no duplicate effects\nEVIDENCE test log\nVERDICT ACCEPT\n",
    "SP/1 TASK\nGOAL inspect\nEXECUTE no\n",
    "\nSP/1 TASK\r\n\tGOAL\tinspect\r\n\r\n",
])
def test_valid_packet_forms(text):
    assert errors_for(text) == []


@pytest.mark.parametrize(("text", "message"), [
    ("", "packet is empty"),
    ("SP/2 TASK\nGOAL test\n", "expected 'SP/1"),
    ("SP/1 UNKNOWN\nGOAL test\n", "expected 'SP/1"),
    ("SP/1 TASK\nGOAL\n", "expected 'KEY value'"),
    ("SP/1 TASK\nGOAL test\n# comment\n", "comments"),
    ("SP/1 CONTEXT\nID example\n", "CONTEXT requires"),
    ("SP/1 RESULT\nCHANGED file.py\n", "RESULT requires STATUS"),
    ("SP/1 REVIEW\nEVIDENCE log\n", "REVIEW requires"),
    ("SP/1 REVIEW\nGOAL inspect\nVERDICT MAYBE\n", "VERDICT must be"),
    ("SP/1 TASK\nGOAL test\nEXECUTE maybe\n", "EXECUTE must be"),
    ("SP/1 TASK\nGOAL test\nSTATUS PASS\n", "not valid for TASK"),
])
def test_invalid_packets(text, message):
    assert any(message in error for error in errors_for(text))


@pytest.mark.parametrize(("packet_type", "required", "record"), [
    ("TASK", "GOAL test", "EXECUTE yes"),
    ("RESULT", "EVIDENCE log", "STATUS PASS"),
    ("REVIEW", "GOAL inspect", "VERDICT ACCEPT"),
])
def test_singular_records_cannot_repeat(packet_type, required, record):
    text = f"SP/1 {packet_type}\n{required}\n{record}\n{record}\n"
    assert any("may appear only once" in error for error in errors_for(text))


def test_parser_preserves_authority_order_and_value_text():
    text = "SP/1 TASK\nGOAL inspect\nAUTH primary\nAUTH secondary\nFACT path=My Files/data.json\n"
    packet_type, records, errors = module.parse(text)
    assert errors == []
    assert packet_type == "TASK"
    assert [(record.key, record.value) for record in records] == [
        ("GOAL", "inspect"), ("AUTH", "primary"), ("AUTH", "secondary"),
        ("FACT", "path=My Files/data.json"),
    ]


def test_validator_record_vocabulary_matches_protocol():
    protocol = (MODULE_PATH.parents[1] / "references" / "protocol.md").read_text(encoding="utf-8")
    record_section = protocol.split("## Common records\n", 1)[1].split("## Required fields\n", 1)[0]
    documented = set(re.findall(r"^### ([A-Z_]+)$", record_section, re.MULTILINE))
    assert set().union(*module.ALLOWED.values()) == documented
