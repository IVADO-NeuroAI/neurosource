# Contributing to NeuroSource

Thank you for helping build the open catalogue of neural foundation models.

## What belongs in this repository

The current focus of NeuroSource is the structured catalog itself:

- model metadata entries
- dataset metadata entries
- schema improvements
- validation improvements
- documentation that helps contributors add high-quality entries

If you are unsure whether a change fits the current repository scope, open an issue or mention it in your pull request.

## How to add an entry

1. Fork this repository.
2. Create a new file under the appropriate catalog directory:
   - `models/<modality>/<model_name>_<year>.yaml`
   - `datasets/<modality>/<dataset_id>.yaml`
3. Follow the relevant schema in `schema/`.
4. Run validation locally if you can.
5. Open a pull request.

## Local validation

If your environment has Python plus `pyyaml` and `jsonschema` installed, you can run:

```bash
python .github/scripts/validate_entries.py
```

The pull request workflow runs the same validation in CI.

## Entry conventions

- Use one YAML file per model.
- Use one YAML file per dataset.
- Use descriptive filenames such as `ShallowFBCSPNet_2017.yaml`.
- Prefer dataset filenames that match the dataset identifier, such as `BNCI2014-001.yaml`.
- Place entries under the modality directory that matches their metadata whenever possible.
- Keep metadata factual and concise.
- Use `dataset_tags` for datasets explicitly mentioned in the paper or codebase.
- Use `notes` for brief context, not long summaries.
- Prefer stable naming so entries remain easy to search and compare.
- When a model references datasets, make sure those dataset entries exist in `datasets/`.

## Example

See `models/eeg/ShallowFBCSPNet_2017.yaml` and `datasets/eeg/BNCI2014-001.yaml`.

## Review checklist

Submissions are reviewed for:

- schema compliance
- correct modality, architecture, and dataset metadata
- valid links
- clear notes
- consistent naming

Contributors can be listed in [CONTRIBUTORS.md](./CONTRIBUTORS.md).
