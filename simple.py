"""Convert a single USDM Excel file to JSON, validate with CDISC CORE, and save results."""

import argparse
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


def main():
    parser = argparse.ArgumentParser(
        prog="simple",
        description="Convert a USDM Excel workbook to JSON and run CDISC CORE validation",
    )
    parser.add_argument("filename", help="Path to the .xlsx file")
    parser.add_argument("-o", "--out", default=None, help="Output directory (defaults to input directory)")
    args = parser.parse_args()

    input_path, tail = os.path.split(args.filename)
    name = tail.replace(".xlsx", "")
    output_path = args.out or input_path
    xlsx_path = os.path.abspath(args.filename)
    json_path = os.path.abspath(os.path.join(output_path, f"{name}.json"))
    csv_path = os.path.abspath(os.path.join(output_path, f"{name}.csv"))
    core_path = os.path.abspath(os.path.join(output_path, f"{name}_core.yaml"))

    print(f"\nSimple Import — USDM Python Package v{code_version}, USDM v{model_version}")
    print(f"Input:  {xlsx_path}")
    print(f"Output: {output_path}\n")

    # Excel → JSON
    db = USDMDb()
    errors = db.from_excel(xlsx_path)
    save_json(db.to_json(), json_path)
    save_csv(errors, csv_path)
    print(f"  {json_path}")
    print(f"  {csv_path}")

    # CDISC CORE validation
    usdm4 = USDM4()
    result = usdm4.validate_core(json_path)
    save_yaml(result.to_dict(), core_path)
    print(f"  {core_path}")
    if result.is_valid:
        print(f"\n  CORE validation passed")
    else:
        print(f"\n  CORE validation: {result.finding_count} finding(s) across {len(result.findings)} rule(s)")
    print()


if __name__ == "__main__":
    main()
