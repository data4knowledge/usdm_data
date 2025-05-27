import os
import json
import csv
import argparse
from usdm_db import USDMDb
from usdm_info import __package_version__ as code_version
from usdm_info import __model_version__ as model_version  

def save_as_csv_file(errors, output_path, filename):
  full_filename = os.path.join(output_path, f"{filename}.csv")
  print(f"CSV: {full_filename}")
  with open(full_filename, 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['sheet','row','column','message','level'])
    writer.writeheader()
    writer.writerows(errors)

def save_as_json_file(raw_json, output_path, filename):
  full_filename = os.path.join(output_path, f"{filename}.json")
  print(f"JSON: {full_filename}")
  with open(full_filename, 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='USDM Simple Test Program',
    description='Will take the USDM conformant Excel workbook and transform into USDM JSON',
    epilog='Note: Not that sophisticated! :)'
  )
  parser.add_argument('filename', help="The name of the Excel file.") 
  args = parser.parse_args()
  filename = args.filename
  
  input_path, tail = os.path.split(filename)
  root_filename = tail.replace(".xlsx", "")
  full_filename = filename
  output_path = input_path
  
  print("")
  print(f"Test Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
  print(f"Output path is: {output_path}")
  print("")

  usdm = USDMDb()
  errors = usdm.from_excel(full_filename)
  raw_json = usdm.to_json()
  save_as_json_file(raw_json, output_path, root_filename)
  save_as_csv_file(errors, output_path, root_filename)
