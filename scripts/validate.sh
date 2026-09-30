#!/bin/sh

set -eu

ROOT="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"

cd "$ROOT"

echo "================================"
echo "       OPTRIX VALIDATION"
echo "================================"
echo

echo "[1/3] Foundation status"
python3 tools/optrix_status.py

echo
echo "[2/3] Status checker tests"
python3 tests/tools/test_optrix_status.py
python3 tests/tools/test_optrix_status_failure.py

echo
echo "[3/3] Status schema test"
python3 tests/tools/test_status_schema.py

echo
echo "================================"
echo "       VALIDATION PASSED"
echo "================================"
