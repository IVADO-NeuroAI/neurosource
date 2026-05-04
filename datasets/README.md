# Datasets

This directory stores structured dataset metadata used by the NeuroSource catalog.

Suggested layout:

```text
datasets/
`-- <modality>/
    `-- <dataset_id>.yaml
```

Dataset entries are intended to be lightweight, factual references that can be reused by model entries through `dataset_tags`.
