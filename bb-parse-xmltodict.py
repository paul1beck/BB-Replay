import xmltodict
import pandas as pd
import copy
from pandas.io.json import json_normalize
from collections import OrderedDict
from utilities import actions, rolls

with open('bbreplay.xml') as fd:
    doc = xmltodict.parse(fd.read())

turns = doc['Replay']['ReplayStep']

rekot_items =[]
items = []
for row in turns:
    if 'RulesEventSpecialAction' in row.keys():
        row.pop('RulesEventSpecialAction')
        # reba_items.append(row)
        # breakout_row = copy.deepcopy(row)
        # if 'RulesEventBoardAction' in breakout_row.keys():
        #     breakout_row.pop('RulesEventBoardAction')
        # breakout_row = OrderedDict({'RulesEventBoardAction':
        #                             OrderedDict({'Results':
        #                                         OrderedDict({'BoardActionResult': row['RulesEventSpecialAction']})})})
        # items.append(breakout_row)

    if 'RulesEventKickOffTable' in row.keys():
        breakout_row = copy.deepcopy(row)
        rekot_items.append(breakout_row)
        if 'RulesEventBoardAction' in breakout_row.keys():
            breakout_row.pop('RulesEventBoardAction')
        breakout_row = OrderedDict({'RulesEventBoardAction':
                                    {'Results': 
                                     {'BoardActionResult': 
                                      {'RollType': '7', 'CoachChoices':
                                       {'ListDices': breakout_row['RulesEventKickOffTable']['ListDice']},
                                       }}}}) #Event not in all Kick Off Tables
        items.append(breakout_row)
        # 'ResultType': breakout_row['RulesEventKickOffTable']['Event']
        #"RulesEventKickOffTable.Event" RulesEventBoardAction.Results.BoardActionResult.ResultType
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
test2 = test[["RulesEventBoardAction.ActionType","RulesEventBoardAction.Results.BoardActionResult.IsOrderCompleted","RulesEventBoardAction.Results.BoardActionResult.RollType","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListDices","BoardState.KickOffTeam","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ConcernedTeam","RulesEventBoardAction.PlayerId","RulesEventEndTurn.TouchdownScorer","RulesEventBoardAction.Results.BoardActionResult.SubResultType","RulesEventBoardAction.Results.BoardActionResult.Requirement","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Type","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Value","RulesEventBoardAction.Results.BoardActionResult.ResultType","RulesEventCoachChoice.IndexChosen","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.PlayerId","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.SkillId","RulesEventBoardAction.Results.BoardActionResult.RollStatus","RulesEventWaitingRequest.ConcernedTeam","BoardState.ActiveTeam","RulesEventEndTurn.Turnover"]]
test2.rename(columns=lambda x: x.split(".")[-1], inplace=True)

## Trying to Update data through Utilities
#test2.ActionType = actions(test2.ActionType)
