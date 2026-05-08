import json
import os
import sys

import yaml
from jsonschema import validate, ValidationError

TAXONOMY_PATH = "schema/taxonomies.yaml"

CATEGORIES = [
    {
        "name": "models",
        "data_path": "models/",
        "multi_file": True,
        "schema_path": "schema/model.schema.json",
        "taxonomy_checks": {
            # "modality": "modalities",
            # "architecture": "architectures",
            # "task": "tasks",
        },
        "taxonomy_list_checks": {
            "modality": "modalities",
        },
        "id_field": "model_name",
    },
    {
        "name": "datasets",
        "data_path": "datasets/",
        "multi_file": True,
        "schema_path": "schema/dataset.schema.json",
        "taxonomy_checks": {
            "species": "species",
            "access_type": "access_types",
            "license": "licenses",
        },
        "taxonomy_list_checks": {
            "modalities": "modalities",
            "recording_task": "recording_tasks",
        },
        "id_field": "dataset_id",
    },
    {
        "name": "repositories",
        "data_path": "repositories/repositories.yaml",
        "multi_file": False,
        "schema_path": "schema/repository.schema.json",
        "taxonomy_checks": {
            "access_type": "access_types",
        },
        "taxonomy_list_checks": {
            "modalities": "modalities",
        },
        "id_field": "repository_name",
    },
]


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_json(path):
    with open(path) as f:
        return json.load(f)


def taxonomy_multivalues(entry, field):
    """Values for taxonomy checks on fields that may be a string or list of strings."""
    value = entry.get(field)
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    return []


def load_entries(category):
    """Load entries as a list of (source_label, entry) tuples."""
    if category["multi_file"]:
        entries = []
        for root, _, files in os.walk(category["data_path"]):
            for f in sorted(files):
                if f.endswith(".yaml"):
                    path = os.path.join(root, f)
                    data = load_yaml(path)
                    if isinstance(data, dict):
                        entries.append((path, data))
                    elif isinstance(data, list):
                        for i, item in enumerate(data):
                            entries.append((f"{path}[{i}]", item))
                    else:
                        entries.append((path, None))
        return entries
    else:
        data = load_yaml(category["data_path"])
        source = category["data_path"]
        if isinstance(data, list):
            return [(f"{source}[{i}]", entry) for i, entry in enumerate(data)]
        return [(source, None)]


def validate_category(category, taxonomies):
    errors = []
    schema = load_json(category["schema_path"])
    name = category["name"]
    id_field = category["id_field"]
    entries = load_entries(category)

    if not entries:
        print(f"  No entries found in {category['data_path']}")
        return errors

    seen_ids = set()

    for source, entry in entries:
        if entry is None:
            errors.append(f"[{name}] {source}: could not parse as a valid entry")
            continue

        entry_label = entry.get(id_field, source)

        try:
            validate(entry, schema)
        except ValidationError as e:
            errors.append(f"[{name}] {entry_label}: schema error: {e.message}")

        for field, taxonomy_key in category["taxonomy_checks"].items():
            value = entry.get(field)
            if value is not None and value not in taxonomies[taxonomy_key]:
                allowed = ", ".join(taxonomies[taxonomy_key])
                errors.append(
                    f"[{name}] {entry_label}: '{field}' value '{value}' "
                    f"not in taxonomies.{taxonomy_key} ({allowed})"
                )

        for field, taxonomy_key in category["taxonomy_list_checks"].items():
            for value in taxonomy_multivalues(entry, field):
                if value not in taxonomies[taxonomy_key]:
                    allowed = ", ".join(taxonomies[taxonomy_key])
                    errors.append(
                        f"[{name}] {entry_label}: '{field}' contains '{value}' "
                        f"not in taxonomies.{taxonomy_key} ({allowed})"
                    )

        entry_id = entry.get(id_field)
        if entry_id:
            if entry_id in seen_ids:
                errors.append(f"[{name}] duplicate {id_field}: '{entry_id}'")
            seen_ids.add(entry_id)

    return errors


def main():
    taxonomies = load_yaml(TAXONOMY_PATH)
    all_errors = []

    for category in CATEGORIES:
        print(f"Validating {category['name']}...")
        errors = validate_category(category, taxonomies)
        all_errors.extend(errors)

    if all_errors:
        print(f"\n{len(all_errors)} validation error(s) found:\n")
        for err in all_errors:
            print(f"  - {err}")
        sys.exit(1)

    print("\nAll entries valid!")


if __name__ == "__main__":
    main()
