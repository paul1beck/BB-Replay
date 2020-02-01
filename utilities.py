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
            
block_dice = {"0": "Skull", "1": "Both Down", "2": "Push", "3": "Stumble", "4": "Pow"}

block_results = {"0":"Attacker Down","1":"Attacker and Defender Down","2":"Wrestle Down","3":"Attacker and Defender Did not Move","4":"Defender Pushed","5":"Attacker in Place, Defender Down","6":"Defender Down"}

roll_status = {"0":"No Re-roll","1":"Re-roll Taken","2":"Re-roll Not Taken","3":"Skill Re-roll"}

result_type = {"0":"Skill Passed","1":"Failure but no Turnover","2":"Failed with Re-Roll","3":"Failed with no Re-roll"}

rolls = {
    "-1": "Unknown",
    "0": "Move",
    "1": "GFI",
    "2": "Dodge",
    "3": "Armor",
    "4": "Injury",
    "5": "Block",
    "6": "Standup",
    "7": "Pickup",
    "8": "CasualtyRoll",
    "9": "Catch",
    "10": "Scatter",
    "12": "Pass",
    "13": "Push",
    "14": "FollowUp",
    "16": "Intercept",
    "17": "WakeUpKO",
    "19": "Touchback",
    "20": "Bonehead",
    "21": "ReallyStupid",
    "22": "WildAnimal",
    "23": "Loner",
    "24": "Landing",
    "25": "Regeneration",
    "26": "InaccuratePass",
    "27": "AlwaysHungry",
    "29": "Dauntless",
    "31": "Jumpup",
    "36": "Leap",
    "37": "FoulAppearance",
    "38": "Tentacles",
    "39": "Chainsaw",
    "40": "TakeRoot",
    "44": "DivingTackle",
    "45": "Pro",
    "46": "HypnoticGaze",
    "50": "BloodLust",
    "52": "Bribe",
    "55": "LightningBolt",
    "56": "ThrowTeamMate",
    "58": "MoveToBall",
    "59": "PilingOnArmour",  # ?
    "60": "PilingOnInjury",  # ?
    "72": "ImpactOfTheBomb",
    "1000": "EndTurn",
    "1001": "Touchdown",
    "1002": "KickoffEvent",
    "1003": "Blitz",
    "1004": "KickBall",
    "1005": "BallAction",
    "2000": "Foul",
}

actions = {
    '0':'Move',             #Move
    '1':'Block',            #Block
    '2':'Blitz',            #Blitz
    '3':'Pass',             #Pass
    '4':'Handoff',          #Ball handoff
    '5':'FoulAR',           #Armor
    '6':'Armor',            #Armor
    '7':'Kickoff',          #Pick Kickoff Location
    '8':'Scatter',          #Pick Kickoff Scatter KickSkill
    '9':'Catch',            #Catch
    '10':'TouchDown',       #Touchdown?
    '11':'StunWake',        #End Turn Stun release?
    '12':'WakeUp',          #Wake up after KO
    '14':'Pickup',          #Pickup Ball
    '15':'ActivationTest',  #Activation Test
    '16':'Landing',
    '18':'Shadowing',
    '19':'Stab',
    '21':'Leap',
    '23':'BallChain',
    '31':'WizardFireBallCast',
    '32':'WizardFireball',
    '33':'WizardLightning', #Wizard Lightning
    '34':'FoulRefCheck',    #Foul - Comes After Armor roll - maybe ref?
    '37':'FreeMove',        #Move after High Kick
    '39':'DodgeAgDivingTackle',
    '42':'ActivatePlayer',  #Select Active Player
    '46':'Unknown_46',      #After Kickoff Choice, has 2 BoardActionResults with RT 69
    '47':'Unknown_47',      #After Kickoff Choice, has 1 BoardActionResult with RT 70
    '48':'SwelteringHeat',
    '50':'BombKnockDown',
    '51':'BombHalfDown',
    '52':'BombThrow',
}