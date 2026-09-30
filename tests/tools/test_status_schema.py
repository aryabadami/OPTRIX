#!/usr/bin/env python3

from pathlib import Path
import tomllib

ROOT = Path(__file__).resolve().parents[2]
STATUS_FILE = ROOT / "research/phase-0-foundation/status.toml"


def test_status_schema():
    with STATUS_FILE.open("rb") as file:
        data = tomllib.load(file)

    assert data["project"] == "OPTRIX"
    assert "project_status" in data
    assert "progress" in data
    assert "active_work" in data
    assert "completion_rules" in data

    required_active_fields = [
        "phase",
        "stage",
        "brick",
        "part",
        "name",
    ]

    for field in required_active_fields:
        assert field in data["active_work"]

    print("PASS: status schema is valid")


if __name__ == "__main__":
    test_status_schema()
