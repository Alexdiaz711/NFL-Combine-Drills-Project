from pymongo import MongoClient
import pandas as pd
import copy
from bs4 import BeautifulSoup

client = MongoClient('localhost', 27017)
db = client['draft']
combine1 = db['combine_pages']
combine2 = db['combine_results']
draft1 = db['draft_pages']
draft2 = db['draft_results']

#Parsing combine data into mongodb collection
for i in range(1994, 2020):
   page = combine1.find_one({'year':i})['html']
   soup = BeautifulSoup(page, "html")
   table = soup.find("table")
   rows = table.find_all("tr")
   all_rows = []

   headers = rows[0].find_all("td")
   column_names = [h.text for h in headers]

   empty_row = {col: None for col in column_names}
   for row in rows[1:-1]:
       new_row = copy.copy(empty_row)
       data_fields = row.find_all("td")
       data = [df.text for df in data_fields]
       data2 = [d.replace('9.99', '') for d in data]       
       for i, col in enumerate(column_names):
           new_row[col] = data2[i]
       all_rows.append(new_row)
       combine2.insert_one(new_row)
        

#Parsing draft data into mongodb collection
for i in range(1994, 2020):
    page = draft1.find_one({'year':i})['html']
    soup = BeautifulSoup(page, "html")
    table = soup.find("table")
    rows = table.find_all("tr")
    all_rows = []

    headers = rows[1].text.split('\n')
    column_names = ['Year',]
    column_names.extend(headers[2:-1])
    
    empty_row = {col: None for col in column_names}
    for row in rows[2:]:
        new_row = copy.copy(empty_row)
        data_fields = row.find_all("td")
        if len(data_fields) == 0:
            continue
        data = [df.text for df in data_fields]
        data2 = [i,]
        data2.extend(data)
        for j, col in enumerate(column_names):
            new_row[col] = data2[j]
        all_rows.append(new_row)
        draft2.insert_one(new_row) 

# Reset of mongoDB connection for data cleaning
client = MongoClient('localhost', 27017)
db = client['draft']
combine = db['combine_results']
draft = db['draft_results'] 

combine_df = pd.DataFrame(list(combine.find()))
draft_df = pd.DataFrame(list(draft.find()))

# cleaning of Combine Data
combine_df = combine_df.drop('_id', axis=1)
change_cols = ['Year', 'Height (in)', 'Weight (lbs)', 'Wonderlic', '40 Yard', 
                'Bench Press', 'Vert Leap (in)', 'Broad Jump (in)', 'Shuttle', '3Cone']
for col in change_cols:
    combine_df[col] = pd.to_numeric(combine_df[col])

# cleaning of Draft Data
draft_df = draft_df.drop(['_id', 'To', 'AP1', 'PB', 'St', 'CarAV', 'DrAV', 'G', 'Cmp',
                             'Att', 'Yds', 'TD', 'Int', 'Rec', 'Solo', 'Sk', ''], axis=1)
change_cols = ['Pick', 'Age']
for col in change_cols:
    draft_df[col] = pd.to_numeric(draft_df[col])

# Storing data as csv
combine_df.to_csv('../data/combine.csv', header=False)
draft_df.to_csv('../data/draft.csv', header=False)

# Storing data in SQL database
#importing data to postgres psql
import psycopg2
#CONNECT TO YOUR OWN PSQL POSTGRES DOCKER CONTAINER
conn = psycopg2.connect(dbname=USERNAME, host='localhost', user='postgres', password=PASSWORD)                                            
cur = conn.cursor()                                                                                                                           

query = ''' 
    CREATE TABLE draft ( 
        id integer, 
        year integer,
        pick integer,
        team varchar(5), 
        name varchar(50), 
        pos varchar(5), 
        age float, 
        college varchar(50) 
    ); ''' 
cur.execute(query)

query = ''' 
    COPY draft 
    FROM '/home/data/Capstone1/NFL_Draft_Analysis/data/draft.csv'
    DELIMITER ',' 
    CSV; ''' 
cur.execute(query)

query = ''' 
    CREATE TABLE combine ( 
        id integer, 
        year integer, 
        name varchar(50), 
        college varchar(50), 
        pos varchar(5), 
        height_in float, 
        weight_lb float, 
        wonderlic integer, 
        forty_yard float, 
        bench_press integer, 
        vert_leap_in float, 
        broad_jump_in float, 
        shuttle float, 
        three_cone float 
    ); ''' 
cur.execute(query)

query = '''  
    COPY combine  
    FROM '/home/data/Capstone1/NFL_Draft_Analysis/data/combine.csv' 
    DELIMITER ','  
    CSV;  '''  
cur.execute(query)
conn.commit() 
conn.close()
