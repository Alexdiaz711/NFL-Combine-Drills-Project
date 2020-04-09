import warnings
warnings.filterwarnings('ignore')
from pymongo import MongoClient
import requests

# Establish the connection to the MongoDB where the web pages will be stored.
client = MongoClient('localhost', 27017)
db = client.draft
draft = db.draft_pages
combine = db.combine_pages

# Loop through each web page and store source code in the MongoDB
for i in range(1994, 2020):
    url = 'https://www.pro-football-reference.com/years/' + str(i) + '/draft.htm'
    r = requests.get(url)
    print(r.status_code)
    draft.insert_one({'year': i, 'html': r.content})

    url = 'https://nflcombineresults.com/nflcombinedata.php?year=' + str(i) + '&pos=&college='
    r = requests.get(url)
    print(r.status_code)
    combine.insert_one({'year': i, 'html': r.content})