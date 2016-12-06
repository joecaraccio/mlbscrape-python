

from sql.pitcher_entry import PitcherEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
from sql.hitter_entry import HitterEntry
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.game import GameEntry
from mine.stat_miner import *
import unittest
from sql.mlb_database import MlbDatabase
from datetime import date
import os

DB_PATH = "test_db.db"


def add_pitcher_entry():
    database_session = MlbDatabase(DB_PATH).open_session()

    starting_pitcher_1 = PitcherEntry('Andrew', 'Cashner', '10468')
    starting_pitcher_1.baseball_reference_id = 'cashnan01'
    starting_pitcher_1.team = 'MIA'
    starting_pitcher_1.pitching_hand = 'R'

    database_session.add(starting_pitcher_1)
    database_session.commit()

    database_session.close()


def add_hitter_postgame_entry():

    database_session = MlbDatabase(DB_PATH).open_session()

    entry = GameEntry('2016-08-21', '15:00', 'TOR', 'MIA')
    database_session.add(entry)
    database_session.commit()

    add_pitcher_entry()

    catcher = HitterEntry('Russell', 'Martin', '8047')
    database_session.add(catcher)
    database_session.commit()

    catcher_postgame_entry = PostgameHitterGameEntry()
    catcher_postgame_entry.rotowire_id = '8047'
    catcher_postgame_entry.pitcher_id = '10468'
    catcher_postgame_entry.game_date = "2016-08-21"
    catcher_postgame_entry.game_time = "15:00"
    catcher_postgame_entry.actual_draftkings_points = 10

    database_session.add(catcher_postgame_entry)
    database_session.commit()

    entry = GameEntry('2016-07-21', '15:00', 'TOR', 'MIA')
    database_session.add(entry)
    database_session.commit()

    catcher_postgame_entry = PostgameHitterGameEntry()
    catcher_postgame_entry.rotowire_id = '8047'
    catcher_postgame_entry.pitcher_id = '10468'
    catcher_postgame_entry.game_date = "2016-07-21"
    catcher_postgame_entry.game_time = "15:00"
    catcher_postgame_entry.actual_draftkings_points = 2

    database_session.add(catcher_postgame_entry)
    database_session.commit()

    database_session.close()


def add_pitcher_postgame_entry():

    database_session = MlbDatabase(DB_PATH).open_session()

    entry = GameEntry('2016-08-21', '15:00', 'TOR', 'MIA')
    database_session.add(entry)
    database_session.commit()

    add_pitcher_entry()

    pitcher_postgame_entry = PostgamePitcherGameEntry()
    pitcher_postgame_entry.rotowire_id = '10468'
    pitcher_postgame_entry.game_date = "2016-08-21"
    pitcher_postgame_entry.game_time = "15:00"
    pitcher_postgame_entry.actual_draftkings_points = 10

    database_session.add(pitcher_postgame_entry)
    database_session.commit()

    entry = GameEntry('2016-07-18', '15:00', 'TOR', 'MIA')
    database_session.add(entry)
    database_session.commit()

    pitcher_postgame_entry = PostgamePitcherGameEntry()
    pitcher_postgame_entry.rotowire_id = '10468'
    pitcher_postgame_entry.game_date = "2016-07-18"
    pitcher_postgame_entry.game_time = "15:00"
    pitcher_postgame_entry.actual_draftkings_points = 4

    database_session.add(pitcher_postgame_entry)
    database_session.commit()

    database_session.close()


class AveragePointsHitterTest(unittest.TestCase):

    def setUp(self):
        add_hitter_postgame_entry()

    def runTest(self):
        database_session = MlbDatabase(DB_PATH).open_session()

        points = get_avg_hitter_points('8047', '2016', database_session)

        self.assertEqual(points, 6.0)

    def tearDown(self):
        os.remove(DB_PATH)


class AveragePointsPitcherTest(unittest.TestCase):

    def setUp(self):
        add_pitcher_postgame_entry()

    def runTest(self):
        database_session = MlbDatabase(DB_PATH).open_session()

        points = get_avg_pitcher_points('10468', '2016', database_session)

        self.assertEqual(points, 7.0)

    def tearDown(self):
        os.remove(DB_PATH)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(AveragePointsHitterTest())
    test_suite.addTest(AveragePointsPitcherTest())
    return test_suite
