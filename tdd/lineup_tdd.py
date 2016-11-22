

from sql.lineup import LineupEntry
from sql.hitter_entry import HitterEntry
from sql.pitcher_entry import PitcherEntry
import unittest
from sql.mlb_database import MlbDatabase
from datetime import date
import os

DB_PATH = "test_db.db"


def add_hitter_entries():
    """ Just add some hitter entries to the test database to satisfy foreign key constraints
    """
    database_session = MlbDatabase(DB_PATH).open_session()

    catcher = HitterEntry('Russell', 'Martin', '8047')
    database_session.add(catcher)
    first_baseman = HitterEntry('Ryan', 'Zimmerman', '8620')
    database_session.add(first_baseman)
    second_baseman = HitterEntry('Chase', 'Utley', '6508')
    database_session.add(second_baseman)
    third_baseman = HitterEntry('Josh', 'Donaldson', '9862')
    database_session.add(third_baseman)
    shortstop = HitterEntry('Manny', 'Machado', '11437')
    database_session.add(shortstop)
    outfielder_1 = HitterEntry('Melvin', 'Upton Jr.', '7140')
    database_session.add(outfielder_1)
    outfielder_2 = HitterEntry('Jose', 'Peraza', '13190')
    database_session.add(outfielder_2)
    outfielder_3 = HitterEntry('Nick', 'Markakis', '7618')
    database_session.add(outfielder_3)

    database_session.commit()
    database_session.close()


def add_pitcher_entries():
    database_session = MlbDatabase(DB_PATH).open_session()

    starting_pitcher_1 = PitcherEntry('Andrew', 'Cashner', '10468')
    database_session.add(starting_pitcher_1)
    starting_pitcher_2 = PitcherEntry('Jeff', 'Samardzija', '9374')
    database_session.add(starting_pitcher_2)

    database_session.commit()
    database_session.close()


class CommitNewLineupTest(unittest.TestCase):

    def setUp(self):
        try:
            os.remove(DB_PATH)
        except OSError:
            pass
        add_hitter_entries()
        add_pitcher_entries()

    def runTest(self):
        database_session = MlbDatabase(DB_PATH).open_session()

        lineup = LineupEntry()
        lineup.starting_pitcher_1 = '10468'
        lineup.starting_pitcher_2 = '9374'
        lineup.catcher = '8047'
        lineup.first_baseman = '8620'
        lineup.second_baseman = '6508'
        lineup.third_baseman = '9862'
        lineup.shortstop = '11437'
        lineup.outfielder_1 = '7140'
        lineup.outfielder_2 = '13190'
        lineup.outfielder_3 = '7618'
        lineup.game_date = date.today()
        lineup.game_time = date.today().ctime()

        database_session.add(lineup)
        database_session.commit()

        database_session.close()

    def tearDown(self):
        os.remove(DB_PATH)


def suite():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(CommitNewLineupTest)
    return test_suite
