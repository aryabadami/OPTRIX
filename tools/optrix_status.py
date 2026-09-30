#!/usr/bin/env python3

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = [
    "research/phase-0-foundation/mission.md",
    "research/phase-0-foundation/principles.toml",
    "research/phase-0-foundation/measurement.toml",
    "research/phase-0-foundation/status.toml",
    "specification/language/core-requirements.md",
    "specification/language/non-goals.md",
    "specification/language/scope.toml",
]


def check_file(relative_path: str) -> bool:
    path = ROOT / relative_path

    if path.exists() and path.is_file() and path.stat().st_size > 0:
        print(f"[PASS] {relative_path}")
        return True

    print(f"[FAIL] {relative_path}")
    return False


def main() -> int:
    print("OPTRIX STATUS CHECK")
    print("===================")
    print(f"Repository: {ROOT}")
    print()

    passed = 0

    for file in REQUIRED_FILES:
        if check_file(file):
            passed += 1

    total = len(REQUIRED_FILES)

    print()
    print(f"Foundation artifacts: {passed}/{total}")

    if passed == total:
        print("STATUS: FOUNDATION CHECK PASSED")
        return 0

    print("STATUS: FOUNDATION CHECK FAILED")
    return 1


if __name__ == "__main__":
    sys.exit(main())
