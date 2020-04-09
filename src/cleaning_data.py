from pymongo import MongoClient
import pandas as pd
import numpy as np


def cast_columns(df, columns):
    '''
    Takes a list of column names from a Pandas DF
    and casts the values in those columns to floats
    ----------
    Parameters
    ----------
    df : Pandas DataFrame
        A DF from which to cast columns to numeric
    columns : list
        A list of column names form a Panddas DF.
    ----------
    Returns 
    ----------
    None
    '''
    for col in columns:
        df[col] = pd.to_numeric(df[col])


def reorg_positions(inputs, output):
    '''
    Takes a list of player position names and changes a players
    position to the output if their current posiiton is in the
    input list
    ----------
    Parameters
    ----------
    inputs : list
        A list of player position strings
    output : string
        A player position string.
    ----------
    Returns 
    ----------
    None
    '''    
    if pos in inputs:
        joined.loc[i, 'POS'] = output


# Connecting to MongoDB and creating Pandas DF's for final cleaning and joining of tables
client = MongoClient('localhost', 27017)
db = client['draft']
combine = db['combine_results']
draft = db['draft_results'] 
combine_df = pd.DataFrame(list(combine.find()))
draft_df = pd.DataFrame(list(draft.find()))


# Dropping uneeded columns and casting types
combine_df = combine_df.drop('_id', axis=1)
change_cols = ['Year', 'Height (in)', 'Weight (lbs)', 'Wonderlic', '40 Yard', 
                'Bench Press', 'Vert Leap (in)', 'Broad Jump (in)', 'Shuttle', '3Cone']
cast_columns(combine_df, change_cols)

draft_df = draft_df.drop(['_id', 'To', 'AP1', 'PB', 'St', 'CarAV', 'DrAV', 'G', 'Cmp',
                             'Att', 'Yds', 'TD', 'Int', 'Rec', 'Solo', 'Sk', ''], axis=1)
change_cols = ['Pick', 'Age']
cast_columns(draft_df, change_cols)


# Cleaning player names from draft
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


# Joining dataframes and marking 1st round picks
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

# Organizing and cleaning player posiiton groups
for i, pos in enumerate(joined['POS']):
    if type(joined.loc[i, 'Pos']) != float:
        joined.loc[i, 'POS'] = joined.loc[i, 'Pos']
for i, pos in enumerate(joined['POS']):
    reorg_positions(['FS', 'SS'], 'S')
    reorg_positions(['EDG'], 'DE')
    reorg_positions(['OLB', 'ILB'], 'LB')
    reorg_positions(['NT'], 'DT')
    reorg_positions(['FB'], 'RB')
    reorg_positions(['DB'], 'CB')
    if pos in ['OT','OL', 'G', 'C', 'LS']:
        if (pos=='OL' and joined.loc[i, 'Height (in)']>=77) or pos == 'OT':
            joined.loc[i, 'POS'] = 'T'         
        else:
            joined.loc[i, 'POS'] = 'IOL'
    if pos == 'DL':
        if joined.loc[i, 'Weight (lbs)']>=285:
            joined.loc[i, 'POS'] = 'DT'         
        else:
            joined.loc[i, 'POS'] = 'DE'
positions = joined['POS'].unique()


#Dropping remaining uneeded columns and renaming kept columns
joined = joined.drop(columns=['index', 'Year_y', 'Player', 'Tm', 'Pos', 'Age', 'College/Univ'])
joined = joined.rename(columns={'Year_x': 'Year',
    'POS': 'Pos',
    '40 Yard': '40 Yard Dash (sec)',
    'Bench Press': 'Bench Press (reps @ 225 lbs)',
    'Vert Leap (in)': 'Vertical Leap (in)',
    'Shuttle': 'Shuttle Drill (sec)',
    '3Cone': '3 Cone Drill (sec)'})


# creating samples of top performers for each drill
# players are grouped by year and position group
# then top performer in group (or top 10%) are added to sample
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


# Creating dictionaries with sample parameters:
n, p, mean, sd, short_name = {}, {}, {}, {}, {}
for k, v in samples_dict.items():
    n[k] = len(v)
    p[k] = np.mean(v)
    mean[k] = (n[k]*p[k])
    sd[k] = np.sqrt(n[k]*p[k]*(1-p[k]))
    short_name[k] = k.split()[0] + ' ' + k.split()[1]
    print('Top Performers in {}: short_name= {}, n={}, mean={:2.2f}, sd={:2.2f}, p={:2.2f}'
          .format(k, short_name[k], n[k], mean[k], sd[k], p[k]))