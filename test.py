import logging
log = logging.basicConfig(level=logging.DEBUG)

import sys
import json
import yaml

if __name__ == "__main__":
  arg_count = len(sys.argv)
  if arg_count == 1:
    print("You need to provide an inoput file name minus the file extension")
  elif arg_count == 2:
    
    from usdm_excel import USDMExcel
    from usdm_info import __package_version__ as code_version
    from usdm_info import __model_version__ as model_version
    
    print("")
    print (f"Test Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
    print("")
    print("")

    filename = sys.argv[1].strip()
    excel = USDMExcel(f"{filename}.xlsx")
    errors = excel.errors()
    if len(errors) > 0:
      with open(f"{filename}_errors.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(errors, f, default_flow_style=False)
    with open(f"{filename}.json", 'w', encoding='utf-8') as f:
      json.dump(json.loads(excel.to_json()), f, indent=2)


    filename = sys.argv[1].strip()
    excel = USDMExcel(f"{filename}.xlsx")
    with open(f"{filename}.json", 'w', encoding='utf-8') as f:
      f.write(json.dumps(json.loads(excel.to_json()), indent=2))
    with open(f"{filename}_USDM.html", 'w', encoding='utf-8') as f:
      f.write(excel.to_html())
    with open(f"{filename}_USDM.pdf", 'w+b') as f:
      f.write(excel.to_pdf())
    with open(f"{filename}_timeline.html", 'w') as f:
      f.write(excel.to_timeline())
    errors = excel.errors()
    if len(errors) > 0:
      with open(f"{filename}_errors.yaml", 'w', encoding='utf-8') as f:
        yaml.dump(errors, f, default_flow_style=False)

  else:
    print("Multiple command line arguments detected.")
