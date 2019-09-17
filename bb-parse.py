import pandas as pd
import xml.etree.ElementTree as et


xml_example = 'bbreplay.xml'

'''
rolls = {
  Unknown = -1,
  Move = 0,
  GFI = 1,
  Dodge = 2,
  Armor = 3,
  Injury = 4,
  Block = 5,
  Pickup=7,
  CasualtyRoll=8,
  Catch=9,
  Kickoff=10,
  Pass = 12,
  Push = 13,
  FollowUp = 14,
  Touchback = 19,
  Bonehead=20, 
  WildAnimal=22, 
  Loner=23,
  Dauntless = 29, 
  Leap=36, 
  HypnoticGaze=46,
  MoveToBall = 58, 
  PilingOnArmour = 59, //?
  PilingOnInjury = 60, //?
  EndTurn = 1000,
  Touchdown = 1001,
  KickoffEvent = 1002,
  Blitz = 1003,
  KickBall = 1004,
  BallAction = 1005,
  Foul = 2000
}
'''

root = et.parse(xml_example).getroot()
tags = {"tags":[]}


def unroll(data):
    '''takes xml root and pulls out every child item'''
    value = {}
    for x in data.findall(".//"):
        if x.text == None:
            unroll(x)
        else: value[x.tag] = x.text
    return value

def unroll2(data):
    frame = {}
    for x in data.findall(".//"):
        value = {}
        if x.text == None:
            unroll(x)
        else: 
            value[x.tag] = x.text
            frame.update(value)
    return frame

#for action in root.iter('RulesEventBoardAction'):
#    stuff = unroll(action)
#    print(stuff)

df=pd.DataFrame()

indexloc=0

for action in root:
    stuff = unroll(action)
    indexloc=+1
#    df.append(pd.DataFrame.from_dict(stuff, orient="columns", index=indexloc))
    df.append(pd.DataFrame.from_dict(stuff, orient="index"))