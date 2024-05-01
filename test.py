import argparse
import logging
import json
import csv

def save_as_csv_file(errors, filename):
  with open(f"{filename}.csv", 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['sheet','row','column','message','level'])
    writer.writeheader()
    writer.writerows(errors)

def save_as_json_file(raw_json, filename, suffix=''):
  filename = f"{filename}_{suffix}.json" if suffix else f"{filename}.json"
  with open(f"{filename}", 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

def save_as_html_file(html, filename, suffix):
  with open(f"{filename}_{suffix}.html", 'w', encoding='utf-8') as f:
    f.write(html)

def save_as_pdf_file(data, filename, suffix):
  with open(f"{filename}_{suffix}.pdf", 'w+b') as f:
    f.write(data)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='USDM Test Program',
    description='Will take the USDM conformant Excel workbook and transform into USDM JSON, HTML, PDF etc',
    epilog='Note: Not that sophisticated! :)'
  )
  parser.add_argument('filename', help="The name of the Excel file without the '.xlsx' extension.") 
  parser.add_argument("--no_watermark", action="store_true", help="No watermark, default is to show watermark") 
  parser.add_argument("--highlight", action="store_false", help="Highlight USDM content, default is not to highlight") 
  parser.add_argument("--m11", action="store_false", help="Generate the M11 fhir message as JSON") 
  parser.add_argument('--debug', action='store_true', help='print debug messages to stderr')
  args = parser.parse_args()
  filename = args.filename
  watermark = not args.no_watermark
  highlight = not args.highlight
  m11 = not args.m11
  debug = args.debug
  level = logging.DEBUG if debug else logging.INFO

  full_filename = f"{filename}.xlsx"
  log = logging.basicConfig(level=level)
  
  from usdm_db import USDMDb
  from usdm_info import __package_version__ as code_version
  from usdm_info import __model_version__ as model_version
  
  print("")
  print(f"Test Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
  print(f"Converting {full_filename} with watermark set {'on' if watermark else 'off'}, highlights {'on' if highlight else 'off'}, M11 FHIR message set {'on' if m11 else 'off'}")
  print("")
  print("")

  usdm = USDMDb()
  errors = usdm.from_excel(full_filename)
  save_as_json_file(json.dumps(json.loads(usdm.to_json())), filename)
  save_as_csv_file(errors, filename)
  if highlight:
    save_as_html_file(usdm.to_html(highlight), filename, 'highlight')
  save_as_html_file(usdm.to_html(), filename, 'USDM')
  save_as_pdf_file(usdm.to_pdf(watermark), filename, 'USDM')
  save_as_html_file(usdm.to_timeline(), filename, 'timeline')
  if m11:
    save_as_json_file(usdm.to_fhir(), filename, 'fhir')
