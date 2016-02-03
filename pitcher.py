from player import Player
import player
from player import game_id_to_date, inning_str_to_outs, inning_str_to_float, era_to_er

# A class housing stats for hitters
class Pitcher(Player):
    def __init__(self,first_name,last_name,id,team,pitching_hand):
        super(Pitcher,self).__init__(first_name,last_name,id,team,pitching_hand)
        
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
            self.mSeasonOuts = inning_str_to_outs(InningsString) - self.mGameOuts
            self.mSeasonSo = int(seasonStatNode.get("so")) - self.mGameSo
            self.mSeasonW = int(seasonStatNode.get("w"))
            self.mSeasonL = int(seasonStatNode.get("l"))
            seasonAndGameInnings = inning_str_to_float(InningsString)
            self.mSeasonEr = era_to_er(seasonStatNode.get("era"), seasonAndGameInnings) - self.mGameEr
            self.mSeasonH = int(seasonStatNode.get("h")) - self.mGameH
            self.mSeasonBb = int(seasonStatNode.get("bb")) - self.mGameBb
            self.mSeasonHr = int(seasonStatNode.get("hr")) - self.mGameHr
        
    # Mine the mlb.com batter XML file and set the career members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    def set_career_stats(self,soup):
        careerStatNode = soup.find("career")
        if careerStatNode is not None:
            InningsString = careerStatNode.get("ip")
            self.mCareerOuts = inning_str_to_outs(InningsString) - self.mGameOuts
            self.mCareerSo = int(careerStatNode.get("so")) - self.mGameSo
            self.mCareerW = int(careerStatNode.get("w"))
            self.mCareerL = int(careerStatNode.get("l"))
            careerAndGameInnings = inning_str_to_float(InningsString)
            self.mCareerEr = era_to_er(careerStatNode.get("era"), careerAndGameInnings) - self.mGameEr
            self.mCareerH = int(careerStatNode.get("h")) - self.mGameH
            self.mCareerBb = int(careerStatNode.get("bb")) - self.mGameBb
            self.mCareerHr = int(careerStatNode.get("hr")) - self.mGameHr
      
    # Mine the mlb.com batter XML file and set the vs members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    def set_vs_stats(self,soup):
        # Versus this team
        vsStatNode = soup.find("team")
        if vsStatNode is not None:
            InningsString = vsStatNode.get("ip")
            self.mVsOuts = inning_str_to_outs(InningsString) - self.mGameOuts
            self.mVsSo = int(vsStatNode.get("so")) - self.mGameSo
            vsAndGameInnings = inning_str_to_float(InningsString)
            self.mVsEr = era_to_er(vsStatNode.get("era"), vsAndGameInnings) - self.mGameEr
            self.mVsH = int(vsStatNode.get("h")) - self.mGameH
            self.mVsBb = int(vsStatNode.get("bb")) - self.mGameBb
            self.mVsHr = int(vsStatNode.get("hr")) - self.mGameHr
            
        # Versus left handed hitters
        vsStatNode = soup.find("vs_lhb")
        if vsStatNode is not None:
            InningsString = vsStatNode.get("ip")
            self.mVsLhbOuts = inning_str_to_outs(InningsString) - self.mGameOuts
            self.mVsLhbSo = float(vsStatNode.get("so"))
            vsAndGameInnings = inning_str_to_float(InningsString)
            self.mVsLhbEr = era_to_er(vsStatNode.get("era"), vsAndGameInnings) - self.mGameEr
            self.mVsLhbAb = float(vsStatNode.get("ab"))
            self.mVsLhbH = float(vsStatNode.get("h"))
            self.mVsLhbBb = float(vsStatNode.get("bb"))
            self.mVsLhbHr = float(vsStatNode.get("hr"))
            
        # Versus right handed hitters
        vsStatNode = soup.find("vs_rhb")
        if vsStatNode is not None:
            InningsString = vsStatNode.get("ip")
            self.mVsRhbOuts = inning_str_to_outs(InningsString) - self.mGameOuts
            self.mVsRhbSo = float(vsStatNode.get("so"))
            vsAndGameInnings = inning_str_to_float(InningsString)
            self.mVsRhbEr = era_to_er(vsStatNode.get("era"), vsAndGameInnings) - self.mGameEr
            self.mVsRhbAb = float(vsStatNode.get("ab"))
            self.mVsRhbH = float(vsStatNode.get("h"))
            self.mVsRhbBb = float(vsStatNode.get("bb"))
            self.mVsRhbHr = float(vsStatNode.get("hr"))
        
    # Mine the mlb.com batter XML file and set the month members
    # @param    soup: The BeautifulSoup XML object for the batter XML file  
    def set_month_stats(self,soup):
        vsStatNode = soup.find("month")
        if vsStatNode is not None:
            InningsString = vsStatNode.get("ip")
            self.mMonthOuts = inning_str_to_outs(InningsString) - self.mGameOuts
            self.mMonthSo = int(vsStatNode.get("so")) - self.mGameSo
            vsAndMonthInnings = inning_str_to_float(InningsString)
            self.mMonthEr = era_to_er(vsStatNode.get("era"), vsAndMonthInnings) - self.mGameEr
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
        