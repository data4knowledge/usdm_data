import logging
log = logging.basicConfig(level=logging.INFO)

import json
import yaml
import csv
from usdm_excel import USDMExcel
from usdm_info import __package_version__ as code_version
from usdm_info import __model_version__ as model_version

def save_as_html_file(html, details):
  with open(f"source_data/{details['path']}/{details['filename']}_USDM.html", 'w', encoding='utf-8') as f:
    f.write(html)

def save_as_json_file(raw_json, details):
  with open(f"source_data/{details['path']}/{details['filename']}.json", 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

def save_as_csv_file(errors, details):
  with open(f"source_data/{details['path']}/{details['filename']}.csv", 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['sheet','row','column','message','level'])
    writer.writeheader()
    writer.writerows(errors)

def save_as_yaml_file(data, filepath):
  with open(filepath, 'w') as f:
    yaml.dump(data, f, default_flow_style=False)

def save_as_node_file(nodes, details, view):
  suffix = file_suffix(view)
  save_as_yaml_file(nodes, f"source_data/{details['path']}/{details['filename']}_{suffix}nodes.yaml")

def save_as_edges_file(nodes, details, view):
  suffix = file_suffix(view)
  save_as_yaml_file(nodes, f"source_data/{details['path']}/{details['filename']}_{suffix}edges.yaml")

def file_suffix(view):
  if view == USDMExcel.TIMELINE_VIEW:
    return 'timeline_'
  return ''

studies = [
  # { 'path': 'NCT04320615', 'filename': 'Roche_NCT04320615_COVID', 'html': False},
  { 'path': 'CDISC_Pilot', 'filename': 'CDISC_Pilot_Study', 'html': True},
  { 'path': 'NCT03421379', 'filename': 'EliLilly_NCT03421379_Diabetes', 'html': False},
]

print("")
print (f"Import Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
print("")
print("")
for study in studies:
  print ("Processing study %s ..." % (study['filename']))
  print("")
  file_path = "source_data/%s/%s.xlsx" % (study['path'], study['filename'])
  x = USDMExcel(file_path)
  save_as_json_file(x.to_json(), study)
  save_as_csv_file(x.errors(), study)
  for view in [USDMExcel.FULL_VIEW, USDMExcel.TIMELINE_VIEW]:
    print("")
    print("VIEW:", str(view))
    nodes, edges = x.to_nodes_and_edges(view)
    save_as_node_file(nodes, study, view)
    save_as_edges_file(edges, study, view)
  if study['html']:
    save_as_html_file(x.to_html(), study)
  print("")
  print("")
  print("ERRORS:", x.errors())
  print("")
  print("----- + -----")
