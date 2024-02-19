import logging
log = logging.basicConfig(level=logging.INFO)

import sys
import json
import csv

def save_as_csv_file(errors, filename):
  with open(f"{filename}.csv", 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['sheet','row','column','message','level'])
    writer.writeheader()
    writer.writerows(errors)

def save_as_json_file(raw_json, filename):
  with open(f"{filename}.json", 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

def save_as_html_file(html, filename, suffix):
  with open(f"{filename}_{suffix}.html", 'w', encoding='utf-8') as f:
    f.write(html)

def save_as_pdf_file(data, filename, suffix):
  with open(f"{filename}_{suffix}.pdf", 'w+b') as f:
    f.write(data)


if __name__ == "__main__":
  arg_count = len(sys.argv)
  if arg_count == 1:
    print("You need to provide an input file name minus the file extension")
  elif arg_count >= 2:

    pdf_test = True    
    if arg_count == 3:
      pdf_test = True if sys.argv[2].strip().lower() in ['true', '1', 't', 'y', 'yes'] else False
    filename = sys.argv[1].strip()
    full_filename = f"{filename}.xlsx"
      
    from usdm_excel import USDMExcel
    from usdm_info import __package_version__ as code_version
    from usdm_info import __model_version__ as model_version
    
    print("")
    print(f"Test Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
    print(f"Converting {full_filename} with test flag set to {pdf_test}")
    print("")
    print("")

    excel = USDMExcel(full_filename)
    save_as_json_file(json.dumps(json.loads(excel.to_json())), filename)
    save_as_csv_file(excel.errors(), filename)
    save_as_html_file(excel.to_html(), filename, 'USDM')
    save_as_pdf_file(excel.to_pdf(pdf_test), filename, 'USDM')
    save_as_html_file(excel.to_timeline(), filename, 'timeline')

  else:
    print("Multiple command line arguments detected.")
