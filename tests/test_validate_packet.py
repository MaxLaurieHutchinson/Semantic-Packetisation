from pathlib import Path
import importlib.util
import sys

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
