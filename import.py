import logging
log = logging.basicConfig(level=logging.INFO)

import json
import yaml
import csv
from usdm_db import USDMDb
from usdm_info import __package_version__ as code_version
from usdm_info import __model_version__ as model_version

ROOT_PATH = "source_data/protocols/"

def read_yaml_file(filename):
  with open(f'{filename}.yaml', "r") as f:
    return yaml.safe_load(f)
  
def save_as_html_file(html, details, suffix):
  with open(f"{ROOT_PATH}{details['output_path']}/{details['filename']}_{suffix}.html", 'w', encoding='utf-8') as f:
    f.write(html)

def save_as_pdf_file(data, details, suffix):
  with open(f"{ROOT_PATH}{details['output_path']}/{details['filename']}_{suffix}.pdf", 'w+b') as f:
    f.write(data)

def save_as_json_file(raw_json, details, suffix=''):
  filename = f"{ROOT_PATH}{details['output_path']}/{details['filename']}_{suffix}.json" if suffix else f"{ROOT_PATH}{details['output_path']}/{details['filename']}.json"
  with open(filename, 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

def save_as_csv_file(errors, details):
  with open(f"{ROOT_PATH}{details['output_path']}/{details['filename']}.csv", 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['sheet','row','column','message','level'])
    writer.writeheader()
    writer.writerows(errors)

def save_as_yaml_file(data, filepath):
  with open(filepath, 'w') as f:
    yaml.dump(data, f, default_flow_style=False)

def save_as_node_file(nodes, details, view):
  suffix = file_suffix(view)
  save_as_yaml_file(nodes, f"{ROOT_PATH}{details['output_path']}/{details['filename']}_{suffix}nodes.yaml")

def save_as_edges_file(nodes, details, view):
  suffix = file_suffix(view)
  save_as_yaml_file(nodes, f"{ROOT_PATH}{details['output_path']}/{details['filename']}_{suffix}edges.yaml")

def file_suffix(view):
  if view == USDMDb.TIMELINE_VIEW:
    return 'timeline_'
  return ''

studies = read_yaml_file('config_data/studies')

print (f"\n\nImport Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}\n\n")
for study in studies:
  print (f"Processing study {(study['filename'])} ...\n\n")
  file_path = f"{ROOT_PATH}%s/%s.xlsx" % (study['input_path'], study['filename'])
  study['output_path'] = study['output_path'] if study['output_path'] else study['input_path']
  x = USDMDb()
  errors = x.from_excel(file_path, study['override_template'])
  print("\n\nJSON and Errors\n\n")
  save_as_json_file(x.to_json(), study)
  save_as_csv_file(errors, study)
  print("Timeline\n\n")
  save_as_html_file(x.to_timeline(), study, 'timeline')
  if study['protocol']:
    print(f"\n\nProtocol HTML and PDF (watermark={study['watermark']}, highlight={study['highlight']})\n\n")
    if study['highlight']:
      save_as_html_file(x.to_html(True), study, 'highlight')
    save_as_html_file(x.to_html(), study, 'USDM')
    save_as_html_file(x.to_timeline(), study, 'timeline')
    save_as_pdf_file(x.to_pdf(study['watermark']), study, 'USDM')
    if x.was_m11():
      save_as_json_file(x.to_fhir(), study, 'fhir')
  print(f"\n\nERRORS:\n{errors}\n\n")
  print(f"----- + -----\n\n")
