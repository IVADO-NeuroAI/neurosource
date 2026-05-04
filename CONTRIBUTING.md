# Contributing to NeuroSource

Thank you for helping build the open catalogue of neural foundation models.

## What belongs in this repository

The current focus of NeuroSource is the structured catalog itself:

- model metadata entries
- schema improvements
- validation improvements
- documentation that helps contributors add high-quality entries

If you are unsure whether a change fits the current repository scope, open an issue or mention it in your pull request.

## How to add a model

1. Fork this repository.
2. Create a new file under `models/<modality>/<model_name>_<year>.yaml`.
3. Follow the schema in `schema/model.schema.json`.
4. Run validation locally if you can.
5. Open a pull request.

## Local validation

If your environment has Python plus `pyyaml` and `jsonschema` installed, you can run:

```bash
python .github/scripts/validate_models.py
```

The pull request workflow runs the same validation in CI.

## Entry conventions

- Use one YAML file per model.
- Use descriptive filenames such as `ShallowFBCSPNet_2017.yaml`.
- Keep metadata factual and concise.
- Use `dataset_tags` for datasets explicitly mentioned in the paper or codebase.
- Use `notes` for brief context, not long summaries.
- Prefer stable naming so entries remain easy to search and compare.

## Example

See `models/eeg/ShallowFBCSPNet_2017.yaml`.

## Review checklist

Submissions are reviewed for:

- schema compliance
- correct modality and architecture metadata
- valid links
- clear notes
- consistent naming

Contributors can be listed in [CONTRIBUTORS.md](./CONTRIBUTORS.md).
