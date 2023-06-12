import logging
log = logging.basicConfig(level=logging.INFO)

import json
import yaml
from usdm_excel import USDMExcel
from usdm_info import __package_version__ as code_version
from usdm_info import __model_version__ as model_version

def save_as_json_file(raw_json, details):
  with open(f"source_data/{details['path']}/{details['filename']}.json", 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

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
  { 'path': 'NCT04320615', 'filename': 'Roche_NCT04320615_COVID' },
  { 'path': 'Other', 'filename': 'cycles_1' },
  { 'path': 'Other', 'filename': 'cycles_2' },
  { 'path': 'Other', 'filename': 'simple_1' },
  { 'path': 'Other', 'filename': 'simple_2' },
  { 'path': 'Other', 'filename': 'profile_1' },
  { 'path': 'Other', 'filename': 'simple_3' },
  { 'path': 'CDISC_Pilot', 'filename': 'CDISC_Pilot_Study' },
  { 'path': 'NCT03421379', 'filename': 'EliLilly_NCT03421379_Diabetes' },
  { 'path': 'Other', 'filename': 'simple_4' },
  { 'path': 'Other', 'filename': 'arms_epochs' }
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
  for view in [USDMExcel.FULL_VIEW, USDMExcel.TIMELINE_VIEW]:
    print("")
    print("VIEW:", str(view))
    nodes, edges = x.to_nodes_and_edges(view)
    save_as_node_file(nodes, study, view)
    save_as_edges_file(edges, study, view)
  print("")
  print("")
  print("ERRORS:", x.errors())
  print("")
  print("----- + -----")
