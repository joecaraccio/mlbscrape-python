
from datetime import date, datetime
from sql.pregame_hitter import PregameHitterGameEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
from sql.hitter_entry import HitterEntry
from sql.pitcher_entry import PitcherEntry
from sql.lineup_history import LineupHistoryEntry
from sql.game import GameEntry
from sql.team_park import ParkEntry
from sqlalchemy import or_
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
from sql.umpire import UmpireCareerEntry
from mine.baseball_reference import PlayerNameNotFound
import math
from mine.team_dict import *
from mine.baseball_reference import *

class NoGamesFound(Exception):
    def __init__(self):
        super(NoGamesFound, self).__init__("No games found.")


class Player(object):
    """ Wrapper class for PregameHitterGameEntry/PregamePitcherGameEntry objects
    """

    def __init__(self, position_string, sql_player):
        self._salary = 0
        self._player = sql_player
        self._position_string = position_string

    def get_salary(self):
        return self._player.draftkings_salary

    def __str__(self):
        return "%s: %s\n" % (self._position_string, str(self._player))

    def get_team(self):
        return self._player.get_team()

    def get_opposing_team(self):
        return self._player.get_opposing_team()

    def get_points(self):
        return self._player.predicted_draftkings_points

    def get_points_per_dollar(self):
        return self._player.points_per_dollar()

    def get_id(self):
        return self._player.rotowire_id


class PositionHeap(object):
    """ Class for managing the addition/removal of players from a position
    """

    def __init__(self, max_players, position_string):
        """ Constructor
        :param max_players: maximum number of players at this position
        :param position_string: a str() representing the position abbreviation
        """
        self._max_players = max_players
        self._position_string = position_string
        self._position_heap = list()
        self._blacklisted_opposing_team = None

    def add(self, sql_player, maximum_salary):
        """ Add a player to the position heap
        Only add the player if they are not facing a blacklisted team and the position is open or the player
        is a better value than the existing player.
        :param sql_player: SQLAlchemy PregameHitterGameEntry or PregamePitcherGameEntry
        :param maximum_salary: the salary available for the meta object
        :return True if the player was added, False otherwise
        """
        is_added = False
        if self._blacklisted_opposing_team is not None:
            if self._blacklisted_opposing_team == sql_player.get_opposing_team():
                return is_added

        if sql_player.draftkings_salary == 0:
            return is_added

        if len(self._position_heap) < self._max_players:
            if sql_player.draftkings_salary <= maximum_salary:
                player_entry = Player(self._position_string, sql_player)
                heapq.heappush(self._position_heap, (sql_player.predicted_draftkings_points, player_entry))
                is_added = True
        else:
            temp_heap = list()
            while len(self._position_heap) > 0:
                player_entry = heapq.heappop(self._position_heap)[1]
                # Player was already added, just add the remaining players
                if is_added:
                    heapq.heappush(temp_heap, (player_entry.get_points(), player_entry))
                else:
                    try:
                        if player_entry.get_points_per_dollar() < sql_player.points_per_dollar():
                            if sql_player.draftkings_salary <= maximum_salary + player_entry.get_salary():
                                new_player = Player(self._position_string, sql_player)
                                heapq.heappush(temp_heap, (new_player.get_points(), new_player))
                                is_added = True
                        # Candidate player is not better than this player, just add the original player
                        else:
                            heapq.heappush(temp_heap, (player_entry.get_points(), player_entry))
                    except ZeroDivisionError:
                        heapq.heappush(temp_heap, (player_entry.get_points(), player_entry))

            self._position_heap = temp_heap

        return is_added

    def remove(self, rotowire_id):
        """ Remove the player with the given RotoWire ID from the heap
        :param rotowire_id: Rotowire ID of the player to remove
        """
        idx = 0
        for player in self._position_heap:
            if player[1].get_id() == rotowire_id:
                self._position_heap.pop(idx)
                heapq.heapify(self._position_heap)
                break
            else:
                idx += 1

    def get_player(self, idx):
        if idx >= len(self._position_heap):
            return None
        else:
            return self._position_heap[idx][1]

    def remove_opposing_team(self, opposing_team):
        """ Remove all the players at this position facing the given team
        :param opposing_team: the opposing team of players to remove
        :return: True if there was a player at this position removed, False otherwise
        """
        is_removed = False
        self._blacklisted_opposing_team = opposing_team
        idx = 0
        for player in self._position_heap:
            if player[1].get_opposing_team() == opposing_team:
                print "Blacklisting team %s" % opposing_team
                self._position_heap.pop(idx)
                is_removed = True
            else:
                idx += 1

        return is_removed

    def get_total_salary(self):
        """ Get the total salary for this position heap
        :return: total salary in dollars
        """
        return sum(player[1].get_salary() for player in self._position_heap)

    def is_open(self):
        """ See if there is room left at this position
        :return: True if there is room left at this position, False otherwise
        """
        return len(self._position_heap) < self._max_players

    def get_worst_player_points(self):
        """ Get the player with the least amount of projected points
        :return: Player object with the least amount of projected points
        """
        points = 0.0
        try:
            points = self._position_heap[0][0]
        except IndexError:
            pass

        return points

    def is_player_assigned(self, sql_player):
        """ Check if the given player is already on the heap
        :param sql_player: SQLAlchemy HitterPregameGameEntry or PitcherPregameGameEntry object
        :return: True if the given player is already on the heap, False otherwise
        """
        for player in self._position_heap:
            if player[1]._player == sql_player:
                return True

        return False

    def __str__(self):
        ret_str = str()
        for player in self._position_heap:
            ret_str += "%s: %s\n" % (self._position_string, player[1])
        return ret_str

    def is_valid(self):
        """ Check to see if the position is full with players
        :return: True if the position is full with players, False otherwise
        """
        return len(self._position_heap) == self._max_players

    def get_teams(self):
        """ Get string representations of the team abbreviation of the players at this position
        :return: list of team abbreviations
        """
        team_list = list()
        for player in self._position_heap:
            team_list.append(player[1].get_team())

        return team_list

    def get_opposing_teams(self):
        """ Get string representations of the opposing team abbreviation of the players at this position
        :return: list of opposing team abbreviations
        """
        team_list = list()
        for player in self._position_heap:
            team_list.append(player[1].get_opposing_team())

        return team_list

    def get_team_points(self, team):
        """ Get the total amount of points the given team is predicted to score at this position
        :param team: team abbreviation
        :return: Total amount of points
        """
        points = 0.0
        for player in self._position_heap:
            if player[1].get_team() == team:
                points += player[1].get_points()

        return points

    def get_ids(self):
        """ Get the RotoWire IDs of the players at this position
        :return: list of RotoWire IDs
        """
        return [player[1].get_id() for player in self._position_heap]


class OptimalLineupDict(dict):
    """ Class for managing the optimal lineup for a given day
    """
    # The maximum number of pitchers and outfielders allowed in a lineup
    MAX_PITCHERS = 2
    MAX_OUTFIELDERS = 3

    FieldingPositions = ["C", "1B", "2B", "3B", "SS", "OF"]
    PitchingPositions = ["SP"]
    PositionList = FieldingPositions + PitchingPositions

    def __init__(self):
        """ Constructor used to initialize the total salary and the heaps
        """
        super(OptimalLineupDict, self).__init__()
        self.position_map = dict()
        self.position_map["C"] = PositionHeap(1, "C")
        self.position_map["1B"] = PositionHeap(1, "1B")
        self.position_map["2B"] = PositionHeap(1, "2B")
        self.position_map["3B"] = PositionHeap(1, "3B")
        self.position_map["SS"] = PositionHeap(1, "SS")
        self.position_map["SP"] = PositionHeap(OptimalLineupDict.MAX_PITCHERS, "SP")
        self.position_map["OF"] = PositionHeap(OptimalLineupDict.MAX_OUTFIELDERS, "OF")

    def get_total_salary(self):
        """ Get the current salary of this lineup
        :return: int the current salary for this team
        """
        return sum(self.position_map[position].get_total_salary() for position in OptimalLineupDict.PositionList)

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
        for position in OptimalLineupDict.PositionList:
            if self.position_map[position].is_player_assigned(sql_player):
                return True

        return False

    def __str__(self):
        ret_str = str()
        for position in OptimalLineupDict.PositionList:
            try:
                ret_str += str(self.position_map[position])
            except IndexError:
                continue

        ret_str += "Total salary: %s" % self.get_total_salary()

        return ret_str

    def is_valid(self):
        for position in OptimalLineupDict.PositionList:
            if not self.position_map[position].is_valid():
                return False

        return True

    def get_worst_position(self):
        """ Get the position with the player with the least predicted points
        :return: the string of the worst position
        """
        worst_point_value = self.position_map["C"].get_worst_player_points()
        position = str()
        for position in OptimalLineupDict.PositionList:
            if self.position_map[position].get_worst_player_points() <= worst_point_value:
                worst_point_value = self.position_map[position].get_worst_player_points()

        return position

    def get_opposing_team_points_dict(self):
        """ Get a dictionary of the hitter opposing teams and how many points they are predicted to score
        :return: dictionary of the hitter opposing teams and how many points they are predicted to score
        """
        team_points_dict = dict()
        for fielding_position in OptimalLineupDict.FieldingPositions:
            position = self.position_map[fielding_position]
            teams = position.get_opposing_teams()
            for team in teams:
                try:
                    team_points_dict[team] = team_points_dict[team] + position.get_team_points(team)
                except KeyError:
                    team_points_dict[team] = position.get_team_points(team)

        return team_points_dict

    def remove_opposing_hitters(self, opposing_team):
        """ Remove the hitters facing the given team
        :param opposing_team: team abbreviation
        """
        for fielding_position in OptimalLineupDict.FieldingPositions:
            self.position_map[fielding_position].remove_opposing_team(opposing_team)

    def delete_bad_opponents(self):
        """ Group hitters together and determine if the sum of their predicted points is greater than the
        opposing pitcher. If so, then delete the pitcher so we can pick a different one. If not, then delete the
        hitters so we can pick different ones.
        """
        team_points_dict = self.get_opposing_team_points_dict()

        pitcher_heap = self.position_map["SP"]
        for pitcher in pitcher_heap._position_heap:
            try:
                # Hitters are projected to do better, delete the pitcher
                if pitcher[1].get_points() < team_points_dict[pitcher[1].get_team()]:
                    pitcher[1].remove_opposing_team(pitcher[1].get_opposing_team())
                # Pitchers are projected to do better, delete the hitters
                else:
                    self.remove_opposing_hitters(pitcher[1].get_team())

            # Pitcher is not facing any of the hitters, move on
            except KeyError:
                continue


def get_optimal_lineup(day=None):
    """ Get the optimal lineup of the players to choose for tonight
    :param day: datetime date object
    :return: an OptimalLineupDict structure
    """

    database_session = MlbDatabase().open_session()

    if day is None:
        day = datetime.now()
        day.replace(hour=23, minute=0, second=0)
    optimal_lineup = OptimalLineupDict()
    player_heap = dict()

    # Look for the hitter entries
    for fielding_position in OptimalLineupDict.FieldingPositions:
        query_results = PregameHitterGameEntry.get_daily_entries_by_position(database_session, fielding_position, day)
        query_result_heap = list()
        for query_result in query_results:
            heapq.heappush(query_result_heap, (-query_result.predicted_draftkings_points, query_result))
        # TODO: revive this when we successfully split up the original heap and the heap used for the optimal lineup
        """while not optimal_lineup.position_map[fielding_position].is_valid() and len(query_results) > 0:
            try:
                candidate_player = heapq.heappop(query_result_heap)[1]
                optimal_lineup.add(candidate_player)
            except IndexError:
                continue
        """
        player_heap[fielding_position] = list()
        while len(query_result_heap) > 0:
            player = heapq.heappop(query_result_heap)
            heapq.heappush(player_heap[fielding_position], player)

    # Look for pitchers
    query_results = PregamePitcherGameEntry.get_all_daily_entries(database_session, day)
    for query_result in query_results:
        heapq.heappush(query_result_heap, (-query_result.predicted_draftkings_points, query_result))
    # TODO: revive this when we successfully split up the original heap and the heap used for the optimal lineup
    """while not optimal_lineup.position_map["SP"].is_valid() and len(query_result_heap) > 0:
        print len(query_results), optimal_lineup.position_map["SP"].is_valid()
        try:
            candidate_player = heapq.heappop(query_result_heap)[1]
            optimal_lineup.add(candidate_player)
        except IndexError:
            continue
    """
    player_heap["SP"] = list()
    while len(query_result_heap) > 0:
        player = heapq.heappop(query_result_heap)
        heapq.heappush(player_heap["SP"], player)

    player_heap_copy = player_heap

    # Print out all the remaining players in order of their value
    player_text = "Fantasy Baseball Predictions\n"
    for fielding_position in OptimalLineupDict.FieldingPositions:
        player_text += fielding_position + "\n"
        while len(player_heap_copy[fielding_position]) > 0:
            player = heapq.heappop(player_heap_copy[fielding_position])
            player_text += "%s\n" % str(player[1])
        player_text += "\n"

    player_text += "SP\n"
    while len(player_heap_copy["SP"]) > 0:
        player = heapq.heappop(player_heap_copy["SP"])
        player_text += "%s\n" % str(player[1])

    send_email(player_text)
    print player_text

    # Replace players one by one who are "overpaid" based on predicted points per dollar
    """while (optimal_lineup.get_total_salary() > CONTEST_SALARY and len(player_heap) > 0) or \
            not optimal_lineup.is_valid():
        worst_position = optimal_lineup.get_worst_position()
        try:
            next_player = heapq.heappop(player_heap[worst_position])[1]
            optimal_lineup.add(next_player)
        except IndexError:
            continue

    # Delete the players facing one another who are predicted to do worse, blacklist that team at that position
    optimal_lineup.delete_bad_opponents()

    # Add players in the same manner, but with the blacklisted team enforced
    while (optimal_lineup.get_total_salary() > CONTEST_SALARY and len(player_heap_copy) > 0) or \
            not optimal_lineup.is_valid():
        worst_position = optimal_lineup.get_worst_position()
        print len(player_heap_copy), worst_position, player_heap_copy[worst_position]
        next_player = heapq.heappop(player_heap_copy[worst_position])[1]
        optimal_lineup.add(next_player)
    """

    # Commit the prediction to the database
    """lineup_db_entry = LineupEntry()
    lineup_db_entry.game_date = str(date.today())
    lineup_db_entry.game_time = datetime.now().strftime("%H:%M:%S")
    lineup_db_entry.starting_pitcher_1 = optimal_lineup.position_map["SP"].get_player(0).get_id()
    lineup_db_entry.starting_pitcher_2 = optimal_lineup.position_map["SP"].get_player(1).get_id()
    lineup_db_entry.catcher = optimal_lineup.position_map["C"].get_player(0).get_id()
    lineup_db_entry.first_baseman = optimal_lineup.position_map["1B"].get_player(0).get_id()
    lineup_db_entry.second_baseman = optimal_lineup.position_map["2B"].get_player(0).get_id()
    lineup_db_entry.third_baseman = optimal_lineup.position_map["3B"].get_player(0).get_id()
    lineup_db_entry.shortstop = optimal_lineup.position_map["SS"].get_player(0).get_id()
    lineup_db_entry.outfielder_1 = optimal_lineup.position_map["OF"].get_player(0).get_id()
    lineup_db_entry.outfielder_2 = optimal_lineup.position_map["OF"].get_player(1).get_id()
    lineup_db_entry.outfielder_3 = optimal_lineup.position_map["OF"].get_player(2).get_id()
    database_session.add(lineup_db_entry)
    database_session.commit()
"""
    print optimal_lineup
    send_email(optimal_lineup.__str__())

    database_session.close()

    return optimal_lineup


def predict_daily_points(day=None):
    database_session = MlbDatabase().open_session()

    if day is None:
        day = datetime.now()
        day = day.replace(hour=23, minute=0, second=0)

    hitter_regression = HitterRegressionForestTrainer()
    hitter_regression.train_network()
    pitcher_regression = PitcherRegressionForestTrainer()
    pitcher_regression.train_network()
    daily_entries = PregameHitterGameEntry.get_all_daily_entries(database_session, day)
    for daily_entry in daily_entries:
        if daily_entry.game_entry is None:
            print "NoneType game entry for %s %s %s %s" % (daily_entry.rotowire_id, daily_entry.home_team,
                                                           daily_entry.game_date, daily_entry.game_time)
            continue

        if daily_entry.game_entry.umpire is None:
            umpire_vector = UmpireCareerEntry.get_nominal_data(database_session)
        else:
            ump_entry = database_session.query(UmpireCareerEntry).get(daily_entry.game_entry.umpire)

            if ump_entry is None:
                umpire_vector = UmpireCareerEntry.get_nominal_data(database_session)
            else:
                umpire_vector = ump_entry.to_input_vector()

        game_datetime = datetime.strptime(daily_entry.game_date, "%Y-%m-%d")
        park_factors = database_session.query(ParkEntry).get((daily_entry.home_team, str(game_datetime.year-1)))
        if park_factors is None:
            print "PredictDailyPoints1: Could not find %s from %i" % (daily_entry.home_team, game_datetime.year-1)
            park_vector = np.array([100, 100])
        else:
            park_vector = park_factors.to_input_vector()

        final_pitcher_array = np.concatenate([daily_entry.to_input_vector(), park_vector, umpire_vector])
        predicted_points = hitter_regression.get_prediction(final_pitcher_array)
        std_dev = hitter_regression.get_std_dev(final_pitcher_array)
        print "Std dev for %s %s is %f" % (daily_entry.hitter_entry.first_name, daily_entry.hitter_entry.last_name, std_dev)

        if predicted_points < 0:
            predicted_points = 0
        daily_entry.predicted_draftkings_points = predicted_points
        database_session.commit()

    daily_entries = PregamePitcherGameEntry.get_all_daily_entries(database_session, day)
    for daily_entry in daily_entries:
        input_vector = daily_entry.to_input_vector()

        if daily_entry.game_entry is None:
            print "NoneType game entry for %s %s %s %s" % (daily_entry.rotowire_id, daily_entry.home_team,
                                                           daily_entry.game_date, daily_entry.game_time)
            continue

        if daily_entry.game_entry.umpire is None:
            umpire_vector = UmpireCareerEntry.get_nominal_data(database_session)
        else:
            ump_entry = database_session.query(UmpireCareerEntry).get(daily_entry.game_entry.umpire)

            if ump_entry is None:
                umpire_vector = UmpireCareerEntry.get_nominal_data(database_session)
            else:
                umpire_vector = ump_entry.to_input_vector()

        game_datetime = datetime.strptime(daily_entry.game_date, "%Y-%m-%d")
        park_factors = database_session.query(ParkEntry).get((daily_entry.home_team, game_datetime.year-1))
        if park_factors is None:
            print "PredictDailyPoints2: Could not find %s from %i" % (daily_entry.home_team, str(game_datetime.year-1))
            park_vector = np.array([100, 100])
        else:
            park_vector = park_factors.to_input_vector()

        final_pitcher_array = np.concatenate([input_vector, daily_entry.get_opponent_vector(), park_vector, umpire_vector])
        predicted_points = pitcher_regression.get_prediction(final_pitcher_array)
        std_dev = pitcher_regression.get_std_dev(final_pitcher_array)
        print "Std dev for %s %s is %f" % (daily_entry.pitcher_entry.first_name, daily_entry.pitcher_entry.last_name, std_dev)
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
    #for game in games:
    #    get_pregame_stats(game)


def get_pregame_stats(game):
    game_miner = GameMiner(game)
    game_miner.update_ids()
    game_miner.update_park_factors()
    game_miner.get_pregame_hitting_stats()
    game_miner.get_pregame_pitching_stats()


def mine_pregame_stats():
    """ Mine the hitter/pitcher stats and predict the outcomes and commit to the database session
    """
    games = get_game_lineups()
    if len(games) == 0:
        raise NoGamesFound
    get_pregame_stats_wrapper(games)


def prefetch_pregame_stats_atomic(game_matchup):
    """ Lookup the lineup the two teams last used this year and mine the stats
    :param game_matchup:
    :return:
    """
    database_session = MlbDatabase().open_session()
    game_date = datetime.strptime(game_matchup.game_date, '%Y-%M-%d')
    away_lineup_query = database_session.query(LineupHistoryEntry).get((game_date.year, game_matchup.away_team))
    home_lineup_query = database_session.query(LineupHistoryEntry).get((game_date.year, game_matchup.home_team))
    away_lineup = list()
    home_lineup = list()
    if away_lineup_query is not None and home_lineup_query is not None:
        try:
            hand = away_lineup_query.catcher_entry.batting_hand
            away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.catcher, "C", hand))
        except AttributeError:
            pass
        try:
            hand = away_lineup_query.first_baseman_entry.batting_hand
            away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.first_baseman, "1B", hand))
        except AttributeError:
            pass
        try:
            hand = away_lineup_query.second_baseman_entry.batting_hand
            away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.second_baseman, "2B", hand))
        except AttributeError:
            pass
        try:
            hand = away_lineup_query.third_baseman_entry.batting_hand
            away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.third_baseman, "3B", hand))
        except AttributeError:
            pass
        try:
            hand = away_lineup_query.shortstop_entry.batting_hand
            away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.shortstop, "SS", hand))
        except AttributeError:
            pass
        try:
            hand = away_lineup_query.left_fielder_entry.batting_hand
            away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.left_fielder, "LF", hand))
        except AttributeError:
            pass
        try:
            hand = away_lineup_query.center_fielder_entry.batting_hand
            away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.center_fielder, "CF", hand))
        except AttributeError:
            pass
        try:
            hand = away_lineup_query.right_fielder_entry.batting_hand
            away_lineup.append(PlayerStruct(game_matchup.away_team, away_lineup_query.right_fielder, "RF", hand))
        except AttributeError:
            pass

        try:
            hand = home_lineup_query.catcher_entry.batting_hand
            home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.catcher, "C", hand))
        except AttributeError:
            pass
        try:
            hand = home_lineup_query.first_baseman_entry.batting_hand
            home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.first_baseman, "1B", hand))
        except AttributeError:
            pass
        try:
            hand = home_lineup_query.second_baseman_entry.batting_hand
            home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.second_baseman, "2B", hand))
        except AttributeError:
            pass
        try:
            hand = home_lineup_query.third_baseman_entry.batting_hand
            home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.third_baseman, "3B", hand))
        except AttributeError:
            pass
        try:
            hand = home_lineup_query.shortstop_entry.batting_hand
            home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.shortstop, "SS", hand))
        except AttributeError:
            pass
        try:
            hand = home_lineup_query.left_fielder_entry.batting_hand
            home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.left_fielder, "LF", hand))
        except AttributeError:
            pass
        try:
            hand = home_lineup_query.center_fielder_entry.batting_hand
            home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.center_fielder, "CF", hand))
        except AttributeError:
            pass
        try:
            hand = home_lineup_query.right_fielder_entry.batting_hand
            home_lineup.append(PlayerStruct(game_matchup.home_team, home_lineup_query.right_fielder, "RF", hand))
        except AttributeError:
            pass
        game = Game(away_lineup, game_matchup.away_pitcher, home_lineup, game_matchup.home_pitcher,
                    game_matchup.game_date, game_matchup.game_time)
        get_pregame_stats(game)

    database_session.close()


def add_game_entries(game_matchups):
    """ Add the bare minimum game info to the database.
    The weather and umpire data will be resolved when the prefetch data is resolved (i.e. right before gametime)
    :param game_matchups: GameMatchup objects
    """
    database_session = MlbDatabase().open_session()
    for game_matchup in game_matchups:
        game_entry = GameEntry(game_matchup.game_date, game_matchup.game_time, game_matchup.home_team,
                               game_matchup.away_team)
        try:
            database_session.add(game_entry)
            database_session.commit()
        except IntegrityError:
            database_session.rollback()


def prefetch_pregame_stats_wrapper(game_matchups):
    thread_pool = Pool(6)
    thread_pool.map(prefetch_pregame_stats_atomic, game_matchups)
    #for game_matchup in game_matchups:
    #    prefetch_pregame_stats_atomic(game_matchup)

def prefetch_pregame_stats():
    game_matchups = get_game_matchups()
    if len(game_matchups) == 0:
        raise NoGamesFound
    add_game_entries(game_matchups)
    prefetch_pregame_stats_wrapper(game_matchups)


def update_salaries(csv_dict=None, game_date=None):
    if game_date is None:
        game_date = datetime.now()
        game_date = game_date.replace(hour=23, minute=0, second=0)
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
            print "Player %s not found in the Draftkings CSV file." % pregame_entry.rotowire_id
        try:
            csv_entry = csv_dict[(hitter_entry.first_name + " " + hitter_entry.last_name + hitter_entry.team).lower()]
            pregame_entry.draftkings_salary = int(csv_entry["Salary"])
            positions = csv_entry["Position"].split("/")
            pregame_entry.primary_position = positions[0]
            pregame_entry.secondary_position = positions[len(positions) - 1]
            pregame_entry.avg_points = float(csv_entry["AvgPointsPerGame"])
            database_session.commit()
        except KeyError:
            print "Player %s not found in the Draftkings CSV file." % (hitter_entry.first_name + " " + hitter_entry.last_name)

    # Pitchers
    pregame_pitchers = PregamePitcherGameEntry.get_all_daily_entries(database_session, game_date)
    for pregame_entry in pregame_pitchers:
        # Lookup the player's name in the database
        # Lookup the name in the dictionary
        pitcher_entry = database_session.query(PitcherEntry).get(pregame_entry.rotowire_id)
        if pitcher_entry is None:
            print "Player %s not found in the Draftkings CSV file." % pregame_entry.rotowire_id
        try:
            csv_entry = csv_dict[(pitcher_entry.first_name + " " + pitcher_entry.last_name + pitcher_entry.team).lower()]
            pregame_entry.draftkings_salary = int(csv_entry["Salary"])
            pregame_entry.avg_points = float(csv_entry["AvgPointsPerGame"])
            database_session.commit()
        except KeyError:
            print "Player %s not found in the Draftkings CSV file." % (pitcher_entry.first_name + " " + pitcher_entry.last_name)

    database_session.close()


class LineupMiner(object):
    def __init__(self, lineup, opposing_pitcher, game_date, game_time, is_home, db_path=None):
        self._lineup = lineup
        self._opposing_pitcher = opposing_pitcher
        self._database_session = MlbDatabase(db_path).open_session()
        self._game_date = game_date
        self._game_time = game_time
        self._is_home = is_home

    def __del__(self):
        self._database_session.close()

    def get_pregame_stats(self):
        """ Fetch the pregame hitting stats from the web
        :return:
        """
        pitcher_entry = self._database_session.query(PitcherEntry).get(self._opposing_pitcher.rotowire_id)
        if pitcher_entry is not None:
            pitcher_hand = pitcher_entry.pitching_hand
        else:
            pitcher_hand = None
        for current_hitter in self._lineup:
            home_team = self._opposing_pitcher.team
            if self._is_home:
                home_team = self._lineup[0].team

            db_hitter = self._database_session.query(PregameHitterGameEntry).get((current_hitter.rotowire_id,
                                                                                  self._game_date,
                                                                                  self._game_time))
            if db_hitter is not None:
                print "'%s' has already been mined today." % current_hitter.rotowire_id
                continue
            pregame_hitter_entry = PregameHitterGameEntry()
            pregame_hitter_entry.rotowire_id = current_hitter.rotowire_id
            pregame_hitter_entry.pitcher_id = self._opposing_pitcher.rotowire_id
            pregame_hitter_entry.is_home_team = self._is_home
            pregame_hitter_entry.home_team = home_team
            hitter_entry = self._database_session.query(HitterEntry).get(current_hitter.rotowire_id)
            if hitter_entry is None:
                print "Hitter %s not found" % current_hitter.name
                continue
            print "Mining %s." % current_hitter.name
            hitter_career_soup = get_hitter_page_career_soup(hitter_entry.baseball_reference_id)
            pregame_hitter_entry = self.mine_career_stats(hitter_entry, pregame_hitter_entry, hitter_career_soup)
            pregame_hitter_entry = self.mine_vs_hand_stats(hitter_entry, pregame_hitter_entry, hitter_career_soup,
                                                           pitcher_hand)
            pregame_hitter_entry = self.mine_recent_stats(hitter_entry, pregame_hitter_entry, hitter_career_soup)
            pregame_hitter_entry = self.mine_season_stats(hitter_entry, pregame_hitter_entry)

            if pitcher_entry is not None:
                pregame_hitter_entry = self.mine_vs_pitcher_stats(hitter_entry, pregame_hitter_entry, pitcher_entry)

            pregame_hitter_entry.game_date = self._game_date
            pregame_hitter_entry.game_time = self._game_time
            try:
                self._database_session.add(pregame_hitter_entry)
                self._database_session.commit()
            except IntegrityError:
                print "Attempt to duplicate hitter entry: %s %s %s" % (current_hitter.name,
                                                                       pregame_hitter_entry.get_team(),
                                                                       pregame_hitter_entry.get_opposing_team())
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
        if pitcher_hand is None:
            return pregame_hitter_entry

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
                try:
                    current_player.name = get_name_from_id(current_player.rotowire_id)
                    if rotowire_team_dict[current_player.team] == "Los Angeles Angels":
                        team = baseball_reference_team_dict.inv["Los Angeles Angels of Anaheim"]
                    else:
                        team = baseball_reference_team_dict.inv[rotowire_team_dict[current_player.team]]

                    baseball_reference_id = get_hitter_id(current_player.name,
                                                          team,
                                                          date.today().year,
                                                          hitter_soup)
                except AttributeError as e:
                    print "Skipping committing this hitter '%s'." % current_player.rotowire_id
                    continue
                except PlayerNameNotFound as e:
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
        yesterdays_date = date.today() - timedelta(days=1)
        hitter_entries = self._database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == str(yesterdays_date))
        for pregame_hitter_entry in hitter_entries:
            hitter_entry = self._database_session.query(HitterEntry).get(pregame_hitter_entry.rotowire_id)
            if hitter_entry is not None:
                stat_row_dict = get_hitting_game_log(hitter_entry.baseball_reference_id, game_date=yesterdays_date)
            else:
                print "Hitter %s not found in database. Deleting entry" % pregame_hitter_entry.rotowire_id
                self._database_session.delete(pregame_hitter_entry)
                self._database_session.commit()
                continue

            if stat_row_dict is None:
                print "Player %s %s did not play yesterday. Deleting pregame entry %s %s" % (hitter_entry.first_name,
                                                                                             hitter_entry.last_name,
                                                                                             pregame_hitter_entry.game_date,
                                                                                             pregame_hitter_entry.get_team())
                self._database_session.delete(pregame_hitter_entry)
                self._database_session.commit()
                continue

            postgame_hitter_entry = PostgameHitterGameEntry()
            postgame_hitter_entry.rotowire_id = hitter_entry.rotowire_id
            postgame_hitter_entry.game_date = pregame_hitter_entry.game_date
            postgame_hitter_entry.game_time = pregame_hitter_entry.game_time
            postgame_hitter_entry.home_team = pregame_hitter_entry.home_team
            postgame_hitter_entry.is_home_team = pregame_hitter_entry.is_home_team
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
        pitcher_entries = self._database_session.query(PregamePitcherGameEntry).filter(PregamePitcherGameEntry.game_date == str(yesterdays_date))
        for pregame_pitcher_entry in pitcher_entries:
            pitcher_entry = self._database_session.query(PitcherEntry).get(pregame_pitcher_entry.rotowire_id)
            if pitcher_entry is not None:
                stat_row_dict = get_pitching_game_log(pitcher_entry.baseball_reference_id, game_date=yesterdays_date)
            else:
                print "Pitcher %s not found in database. Deleting entry" % pregame_pitcher_entry.rotowire_id
                self._database_session.delete(pregame_pitcher_entry)
                self._database_session.commit()
                continue

            if stat_row_dict is None:
                print "Player %s %s did not play yesterday. Deleting pregame entry %s %s" % (pitcher_entry.first_name,
                                                                                             pitcher_entry.last_name,
                                                                                             pregame_pitcher_entry.game_date,
                                                                                             pregame_pitcher_entry.get_team())
                self._database_session.delete(pregame_pitcher_entry)
                self._database_session.commit()
                continue

            postgame_pitcher_entry = PostgamePitcherGameEntry()
            postgame_pitcher_entry.rotowire_id = pitcher_entry.rotowire_id
            postgame_pitcher_entry.game_date = pregame_pitcher_entry.game_date
            postgame_pitcher_entry.game_time = pregame_pitcher_entry.game_time
            postgame_pitcher_entry.home_team = pregame_pitcher_entry.home_team
            postgame_pitcher_entry.is_home_team = pregame_pitcher_entry.is_home_team
            postgame_pitcher_entry.game_ip = float(stat_row_dict["IP"])
            postgame_pitcher_entry.game_so = int(stat_row_dict["SO"])
            if "W" in stat_row_dict["Rslt"]:
                postgame_pitcher_entry.game_wins = 1
            postgame_pitcher_entry.game_er = int(stat_row_dict["ER"])
            postgame_pitcher_entry.game_h = int(stat_row_dict["H"])
            postgame_pitcher_entry.game_bb = int(stat_row_dict["BB"])
            postgame_pitcher_entry.game_hbp = int(stat_row_dict["HBP"])
            if postgame_pitcher_entry.game_ip == 9:
                postgame_pitcher_entry.game_cg = 1
                if int(stat_row_dict["R"]) == 0:
                    postgame_pitcher_entry.game_cgso = 1
                if int(stat_row_dict["H"]) == 0:
                    postgame_pitcher_entry.game_no_hitter = 1
            postgame_pitcher_entry.actual_draftkings_points = get_pitcher_points(postgame_pitcher_entry)
            try:
                self._database_session.add(postgame_pitcher_entry)
                self._database_session.commit()
            except IntegrityError:
                self._database_session.rollback()
                print "Attempt to duplicate pitcher postgame results: %s %s %s %s" % (pitcher_entry.first_name,
                                                                                      pitcher_entry.last_name,
                                                                                      pitcher_entry.team,
                                                                                      pregame_pitcher_entry.game_date)

    def update_lineup_history(self):
        """ Update the lineup history object for this team and year
        :param lineup: list of PlayerStruct objects
        :param database_session: SQLAlchemy session object
        """
        lineup_history_query = self._database_session.query(LineupHistoryEntry).get((date.today().year, self._lineup[0].team))
        if lineup_history_query is None:
            lineup_history = LineupHistoryEntry()
        else:
            lineup_history = lineup_history_query
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
                lineup_history.right_fielder = player.rotowire_id

        try:
            if lineup_history_query is None:
                self._database_session.add(lineup_history)
            self._database_session.commit()
        except IntegrityError:
            self._database_session.rollback()

    def correct_prefetched_lineup(self, db_lineup_query):
        for player in self._lineup:
            for game_player in db_lineup_query:
                if game_player.rotowire_id == player.rotowire_id:
                    break
                #TODO: fix this deletion
#                if game_player == db_lineup_query[db_lineup_query.count()-1]:
#                    self._database_session.delete(game_player)
#                    self._database_session.commit()

    def get_team(self):
        return self._lineup[0].team


class PitcherMiner(object):
    def __init__(self, lineup, pitcher, game_date, game_time, is_home, db_path=None):
        self._lineup = lineup
        self._pitcher = pitcher
        self._database_session = MlbDatabase(db_path).open_session()
        self._game_date = game_date
        self._game_time = game_time
        self._is_home = is_home

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
        home_team = self._lineup[0].team
        if self._is_home:
            home_team = self._pitcher.team
        db_pitcher = self._database_session.query(PregameHitterGameEntry).get((self._pitcher.rotowire_id,
                                                                               self._game_date,
                                                                               self._game_time))
        if db_pitcher is not None:
            print "'%s' has already been mined today." % db_pitcher.rotowire_id
            return

        pregame_pitcher_entry = PregamePitcherGameEntry()
        pregame_pitcher_entry.rotowire_id = self._pitcher.rotowire_id
        pregame_pitcher_entry.team = self._pitcher.team
        pregame_pitcher_entry.game_date = self._game_date
        pregame_pitcher_entry.game_time = self._game_time
        pregame_pitcher_entry.is_home_team = self._is_home
        pregame_pitcher_entry.home_team = home_team

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
                                                                   pregame_pitcher_entry.get_opposing_team())
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
        sql_opposing_lineup = list()
        home_team = self._pitcher.team
        if not self._is_home:
            home_team = self._lineup[0].team
        for lineup_player in self._lineup:
            sql_opposing_lineup.append(self._database_session.query(PregameHitterGameEntry).get((lineup_player.rotowire_id,
                                                                                                 self._game_date,
                                                                                                 self._game_time)))
        for hitter in sql_opposing_lineup:
            try:
                pregame_pitcher_entry.vs_h += hitter.vs_h
                pregame_pitcher_entry.vs_bb += hitter.vs_bb
                pregame_pitcher_entry.vs_so += hitter.vs_so
                pregame_pitcher_entry.vs_hr += hitter.vs_hr
                pregame_pitcher_entry.vs_bf += hitter.vs_pa
                # Approximate earned runs by the RBIs of opposing hitters
                pregame_pitcher_entry.vs_er += hitter.vs_rbi
            except AttributeError:
                continue

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
            try:
                self._pitcher.name = get_name_from_id(self._pitcher.rotowire_id)
                baseball_reference_id = get_pitcher_id(self._pitcher.name,
                                                       baseball_reference_team_dict.inv[rotowire_team_dict[self._pitcher.team]],
                                                       date.today().year,
                                                       pitcher_soup)
            except AttributeError:
                print "Skipping committing this pitcher '%s'." % self._pitcher.rotowire_id
                return
            except PlayerNameNotFound:
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
                stat_row_dict = get_pitching_game_log(pitcher_entry.baseball_reference_id,
                                                      game_date=date.today()-timedelta(days=1))
            except TableRowNotFound:
                print "Player %s %s did not play yesterday. Deleting pregame entry %s %s" % \
                      (pitcher_entry.first_name,
                       pitcher_entry.last_name,
                       pregame_pitcher_entry.game_date,
                       pregame_pitcher_entry.get_opposing_team())

                self._database_session.delete(pregame_pitcher_entry)
                self._database_session.commit()
                continue

            postgame_pitcher_entry = PostgamePitcherGameEntry()
            postgame_pitcher_entry.rotowire_id = pitcher_entry.rotowire_id
            postgame_pitcher_entry.game_date = pregame_pitcher_entry.game_date
            postgame_pitcher_entry.game_time = pregame_pitcher_entry.game_time
            postgame_pitcher_entry.home_team = pregame_pitcher_entry.home_team
            postgame_pitcher_entry.is_home_team = pregame_pitcher_entry.is_home_team
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
                                                                                      pregame_pitcher_entry.get_opposing_team(),
                                                                                      postgame_pitcher_entry.game_date)

    def get_team(self):
        return self._pitcher.team


class GameMiner(object):
    def __init__(self, game, db_path=None):

        self._database_session = MlbDatabase(db_path).open_session()
        self._game = game
        self._home_lineup_miner = LineupMiner(game.home_lineup, game.away_pitcher, game.game_date,
                                              game.game_time, is_home=True, db_path=db_path)
        self._home_pitcher_miner = PitcherMiner(game.away_lineup, game.home_pitcher, game.game_date,
                                                game.game_time, is_home=True, db_path=db_path)
        self._away_lineup_miner = LineupMiner(game.away_lineup, game.home_pitcher, game.game_date,
                                              game.game_time, is_home=False, db_path=db_path)
        self._away_pitcher_miner = PitcherMiner(game.home_lineup, game.away_pitcher, game.game_date,
                                                game.game_time, is_home=False, db_path=db_path)

    def __del__(self):
        self._database_session.close()

    def update_ids(self):
        """ Check if each player is represented in the database. If not, commit a new entry
        :param games: list of Game objects
        """
        self._away_lineup_miner.update_ids()
        self._away_pitcher_miner.update_id()
        self._home_lineup_miner.update_ids()
        self._home_pitcher_miner.update_id()

    def get_pregame_hitting_stats(self):
        away_lineup = self._database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == self._game.game_date,
                                                                                  PregameHitterGameEntry.game_time == self._game.game_time,
                                                                                  PregameHitterGameEntry.home_team == self._game.home_pitcher.team,
                                                                                  PregameHitterGameEntry.is_home_team == False)
        self._away_lineup_miner.correct_prefetched_lineup(away_lineup)
        home_lineup = self._database_session.query(PregameHitterGameEntry).filter(PregameHitterGameEntry.game_date == self._game.game_date,
                                                                                  PregameHitterGameEntry.game_time == self._game.game_time,
                                                                                  PregameHitterGameEntry.home_team == self._game.home_pitcher.team,
                                                                                  PregameHitterGameEntry.is_home_team == True)
        self._home_lineup_miner.correct_prefetched_lineup(home_lineup)
        self._away_lineup_miner.get_pregame_stats()
        self._home_lineup_miner.get_pregame_stats()

    def get_pregame_pitching_stats(self):
        home_pitcher = self._database_session.query(PregamePitcherGameEntry).get((self._game.home_pitcher.rotowire_id,
                                                                                  self._game.game_date,
                                                                                  self._game.game_time))
        if home_pitcher is not None:
            if home_pitcher.rotowire_id != self._game.home_pitcher.rotowire_id:
                self._database_session.delete(home_pitcher)
                self._database_session.commit()
                try:
                    self._home_pitcher_miner.get_pregame_stats()
                except PitcherNotFound:
                    pass
        else:
            try:
                self._home_pitcher_miner.get_pregame_stats()
            except PitcherNotFound:
                pass
        away_pitcher = self._database_session.query(PregamePitcherGameEntry).get((self._game.away_pitcher.rotowire_id,
                                                                                  self._game.game_date,
                                                                                  self._game.game_time))
        if away_pitcher is not None:
            if away_pitcher.rotowire_id != self._game.away_pitcher.rotowire_id:
                self._database_session.delete(away_pitcher)
                self._database_session.commit()
                try:
                    self._away_pitcher_miner.get_pregame_stats()
                except PitcherNotFound:
                    pass
        else:
            try:
                self._away_pitcher_miner.get_pregame_stats()
            except PitcherNotFound:
                pass

    def add_team_park_factors(self):
        team_abbrev = self._home_pitcher_miner.get_team()
        year = datetime.strptime(self._game.game_date, '%Y-%M-%d').year
        # Use the Rotowire team dict so Baseball Reference can work with it
        hitter_factor, pitcher_factor = get_team_info(baseball_reference_team_dict[team_abbrev], year)
        park_entry = ParkEntry(team_abbrev, year)
        park_entry.park_hitter_score = hitter_factor
        park_entry.park_pitcher_score = pitcher_factor
        try:
            self._database_session.add(park_entry)
            self._database_session.commit()
        except IntegrityError:
            self._database_session.rollback()

    def update_park_factors(self):
        game_date = datetime.strptime(self._game.game_date, '%Y-%M-%d')
        park_factors = self._database_session.query(ParkEntry).get((self._home_pitcher_miner.get_team(),
                                                                    game_date.year-1))
        if park_factors is None:
            self.add_team_park_factors()


class UmpireMiner(object):
    def __init__(self, db_path=None):
        if db_path is None:
            db_path = 'sqlite:///mlb_stats.db'
        else:
            db_path = 'sqlite:///' + db_path

        self._database_session = MlbDatabase(db_path).open_session()

    def __del__(self):
        self._database_session.close()

    def mine_umpire_data(self):
        url = "https://swishanalytics.com/mlb/mlb-umpire-factors"
        umpire_soup = get_soup_from_url(url)

        stat_table = umpire_soup.find("table", {"id": "ump-table"}).find("tbody")

        if stat_table is not None:
            ump_rows = stat_table.findAll("tr")
            for ump_row in ump_rows:
                ump_data = ump_row.findAll("td")
                ump_entry = self._database_session.query(UmpireCareerEntry).get(str(ump_data[0].text.strip()))
                if ump_entry is None:
                    ump_entry = UmpireCareerEntry(str(ump_data[0].text.strip()))

                ump_entry.ks_pct = float(ump_data[3].text.strip().replace("%", "")) / 100
                ump_entry.walks_pct = float(ump_data[4].text.strip().replace("%", "")) / 100
                ump_entry.runs_per_game = float(ump_data[5].text.strip())
                ump_entry.batting_average = float(ump_data[6].text.strip())
                ump_entry.on_base_pct = float(ump_data[7].text.strip())
                ump_entry.slugging_pct = float(ump_data[8].text.strip())

                ump_entry.ks_boost = float(ump_data[9].text.strip().replace("x", ""))
                ump_entry.walks_boost = float(ump_data[10].text.strip().replace("x", ""))
                ump_entry.runs_boost = float(ump_data[11].text.strip().replace("x", ""))
                ump_entry.batting_average_boost = float(ump_data[12].text.strip().replace("x", ""))
                ump_entry.on_base_pct_boost = float(ump_data[13].text.strip().replace("x", ""))
                ump_entry.slugging_pct_boost = float(ump_data[14].text.strip().replace("x", ""))

                try:
                    self._database_session.add(ump_entry)
                    self._database_session.commit()
                except IntegrityError:
                    self._database_session.rollback()