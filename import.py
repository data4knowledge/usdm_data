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
    f.write(json.dumps(json_object, indent=2))

def save_as_yaml_file(data, filepath):
  with open(filepath, 'w') as f:
    yaml.dump(data, f, default_flow_style=False)

def save_as_node_file(nodes, filename):
  save_as_yaml_file(nodes, 'source_data/%s_nodes.yaml' % (filename))

def save_as_edges_file(nodes, filename):
  save_as_yaml_file(nodes, 'source_data/%s_edges.yaml' % (filename))

studies = [
  'Roche Phase 3 NCT04320615',
  'cycles_1',
  'simple_1',
  'simple_2',
  'profile_1'
]

print("")
print (f"Import Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
print("")
print("")
for study in studies:
  print ("Processing study %s ..." % (study))
  file_path = "source_data/%s.xlsx" % (study)
  x = USDMExcel(file_path)
  save_as_json_file(x.to_json(), study)
  nodes, edges = x.to_nodes_and_edges()
  save_as_node_file(nodes, study)
  save_as_edges_file(edges, study)
  print("ERRORS:", x.errors().dump())
  print("")
  print("")