import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import ValidationError, validate


REPO_ROOT = Path(__file__).resolve().parents[2]

CATEGORIES = [
    {
        "name": "models",
        "root": REPO_ROOT / "models",
        "schema": REPO_ROOT / "schema" / "model.schema.json",
        "id_field": "model_name",
        "filename_pattern": r"^[A-Za-z0-9_-]+_\d{4}\.yaml$",
    },
    {
        "name": "datasets",
        "root": REPO_ROOT / "datasets",
        "schema": REPO_ROOT / "schema" / "dataset.schema.json",
        "id_field": "dataset_id",
        "filename_pattern": r"^[A-Za-z0-9_-]+(?:_\d{4})?\.yaml$",
    },
]


def load_json(path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_yaml(path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def iter_yaml_files(root):
    if not root.exists():
        return []
    return sorted(root.rglob("*.yaml"))


def validate_entry_file(path, schema, filename_pattern):
    errors = []

    if not re.match(filename_pattern, path.name):
        errors.append(f"{path}: filename does not match expected convention")

    data = load_yaml(path)
    if not isinstance(data, dict):
        errors.append(f"{path}: YAML entry must be a single mapping/object")
        return None, errors

    try:
        validate(data, schema)
    except ValidationError as exc:
        errors.append(f"{path}: {exc.message}")

    return data, errors


def collect_category(category):
    schema = load_json(category["schema"])
    entries = []
    errors = []
    seen_ids = set()

    for path in iter_yaml_files(category["root"]):
        data, file_errors = validate_entry_file(
            path, schema, category["filename_pattern"]
        )
        errors.extend(file_errors)
        if data is None:
            continue

        entry_id = data.get(category["id_field"])
        if entry_id in seen_ids:
            errors.append(
                f"{path}: duplicate {category['id_field']} '{entry_id}'"
            )
        else:
            seen_ids.add(entry_id)

        entries.append((path, data))

    return entries, errors


def validate_cross_references(model_entries, dataset_entries):
    errors = []
    dataset_ids = {entry["dataset_id"] for _, entry in dataset_entries}

    for path, entry in model_entries:
        for dataset_tag in entry.get("dataset_tags", []):
            if dataset_tag not in dataset_ids:
                errors.append(
                    f"{path}: dataset_tags contains unknown dataset id '{dataset_tag}'"
                )

    return errors


def main():
    collected = {}
    errors = []

    for category in CATEGORIES:
        entries, category_errors = collect_category(category)
        collected[category["name"]] = entries
        errors.extend(category_errors)

    errors.extend(
        validate_cross_references(
            collected.get("models", []),
            collected.get("datasets", []),
        )
    )

    if errors:
        print("Catalog validation failed:\n")
        for error in errors:
            print(f"- {error}")
        return 1

    model_count = len(collected.get("models", []))
    dataset_count = len(collected.get("datasets", []))
    print(
        f"Validated catalog successfully: {model_count} model(s), "
        f"{dataset_count} dataset(s)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
