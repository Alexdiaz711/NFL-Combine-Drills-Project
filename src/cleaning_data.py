from pymongo import MongoClient
import pandas as pd
import numpy as np

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

#cleaning player names from draft
draft_df['Player'] = draft_df['Player'].str.strip(' HOF')
draft_df['Player'] = draft_df['Player'].str.upper()
combine_df['Name'] = combine_df['Name'].str.upper()
draft_df = draft_df.replace('EATH SHULER', 'HEATH SHULER')
draft_df = draft_df.replace('ENRY FORD', 'HENRY FORD')
draft_df = draft_df.replace("TRE' JOHNSON", 'TRE JOHNSON')
draft_df = draft_df.replace("J.J. STOKES", 'J J STOKES')
draft_df = draft_df.replace("RUBEN BROWN", 'REUBEN BROWN')
draft_df = draft_df.replace("UGH DOUGLAS", 'HUGH DOUGLAS')
draft_df = draft_df.replace("DEVIN BUS", 'DEVIN BUSH')
combine_df.loc[580, 'Name'] = 'JAMES STEWART 1'
draft_df.loc[240, 'Player'] = 'JAMES STEWART 1'
combine_df.loc[658, 'Name'] = 'REGGIE BROWN 1'
draft_df.loc[487, 'Player'] = 'REGGIE BROWN 1'
draft_df = draft_df.replace("RLANDO PACE", 'ORLANDO PACE')
draft_df = draft_df.replace("ANTOWAIN SMIT", 'ANTOWAIN SMITH')
draft_df = draft_df.replace("RYAN LEA", 'RYAN LEAF')
draft_df = draft_df.replace("ANDRE WADSWORT", 'ANDRE WADSWORTH')
draft_df = draft_df.replace("RED TAYLOR", 'FRED TAYLOR')
draft_df = draft_df.replace("R.W. MCQUARTERS", 'ROBERT MCQUARTERS')
draft_df = draft_df.replace("MARCUS NAS", 'MARCUS NASH')
draft_df = draft_df.replace("ERNANDO BRYANT", 'FERNANDO BRYANT')
draft_df = draft_df.replace("CHRIS MCINTOS", 'CHRIS MCINTOSH')
draft_df = draft_df.replace("R. JAY SOWARD", 'R.JAY SOWARD')
draft_df = draft_df.replace("JUSTIN SMIT", 'JUSTIN SMITH')
draft_df = draft_df.replace("REDDIE MITCHELL", 'FREDDIE MITCHELL')
draft_df = draft_df.replace("DONTE' STALLWORT", 'DONTE STALLWORTH')
draft_df = draft_df.replace("ALBERT HAYNESWORT", 'ALBERT HAYNESWORTH')
draft_df = draft_df.replace("MIKE RUMP", 'MIKE RUMPH')
draft_df = draft_df.replace("MARC COLOMB", 'MARC COLOMBO')
draft_df = draft_df.replace("YRON LEFTWIC", 'BYRON LEFTWICH')
draft_df = draft_df.replace("WILLIAM JOSEP", 'WILLIAM JOSEPH')
draft_df = draft_df.replace("WILL SMIT", 'WILL SMITH')
draft_df = draft_df.replace("ALEX SMIT", 'ALEX SMITH')
combine_df.loc[3556, 'Name'] = 'ALEX SMITH 1'
draft_df.loc[2737, 'Player'] = 'ALEX SMITH 1'
combine_df.loc[3435, 'POS'] = 'OLB'
combine_df = combine_df.drop([3434])
draft_df = draft_df.replace("ABIAN WASHINGTON", 'FABIAN WASHINGTON')
draft_df = draft_df.replace("EATH MILLER", 'HEATH MILLER')
draft_df = draft_df.replace("D'BRICKASHAW FERGUSON", 'DBRICKASHAW FERGUSON')
draft_df = draft_df.replace("ALOTI NGATA", 'HALOTI NGATA')
draft_df = draft_df.replace("ELIX JONES", 'FELIX JONES')
draft_df = draft_df.replace("AKEEM NICKS", 'HAKEEM NICKS')
draft_df = draft_df.replace("JONATHAN BALDWIN", 'JON BALDWIN')
combine_df.loc[5988, 'Name'] = 'ROBERT GRIFFIN III'
draft_df.loc[4520, 'Player'] = 'ROBERT GRIFFIN III'
draft_df = draft_df.replace("LETCHER COX", 'FLETCHER COX')
draft_df = draft_df.replace("ARRISON SMITH", 'HARRISON SMITH')
draft_df = draft_df.replace("EZEKIEL ANSAH", 'EZEKIAL ANSAH')
draft_df = draft_df.replace("EJ MANUEL", 'E.J. MANUEL')
draft_df = draft_df.replace("DELL BECKHAM", 'ODELL BECKHAM')
combine_df = combine_df.drop([6804])
draft_df = draft_df.replace("JA'WUAN JAMES", "JAWUAN JAMES")
draft_df = draft_df.replace("A HA CLINTON-DIX", "HAHA CLINTON-DIX")
draft_df = draft_df.replace("MARCUS SMIT", "MARCUS SMITH")
draft_df = draft_df.replace("BRANDON SCHER", "BRANDON SCHERFF")
combine_df.loc[7747, 'Name'] = 'KEVIN WHITE 1'
draft_df.loc[5288, 'Player'] = 'KEVIN WHITE 1'
draft_df = draft_df.replace("BUD DUPREE", "ALVIN DUPREE")
draft_df = draft_df.replace("JARED G", "JARED GOFF")
draft_df = draft_df.replace("KARL JOSEP", "KARL JOSEPH")
draft_df = draft_df.replace("PAXTON LYNC", "PAXTON LYNCH")
draft_df = draft_df.replace("EMMANUEL OGBA", "EMMANUEL OGBAH")
draft_df = draft_df.replace("AASON REDDICK", "HAASON REDDICK")
draft_df = draft_df.replace("ADOREE' JACKSON", "ADOREE JACKSON")
draft_df = draft_df.replace(".J. HOWARD", "O.J. HOWARD")
draft_df = draft_df.replace("TRE'DAVIOUS WHITE", "TREDAVIOUS WHITE")
draft_df = draft_df.replace("ROQUAN SMIT", "ROQUAN SMITH")
draft_df = draft_df.replace("DA'RON PAYNE", "DARON PAYNE")
draft_df = draft_df.replace("LEIGHTON VANDER ESC", "LEIGHTON VANDER ESCH")
draft_df = draft_df.replace("RANK RAGNOW", "FRANK RAGNOW")
draft_df = draft_df.replace("AYDEN HURST", "HAYDEN HURST")
combine_df.loc[9119, 'Name'] = 'MIKE HUGHES 1'
draft_df.loc[6073, 'Player'] = 'MIKE HUGHES 1'


#joining dataframes and marking 1st round picks
for i in range(1994, 2020):
    combine = combine_df[combine_df['Year']==i]
    draft = draft_df[draft_df['Year']==i]
    temp = combine.merge(draft, how='left', left_on='Name', right_on='Player')
    temp.loc[temp['Pick'] <= 32, '1RD Pick'] = 1
    temp.loc[temp['Pick'] > 32, '1RD Pick'] = 0
    temp['1RD Pick'] = temp['1RD Pick'].fillna(0)
    if i == 1994:
        joined = temp.copy()
    else:
        joined = joined.append(temp)
joined = joined.reset_index()

#organizing and cleaning player posiiton groups
for i, pos in enumerate(joined['POS']):
    if type(joined['Pos'][i]) != float:
        joined.POS[i] = joined.Pos[i]        
joined = joined.drop('Pos', axis=1)
for i, pos in enumerate(joined['POS']):
    if joined['POS'][i] in ['FS', 'SS']:
        joined.POS[i] = 'S'        
for i, pos in enumerate(joined['POS']):
    if joined['POS'][i] in ['OT','OL', 'G', 'C', 'LS']:
        if (joined['POS'][i]=='OL' and joined['Height (in)'][i]>=77) or joined['POS'][i] == 'OT':
            joined.POS[i] = 'T'         
        else:
            joined.POS[i] = 'IOL'            
for i, pos in enumerate(joined['POS']):
    if joined['POS'][i] in ['EDG']:
        joined.POS[i] = 'DE'
for i, pos in enumerate(joined['POS']):
    if joined['POS'][i] in ['OLD', 'ILB']:
        joined.POS[i] = 'LB'        
for i, pos in enumerate(joined['POS']):
    if joined['POS'][i] in ['NT']:
        joined.POS[i] = 'DT'        
for i, pos in enumerate(joined['POS']):
    if joined['POS'][i] in ['DL']:
        if joined['Weight (lbs)'][i]>=285:
            joined.POS[i] = 'DT'         
        else:
            joined.POS[i] = 'DE'      
for i, pos in enumerate(joined['POS']):
    if joined['POS'][i] in ['FB']:
        joined.POS[i] = 'RB'        
for i, pos in enumerate(joined['POS']):
    if joined['POS'][i] in ['DB']:
        joined.POS[i] = 'CB'
positions = joined['POS'].unique()


# Renaming columns and droping unneeded Columns
joined = joined.rename(columns={'Year_x': 'Year',
    'POS': 'Pos',
    '40 Yard': '40 Yard Dash (sec)',
    'Bench Press': 'Bench Press (reps @ 225 lbs)',
    'Vert Leap (in)': 'Vertical Leap (in)',
    'Shuttle': 'Shuttle Drill (sec)',
    '3Cone': '3 Cone Drill (sec)'})
joined = joined.drop(columns=['index', 'Year_y', 'Player', 'Tm', 'Age', 'College/Univ'])

# Recording samples' data
samples_dict = {}
drills = ['40 Yard Dash (sec)', 'Bench Press (reps @ 225 lbs)', 'Vertical Leap (in)', 
    'Broad Jump (in)', 'Shuttle Drill (sec)', '3 Cone Drill (sec)']
for drill in drills:
    for i in range(1994, 2020):
        for pos in positions:
            temp = joined[joined['Pos']==pos][joined['Year']==i][[drill, '1RD Pick']]
            num = int(round(temp.count()[0]/10))
            if num < 1:
                num = 1
            if drill in ['40 Yard Dash (sec)', 'Shuttle Drill (sec)', '3 Cone Drill (sec)']:
                top_ten_perc = temp.sort_values(drill)[:num]
            else:
                top_ten_perc = temp.sort_values(drill, ascending=False)[:num]
            sample = [int(x) for x in top_ten_perc['1RD Pick']]                                   
            if drill in samples_dict.keys():
                samples_dict[drill].extend(sample)
            else:
                samples_dict[drill] = sample