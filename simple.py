import logging
log = logging.basicConfig(level=logging.INFO)

import sys
import json

if __name__ == "__main__":
  arg_count = len(sys.argv)
  if arg_count == 1:
    print("You need to provide an input file name minus the file extension")
  elif arg_count == 2:
    
    from usdm_excel import USDMExcel
    
    filename = sys.argv[1].strip()
    excel = USDMExcel(f"source_data/{filename}.xlsx")
    with open(f"source_data/{filename}.json", 'w', encoding='utf-8') as f:
      f.write(json.dumps(json.loads(excel.to_json()), indent=2))
  else:
    print("Multiple command line arguments detected.")
