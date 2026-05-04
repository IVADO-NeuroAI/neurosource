# Schema

`model.schema.json` defines the required structure for model catalog entries.

## Required fields

- `model_name`
- `modality`
- `architecture`
- `year`
- `paper_url`

## Optional fields

- `task`
- `paper_doi`
- `code_url`
- `dataset_tags`
- `open_weights`
- `notes`

## Notes

- `dataset_tags` is currently a freeform list of dataset identifiers or short names.
- `notes` should stay short and factual.
- Entries are stored as YAML files under `models/<modality>/`.
