import logging
log = logging.basicConfig(level=logging.INFO)

import json
import yaml
import csv
from usdm_db import USDMDb
from usdm_info import __package_version__ as code_version
from usdm_info import __model_version__ as model_version

ROOT_PATH = "source_data/protocols/"

def save_as_html_file(html, details, suffix):
  with open(f"{ROOT_PATH}{details['path']}/{details['filename']}_{suffix}.html", 'w', encoding='utf-8') as f:
    f.write(html)

def save_as_pdf_file(data, details, suffix):
  with open(f"{ROOT_PATH}{details['path']}/{details['filename']}_{suffix}.pdf", 'w+b') as f:
    f.write(data)

def save_as_json_file(raw_json, details):
  with open(f"{ROOT_PATH}{details['path']}/{details['filename']}.json", 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

def save_as_csv_file(errors, details):
  with open(f"{ROOT_PATH}{details['path']}/{details['filename']}.csv", 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['sheet','row','column','message','level'])
    writer.writeheader()
    writer.writerows(errors)

def save_as_yaml_file(data, filepath):
  with open(filepath, 'w') as f:
    yaml.dump(data, f, default_flow_style=False)

def save_as_node_file(nodes, details, view):
  suffix = file_suffix(view)
  save_as_yaml_file(nodes, f"{ROOT_PATH}{details['path']}/{details['filename']}_{suffix}nodes.yaml")

def save_as_edges_file(nodes, details, view):
  suffix = file_suffix(view)
  save_as_yaml_file(nodes, f"{ROOT_PATH}{details['path']}/{details['filename']}_{suffix}edges.yaml")

def file_suffix(view):
  if view == USDMDb.TIMELINE_VIEW:
    return 'timeline_'
  return ''

studies = [
  # { 'path': 'NCT04320615', 'filename': 'Roche_NCT04320615_COVID', 'protocol': False, 'watermark': False, 'highlight': False},
  { 'path': 'CDISC_Pilot', 'filename': 'CDISC_Pilot_Study', 'protocol': True, 'watermark': False, 'highlight': True},
  { 'path': 'NCT03421379', 'filename': 'EliLilly_NCT03421379_Diabetes', 'protocol': True, 'watermark': False, 'highlight': True},
]

print (f"\n\nImport Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}\n\n")
for study in studies:
  print (f"Processing study {(study['filename'])} ...\n\n")
  file_path = "{ROOT_PATH}%s/%s.xlsx" % (study['path'], study['filename'])
  x = USDMDb()
  errors = x.from_excel(file_path)
  print("\n\nJSON and Errors\n\n")
  save_as_json_file(x.to_json(), study)
  save_as_csv_file(errors, study)
  print("Timeline\n\n")
  save_as_html_file(x.to_timeline(), study, 'timeline')
  # for view in [USDMDb.FULL_VIEW, USDMDb.TIMELINE_VIEW]:
  #   print(f"{str(view)} view\n\n")
  #   nodes, edges = x.to_nodes_and_edges(view)
  #   save_as_node_file(nodes, study, view)
  #   save_as_edges_file(edges, study, view)
  if study['protocol']:
    print(f"\n\nProtocol HTML and PDF (watermark={study['watermark']}, highlight={study['highlight']})\n\n")
    if study['highlight']:
      save_as_html_file(x.to_html(True), study, 'highlight')
    save_as_html_file(x.to_html(), study, 'USDM')
    save_as_html_file(x.to_timeline(), study, 'timeline')
    save_as_pdf_file(x.to_pdf(study['watermark']), study, 'USDM')
  print(f"\n\nERRORS:\n{errors}\n\n")
  print(f"----- + -----\n\n")
