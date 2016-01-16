
# Class for mining past regular season data

from bs4 import BeautifulSoup
import urllib
from Hitter import Hitter
from HitterGameEntry import HitterGameEntry
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
    # @param    day_url: an absolute URL for the day of interest
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
                playersSoup = url_to_soup(game_url + "players.xml")
                battersSoup = url_to_soup(game_url + "boxscore.xml")
                gameId = battersSoup.find("boxscore").get("game_id")
                if playersSoup is not None and battersSoup is not None:
                    print "Mining: " + str(gameId)
                    players = playersSoup.find_all("player")
                    for player in players:
                        if player.has_attr("bat_order"):
                            hitter = Hitter(player.get("first"),player.get("last"),player.get("id"),
                                            player.get("team_abbrev"),player.get("bat_order"))
                            hitter.set_game_results(gameId,battersSoup.find("batter", {"id" : player.get("id")}))
        
                            # Mine the pregame stats
                            pregameStatsSoup = url_to_soup(game_url + "batters/" + player.get("id") + ".xml")
                            hitter.set_season_stats(pregameStatsSoup)
                            hitter.set_career_stats(pregameStatsSoup)
                            hitter.set_vs_stats(pregameStatsSoup)
                            # TODO: explore some ways of mining different data for month stats
                            hitter.set_month_stats(pregameStatsSoup) 
                
                            # Commit the results to the database
                            self._commit_hitter(hitter)
            else:
                print "Game is not a regular season game."
        
    def _commit_hitter(self,hitter):
        hitterGameEntry = HitterGameEntry(hitter)
        hitterEntry = HitterEntry(hitter)
        try:
            # Query the database for the HitterEntry object
            dbQuery = self._mSession.query(HitterEntry).filter(HitterEntry.PitchFxId == hitter.mPitchFxId)
            hitterEntryObject = dbQuery.first()
            # Hitter object already exists in database
            if hitterEntryObject is not None:
                hitterEntryObject = hitterEntry
            # Hitter object doesn't exist yet in database
            else:
                self._mSession.add(hitterEntry)
                
            self._mSession.commit()
        except:
            return
        
        try:
            self._mSession.add(hitterGameEntry)
            self._mSession.commit()
        except sqlalchemy.exc.IntegrityError:
            print "Attempt to duplicate hitter entry: " + hitterGameEntry.mLastName + ", " + hitterGameEntry.mFirstName + " " + hitterGameEntry.mGameId
            self._mSession.rollback()
                 
            
            