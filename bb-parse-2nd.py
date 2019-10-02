
import xml.etree.cElementTree as et
import pandas as pd
import numpy as np
import copy

""" File attempting to clean up code and increase efficiency of the original"""

rolls = {
  '-1': 'Unknown',
  '0':'Move',
  '1':'GFI',
  '2':'Dodge',
  '3':'Armor',
  '4':'Injury',
  '5':'Block',
  '6':'Standup',
  '7':'Pickup',
  '8':'CasualtyRoll',
  '9':'Catch',
  '10':'Kickoff',
  '12':'Pass',
  '13':'Push',
  '14':'FollowUp',
  '16':'Intercept',
  '17':'WakeUpKO',
  '19':'Touchback',
  '20':'Bonehead',
  '21':'ReallyStupid',
  '22':'WildAnimal', 
  '23':'Loner',
  '24':'Landing',
  '25':'Regeneration',
  '26':'InaccuratePass',
  '27':'AlwaysHungry',
  '29':'Dauntless',
  '31':'Jumpup',
  '36':'Leap', 
  '37':'FoulAppearance',
  '38':'Tentacles',
  '39':'Chainsaw',
  '40':'TakeRoot',
  '44':'DivingTackle',
  '45':'Pro',
  '46':'HypnoticGaze',
  '50':'BloodLust',
  '52':'Bribe',
  '55':'LightningBolt',
  '56':'ThrowTeamMate',
  '58':'MoveToBall',
  '59':'PilingOnArmour', # ?
  '60':'PilingOnInjury', # ?
  '72':'ImpactOfTheBomb',
  '1000':'EndTurn',
  '1001':'Touchdown',
  '1002':'KickoffEvent',
  '1003':'Blitz',
  '1004':'KickBall',
  '1005':'BallAction',
  '2000':'Foul',
}

def add_roll_name(num):
    '''Uses rolls dictionary to match against the roll value in the export'''
    for x in rolls.keys():
        if x==num:
            return rolls[x]

def add_player_name(frame, names):
    '''Uses name dictionary to update player names'''
    pass


#def flatten_rolltype(df):
#    new_df = pd.DataFrame()
#    for index, row in df.iterrows():
#        if type(row['RollType'])==str:
#            row['RollName']=add_roll_name(row['RollType'])
#            new_df = new_df.append(row)
#        else:
#            for x in range(len(row['RollType'])):
#                breakout_row = copy.deepcopy(row)
#                breakout_row['RollType'] = row['RollType'][x]
#                breakout_row['ListDices'] = row['ListDices'][x] if row['ListDices']!=None else None
#                breakout_row['Requirement'] = row['Requirement'][x] if type(row['Requirement'])==list else row['Requirement']
#                breakout_row['RollName']=add_roll_name(row['RollType'][x])
#                new_df = new_df.append(breakout_row)
#    return new_df.reset_index(drop=True)

def unroll(node, find):
    '''Takes each XML node, searches for 'find' namespace and returns a list'''
    value=[]
    for x in node.iterfind('.//'+find):
#        if find=='RollType' and x.text in ('14','13'):
#            pass
#        else: value.append(x.text)
        value.append(x.text)
    if find=='PlayerId' and len(value)>0:
        value = value[0]
    return value if len(value)>0 else None


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
    df_xml = df_xml.dropna(subset=['RollType']).reset_index(drop=True)
    return df_xml

 
test = main()
