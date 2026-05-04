import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import ValidationError, validate


REPO_ROOT = Path(__file__).resolve().parents[2]
MODELS_DIR = REPO_ROOT / "models"
SCHEMA_PATH = REPO_ROOT / "schema" / "model.schema.json"
FILENAME_PATTERN = re.compile(r"^[A-Za-z0-9_-]+_\d{4}\.yaml$")


def load_schema():
    with SCHEMA_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_model_files():
    return sorted(MODELS_DIR.rglob("*.yaml"))


def validate_file(path, schema):
    errors = []

    if not FILENAME_PATTERN.match(path.name):
        errors.append(
            f"{path}: filename must follow <model_name>_<year>.yaml"
        )

    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)

    if not isinstance(data, dict):
        errors.append(f"{path}: YAML entry must be a single mapping/object")
        return errors

    try:
        validate(data, schema)
    except ValidationError as exc:
        errors.append(f"{path}: {exc.message}")

    return errors


def main():
    schema = load_schema()
    files = iter_model_files()

    if not files:
        print("No model files found.")
        return 1

    errors = []
    for path in files:
        errors.extend(validate_file(path, schema))

    if errors:
        print("Validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"Validated {len(files)} model file(s) successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
