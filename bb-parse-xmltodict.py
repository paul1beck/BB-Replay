import xmltodict
import pandas as pd
import copy
from pandas.io.json import json_normalize

with open('bbreplay.xml') as fd:
    doc = xmltodict.parse(fd.read())

turns = doc['Replay']['ReplayStep']

items = []
for row in turns:
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
# test.drop(columns=['RulesEventKickOffChoice.KickOffTeam'])
# # test.rename(columns=lambda x: x.split(".")[-1], inplace=True)
# test.drop(columns=['RequestType','CellTo','CellFrom','ListModifiers'])
# test2 = test[['ActionType','IsOrderCompleted','RollType','ListDices','ConcernedTeam',
#              'PlayerId','ListDice','TouchdownScorer','SubResultType','Requirement',
#              'ResultType','Reroll','IndexChosen','Turnover','PlayingTeam']]

#RulesEventSpecialAction.PlayerId RulesEventSpecialAction.ActionType for dodges?
