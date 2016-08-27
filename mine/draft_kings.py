
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
from Released.mlbscrape_python.learn.train_regression import HitterRegressionForestTrainer, PitcherRegressionForestTrainer
from Released.mlbscrape_python.sql.lineup import LineupEntry


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
        self._total_salary = 0
        for position in OptimalLineupDict.FieldingPositions:
            self[position] = None
        self["OF"] = list()
        self["SP"] = list()

    def get_total_salary(self):
        """ Get the current salary of this lineup
        :return: int the current salary for this team
        """
        return self._total_salary

    def is_position_open(self, position):
        try:
            if self[position] is None:
                return True
            elif position == "OF" and len(self["OF"]) == 3:
                return True
        except KeyError:
            return True

        return True

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
            if primary_position == "OF":
                primary_player = self["OF"][0][1]
            else:
                primary_player = self[primary_position]

            if secondary_position == "OF":
                secondary_player = self["OF"][0][1]
            else:
                secondary_player = self[secondary_position]

            if primary_player.predicted_draftkings_points < secondary_player.predicted_draftkings_points:
                return secondary_position, primary_position

        return primary_position, secondary_position

    def _add_player(self, sql_player, position):
        """ Add a player to the optimal lineup dictionary based on his primary position
        :param sql_player: a SQLAlchemy player object
        :return: True if the player was added to the dictionary, False otherwise
        """

        if self.is_in_dict(sql_player):
            return False

        try:
            points_per_dollar = sql_player.points_per_dollar()
        except ZeroDivisionError:
            return False

        if position == "SP":
            max_number_players = OptimalLineupDict.MAX_PITCHERS
        elif position == "OF":
            max_number_players = OptimalLineupDict.MAX_OUTFIELDERS
        else:
            max_number_players = 0

        if position == "SP" or position == "OF":
            if len(self[position]) < max_number_players:
                if self.get_total_salary() + sql_player.draftkings_salary <= Draftkings.CONTEST_SALARY:
                    heapq.heappush(self[position], (sql_player.predicted_draftkings_points, sql_player))
                    self._total_salary += sql_player.draftkings_salary
                    return True
            else:
                for i in range(0, len(self[position])):
                    worst_player = self[position][i][1]
                    if worst_player.points_per_dollar() < points_per_dollar:
                        if self.get_total_salary() + sql_player.draftkings_salary - worst_player.draftkings_salary <= Draftkings.CONTEST_SALARY:
                            heapq.heappushpop(self[position], (sql_player.predicted_draftkings_points, sql_player))
                            self._total_salary -= worst_player.draftkings_salary
                            self._total_salary += sql_player.draftkings_salary
                            return True
        else:
            if self[position] is None:
                if self.get_total_salary() + sql_player.draftkings_salary <= Draftkings.CONTEST_SALARY:
                    self._total_salary += sql_player.draftkings_salary
                    self[position] = sql_player
                    return True
            worst_player = self[position]
            if worst_player.points_per_dollar() < points_per_dollar:
                if self.get_total_salary() + sql_player.draftkings_salary - worst_player.draftkings_salary <= Draftkings.CONTEST_SALARY:
                    self._total_salary -= worst_player.draftkings_salary
                    self._total_salary += sql_player.draftkings_salary
                    self[position] = sql_player
                    return True

        return False

    def is_in_dict(self, sql_player):
        try:
            if type(sql_player) is PregamePitcherGameEntry:
                for pitcher in self["SP"]:
                    if pitcher == sql_player:
                        return True

            else:
                for fielding_position in OptimalLineupDict.FieldingPositions:
                    if fielding_position == "OF":
                        for outfielder in self["OF"]:
                            if outfielder[1] == sql_player:
                                return True
                    else:
                        if self[sql_player.primary_position] == sql_player or self[sql_player.secondary_position] == sql_player:
                            return True
        except KeyError:
            pass

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

    def is_valid(self):
        try:
            if len(self["SP"]) == OptimalLineupDict.MAX_PITCHERS and len(self["OF"]) == OptimalLineupDict.MAX_OUTFIELDERS \
            and self["1B"] is not None and self["2B"] is not None and self["3B"] is not None and self["SS"] is not None \
            and self["C"] is not None:
                return True
        except KeyError:
            return False

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
        player_heap = list()

        # Look for the hitter entries
        for fielding_position in OptimalLineupDict.FieldingPositions:
            query_results = PregameHitterGameEntry.get_daily_entries_by_position(database_session, fielding_position, day)
            query_results = list(query_results.order_by(desc(PregameHitterGameEntry.predicted_draftkings_points)))
            if fielding_position == "OF":
                while len(optimal_lineup["OF"]) < OptimalLineupDict.MAX_OUTFIELDERS and len(query_results) > 0:
                    candidate_player = heapq.heappop(query_results)
                    if not optimal_lineup.is_in_dict(candidate_player):
                        optimal_lineup.add(candidate_player)
            else:
                try:
                    candidate_player = heapq.heappop(query_results)
                except IndexError:
                    print "Exception."
                if not optimal_lineup.is_in_dict(candidate_player):
                    optimal_lineup.add(candidate_player)
            for player in query_results:
                try:
                    heapq.heappush(player_heap, (-player.predicted_draftkings_points, player))
                except ZeroDivisionError:
                    continue

        # Look for pitchers
        query_results = PregamePitcherGameEntry.get_all_daily_entries(database_session, day)
        query_results = list(query_results.order_by(desc(PregamePitcherGameEntry.predicted_draftkings_points)))
        for i in range(0, OptimalLineupDict.MAX_PITCHERS):
            candidate_player = heapq.heappop(query_results)
            if not optimal_lineup.is_in_dict(candidate_player):
                optimal_lineup.add(candidate_player)

        for pitcher in query_results:
            try:
                heapq.heappush(player_heap, (-pitcher.predicted_draftkings_points, pitcher))
            except ZeroDivisionError:
                continue

        # Replace players one by one who are "overpaid" based on predicted points per dollar
        while (optimal_lineup.get_total_salary() > Draftkings.CONTEST_SALARY and len(player_heap) > 0) or \
                not optimal_lineup.is_valid():
            next_player = heapq.heappop(player_heap)[1]
            if not optimal_lineup.is_in_dict(next_player):
                optimal_lineup.add(next_player)

        # Print out all the remaining players in order of their value
        print "Runner-up players"
        for player in player_heap:
            print player[1]
        print " "

        # Commit the prediction to the database
        lineup_db_entry = LineupEntry()
        lineup_db_entry.game_date = date.today()
        lineup_db_entry.game_time = datetime.now().strftime("%H:%M:%S")
        lineup_db_entry.starting_pitcher_1 = optimal_lineup["SP"][0][1].rotowire_id
        lineup_db_entry.starting_pitcher_2 = optimal_lineup["SP"][1][1].rotowire_id
        lineup_db_entry.catcher = optimal_lineup["C"].rotowire_id
        lineup_db_entry.first_baseman = optimal_lineup["1B"].rotowire_id
        lineup_db_entry.second_baseman = optimal_lineup["2B"].rotowire_id
        lineup_db_entry.third_baseman = optimal_lineup["3B"].rotowire_id
        lineup_db_entry.shortstop = optimal_lineup["SS"].rotowire_id
        lineup_db_entry.outfielder_1 = optimal_lineup["OF"][0][1].rotowire_id
        lineup_db_entry.outfielder_2 = optimal_lineup["OF"][1][1].rotowire_id
        lineup_db_entry.outfielder_3 = optimal_lineup["OF"][2][1].rotowire_id
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
            predicted_points = pitcher_regression.get_prediction(daily_entry.to_input_vector())
            if predicted_points < 0:
                predicted_points = 0
            daily_entry.predicted_draftkings_points = predicted_points
            database_session.commit()