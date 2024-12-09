import os
import json
import argparse
import pandas as pd
from datetime import datetime

from jsonschema import validators, exceptions

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--schema_file",
                        help="USDM OpenAPI 3.1 JSON file")
    parser.add_argument("-d", "--data_file",
                        help="USDM data JSON file")
    args = parser.parse_args()
    return args

def replace_deep(data, a, b):
    if isinstance(data, str):
        return data.replace(a, b)
    elif isinstance(data, dict):
        return {k: replace_deep(v, a, b) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_deep(v, a, b) for v in data]
    else:
        # nothing to do?
        return data

def list_errors(tree: exceptions.ErrorTree, errctx: str = None):

    for ve in tree.errors.values():
        errlist["json_path"].append(ve.json_path)
        errlist["validator"].append(ve.validator)
        errlist["validator_value"].append(str(ve.validator_value))
        errlist["title"].append(ve.schema.get("title", ""))
        errlist["message"].append(
            ve.message.replace(str(ve.instance), f"[Value of {ve.json_path}]")
            if len(str(ve.instance)) > len(ve.json_path) + 11
            and str(ve.instance) in ve.message
            else ve.message
        )
        errlist["error_context"].append(errctx if errctx else "")

    if len(tree._contents) > 0:
        for k, v in tree._contents.items():
            list_errors(tree=v, errctx=k)

if __name__ == "__main__":
  args = parse_arguments()
  with open(args.schema_file) as schemajson:
      openapi = schemajson.read()
  openapi = json.loads(openapi)
  
  schema = {"$defs": {}}
  for sn, sd in openapi["components"]["schemas"].items():
      if sn == "Wrapper-Input":
          for k, v in sd.items():
              schema[k] = replace_deep(v, "components/schemas", "$defs")
      else:
          schema["$defs"][sn] = replace_deep(sd, "components/schemas", "$defs")

  with open(args.data_file, "r") as file:
      usdmjson = json.load(file)

  cls = validators.validator_for(schema)
  cls.check_schema(schema)
  validator = cls(schema)

  errtree = exceptions.ErrorTree(validator.iter_errors(usdmjson))
  print(f"{errtree.total_errors} errors found in {args.data_file}")
  errlist = {
      "json_path": [],
      "validator": [],
      "validator_value": [],
      "title": [],
      "message": [],
      "error_context": [],
  }
  list_errors(errtree)
  if len(errlist["json_path"]) > 0:
      errdf = pd.DataFrame.from_dict(errlist)
      timestamp = (
          datetime.fromisoformat(datetime.now().isoformat())
          .replace(microsecond=0)
          .isoformat()
          .replace(":", "-")
      )
      with pd.ExcelWriter(
          os.path.join(
              ".",
              f"{os.path.basename(args.data_file).split('.')[0]}" +
              f"-{timestamp}.xlsx",
          )
      ) as writer:
          errdf.to_excel(
              writer,
              sheet_name="Errors",
              index=False,
          )
