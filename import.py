"""Import USDM studies from Excel, validate with CDISC CORE, and export artefacts."""

import csv
import json
import logging
import os

import yaml

from usdm_db import USDMDb
from usdm4 import USDM4
from usdm_info import __package_version__ as code_version
from usdm_info import __model_version__ as model_version

logging.basicConfig(level=logging.INFO)

ROOT_PATH = "source_data/protocols"


def read_studies(filename: str) -> list[dict]:
    with open(f"{filename}.yaml") as f:
        return yaml.safe_load(f)


def study_path(study: dict, *parts: str) -> str:
    """Build an absolute path under ROOT_PATH / study directory."""
    return os.path.abspath(os.path.join(ROOT_PATH, study["input_path"], *parts))


def save_json(data_json: str, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(json.loads(data_json), f, indent=2)


def save_csv(errors: list[dict], filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["sheet", "row", "column", "message", "level"])
        writer.writeheader()
        writer.writerows(errors)


def save_yaml(data: dict, filepath: str) -> None:
    with open(filepath, "w") as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False)


def save_html(html: str, filepath: str) -> None:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)


def process_study(study: dict, usdm4: USDM4) -> None:
    name = study["filename"]
    xlsx_path = study_path(study, f"{name}.xlsx")
    json_path = study_path(study, f"{name}.json")
    csv_path = study_path(study, f"{name}.csv")
    core_path = study_path(study, f"{name}_core.yaml")

    # Excel → JSON
    db = USDMDb()
    errors = db.from_excel(xlsx_path)
    save_json(db.to_json(), json_path)
    save_csv(errors, csv_path)
    print(f"  Exported JSON and error log")

    # CDISC CORE validation
    print(f"  Validating: {json_path}")
    result = usdm4.validate_core(json_path)
    save_yaml(result.to_dict(), core_path)
    if result.is_valid:
        print(f"  CORE validation passed")
    else:
        print(f"  CORE validation: {result.finding_count} finding(s) across {len(result.findings)} rule(s)")

    # Protocol HTML per template
    if study.get("protocol"):
        for template in db.templates():
            template_dir = study_path(study, template.lower())
            os.makedirs(template_dir, exist_ok=True)
            html_path = os.path.join(template_dir, f"{name}_USDM.html")
            save_html(db.to_html(template), html_path)
            print(f"  Exported protocol HTML ({template})")


def main():
    studies = read_studies("config_data/studies")
    usdm4 = USDM4()

    print(f"\nImport Utility — USDM Python Package v{code_version}, USDM v{model_version}\n")

    for study in studies:
        print(f"Processing {study['filename']} ...")
        process_study(study, usdm4)
        print()


if __name__ == "__main__":
    main()
