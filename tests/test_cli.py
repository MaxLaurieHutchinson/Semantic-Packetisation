"""Exercise the public scripts without optional site packages or network access."""

from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]


def run_script(name, *args):
    return subprocess.run(
        [sys.executable, "-S", str(ROOT / "scripts" / name), *map(str, args)],
        capture_output=True, text=True, encoding="utf-8", timeout=10,
    )


@pytest.mark.parametrize("script", ["validate_packet.py", "compare_payloads.py"])
@pytest.mark.parametrize("bad_input", ["missing", "invalid_utf8"])
def test_input_errors_are_readable(script, bad_input, tmp_path):
    bad = tmp_path / "bad.txt"
    if bad_input == "invalid_utf8":
        bad.write_bytes(b"\xff")
    good = tmp_path / "good.sp"
    good.write_text("SP/1 TASK\nGOAL inspect\n", encoding="utf-8")
    args = [bad] if script == "validate_packet.py" else [bad, good]
    result = run_script(script, *args)
    assert result.returncode == 2
    assert "ERROR:" in result.stderr
    assert "Traceback" not in result.stderr


def test_validator_success_explains_its_limit(tmp_path):
    packet = tmp_path / "task.sp"
    packet.write_text("SP/1 TASK\nGOAL inspect\n", encoding="utf-8")
    result = run_script("validate_packet.py", packet)
    assert result.returncode == 0
    assert "VALID SP/1 TASK" in result.stdout
    assert "structure only" in result.stdout


def test_invalid_packet_returns_failure(tmp_path):
    packet = tmp_path / "bad.sp"
    packet.write_text("SP/1 TASK\nACTION inspect\n", encoding="utf-8")
    result = run_script("validate_packet.py", packet)
    assert result.returncode == 1
    assert "TASK requires GOAL" in result.stdout


def test_comparison_reports_proxies_without_optional_tokenizer(tmp_path):
    source, packet = tmp_path / "source.txt", tmp_path / "packet.sp"
    source.write_text("a b c d", encoding="utf-8")
    packet.write_text("a b", encoding="utf-8")
    result = run_script("compare_payloads.py", source, packet)
    assert result.returncode == 0
    assert "words_proxy\t4\t2\t50.0%" in result.stdout
    assert "tokens\tunavailable\tunavailable\tn/a" in result.stdout
    assert "proxies only" in result.stdout
