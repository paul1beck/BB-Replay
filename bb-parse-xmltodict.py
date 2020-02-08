import xmltodict
import pandas as pd
import copy
from pandas.io.json import json_normalize
from collections import OrderedDict
import utilities

with open('bbreplay.xml') as fd:
    doc = xmltodict.parse(fd.read())

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
test2 = test[["Turn","RulesEventBoardAction.ActionType","RulesEventBoardAction.Results.BoardActionResult.IsOrderCompleted","RulesEventBoardAction.Results.BoardActionResult.RollType","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListDices","BoardState.KickOffTeam","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ConcernedTeam","RulesEventBoardAction.PlayerId","RulesEventEndTurn.TouchdownScorer","RulesEventBoardAction.Results.BoardActionResult.SubResultType","RulesEventBoardAction.Results.BoardActionResult.Requirement","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Type","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Value","RulesEventBoardAction.Results.BoardActionResult.ResultType","RulesEventCoachChoice.IndexChosen","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.PlayerId","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.SkillId","RulesEventBoardAction.Results.BoardActionResult.RollStatus","RulesEventWaitingRequest.ConcernedTeam","BoardState.ActiveTeam","RulesEventEndTurn.Turnover"]]
test2.rename(columns=lambda x: x.split(".")[-1], inplace=True)
test2['ActionDesc'] = test2['ActionType'].fillna("").apply(utilities.actionDesc)
test2['RollDesc'] = test2['RollType'].fillna("").apply(utilities.rollDesc)
export_csv = test2.to_csv (r'replay_export.csv', index = None, header=True)