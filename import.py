import logging
log = logging.basicConfig(level=logging.INFO)

import json
import yaml
from usdm_excel import USDMExcel
from usdm_info import __package_version__ as code_version
from usdm_info import __model_version__ as model_version

def save_as_json_file(raw_json, filename):
  with open('source_data/%s.json' % (filename), 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

def save_as_yaml_file(data, filepath):
  with open(filepath, 'w') as f:
    yaml.dump(data, f, default_flow_style=False)

def save_as_node_file(nodes, filename, view):
  suffix = file_suffix(view)
  save_as_yaml_file(nodes, f'source_data/{filename}_{suffix}nodes.yaml')

def save_as_edges_file(nodes, filename, view):
  suffix = file_suffix(view)
  save_as_yaml_file(nodes, f'source_data/{filename}_{suffix}edges.yaml')

def file_suffix(view):
  if view == USDMExcel.TIMELINE_VIEW:
    return 'timeline_'
  return ''

studies = [
  'Roche_NCT04320615_COVID',
  'cycles_1',
  'cycles_2',
  'simple_1',
  'simple_2',
  'profile_1',
  'simple_3',
  'CDISC_Pilot_Study',
  'EliLilly_NCT03421379_Diabetes',
  'simple_4'
]

print("")
print (f"Import Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
print("")
print("")
for study in studies:
  print ("Processing study %s ..." % (study))
  print("")
  file_path = "source_data/%s.xlsx" % (study)
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
