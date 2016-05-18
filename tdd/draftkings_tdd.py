
import unittest
from mlbscrape_python.mine.draft_kings import Draftkings
from mlbscrape_python.mine.draft_kings import OptimalLineupDict
from mlbscrape_python.sql.pregame_hitter import PregameHitterGameEntry
from mlbscrape_python.sql.pregame_pitcher import PregamePitcherGameEntry


class OptimalLineupTest(unittest.TestCase):
    """ Base class used to initialize the optimal lineup before operating on it
    """
    OPTIMAL_LINEUP_SP1_ID = "1"
    OPTIMAL_LINEUP_SP1_SALARY = 10000
    OPTIMAL_LINEUP_SP1_POINTS = 23.5

    OPTIMAL_LINEUP_SP2_ID = "2"
    OPTIMAL_LINEUP_SP2_SALARY = 8500
    OPTIMAL_LINEUP_SP2_POINTS = 19.8

    OPTIMAL_LINEUP_C_ID = "3"
    OPTIMAL_LINEUP_C_SALARY = 3000
    OPTIMAL_LINEUP_C_POINTS = 8

    OPTIMAL_LINEUP_1B_ID = "4"
    OPTIMAL_LINEUP_1B_SALARY = 5800
    OPTIMAL_LINEUP_1B_POINTS = 12

    OPTIMAL_LINEUP_2B_ID = "5"
    OPTIMAL_LINEUP_2B_SALARY = 4800
    OPTIMAL_LINEUP_2B_POINTS = 10

    OPTIMAL_LINEUP_3B_ID = "6"
    OPTIMAL_LINEUP_3B_SALARY = 5600
    OPTIMAL_LINEUP_3B_POINTS = 15

    OPTIMAL_LINEUP_SS_ID = "7"
    OPTIMAL_LINEUP_SS_SALARY = 5500
    OPTIMAL_LINEUP_SS_POINTS = 14

    OPTIMAL_LINEUP_OF1_ID = "8"
    OPTIMAL_LINEUP_OF1_SALARY = 7200
    OPTIMAL_LINEUP_OF1_POINTS = 17

    OPTIMAL_LINEUP_OF2_ID = "9"
    OPTIMAL_LINEUP_OF2_SALARY = 6500
    OPTIMAL_LINEUP_OF2_POINTS = 15

    OPTIMAL_LINEUP_OF3_ID = "10"
    OPTIMAL_LINEUP_OF3_SALARY = 6000
    OPTIMAL_LINEUP_OF3_POINTS = 13

    def setUp(self):
        self.optimal_lineup = OptimalLineupDict()
        player = PregameHitterGameEntry()
        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_SP1_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_SP1_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_SP1_POINTS
        player.primary_position = "SP"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_SP2_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_SP2_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_SP2_POINTS
        player.primary_position = "SP"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_C_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_C_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_C_POINTS
        player.primary_position = "C"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_1B_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_1B_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_1B_POINTS
        player.primary_position = "1B"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_2B_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_2B_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_2B_POINTS
        player.primary_position = "2B"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_3B_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_3B_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_3B_POINTS
        player.primary_position = "3B"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_SS_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_SS_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_SS_POINTS
        player.primary_position = "SS"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_OF1_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_OF1_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_OF1_POINTS
        player.primary_position = "OF"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_OF2_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_OF2_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_OF2_POINTS
        player.primary_position = "OF"
        self.optimal_lineup.add(player)

        player.rotowire_id = OptimalLineupTest.OPTIMAL_LINEUP_OF3_ID
        player.draftkings_salary = OptimalLineupTest.OPTIMAL_LINEUP_OF3_SALARY
        player.predicted_draftkings_points = OptimalLineupTest.OPTIMAL_LINEUP_OF3_POINTS
        player.primary_position = "OF"
        self.optimal_lineup.add(player)


class TestTotalSalaryInitial(OptimalLineupTest):
    """ Test to just make sure the total salary is calculated correctly when initializing the lineup
    """

    def runTest(self):
        total_salary = OptimalLineupTest.OPTIMAL_LINEUP_SP1_SALARY + OptimalLineupTest.OPTIMAL_LINEUP_SP2_SALARY + \
                       OptimalLineupTest.OPTIMAL_LINEUP_C_SALARY + OptimalLineupTest.OPTIMAL_LINEUP_1B_SALARY + \
                       OptimalLineupTest.OPTIMAL_LINEUP_2B_SALARY + OptimalLineupTest.OPTIMAL_LINEUP_3B_SALARY + \
                       OptimalLineupTest.OPTIMAL_LINEUP_SS_SALARY + OptimalLineupTest.OPTIMAL_LINEUP_OF1_SALARY + \
                       OptimalLineupTest.OPTIMAL_LINEUP_OF2_SALARY + OptimalLineupTest.OPTIMAL_LINEUP_OF3_SALARY

        self.assertEqual(self.optimal_lineup.get_total_salary(), total_salary)


class TestAddOutfielder(OptimalLineupTest):
    """ Test of a SS where the candidate SS is a better deal than the
    """
    CANDIDATE_ID = "9999"
    CANDIDATE_PRIMARY_POS = "SS"
    CANDIDATE_SECONDARY_POS = "3B"
    CANDIDATE_POINTS = 10
    CANDIDATE_SALARY = 3000

    def runTest(self):
        player = PregameHitterGameEntry()
        player.rotowire_id = TestAddOutfielder.CANDIDATE_ID
        player.primary_position = TestAddOutfielder.CANDIDATE_PRIMARY_POS
        player.secondary_position = TestAddOutfielder.CANDIDATE_SECONDARY_POS
        player.predicted_draftkings_points = TestAddOutfielder.CANDIDATE_POINTS
        player.draftkings_salary = TestAddOutfielder.CANDIDATE_SALARY
        self.optimal_lineup.add(player)
        self.assertTrue(self.optimal_lineup[TestAddOutfielder.CANDIDATE_PRIMARY_POS].rotowire_id,
                        TestAddOutfielder.CANDIDATE_ID)


class GetSalariesTest(unittest.TestCase):
    """ Test case for testing the methods of getting the salaries for Draftkings
    """
    def test_pitcher_typical(self):
        CSV_LOCATION = "players.csv"
        NAME = "Felix Hernandez"
        TEAM = "Sea"

        csv_dict = Draftkings.get_csv_dict(CSV_LOCATION)
        try:
            csv_entry = csv_dict[NAME.lower() + TEAM.lower()]
        except KeyError:
            self.assertTrue(False)

        self.assertEqual(int(csv_entry["Salary"]), 10400)

    def test_hitter_typical(self):
        CSV_LOCATION = "players.csv"
        NAME = "Jon Jay"
        TEAM = "SD"

        csv_dict = Draftkings.get_csv_dict(CSV_LOCATION)
        try:
            csv_entry = csv_dict[NAME.lower() + TEAM.lower()]
        except KeyError:
            self.assertTrue(False)

        self.assertEqual(int(csv_entry["Salary"]), 2700)


def suite():
    test_suite = unittest.TestLoader().loadTestsFromTestCase(GetSalariesTest)
    test_suite.addTest(TestTotalSalaryInitial())
    test_suite.addTest(TestAddOutfielder())
    return test_suite
