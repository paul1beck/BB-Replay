import xmltodict
import pandas as pd
import copy
import ast
from pandas.io.json import json_normalize
from collections import OrderedDict
import utilities

pd.options.mode.chained_assignment = None

with open('bbreplay.xml') as fd:
    doc = xmltodict.parse(fd.read())
    
# with open('Coach-170381-a866b2cdfd9c45a1887d0f54b264bfef_2020-02-02_20_24_01.xml') as fd:
#     doc = xmltodict.parse(fd.read())
    
turns = doc['Replay']['ReplayStep']

items = []
for row in turns:

    if 'BoardState' in row.keys():
        turn=[]
        for tstate in row['BoardState']['ListTeams']['TeamState']:
            if 'GameTurn' in tstate.keys():
                turn.append(tstate['GameTurn'])
        row['Turn']=turn
        
    if 'RulesEventSpecialAction' in row.keys():
        row.pop('RulesEventSpecialAction')

    if 'RulesEventKickOffTable' in row.keys():
        breakout_row = copy.deepcopy(row)
        event=''
        if 'Event' in breakout_row['RulesEventKickOffTable'].keys():
            event=breakout_row['RulesEventKickOffTable']['Event']

        if 'RulesEventBoardAction' in breakout_row.keys():
            breakout_row.pop('RulesEventBoardAction')
        breakout_row = OrderedDict({'RulesEventBoardAction':
                                    {'ActionType': '7','Results': 
                                     {'BoardActionResult': 
                                      {'RollType': '', 'ResultType': event, 'CoachChoices':
                                       {'ListDices': breakout_row['RulesEventKickOffTable']['ListDice']},
                                       }}}})
        items.append(breakout_row)
        row.pop('RulesEventKickOffTable')

    if 'RulesEventBoardAction' in row.keys():
        if type(row['RulesEventBoardAction'])==list:
            for reba_item in row['RulesEventBoardAction']:
                breakout_row = copy.deepcopy(row)
                breakout_row['RulesEventBoardAction'] = reba_item
                items.append(breakout_row)
        else:
            items.append(row)

parse = []
for item in items:
    if 'Results' in item['RulesEventBoardAction'].keys():    
        if type(item['RulesEventBoardAction']['Results']['BoardActionResult'])==list:
            for stuff in item['RulesEventBoardAction']['Results']['BoardActionResult']:
                breakout_stuff = copy.deepcopy(item)
                breakout_stuff['RulesEventBoardAction']['Results']['BoardActionResult'] = stuff
                parse.append(breakout_stuff)
        else:
            parse.append(item)
        
test = json_normalize(parse)
test2 = test[["Turn","RulesEventBoardAction.ActionType","RulesEventBoardAction.Results.BoardActionResult.IsOrderCompleted","RulesEventBoardAction.Results.BoardActionResult.RollType","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListDices","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ConcernedTeam","RulesEventBoardAction.PlayerId","RulesEventBoardAction.Results.BoardActionResult.SubResultType","RulesEventBoardAction.Results.BoardActionResult.Requirement","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Type","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Value","RulesEventBoardAction.Results.BoardActionResult.ResultType","RulesEventCoachChoice.IndexChosen","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.SkillId","RulesEventBoardAction.Results.BoardActionResult.RollStatus","BoardState.ActiveTeam"]]
test2.rename(columns=lambda x: x.split(".")[-1], inplace=True)
test2.drop(test2[(test2.IsOrderCompleted!='1') & (test2.RollType!='5')].index, inplace=True)
test2.drop(test2[(test2.RollType=='13') | (test2.RollType=='14') | (test2.RollType=='62')].index, inplace=True)
test2['ActionDesc'] = test2['ActionType'].fillna("").apply(utilities.actionDesc)
test2['RollDesc'] = test2['RollType'].fillna("").apply(utilities.rollDesc)
test2['ReRollStatus'] = test2['RollStatus'].fillna("").apply(utilities.rerollStatus)
test2['ListDices'] = test2['ListDices'].fillna('[""]').apply(ast.literal_eval)
test2 = test2.dropna(subset=['RollType','ListDices']).reset_index(drop=True)

team_data = pd.DataFrame()
for team in turns[-2]['BoardState']['ListTeams']['TeamState']:
    for player_obj in team['ListPitchPlayers']['PlayerState']:
        player = json_normalize(player_obj['Data'])
        player['Team'] = team['Data']['Name']
        player['IdRace'] = team['Data']['IdRace']
        team_data = team_data.append(player, ignore_index = True)
        
team_data['TeamId'] = team_data['TeamId'].fillna(0)
team_data['Race'] = team_data['IdRace'].fillna("").apply(utilities.raceLabel)
team_data.rename(columns={'Id':'PlayerId'}, inplace=True)
team_merge = team_data[['PlayerId',"IdPlayerTypes","Name","Team","Race"]]

combine = pd.merge(test2, team_merge, how="left", on="PlayerId", )

export_file = combine[['Turn','ActiveTeam','ConcernedTeam','Team','Name','Race','IdPlayerTypes','ActionDesc','RollDesc','ListDices','Requirement','SubResultType','ReRollStatus','IsOrderCompleted']]
#'Type','Value','ResultType','IndexChosen','SkillId','RollStatus'
export_csv = export_file.to_csv (r'replay_export.csv', index = None, header=True)