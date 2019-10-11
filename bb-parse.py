import xml.etree.cElementTree as et
import pandas as pd
import copy

from utilities import add_roll_name



def flatten_rolltype(df):
    new_df = pd.DataFrame()
    for index, row in df.iterrows():
        if type(row['RollType'])==str:
            row['RollName']=add_roll_name(row['RollType'])
            new_df = new_df.append(row)
        else:
            for x in range(len(row['RollType'])):
                breakout_row = copy.deepcopy(row)
                breakout_row['RollType'] = row['RollType'][x]
                breakout_row['ListDices'] = row['ListDices'][x] if row['ListDices']!=None else None
                breakout_row['Requirement'] = row['Requirement'][x] if type(row['Requirement'])==list else row['Requirement']
                breakout_row['RollName']=add_roll_name(row['RollType'][x])
                new_df = new_df.append(breakout_row)
    return new_df.reset_index(drop=True)

def unroll(node, find):
    value=[]
    for x in node.iterfind('.//'+find):
        if find=='RollType' and x.text in ('14','13'):
            pass
        else: value.append(x.text)
    if find=='PlayerId' and len(value)>1:
        value = value[0]
    return value[0] if len(value)==1 else tuple(value) if len(value)>1 else None


def main():
    """ main """
    parsed_xml = et.parse("bbreplay.xml")
    dfcols = ['PlayerId','Requirement','RollType','ListDices','Reroll','IsOrderCompleted','GameTurn']
    findcols = ['PlayerId','Requirement','RollType','ListDices','Reroll','IsOrderCompleted']
    df_xml = pd.DataFrame(columns=dfcols)
 
    for node in parsed_xml.getroot():
        for action in node.iterfind('./RulesEventBoardAction'):
            items = []
            for col in findcols:
                items.append(unroll(action,col))
            items.append(unroll(node, 'GameTurn'))
            df_xml = df_xml.append(
                pd.Series(items, index=dfcols),
                ignore_index=True)
    df_xml = df_xml.dropna(subset=['RollType','ListDices']).reset_index(drop=True)
    return df_xml

 
test = main()
test2 = flatten_rolltype(test)
test3 = test2.dropna(subset=['IsOrderCompleted']).reset_index(drop=True)