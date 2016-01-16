
def game_id_to_date(game_id):
    gameId = str(game_id)
    date_fields = gameId.split("/")
    return str(date_fields[0] + "/" + date_fields[1] + "/" + date_fields[2])

# A class housing stats for hitters
class Hitter(object):
    def __init__(self,first_name,last_name,id,team,batting_order):
        self.mFirstName = first_name
        self.mLastName = last_name
        self.mPitchFxId = int(id)
        self.mTeamAbbrev = str(team)
        self.mBattingOrder = int(batting_order)
        self.mTotalPoints = 0
        
    # Mine the mlb.com boxscore XML file for the actual results of the game
    # @param    game_id: The unique ID for the MLB game
    # @param    soup_node: The BeautifulSoup XML node for the game results
    def set_game_results(self,game_id,soup_node):
        self.mGameId = str(game_id)
        self.mGameDate = game_id_to_date(game_id)
        self.mGameAb = float(soup_node.get("ab"))
        self.mGameH = float(soup_node.get("h"))
        self.mGame2b = float(soup_node.get("d"))
        self.mGame3b = float(soup_node.get("t"))
        self.mGameHbp = float(soup_node.get("hbp"))
        self.mGameBb = float(soup_node.get("bb"))
        self.mGameSo = float(soup_node.get("so"))
        self.mGameR = float(soup_node.get("r"))
        self.mGameSb = float(soup_node.get("sb"))
        self.mGameCs = float(soup_node.get("cs"))
        self.mGameHr = float(soup_node.get("hr"))
        self.mGameRbi = float(soup_node.get("rbi"))
        self.calculate_draftkings_points()
    
    # Mine the mlb.com batter XML file and set the season members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    def set_season_stats(self,soup):
        seasonStatNode = soup.find("season")
        if seasonStatNode is not None:
            self.mSeasonAb = float(seasonStatNode.get("ab"))
            self.mSeasonH = float(seasonStatNode.get("h"))
            self.mSeasonBb = float(seasonStatNode.get("bb"))
            self.mSeasonSo = float(seasonStatNode.get("so"))
            self.mSeasonR = float(seasonStatNode.get("r"))
            self.mSeasonSb = float(seasonStatNode.get("sb"))
            self.mSeasonCs = float(seasonStatNode.get("cs"))
            self.mSeasonHr = float(seasonStatNode.get("hr"))
            self.mSeasonRbi = float(seasonStatNode.get("rbi"))
            self.mSeasonOps = float(seasonStatNode.get("ops"))
        
    # Mine the mlb.com batter XML file and set the career members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    def set_career_stats(self,soup):
        careerStatNode = soup.find("career")
        if careerStatNode is not None:
            self.mCareerAb = float(careerStatNode.get("ab"))
            self.mCareerH = float(careerStatNode.get("h"))
            self.mCareerBb = float(careerStatNode.get("bb"))
            self.mCareerSo = float(careerStatNode.get("so"))
            self.mCareerR = float(careerStatNode.get("r"))
            self.mCareerSb = float(careerStatNode.get("sb"))
            self.mCareerCs = float(careerStatNode.get("cs"))
            self.mCareerHr = float(careerStatNode.get("hr"))
            self.mCareerRbi = float(careerStatNode.get("rbi"))
            self.mCareerOps = float(careerStatNode.get("ops"))
      
    # Mine the mlb.com batter XML file and set the vs members
    # @param    soup: The BeautifulSoup XML object for the batter XML file  
    def set_vs_stats(self,soup):
        vsStatNode = soup.find("vs_p")
        if vsStatNode is not None:
            self.mVsAb = float(vsStatNode.get("ab"))
            self.mVsH = float(vsStatNode.get("h"))
            self.mVsBb = float(vsStatNode.get("bb"))
            self.mVsSo = float(vsStatNode.get("so"))
            self.mVsR = float(vsStatNode.get("r"))
            self.mVsSb = float(vsStatNode.get("sb"))
            self.mVsCs = float(vsStatNode.get("cs"))
            self.mVsHr = float(vsStatNode.get("hr"))
            self.mVsRbi = float(vsStatNode.get("rbi"))
            self.mVsOps = float(vsStatNode.get("ops"))
            
    # Mine the mlb.com batter XML file and set the month members
    # @param    soup: The BeautifulSoup XML object for the batter XML file  
    def set_month_stats(self,soup):
        vsStatNode = soup.find("month")
        if vsStatNode is not None:
            self.mMonthAb = float(vsStatNode.get("ab"))
            self.mMonthH = float(vsStatNode.get("h"))
            self.mMonthBb = float(vsStatNode.get("bb"))
            self.mMonthSo = float(vsStatNode.get("so"))
            self.mMonthR = float(vsStatNode.get("r"))
            self.mMonthSb = float(vsStatNode.get("sb"))
            self.mMonthCs = float(vsStatNode.get("cs"))
            self.mMonthHr = float(vsStatNode.get("hr"))
            self.mMonthRbi = float(vsStatNode.get("rbi"))
            self.mMonthOps = float(vsStatNode.get("ops"))
    
    # Calculat the DraftKings points from the game results    
    def calculate_draftkings_points(self):
        self.mTotalPoints = 3 * (self.mGameH - self.mGame2b - self.mGame3b - self.mGameHr)
        self.mTotalPoints += 5*self.mGame2b
        self.mTotalPoints += 8*self.mGame3b
        self.mTotalPoints += 10*self.mGameHr
        self.mTotalPoints += 2*self.mGameRbi
        self.mTotalPoints += 2*self.mGameR
        self.mTotalPoints += 2*self.mGameBb
        self.mTotalPoints += 2*self.mGameHbp
        self.mTotalPoints += 5*self.mGameSb
        self.mTotalPoints -= 2*self.mGameCs
        