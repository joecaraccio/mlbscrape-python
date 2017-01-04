
from datetime import date, datetime
from sql.pregame_hitter import PregameHitterGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
from sql.hitter_entry import HitterEntry
from sql.pitcher_entry import PitcherEntry
from sql.lineup_history import LineupHistoryEntry
from sqlalchemy import desc, or_
import heapq
from learn.train_regression import HitterRegressionForestTrainer, PitcherRegressionForestTrainer, HitterRegressionTrainer, PitcherRegressionTrainer
from sql.lineup import LineupEntry
import numpy as np
from email_service import send_email
from sql.mlb_database import MlbDatabase
from draft_kings import CONTEST_SALARY, get_csv_dict
from rotowire import *
from multiprocessing import Pool
from sqlalchemy.exc import IntegrityError
from mine.draft_kings import *


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
        self.position_map = dict()
        self.position_map["C"] = Position("C")
        self.position_map["1B"] = Position("1B")
        self.position_map["2B"] = Position("2B")
        self.position_map["3B"] = Position("3B")
        self.position_map["SS"] = Position("SS")
        self.position_map["SP"] = PositionHeap(OptimalLineupDict.MAX_PITCHERS, "SP")
        self.position_map["OF"] = PositionHeap(OptimalLineupDict.MAX_OUTFIELDERS, "OF")

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

        return self.position_map[position].add(sql_player, CONTEST_SALARY - self.get_total_salary())

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


def get_optimal_lineup(day=None):
    """ Get the optimal lineup of the players to choose for tonight
    :param day: datetime date object
    :return: an OptimalLineupDict structure
    """

    database_session = MlbDatabase().open_session()

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
    while (optimal_lineup.get_total_salary() > CONTEST_SALARY and len(player_heap) > 0) or \
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

    database_session.close()

    return optimal_lineup


def predict_daily_points(day=None):
    database_session = MlbDatabase().open_session()

    if day is None:
        day = date.today()

    hitter_regression = HitterRegressionForestTrainer()
    hitter_regression.train_network()
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

    database_session.close()


def get_avg_hitter_points(player_id, year, database_session=None):
    if database_session is None:
        database_session = MlbDatabase().open_session()

    player_entries = database_session.query(PostgameHitterGameEntry).filter(PostgameHitterGameEntry.rotowire_id ==
                                                                            player_id)
    counter = 0
    total_points = 0
    for entry in player_entries:
        if entry.game_date.split("-")[0] == year:
            counter += 1
            total_points += entry.actual_draftkings_points

    if counter == 0:
        return 0

    return float(total_points) / float(counter)


def get_avg_pitcher_points(player_id, year, database_session=None):
    if database_session is None:
        database_session = MlbDatabase().open_session()

    player_entries = database_session.query(PostgamePitcherGameEntry).filter(PostgamePitcherGameEntry.rotowire_id ==
                                                                            player_id)
    counter = 0
    total_points = 0
    for entry in player_entries:
        if entry.game_date.split("-")[0] == year:
            counter += 1
            total_points += entry.actual_draftkings_points

    if counter == 0:
        return 0

    return float(total_points) / float(counter)


def get_pregame_stats_wrapper(games):
    thread_pool = Pool(6)

    thread_pool.map(get_pregame_stats, games)


def get_pregame_stats(game):
    game_miner = GameMiner(game)
    game_miner.update_ids()
    game_miner.get_pregame_hitting_stats()
    game_miner.get_pregame_pitching_stats()


def mine_pregame_stats():
    """ Mine the hitter/pitcher stats and predict the outcomes and commit to the database session
    """
    games = get_game_lineups()
    get_pregame_stats_wrapper(games)


def prefetch_pregame_stats_atomic(game_matchup):
    """ Lookup the lineup the two teams last used this year and mine the stats
    :param game_matchup:
    :return:
    """
    database_session = MlbDatabase().open_session()
    away_lineup_query = database_session.query(LineupHistoryEntry).get((game_matchup.year, game_matchup.away_team))
    home_lineup_query = database_session.query(LineupHistoryEntry).get((game_matchup.year, game_matchup.home_team))
    away_lineup = list()
    home_lineup = list()
    if away_lineup_query is not None and home_lineup_query is not None:
        hand = away_lineup_query.catcher_entry.batting_hand
        away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.catcher, "C", hand))
        hand = away_lineup_query.first_baseman_entry.batting_hand
        away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.first_baseman, "1B", hand))
        hand = away_lineup_query.second_baseman_entry.batting_hand
        away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.second_baseman, "2B", hand))
        hand = away_lineup_query.third_baseman_entry.batting_hand
        away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.third_baseman, "3B", hand))
        hand = away_lineup_query.shortstop_entry.batting_hand
        away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.shortstop, "SS", hand))
        hand = away_lineup_query.left_fielder_entry.batting_hand
        away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.left_fielder, "LF", hand))
        hand = away_lineup_query.center_fielder_entry.batting_hand
        away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.center_fielder, "CF", hand))
        hand = away_lineup_query.right_fielder_entry.batting_hand
        away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.right_fielder, "RF", hand))

        hand = home_lineup_query.catcher_entry.batting_hand
        home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.catcher, "C", hand))
        hand = home_lineup_query.first_baseman_entry.batting_hand
        home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.first_baseman, "1B", hand))
        hand = home_lineup_query.second_baseman_entry.batting_hand
        home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.second_baseman, "2B", hand))
        hand = home_lineup_query.third_baseman_entry.batting_hand
        home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.third_baseman, "3B", hand))
        hand = home_lineup_query.shortstop_entry.batting_hand
        home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.shortstop, "SS", hand))
        hand = home_lineup_query.left_fielder_entry.batting_hand
        home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.left_fielder, "LF", hand))
        hand = home_lineup_query.center_fielder_entry.batting_hand
        home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.center_fielder, "CF", hand))
        hand = home_lineup_query.right_fielder_entry.batting_hand
        home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.right_fielder, "RF", hand))
        game = Game(away_lineup, game_matchup.away_pitcher, home_lineup, game_matchup.home_pitcher,
                    game_matchup.game_date, game_matchup.game_time)
        get_pregame_stats(game)

    database_session.close()


def prefetch_pregame_stats_wrapper(game_matchups):
    thread_pool = Pool(6)

    thread_pool.map(prefetch_pregame_stats_atomic, game_matchups)


def prefetch_pregame_stats():
    game_matchups = get_game_matchups()
    prefetch_pregame_stats_wrapper(game_matchups)


def update_salaries(csv_dict=None, game_date=None):
    if game_date is None:
        game_date = date.today()
    if csv_dict is None:
        csv_dict = get_csv_dict()

    database_session = MlbDatabase().open_session()
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
            pregame_entry.avg_points = float(csv_entry["AvgPointsPerGame"])
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
            pregame_entry.avg_points = float(csv_entry["AvgPointsPerGame"])
            database_session.commit()
        except KeyError:
            print "Player %s not found in the Draftkings CSV file. Deleting entry." % (pitcher_entry.first_name + " " + pitcher_entry.last_name)
            database_session.delete(pregame_entry)
            database_session.commit()

    database_session.close()


class LineupMiner(object):
    def __init__(self, lineup, opposing_pitcher, db_path=None):
        self._lineup = lineup
        self._opposing_pitcher = opposing_pitcher
        if db_path is None:
            db_path = 'sqlite:////mlb_stats.db'
        else:
            db_path = 'sqlite:///' + db_path
        self._database_session = MlbDatabase(db_path).open_session()

    def __del__(self):
        self._database_session.close()

    def get_pregame_stats(self):
        """ Fetch the pregame hitting stats from the web
        :param game: Game object
        :return:
        """
        pitcher_entry = self._database_session.query(PitcherEntry).get(self._opposing_pitcher.rotowire_id)
        if pitcher_entry is not None:
            pitcher_hand = pitcher_entry.pitching_hand
        else:
            pitcher_hand = None
        for current_hitter in self._lineup:
            pregame_hitter_entry = PregameHitterGameEntry()
            pregame_hitter_entry.rotowire_id = current_hitter.rotowire_id
            pregame_hitter_entry.pitcher_id = self._opposing_pitcher.rotowire_id
            pregame_hitter_entry.team = current_hitter.team
            hitter_entry = self._database_session.query(HitterEntry).get(current_hitter.rotowire_id)
            if hitter_entry is None:
                print "Hitter %s not found" % current_hitter.name
                continue
            print "Mining %s." % current_hitter.name
            hitter_career_soup = get_hitter_page_career_soup(hitter_entry.baseball_reference_id)
            pregame_hitter_entry = self.mine_career_hitting_stats(hitter_entry, pregame_hitter_entry, hitter_career_soup)
            pregame_hitter_entry = self.mine_vs_hand_hitting_stats(hitter_entry, pregame_hitter_entry, hitter_career_soup, pitcher_hand)
            pregame_hitter_entry = self.mine_recent_hitting_stats(hitter_entry, pregame_hitter_entry, hitter_career_soup, pitcher_hand)

            if pitcher_entry is not None:
                pregame_hitter_entry = self.mine_vs_pitcher_hitting_stats(hitter_entry, pregame_hitter_entry, pitcher_entry)
                pregame_hitter_entry.opposing_team = pitcher_entry.team

            pregame_hitter_entry.game_date = date.today()
            try:
                self._database_session.add(pregame_hitter_entry)
                self._database_session.commit()
            except IntegrityError:
                print "Attempt to duplicate hitter entry: %s %s %s" % (current_hitter.name,
                                                                       pregame_hitter_entry.team,
                                                                       pregame_hitter_entry.opposing_team)
                self._database_session.rollback()

    def mine_career_stats(self, hitter_entry, pregame_hitter_entry, hitter_career_soup):
        try:
            career_stats = get_career_hitting_stats(hitter_entry.baseball_reference_id, hitter_career_soup)
            pregame_hitter_entry.career_pa = int(career_stats["PA"])
            pregame_hitter_entry.career_ab = int(career_stats["AB"])
            pregame_hitter_entry.career_r = int(career_stats["R"])
            pregame_hitter_entry.career_h = int(career_stats["H"])
            pregame_hitter_entry.career_hr = int(career_stats["HR"])
            pregame_hitter_entry.career_rbi = int(career_stats["RBI"])
            pregame_hitter_entry.career_sb = int(career_stats["SB"])
            pregame_hitter_entry.career_cs = int(career_stats["CS"])
            pregame_hitter_entry.career_bb = int(career_stats["BB"])
            pregame_hitter_entry.career_so = int(career_stats["SO"])
        #TODO: add ColumnNotFound exception
        except (TableNotFound, TableRowNotFound) as e:
            print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

        return pregame_hitter_entry

    def mine_vs_hand_stats(self, hitter_entry, pregame_hitter_entry, hitter_career_soup, pitcher_hand):
        try:
            vs_hand_stats = get_vs_hand_hitting_stats(hitter_entry.baseball_reference_id, pitcher_hand, hitter_career_soup)
            pregame_hitter_entry.vs_hand_pa = int(vs_hand_stats["PA"])
            pregame_hitter_entry.vs_hand_ab = int(vs_hand_stats["AB"])
            pregame_hitter_entry.vs_hand_r = int(vs_hand_stats["R"])
            pregame_hitter_entry.vs_hand_h = int(vs_hand_stats["H"])
            pregame_hitter_entry.vs_hand_hr = int(vs_hand_stats["HR"])
            pregame_hitter_entry.vs_hand_rbi = int(vs_hand_stats["RBI"])
            pregame_hitter_entry.vs_hand_sb = int(vs_hand_stats["SB"])
            pregame_hitter_entry.vs_hand_cs = int(vs_hand_stats["CS"])
            pregame_hitter_entry.vs_hand_bb = int(vs_hand_stats["BB"])
            pregame_hitter_entry.vs_hand_so = int(vs_hand_stats["SO"])
        except (TableNotFound, TableRowNotFound) as e:
            print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

        return pregame_hitter_entry

    def mine_recent_stats(self, hitter_entry, pregame_hitter_entry, hitter_career_soup):
        try:
            recent_stats = get_recent_hitting_stats(hitter_entry.baseball_reference_id, hitter_career_soup)
            pregame_hitter_entry.recent_pa = int(recent_stats["PA"])
            pregame_hitter_entry.recent_ab = int(recent_stats["AB"])
            pregame_hitter_entry.recent_r = int(recent_stats["R"])
            pregame_hitter_entry.recent_h = int(recent_stats["H"])
            pregame_hitter_entry.recent_hr = int(recent_stats["HR"])
            pregame_hitter_entry.recent_rbi = int(recent_stats["RBI"])
            pregame_hitter_entry.recent_sb = int(recent_stats["SB"])
            pregame_hitter_entry.recent_cs = int(recent_stats["CS"])
            pregame_hitter_entry.recent_bb = int(recent_stats["BB"])
            pregame_hitter_entry.recent_so = int(recent_stats["SO"])
        except (TableNotFound, TableRowNotFound) as e:
            print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

        return pregame_hitter_entry

    def mine_season_stats(self, hitter_entry, pregame_hitter_entry):
        try:
            season_stats = get_season_hitting_stats(hitter_entry.baseball_reference_id)
            pregame_hitter_entry.season_pa = int(season_stats["PA"])
            pregame_hitter_entry.season_ab = int(season_stats["AB"])
            pregame_hitter_entry.season_r = int(season_stats["R"])
            pregame_hitter_entry.season_h = int(season_stats["H"])
            pregame_hitter_entry.season_hr = int(season_stats["HR"])
            pregame_hitter_entry.season_rbi = int(season_stats["RBI"])
            pregame_hitter_entry.season_sb = int(season_stats["SB"])
            pregame_hitter_entry.season_cs = int(season_stats["CS"])
            pregame_hitter_entry.season_bb = int(season_stats["BB"])
            pregame_hitter_entry.season_so = int(season_stats["SO"])
        except (TableNotFound, TableRowNotFound) as e:
            print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

        return pregame_hitter_entry

    def mine_vs_pitcher_stats(self, hitter_entry, pregame_hitter_entry, pitcher_entry):
        try:
            vs_pitcher_stats = get_vs_pitcher_stats(hitter_entry.baseball_reference_id,
                                                                      pitcher_entry.baseball_reference_id)
            pregame_hitter_entry.vs_pa = int(vs_pitcher_stats["PA"])
            pregame_hitter_entry.vs_ab = int(vs_pitcher_stats["AB"])
            pregame_hitter_entry.vs_h = int(vs_pitcher_stats["H"])
            pregame_hitter_entry.vs_hr = int(vs_pitcher_stats["HR"])
            pregame_hitter_entry.vs_rbi = int(vs_pitcher_stats["RBI"])
            pregame_hitter_entry.vs_bb = int(vs_pitcher_stats["BB"])
            pregame_hitter_entry.vs_so = int(vs_pitcher_stats["SO"])
        except (TableNotFound, TableRowNotFound, DidNotFacePitcher) as e:
            print str(e), "with", str(hitter_entry.first_name), str(hitter_entry.last_name)

        return pregame_hitter_entry

    def update_ids(self):
        hitter_soup = get_hitter_soup()
        for current_player in self._lineup:
            db_query = self._database_session.query(HitterEntry).get(current_player.rotowire_id)
            # Found entry, copy the name from the database
            if db_query is not None:
                current_player.name = db_query.first_name + " " + db_query.last_name
                if db_query.team != current_player.team:
                    db_query.team = current_player.team
                    self._database_session.commit()
            # Didn't find entry, create new one
            else:
                current_player.name = get_name_from_id(current_player.rotowire_id)
                try:
                    baseball_reference_id = get_hitter_id(current_player.name,
                                                          team_dict.inv[team_dict[current_player.team]],
                                                          date.today().year,
                                                          hitter_soup)
                except NameNotFound:
                    print "Skipping committing this hitter '%s'." % current_player.name
                    continue

                self.create_new_hitter_entry(current_player, baseball_reference_id)

        self.update_lineup_history()

    def create_new_hitter_entry(self, player_struct, baseball_reference_id):
        name = player_struct.name.split()
        first_name = name[0]
        last_name = " ".join(str(x) for x in name[1:len(name)])
        entry = HitterEntry(first_name, last_name, player_struct.rotowire_id)
        entry.team = player_struct.team
        entry.batting_hand = player_struct.hand
        entry.baseball_reference_id = baseball_reference_id

        self._database_session.add(entry)
        self._database_session.commit()

    def mine_yesterdays_results(self):
        hitter_entries = self._database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == (date.today() - timedelta(days=1)))
        for pregame_hitter_entry in hitter_entries:
            hitter_entry = self._database_session.query(HitterEntry).get(pregame_hitter_entry.rotowire_id)
            try:
                stat_row_dict = get_yesterdays_hitting_game_log(hitter_entry.baseball_reference_id)
            except TableRowNotFound:
                print "Player %s %s did not play yesterday. Deleting pregame entry %s %s" % (hitter_entry.first_name,
                                                                                             hitter_entry.last_name,
                                                                                             pregame_hitter_entry.game_date,
                                                                                             pregame_hitter_entry.opposing_team)
                self._database_session.delete(pregame_hitter_entry)
                self._database_session.commit()
                continue

            # TODO: add a __eq__ method so these chunks are contained within the class
            postgame_hitter_entry = PostgameHitterGameEntry()
            postgame_hitter_entry.rotowire_id = hitter_entry.rotowire_id
            postgame_hitter_entry.game_date = pregame_hitter_entry.game_date
            postgame_hitter_entry.game_h = int(stat_row_dict["H"])
            postgame_hitter_entry.game_bb = int(stat_row_dict["BB"])
            postgame_hitter_entry.game_hbp = int(stat_row_dict["HBP"])
            postgame_hitter_entry.game_r = int(stat_row_dict["R"])
            postgame_hitter_entry.game_sb = int(stat_row_dict["SB"])
            postgame_hitter_entry.game_hr = int(stat_row_dict["HR"])
            postgame_hitter_entry.game_rbi = int(stat_row_dict["RBI"])
            postgame_hitter_entry.game_2b = int(stat_row_dict["2B"])
            postgame_hitter_entry.game_3b = int(stat_row_dict["3B"])
            postgame_hitter_entry.game_1b = postgame_hitter_entry.game_h - postgame_hitter_entry.game_2b - \
                                            postgame_hitter_entry.game_3b - postgame_hitter_entry.game_hr
            postgame_hitter_entry.actual_draftkings_points = get_hitter_points(postgame_hitter_entry)
            try:
                self._database_session.add(postgame_hitter_entry)
                self._database_session.commit()
            except IntegrityError:
                self._database_session.rollback()
                print "Attempt to duplicate hitter postgame results: %s %s %s %s" % (hitter_entry.first_name,
                                                                                     hitter_entry.last_name,
                                                                                     hitter_entry.team,
                                                                                     pregame_hitter_entry.game_date)

    def update_lineup_history(self):
        """ Update the lineup history object for this team and year
        :param lineup: list of PlayerStruct objects
        :param database_session: SQLAlchemy session object
        """
        lineup_history = LineupHistoryEntry()
        lineup_history.team = self._lineup[0].team
        lineup_history.year = date.today().year
        for player in self._lineup:
            if player.position == "C":
                lineup_history.catcher = player.rotowire_id
            elif player.position == "1B":
                lineup_history.first_baseman = player.rotowire_id
            elif player.position == "2B":
                lineup_history.second_baseman = player.rotowire_id
            elif player.position == "3B":
                lineup_history.third_baseman = player.rotowire_id
            elif player.position == "SS":
                lineup_history.shortstop = player.rotowire_id
            elif player.position == "LF":
                lineup_history.left_fielder = player.rotowire_id
            elif player.position == "CF":
                lineup_history.center_fielder = player.rotowire_id
            elif player.position == "RF":
                lineup_history.shortstop = player.rotowire_id

        self._database_session.add(lineup_history)
        self._database_session.commit()

    def correct_prefetched_lineup(self, db_lineup_query):
        for player in self._lineup:
            for game_player in db_lineup_query:
                if game_player.rotowire_id == player.rotowire_id:
                    break
                if game_player == db_lineup_query[db_lineup_query.count()-1]:
                    self._database_session.delete(player)
                    self._database_session.commit()


class PitcherMiner(object):
    def __init__(self, lineup, pitcher, game_date, db_path=None):
        self._lineup = lineup
        self._pitcher = pitcher
        if db_path is None:
            db_path = 'sqlite:////mlb_stats.db'
        else:
            db_path = 'sqlite:///' + db_path
        self._database_session = MlbDatabase(db_path).open_session()
        self._game_date = game_date

    def __del__(self):
        self._database_session.close()

    def get_pregame_stats(self):
        """ Get pregame stats for the given pitcher
        :param pitcher_id: unique Rotowire ID for the corresponing pitcher
        :param team: team abbreviation for the corresponding pitcher
        :param opposing_team: team abbreviation for the team the pitcher is facing
        :param database_session: SQLAlchemy database session
        :param game_date: the date of the game (in the following form yyyy-mm-dd)
        :return: a PregamePitcherGameEntry object without the predicted_draftkings_points field populated
        """
        pregame_pitcher_entry = PregamePitcherGameEntry()
        pregame_pitcher_entry.rotowire_id = self._pitcher.rotowire_id
        pregame_pitcher_entry.team = self._pitcher.team
        pregame_pitcher_entry.opposing_team = self._lineup[0].team
        pregame_pitcher_entry.game_date = self._game_date

        pitcher_entry = self._database_session.query(PitcherEntry).get(self._pitcher.rotowire_id)
        if pitcher_entry is None:
            raise PitcherNotFound(self._pitcher.rotowire_id)

        pitcher_career_soup = get_pitcher_page_career_soup(pitcher_entry.baseball_reference_id)
        pregame_pitcher_entry = self.mine_career_stats(pregame_pitcher_entry, pitcher_entry, pitcher_career_soup)
        pregame_pitcher_entry = self.mine_vs_stats(pregame_pitcher_entry)
        pregame_pitcher_entry = self.mine_recent_stats(pregame_pitcher_entry, pitcher_entry, pitcher_career_soup)
        pregame_pitcher_entry = self.mine_season_stats(pregame_pitcher_entry, pitcher_entry)

        try:
            self._database_session.add(pregame_pitcher_entry)
            self._database_session.commit()
        except IntegrityError:
            print "Attempt to duplicate hitter entry: %s %s %s" % (self._pitcher.name,
                                                                   self._pitcher.rotowire_id.team,
                                                                   pregame_pitcher_entry.opposing_team)
            self._database_session.rollback()

    def mine_career_stats(self, pregame_pitcher_entry, pitcher_entry, pitcher_career_soup):
        try:
            career_stats = get_career_pitching_stats(pitcher_entry.baseball_reference_id, pitcher_career_soup)
            pregame_pitcher_entry.career_bf = int(career_stats["BF"])
            pregame_pitcher_entry.career_ip = float(career_stats["IP"])
            pregame_pitcher_entry.career_h = int(career_stats["H"])
            pregame_pitcher_entry.career_hr = int(career_stats["HR"])
            pregame_pitcher_entry.career_er = int(career_stats["ER"])
            pregame_pitcher_entry.career_bb = int(career_stats["BB"])
            pregame_pitcher_entry.career_so = int(career_stats["SO"])
            pregame_pitcher_entry.career_wins = int(career_stats["W"])
            pregame_pitcher_entry.career_losses = int(career_stats["L"])
        except (TableNotFound, TableRowNotFound) as e:
            print str(e), "with", str(pitcher_entry.first_name), str(pitcher_entry.last_name)

        return pregame_pitcher_entry

    def mine_vs_stats(self, pregame_pitcher_entry):
        opposing_lineup = self._database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == self._game_date,
                                                                                      PregameHitterGameEntry.opposing_team == opposing_team)
        for hitter in opposing_lineup:
            pregame_pitcher_entry.vs_h += hitter.vs_h
            pregame_pitcher_entry.vs_bb += hitter.vs_bb
            pregame_pitcher_entry.vs_so += hitter.vs_so
            pregame_pitcher_entry.vs_hr += hitter.vs_hr
            pregame_pitcher_entry.vs_bf += hitter.vs_pa
            # Approximate earned runs by the RBIs of opposing hitters
            pregame_pitcher_entry.vs_er += hitter.vs_rbi

        return pregame_pitcher_entry

    def mine_recent_stats(self, pregame_pitcher_entry, pitcher_entry, pitcher_career_soup):
        try:
            recent_stats = get_recent_pitcher_stats(pitcher_entry.baseball_reference_id, pitcher_career_soup)
            pregame_pitcher_entry.recent_bf = int(recent_stats["BF"])
            pregame_pitcher_entry.recent_ip = float(recent_stats["IP"])
            pregame_pitcher_entry.recent_h = int(recent_stats["H"])
            pregame_pitcher_entry.recent_hr = int(recent_stats["HR"])
            pregame_pitcher_entry.recent_er = int(recent_stats["ER"])
            pregame_pitcher_entry.recent_bb = int(recent_stats["BB"])
            pregame_pitcher_entry.recent_so = int(recent_stats["SO"])
            pregame_pitcher_entry.recent_wins = int(recent_stats["W"])
            pregame_pitcher_entry.recent_losses = int(recent_stats["L"])
        except (TableNotFound, TableRowNotFound) as e:
            print str(e), "with", str(pitcher_entry.first_name), str(pitcher_entry.last_name)

        return pregame_pitcher_entry

    def mine_season_stats(self, pregame_pitcher_entry, pitcher_entry):
        try:
            season_stats = get_season_pitcher_stats(pitcher_entry.baseball_reference_id)
            pregame_pitcher_entry.season_bf = int(season_stats["BF"])
            pregame_pitcher_entry.season_ip = float(season_stats["IP"])
            pregame_pitcher_entry.season_h = int(season_stats["H"])
            pregame_pitcher_entry.season_hr = int(season_stats["HR"])
            pregame_pitcher_entry.season_er = int(season_stats["ER"])
            pregame_pitcher_entry.season_bb = int(season_stats["BB"])
            pregame_pitcher_entry.season_so = int(season_stats["SO"])
            pregame_pitcher_entry.season_wins = int(season_stats["W"])
            pregame_pitcher_entry.season_losses = int(season_stats["L"])
        except (TableNotFound, TableRowNotFound) as e:
            print str(e), "with", str(pitcher_entry.first_name), str(pitcher_entry.last_name)

        return pregame_pitcher_entry

    def update_id(self):
        pitcher_soup = get_pitcher_soup()
        db_query = self._database_session.query(PitcherEntry).get(self._pitcher.rotowire_id)
        # Found unique entry, check to make sure the team matches the database
        if db_query is not None:
            self._pitcher.name = db_query.first_name + " " + db_query.last_name
            if self._pitcher.team != db_query.team:
                db_query.team = self._pitcher.team
                self._database_session.commit()
        # Found no entries, create a bare bones entry with just the name and id
        else:
            self._pitcher.name = get_name_from_id(self._pitcher.rotowire_id)
            try:
                baseball_reference_id = get_pitcher_id(self._pitcher.name,
                                                       team_dict.inv[team_dict[self._pitcher.team]],
                                                       date.today().year,
                                                       pitcher_soup)
            except NameNotFound:
                print "Skipping committing this pitcher '%s'." % self._pitcher.name
                return

            self.create_new_pitcher_entry(baseball_reference_id)

    def create_new_pitcher_entry(self, baseball_reference_id):
        name = self._pitcher.name.split()
        first_name = name[0]
        last_name = " ".join(str(x) for x in name[1:len(name)])
        entry = PitcherEntry(first_name, last_name, self._pitcher.rotowire_id)
        entry.team = self._pitcher.team
        entry.pitching_hand = self._pitcher.hand
        entry.baseball_reference_id = baseball_reference_id

        self._database_session.add(entry)
        self._database_session.commit()

    def mine_yesterdays_results(self):
        pitcher_entries = self._database_session.query(PregamePitcherGameEntry).filter(PregamePitcherGameEntry.game_date == (date.today() - timedelta(days=1)))
        for pregame_pitcher_entry in pitcher_entries:
            pitcher_entry = self._database_session.query(PitcherEntry).get(pregame_pitcher_entry.rotowire_id)
            print "Mining yesterday for %s %s" % (pitcher_entry.first_name, pitcher_entry.last_name)
            try:
                stat_row_dict = get_pitching_game_log(pitcher_entry.baseball_reference_id)
            except TableRowNotFound:
                print "Player %s %s did not play yesterday. Deleting pregame entry %s %s" % \
                      (pitcher_entry.first_name,
                       pitcher_entry.last_name,
                       pregame_pitcher_entry.game_date,
                       pregame_pitcher_entry.opposing_team)

                self._database_session.delete(pregame_pitcher_entry)
                self._database_session.commit()
                continue

            postgame_pitcher_entry = PostgamePitcherGameEntry()
            postgame_pitcher_entry.rotowire_id = pitcher_entry.rotowire_id
            postgame_pitcher_entry.game_date = pregame_pitcher_entry.game_date
            postgame_pitcher_entry.game_ip = float(stat_row_dict["IP"])
            postgame_pitcher_entry.game_so = int(stat_row_dict["SO"])
            if str(stat_row_dict["Dec"])[0] == "W":
                postgame_pitcher_entry.game_wins = 1
            postgame_pitcher_entry.game_er = int(stat_row_dict["ER"])
            postgame_pitcher_entry.game_er = int(stat_row_dict["ER"])
            postgame_pitcher_entry.game_h = int(stat_row_dict["H"])
            postgame_pitcher_entry.game_bb = int(stat_row_dict["BB"])
            postgame_pitcher_entry.game_hbp = int(stat_row_dict["HBP"])
            if stat_row_dict["Inngs"] == "CG":
                postgame_pitcher_entry.game_cg = 1
            if stat_row_dict["Inngs"] == "SHO":
                postgame_pitcher_entry.game_cgso = 1
            if postgame_pitcher_entry.game_cg == 1 and postgame_pitcher_entry.game_h == 0:
                postgame_pitcher_entry.game_no_hitter = 1
            postgame_pitcher_entry.actual_draftkings_points = get_pitcher_points(postgame_pitcher_entry)
            try:
                self._database_session.add(postgame_pitcher_entry)
                self._database_session.commit()
            except IntegrityError:
                self._database_session.rollback()
                print "Attempt to duplicate pitcher postgame results: %s %s %s %s" % (pitcher_entry.first_name,
                                                                                      pitcher_entry.last_name,
                                                                                      pregame_pitcher_entry.opposing_team,
                                                                                      postgame_pitcher_entry.game_date)


class GameMiner(object):
    def __init__(self, game, db_path=None):
        if db_path is None:
            db_path = 'sqlite:////mlb_stats.db'
        else:
            db_path = 'sqlite:///' + db_path

        self._database_session = MlbDatabase(db_path).open_session()
        self._game = game
        self._home_lineup_miner = LineupMiner(game.home_lineup, game.away_pitcher, db_path)
        self._home_pitcher_miner = PitcherMiner(game.away_lineup, game.home_pitcher, game.game_date, db_path)
        self._away_lineup_miner = LineupMiner(game.away_lineup, game.home_pitcher, db_path)
        self._away_pitcher_miner = PitcherMiner(game.home_lineup, game.away_pitcher, game.game_date, db_path)

    def __del__(self):
        self._database_session.close()

    def update_ids(self):
        """ Check if each player is represented in the database. If not, commit a new entry
        :param games: list of Game objects
        """
        self._away_lineup_miner.update_ids()
        self._away_pitcher_miner.update_ids()
        self._home_lineup_miner.update_ids()
        self._home_pitcher_miner.update_ids()

    def get_pregame_hitting_stats(self):
        away_lineup = self._database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.team == self._game.away_pitcher.team,
                                                                                  PregameHitterGameEntry.game_date == self._game.game_date,
                                                                                  PregameHitterGameEntry.game_time == self._game.game_time)
        self._away_lineup_miner.correct_prefetched_lineup(away_lineup)
        home_lineup = self._database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.team == self._game.home_pitcher.team,
                                                                                  PregameHitterGameEntry.game_date == self._game.game_date,
                                                                                  PregameHitterGameEntry.game_time == self._game.game_time)
        self._home_lineup_miner.correct_prefetched_lineup(home_lineup)
        self._away_lineup_miner.get_pregame_stats()
        self._home_lineup_miner.get_pregame_stats()

    def get_pregame_pitching_stats(self):
        home_pitcher = self._database_session.query(PregamePitcherGameEntry).filter(PregameHitterGameEntry.team == self._game.home_pitcher.team,
                                                                                  PregameHitterGameEntry.game_date == self._game.game_date,
                                                                                  PregameHitterGameEntry.game_time == self._game.game_time)[0]
        if home_pitcher.rotowire_id != self._game.home_pitcher.rotowire_id:
            self._database_session.delete(home_pitcher)
            self._database_session.commit()
        self._home_pitcher_miner.get_pregame_stats()
        away_pitcher = self._database_session.query(PregamePitcherGameEntry).get((self._game.away_pitcher.rotowire_id,
                                                                                  self._game.game_date,
                                                                                  self._game.game_time))
        if away_pitcher.rotowire_id != self._game.away_pitcher.rotowire_id:
            self._database_session.delete(away_pitcher)
            self._database_session.commit()
        self._away_pitcher_miner.get_pregame_stats()