# USDM Data

Processes USDM-conformant Excel workbooks into USDM API JSON, runs CDISC CORE validation, and generates protocol HTML.

## Scripts

**`import.py`** — Batch import. Processes all studies listed in `config_data/studies.yaml`, generating JSON, error CSVs, CORE validation results, and protocol HTML for each.

```bash
python import.py
```

**`simple.py`** — Single file import. Converts one `.xlsx` file to JSON, saves the error CSV, and runs CORE validation.

```bash
python simple.py path/to/study.xlsx
python simple.py path/to/study.xlsx -o /output/dir
```

## Configuration

`config_data/studies.yaml` defines the studies processed by `import.py`. Each entry specifies the input directory, filename, and whether to generate protocol HTML. All paths are relative to `source_data/protocols/`.

## Output files

For each study, the following files are generated alongside the input `.xlsx`:

- `<name>.json` — USDM API JSON
- `<name>.csv` — Excel import errors and warnings
- `<name>_core.yaml` — CDISC CORE validation findings
- `<template>/<name>_USDM.html` — Protocol HTML (one per template, if enabled)

## Studies

The current set of mapped studies includes:

- CDISC Pilot Study
- Eli Lilly NCT03421379 Diabetes
- Alexion NCT04573309 Wilson's Disease
- Sanofi NCT03637764 Oncology
- Eli Lilly NCT02107703, NCT04004988, NCT04184622, NCT04557384, NCT04677179, NCT05176314, NCT05324124
- Roche NCT02291289, NCT03817853, NCT04320615
- Novo Nordisk NCT03548935, NCT03548987, NCT03693430
- AstraZeneca NCT03402841, Amgen NCT03283098, BMS NCT04730349
- KalVista NCT05259917, Tesaro NCT01847274, Investigator NCT03523273

## Dependencies

See `requirements.txt`. The key packages are:

- `usdm` — Excel-to-USDM conversion, model classes, HTML/PDF rendering
- `usdm4` — USDM v4 support, CDISC CORE validation

