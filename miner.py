
# Class for mining past regular season data

from bs4 import BeautifulSoup
import urllib
from Hitter import Hitter
from HitterEntry import HitterEntry
import sqlalchemy

def url_to_soup(url):
    try:
        xml = urllib.urlopen(url)
        if xml.code == 404:
            print "Attempt to access invalid URL: " + xml.url
            return
        return BeautifulSoup(xml)
    except:
        print "Unable to obtain season soup " + str(url)
        return None
    
# Methods for obtaining static data for insertion into the Database
class StatMiner(object):
    mPitchFxBaseUrl = "http://mlb.mlb.com/gdcross/components/game/mlb/"
    
    #TODO: implement this
    def __init__(self,database_session):
        self._mSession = database_session
    
    # Mine an entire season
    # @param    season: 4-digit season year
    def mine_season(self,season):
        yearUrl = self.mPitchFxBaseUrl + "year_" + season + "/"
        yearSoup = url_to_soup(yearUrl)
        if yearSoup is not None:
            monthNodes = yearSoup.find_all("a")
            # Keep only URLs with 
            for monthNode in monthNodes:
                if "month" in monthNode.get("href"):
                    self.mine_month(yearUrl + monthNode.get("href"))
                
    # Mine a single month
    # @param    month_url: an absolute URL for the month of interest
    def mine_month(self,month_url):
        monthSoup = url_to_soup(month_url)
        if monthSoup is not None:
            dayNodes = monthSoup.find_all("a")
            for dayNode in dayNodes:
                if "day" in dayNode.get("href"):
                    self.mine_day(month_url + dayNode.get("href"))    
                
    # Mine a single day
    # @param    day_url: 
    def mine_day(self,day_url):
        daySoup = url_to_soup(day_url)
        if daySoup is not None:
            gameNodes = daySoup.find_all("a")     
            for gameNode in gameNodes:
                if "gid" in gameNode.get("href"):
                    self.mine_game(day_url + gameNode.get("href"))
                
    # Mine a single game and commit it to the database
    # @param    game_url: an absolute URL for the game of interest
    def mine_game(self,game_url):
        gameTypeTestSoup = url_to_soup(game_url + "game.xml")
        if gameTypeTestSoup is not None:
            gameNode = gameTypeTestSoup.find("game")
            # Check if the game is a regular season game
            # TODO: add postseason games?
            if gameNode.get("type") == "R":
                battersSoup = url_to_soup(game_url + "boxscore.xml")
                if battersSoup is not None:
                    gameId = battersSoup.find("boxscore").get("game_id")
                    print "Mining " + str(gameId)
                    batterNodes = battersSoup.find_all("batter")
                    for batterNode in batterNodes:
                        playerName = batterNode.get("name_display_first_last").split()
                        hitter = Hitter(playerName[0],playerName[1],batterNode.get("id"))
                        hitter.set_game_results(gameId,batterNode)
        
                        # Mine the pregame stats
                        #TODO use players.xml to add the batting order attributes, which means we need to get rid of pinch hitters
                        pregameStatsSoup = url_to_soup(game_url + "batters/" + batterNode.get("id") + ".xml")
                        hitter.set_season_stats(pregameStatsSoup)
                        hitter.set_career_stats(pregameStatsSoup)
                        hitter.set_vs_stats(pregameStatsSoup) 
                
                        # Commit the results to the database
                        self._commit_hitter(hitter)
            else:
                print "Game is not a regular season game."
                    
            #for instance in session.query(HitterEntry).order_by(HitterEntry.mPitchFxId):
            #    print instance.mFirstName, instance.mLastName
        
    def _commit_hitter(self,hitter):
        hitterEntry = HitterEntry(hitter)
        try:
            self._mSession.add(hitterEntry)
            self._mSession.commit()
        except sqlalchemy.exc.IntegrityError:
            print "Attempt to duplicate hitter entry: " + hitterEntry.mLastName + ", " + hitterEntry.mFirstName + " " + hitterEntry.mGameId
            self._mSession.rollback()
                 
            
            