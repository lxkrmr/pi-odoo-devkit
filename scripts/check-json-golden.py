#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


PATH_HINTS = ("/", "\\")


def match(expected, actual, path: str = "$") -> list[str]:
    errors: list[str] = []

    if isinstance(expected, str) and expected.startswith("__") and expected.endswith("__"):
        token = expected
        if token == "__any__":
            return errors
        if token == "__string__" and not isinstance(actual, str):
            return [f"{path}: expected string, got {type(actual).__name__}"]
        if token == "__path__":
            if not isinstance(actual, str):
                return [f"{path}: expected path string, got {type(actual).__name__}"]
            if not actual or not any(sep in actual for sep in PATH_HINTS):
                return [f"{path}: expected path-like string, got {actual!r}"]
            return errors
        if token == "__bool__" and not isinstance(actual, bool):
            return [f"{path}: expected bool, got {type(actual).__name__}"]
        if token == "__number__" and not isinstance(actual, (int, float)):
            return [f"{path}: expected number, got {type(actual).__name__}"]
        if token == "__array__" and not isinstance(actual, list):
            return [f"{path}: expected array, got {type(actual).__name__}"]
        if token == "__object__" and not isinstance(actual, dict):
            return [f"{path}: expected object, got {type(actual).__name__}"]
        return errors

    if type(expected) is not type(actual):
        return [f"{path}: expected {type(expected).__name__}, got {type(actual).__name__}"]

    if isinstance(expected, dict):
        expected_keys = set(expected.keys())
        actual_keys = set(actual.keys())
        if expected_keys != actual_keys:
            missing = sorted(expected_keys - actual_keys)
            extra = sorted(actual_keys - expected_keys)
            if missing:
                errors.append(f"{path}: missing keys: {missing}")
            if extra:
                errors.append(f"{path}: unexpected keys: {extra}")
            return errors
        for key in expected:
            errors.extend(match(expected[key], actual[key], f"{path}.{key}"))
        return errors

    if isinstance(expected, list):
        if len(expected) != len(actual):
            return [f"{path}: expected list length {len(expected)}, got {len(actual)}"]
        for i, (e, a) in enumerate(zip(expected, actual)):
            errors.extend(match(e, a, f"{path}[{i}]"))
        return errors

    if expected != actual:
        return [f"{path}: expected {expected!r}, got {actual!r}"]

    return errors


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: check-json-golden.py <expected.json> <actual.json>", file=sys.stderr)
        raise SystemExit(2)

    expected = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    actual = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))

    errors = match(expected, actual)
    if errors:
        print("Golden JSON mismatch:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        raise SystemExit(1)


if __name__ == "__main__":
    main()
