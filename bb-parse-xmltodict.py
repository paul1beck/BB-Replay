import xmltodict
import pandas as pd
from pandas.io.json import json_normalize

with open('bbreplay.xml') as fd:
    doc = xmltodict.parse(fd.read())

steps = doc['Replay']['ReplayStep']

items = []
for row in steps:
    if 'RulesEventBoardAction' in row.keys():
        if type(row['RulesEventBoardAction'])==list:
            for reba_item in row['RulesEventBoardAction']:
                items.append(reba_item['Results'])
        else:
            items.append(row['RulesEventBoardAction']['Results'])

#need to parse out BoardActionResult


test = json_normalize(items)
test.rename(columns=lambda x: x.split(".")[-1], inplace=True)

# #Used to get a list of columns
# header = []
# for col in test.columns:
#     header.append(col)
# print(header)

##Example of 
# test2 = test[['RequestType', 'ActionType','BoardActionResult', 'ListModifiers', 'IsOrderCompleted', 'RollType', 'ListDices', 'ListSkills', 'PlayerId', 'ConcernedTeam', 'SubResultType', 'Requirement', 'RequestType', 'Skill', 'Type', 'Value', 'ResultType', 'Reroll', 'PlayerId', 'SkillId', 'DiceModifier','RollStatus']]