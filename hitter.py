from player import Player
from player import game_id_to_date
import player

# A class housing stats for hitters
class Hitter(Player):
    def __init__(self,first_name,last_name,id,team,batting_order,batting_hand):
        super(Hitter,self).__init__(first_name,last_name,id,team,batting_hand)
        self.mBattingOrder = int(batting_order)
        
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
            self.mSeasonAb = float(seasonStatNode.get("ab")) - self.mGameAb
            self.mSeasonH = float(seasonStatNode.get("h")) - self.mGameH
            self.mSeasonBb = float(seasonStatNode.get("bb"))  - self.mGameBb
            self.mSeasonSo = float(seasonStatNode.get("so"))  - self.mGameSo
            self.mSeasonR = float(seasonStatNode.get("r")) - self.mGameR
            self.mSeasonSb = float(seasonStatNode.get("sb")) - self.mGameSb
            self.mSeasonCs = float(seasonStatNode.get("cs")) - self.mGameCs
            self.mSeasonHr = float(seasonStatNode.get("hr")) - self.mGameHr
            self.mSeasonRbi = float(seasonStatNode.get("rbi")) - self.mGameRbi
        
    # Mine the mlb.com batter XML file and set the career members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    def set_career_stats(self,soup):
        careerStatNode = soup.find("career")
        if careerStatNode is not None:
            self.mCareerAb = float(careerStatNode.get("ab")) - self.mGameAb
            self.mCareerH = float(careerStatNode.get("h")) - self.mGameH
            self.mCareerBb = float(careerStatNode.get("bb")) - self.mGameBb
            self.mCareerSo = float(careerStatNode.get("so")) - self.mGameSo
            self.mCareerR = float(careerStatNode.get("r"))  - self.mGameR
            self.mCareerSb = float(careerStatNode.get("sb")) - self.mGameSb
            self.mCareerCs = float(careerStatNode.get("cs")) - self.mGameCs
            self.mCareerHr = float(careerStatNode.get("hr")) - self.mGameHr
            self.mCareerRbi = float(careerStatNode.get("rbi")) - self.mGameRbi
      
    # Mine the mlb.com batter XML file and set the vs members
    # @param    soup: The BeautifulSoup XML object for the batter XML file
    # Note: For some reason, these stats don't follow the convention of including the results from the game.  
    def set_vs_stats(self,soup):
        # Versus this pitcher
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
            
        # Versus left handed pitching
        vsStatNode = soup.find("vs_lhp")
        if vsStatNode is not None:
            self.mVsLhpAb = float(vsStatNode.get("ab"))
            self.mVsLhpH = float(vsStatNode.get("h"))
            self.mVsLhpBb = float(vsStatNode.get("bb"))
            self.mVsLhpSo = float(vsStatNode.get("so"))
            self.mVsLhpR = float(vsStatNode.get("r"))
            self.mVsLhpSb = float(vsStatNode.get("sb"))
            self.mVsLhpCs = float(vsStatNode.get("cs"))
            self.mVsLhpHr = float(vsStatNode.get("hr"))
            self.mVsLhpRbi = float(vsStatNode.get("rbi"))
            
        # Versus right handed pitching
        vsStatNode = soup.find("vs_rhp")
        if vsStatNode is not None:
            self.mVsRhpAb = float(vsStatNode.get("ab"))
            self.mVsRhpH = float(vsStatNode.get("h"))
            self.mVsRhpBb = float(vsStatNode.get("bb"))
            self.mVsRhpSo = float(vsStatNode.get("so"))
            self.mVsRhpR = float(vsStatNode.get("r"))
            self.mVsRhpSb = float(vsStatNode.get("sb"))
            self.mVsRhpCs = float(vsStatNode.get("cs"))
            self.mVsRhpHr = float(vsStatNode.get("hr"))
            self.mVsRhpRbi = float(vsStatNode.get("rbi"))
            
    # Mine the mlb.com batter XML file and set the month members
    # @param    soup: The BeautifulSoup XML object for the batter XML file  
    def set_month_stats(self,soup):
        vsStatNode = soup.find("month")
        if vsStatNode is not None:
            self.mMonthAb = float(vsStatNode.get("ab")) - self.mGameAb
            self.mMonthH = float(vsStatNode.get("h")) - self.mGameH
            self.mMonthBb = float(vsStatNode.get("bb")) - self.mGameBb
            self.mMonthSo = float(vsStatNode.get("so")) - self.mGameSo
            self.mMonthR = float(vsStatNode.get("r")) - self.mGameR
            self.mMonthSb = float(vsStatNode.get("sb")) - self.mGameSb
            self.mMonthCs = float(vsStatNode.get("cs")) - self.mGameCs
            self.mMonthHr = float(vsStatNode.get("hr")) - self.mGameHr
            self.mMonthRbi = float(vsStatNode.get("rbi")) - self.mGameRbi
    
    # Calculate the DraftKings points from the game results    
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
        