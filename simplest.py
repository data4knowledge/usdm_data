import json
import logging

log = logging.basicConfig(level=logging.INFO)

from usdm_excel import USDMExcel

filename = 'simple_1'
excel = USDMExcel(f"source_data/{filename}.xlsx")
with open(f"source_data/{filename}.json", 'w', encoding='utf-8') as f:
  f.write(json.dumps(json.loads(excel.to_json()), indent=2))
