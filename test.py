import argparse
import logging
import json
import csv
import os
from usdm_db import USDMDb
from usdm_info import __package_version__ as code_version
from usdm_info import __model_version__ as model_version  
  
def save_as_csv_file(errors, output_path, filename):
  full_filename = os.path.join(output_path, f"{filename}.csv")
  print(f"CSV: {full_filename}")
  with open(full_filename, 'w', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['sheet','row','column','message','level'])
    writer.writeheader()
    writer.writerows(errors)

def save_as_json_file(raw_json, output_path, filename, suffix=''):
  full_filename = os.path.join(output_path, f"{filename}_{suffix}.json" if suffix else f"{filename}.json")
  print(f"JSON: {full_filename}")
  with open(full_filename, 'w', encoding='utf-8') as f:
    json_object = json.loads(raw_json)
    json.dump(json_object, f, indent=2)

def save_as_html_file(html, output_path, filename, suffix):
  full_filename = os.path.join(output_path, f"{filename}_{suffix}.html")
  print(f"HTML: {full_filename}")
  with open(full_filename, 'w', encoding='utf-8') as f:
    f.write(html)

def save_as_pdf_file(data, output_path, filename, suffix):
  full_filename = os.path.join(output_path, f"{filename}_{suffix}.pdf")
  print(f"PDF: {full_filename}")
  with open(full_filename, 'w+b') as f:
    f.write(data)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='USDM Test Program',
    description='Will take the USDM conformant Excel workbook and transform into USDM JSON, HTML, PDF etc',
    epilog='Note: Not that sophisticated! :)'
  )
  parser.add_argument('filename', help="The name of the Excel file.") 
  parser.add_argument('-o', '--out', help="The path of where the output files should be written. Defaults to the input path.", default=None) 
  parser.add_argument('-t', "--template", help="Override the configured template with the specified one", default=None) 
  parser.add_argument('-nw', "--no_watermark", action="store_true", help="No watermark, default is to show the watermark") 
  parser.add_argument('-hl', "--highlight", action="store_false", help="Highlight USDM content, default is not to highlight") 
  parser.add_argument('-d', '--debug', action='store_true', help='print debug messages to stderr')
  args = parser.parse_args()
  filename = args.filename
  output_path = args.out
  template = args.template
  watermark = not args.no_watermark
  highlight = not args.highlight
  debug = args.debug
  level = logging.DEBUG if debug else logging.INFO

  input_path, tail = os.path.split(filename)
  root_filename = tail.replace(".xlsx", "")
  full_filename = filename
  output_path = output_path if output_path else input_path
  log = logging.basicConfig(level=level)
  
  print("")
  print(f"Test Utility, using USDM Python Package v{code_version} supporting USDM version v{model_version}")
  print(f"Converting {full_filename} with watermark set {'on' if watermark else 'off'}, highlights {'on' if highlight else 'off'}")
  print(f"Output path is: {output_path}")
  if template:
    print(f"Overiding configured template with: {template}")
  print("")
  print("")

  usdm = USDMDb()
  errors = usdm.from_excel(full_filename)
  template = usdm.default_template() if not template else template.upper()
  save_as_json_file(json.dumps(json.loads(usdm.to_json())), output_path, root_filename)
  save_as_csv_file(errors, output_path, root_filename)
  if highlight:
    save_as_html_file(usdm.to_html(template, highlight), output_path, root_filename, 'highlight')
  save_as_html_file(usdm.to_html(template), output_path, root_filename, 'USDM')
  save_as_pdf_file(usdm.to_pdf(template, watermark), output_path, root_filename, 'USDM')
  save_as_html_file(usdm.to_timeline(), output_path, root_filename, 'timeline')
  if usdm.is_m11():
    save_as_json_file(usdm.to_fhir("M11"), output_path, root_filename, 'fhir')
