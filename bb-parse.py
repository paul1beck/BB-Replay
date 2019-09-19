
import xml.etree.cElementTree as et
import pandas as pd


rolls = {
  -1: 'Unknown',
  0:'Move',
  1:'GFI',
  2:'Dodge',
  3:'Armor',
  4:'Injury',
  5:'Block',
  7:'Pickup',
  8:'CasualtyRoll',
  9:'Catch',
  10:'Kickoff',
  12:'Pass',
  13:'Push',
  14:'FollowUp',
  19:'Touchback',
  20:'Bonehead', 
  22:'WildAnimal', 
  23:'Loner',
  29:'Dauntless',
  36:'Leap', 
  46:'HypnoticGaze',
  58:'MoveToBall',
  59:'PilingOnArmour', # ?
  60:'PilingOnInjury', # ?
  1000:'EndTurn',
  1001:'Touchdown',
  1002:'KickoffEvent',
  1003:'Blitz',
  1004:'KickBall',
  1005:'BallAction',
  2000:'Foul'
}


 
def unroll(node, find):
    value=[]
    for x in node.iterfind('.//'+find):
        if find=='RollType' and x.text in ('14','13'):
            pass
        else: value.append(x.text)
    if find=='PlayerId' and len(value)>1:
        value = value[0]
    return value[0] if len(value)==1 else value if len(value)>1 else None


def main():
    """ main """
    parsed_xml = et.parse("bbreplay.xml")
    dfcols = ['PlayerId', 'Requirement', 'RollType', 'ListDices','Reroll','GameTurn']
    findcols = ['PlayerId', 'Requirement', 'RollType', 'ListDices','Reroll']
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
    df_xml = df_xml.dropna(thresh=3)
    return df_xml

 
test = main()