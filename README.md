<p align="left">
  <img src="https://img.shields.io/badge/status-mvp-brightgreen.svg" alt="status">
  <img src="https://img.shields.io/badge/contributions-welcome-blueviolet.svg" alt="contributions welcome">
  <img src="https://img.shields.io/badge/license-BSD-lightgrey.svg" alt="license">
</p>

# NeuroSource
### *A living, open catalogue of neural foundation models.*

> **NeuroSource** is a community-curated repository of baseline and foundation models for neural data.
> It provides a structured, open, and reviewable way to document models across modalities, tasks, and architectures.

---

## Why this exists

Neural data research is expanding quickly, but it is still hard to answer basic questions such as:

- Which models exist for a given modality?
- What datasets do they use?
- Which architectures and tasks are most common?
- Which projects expose code or open weights?
- Which data hosting platforms and archives are commonly used?

NeuroSource makes that information structured, searchable, and reviewable in the open.

---

## What this repository contains

This repository contains:

- A JSON schema for model entries
- A JSON schema for dataset entries
- A JSON schema for data repository (hosting platform) entries
- YAML catalog records for models, organized by modality
- YAML catalog records for datasets, organized by modality (including multimodal collections)
- A consolidated YAML catalog of data repositories under `repositories/`
- CI validation for contributed entries
- Basic contribution guidance for community submissions

---

## Repository structure

```text
neurosource/
|-- .github/
|   |-- scripts/
|   `-- workflows/
|-- models/
|   `-- eeg/
|   `-- spikes/
|   `...
|-- datasets/
|   `-- eeg/
|   `-- spikes/
|   `...
|-- repositories/
|-- papers/
|-- schema/
|-- docs/
|-- CONTRIBUTING.md
|-- CONTRIBUTORS.md
`-- README.md
```

Key directories:

- `models/`: YAML model entries in per-modality subdirectories (for example `eeg/`, `meg/`, `func/`)
- `datasets/`: YAML dataset entries in per-modality or composite subdirectories (for example `eeg/`, `multimodal/`)
- `repositories/`: YAML definitions of data hosting platforms and archives (currently `repositories.yaml`), referenced from dataset entries via the `repository` field where applicable
- `schema/`: JSON schemas used to validate catalog metadata
- `.github/workflows/`: automated validation on pull requests
- `papers/`: optional notes or summaries that complement catalog entries

---

## Validation

Catalog entries are validated automatically in pull requests.

The validator currently checks:

- schema compliance for models, datasets, and repositories
- YAML structure
- filename conventions (models and datasets)
- folder-to-modality consistency for models and datasets
- dataset references used by model entries (`dataset_tags`)

Validation logic lives in `.github/scripts/validate_catalog.py`.

---

## Example model entry

Current examples include:

- `models/eeg/ShallowFBCSPNet_2017.yaml`
- `models/eeg/EEGPT_2023.yaml`
- `datasets/eeg/BNCI_Horizon_2020.yaml`
- `repositories/repositories.yaml`

Example format:

```yaml
model_name: ShallowFBCSPNet
modality: [EEG]
architecture: CNN
task: classification
year: 2017
paper_url: http://dx.doi.org/10.1002/hbm.23730
code_url: https://github.com/braindecode/braindecode/models/shallow_fbcsp.py
dataset_tags: [BNCI2014-001]
open_weights: false
notes: "Baseline CNN widely used for EEG decoding."
```

---

## Example repository entry

Repositories document hosting platforms (for example OpenNeuro or PhysioNet). Dataset entries can point to a platform using the `repository` string; use a `repository_name` that matches an entry in `repositories/repositories.yaml` so the catalog stays consistent.

Example shape (see `schema/repository.schema.json` for all fields):

```yaml
repository_name: OpenNeuro
url: https://openneuro.org
description: Free and open platform for sharing BIDS-compliant neuroimaging data.
modalities:
  - EEG
  - iEEG
  - MEG
  - fMRI
  - MRI_T1
  - PET
  - NIRS
access_type: open
data_formats:
  - BIDS
```

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md) for the contribution workflow.

In short:

1. Fork the repository.
2. Add a model file under `models/<modality>/<model_name>_<year>.yaml`.
3. Add a dataset file under `datasets/<modality>/` (or the appropriate composite directory such as `datasets/multimodal/`) when needed.
4. If you introduce a new hosting platform or need to correct repository metadata, add or update the matching entry in `repositories/repositories.yaml` (see `schema/repository.schema.json`).
5. Follow the relevant schema in `schema/`.
6. Open a pull request.

Pull requests are validated automatically for schema compliance.

---

## Design principles

- Keep entries lightweight and easy to contribute
- Prefer structured metadata over long freeform summaries
- Make additions easy to review automatically
- Keep the repository useful even without a separate web interface
- Preserve consistency across linked catalog entries

---

## Citation

If you use or reference **NeuroSource** in your work:

```bibtex
@misc{neurosource2025,
  title        = {NeuroSource: An Open Catalogue of Neural Foundation Models},
  author       = {Contributors to the NeuroSource Project},
  year         = {2025},
  howpublished = {\url{https://github.com/IVADO-NeuroAI/neurosource}}
}
```
