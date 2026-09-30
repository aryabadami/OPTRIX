#!/usr/bin/env python3

from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[2]
STATUS_TOOL = ROOT / "tools" / "optrix_status.py"


def test_status_checker_detects_missing_artifact():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_root = Path(temp_dir)

        source = STATUS_TOOL.read_text()
        modified = source.replace(
            'ROOT = Path(__file__).resolve().parents[1]',
            f'ROOT = Path("{temp_root}")'
        )

        temporary_tool = temp_root / "optrix_status.py"
        temporary_tool.write_text(modified)

        result = subprocess.run(
            [sys.executable, str(temporary_tool)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "FOUNDATION CHECK FAILED" in result.stdout

        print("PASS: failure detection works")


if __name__ == "__main__":
    test_status_checker_detects_missing_artifact()
