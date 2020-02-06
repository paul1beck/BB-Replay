import xmltodict
import pandas as pd
import copy
from pandas.io.json import json_normalize
from collections import OrderedDict

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
        rekot_items.append(row)
        # breakout_row = copy.deepcopy(row)
        # if 'RulesEventBoardAction' in breakout_row.keys():
        #     breakout_row.pop('RulesEventBoardAction')
        # breakout_row = OrderedDict({'RulesEventBoardAction':
        #                             OrderedDict({'Results':
        #                                         OrderedDict({'BoardActionResult': row['RulesEventSpecialAction']})})})
        # items.append(breakout_row)
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
# # test.rename(columns=lambda x: x.split(".")[-1], inplace=True)
# test.drop(columns=['RequestType','CellTo','CellFrom','ListModifiers'])
# test2 = test[['ActionType','IsOrderCompleted','RollType','ListDices','ConcernedTeam',
#              'PlayerId','ListDice','TouchdownScorer','SubResultType','Requirement',
#              'ResultType','Reroll','IndexChosen','Turnover','PlayingTeam']]
# test2 = test[["RulesEventBoardAction.ActionType","RulesEventBoardAction.Results.BoardActionResult.IsOrderCompleted","RulesEventBoardAction.Results.BoardActionResult.RollType","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListDices","BoardState.KickOffTeam","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ConcernedTeam","RulesEventBoardAction.PlayerId","RulesEventKickOffTable.ListDice","RulesEventKickOffTable.Event","RulesEventEndTurn.TouchdownScorer","RulesEventBoardAction.Results.BoardActionResult.SubResultType","RulesEventBoardAction.Results.BoardActionResult.Requirement","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Type","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Value","RulesEventBoardAction.Results.BoardActionResult.ResultType","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.Reroll","RulesEventCoachChoice.IndexChosen","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.PlayerId","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.SkillId","RulesEventBoardAction.Results.BoardActionResult.RollStatus","RulesEventWaitingRequest.ConcernedTeam","BoardState.ActiveTeam","RulesEventEndTurn.Turnover"]]
test2 = test[["RulesEventBoardAction.ActionType","RulesEventBoardAction.Results.BoardActionResult.IsOrderCompleted","RulesEventBoardAction.Results.BoardActionResult.RollType","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListDices","BoardState.KickOffTeam","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ConcernedTeam","RulesEventBoardAction.PlayerId","RulesEventEndTurn.TouchdownScorer","RulesEventBoardAction.Results.BoardActionResult.SubResultType","RulesEventBoardAction.Results.BoardActionResult.Requirement","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Type","RulesEventBoardAction.Results.BoardActionResult.ListModifiers.DiceModifier.Value","RulesEventBoardAction.Results.BoardActionResult.ResultType","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.Reroll","RulesEventCoachChoice.IndexChosen","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.PlayerId","RulesEventBoardAction.Results.BoardActionResult.CoachChoices.ListSkills.SkillInfo.SkillId","RulesEventBoardAction.Results.BoardActionResult.RollStatus","RulesEventWaitingRequest.ConcernedTeam","BoardState.ActiveTeam","RulesEventEndTurn.Turnover"]]
#RulesEventSpecialAction.PlayerId RulesEventSpecialAction.ActionType for dodges?
