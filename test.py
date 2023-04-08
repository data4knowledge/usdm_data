import logging
log = logging.basicConfig(level=logging.INFO)

import sys
import json
import yaml

if __name__ == "__main__":
  arg_count = len(sys.argv)
  if arg_count == 1:
    print("You need to provide an inoput file name minus the file extension")
  elif arg_count == 2:
    
    from usdm_excel import USDMExcel
    
    filename = sys.argv[1].strip()
    excel = USDMExcel(f"test_data/{filename}.xlsx")
    errors = excel.errors()
    if errors.count() > 0:
      with open(f"test_data/{filename}_errors.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(errors.dump(), f, default_flow_style=False)
    else:
      with open(f"test_data/{filename}.json", 'w', encoding='utf-8') as f:
        f.write(json.dumps(json.loads(excel.to_json()), indent=2))
  else:
    print("Multiple command line arguments detected.")
