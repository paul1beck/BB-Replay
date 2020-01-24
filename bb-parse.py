import xml.etree.cElementTree as et
import pandas as pd
import copy

from utilities import add_roll_name

def flatten_rolltype(df):
    new_df = pd.DataFrame()
    for index, row in df.iterrows():
        if type(row['RollType'])==str:
            row['RollName']=add_roll_name('rolls',row['RollType'])
            new_df = new_df.append(row)
        else:
            for x in range(len(row['RollType'])):
                breakout_row = copy.deepcopy(row)
                breakout_row['RollType'] = row['RollType'][x]
                breakout_row['ListDices'] = row['ListDices'][x] if row['ListDices']!=None else None
                breakout_row['Requirement'] = breakout('Requirement',x,row)
                breakout_row['IsOrderCompleted'] = breakout('IsOrderCompleted',x,row)
                breakout_row['ResultType']=breakout('ResultType',x,row)
                breakout_row['RollName']=add_roll_name('rolls',row['RollType'][x])
                if row['ResultType']==None:
                    pass
                else:
                    breakout_row['Roll Result']=add_roll_name('result_type',row['ResultType'][x])
                new_df = new_df.append(breakout_row)
    return new_df.reset_index(drop=True)

def unroll(node, find):
    value=[]
    for x in node.iterfind('.//'+find):
        if find=='RollType' and x.text in ('14','13'):
            pass
        elif x.text==None:
            value.append(0)
        else: value.append(x.text)
    if find=='PlayerId' and type(value)==list and len(value)>1:
        value = [value[0]]
    return value[0] if len(value)==1 else tuple(value) if len(value)>1 else None

def breakout(header,x,data):
    if data[header]==None:
        return None
    elif len(data[header])==len(data['RollType']):
        return data[header][x]
    else:
        return data[header]

def main():
    """ main """
    parsed_xml = et.parse("bbreplay.xml")
    dfcols = ['Requirement','RollType','ListDices','RollStatus','ResultType','IsOrderCompleted','PlayerId','GameTurn']
    findcols = ['Requirement','RollType','ListDices','RollStatus','ResultType','IsOrderCompleted']
    df_xml = pd.DataFrame(columns=dfcols)
 
    for node in parsed_xml.getroot():
        for action in node.iterfind('./RulesEventBoardAction'):
            items = []
            for col in findcols:
                items.append(unroll(action,col))
            items.append(unroll(node, 'PlayerId'))
            items.append(unroll(node, 'GameTurn'))
            df_xml = df_xml.append(
                pd.Series(items, index=dfcols),
                ignore_index=True)
    df_xml = df_xml.dropna(subset=['RollType','ListDices']).reset_index(drop=True)
    return df_xml

 
test = main()
test2 = flatten_rolltype(test)
test3 = test2.dropna(subset=['IsOrderCompleted']).reset_index(drop=True)

def players():
    player_cols = ['TeamId','Name','IdPlayerTypes','Id','ListSkills']
    player_list = pd.DataFrame()
    parsed_xml = et.parse("bbreplay.xml")
    for node in parsed_xml.getroot():
        player_data = node.iterfind('.//PlayerData')
        for player in player_data:
            player_info=[]
            for col in player_cols:
                player_info.append(unroll(player,col))
            player_list = player_list.append(pd.Series(player_info, index=player_cols), ignore_index=True)
    player_list['TeamId'].fillna(0, inplace = True)
    return player_list

#ptest = players() 

