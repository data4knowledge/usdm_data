import logging
log = logging.basicConfig(level=logging.INFO)

import json
from usdm_excel import USDMExcel

excel = USDMExcel("source_data/simple_1.xlsx")
with open('source_data/simple_test.json', 'w', encoding='utf-8') as f:
  f.write(json.dumps(json.loads(excel.to_json()), indent=2))