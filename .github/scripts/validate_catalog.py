import json
import re
import sys
from pathlib import Path

import yaml
from jsonschema import Draft7Validator, FormatChecker


REPO_ROOT = Path(__file__).resolve().parents[2]
FORMAT_CHECKER = FormatChecker()
TAXONOMY_PATH = REPO_ROOT / "schema" / "taxonomies.yaml"
MODALITY_DIR_MAP = {
    "EEG": "eeg",
    "MEG": "meg",
    "fMRI": "fmri",
    "ECoG": "ecog",
    "spikes": "spikes",
    "LFP": "lfp",
    "calcium": "calcium",
    "other": "other",
}

CATEGORIES = [
    {
        "name": "models",
        "root": REPO_ROOT / "models",
        "schema": REPO_ROOT / "schema" / "model.schema.json",
        "id_field": "model_name",
        "filename_pattern": r"^[A-Za-z0-9_-]+_\d{4}\.yaml$",
        "taxonomy_checks": {},
        "taxonomy_list_checks": {
            "modality": "modalities",
            # "architecture": "architectures",
            # "task": "tasks",
        },
    },
    {
        "name": "datasets",
        "root": REPO_ROOT / "datasets",
        "schema": REPO_ROOT / "schema" / "dataset.schema.json",
        "id_field": "dataset_id",
        "filename_pattern": r"^[A-Za-z0-9_-]+(?:_\d{4})?\.yaml$",
        "taxonomy_checks": {
            "species": "species",
            "access_type": "access_types",
            "license": "licenses",
        },
        "taxonomy_list_checks": {
            "modalities": "modalities",
            "recording_task": "recording_tasks",
        },
    },
    {
        "name": "repositories",
        "root": REPO_ROOT / "repositories",
        "schema": REPO_ROOT / "schema" / "repository.schema.json",
        "id_field": "repository_name",
        "taxonomy_checks": {
            "access_type": "access_types",
        },
        "taxonomy_list_checks": {
            "modalities": "modalities",
        },
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


def taxonomy_multivalues(entry, field):
    """Return values for a field that may be a string or list of strings."""
    value = entry.get(field)
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return value
    return []


def validate_taxonomy(label, entry, category, taxonomies):
    errors = []

    for field, taxonomy_key in category.get("taxonomy_checks", {}).items():
        value = entry.get(field)
        if value is not None and value not in taxonomies[taxonomy_key]:
            allowed = ", ".join(taxonomies[taxonomy_key])
            errors.append(
                f"{label}: '{field}' value '{value}' "
                f"not in taxonomies.{taxonomy_key} ({allowed})"
            )

    for field, taxonomy_key in category.get("taxonomy_list_checks", {}).items():
        for value in taxonomy_multivalues(entry, field):
            if value not in taxonomies[taxonomy_key]:
                allowed = ", ".join(taxonomies[taxonomy_key])
                errors.append(
                    f"{label}: '{field}' contains '{value}' "
                    f"not in taxonomies.{taxonomy_key} ({allowed})"
                )

    return errors


def slugify_model_name(name):
    return re.sub(r"[^A-Za-z0-9_-]+", "", name)


def validate_entry_file(path, schema, filename_pattern):
    errors = []

    if filename_pattern and not re.match(filename_pattern, path.name):
        errors.append(f"{path}: filename does not match expected convention")

    raw = load_yaml(path)

    if isinstance(raw, dict):
        items = [(path, raw)]
    elif isinstance(raw, list):
        items = [(f"{path}[{i}]", item) for i, item in enumerate(raw)]
    else:
        errors.append(f"{path}: YAML must be a mapping or list of mappings")
        return [], errors

    validator = Draft7Validator(schema, format_checker=FORMAT_CHECKER)
    validated = []
    for label, data in items:
        if not isinstance(data, dict):
            errors.append(f"{label}: entry must be a mapping/object")
            continue
        for error in validator.iter_errors(data):
            errors.append(f"{label}: {error.message}")
        validated.append((label, data))

    return validated, errors


def validate_model_consistency(path, entry):
    errors = []

    modalities = entry["modality"]
    parent_dir = path.parent.name
    expected_dirs = {MODALITY_DIR_MAP[m] for m in modalities if m in MODALITY_DIR_MAP}
    if expected_dirs and parent_dir not in expected_dirs:
        errors.append(
            f"{path}: modality {modalities} should live under one of "
            f"{sorted(expected_dirs)}"
        )

    expected_name = f"{slugify_model_name(entry['model_name'])}_{entry['year']}.yaml"
    if path.name != expected_name:
        errors.append(
            f"{path}: filename should be '{expected_name}' based on model_name and year"
        )

    return errors


def validate_dataset_consistency(path, entry):
    errors = []

    if len(entry["modalities"]) == 1:
        expected_dir = MODALITY_DIR_MAP.get(entry["modalities"][0], "other")
        parent_dir = path.parent.name
        if parent_dir != expected_dir:
            errors.append(
                f"{path}: single-modality dataset should live under '{expected_dir}/'"
            )
    elif path.parent.name == "other":
        pass

    expected_name = f"{entry['dataset_id']}.yaml"
    if path.name != expected_name:
        errors.append(
            f"{path}: filename should be '{expected_name}' based on dataset_id"
        )

    return errors


def collect_category(category, taxonomies):
    schema = load_json(category["schema"])
    entries = []
    errors = []
    seen_ids = set()

    for path in iter_yaml_files(category["root"]):
        items, file_errors = validate_entry_file(
            path, schema, category.get("filename_pattern")
        )
        errors.extend(file_errors)

        for label, data in items:
            if category["name"] == "models":
                errors.extend(validate_model_consistency(path, data))
            elif category["name"] == "datasets":
                errors.extend(validate_dataset_consistency(path, data))

            errors.extend(validate_taxonomy(label, data, category, taxonomies))

            entry_id = data.get(category["id_field"])
            if entry_id in seen_ids:
                errors.append(
                    f"{label}: duplicate {category['id_field']} '{entry_id}'"
                )
            else:
                seen_ids.add(entry_id)

            entries.append((label, data))

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
    taxonomies = load_yaml(TAXONOMY_PATH)
    collected = {}
    errors = []

    for category in CATEGORIES:
        entries, category_errors = collect_category(category, taxonomies)
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
    repo_count = len(collected.get("repositories", []))
    print(
        f"Validated catalog successfully: {model_count} model(s), "
        f"{dataset_count} dataset(s), {repo_count} repository(ies)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
