from github import Github
import requests
import urllib.request
import os

access_token = os.getenv('git_access_token')
owner = 'data4knowledge'
repo = 'dafs'

g = Github(access_token)
repository = g.get_repo("data4knowledge/dafs")
contents = repository.get_contents("instances")
for content in contents:
        path = content.path

r = requests.get(
    'https://api.github.com/repos/{owner}/{repo}/contents/instances/'.format(
    owner=owner, repo=repo),
    headers={
        'accept': 'application/vnd.github.v3.raw',
        'authorization': 'token {}'.format(access_token)
            })
data = r.json()
for d in data:
         print(d['download_url'])
         ttl_file = urllib.request.urlopen(d['download_url'], timeout=30).read().decode('utf-8')
         with open('source_data/dafs_ttl/'+d['name'], 'w') as target:
          target.write(ttl_file)     