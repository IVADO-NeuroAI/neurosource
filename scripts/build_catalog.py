"""
Reads YAML catalog entries and generates JSON data files for the Docusaurus site.

Output goes to website/src/data/ so React pages can import them directly.
"""

import json
import os
import sys

import yaml

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(REPO_ROOT, "website", "src", "data")

CATEGORIES = [
    {
        "name": "models",
        "data_path": os.path.join(REPO_ROOT, "models"),
        "multi_file": True,
        "id_field": "model_name",
    },
    {
        "name": "datasets",
        "data_path": os.path.join(REPO_ROOT, "datasets"),
        "multi_file": True,
        "id_field": "dataset_id",
    },
    {
        "name": "repositories",
        "data_path": os.path.join(REPO_ROOT, "repositories", "repositories.yaml"),
        "multi_file": False,
        "id_field": "repository_name",
    },
]


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f)


def load_entries(category):
    """Load entries from either a directory of files or a single list file."""
    entries = []
    if category["multi_file"]:
        for root, _, files in os.walk(category["data_path"]):
            for f in sorted(files):
                if f.endswith(".yaml"):
                    path = os.path.join(root, f)
                    data = load_yaml(path)
                    if isinstance(data, dict):
                        entries.append(data)
                    elif isinstance(data, list):
                        entries.extend(data)
    else:
        data = load_yaml(category["data_path"])
        if isinstance(data, list):
            entries.extend(data)
        elif isinstance(data, dict):
            entries.append(data)
    return entries


def build_taxonomies():
    """Load taxonomies and write as JSON."""
    tax_path = os.path.join(REPO_ROOT, "schema", "taxonomies.yaml")
    taxonomies = load_yaml(tax_path)
    output_path = os.path.join(OUTPUT_DIR, "taxonomies.json")
    with open(output_path, "w") as f:
        json.dump(taxonomies, f, indent=2)
    print(f"  Wrote {output_path}")
    return taxonomies


def build_category(category):
    """Load all entries for a category and write as JSON."""
    entries = load_entries(category)
    output_path = os.path.join(OUTPUT_DIR, f"{category['name']}.json")
    with open(output_path, "w") as f:
        json.dump(entries, f, indent=2)
    print(f"  Wrote {output_path} ({len(entries)} entries)")
    return entries


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    print("Building catalog data for Docusaurus...\n")

    print("Taxonomies:")
    build_taxonomies()

    print("\nEntries:")
    for category in CATEGORIES:
        build_category(category)

    print("\nDone!")


if __name__ == "__main__":
    main()
