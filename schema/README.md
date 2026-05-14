# Schema

The `schema/` directory defines the required structure for catalog entries.

## Available schemas

- `model.schema.json`
- `dataset.schema.json`
- `repository.schema.json`

## Model required fields

- `model_name`
- `modality`
- `architecture`
- `year`
- `paper_url`

## Dataset required fields

- `dataset_id`
- `dataset_name`
- `modalities`
- `access_type`
- `url`

## Repository required fields

- `repository_name`
- `url`
- `modalities`
- `access_type`

## Common notes

- model entries live under `models/<modality>/`
- dataset entries live under `datasets/<modality>/` (or composite directories such as `datasets/multimodal/` when applicable)
- repository entries live in `repositories/repositories.yaml`
- `dataset_tags` in models should reference existing dataset IDs
- `notes` should stay short and factual
