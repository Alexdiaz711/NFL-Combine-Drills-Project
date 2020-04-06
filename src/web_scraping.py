import warnings
warnings.filterwarnings('ignore')
from pymongo import MongoClient
import requests

client = MongoClient('localhost', 27017)
db = client.draft
draft = db.draft_pages

for i in range(1994, 2020):
    url = 'https://www.pro-football-reference.com/years/' + str(i) + '/draft.htm'
    r = requests.get(url)
    print(r.status_code)
    draft.insert_one({'year': i, 'html': r.content})

combine = db.combine_pages

for i in range(1994, 2020):
    url = 'https://nflcombineresults.com/nflcombinedata.php?year=' + str(i) + '&pos=&college='
    r = requests.get(url)
    print(r.status_code)
    combine.insert_one({'year': i, 'html': r.content})