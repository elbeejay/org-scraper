"""Script that digs into a GitHub org. to get repo. info."""
import requests
import json

# get list of all repositories from org page
org_url = 'https://github.com/orgs/worldbank/repositories?page='

# have to loop to go through the various pages

# create empty list to aggregate dictionary lists of repo info
repo_info = []

# look at main page to get the last page number
r = requests.get(org_url + '1', timeout=120)
html = r.text
resp = json.loads(html)
last_page = resp['payload']['pageCount']

# loop through pages
for i in range(1, last_page + 1):
    # get html
    r = requests.get(org_url + str(i), timeout=120)
    # check status code
    if r.status_code != 200:
        print(i)
        print('Error: ' + str(r.status_code))
        break
    # get html
    html = r.text
    # parse html using json
    resp = json.loads(html)
    # store repo information
    if isinstance(resp['payload']['repositories'], list):
        repo_info += resp['payload']['repositories']
    else:
        raise ValueError(f"Error, resp payload is type: {type(resp['payload']['repositories'])}, not a list")

# pare down big dictionaries to keys of interest
key_list = [
    'name',
    'primaryLanguage',
    'starsCount',
    'forksCount',
    'lastUpdated'
]
# loop through list of dictionaries and pare down
repo_info_pared = []
for repo in repo_info:
    repo_info_pared.append({k: repo[k] for k in key_list})

# write to JSON
with open('repo_info.json', 'w') as f:
    json.dump(repo_info_pared, f, indent=4)
