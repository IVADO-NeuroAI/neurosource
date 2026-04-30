import json
import sys

import yaml
from jsonschema import validate, ValidationError

TAXONOMY_PATH = "schema/taxonomies.yaml"

CATEGORIES = [
    {
        "name": "models",
        "data_path": "models/models.yaml",
        "schema_path": "schema/model.schema.json",
        "taxonomy_checks": {
            "modality": "modalities",
            "architecture": "architectures",
            "task": "tasks",
        },
        "taxonomy_list_checks": {},
        "id_field": "model_name",
    },
    {
        "name": "datasets",
        "data_path": "datasets/datasets.yaml",
        "schema_path": "schema/dataset.schema.json",
        "taxonomy_checks": {
            "species": "species",
            "recording_task": "recording_tasks",
            "access_type": "access_types",
            "license": "licenses",
        },
        "taxonomy_list_checks": {
            "modalities": "modalities",
        },
        "id_field": "dataset_id",
    },
    {
        "name": "repositories",
        "data_path": "repositories/repositories.yaml",
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


def validate_category(category, taxonomies):
    errors = []
    data = load_yaml(category["data_path"])
    schema = load_json(category["schema_path"])
    name = category["name"]

    if not isinstance(data, list):
        errors.append(f"[{name}] Expected a YAML list, got {type(data).__name__}")
        return errors

    seen_ids = set()
    id_field = category["id_field"]

    for i, entry in enumerate(data):
        entry_label = entry.get(id_field, f"entry #{i + 1}")

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
            values = entry.get(field, [])
            for value in values:
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
