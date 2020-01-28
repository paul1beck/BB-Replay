import xmltodict
import pandas as pd
from pandas.io.json import json_normalize

with open('bbreplay.xml') as fd:
    doc = xmltodict.parse(fd.read())

steps = doc['Replay']['ReplayStep']

items = []
for row in steps:
    if 'RulesEventBoardAction' in row.keys():
        for action in row['RulesEventBoardAction']:
            items.append(action)

filtered_items = []
for row in items:
    if type(row)==str:
        pass
    else:
        filtered_items.append(row)

things = []
for thing in filtered_items:
    for rows in thing['Results']['BoardActionResult']:
        things.append(rows)
test = json_normalize(things,max_level=50)
