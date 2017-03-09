

from sql.pitcher_entry import PitcherEntry
from sql.pregame_pitcher import PregamePitcherGameEntry
from sql.postgame_pitcher import PostgamePitcherGameEntry
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
    starting_pitcher_1.home_team = 'MIA'
    starting_pitcher_1.pitching_hand = 'R'

    database_session.add(starting_pitcher_1)
    database_session.commit()

    database_session.close()


class CommitNewPitcherTest(unittest.TestCase):

    def runTest(self):
        database_session = MlbDatabase(DB_PATH).open_session()

        starting_pitcher_1 = PitcherEntry('Andrew', 'Cashner', '10468')
        starting_pitcher_1.baseball_reference_id = 'cashnan01'
        starting_pitcher_1.home_team = 'MIA'
        starting_pitcher_1.pitching_hand = 'R'

        database_session.add(starting_pitcher_1)
        database_session.commit()

        database_session.close()

    def tearDown(self):
        os.remove(DB_PATH)


class CommitNewPregamePitcherTest(unittest.TestCase):

    HOME_TEAM = 'BOS'

    def setUp(self):
        add_pitcher_entry()
        database_session = MlbDatabase(DB_PATH).open_session()
        entry = GameEntry(date.today(), date.today().ctime(), CommitNewPregamePitcherTest.HOME_TEAM, 'MIA')
        database_session.add(entry)
        database_session.commit()

        database_session.close()

    def runTest(self):
        database_session = MlbDatabase(DB_PATH).open_session()

        entry = PregamePitcherGameEntry()
        entry.rotowire_id = '10468'
        entry.game_date = date.today()
        entry.game_time = date.today().ctime()
        entry.home_team = CommitNewPregamePitcherTest.HOME_TEAM

        database_session.add(entry)
        database_session.commit()

        database_session.close()

    def tearDown(self):
        os.remove(DB_PATH)


class CommitNewPostgamePitcherTest(unittest.TestCase):

    def setUp(self):
        add_pitcher_entry()
        database_session = MlbDatabase(DB_PATH).open_session()

        entry = GameEntry(date.today(), date.today().ctime(), CommitNewPregamePitcherTest.HOME_TEAM, 'MIA')
        database_session.add(entry)
        database_session.commit()

        database_session.close()

    def runTest(self):
        database_session = MlbDatabase(DB_PATH).open_session()

        entry = PostgamePitcherGameEntry()
        entry.rotowire_id = '10468'
        entry.game_date = date.today()
        entry.game_time = date.today().ctime()
        entry.home_team = CommitNewPregamePitcherTest.HOME_TEAM

        database_session.close()

    def tearDown(self):
        os.remove(DB_PATH)


def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(CommitNewPitcherTest())
    test_suite.addTest(CommitNewPregamePitcherTest())
    test_suite.addTest(CommitNewPostgamePitcherTest())
    return test_suite
