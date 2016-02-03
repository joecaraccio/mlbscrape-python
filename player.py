
def game_id_to_date(game_id):
    gameId = str(game_id)
    date_fields = gameId.split("/")
    return str(date_fields[0] + "/" + date_fields[1] + "/" + date_fields[2])

def inning_str_to_outs(innings):
    partialOuts = int(str(innings).split(".")[1])
    wholeInnings = int(str(innings).split(".")[0])
    assert partialOuts >= 0 and partialOuts < 3
    return 3*wholeInnings + partialOuts

def inning_str_to_float(innings):
    partialOuts = int(str(innings).split(".")[1])
    wholeInnings = int(str(innings).split(".")[0])
    return wholeInnings + float(partialOuts)/3

def era_to_er(era,innings):
    return round(float(era)*innings/9)

# A base class for batter and pitchers
class Player(object):
    def __init__(self,first_name,last_name,id,team,hand):
        self.mFirstName = first_name
        self.mLastName = last_name
        self.mPitchFxId = int(id)
        self.mTeamAbbrev = str(team)
        self.mTotalPoints = 0
        self.mPlayingHand = hand