

def game_id_to_date(game_id):
    gameId = str(game_id)
    date_fields = gameId.split("/")
    return str(date_fields[0] + "/" + date_fields[1] + "/" + date_fields[2])

# A class housing stats for hitters
class Pitcher(object):
    def __init__(self,first_name,last_name,id,team):
        self.mFirstName = first_name
        self.mLastName = last_name
        self.mPitchFxId = int(id)
        self.mTeamAbbrev = str(team)
        self.mTotalPoints = 0
        
    # Mine the mlb.com boxscore XML file for the actual results of the game
    # @param    game_id: The unique ID for the MLB game
    # @param    soup_node: The BeautifulSoup XML node for the game results
    def set_game_results(self,game_id,soup_node):
        self.mGameId = str(game_id)
        self.mGameDate = game_id_to_date(game_id)
        self.mGameOuts = int(soup_node.get("out"))
        self.mGameSo = int(soup_node.get("so"))
        self.mGameW = 0
        if soup_node.has_attr("win"):
            if str(soup_node.get("win")) == "true":
                self.mGameW = 1 
        self.mGameL = 0
        if soup_node.has_attr("loss"):
            if str(soup_node.get("loss")) == "true":
                self.mGameL = 1
        self.mGameEr = int(soup_node.get("er"))
        self.mGameH = int(soup_node.get("h"))
        self.mGameBb = int(soup_node.get("bb"))
        self.mGameHr = int(soup_node.get("hr"))
        # TODO: it is possible to throw a complete game and lose and get less than 27 outs
        if self.mGameOuts == 27:
            self.mGameCg = 1
        else:
            self.mGameCg = 0
        if self.mGameCg == 1:
            if int(soup_node.get("r")) == 0:
                self.mGameCgSo = 1
            else:
                self.mGameCgSo = 0
        else:
            self.mGameCgSo = 0
        if self.mGameOuts == 27 and self.mGameH == 0:
            self.mGameNoH = 1
        else:
            self.mGameNoH = 0
            
        self.calculate_draftkings_points()
    
    # Mine the mlb.com batter XML file and set the season members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    def set_season_stats(self,soup):
        seasonStatNode = soup.find("season")
        if seasonStatNode is not None:
            InningsString = seasonStatNode.get("ip")
            partialOuts = int(str(InningsString).split(".")[1])
            assert partialOuts >= 0 and partialOuts < 3
            seasonAndGameInnings = int(str(InningsString).split(".")[0]) + float(partialOuts)/3
            self.mSeasonOuts = 3*int(str(InningsString).split(".")[0]) + partialOuts - self.mGameOuts
            self.mSeasonSo = int(seasonStatNode.get("so")) - self.mGameSo
            self.mSeasonW = int(seasonStatNode.get("w"))
            self.mSeasonL = int(seasonStatNode.get("l"))
            self.mSeasonEr = round(float(seasonStatNode.get("era"))*seasonAndGameInnings/9) - self.mGameEr
            self.mSeasonH = int(seasonStatNode.get("h")) - self.mGameH
            self.mSeasonBb = int(seasonStatNode.get("bb")) - self.mGameBb
            self.mSeasonHr = int(seasonStatNode.get("hr")) - self.mGameHr
        
    # Mine the mlb.com batter XML file and set the career members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    def set_career_stats(self,soup):
        careerStatNode = soup.find("career")
        if careerStatNode is not None:
            InningsString = careerStatNode.get("ip")
            partialOuts = int(str(InningsString).split(".")[1])
            assert partialOuts >= 0 and partialOuts < 3
            careerAndGameInnings = int(str(InningsString).split(".")[0]) + float(partialOuts)/3
            self.mCareerOuts = 3*int(str(InningsString).split(".")[0]) + partialOuts - self.mGameOuts
            self.mCareerSo = int(careerStatNode.get("so")) - self.mGameSo
            self.mCareerW = int(careerStatNode.get("w"))
            self.mCareerL = int(careerStatNode.get("l"))
            self.mCareerEr = round(float(careerStatNode.get("era"))*careerAndGameInnings/9) - self.mGameEr
            self.mCareerH = int(careerStatNode.get("h")) - self.mGameH
            self.mCareerBb = int(careerStatNode.get("bb")) - self.mGameBb
            self.mCareerHr = int(careerStatNode.get("hr")) - self.mGameHr
      
    # Mine the mlb.com batter XML file and set the vs members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    def set_vs_stats(self,soup):
        vsStatNode = soup.find("team")
        if vsStatNode is not None:
            InningsString = vsStatNode.get("ip")
            partialOuts = int(str(InningsString).split(".")[1])
            assert partialOuts >= 0 and partialOuts < 3
            vsAndGameInnings = int(str(InningsString).split(".")[0]) + float(partialOuts)/3
            self.mVsOuts = 3*int(str(InningsString).split(".")[0]) + partialOuts - self.mGameOuts
            self.mVsSo = int(vsStatNode.get("so")) - self.mGameSo
            self.mVsEr = round(float(vsStatNode.get("era"))*vsAndGameInnings)/9 - self.mGameEr
            self.mVsH = int(vsStatNode.get("h")) - self.mGameH
            self.mVsBb = int(vsStatNode.get("bb")) - self.mGameBb
            self.mVsHr = int(vsStatNode.get("hr")) - self.mGameHr
            
    # Mine the mlb.com batter XML file and set the month members
    # @param    soup: The BeautifulSoup XML object for the batter XML file  
    def set_month_stats(self,soup):
        vsStatNode = soup.find("month")
        if vsStatNode is not None:
            InningsString = vsStatNode.get("ip")
            partialOuts = int(str(InningsString).split(".")[1])
            assert partialOuts >= 0 and partialOuts < 3
            vsAndGameInnings = int(str(InningsString).split(".")[0]) + float(partialOuts)/3
            self.mMonthOuts = 3*int(str(InningsString).split(".")[0]) + partialOuts - self.mGameOuts
            self.mMonthSo = int(vsStatNode.get("so")) - self.mGameSo
            self.mMonthEr = round(float(vsStatNode.get("era"))*vsAndGameInnings/9) - self.mGameEr
            self.mMonthH = int(vsStatNode.get("h")) - self.mGameH
            self.mMonthBb = int(vsStatNode.get("bb")) - self.mGameBb
            self.mMonthHr = int(vsStatNode.get("hr")) - self.mGameHr
    
    # Calculate the DraftKings points from the game results    
    def calculate_draftkings_points(self):
        self.mTotalPoints = 2.25*(float(self.mGameOuts) / 3)
        self.mTotalPoints += 2*self.mGameSo
        self.mTotalPoints += 5*self.mGameW
        self.mTotalPoints -= 2*self.mGameEr
        self.mTotalPoints -= 0.6*self.mGameH
        self.mTotalPoints -= 0.6*self.mGameBb
        # TODO: we may need to get HBP data from elsewhere
        #self.mTotalPoints -= 0.6*self.mGameHbp
        self.mTotalPoints += 2.5*self.mGameCg
        self.mTotalPoints += 2.5*self.mGameCgSo
        self.mTotalPoints += 5*self.mGameNoH
        