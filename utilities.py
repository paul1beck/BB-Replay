def add_roll_name(desc, num):
    '''Uses rolls dictionary to match against the roll value in the export'''
    if desc=='rolls':
        for x in rolls.keys():
            if x==num:
                return rolls[x]
    elif desc=='block_dice':
        for x in block_dice.keys():
            if x==num:
                return block_dice[x]
    elif desc=='block_results':
        for x in block_results.keys():
            if x==num:
                return block_results[x]
    elif desc=='roll_status':
        for x in roll_status.keys():
            if x==num:
                return roll_status[x]
    elif desc=='result_type' and num!=None:
        for x in result_type.keys():
            if x==num:
                return result_type[x]

            
def actionDesc(data):
    return actions[data]

def rollDesc(data):
    return rolls[data]

def blockResults(data):
    return block_results[data]

def blockDice(data):
    return block_dice[data]

def rerollStatus(data):
    return roll_status[data]

def raceLabel(data):
    return races[data]

block_dice = {"0": "Skull", "1": "Both Down", "2": "Push", "3": "Stumble", "4": "Pow"}

block_results = {"0":"Attacker Down","1":"Attacker and Defender Down","2":"Wrestle Down","3":"Attacker and Defender Did not Move","4":"Defender Pushed","5":"Attacker in Place, Defender Down","6":"Defender Down"}

roll_status = {"0":"No Re-roll","1":"Team Re-roll","2":"No Re-roll","3":"Skill Re-roll", "4":"Skill Re-roll","":""}

result_type = {"0":"Skill Passed","1":"Failure but no Turnover","2":"Failed with Re-Roll","3":"Failed with no Re-roll"}

rolls = {
    "-1": "Unknown",
    "": "",
    "0": "Move",
    "1": "GFI",
    "2": "Dodge",
    "3": "Armor",
    "4": "Injury",
    "5": "Block",
    "6": "Standup",
    "7": "Pickup",
    "8": "Casualty Roll",
    "9": "Catch",
    "10": "Scatter",
    "11": "Throw In",
    "12": "Pass",
    "13": "Push",
    "14": "Follow Up",
    "15": "Foul Ref Check",
    "16": "Intercept",
    "17": "Wake Up from KO",
    "19": "Touchback",
    "20": "Bonehead",
    "21": "Really Stupid",
    "22": "Wild Animal",
    "23": "Loner",
    "24": "Landing",
    "25": "Regeneration",
    "26": "Inaccurate Pass",
    "27": "Always Hungry",
    "29": "Dauntless",
    "30": "Safe Throw",
    "31": "Jumpup",
    "32": "Shadowing",
    "34": "Leap",
    "36": "Leap",
    "37": "Foul Appearance",
    "38": "Tentacles",
    "39": "Chainsaw",
    "40": "TakeRoot",
    "41": "Ball And Chain",
    "44": "Diving Tackle",
    "45": "Pro",
    "46": "Hypnotic Gaze",
    "49": "Animosity",
    "50": "BloodLust",
    "52": "Bribe",
    "54": "Fireball",
    "55": "Lightning Bolt",
    "56": "Throw Team Mate",
    "58": "Extra Scatter",
    "59": "Piling On Armour",  # ?
    "60": "Piling On Injury",  # ?
    "61": "Wrestle",
    "62": "Dodge",
    "63": "StandFirm",
    "64": "Juggernaut",
    "69": "Fame",
    "70": "Weather",
    "71": "Sweltering Heat",
    "72": "Impact Of The Bomb",
    "73": "Chainsaw Armor",
    "1000": "EndTurn",
    "1001": "Touchdown",
    "1002": "Kickoff Event",
    "1003": "Blitz",
    "1004": "Kick Ball",
    "1005": "Ball Action",
    "2000": "Foul",
}

actions = {
    '-1' : 'Unknown',
    "": "",
    '0':'Move',             #Move
    '1':'Block',            #Block
    '2':'Blitz',            #Blitz
    '3':'Pass',             #Pass
    '4':'Handoff',          #Ball handoff
    '5':'Foul',             #Armor
    '6':'Armor',            #Armor
    '7':'Kickoff',          #Pick Kickoff Location
    '8':'Scatter',          #Pick Kickoff Scatter KickSkill
    '9':'Catch',            #Catch
    '10':'Touchdown',      #Touchdown?
    '11':'Wake up from Stun',#End Turn Stun release?
    '12':'Wake up from KO', #Wake up after KO
    '14':'Pickup',          #Pickup Ball
    '15':'Activation',  #Activation Test
    '16':'Landing',
    '18':'Shadowing',
    '19':'Stab',
    '21':'Leap',
    '23':'Ball Chain',
    '31':'Fireball',
    '32':'Fireball',
    '33':'Lightning bolt', #Wizard Lightning
    '34':'FoulRefCheck',    #Foul - Comes After Armor roll - maybe ref?
    '37':'Free Move',        #Move after High Kick
    '39':'Dodge Against Diving Tackle',
    '42':'Activate Player',  #Select Active Player
    '46':'Unknown_46',      #After Kickoff Choice, has 2 BoardActionResults with RT 69
    '47':'Unknown_47',      #After Kickoff Choice, has 1 BoardActionResult with RT 70
    '48':'Sweltering Heat',
    '50':'Bomb Knock Down',
    '51':'Bomb Half Down',
    '52':'Bomb Throw',
    'Unknown_46':'Unknown_46',      #After Kickoff Choice, has 2 BoardActionResults with RT 69
    'Unknown_47':'Unknown_47',      #After Kickoff Choice, has 1 BoardActionResult with RT 70
}

races = {
    "1":"Human",
    "2":"Dwarf",
    "3":"Skaven",
    "4":"Orc",
    "5":"Lizardman",
    "6":"Goblin",
    "7":"Wood Elf",
    "8":"Chaos",
    "9":"Dark Elf",
    "10":"Undead",
    "11":"Halfling",
    "12":"Norse",
    "13":"Amazon",
    "14":"Elven Union",
    "15":"High Elf",
    "16":"Khemri",
    "17":"Necromantic",
    "18":"Nurgle",
    "19":"Ogre",
    "20":"Vampire",
    "21":"Chaos Dwarf",
    "22":"Underworld Denizens",
    "24":"Bretonnian",
    "25":"Kislev"}

race_list = ['','Human','Dwarf','Skaven','Orc','Lizardman','Goblin','Wood Elf','Chaos','Dark Elf','Undead','Halfling','Norse','Amazon','Elven Union','High Elf','Khemri','Necromantic','Nurgle','Ogre','Vampire','Chaos Dwarf','Underworld','','Bretonnian','Kislev']

skills = ['','Strip Ball', 'Increased Strength', 'Increased Agility', 'Increased Movement', 'Increased Armour', 'Catch', 'Dodge', 'Sprint', 'Pass Block', 'Foul Appearance', 'Leap', 'Extra Arms', 'Mighty Blow', 'Leader', 'Horns', 'Two Heads', 'Stand Firm', 'Always Hungry', 'Regeneration', 'Take Root', 'Accurate', 'Break Tackle', 'Sneaky Git', '', 'Chainsaw', 'Dauntless', 'Dirty Player', 'Diving Catch', 'Dump Off', 'Block', 'Bone Head', 'Very Long Legs', 'Disturbing Presence', 'Diving Tackle', 'Fend', 'Frenzy', 'Grab', 'Guard', 'Hail MaryPass', 'Juggernaut', 'Jump Up', '', '', 'Loner', 'Nerves Of Steel', 'No Hands', 'Pass', 'Piling On', 'Prehensile Tail', 'Pro', 'Really Stupid', 'Right Stuff', 'Safe Throw', 'Secret Weapon', 'Shadowing', 'Side Step', 'Tackle', 'Strong Arm', 'Stunty', 'Sure Feet', 'Sure Hands', '', 'Thick Skull', 'Throw TeamMate', '', '', 'Wild Animal', 'Wrestle', 'Tentacles', 'Multiple Block', 'Kick', 'Kick Off Return', '', 'Big Hand', 'Claw', 'BallChain', 'Stab', 'Hypnotic Gaze', 'Stakes', 'Bombardier', 'Decay', 'Nurgles Rot', 'Titchy', 'Blood Lust', 'Fan Favourite', 'Animosity']


rolls_num = {
    -1: "Unknown",
    "": "",
    0: "Move",
    1: "GFI",
    2: "Dodge",
    3: "Armor",
    4: "Injury",
    5: "Block",
    6: "Standup",
    7: "Pickup",
    8: "Casualty Roll",
    9: "Catch",
    10: "Scatter",
    11: "Throw In",
    12: "Pass",
    13: "Push",
    14: "Follow Up",
    15: "Foul Ref Check",
    16: "Intercept",
    17: "Wake Up from KO",
    19: "Touchback",
    20: "Bonehead",
    21: "Really Stupid",
    22: "Wild Animal",
    23: "Loner",
    24: "Landing",
    25: "Regeneration",
    26: "Inaccurate Pass",
    27: "Always Hungry",
    29: "Dauntless",
    30: "Safe Throw",
    31: "Jumpup",
    32: "Shadowing",
    34: "Leap",
    36: "Leap",
    37: "Foul Appearance",
    38: "Tentacles",
    39: "Chainsaw",
    40: "TakeRoot",
    41: "Ball And Chain",
    44: "Diving Tackle",
    45: "Pro",
    46: "Hypnotic Gaze",
    49: "Animosity",
    50: "BloodLust",
    52: "Bribe",
    54: "Fireball",
    55: "Lightning Bolt",
    56: "Throw Team Mate",
    58: "Extra Scatter",
    59: "Piling On Armour",  # ?
    60: "Piling On Injury",  # ?
    61: "Wrestle",
    62: "Dodge",
    63: "StandFirm",
    64: "Juggernaut",
    69: "Fame",
    70: "Weather",
    71: "Sweltering Heat",
    72: "Impact Of The Bomb",
    73: "Chainsaw Armor",
    1000: "EndTurn",
    1001: "Touchdown",
    1002: "Kickoff Event",
    1003: "Blitz",
    1004: "Kick Ball",
    1005: "Ball Action",
    2000: "Foul",
}

actions_num = {
    -1 : 'Unknown',
    "": "",
    0:'Move',             #Move
    1:'Block',            #Block
    2:'Blitz',            #Blitz
    3:'Pass',             #Pass
    4:'Handoff',          #Ball handoff
    5:'Foul',             #Armor
    6:'Armor',            #Armor
    7:'Kickoff',          #Pick Kickoff Location
    8:'Scatter',          #Pick Kickoff Scatter KickSkill
    9:'Catch',            #Catch
    10:'Touchdown',      #Touchdown?
    11:'Wake up from Stun',#End Turn Stun release?
    12:'Wake up from KO', #Wake up after KO
    14:'Pickup',          #Pickup Ball
    15:'Activation',  #Activation Test
    16:'Landing',
    18:'Shadowing',
    19:'Stab',
    21:'Leap',
    23:'Ball Chain',
    31:'Fireball',
    32:'Fireball',
    33:'Lightning bolt', #Wizard Lightning
    34:'FoulRefCheck',    #Foul - Comes After Armor roll - maybe ref?
    37:'Free Move',        #Move after High Kick
    39:'Dodge Against Diving Tackle',
    42:'Activate Player',  #Select Active Player
    46:'Unknown_46',      #After Kickoff Choice, has 2 BoardActionResults with RT 69
    47:'Unknown_47',      #After Kickoff Choice, has 1 BoardActionResult with RT 70
    48:'Sweltering Heat',
    50:'Bomb Knock Down',
    51:'Bomb Half Down',
    52:'Bomb Throw',
    'Unknown_46':'Unknown_46',      #After Kickoff Choice, has 2 BoardActionResults with RT 69
    'Unknown_47':'Unknown_47',      #After Kickoff Choice, has 1 BoardActionResult with RT 70
}

block_dice_num = {0:"Skull", 1:"Both Down", 2:"Push", 3:"Stumble", 4:"Pow"}

block_results_num = {0:"Attacker Down",1:"Attacker and Defender Down",2:"Wrestle Down",3:"Attacker and Defender Did not Move",4:"Defender Pushed",5:"Attacker in Place, Defender Down",6:"Defender Down"}

roll_status_num = {0:"No Re-roll",1:"Team Re-roll",2:"No Re-roll",3:"Skill Re-roll", 4:"Skill Re-roll","":""}

result_type_num = {0:"Skill Passed",1:"Failure but no Turnover",2:"Failed with Re-Roll",3:"Failed with no Re-roll"}

def labelRoll(data):
    return rolls_num[data]

def labelActions(data):
    return actions_num[data]

def labelBlock(data):
    return block_dice_num[data]

def labelBlockResults(data):
    return block_results_num[data]

def labelRollStatus(data):
    return roll_status_num[data]

def labelResultType(data):
    return result_type_num[data]