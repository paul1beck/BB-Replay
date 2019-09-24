
import xml.etree.cElementTree as et
import pandas as pd
import numpy as np


rolls = {
  -1: 'Unknown',
  0:'Move',
  1:'GFI',
  2:'Dodge',
  3:'Armor',
  4:'Injury',
  5:'Block',
  7:'Pickup',
  8:'CasualtyRoll',
  9:'Catch',
  10:'Kickoff',
  12:'Pass',
  13:'Push',
  14:'FollowUp',
  19:'Touchback',
  20:'Bonehead', 
  22:'WildAnimal', 
  23:'Loner',
  29:'Dauntless',
  36:'Leap', 
  46:'HypnoticGaze',
  58:'MoveToBall',
  59:'PilingOnArmour', # ?
  60:'PilingOnInjury', # ?
  1000:'EndTurn',
  1001:'Touchdown',
  1002:'KickoffEvent',
  1003:'Blitz',
  1004:'KickBall',
  1005:'BallAction',
  2000:'Foul'
}

def unnesting(df, explode):
    idx = df.index.repeat(df[explode[0]].str.len())
    df1 = pd.concat([pd.DataFrame({x:np.concatenate(df[x].values)}) for x in explode], axis=1)
    df1.index = idx
    return df1.join(df.drop(explode, 1), how='left')



def extends_iloc(df):
    cols_to_flatten = [colname for colname in df.columns if isinstance(df.iloc[0][colname],list)]
    lens = df[cols_to_flatten[0]].apply(len)
    vals = range(df.shape[0])
    ilocations=np.repeat(vals,lens)
    with_idx=[(i,c) for (i,c) in enumerate(df.columns) if c not in cols_to_flatten]
    col_idxs=list(zip(*with_idx)[0])
    new_df=df.iloc[ilocations, col_idxs].copy()
    for col_target in cols_to_flatten:
        col_flat = [item for sublist in df[col_target] for item in sublist]
        new_df[col_target]=col_flat
    return new_df
 
def extends_iloc_test(df):
    cols_to_flatten = ['RollType','ListDices']
    lens = df[cols_to_flatten[0]].apply(len)
    vals = range(df.shape[0])
    ilocations=np.repeat(vals,lens)
    col_idxs=['PlayerId','Requirement','Reroll','GameTurn']
    new_df=df.iloc[ilocations, col_idxs].copy()
    for col_target in cols_to_flatten:
        col_flat = [item for sublist in df[col_target] for item in sublist]
        new_df[col_target]=col_flat
    return new_df    

def unroll(node, find):
    value=[]
    for x in node.iterfind('.//'+find):
        if find=='RollType' and x.text in ('14','13'):
            pass
        else: value.append(x.text)
    if find=='PlayerId' and len(value)>1:
        value = value[0]
    return value[0] if len(value)==1 else value if len(value)>1 else None


def main():
    """ main """
    parsed_xml = et.parse("bbreplay.xml")
    dfcols = ['PlayerId','Requirement','RollType','ListDices','Reroll','GameTurn']
    findcols = ['PlayerId','Requirement','RollType','ListDices','Reroll']
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
    df_xml = df_xml.dropna(thresh=3).reset_index(drop=True)
    return df_xml

 
test = main()
test2 = extends_iloc_test(test)