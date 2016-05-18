
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urlparse import urljoin
from urllib import urlretrieve
import csv
import time
from datetime import date
from mlbscrape_python.sql.pregame_hitter import PregameHitterGameEntry
from mlbscrape_python.sql.pregame_pitcher import PregamePitcherGameEntry
from mlbscrape_python.sql.hitter_entry import HitterEntry
from mlbscrape_python.sql.pitcher_entry import PitcherEntry
from sqlalchemy import or_
import heapq


class OptimalLineupDict(dict):

    # The maximum number of pitchers and outfielders allowed in a lineup
    MAX_PITCHERS = 2
    MAX_OUTFIELDERS = 3

    class FieldingPositions:
        """ A string enum for fielding positions in lineups
        """
        CATCHER = "C"
        FIRST_BASE = "1B"
        SECOND_BASE = "2B"
        THIRD_BASE = "3B"
        SHORTSTOP = "SS"
        OUTFIELDER = "OF"

    class PitchingPositions:
        """ A string enum for pitching positions in lineups
        """
        STARTING_PITCHER = "SP"
        RELIEF_PITCHER = "RP"

    def __init__(self):
        """ Constructor used to initialize the total salary and the heaps
        """
        super(OptimalLineupDict, self).__init__()
        self._total_salary = 0
        self[OptimalLineupDict.FieldingPositions.OUTFIELDER] = list()
        self[OptimalLineupDict.PitchingPositions.STARTING_PITCHER] = list()

    def get_total_salary(self):
        """ Get the current salary of this lineup
        :return: int the current salary for this team
        """
        return self._total_salary

    #TODO: move this to the base player sql class
    @staticmethod
    def points_per_dollar(sql_player):
        """ Calculate the predicted points per dollar for this player.
        Return 0 if the Draftkings salary is equal to zero
        :param sql_player: a SQLAlchemy player object
        :return: float representing the predicted points per dollar
        """
        if float(sql_player.draftkings_salary) == 0.0:
            return 0.0

        return float(sql_player.predicted_draftkings_points) / float(sql_player.draftkings_salary)

    def _add_pitcher(self, sql_player):
        """ Add the pitcher object to the pitcher heap if:
        1. There are empty spots on the pitcher heap
        2. The points per dollar metric for the candidate is less than the least valuable pitcher
        :param sql_player: a SQLAlchemy object with the first_name and last_name attribute
        """
        pitcher_heap = self[OptimalLineupDict.PitchingPositions.STARTING_PITCHER]
        # Empty pitcher spots, just add the player
        if len(pitcher_heap) < OptimalLineupDict.MAX_PITCHERS:
            heapq.heappush(pitcher_heap, [self.points_per_dollar(sql_player), sql_player])
            self._total_salary += sql_player.draftkings_salary
        else:
            worst_pitcher = heapq.nsmallest(pitcher_heap, 1)[1]
            if self.points_per_dollar(worst_pitcher) < self.points_per_dollar(sql_player):
                heapq.heappushpop(pitcher_heap, [self.points_per_dollar(sql_player), sql_player])
                self._total_salary -= worst_pitcher.draftkings_salary
                self._total_salary += sql_player.draftkings_salary
            else:
                return False

        return True

    def _add_outfielder(self, sql_player):
        """ Add the outfielder object to the outfielder heap if:
        1. There are empty spots on the outfielder heap
        2. The points per dollar metric for the candidate is less than the least valuable outfielder
        :param sql_player: a SQLAlchemy object with the first_name and last_name attribute
        :return Boolean: True if the player was added, False otherwise
        """
        outfielder_heap = self[OptimalLineupDict.FieldingPositions.OUTFIELDER]
        # Empty outfielder spots, just add the player
        if len(outfielder_heap) < OptimalLineupDict.MAX_OUTFIELDERS:
            heapq.heappush(outfielder_heap, [self.points_per_dollar(sql_player), sql_player])
            self._total_salary += sql_player.draftkings_salary
        else:
            worst_outfielder = heapq.nsmallest(outfielder_heap, 1)[1]
            if self.points_per_dollar(worst_outfielder) < self.points_per_dollar(sql_player):
                heapq.heappushpop(outfielder_heap, [self.points_per_dollar(sql_player), sql_player])
                self._total_salary -= worst_outfielder.draftkings_salary
                self._total_salary += sql_player.draftkings_salary
            else:
                return False

        return True

    def add(self, sql_player):
        """Add a player to the optimal lineup dictionary based on his positions
        :param sql_player: a SQLAlchemy object with the first_name and last_name attribute
        """
        if self._add_player(sql_player, sql_player.primary_position) is not True:
            if sql_player.primary_position != sql_player.secondary_position:
                self._add_player(sql_player, sql_player.secondary_position)

    def _add_player(self, sql_player, position):
        """ Add a player to the optimal lineup dictionary based on his primary position
        :param sql_player: a SQLAlchemy player object
        :return: True if the player was added to the dictionary, False otherwise
        """
        if position == OptimalLineupDict.FieldingPositions.OUTFIELDER:
            if self._add_outfielder(sql_player) is True:
                return True
        elif position == OptimalLineupDict.PitchingPositions.STARTING_PITCHER:
            if self._add_pitcher(sql_player) is True:
                return True
        else:
            try:
                worst_player = self[position]
                if self.points_per_dollar(worst_player) < self.points_per_dollar(sql_player):
                    self[position] = sql_player
                    self._total_salary -= worst_player.draftkings_salary
                    self._total_salary += sql_player.draftkings_salary
                    return True
            except KeyError:
                self[position] = sql_player
                self._total_salary += sql_player.draftkings_salary
                return True

        return False


# Class to interact with Draftkings and obtain the available players and salaries
class Draftkings(object):

    ROTOWIRE_DAILY_LINEUPS_URL = "http://www.rotowire.com/baseball/daily_lineups.htm"
    ROTOWIRE_LINK_TEXT = "See daily player values on DraftKings"
    CONTEST_SALARY = 50000

    class NameNotFound(Exception):
        def __init__(self, name):
            super(Draftkings.NameNotFound, self).__init__("Name '%s' not found in the Baseball Reference page" %
                                                                  name)

    @staticmethod
    def save_daily_csv():
        browser = webdriver.Firefox()
        browser.get(Draftkings.ROTOWIRE_DAILY_LINEUPS_URL)
        draftkings_button = browser.find_element_by_link_text(Draftkings.ROTOWIRE_LINK_TEXT)
        draftkings_button.click()
        browser.switch_to.window(browser.window_handles[len(browser.window_handles)-1])
        wait = WebDriverWait(browser, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'fancybox-outer')))
        print("Page loaded")
        browser.find_element_by_id("fancybox-close").click()
        #wait.until(EC.element_to_be_clickable((By.XPATH, '//div[contains(@class, "tabs")]/ul/li[text() = "All"]')))
        #browser.find_element_by_xpath('//div[contains(@class, "tabs")]/ul/li[text() = "All"]').click()

        # download the file
        csv_url = urljoin(browser.current_url, browser.find_element_by_css_selector("a.export-to-csv").get_attribute("href"))
        urlretrieve(csv_url, "players.csv")

    @staticmethod
    def get_csv_dict(filename=None):
        """ Create a dictionary of dictionaries indexed by a concatentation of name and Draftkings team abbreviation
        """
        if filename is None:
            filename = "players.csv"

        csv_dict = dict()
        with open(filename) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                csv_dict[(row["Name"] + row["teamAbbrev"]).lower()] = row

        return csv_dict

    @staticmethod
    def update_salaries(database_session, csv_dict=None, game_date=None):
        if game_date is None:
            game_date = date.today()
        if csv_dict is None:
            csv_dict = Draftkings.get_csv_dict()
        #Hitters
        pregame_hitters = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == game_date)
        for pregame_entry in pregame_hitters:
            # Lookup the player's name in the database
            # Lookup the name in the dictionary
            hitter_entry = database_session.query(HitterEntry).filter(HitterEntry.rotowire_id == pregame_entry.rotowire_id)[0]
            try:
                csv_entry = csv_dict[(hitter_entry.first_name + " " + hitter_entry.last_name + hitter_entry.team).lower()]
                pregame_entry.draftkings_salary = int(csv_entry["Salary"])
                positions = csv_entry["Position"].split("/")
                pregame_entry.primary_position = positions[0]
                pregame_entry.secondary_position = positions[len(positions) - 1]
                database_session.commit()
            except KeyError:
                print "Player %s not found in the Draftkings CSV file. Deleting entry." % (hitter_entry.first_name + " " + hitter_entry.last_name)
                database_session.delete(pregame_entry)
                database_session.commit()

        # Pitchers
        pregame_pitchers = database_session.query(PregamePitcherGameEntry).filter(PregamePitcherGameEntry.game_date == game_date)
        for pregame_entry in pregame_pitchers:
            # Lookup the player's name in the database
            # Lookup the name in the dictionary
            pitcher_entry = database_session.query(PitcherEntry).filter(PitcherEntry.rotowire_id == pregame_entry.rotowire_id)[0]
            try:
                csv_entry = csv_dict[(pitcher_entry.first_name + " " + pitcher_entry.last_name + pitcher_entry.team).lower()]
                pregame_entry.draftkings_salary = int(csv_entry["Salary"])
                database_session.commit()
            except KeyError:
                print "Player %s not found in the Draftkings CSV file. Deleting entry." % (pitcher_entry.first_name + " " + pitcher_entry.last_name)
                database_session.delete(pregame_entry)
                database_session.commit()

    @staticmethod
    def get_hitter_points(postgame_hitter):
        points = float()
        points += 3*postgame_hitter.game_1b
        points += 5*postgame_hitter.game_2b
        points += 8*postgame_hitter.game_3b
        points += 10*postgame_hitter.game_hr
        points += 2*postgame_hitter.game_rbi
        points += 2*postgame_hitter.game_r
        points += 2*postgame_hitter.game_bb
        points += 2*postgame_hitter.game_hbp
        points += 5*postgame_hitter.game_sb

        return points

    @staticmethod
    def get_pitcher_points(postgame_pitcher):
        points = float()
        string_ip = str(postgame_pitcher.game_ip)
        innings_pitched_float = 0.333*float(string_ip.split(".")[1]) + float(string_ip.split(".")[0])
        points += 2.25*innings_pitched_float
        points += 2*postgame_pitcher.game_so
        points += 4*postgame_pitcher.game_wins
        points -= 2*postgame_pitcher.game_er
        points -= 0.6*postgame_pitcher.game_h
        points -= 0.6*postgame_pitcher.game_bb
        points -= 0.6*postgame_pitcher.game_hbp
        points += 2.5*postgame_pitcher.game_cg
        points += 2.5*postgame_pitcher.game_cgso
        points += 5*postgame_pitcher.game_no_hitter

        return points


    @staticmethod
    def get_optimal_lineup(database_session):
        """ Get the optimal lineup of the players to choose for tonight
        :param database_session: SQLAlchemy database session
        :return:
        """
        optimal_lineup_dict = dict()
        player_heap = list()
        current_salary = 0
        # Look for the hitter entries
        for fielding_position in vars(Draftkings.FieldingPositions):
            query_results = database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry == date.today(),
                                                                                  or_(PregameHitterGameEntry.primary_position == fielding_position,
                                                                                      PregameHitterGameEntry.secondary_position == fielding_position)).order_by(PregameHitterGameEntry.predicted_draftkings_points)
            if fielding_position == Draftkings.FieldingPositions.OUTFIELDER and query_results.count() > 2:
                optimal_lineup_dict[fielding_position] = list([query_results[0], query_results[1], query_results[2]])
                current_salary += (query_results[0].draftkings_salary + query_results[1].draftkings_salary + query_results[2].draftkings_salary)
                if query_results.count() > 3:
                    for player in query_results[3:query_results.count()]:
                        try:
                            heapq.heappush(player_heap, (float(player.predicted_draftkings_points)/float(player.draftkings_salary), player))
                        except ZeroDivisionError:
                            pass
            else:
                optimal_lineup_dict[fielding_position] = query_results.first()
                current_salary += optimal_lineup_dict[fielding_position].draftkings_salary
                if query_results.count() > 1:
                    for player in query_results[1:query_results.count()]:
                        try:
                            heapq.heappush(player_heap, (float(player.predicted_draftkings_points)/float(player.draftkings_salary), player))
                        except ZeroDivisionError:
                            pass

        # Look for pitchers
        query_results = database_session.query(PregamePitcherGameEntry).filter(PregamePitcherGameEntry.game_date == date.today()).order_by(PregamePitcherGameEntry.predicted_draftkings_points)
        if query_results.count() > 1:
            optimal_lineup_dict[fielding_position] = list([query_results[0], query_results[1]])
            current_salary += (query_results[0].draftkings_salary + query_results[1].draftkings_salary)
            if query_results.count() > 2:
                for player in query_results[2:query_results.count()]:
                    try:
                        heapq.heappush(player_heap, (float(player.predicted_draftkings_points)/float(player.draftkings_salary), player))
                    except ZeroDivisionError:
                        pass

        # Replace players one by one who are "overpaid" based on predicted points per dollar
        while current_salary > Draftkings.CONTEST_SALARY and len(player_heap) > 0:
            next_player = heapq.heappop(player_heap)
            # Pitchers
            if isinstance(next_player[1], PregamePitcherGameEntry):
                for i in range(len(optimal_lineup_dict[Draftkings.PitchingPositions.STARTING_PITCHER])-1,0,-1):
                    player_replaced = optimal_lineup_dict[Draftkings.PitchingPositions.STARTING_PITCHER][i]
                    try:
                        if float(player_replaced.predicted_draftkings_points)/float(player_replaced.draftkings_salary) < next_player[0]:
                            current_salary -= player_replaced.draftkings_salary
                            optimal_lineup_dict[Draftkings.PitchingPositions.STARTING_PITCHER][i] = next_player[1]
                            current_salary += next_player[1].draftkings_salary
                            break
                    except ZeroDivisionError:
                        pass
            # Hitters
            else:
                hitter_heap = list()
                if next_player[1].primary_position == Draftkings.FieldingPositions.OUTFIELDER:
                    for optimal_hitter in optimal_lineup_dict[next_player[1].primary_position]:
                        try:
                            heapq.heappush(hitter_heap, (float(optimal_hitter.draftkings_salary)/float(optimal_hitter.predicted_draftkings_points),
                                                         Draftkings.FieldingPositions.OUTFIELDER, optimal_hitter))
                        except ZeroDivisionError:
                            pass
                else:
                    optimal_hitter = optimal_lineup_dict[next_player[1].primary_position]
                    try:
                        heapq.heappush(hitter_heap, (float(optimal_hitter.draftkings_salary)/float(optimal_hitter.predicted_draftkings_points),
                                                     next_player[1].primary_position, optimal_hitter))
                    except ZeroDivisionError:
                        pass

                if next_player[1].secondary_position != next_player[1].primary_position:
                    if next_player[1].secondary_position == Draftkings.FieldingPositions.OUTFIELDER:
                        for optimal_hitter in optimal_lineup_dict[next_player[1].secondary_position]:
                            try:
                                heapq.heappush(hitter_heap, (float(optimal_hitter.draftkings_salary)/float(optimal_hitter.predicted_draftkings_points),
                                                             next_player[1].secondary_position, optimal_hitter))
                            except ZeroDivisionError:
                                pass
                    else:
                        try:
                            heapq.heappush(hitter_heap, (float(optimal_hitter.draftkings_salary)/float(optimal_hitter.predicted_draftkings_points),
                                                         next_player[1].secondary_position, optimal_hitter))
                        except ZeroDivisionError:
                            pass

                while len(hitter_heap) > 0:
                    player_replaced = hitter_heap.heappop()
                    if float(player_replaced[0]) < next_player[0]:
                        if player_replaced[1] == Draftkings.FieldingPositions.OUTFIELDER:
                            for i in range(0, len(optimal_lineup_dict[Draftkings.FieldingPositions.OUTFIELDER])):
                                if optimal_lineup_dict[Draftkings.FieldingPositions.OUTFIELDER][i].rotowire_id == player_replaced[2].rotowire_id:
                                    optimal_lineup_dict[Draftkings.FieldingPositions.OUTFIELDER][i] = next_player[1]
                        else:
                            optimal_lineup_dict[player_replaced[1]] = next_player[1]

                        current_salary -= player_replaced[2].draftkings_salary
                        current_salary += next_player[1].draftkings_salary

        return optimal_lineup_dict


