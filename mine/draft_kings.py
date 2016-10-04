
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urlparse import urljoin
from urllib import urlretrieve
import csv
from datetime import date, datetime
from Released.mlbscrape_python.sql.pregame_hitter import PregameHitterGameEntry
from Released.mlbscrape_python.sql.pregame_pitcher import PregamePitcherGameEntry
from Released.mlbscrape_python.sql.hitter_entry import HitterEntry
from Released.mlbscrape_python.sql.pitcher_entry import PitcherEntry
from sqlalchemy import desc, or_
import heapq
from Released.mlbscrape_python.learn.train_regression import HitterRegressionForestTrainer, PitcherRegressionForestTrainer, HitterRegressionTrainer, PitcherRegressionTrainer
from Released.mlbscrape_python.sql.lineup import LineupEntry
import numpy as np
from email_service import send_email


class Position(object):
    def __init__(self, position_string):
        self._salary = 0
        self._player = None
        self._position_string = position_string

    def add(self, sql_player, maximum_salary):
        if self._player is None:
            if sql_player.draftkings_salary <= maximum_salary:
                self._player = sql_player
                return True
        else:
            try:
                if self._player.points_per_dollar() < sql_player.points_per_dollar():
                    if sql_player.draftkings_salary <= maximum_salary + self._player.draftkings_salary:
                        self._player = sql_player
                        return True
            except ZeroDivisionError:
                pass

        return False

    def get_total_salary(self):
        if self._player is None:
            return 0

        return self._player.draftkings_salary

    def is_open(self):
        return self._player is None

    def get_worst_player_points(self):
        return self._player.predicted_draftkings_points

    def is_player_assigned(self, sql_player):
        return self._player == sql_player

    def __str__(self):
        return "%s: %s\n" % (self._position_string, self._player)

    def is_valid(self):
        return self._player is not None


class PositionHeap(object):
    def __init__(self, max_players, position_string):
        """ Constructor
        :param max_players: maximum number of players at this position
        :param position_string: a str() representing the position abbreviation
        """
        self._max_players = max_players
        self._position_string = position_string
        self._position_heap = list()

    def add(self, sql_player, maximum_salary):
        """ Add a player to the position heap
        :param sql_player: SQLAlchemy player
        :param maximum_salary: the salary available for the meta object
        :return True if the player was added, False otherwise
        """
        is_added = False
        if len(self._position_heap) < self._max_players:
            if sql_player.draftkings_salary <= maximum_salary:
                heapq.heappush(self._position_heap, (sql_player.predicted_draftkings_points, sql_player))
                is_added = True
        else:
            temp_heap = list()
            while len(self._position_heap) > 0:
                player = heapq.heappop(self._position_heap)[1]
                if is_added:
                    heapq.heappush(temp_heap, (player.predicted_draftkings_points, player))
                else:
                    try:
                        if player.points_per_dollar() < sql_player.points_per_dollar():
                            if sql_player.draftkings_salary <= maximum_salary + player.draftkings_salary:
                                heapq.heappush(temp_heap, (sql_player.predicted_draftkings_points, sql_player))
                                is_added = True
                    except ZeroDivisionError:
                        heapq.heappush(temp_heap, (player.predicted_draftkings_points, player))

            self._position_heap = temp_heap

        return is_added

    def get_total_salary(self):
        """ Get the total salary for this position heap
        :return: total salary in dollars
        """
        return sum(player[1].draftkings_salary for player in self._position_heap)

    def is_open(self):
        return len(self._position_heap) < self._max_players

    def get_worst_player_points(self):
        return self._position_heap[0][0]

    def is_player_assigned(self, sql_player):
        for player in self._position_heap:
            if player == sql_player:
                return True

        return False

    def __str__(self):
        ret_str = str()
        for player in self._position_heap:
            ret_str += "%s: %s\n" % (self._position_string, player[1])
        return ret_str

    def is_valid(self):
        return len(self._position_heap) == self._max_players


class OptimalLineupDict(dict):
    """ Class for managing the optimal lineup for a given day
    """
    # The maximum number of pitchers and outfielders allowed in a lineup
    MAX_PITCHERS = 2
    MAX_OUTFIELDERS = 3

    FieldingPositions = ["C", "1B", "2B", "3B", "SS", "OF"]
    PitchingPositions = ["SP", "RP"]

    def __init__(self):
        """ Constructor used to initialize the total salary and the heaps
        """
        super(OptimalLineupDict, self).__init__()
        self.catcher = Position("C")
        self.first_baseman = Position("1B")
        self.second_baseman = Position("2B")
        self.third_baseman = Position("3B")
        self.shortstop = Position("SS")
        self.outfielders = PositionHeap(OptimalLineupDict.MAX_OUTFIELDERS, "OF")
        self.starting_pitchers = PositionHeap(OptimalLineupDict.MAX_PITCHERS, "SP")
        self.position_map = dict()
        self.position_map["C"] = self.catcher
        self.position_map["1B"] = self.first_baseman
        self.position_map["2B"] = self.second_baseman
        self.position_map["3B"] = self.third_baseman
        self.position_map["SS"] = self.shortstop
        self.position_map["SP"] = self.starting_pitchers
        self.position_map["OF"] = self.outfielders

    def get_total_salary(self):
        """ Get the current salary of this lineup
        :return: int the current salary for this team
        """
        return sum(self.position_map[position].get_total_salary() for position in OptimalLineupDict.FieldingPositions) + \
               self.position_map["SP"].get_total_salary()

    def is_position_open(self, position):
        return self.position_map[position].is_open()

    def add(self, sql_player):
        """Add a player to the optimal lineup dictionary based on his positions
        :param sql_player: a SQLAlchemy object with the first_name and last_name attribute
        """

        if type(sql_player) is PregamePitcherGameEntry:
            self._add_player(sql_player, "SP")
        else:
            best_position_candidate, worst_position_candidate = self.get_position_priorities(sql_player.primary_position,
                                                                                             sql_player.secondary_position)
            if not self._add_player(sql_player, best_position_candidate):
                self._add_player(sql_player, worst_position_candidate)

    def get_position_priorities(self, primary_position, secondary_position):
        """ Decide which position would be better for this player to play based on projected points
        :param primary_position: the primary position of the player
        :param secondary_position: the secondary position of the player
        :return: a list of the posiitons from most suitable to least suitable
        """

        # Primary position is open
        if self.is_position_open(primary_position):
            return primary_position, secondary_position

        # Primary position not open, Secondary position is open
        if self.is_position_open(secondary_position):
            return secondary_position, primary_position
        # Both positions not open, some arbitration required
        else:
            if self.position_map[primary_position].get_worst_player_points() < \
                    self.position_map[secondary_position].get_worst_player_points():
                return secondary_position, primary_position

        return primary_position, secondary_position

    def _add_player(self, sql_player, position):
        """ Add a player to the optimal lineup dictionary based on his primary position
        :param sql_player: a SQLAlchemy player object
        :return: True if the player was added to the dictionary, False otherwise
        """

        if self.is_in_dict(sql_player):
            return False

        return self.position_map[position].add(sql_player, Draftkings.CONTEST_SALARY - self.get_total_salary())

    def is_in_dict(self, sql_player):
        return_value = False
        if type(sql_player) is PregamePitcherGameEntry:
            return self.position_map["SP"].is_player_assigned(sql_player)
        else:
            for fielding_position in OptimalLineupDict.FieldingPositions:
                if self.position_map[fielding_position].is_player_assigned(sql_player):
                    return True

        return return_value

    def __str__(self):
        ret_str = str()
        for fielding_position in OptimalLineupDict.FieldingPositions:
            ret_str += str(self.position_map[fielding_position])

        ret_str += str(self.position_map["SP"])

        ret_str += "Total salary: %s" % self.get_total_salary()

        return ret_str

    def is_valid(self):
        if not self.position_map["SP"].is_valid():
            return False
        for position in OptimalLineupDict.FieldingPositions:
            if not self.position_map[position].is_valid():
                return False

        return True

    def get_worst_position(self):
        """ Get the position with the player with the least predicted points
        :return: the string of the worst position
        """
        worst_point_value = self.position_map["C"].get_worst_player_points()
        position = str()
        for fielding_position in OptimalLineupDict.FieldingPositions:
            if self.position_map[fielding_position].get_worst_player_points() <= worst_point_value:
                worst_point_value = self.position_map[fielding_position].get_worst_player_points()
                position = fielding_position

        if self.position_map["SP"].get_worst_player_points() <= worst_point_value:
            position = "SP"

        return position


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
        browser = webdriver.Chrome()
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
            hitter_entry = database_session.query(HitterEntry).get(pregame_entry.rotowire_id)
            if hitter_entry is None:
                print "Player %s not found in the Draftkings CSV file. Deleting entry." % pregame_entry.rotowire_id
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
            pitcher_entry = database_session.query(PitcherEntry).get(pregame_entry.rotowire_id)
            if pitcher_entry is None:
                print "Player %s not found in the Draftkings CSV file. Deleting entry." % pregame_entry.rotowire_id
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
        :return: an OptimalLineupDict structure
        """
        if day is None:
            day = date.today()
        optimal_lineup = OptimalLineupDict()
        player_heap = dict()

        # Look for the hitter entries
        for fielding_position in OptimalLineupDict.FieldingPositions:
            query_results = PregameHitterGameEntry.get_daily_entries_by_position(database_session, fielding_position, day)
            query_results = list(query_results.order_by(desc(PregameHitterGameEntry.predicted_draftkings_points)))
            query_result_heap = list()
            for query_result in query_results:
                heapq.heappush(query_result_heap, (-query_result.predicted_draftkings_points, query_result))
            while not optimal_lineup.position_map[fielding_position].is_valid() and len(query_results) > 0:
                candidate_player = heapq.heappop(query_result_heap)[1]
                optimal_lineup.add(candidate_player)

            player_heap[fielding_position] = list()
            while len(query_result_heap) > 0:
                player = heapq.heappop(query_result_heap)
                heapq.heappush(player_heap[fielding_position], player)

        # Look for pitchers
        query_results = PregamePitcherGameEntry.get_all_daily_entries(database_session, day)
        query_results = list(query_results.order_by(desc(PregamePitcherGameEntry.predicted_draftkings_points)))
        for query_result in query_results:
            heapq.heappush(query_result_heap, (-query_result.predicted_draftkings_points, query_result))
        while not optimal_lineup.position_map["SP"].is_valid() and len(query_results) > 0:
            candidate_player = heapq.heappop(query_result_heap)[1]
            optimal_lineup.add(candidate_player)

        player_heap["SP"] = list()
        while len(query_result_heap) > 0:
            player = heapq.heappop(query_result_heap)
            heapq.heappush(player_heap["SP"], player)

        # Replace players one by one who are "overpaid" based on predicted points per dollar
        while (optimal_lineup.get_total_salary() > Draftkings.CONTEST_SALARY and len(player_heap) > 0) or \
                not optimal_lineup.is_valid():
            worst_position = optimal_lineup.get_worst_position()
            next_player = heapq.heappop(player_heap[worst_position])[1]
            optimal_lineup.add(next_player)

        # Print out all the remaining players in order of their value
        runner_up_text = "Runner-up players\n"
        for fielding_position in OptimalLineupDict.FieldingPositions:
            runner_up_text += fielding_position + "\n"
            while len(player_heap[fielding_position]) > 0:
                player = heapq.heappop(player_heap[fielding_position])
                runner_up_text += "%s\n" % str(player[1])
            runner_up_text += "\n"

        runner_up_text += "SP\n"
        while len(player_heap["SP"]) > 0:
            player = heapq.heappop(player_heap["SP"])
            runner_up_text += "%s\n" % str(player[1])

        send_email(runner_up_text)
        print runner_up_text

        # Commit the prediction to the database
        lineup_db_entry = LineupEntry()
        lineup_db_entry.game_date = date.today()
        lineup_db_entry.game_time = datetime.now().strftime("%H:%M:%S")
        lineup_db_entry.starting_pitcher_1 = optimal_lineup.position_map["SP"]._position_heap[0][1].rotowire_id
        lineup_db_entry.starting_pitcher_2 = optimal_lineup.position_map["SP"]._position_heap[1][1].rotowire_id
        lineup_db_entry.catcher = optimal_lineup.position_map["C"]._player.rotowire_id
        lineup_db_entry.first_baseman = optimal_lineup.position_map["1B"]._player.rotowire_id
        lineup_db_entry.second_baseman = optimal_lineup.position_map["2B"]._player.rotowire_id
        lineup_db_entry.third_baseman = optimal_lineup.position_map["3B"]._player.rotowire_id
        lineup_db_entry.shortstop = optimal_lineup.position_map["SS"]._player.rotowire_id
        lineup_db_entry.outfielder_1 = optimal_lineup.position_map["OF"]._position_heap[0][1].rotowire_id
        lineup_db_entry.outfielder_2 = optimal_lineup.position_map["OF"]._position_heap[1][1].rotowire_id
        lineup_db_entry.outfielder_3 = optimal_lineup.position_map["OF"]._position_heap[2][1].rotowire_id
        database_session.add(lineup_db_entry)
        database_session.commit()

        return optimal_lineup

    @staticmethod
    def predict_daily_points(database_session, day=None):
        if day is None:
            day = date.today()
        #hitter_regression = HitterRegressionTrainer()
        hitter_regression = HitterRegressionForestTrainer()
        hitter_regression.train_network()
        #pitcher_regression = PitcherRegressionTrainer()
        pitcher_regression = PitcherRegressionForestTrainer()
        pitcher_regression.train_network()
        daily_entries = PregameHitterGameEntry.get_all_daily_entries(database_session, day)
        for daily_entry in daily_entries:
            predicted_points = hitter_regression.get_prediction(daily_entry.to_input_vector())

            if predicted_points < 0:
                predicted_points = 0
            daily_entry.predicted_draftkings_points = predicted_points
            database_session.commit()

        daily_entries = PregamePitcherGameEntry.get_all_daily_entries(database_session, day)
        for daily_entry in daily_entries:
            hitter_array = daily_entry.get_opponent_vector(database_session)
            final_array = np.concatenate([daily_entry.to_input_vector(), hitter_array])
            predicted_points = pitcher_regression.get_prediction(final_array)
            if predicted_points < 0:
                predicted_points = 0
            daily_entry.predicted_draftkings_points = predicted_points
            database_session.commit()