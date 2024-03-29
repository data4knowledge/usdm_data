import argparse
import sys
import json
import requests

class Service():

  def __init__(self, endpoint):
    self.endpoint = endpoint

  def display_response(self, title, endpoint_url, r):
    resp = json.loads(r.text)
    print("%s (%s)" % (title, endpoint_url))
    print(json.dumps(resp, indent=4, sort_keys=True))
    print("")
    print("")

  def post(self, url, body):
    print("Post ...")
    endpoint_url = "%s%s" % (self.endpoint, url)
    r = requests.post(endpoint_url, data=body)
    self.display_response("Post", endpoint_url, r)
    return r.json()
  
  def get(self, url):
    print("Get ...")
    endpoint_url = "%s%s" % (self.endpoint, url)
    r = requests.get(endpoint_url)
    if r.status_code != 200:
      print("Get (%s)" % (endpoint_url))
      print("Bad response, code [%s], text [%s]" % (r.status_code, r.text))
      return {}
    else:
      self.display_response("Get", endpoint_url, r)
      return r.json()

def file_read(filename):
  f = open('%s.json' % (filename))
  return json.load(f)

if __name__ == "__main__":
  parser = argparse.ArgumentParser(
    prog='USDM Inject Program',
    description='Will send a USDM JSON file to a specified endpoint',
    epilog='Note: Not that sophisticated! :)'
  )
  parser.add_argument('filename', help="The name of the JSON file. Provide the full path but without the JSON extension") 
  parser.add_argument('endpoint', help="The name of the endpoint. Can be web or localhost.")
  args = parser.parse_args()
  filename = args.filename
  endpoint = args.endpoint
  
  service = Service(endpoint)
  data = file_read(filename)
  service.post("studyDefinitions", json.dumps(data))
