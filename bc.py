import logging
log = logging.basicConfig(level=logging.INFO)

import json
import yaml

if __name__ == "__main__":
  from usdm_info import __package_version__ as code_version
  from usdm_info import __model_version__ as model_version
  from usdm_excel import cdisc_bc_library

  print("")
  print (f"BC Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
  print("")
  print("")

  items = cdisc_bc_library.catalogue()
  bc_list = []
  for index, item in enumerate(items):
    name = item.title()
    filename = name.lower().replace(' ', '_')
    filename = filename.replace('/', '-')

    syn = cdisc_bc_library.synonyms(item)
    bc_list.append({ 'name': name, 'synonyms': syn})
    print("BC:", name)

    cdisc_json = cdisc_bc_library.to_cdisc_json(item)
    with open(f"bc_data/cdisc/{filename}.json", 'w', encoding='utf-8') as f:
      json.dump(cdisc_json, f, indent=2)

    usdm_json = cdisc_bc_library.to_usdm_json(item)
    with open(f"bc_data/usdm/{filename}.json", 'w', encoding='utf-8') as f:
      json.dump(json.loads(usdm_json), f, indent=2)

    print(f"{index + 1}. BC: {name}")
    
  with open(f"bc_data/catalogue.yaml", 'w', encoding='utf-8') as f:
    yaml.dump(bc_list, f, default_flow_style=False)
