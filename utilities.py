def add_roll_name(num):
    '''Uses rolls dictionary to match against the roll value in the export'''
    for x in rolls.keys():
        if x==num:
            return rolls[x]

block_dice = {"0": "Skull", "1": "Both Down", "2": "Push", "3": "Stumble", "4": "Pow"}

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
    "10": "Kickoff",
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
