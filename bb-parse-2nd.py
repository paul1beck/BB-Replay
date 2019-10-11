import xml.etree.cElementTree as et
import pandas as pd
import copy
from ast import literal_eval

from utilities import add_roll_name

""" File attempting to clean up code and increase efficiency of the original"""

def add_player_name(frame, names):
    '''Uses name dictionary to update player names'''
    pass


def find_in_xml(node, name):
    """Takes each XML node, searches for 'name' in namespace and returns a list"""
    value=[]
    for x in node.iterfind('.//'+name):
        if name=='RollType' and x.text in ('14','13'):
            pass
        elif name=='ListDices':
            value.append(literal_eval(x.text))
        else: value.append(x.text)
    if name=='PlayerId' and len(value)>1:
        value = [value[0]]
    return value[0] if len(value)==1 else tuple(value) if len(value)>1 else None

def clean_block_dice(dice):
    """Removes the 2nd half of the dice in the list as they are not used"""
    return dice[:int(len(dice)/2)]

def main():
    """ main """
    parsed_xml = et.parse("bbreplay.xml")
    dfcols = ['Requirement','RollType','ListDices','Reroll','IsOrderCompleted','GameTurn','PlayerId']
    findcols = ['Requirement','RollType','ListDices','Reroll','IsOrderCompleted']
    df_xml = pd.DataFrame(columns=dfcols)
 
    for node in parsed_xml.getroot():
        for action in node.iterfind('./RulesEventBoardAction'):
            items = {}
            for col in findcols:
                items[action] = find_in_xml(action,col)
            items['GameTurn'] = find_in_xml(node, 'GameTurn')
            items['PlayerId'] = find_in_xml(node, 'PlayerId')
            if type(items[1])==tuple:
                print(items[1])
            if items[1]=='5':
                items[2]=clean_block_dice(items[2])
            if items[2]==None:
                pass
            elif type(items[2])==int:
                df_xml = df_xml.append(
                    pd.Series(items, index=dfcols),
                    ignore_index=True)
            elif len(items[2])>1 and type(items[2])==tuple:
                breakout_row = copy.deepcopy(items)
#                print(breakout_row)
                df_xml = df_xml.append(
                    pd.Series(breakout_row, index=dfcols),
                    ignore_index=True)

    df_xml = df_xml.dropna(subset=['RollType']).reset_index(drop=True)
    return df_xml

 
test = main()
