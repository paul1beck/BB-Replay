
import xml.etree.cElementTree as et
import pandas as pd

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

 
def unroll(node, find):
    value=None
    for x in node.findall('.//'+find):
        if x.text==None:
            unroll(x, './/'+find)
        else: value=x.text 
    return value


def main():
    """ main """
    parsed_xml = et.parse("bbreplay.xml")
    dfcols = ['PlayerId', 'RequestType', 'Requirement', 'RollType', 'ListDices']
    df_xml = pd.DataFrame(columns=dfcols)
 
    for node in parsed_xml.getroot():
        items = []
        for col in dfcols:
            items.append(unroll(node,col))

        df_xml = df_xml.append(
            pd.Series(items, index=dfcols),
            ignore_index=True)
    return df_xml

 
test = main()