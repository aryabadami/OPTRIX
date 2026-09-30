#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
STATUS_TOOL = ROOT / "tools" / "optrix_status.py"


def run_status_checker():
    return subprocess.run(
        [sys.executable, str(STATUS_TOOL)],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )


def test_status_checker_passes():
    result = run_status_checker()

    assert result.returncode == 0
    assert "FOUNDATION CHECK PASSED" in result.stdout


if __name__ == "__main__":
    test_status_checker_passes()
    print("PASS: status checker test")
