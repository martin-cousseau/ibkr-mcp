#!/usr/bin/env python3
"""Validate plugin.json and mcp.json against Agent Plugins 1.0.0 schemas."""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

try:
    import jsonschema
    from jsonschema import Draft202012Validator
except ImportError:
    print("MISSING: jsonschema")
    sys.exit(2)


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def validate(instance_path: Path, schema_path: Path) -> None:
    instance = load(instance_path)
    schema = load(schema_path)
    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    if errors:
        print(f"FAIL {instance_path.name}")
        for err in errors:
            loc = ".".join(str(p) for p in err.path) or "<root>"
            print(f"  {loc}: {err.message}")
        raise SystemExit(1)
    print(f"PASS {instance_path.name} against {schema_path.name}")


def main() -> None:
    print("jsonschema", jsonschema.__version__)
    validate(ROOT / "plugin.json", ROOT / "schemas" / "plugin.schema.json")
    validate(ROOT / "mcp.json", ROOT / "schemas" / "mcp.schema.json")
    print("ALL PASS")


if __name__ == "__main__":
    main()
