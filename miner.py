

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


class StatMiner(object):
    """ Class for mining PitchFX data and committing it to a database
    """
    PITCH_FX_BASE_URL = "http://mlb.mlb.com/gdcross/components/game/mlb/"
    
    def __init__(self, database_session):
        """ Constructor
        :param database_session: an SQLAlchemy database session
        """
        self._session = database_session

    @staticmethod
    def str_to_date(date_string):
        """ Convert a PitchFx date string to a Date object
        :param date_string: a PitchFx date string
        :return the Date object representing the string
        """
        date_members = date_string.split("/")
        date_object = date(int(date_members[0]), int(date_members[1]), int(date_members[2]))
        return date_object

    @staticmethod
    def get_soup_from_url(url):
        for i in range(3):
            soup = StatMiner.url_to_soup(url)
            if soup is not None:
                return soup
            else:
                print "Trying to obtain soup again..."

        print "Exhausted all attempts to get the soup. Check your internet connection."
        return None

    @staticmethod
    def url_to_soup(url):
        """ Take a URL and get the BeautifulSoup object
        :param url: the absolute URL string
        :return the BeautifulSoup object returned, return None if the object was not successfully created
        """
        try:
            xml = urllib.urlopen(url)
            if xml.code == 404:
                print "Attempt to access invalid URL: " + xml.url
                return None
            return BeautifulSoup(xml)
        except:
            print "Unable to obtain season soup " + str(url)
            return None

    def mine_season(self, season):
        """ Mine an entire MLB season
        :param season: 4-digit season year
        """
        year_url = self.PITCH_FX_BASE_URL + "year_" + season + "/"
        year_soup = StatMiner.get_soup_from_url(year_url)
        if year_soup is not None:
            month_nodes = year_soup.find_all("a")
            # Keep only URLs with 
            for month_node in month_nodes:
                if "month" in month_node.get("href"):
                    if 4 <= int(month_node.get("href").replace("/", "").split("_")[1]) <= 10:
                        self.mine_month(year_url + month_node.get("href"))

    def mine_month(self, month_url):
        """ Mine a single month
        :param month_url: an absolute URL for the month of interest
        """
        month_soup = StatMiner.get_soup_from_url(month_url)
        if month_soup is not None:
            day_nodes = month_soup.find_all("a")
            for day_node in day_nodes:
                if "day" in day_node.get("href"):
                    self.mine_day(month_url + day_node.get("href"))

    def mine_day(self, day_url):
        """ Mine a single day
        :param day_url: an absolute URL for the day of interest
        """
        day_soup = StatMiner.get_soup_from_url(day_url)
        if day_soup is not None:
            game_nodes = day_soup.find_all("a")
            for game_node in game_nodes:
                if "gid" in game_node.get("href"):
                    self.mine_game(day_url + game_node.get("href"))

    def mine_game(self, game_url):
        """ Mine a single game and commit it to the database
        :param game_url: an absolute URL for the game of interest
        """
        game_type_test_soup = StatMiner.get_soup_from_url(game_url + "game.xml")
        if game_type_test_soup is not None:
            game_node = game_type_test_soup.find("game")
            # Check if the game is a regular season game
            # TODO: add postseason games?
            if game_node.get("type") == "R":
                players_soup = StatMiner.get_soup_from_url(game_url + "players.xml")
                boxscore_soup = StatMiner.get_soup_from_url(game_url + "boxscore.xml")
                game_id = boxscore_soup.find("boxscore").get("game_id")
                if players_soup is not None and boxscore_soup is not None:
                    print "Mining: " + str(game_id)
                    players = players_soup.find_all("player")
                    # Hitters
                    for player in players:
                        if player.has_attr("bat_order"):
                            hitter = Hitter(player.get("first"), player.get("last"), player.get("id"),
                                            player.get("team_abbrev"), player.get("bat_order"), player.get("bats"))
                            hitter.set_game_results(game_id, boxscore_soup.find("batter", {"id": player.get("id")}))
        
                            # Mine the pregame stats
                            pregame_stats_soup = StatMiner.get_soup_from_url(game_url + "batters/" + player.get("id") + ".xml")
                            try:
                                hitter.set_season_stats(pregame_stats_soup)
                                hitter.set_career_stats(pregame_stats_soup)
                                hitter.set_vs_stats(pregame_stats_soup)
                                # TODO: explore some ways of mining different data for month stats
                                hitter.set_month_stats(pregame_stats_soup)
                                # Commit the results to the database
                                self._commit_hitter(hitter)
                            except ValueError:
                                print "The hitter's stats are not formatted correctly. Skipping " \
                                  "hitter: " + hitter.first_name + " " + hitter.last_name
                            
                    # Starting pitchers
                    pitchers_soup = boxscore_soup.findAll("pitching")
                    for pitcherNode in pitchers_soup:
                        # The starting pitcher will always just be the first entry
                        starting_pitcher_node = pitcherNode.find("pitcher")
                        starting_pitcher_soup = StatMiner.get_soup_from_url(game_url + "pitchers/" + starting_pitcher_node.get("id") + ".xml")
                        player = starting_pitcher_soup.find("player")
                        
                        starting_pitcher = Pitcher(player.get("first_name"), player.get("last_name"), player.get("id"),
                                                   player.get("team"), player.get("throws"))
                        try:
                            starting_pitcher.set_game_results(game_id, starting_pitcher_node)
                            starting_pitcher.set_season_stats(starting_pitcher_soup)
                            starting_pitcher.set_career_stats(starting_pitcher_soup)
                            starting_pitcher.set_vs_stats(starting_pitcher_soup)
                            starting_pitcher.set_month_stats(starting_pitcher_soup)
                            self._commit_pitcher(starting_pitcher)
                        except ValueError:
                            print "The pitcher's stats are not formatted correctly. Skipping " \
                                  "pitcher: " + starting_pitcher.first_name + " " + starting_pitcher.last_name
                            return
                        
            else:
                print "Game is not a regular season game."

    def _commit_hitter(self, hitter):
        """ Copy a Hitter object to a HitterGameEntry and HitterEntry object and commit to the database
        :param hitter: Hitter object to copy
        """
        hitter_game_entry = HitterGameEntry(hitter)
        hitter_entry = HitterEntry(hitter)
        try:
            # Query the database for the HitterEntry object
            db_query = self._session.query(HitterEntry).filter(HitterEntry.pitch_fx_id == hitter.pitch_fx_id)
            hitter_entry_object = db_query.first()
        except:
            print "Query for previous hitter entry failed."
            return

        # Hitter object already exists in database
        if hitter_entry_object is not None:
            stored_date = StatMiner.str_to_date(hitter_entry_object.last_game_date)
            new_date = StatMiner.str_to_date(hitter_entry.last_game_date)
            if new_date > stored_date:
                hitter_entry_object = hitter_entry
                self._session.commit()
        # Hitter object doesn't exist yet in database
        else:
            try:
                self._session.add(hitter_entry)
                self._session.commit()
            except sqlalchemy.exc.IntegrityError:
                print "Attempt to duplicate hitter entry: " + hitter_game_entry.last_name + ", " + \
                      hitter_game_entry.first_name + " " + hitter_game_entry.game_id
                self._session.rollback()
        
        try:
            self._session.add(hitter_game_entry)
            self._session.commit()
        except sqlalchemy.exc.IntegrityError:
            print "Attempt to duplicate hitter game entry: " + hitter_game_entry.last_name + ", " + \
                  hitter_game_entry.first_name + " " + hitter_game_entry.game_id
            self._session.rollback()
    
    # Copy a Pitcher object to a PitcherGameEntry and PitcherEntry object and commit to the database
    # @param    pitcher: Pitcher object to copy        
    def _commit_pitcher(self, pitcher):
        pitcher_game_entry = PitcherGameEntry(pitcher)
        pitcher_entry = PitcherEntry(pitcher)
        try:
            # Query the database for the HitterEntry object
            db_query = self._session.query(PitcherEntry).filter(PitcherEntry.pitch_fx_id == pitcher.pitch_fx_id)
            pitcher_entry_object = db_query.first()
        except:
            print "Query for previous pitcher entry failed."
            return
        
        # Hitter object already exists in database
        if pitcher_entry_object is not None:
            stored_date = StatMiner.str_to_date(pitcher_entry_object.last_game_date)
            new_date = StatMiner.str_to_date(pitcher_entry.last_game_date)
            if new_date > stored_date:
                pitcher_entry_object = pitcher_entry
                self._session.commit()
        # Hitter object doesn't exist yet in database
        else:
            try:
                self._session.add(pitcher_entry)
                self._session.commit()
            except sqlalchemy.exc.IntegrityError:
                print "Attempt to duplicate pitcher entry: " + pitcher_game_entry.last_name + ", " + \
                      pitcher_game_entry.first_name + " " + pitcher_game_entry.game_id
                self._session.rollback()
        
        try:
            self._session.add(pitcher_game_entry)
            self._session.commit()
        except sqlalchemy.exc.IntegrityError:
            print "Attempt to duplicate pitcher game entry: " + pitcher_game_entry.last_name + ", " + \
                  pitcher_game_entry.first_name + " " + pitcher_game_entry.game_id
            self._session.rollback()
