
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urlparse import urljoin
from urllib import urlretrieve
import csv
from datetime import date
from sql.pregame_hitter import PregameHitterGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.hitter_entry import HitterEntry
from sql.pitcher_entry import PitcherEntry
from sqlalchemy import desc, or_
import heapq
from learn.train_network import HitterNetworkTrainer, PitcherNetworkTrainer


class OptimalLineupDict(dict):

    # The maximum number of pitchers and outfielders allowed in a lineup
    MAX_PITCHERS = 2
    MAX_OUTFIELDERS = 3

    FieldingPositions = ["C", "1B", "2B", "3B", "SS", "OF"]
    PitchingPositions = ["SP", "RP"]

    def __init__(self):
        """ Constructor used to initialize the total salary and the heaps
        """
        super(OptimalLineupDict, self).__init__()
        self._total_salary = 0
        self["OF"] = list()
        self["SP"] = list()

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

    #TODO: move this to the base player sql class
    @staticmethod
    def dollars_per_point(sql_player):
        """ Calculate the predicted points per dollar for this player.
        Return 0 if the Draftkings salary is equal to zero
        :param sql_player: a SQLAlchemy player object
        :return: float representing the predicted points per dollar
        """
        return float(sql_player.draftkings_salary) / float(sql_player.predicted_draftkings_points)

    def _add_pitcher(self, sql_player):
        """ Add the pitcher object to the pitcher heap if:
        1. There are empty spots on the pitcher heap
        2. The points per dollar metric for the candidate is less than the least valuable pitcher
        :param sql_player: a SQLAlchemy object with the first_name and last_name attribute
        """
        pitcher_heap = self["SP"]
        try:
            dollars_per_point = self.dollars_per_point(sql_player)
        except ZeroDivisionError:
            return False
        # Empty pitcher spots, just add the player
        if len(pitcher_heap) < OptimalLineupDict.MAX_PITCHERS:
            heapq.heappush(pitcher_heap, (dollars_per_point, sql_player))
            self._total_salary += sql_player.draftkings_salary
        else:
            worst_pitcher = heapq.nlargest(pitcher_heap, 1)[0][1]
            if self.dollars_per_point(worst_pitcher) > dollars_per_point:
                heapq.heappushpop(pitcher_heap, (dollars_per_point, sql_player))
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
        outfielder_heap = self["OF"]
        try:
            dollars_per_point = self.dollars_per_point(sql_player)
        except ZeroDivisionError:
            return False

        # Empty outfielder spots, just add the player
        if len(outfielder_heap) < OptimalLineupDict.MAX_OUTFIELDERS:
            heapq.heappush(outfielder_heap, (dollars_per_point, sql_player))
            self._total_salary += sql_player.draftkings_salary
        else:
            worst_outfielder = heapq.nlargest(1, outfielder_heap)[0][1]
            if self.dollars_per_point(worst_outfielder) < dollars_per_point:
                heapq.heappushpop(outfielder_heap, (dollars_per_point, sql_player))
                self._total_salary -= worst_outfielder.draftkings_salary
                self._total_salary += sql_player.draftkings_salary
            else:
                return False

        return True

    def add(self, sql_player):
        """Add a player to the optimal lineup dictionary based on his positions
        :param sql_player: a SQLAlchemy object with the first_name and last_name attribute
        """
        if type(sql_player) is PregamePitcherGameEntry:
            self._add_pitcher(sql_player)
        else:
            if self._add_player(sql_player, sql_player.primary_position) is not True:
                if sql_player.primary_position != sql_player.secondary_position:
                    self._add_player(sql_player, sql_player.secondary_position)

    def _add_player(self, sql_player, position):
        """ Add a player to the optimal lineup dictionary based on his primary position
        :param sql_player: a SQLAlchemy player object
        :return: True if the player was added to the dictionary, False otherwise
        """
        if position == "OF":
            if self._add_outfielder(sql_player) is True:
                return True
        elif position == "SP":
            if self._add_pitcher(sql_player) is True:
                return True
        else:
            try:
                worst_player = self[position]
                if self.dollars_per_point(worst_player) < self.dollars_per_point(sql_player):
                    self[position] = sql_player
                    self._total_salary -= worst_player.draftkings_salary
                    self._total_salary += sql_player.draftkings_salary
                    return True
            except KeyError:
                self[position] = sql_player
                self._total_salary += sql_player.draftkings_salary
                return True
            except ZeroDivisionError:
                return False

        return False

    def __str__(self):
        ret_str = str()
        for fielding_position in OptimalLineupDict.FieldingPositions:
            if fielding_position == "OF":
                for outfielder in self["OF"]:
                    try:
                        ret_str += "%s: %s\n" % ("OF", outfielder[1])
                    except KeyError:
                        ret_str += "%s: \n" % "OF"
            else:
                try:
                    ret_str += "%s: %s\n" % (fielding_position, self[fielding_position])
                except KeyError:
                    ret_str += "%s: \n" % fielding_position

        for pitcher in self["SP"]:
            try:
                ret_str += "%s: %s\n" % ("SP", pitcher[1])
            except KeyError:
                ret_str += "%s: \n" % "SP"

        ret_str += "Total salary: %s" % self._total_salary

        return ret_str

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
    #TODO: migrate to intermediary miner
    def update_salaries(database_session, csv_dict=None, game_date=None):
        if game_date is None:
            game_date = date.today()
        if csv_dict is None:
            csv_dict = Draftkings.get_csv_dict()
        #Hitters
        pregame_hitters = PregameHitterGameEntry.get_all_daily_entries(database_session, game_date)
        for pregame_entry in pregame_hitters:
            # Lookup the player's name in the database
            # Lookup the name in the dictionary
            hitter_entry = database_session.query(HitterEntry).filter(HitterEntry.rotowire_id == pregame_entry.rotowire_id).first()
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
        pregame_pitchers = PregamePitcherGameEntry.get_all_daily_entries(database_session, game_date)
        for pregame_entry in pregame_pitchers:
            # Lookup the player's name in the database
            # Lookup the name in the dictionary
            pitcher_entry = database_session.query(PitcherEntry).filter(PitcherEntry.rotowire_id == pregame_entry.rotowire_id).first()
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
    #TODO: migrate to an intermediary miner
    def get_optimal_lineup(database_session, day=None):
        """ Get the optimal lineup of the players to choose for tonight
        :param database_session: SQLAlchemy database session
        :return:
        """
        if day is None:
            day = date.today()
        optimal_lineup = OptimalLineupDict()
        player_heap = list()

        # Look for the hitter entries
        for fielding_position in OptimalLineupDict.FieldingPositions:
            query_results = PregameHitterGameEntry.get_daily_entries_by_position(database_session, fielding_position, day)
            query_results = list(query_results.order_by(desc(PregameHitterGameEntry.predicted_draftkings_points)))
            if fielding_position == "OF":
                for i in range(0, OptimalLineupDict.MAX_OUTFIELDERS):
                    optimal_lineup.add(heapq.heappop(query_results))
            else:
                optimal_lineup.add(heapq.heappop(query_results))
            for player in query_results:
                try:
                    dollars_per_point = OptimalLineupDict.dollars_per_point(player)
                    if dollars_per_point > 0:
                        heapq.heappush(player_heap, (dollars_per_point, player))
                except ZeroDivisionError:
                    continue

        # Look for pitchers
        query_results = PregamePitcherGameEntry.get_all_daily_entries(database_session, day)
        query_results = list(query_results.order_by(desc(PregamePitcherGameEntry.predicted_draftkings_points)))
        for i in range(0, OptimalLineupDict.MAX_PITCHERS):
            optimal_lineup.add(heapq.heappop(query_results))

        for pitcher in query_results:
            try:
                dollars_per_point = OptimalLineupDict.dollars_per_point(pitcher)
                if dollars_per_point > 0:
                    heapq.heappush(player_heap, (OptimalLineupDict.dollars_per_point(pitcher), pitcher))
            except ZeroDivisionError:
                continue

        # Replace players one by one who are "overpaid" based on predicted points per dollar
        while optimal_lineup.get_total_salary() > Draftkings.CONTEST_SALARY and len(player_heap) > 0:
            next_player = heapq.heappop(player_heap)
            optimal_lineup.add(next_player)

        # Print out all the remaining players in order of their value
        print "Runner-up players"
        for player in player_heap:
            print player[1]
        print " "

        return optimal_lineup

    @staticmethod
    def predict_daily_points(database_session, day=None):
        if day is None:
            day = date.today()
        daily_entries = PregameHitterGameEntry.get_all_daily_entries(database_session, day)
        for daily_entry in daily_entries:
            predicted_points = HitterNetworkTrainer.get_prediction(daily_entry.to_input_vector())
            if predicted_points < 0:
                predicted_points = 0
            daily_entry.predicted_draftkings_points = predicted_points
            database_session.commit()

        daily_entries = PregamePitcherGameEntry.get_all_daily_entries(database_session, day)
        for daily_entry in daily_entries:
            predicted_points = PitcherNetworkTrainer.get_prediction(daily_entry.to_input_vector())
            if predicted_points < 0:
                predicted_points = 0
            daily_entry.predicted_draftkings_points = predicted_points
            database_session.commit()

