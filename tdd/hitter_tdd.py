
from sql.pitcher_entry import PitcherEntry
from sql.hitter_entry import HitterEntry
from sql.pregame_hitter import PregameHitterGameEntry
from sql.postgame_hitter import PostgameHitterGameEntry
from sql.game import GameEntry
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


def add_hitter_entry():
    database_session = MlbDatabase(DB_PATH).open_session()

    hitter = HitterEntry('Wil', 'Myers', '10972')
    hitter.baseball_reference_id = 'myerswi01'
    hitter.team = 'SD'
    hitter.batting_hand = 'R'

    database_session.add(hitter)
    database_session.commit()

    database_session.close()


class CommitNewHitterTest(unittest.TestCase):

    def runTest(self):
        add_hitter_entry()

    def tearDown(self):
        os.remove(DB_PATH)


class CommitNewPregameHitterTest(unittest.TestCase):

    def setUp(self):
        add_hitter_entry()
        add_pitcher_entry()
        database_session = MlbDatabase(DB_PATH).open_session()
        entry = GameEntry(date.today(), date.today().ctime(), 'SD', 'BOS')
        database_session.add(entry)
        database_session.commit()

        database_session.close()

    def runTest(self):
        database_session = MlbDatabase(DB_PATH).open_session()

        entry = PregameHitterGameEntry()
        entry.rotowire_id = '10972'
        entry.game_date = date.today()
        entry.game_time = date.today().ctime()

        database_session.add(entry)
        database_session.commit()

        database_session.close()

    def tearDown(self):
        os.remove(DB_PATH)


class CommitNewPostgameHitterTest(unittest.TestCase):

    def setUp(self):
        add_hitter_entry()
        add_pitcher_entry()
        database_session = MlbDatabase(DB_PATH).open_session()

        entry = GameEntry(date.today(), date.today().ctime(), 'SD', 'BOS')
        database_session.add(entry)
        database_session.commit()

        database_session.close()

    def runTest(self):
        database_session = MlbDatabase(DB_PATH).open_session()

        entry = PostgameHitterGameEntry()
        entry.rotowire_id = '10972'

        database_session.close()

    def tearDown(self):
        os.remove(DB_PATH)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(CommitNewHitterTest())
    test_suite.addTest(CommitNewPregameHitterTest())
    test_suite.addTest(CommitNewPostgameHitterTest())
    return test_suite
