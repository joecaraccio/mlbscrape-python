
# Class for mining past regular season data

from bs4 import BeautifulSoup
import urllib
from hitter import Hitter
from hitter_game_entry import HitterGameEntry
from hitter_entry import HitterEntry
from pitcher import Pitcher
from pitcher_game_entry import PitcherGameEntry
from pitcher_entry import PitcherEntry
import sqlalchemy
from datetime import date

# Convert a PitchFx date string to a date object
# @param       date_string: a PitchFx date string
# @return      date: the date object representing the string
def str_to_date(date_string):
    dateMembers = date_string.split("/")
    dateObject = date(int(dateMembers[0]),int(dateMembers[1]),int(dateMembers[2]))
    return dateObject

# Take a URL and get the BeautifulSoup object
# @param    url: the absolute URL string
# @return    the BeautifulSoup object returned, return None if the object was not successfully created
def url_to_soup(url):
    try:
        xml = urllib.urlopen(url)
        if xml.code == 404:
            print "Attempt to access invalid URL: " + xml.url
            return None
        return BeautifulSoup(xml)
    except:
        print "Unable to obtain season soup " + str(url)
        return None
    
# Methods for obtaining static data for insertion into the Database
class StatMiner(object):
    mPitchFxBaseUrl = "http://mlb.mlb.com/gdcross/components/game/mlb/"
    
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
                boxscoreSoup = url_to_soup(game_url + "boxscore.xml")
                gameId = boxscoreSoup.find("boxscore").get("game_id")
                if playersSoup is not None and boxscoreSoup is not None:
                    print "Mining: " + str(gameId)
                    players = playersSoup.find_all("player")
                    # Hitters
                    for player in players:
                        if player.has_attr("bat_order"):
                            hitter = Hitter(player.get("first"),player.get("last"),player.get("id"),
                                            player.get("team_abbrev"),player.get("bat_order"),player.get("bats"))
                            hitter.set_game_results(gameId,boxscoreSoup.find("batter", {"id" : player.get("id")}))
        
                            # Mine the pregame stats
                            pregameStatsSoup = url_to_soup(game_url + "batters/" + player.get("id") + ".xml")
                            hitter.set_season_stats(pregameStatsSoup)
                            hitter.set_career_stats(pregameStatsSoup)
                            hitter.set_vs_stats(pregameStatsSoup)
                            # TODO: explore some ways of mining different data for month stats
                            hitter.set_month_stats(pregameStatsSoup) 
                
                            # Commit the results to the database
                            self._commit_hitter(hitter)
                            
                    # Starting pitchers
                    pitchersSoup = boxscoreSoup.findAll("pitching")
                    for pitcherNode in pitchersSoup:
                        # The starting pitcher will always just be the first entry
                        startingPitcherNode = pitcherNode.find("pitcher")
                        startingPitcherSoup = url_to_soup(game_url + "pitchers/" + startingPitcherNode.get("id") + ".xml")
                        player = startingPitcherSoup.find("player")
                        
                        startingPitcher = Pitcher(player.get("first_name"),player.get("last_name"),player.get("id"),
                                            player.get("team"),player.get("throws"))
                        startingPitcher.set_game_results(gameId,startingPitcherNode)
                        startingPitcher.set_season_stats(startingPitcherSoup)
                        startingPitcher.set_career_stats(startingPitcherSoup)
                        startingPitcher.set_vs_stats(startingPitcherSoup)
                        startingPitcher.set_month_stats(startingPitcherSoup)
                        
                        self._commit_pitcher(startingPitcher)
                        
            else:
                print "Game is not a regular season game."
        
    # Copy a Hitter object to a HitterGameEntry and HitterEntry object and commit to the database
    # @param    hitter: Hitter object to copy
    def _commit_hitter(self,hitter):
        hitterGameEntry = HitterGameEntry(hitter)
        hitterEntry = HitterEntry(hitter)
        try:
            # Query the database for the HitterEntry object
            dbQuery = self._mSession.query(HitterEntry).filter(HitterEntry.PitchFxId == hitter.mPitchFxId)
            hitterEntryObject = dbQuery.first()
        except:
            print "Query for previous hitter entry failed."
            return
        
        # Hitter object already exists in database
        if hitterEntryObject is not None:
            storedDate = str_to_date(hitterEntryObject.LastGameDate)
            newDate = str_to_date(hitterEntry.LastGameDate)
            if newDate > storedDate:
                hitterEntryObject = hitterEntry
                self._mSession.commit()
        # Hitter object doesn't exist yet in database
        else:
            try:
                self._mSession.add(hitterEntry)
                self._mSession.commit()
            except sqlalchemy.exc.IntegrityError:
                print "Attempt to duplicate hitter entry: " + hitterGameEntry.LastName + ", " + hitterGameEntry.FirstName + " " + hitterGameEntry.GameId
                self._mSession.rollback()
        
        try:
            self._mSession.add(hitterGameEntry)
            self._mSession.commit()
        except sqlalchemy.exc.IntegrityError:
            print "Attempt to duplicate hitter game entry: " + hitterGameEntry.LastName + ", " + hitterGameEntry.FirstName + " " + hitterGameEntry.GameId
            self._mSession.rollback()
    
    # Copy a Pitcher object to a PitcherGameEntry and PitcherEntry object and commit to the database
    # @param    pitcher: Pitcher object to copy        
    def _commit_pitcher(self,pitcher):
        pitcherGameEntry = PitcherGameEntry(pitcher)
        pitcherEntry = PitcherEntry(pitcher)
        try:
            # Query the database for the HitterEntry object
            dbQuery = self._mSession.query(PitcherEntry).filter(PitcherEntry.PitchFxId == pitcher.mPitchFxId)
            pitcherEntryObject = dbQuery.first()
        except:
            print "Query for previous pitcher entry failed."
            return
        
        # Hitter object already exists in database
        if pitcherEntryObject is not None:
            storedDate = str_to_date(pitcherEntryObject.LastGameDate)
            newDate = str_to_date(pitcherEntry.LastGameDate)
            if newDate > storedDate:
                pitcherEntryObject = pitcherEntry
                self._mSession.commit()
        # Hitter object doesn't exist yet in database
        else:
            try:
                self._mSession.add(pitcherEntry)
                self._mSession.commit()
            except sqlalchemy.exc.IntegrityError:
                print "Attempt to duplicate pitcher entry: " + pitcherGameEntry.LastName + ", " + pitcherGameEntry.FirstName + " " + pitcherGameEntry.GameId
                self._mSession.rollback()
        
        try:
            self._mSession.add(pitcherGameEntry)
            self._mSession.commit()
        except sqlalchemy.exc.IntegrityError:
            print "Attempt to duplicate pitcher game entry: " + pitcherGameEntry.LastName + ", " + pitcherGameEntry.FirstName + " " + pitcherGameEntry.GameId
            self._mSession.rollback()
                 
            
            